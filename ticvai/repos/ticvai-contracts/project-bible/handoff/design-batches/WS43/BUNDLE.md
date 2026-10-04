# WS43 — Product Lifecycle   Catalogue Governance board 1

**10 screens · 11 operations · 26 schemas · 2 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-118` | Product Lifecycle Command Center | B | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `ADM-119` | Product Creation Workspace | B | 0 | 0 | 6 | 25 | 8 | 3 | — | notStarted (generated) |
| `ADM-120` | Lifecycle Status & Workflow Configuration | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-121` | Bulk Product Creation & Catalogue Import | B–D | 0 | 0 | 6 | 0 | 2 | 3 | — | notStarted (generated) |
| `ADM-122` | Product Import / Export & Environment Transfer | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-123` | Product Context, Ownership & Assignment | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-124` | Channel Publication & Availability | B | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-125` | Publication & Activation Scheduler | B | 11 | 19 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-126` | Product Duplication & Template Library | B | 26 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-127` | AI Catalogue Builder & Configuration Review | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-118, ADM-119, ADM-120, ADM-121, ADM-122, ADM-123, ADM-124, ADM-125, ADM-127 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-118` Product Lifecycle Command Center

**Provide administrators with a centralized operational view of every product and its current lifecycle state.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-118 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-lifecycle-command-center-adm-118` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every product and its lifecycle state, counted and filterable by venue and department, the hub of the product governance board. Every product is authorised before it sells.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product type | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProductLifecycle` ?productType |
| Location | picker: choose a location | — | — | `listProductLifecycle` ?locationId |
| Lifecycle state | select | — | Draft · In review · Approved · Live · Withdrawn · Archived | `listProductLifecycle` ?lifecycleState |
| Owner | text field | — | — | `listProductLifecycle` ?owner |
| Department | text field | — | — | `listProductLifecycle` ?department |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listProductLifecycle` ?channel |
| Effective on | date picker | — | — | `listProductLifecycle` ?effectiveOn |
| Created from | date picker | — | — | `listProductLifecycle` ?createdFrom |
| Created to | date picker | — | — | `listProductLifecycle` ?createdTo |
| Modified since | date picker | — | — | `listProductLifecycle` ?modifiedSince |
| Search | text field | — | — | `listProductLifecycle` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **state counts**: Draft, In review, Approved, Live, Withdrawn, Archived as filter cards; the visual workflow draft to live beneath. *(source: contracts/spine/catalogue.yaml#listProductLifecycle / DI-438 / DI-577)*

**Data it reads**: `listProductLifecycle` (onLoad, Product Lifecycle Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-119` Product Creation Workspace: *Works in Product Creation Workspace*; calls `listProductLifecycle`
- → `ADM-120` Lifecycle Status & Workflow Configuration: *Works in Lifecycle Status & Workflow Configuration*; calls `listProductLifecycle`
- → `ADM-122` Product Import / Export & Environment Transfer: *Works in Product Import / Export & Environment Transfer*; calls `listProductLifecycle`
- → `ADM-123` Product Context, Ownership & Assignment: *Works in Product Context, Ownership & Assignment*; calls `listProductLifecycle`
- → `ADM-124` Channel Publication & Availability: *Works in Channel Publication & Availability*; calls `listProductLifecycle`
- → `ADM-125` Publication & Activation Scheduler: *Works in Publication & Activation Scheduler*; calls `listProductLifecycle`
- → `ADM-126` Product Duplication & Template Library: *Works in Product Duplication & Template Library*; calls `listProductLifecycle`
- → `ADM-127` AI Catalogue Builder & Configuration Review: *Works in AI Catalogue Builder & Configuration Review*; calls `listProductLifecycle`
- → `ADM-121` Bulk Product Creation & Catalogue Import: *Works in Bulk Product Creation & Catalogue Import, a section of BO-117, which saves the record with…*; calls `listProductLifecycle`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product lifecycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-007`: Same states and badges as the venue directory.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
counts:
  draft: 14
  inReview: 6
  approved: 3
  live: 212
  withdrawn: 9
```

#### Permissions

- `listProductLifecycle` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product lifecycle dashboard shows counts of products in draft, in approval and published, filterable by venue/department; every product must be authorised before publishing online or on-site. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-438)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-118` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-118`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 1: Opens Product Lifecycle Command Center → Provide administrators with a centralized operational view of every product and its current lifecycle state.
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F152 branch at step 1 (expected): when Nothing has been set up on Product Lifecycle Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F152 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-118?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-119`, `ADM-120`, `ADM-122`, `ADM-123`, `ADM-124`, `ADM-125`, `ADM-126`, `ADM-127`, `ADM-121`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-119` Product Creation Workspace

**Provide a governed starting point for creating a new ticketing product. (a section of BO-007 Product Directory since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-119 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/product-directory/product-creation-workspace-adm-119` |

**What the spec says about it.** **Merged into BO-007 Product Directory as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-007: it renders inside BO-007's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The governed starting point for a new product: the four creation paths (from scratch, from a template, clone, import) and the AI assistant, then the basic information, kind first.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createProduct and nothing that returns the current configuration. (CHG-MOV-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kind**: Chosen first with the six core ticket types the client named (open-dated, group and family, membership, event, gift voucher, money card) mapped to product kinds. *(source: DI-433 / contracts/spine/catalogue.yaml#/components/schemas/ProductKind)*
- **code**: Unique across the tenant (R108). *(source: contracts/spine/catalogue.yaml#createProduct / R108)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `createProduct`
- → `BO-007` Product Directory: *Open Product Directory*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product creation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product creation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product creation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product creation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or … |

#### Consistency with other screens

- Match `BO-007`: Same "New product" paths as on the venue directory.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
product:
  name: Twilight Ticket
  nameAr: تذكرة الغروب
  code: AQUA-TWILIGHT
  kind: timedAdmission
  venue: Coastal Aqua
```

#### Permissions

- `createProduct` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.21 | VIP Package Purchases - System shall support VIP package purchases. | Guest Mobile App & Branding | CONTRACTED | `createProduct` |
| 1.1.1 | The system should be able to sell open-dated tickets for attractions. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.6 | The system should be able to sell membership passes for an attraction (e.g. annual pass, monthly pass) for configurable duration. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.8 | The system should be able to sell add-on items for all type of tickets. Add-ons can also be configured as a stand-alone product and able to be purchased on their own. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.42 | Configure unlimited ticket products and categories | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.44 | Support admission, membership, voucher, package and pass products | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.93 | Membership product management | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.124 | Channel-based restrictions | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.3.52 | Wall climbing activities (product management, sales, ticketing, bookings). | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.4.5 | System shall support creation and maintenance of products in Draft status without exposing them to sales channels. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 4.6.8 | The system should be able to allow sale of special items which are added for use by a group/school visit or special guest type. | Bundles and Promotions | CONTRACTED | `createProduct` |
| 7.3.4 | Use predefined naming schema and code format (e.g., [ParkCode]-[ProductType]-[Variant]). | F&B POS | CONTRACTED | `createProduct` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: all policy types — reschedule, exchange, refund, cancellation, upgrade/downgrade, ownership transfer, membership-to-pass conversion — are managed centrally within the unified product configuration, not separate screens. Each product also maps pricing, GL account code, promotions and channel availability. *(agreed · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 5. Key Decisions · DI-466)*
- Decision: special product types — group (min/max size, single or multiple QR codes), family (min/max composition) and corporate/allocation tickets — are configured within the same unified product configuration screen, not separate screens. *(agreed · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships; 5. Key Decisions · DI-465)*
- Products are classified by configurable components (e.g. resident/non-resident → standard/VIP tier → adult/child/youth), not a fixed structure; components can be added and a simple venue may use only guest category. Tickets can be anonymous or require captured guest details. *(client request · MoM 25 Aug 2026, 4.4 Product Combination Matrix & Ownership · DI-450)*
- Content localisation: separate content (images, descriptions) per sales channel (POS vs. B2C/B2B) and per language (e.g. English/Arabic). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-442)*
- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*
- Six core ticket types: Open-Dated (no fixed date; GA and B2B/travel-agent QR resale), Group & Family (configurable group size, single-scan or multi-scan QR), Membership/Subscription (full details per member; renew/upgrade/cancel), Event (date/time selection, resources, capacity), Gift Voucher, Money Card. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-433)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker · keyword 'ticket type')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-119` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-119`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 2: Works in Product Creation Workspace → Provide a governed starting point for creating a new ticketing product.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-119?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Cancel.
- [ ] Every transition is wired: `ADM-118`, `BO-007`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-120` Lifecycle Status & Workflow Configuration

**Configure how products move between lifecycle states.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-120 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/lifecycle-status-workflow-configuration-adm-120` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of the lifecycle status workflow (setLifecycleStatuWorkflow has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which lifecycle statuses are used, which transitions are allowed, and what may be edited in each status.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Configurable statuses contradict the fixed ProductLifecycleState enum that transitionProductLifecycle moves along. (CHG-MOV-008)
- The operation is named setLifecycleStatuWorkflow (typo). (CHG-MOV-008)
- No read operation: the screen declares only setLifecycleStatuWorkflow and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **transitions**: A state diagram with allowed arrows toggled; edit permissions per status as a matrix. *(source: contracts/spine/catalogue.yaml#setLifecycleStatuWorkflow)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `setLifecycleStatuWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lifecycle status workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lifecycle status workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lifecycle status workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the lifecycle status workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  status: Live
  editable:
  - description
  - media
  locked:
  - price
  - entitlement
```

#### Permissions

- `setLifecycleStatuWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-120` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-120`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 4: Works in Lifecycle Status & Workflow Configuration → Configure how products move between lifecycle states.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-120?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-121` Bulk Product Creation & Catalogue Import

**Allow large catalogues to be created efficiently rather than configuring every product manually. This directly addresses the matrix requirement for catalogue creation through bulk-file upload. (a section of BO-117 Product Import, Governance & AI Configuration Assistant since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/product-import-governance-ai-configuration-assistant/bulk-product-creation-catalogue-import-adm-121` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `createBulkProductCatalogue` duplicated BO-117 Product Import, Governance & AI Configuration Assistant's importProductCatalogue and commitCatalogueImport, so it is removed from the contract (BC-010) and BO-117 saves this record. This id stays the anchor of its section of BO-117: nothing on it writes separately. **Merged into BO-117 Product Import, Governance & AI Configuration Assistant as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-117: it renders inside BO-117's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Create a large catalogue from a file (Excel, CSV, template, catalogue file, PDF brochure, product document): map columns, validate, correct or exclude rows, then commit. Every created product is a draft; nothing the import or the AI proposes is live.

**Fixed on main** (the package already carries these; draw what it says): createBulkProductCatalogue is a second catalogue-import operation beside importProductCatalogue and commitCatalogueImport. (CHG-CLN-001); No read operation: the screen declares only createBulkProductCatalogue and nothing that returns the current configuration. (CHG-MOV-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **columnMapping**: Source columns on the left, TICVAI fields on the right, with required fields marked and auto-matched where names match. *(source: contracts/spine/catalogue.yaml#/components/schemas/BulkProductCreationCatalogueImportInput)*
- **rowCorrections and excludedRows**: Edit a failing row inline and re-validate, or exclude it; the counts update. *(source: contracts/spine/catalogue.yaml#/components/schemas/BulkProductCreationCatalogueImportInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Download error report**: A file of failing rows with the reason per row. *(source: contracts/spine/catalogue.yaml#/components/schemas/BulkProductCreationCatalogueImportInput)*

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*
- → `BO-117` Product Import, Governance & AI Configuration Assistant: *Open Product Import, Governance & AI Configuration Assistant*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bulk product creation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bulk product creation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved yet. The create action is BO-117's (importProductCatalogue and commitCatalogueImport); this section offers none of its own. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bulk product creation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-117 Product Import, Governance & AI Configuration Assistant requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-117`: The venue's import on P08 is the same two-phase job (preview, findings, commit); same layout.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  file: coastal-aqua-2027-catalogue.xlsx
  target: Coastal Aqua
  parsed: 340
  failed: 6
  template: Water park admission template
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-117 Product Import, Governance & AI Configuration Assistant requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker · keyword 'ticket type')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-121` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-121`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 6: Works in Bulk Product Creation & Catalogue Import, a section of BO-117, which saves the record with … → Allow large catalogues to be created efficiently rather than configuring every product manually. This directly addresses the matrix requirement for catalogue creation through bulk-file upload.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-121?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Cancel.
- [ ] Every transition is wired: `ADM-118`, `BO-117`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-122` Product Import / Export & Environment Transfer

**Allow controlled movement of product configurations between TICVAI environments. This covers the matrix requirement for importing/exporting catalogue products between different environments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-122 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-import-export-environment-transfer-adm-122` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Move product configuration between environments (development, sandbox, UAT, staging, production): export, import, reference mapping, missing references.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **After go-live, is configuration promoted from pre-production to production only as configuration?** → Industry standard for production change: never merge or reverse-migrate production databases. Schema goes forward-only through versioned migrations (expand then contract). Configuration moves as a versioned package exported with stable keys, diffed against production, approved, applied as an idempotent upsert by key, and audited; rollback re-applies the previous package. Secrets and environment settings never travel in it. *(decided by Chinmay, 2026-10-02; DEC-168 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Direction | segmented control | — | Export · Import | `listProductImportExport` ?direction |
| Environment | radio group | — | Development · Sandbox · Uat · Staging · Production | `listProductImportExport` ?environment |
| Status | text field | — | — | `listProductImportExport` ?status |
| Search | text field | — | — | `listProductImportExport` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **transfer jobs**: Direction, source and target environment, products, missing references, status. *(source: contracts/spine/catalogue.yaml#listProductImportExport)*
- **How production changes**: Never merge or reverse-migrate a production database. Schema goes forward only, through versioned migrations (expand, then contract). Configuration moves as a versioned package exported with stable keys, diffed against production, approved, applied as an idempotent upsert by key and audited; rollback re-applies the previous package. Secrets and environment settings never travel in it. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-006))*

**Data it reads**: `listProductImportExport` (onLoad, Product Import / Export & Environment Transfer)

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `listProductImportExport`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product import export list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product import export untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product import export yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product import export are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  direction: import
  from: uat
  to: production
  products: 18
  missingReferences:
  - tax profile AE-VAT-5
```

#### Permissions

- `listProductImportExport` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-122` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-122`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 8: Works in Product Import / Export & Environment Transfer → Allow controlled movement of product configurations between TICVAI environments. This covers the matrix requirement for importing/exporting catalogue products between different environments.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-122?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-123` Product Context, Ownership & Assignment

**Define where the product belongs and who is responsible for it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-123 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-context-ownership-assignment-adm-123` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of product context and ownership assignments.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a product belongs and who answers for it: business unit, legal entity, venue, attraction, event, site, location, owner, responsible department, operational and customer contacts.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setProductContextOwnership and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **ownership**: Owner and department as people and department pickers; legal entity drives which ledger books it. *(source: contracts/spine/catalogue.yaml#setProductContextOwnership)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `setProductContextOwnership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product context ownership list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product context ownership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product context ownership yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product context ownership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
context:
  product: Day Pass
  legalEntity: Dune Park LLC
  owner: Layla Hassan
  department: Ticketing
```

#### Permissions

- `setProductContextOwnership` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-123` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-123`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 10: Works in Product Context, Ownership & Assignment → Define where the product belongs and who is responsible for it.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-123?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-124` Channel Publication & Availability

**Control where a product may be exposed for sale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-124 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/channel-publication-availability-adm-124` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of what is published to which channel (publishChannelAvailability has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a product may be exposed for sale: per channel, the sites, POS groups and venues and effective dates, with a preview and missing dependencies; issued tickets are unaffected.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only publishChannelAvailability and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **publication preview**: Per channel what the guest or cashier will see from when, and "issued tickets unaffected" with the count. *(source: contracts/spine/catalogue.yaml#publishChannelAvailability)*

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `publishChannelAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel publication availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel publication availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel publication availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel publication availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channels:
- channel: Website
  from: '2026-12-01'
- channel: Point of sale
  posGroups:
  - Main Gate tills
```

#### Permissions

- `publishChannelAvailability` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-124` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-124`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 12: Works in Channel Publication & Availability → Control where a product may be exposed for sale.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-124?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-125` Publication & Activation Scheduler

**Automate future product lifecycle actions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-125 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/publication-activation-scheduler-adm-125` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Future lifecycle actions on a calendar: publication, sales start, activation, sales suspension, deactivation, end of sale, retirement, per venue and channel and time zone; affected bookings shown before confirming.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listScheduledLifecycleActions` ?from |
| To | date and time picker | — | — | `listScheduledLifecycleActions` ?to |
| Action type | select | — | Publication · Sales start · Activation · Sales suspension · Deactivation · End of sale · Retirement | `listScheduledLifecycleActions` ?actionType |
| Status | radio group | — | Scheduled · Executed · Failed · Cancelled | `listScheduledLifecycleActions` ?status |
| Product | picker: choose a product | — | — | `listScheduledLifecycleActions` ?productId |

**Sent by *Publish*** (`publishActivationScheduler`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action type `actionType` | select | optional | — | Publication · Sales start · Activation · Sales suspension · Deactivation · End of sale · Retirement | — | Scheduled action (Configurable Actions, pack p.10) | `publishActivationScheduler` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Date and time the action runs | `publishActivationScheduler` body |
| Time zone `timeZone` | text field | optional | — | — | — | IANA time zone the date is entered in | `publishActivationScheduler` body |
| Venue `venueId` | text field | optional | — | — | — | Venue id | `publishActivationScheduler` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | Channels the action applies to; empty = all | `publishActivationScheduler` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Product id | `publishActivationScheduler` body |
| Target state `targetState` | select | optional | — | Draft · In review · Approved · Live · Withdrawn · Archived | — | Lifecycle state the product moves to | `publishActivationScheduler` body |
| Notify roles `notifyRoles` | list of values (chips) | optional | — | — | — | Roles notified when the action runs or fails | `publishActivationScheduler` body |
| Pre action validation `preActionValidation` | toggle | optional | — | — | — | Validate the product before running; the action fails with issues if blockers exist | `publishActivationScheduler` body |
| Failure handling `failureHandling` | segmented control | optional | — | Retry then notify · Skip and notify · Hold for manual action | — | Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out) | `publishActivationScheduler` body |
| Schedule `scheduleId` | picker: choose a schedule | optional | — | — | shows names, sends the id | Existing scheduled action to change; empty to create | `publishActivationScheduler` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scheduledAt and timeZone**: Venue time zone by default, shown explicitly. *(source: contracts/spine/catalogue.yaml#publishActivationScheduler / DI-579)*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (timeline, from `listScheduledLifecycleActions`): **Every scheduled lifecycle action in the range, on a calendar**: upcoming as scheduled, done as executed, failed with its reason, so failed jobs and conflicts show where they happened. Without a range, the next 31 days (decided 29 September, readiness close-out).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Action type | chip: Publication, Sales start, Activation, Sales suspension, Deactivation, End of sale… | Scheduled action (Configurable Actions, pack p.10) |
| Scheduled at | 1 Oct 2026, 14:30 | Date and time the action runs |
| Time zone | text | IANA time zone the date is entered in |
| Venue | text | Venue id |
| Channels | list or chips (count when long) | Channels the action applies to; empty = all |
| Product | the name it points at, never the id | Product id |
| Target state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Lifecycle state the product moves to |
| Notify roles | list or chips (count when long) | Roles notified when the action runs or fails |
| Pre action validation | yes / no (icon or chip) | Validate the product before running; the action fails with issues if blockers exist |
| Failure handling | chip: Retry then notify, Skip and notify, Hold for manual action | Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out) |
| Validation issues | list or chips (count when long) | Lifecycle conflicts found for this action (decided 29 September, readiness close-out) |
| Code | chip: After validity end, Overlaps other action, Product not approved, Invalid … | — |
| Message | text | — |
| Schedule | the name it points at, never the id | Scheduled action id |
| Status | text | Scheduled action status: scheduled, executed, failed or cancelled |
| Failure reason | text | Why the last run failed |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | `publishActivationScheduler` PUT `/activation-scheduler` | PublicationActivationSchedulerInput | PublicationActivationSchedulerView | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listScheduledLifecycleActions` (onLoad, Scheduled lifecycle actions, for the scheduler calendar)

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `publishActivationScheduler`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The publication activation scheduler list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the publication activation scheduler untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No publication activation scheduler yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the publication activation scheduler are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A range longer than 366 days, or `to` before `from`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action:
  product: Summer Splash Pass
  type: endOfSale
  at: 2026-09-30 23:59 Asia/Dubai
```

#### Permissions

- `publishActivationScheduler` → `PRODUCT_CONFIGURE` (configure) · staff
- `listScheduledLifecycleActions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-125` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-125`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 14: Works in Publication & Activation Scheduler → Automate future product lifecycle actions.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-125?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-126` Product Duplication & Template Library

**Accelerate product configuration by allowing administrators to reuse proven configurations. The source matrix explicitly requires duplication of products together with associated configuration, rules, pricing and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-126 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Duplication Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-duplication-template-library-adm-126` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Reuse proven configurations: duplicate a product with its rules, pricing and entitlements, or save it as a template.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Core product details | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Pricing references | select field | — | — | — | — | — | — |
| Entitlements | select field | — | — | — | — | — | — |
| Capacity references | select field | — | — | — | — | — | — |
| Eligibility | select field | — | — | — | — | — | — |
| Sales channels | select field | — | — | — | — | — | — |
| Media | select field | — | — | — | — | — | — |
| Policies | select field | — | — | — | — | — | — |
| Rules | select field | — | — | — | — | — | — |
| Content | select field | — | — | — | — | — | — |
| Images | select field | — | — | — | — | — | — |
| Relationships | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template kind | select | — | Standard admission · Child admission · Vip ticket · Timeslot ticket · Event ticket · Group product · Annual pass · Add on · Venue specific | `listProductDuplicationTemplate` ?templateKind |
| Product type | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProductDuplicationTemplate` ?productType |
| Search | text field | — | — | `listProductDuplicationTemplate` ?search |

**Form: Save configuration template** (modal, opened by *Save configuration template*; *Save configuration template* calls `setConfigurationTemplate`, *Cancel* sends nothing)

**Collects what `setConfigurationTemplate` sends before it is called.** Required: `subject`, `name`, `status`. Optional: `description`, `templateKind`, `productKind`, `venueId`, `sourceProductId`, `sourcePriceListId`, `includedComponents`, `reviewFields`, `isAiDrafted`, `ownerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subject` | segmented control | required | — | Product · Price list | — | — | `setConfigurationTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setConfigurationTemplate` body |
| Description `description` | text area | optional | — | — | — | — | `setConfigurationTemplate` body |
| Template kind `templateKind` | text field | optional | — | max length 60 | — | Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`. | `setConfigurationTemplate` body |
| Product kind `productKind` | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `setConfigurationTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source product `sourceProductId` | picker: choose a source product | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source price list `sourcePriceListId` | picker: choose a source price list | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Included components `includedComponents` | list of values (chips) | optional | — | — | — | Product or price-list component names, per `subject`. | `setConfigurationTemplate` body |
| Review fields `reviewFields` | multi-select chips | optional | — | Dates · Prices · Venue · Capacity · Event · Tax · Channels | — | — | `setConfigurationTemplate` body |
| Is AI drafted `isAiDrafted` | toggle | optional | off | — | — | — | `setConfigurationTemplate` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setConfigurationTemplate` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |

Errors to draw in the form: 422 `sourceRequired`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save configuration template (primary button) | `setConfigurationTemplate` PUT `/configuration-templates` | ConfigurationTemplate | ConfigurationTemplate | 422 `sourceRequired`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listProductDuplicationTemplate` (onLoad, Product Duplication & Template Library)

**Where the user goes next**

- → `ADM-118` Product Lifecycle Command Center: *Returns to the board's landing screen*; calls `listProductDuplicationTemplate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product duplication template configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product duplication template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product duplication template configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `sourceRequired`. |

#### Consistency with other screens

- Match `ADM-056`: One template library for products and price lists.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
template:
  name: Events template
  basedOn: Dune Nights 2026
  includes:
  - ticket types
  - entitlement
  - policies
```

#### Permissions

- `listProductDuplicationTemplate` → `PRODUCT_VIEW` (read) · staff
- `setConfigurationTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-126` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-126`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 16: Works in Product Duplication & Template Library → Accelerate product configuration by allowing administrators to reuse proven configurations. The source matrix explicitly requires duplication of products together with associated configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-126?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save configuration template.
- [ ] Every transition is wired: `ADM-118`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-127` AI Catalogue Builder & Configuration Review

**Provide TICVAI's AI-first interface for accelerating product creation and configuration. This directly supports the matrix requirement allowing administrators to upload spreadsheets, brochures, PDFs or existing catalogues and use AI to generate product structures, pricing, rules, entitlements and configurations. Board 2 governs what happens after a product has been created or while an existing product is being changed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-127 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/ai-catalogue-builder-configuration-review-adm-127` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of a catalogue review (setCatalogueReview has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The AI-first way to build a catalogue: describe it, or upload a spreadsheet, brochure, PDF or catalogue; the assistant drafts products, asks for what is missing and every result is a draft for review.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setCatalogueReview and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **review**: Proposed products with assumptions and confidence, each accept, edit or reject. *(source: contracts/spine/catalogue.yaml#setCatalogueReview / DI-440)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The catalogue review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the catalogue review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No catalogue review yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the catalogue review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-117`: The venue screen uses generateConfiguration; same blueprint layout.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
session:
  input: dune-park-brochure-2027.pdf
  proposed: 23
  needsInput: 4
```

#### Permissions

- `setCatalogueReview` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI-assisted draft: an AI wizard asks what ticket type to create and the relevant fields, then auto-configures a draft for review before approval/publish. Agreed extension (Chinmay): it also parses unstructured input (incl. OCR on images) and prompts the user for missing details. *(agreed · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-440)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-127` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-127`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 1
- Flow F152 *Product Lifecycle Catalogue Governance board 1: Product Lifecycle Command Center*, step 18: Works in AI Catalogue Builder & Configuration Review → Provide TICVAI's AI-first interface for accelerating product creation and configuration. This directly supports the matrix requirement allowing administrators to upload spreadsheets, brochures, PDFs …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-127?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
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

### In P08 · Catalogue

- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*

**22 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createProduct": {"method":"POST","path":"/products","contract":"catalogue","summary":"Create a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreateProductRequest","responds":"Product"},
"listProductDuplicationTemplate": {"method":"GET","path":"/product-duplication-template","contract":"catalogue","summary":"Product Duplication & Template Library","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateKind","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductImportExport": {"method":"GET","path":"/product-import-export","contract":"catalogue","summary":"Product Import / Export & Environment Transfer","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"direction","in":"query","required":false},{"name":"environment","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductLifecycle": {"method":"GET","path":"/product-lifecycle","contract":"catalogue","summary":"Product Lifecycle Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productType","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"locationId","in":"query","required":false},{"name":"lifecycleState","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"effectiveOn","in":"query","required":false},{"name":"createdFrom","in":"query","required":false},{"name":"createdTo","in":"query","required":false},{"name":"modifiedSince","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScheduledLifecycleActions": {"method":"GET","path":"/activation-scheduler","contract":"catalogue","summary":"Scheduled lifecycle actions, for the scheduler calendar","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"actionType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishActivationScheduler": {"method":"PUT","path":"/activation-scheduler","contract":"catalogue","summary":"Publication & Activation Scheduler","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PublicationActivationSchedulerInput","responds":"PublicationActivationSchedulerView"},
"publishChannelAvailability": {"method":"PUT","path":"/channel-availability","contract":"catalogue","summary":"Channel Publication & Availability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPublicationAvailabilityInput","responds":"ChannelPublicationAvailabilityView"},
"setCatalogueReview": {"method":"PUT","path":"/catalogue-review","contract":"catalogue","summary":"AI Catalogue Builder & Configuration Review","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCatalogueBuilderConfigurationReviewInput","responds":"AiCatalogueBuilderConfigurationReviewView"},
"setConfigurationTemplate": {"method":"PUT","path":"/configuration-templates","contract":"catalogue","summary":"Create or update a product or price-list template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationTemplate","responds":"ConfigurationTemplate"},
"setLifecycleStatuWorkflow": {"method":"PUT","path":"/lifecycle-statu-workflow","contract":"catalogue","summary":"Lifecycle Status & Workflow Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LifecycleStatusWorkflowConfigurationInput","responds":"LifecycleStatusWorkflowConfigurationView"},
"setProductContextOwnership": {"method":"PUT","path":"/product-context-ownership","contract":"catalogue","summary":"Product Context, Ownership & Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductContextOwnershipAssignmentInput","responds":"ProductContextOwnershipAssignmentView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiCatalogueBuilderConfigurationReviewInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What AI Catalogue Builder & Configuration Review submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"prompt":{"type":"string","description":"Natural-language request","nullable":true},"sessionId":{"type":"string","description":"Existing session to update; empty to start one","format":"uuid","nullable":true},"inputMethod":{"type":"string","enum":["naturalLanguage","excel","csv","pdf","brochure","existingCatalogue","referenceProduct"],"description":"Input method (pack p.12)"},"fileId":{"type":"string","description":"Uploaded source file id","nullable":true},"referenceProductId":{"type":"string","description":"Existing product used as reference","format":"uuid","nullable":true},"decisions":{"type":"array","items":{"type":"object","properties":{"recommendationId":{"type":"string"},"decision":{"type":"string","enum":["accepted","modified","rejected","requiresReview"]},"modifiedValue":{"type":"string","nullable":true}}},"description":"Administrator's classification of each recommendation"},"createDraft":{"type":"boolean","description":"Build the draft product from the accepted/modified recommendations"}}},
"AiCatalogueBuilderConfigurationReviewView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Catalogue Builder & Configuration Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"prompt":{"type":"string","description":"Natural-language request","nullable":true},"sessionId":{"type":"string","description":"Review session id","format":"uuid"},"inputMethod":{"type":"string","enum":["naturalLanguage","excel","csv","pdf","brochure","existingCatalogue","referenceProduct"],"description":"Input method (pack p.12)"},"fileId":{"type":"string","description":"Uploaded source file id","nullable":true},"referenceProductId":{"type":"string","description":"Existing product used as reference","format":"uuid","nullable":true},"recommendations":{"type":"array","items":{"type":"object","properties":{"recommendationId":{"type":"string"},"area":{"type":"string","enum":["productStructure","ticketType","nameDescription","validity","pricing","entitlements","eligibility","capacity","channels","media","relationships","policies","missingInformation"]},"sourceExcerpt":{"type":"string","description":"Source"},"interpretation":{"type":"string","description":"AI interpretation"},"proposedValue":{"type":"string","description":"Proposed TICVAI configuration"},"confidence":{"type":"string","enum":["high","medium","low","requiresClarification","missing"]},"decision":{"type":"string","enum":["accepted","modified","rejected","requiresReview"]},"modifiedValue":{"type":"string","nullable":true}}},"description":"AI recommendations: Source -> AI interpretation -> Proposed configuration, with confidence and the administrator's classification"},"draftProductId":{"type":"string","description":"Draft product built from the accepted recommendations","format":"uuid","nullable":true}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelPublicationAvailabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ChannelPublicationAvailabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"publicationPreview":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"venueId":{"type":"string"},"exposed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"description":"Preview of where the product will actually be on sale"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["channelNotConfigured","noPriceForChannel","noCapacityAllocation","productNotApproved","venueNotAssigned"]},"message":{"type":"string"}}},"description":"Missing channel dependencies (decided 29 September, readiness close-out)"},"productId":{"type":"string","description":"Product id","format":"uuid"},"issuedEntitlementsUnaffected":{"type":"integer","description":"Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"}}},
"ConfigurationTemplate": {"type":"object","x-ticvai-persistence":"catalogue.configuration_template","description":"**A reusable starting point for a product or a price list** (29 September, data model DM3). Merges the product duplication and template library (ADM-126) and price list templates (ADM-063). `subject` says which; a template copies the listed components and marks `reviewFields` for the operator to confirm.","required":["id","scopePath","subject","name","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"subject":{"type":"string","enum":["product","priceList"]},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"templateKind":{"type":"string","maxLength":60,"nullable":true,"description":"Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`."},"productKind":{"allOf":[{"$ref":"#/components/schemas/ProductKind"}],"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceProductId":{"type":"string","format":"uuid","nullable":true},"sourcePriceListId":{"type":"string","format":"uuid","nullable":true},"includedComponents":{"type":"array","items":{"type":"string"},"description":"Product or price-list component names, per `subject`."},"reviewFields":{"type":"array","items":{"type":"string","enum":["dates","prices","venue","capacity","event","tax","channels"]}},"isAiDrafted":{"type":"boolean","default":false},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CreateProductRequest": {"type":"object","required":["code","name","kind","venueId"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`.\n"},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid"},"dataMaskValues":{"type":"object","additionalProperties":true},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"See `Product.salesContact` (W3, 29 September)."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"See `Product.bookingFlowId` (W8, W12, 29 September)."},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"}},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"}},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"}},"requiresTimeWindow":{"type":"boolean"}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LifecycleStatusWorkflowConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Lifecycle Status & Workflow Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"availableLifecycleStatuses":{"type":"array","items":{"type":"object","properties":{"state":{"$ref":"#/components/schemas/ProductLifecycleState"},"label":{"type":"string","description":"Venue's display label for the state"},"enabled":{"type":"boolean"}}},"description":"Available lifecycle statuses, in sequence order; states come from ProductLifecycleState, the venue sets labels and switches optional ones off (decided 29 September, readiness close-out)"},"allowedStatusTransitions":{"type":"array","items":{"type":"object","properties":{"from":{"$ref":"#/components/schemas/ProductLifecycleState"},"to":{"$ref":"#/components/schemas/ProductLifecycleState"},"initiatorRoles":{"type":"array","items":{"type":"string"},"description":"Roles that can initiate this transition"},"trigger":{"type":"string","enum":["manual","automatic"],"description":"Whether the transition is manual or automatic (scheduler)"},"approvalRequired":{"type":"boolean"},"requiredSections":{"type":"array","items":{"type":"string","enum":["validity","entitlements","capacity","pricing","eligibility","media","channels","policies"]},"description":"Required information / validation before the transition (the completeness sections of p.5)"},"effectiveDateRequired":{"type":"boolean"},"reasonRequired":{"type":"boolean","description":"Reason/comment required"},"notifyRoles":{"type":"array","items":{"type":"string"},"description":"Notification triggers: roles notified when the transition happens (sent through the central notifications module)"}}},"description":"Allowed status transitions, each with its initiator roles, trigger, approval, required information, effective-date, reason and notification rules"},"statusSpecificEditPermissions":{"type":"array","items":{"type":"object","properties":{"state":{"$ref":"#/components/schemas/ProductLifecycleState"},"editableByRoles":{"type":"array","items":{"type":"string"}},"lockedSections":{"type":"array","items":{"type":"string"}}}},"description":"Status-specific edit permissions: who may edit a product in each state, and which sections are locked"}}},
"LifecycleStatusWorkflowConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Lifecycle Status & Workflow Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"availableLifecycleStatuses":{"type":"array","items":{"type":"object","properties":{"state":{"$ref":"#/components/schemas/ProductLifecycleState"},"label":{"type":"string","description":"Venue's display label for the state"},"enabled":{"type":"boolean"}}},"description":"Available lifecycle statuses, in sequence order; states come from ProductLifecycleState, the venue sets labels and switches optional ones off (decided 29 September, readiness close-out)"},"allowedStatusTransitions":{"type":"array","items":{"type":"object","properties":{"from":{"$ref":"#/components/schemas/ProductLifecycleState"},"to":{"$ref":"#/components/schemas/ProductLifecycleState"},"initiatorRoles":{"type":"array","items":{"type":"string"},"description":"Roles that can initiate this transition"},"trigger":{"type":"string","enum":["manual","automatic"],"description":"Whether the transition is manual or automatic (scheduler)"},"approvalRequired":{"type":"boolean"},"requiredSections":{"type":"array","items":{"type":"string","enum":["validity","entitlements","capacity","pricing","eligibility","media","channels","policies"]},"description":"Required information / validation before the transition (the completeness sections of p.5)"},"effectiveDateRequired":{"type":"boolean"},"reasonRequired":{"type":"boolean","description":"Reason/comment required"},"notifyRoles":{"type":"array","items":{"type":"string"},"description":"Notification triggers: roles notified when the transition happens (sent through the central notifications module)"}}},"description":"Allowed status transitions, each with its initiator roles, trigger, approval, required information, effective-date, reason and notification rules"},"statusSpecificEditPermissions":{"type":"array","items":{"type":"object","properties":{"state":{"$ref":"#/components/schemas/ProductLifecycleState"},"editableByRoles":{"type":"array","items":{"type":"string"}},"lockedSections":{"type":"array","items":{"type":"string"}}}},"description":"Status-specific edit permissions: who may edit a product in each state, and which sections are locked"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductContextOwnershipAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Product Context, Ownership & Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"businessUnit":{"type":"string","description":"Business unit id","nullable":true},"legalEntity":{"type":"string","description":"Legal entity id","nullable":true},"venue":{"type":"string","description":"Venue id"},"attraction":{"type":"string","description":"Attraction id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"site":{"type":"string","description":"Site id","nullable":true},"location":{"type":"string","description":"Location id","nullable":true},"productOwner":{"type":"string","description":"Product owner (principal id)"},"responsibleDepartment":{"type":"string","description":"Responsible department"},"operationalContact":{"type":"string","description":"Operational contact (principal id or name)","nullable":true},"customerSegment":{"type":"array","items":{"type":"string"},"description":"Applicable customer segments"},"market":{"type":"string","description":"Market","nullable":true},"salesTerritory":{"type":"string","description":"Sales territory","nullable":true},"brand":{"type":"string","description":"Brand (catalogue brand category id)","nullable":true},"productFamily":{"type":"string","description":"Product family","nullable":true},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ProductContextOwnershipAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Context, Ownership & Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tenant":{"type":"string","description":"Tenant id (set from the caller's tenant)"},"businessUnit":{"type":"string","description":"Business unit id","nullable":true},"legalEntity":{"type":"string","description":"Legal entity id","nullable":true},"venue":{"type":"string","description":"Venue id"},"attraction":{"type":"string","description":"Attraction id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"site":{"type":"string","description":"Site id","nullable":true},"location":{"type":"string","description":"Location id","nullable":true},"productOwner":{"type":"string","description":"Product owner (principal id)"},"creator":{"type":"string","description":"Creator (principal id), recorded by the system"},"responsibleDepartment":{"type":"string","description":"Responsible department"},"operationalContact":{"type":"string","description":"Operational contact (principal id or name)","nullable":true},"customerSegment":{"type":"array","items":{"type":"string"},"description":"Applicable customer segments"},"market":{"type":"string","description":"Market","nullable":true},"salesTerritory":{"type":"string","description":"Sales territory","nullable":true},"brand":{"type":"string","description":"Brand (catalogue brand category id)","nullable":true},"productFamily":{"type":"string","description":"Product family","nullable":true},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductDuplicationTemplateLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Duplication & Template Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"includedComponents":{"type":"array","items":{"type":"string","enum":["coreProductDetails","validity","pricingReferences","entitlements","capacityReferences","eligibility","salesChannels","media","policies","rules","content","images","relationships"]},"description":"Duplication options copied by this template"},"templateId":{"type":"string","description":"Template id","format":"uuid"},"name":{"type":"string","description":"Template name"},"templateKind":{"type":"string","enum":["standardAdmission","childAdmission","vipTicket","timeslotTicket","eventTicket","groupProduct","annualPass","addOn","venueSpecific"],"description":"Template kind (Template Library, pack p.11)"},"productType":{"allOf":[{"$ref":"#/components/schemas/ProductKind"}],"description":"Product type the template creates"},"venueId":{"type":"string","description":"Venue for a venue-specific template; empty for all venues","format":"uuid","nullable":true},"sourceProductId":{"type":"string","description":"Product the template was saved from","format":"uuid","nullable":true},"reviewFields":{"type":"array","items":{"type":"string","enum":["dates","prices","venue","capacity","event","tax","channels"]},"description":"Smart Clone: sensitive fields the user must review before the clone is saved (default all seven) (decided 29 September, readiness close-out)"},"updatedAt":{"type":"string","description":"Last changed","format":"date-time"}}},
"ProductImportExportEnvironmentTransferView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Import / Export & Environment Transfer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"referenceMappings":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["venue","location","dependency"]},"sourceRef":{"type":"string"},"targetRef":{"type":"string","nullable":true}}},"description":"Venue/location and dependency references mapped from source to target"},"missingReferences":{"type":"array","items":{"type":"string"},"description":"References with no mapping in the target environment"},"changePreview":{"type":"array","items":{"type":"object","properties":{"productId":{"type":"string"},"component":{"type":"string"},"change":{"type":"string","enum":["create","update","unchanged","conflict"]},"detail":{"type":"string"}}},"description":"Source vs target comparison: what executing will change"},"transferId":{"type":"string","description":"Transfer / package id","format":"uuid"},"direction":{"type":"string","enum":["export","import"],"description":"Direction"},"sourceEnvironment":{"type":"string","enum":["development","sandbox","uat","staging","production"],"description":"Environment (the pack's example list, p.7) (decided 29 September, readiness close-out)"},"targetEnvironment":{"type":"string","enum":["development","sandbox","uat","staging","production"],"description":"Environment (the pack's example list, p.7) (decided 29 September, readiness close-out)"},"productIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Products in the package"},"components":{"type":"array","items":{"type":"string","enum":["coreProductDetails","validity","pricingReferences","entitlements","capacityReferences","eligibility","salesChannels","media","policies","rules","relationships"]},"description":"Associated configuration components included"},"status":{"type":"string","description":"Transfer status: draft, validated, awaitingApproval, executing, completed or failed (decided 29 September, readiness close-out)"},"requestedBy":{"type":"string","description":"Requested by (principal display name)"},"createdAt":{"type":"string","description":"Created","format":"date-time"},"completedAt":{"type":"string","description":"Transfer result time","format":"date-time","nullable":true}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Lifecycle Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"lifecycleState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Current lifecycle state (see handoff for how the pack's 11 statuses map to it)"},"channelPublication":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"published":{"type":"boolean"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true}}},"description":"Publication status by channel"},"effectiveFrom":{"type":"string","description":"Effective / activation date-time: when the product becomes commercially active","format":"date-time","nullable":true},"pendingActions":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string","enum":["publication","salesStart","activation","salesSuspension","deactivation","endOfSale","retirement","approval"]},"dueAt":{"type":"string","format":"date-time","nullable":true}}},"description":"Pending lifecycle actions: scheduled or awaiting approval, soonest first"},"productId":{"type":"string","description":"Product id","format":"uuid"},"productName":{"type":"string","description":"Internal product name"},"productType":{"allOf":[{"$ref":"#/components/schemas/ProductKind"}],"description":"Product type"},"venueId":{"type":"string","description":"Venue id","format":"uuid"},"locationId":{"type":"string","description":"Location id","format":"uuid","nullable":true},"productOwner":{"type":"string","description":"Product owner (principal display name)"},"responsibleDepartment":{"type":"string","description":"Responsible department"},"effectiveTo":{"type":"string","description":"End of the effective period; empty for open-ended","format":"date-time","nullable":true},"createdAt":{"type":"string","description":"Creation date-time","format":"date-time"},"lastModifiedAt":{"type":"string","description":"Last modification date-time","format":"date-time"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["missingValidity","missingEntitlements","missingCapacity","missingPricing","missingEligibility","missingMedia","missingChannels","missingPolicies","missingOwner","awaitingApproval"]},"message":{"type":"string"}}},"description":"Incomplete configuration or publication blockers (pack p.4); codes follow the configuration-completeness sections of p.5 (decided 29 September, readiness close-out)"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI attention flags (incomplete setup, unusual configuration, approaching activation, lifecycle conflicts); advisory only"}}},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"PublicationActivationSchedulerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Publication & Activation Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"actionType":{"type":"string","enum":["publication","salesStart","activation","salesSuspension","deactivation","endOfSale","retirement"],"description":"Scheduled action (Configurable Actions, pack p.10)"},"scheduledAt":{"type":"string","description":"Date and time the action runs","format":"date-time"},"timeZone":{"type":"string","description":"IANA time zone the date is entered in"},"venueId":{"type":"string","description":"Venue id","nullable":true},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels the action applies to; empty = all"},"productId":{"type":"string","description":"Product id","format":"uuid"},"targetState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Lifecycle state the product moves to"},"notifyRoles":{"type":"array","items":{"type":"string"},"description":"Roles notified when the action runs or fails"},"preActionValidation":{"type":"boolean","description":"Validate the product before running; the action fails with issues if blockers exist"},"failureHandling":{"type":"string","enum":["retryThenNotify","skipAndNotify","holdForManualAction"],"description":"Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out)"},"scheduleId":{"type":"string","description":"Existing scheduled action to change; empty to create","format":"uuid","nullable":true}}},
"PublicationActivationSchedulerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Publication & Activation Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"actionType":{"type":"string","enum":["publication","salesStart","activation","salesSuspension","deactivation","endOfSale","retirement"],"description":"Scheduled action (Configurable Actions, pack p.10)"},"scheduledAt":{"type":"string","description":"Date and time the action runs","format":"date-time"},"timeZone":{"type":"string","description":"IANA time zone the date is entered in"},"venueId":{"type":"string","description":"Venue id","nullable":true},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels the action applies to; empty = all"},"productId":{"type":"string","description":"Product id","format":"uuid"},"targetState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Lifecycle state the product moves to"},"notifyRoles":{"type":"array","items":{"type":"string"},"description":"Roles notified when the action runs or fails"},"preActionValidation":{"type":"boolean","description":"Validate the product before running; the action fails with issues if blockers exist"},"failureHandling":{"type":"string","enum":["retryThenNotify","skipAndNotify","holdForManualAction"],"description":"Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out)"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["afterValidityEnd","overlapsOtherAction","productNotApproved","invalidTransition","pastDate"]},"message":{"type":"string"}}},"description":"Lifecycle conflicts found for this action (decided 29 September, readiness close-out)"},"scheduleId":{"type":"string","description":"Scheduled action id","format":"uuid"},"status":{"type":"string","description":"Scheduled action status: scheduled, executed, failed or cancelled"},"failureReason":{"type":"string","description":"Why the last run failed","nullable":true}}}
}
```
