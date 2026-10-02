# WS50 — Promotions   Bundles Management board 6

**10 screens · 13 operations · 14 schemas · 3 permissions**

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
  `PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-188` | Dynamic Bundle Operations Command Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-189` | Component Inventory & Availability Matrix | B–D | 0 | 0 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `ADM-190` | Bundle Sellability & Dependency Rule Engine | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-191` | Capacity Pool & Reservation Manager | B–D | 19 | 12 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-192` | Dynamic Component Substitution Engine | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-193` | Dynamic Bundle Rule & Composition Engine | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-194` | Real-Time Availability & Checkout Validation | B–D | 1 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-195` | Bundle Availability by Channel, Venue & Partner | B–D | 17 | 12 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-196` | Bundle Availability Forecast, Alerts & Recovery | B–D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-197` | Dynamic Bundle Simulation & AI Optimization | B–D | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-189, ADM-190, ADM-193, ADM-194, ADM-196, ADM-197 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-188` Dynamic Bundle Operations Command Center

**Provide real-time visibility into the operational health of all active bundles.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-bundle-operations-command-center-adm-188` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The operational health of active bundles: availability, sales, substitutions.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listDynamicBundle2, listDynamicBundle, listDynamicBundleRule return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDynamicBundle2, listDynamicBundle, listDynamicBundleRule carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listDynamicBundle2 / contracts/satellite/promotions.yaml#listDynamicBundle / contracts/satellite/promotions.yaml#listDynamicBundleRule; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Dynamic Bundles** (metric tile)

**Sellable Bundles** (metric tile)

**Partially Available Bundles** (metric tile)

**Unavailable Bundles** (metric tile)

**Bundles with Low Capacity** (metric tile)

**Components Sold Out** (metric tile)

**Substitutions Triggered** (metric tile)

**Bundle Sales Today** (metric tile)

**Failed Bundle Attempts** (metric tile)

**Capacity Reserved** (metric tile)

**Revenue at Risk** (metric tile)

**Recovered Revenue** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **bundle health**: Bundles at risk first. *(source: contracts/satellite/promotions.yaml#listDynamicBundle)*

**Data it reads**: `listDynamicBundle2` (onLoad, Dynamic Bundle Simulation & AI Optimization); `listDynamicBundle` (onLoad, Dynamic Bundle Operations Command Center); `listDynamicBundleRule` (onLoad, Dynamic Bundle Rule & Composition Engine)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-189` Component Inventory & Availability Matrix: *Works in Component Inventory & Availability Matrix*; calls `listDynamicBundle`
- → `ADM-190` Bundle Sellability & Dependency Rule Engine: *Works in Bundle Sellability & Dependency Rule Engine*; calls `listDynamicBundle`
- → `ADM-191` Capacity Pool & Reservation Manager: *Works in Capacity Pool & Reservation Manager*; calls `listDynamicBundle`
- → `ADM-192` Dynamic Component Substitution Engine: *Works in Dynamic Component Substitution Engine*; calls `listDynamicBundle`
- → `ADM-193` Dynamic Bundle Rule & Composition Engine: *Works in Dynamic Bundle Rule & Composition Engine*; calls `listDynamicBundle`
- → `ADM-194` Real-Time Availability & Checkout Validation: *Works in Real-Time Availability & Checkout Validation*; calls `listDynamicBundle`
- → `ADM-195` Bundle Availability by Channel, Venue & Partner: *Works in Bundle Availability by Channel, Venue & Partner*; calls `listDynamicBundle`
- → `ADM-196` Bundle Availability Forecast, Alerts & Recovery: *Works in Bundle Availability Forecast, Alerts & Recovery*; calls `listDynamicBundle`
- → `ADM-197` Dynamic Bundle Simulation & AI Optimization: *Works in Dynamic Bundle Simulation & AI Optimization*; calls `listDynamicBundle`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic bundle operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic bundle operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic bundle operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic bundle operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  bundle: Pick 3 attractions
  status: at risk
  reason: Planetarium closed Sat
```

#### Permissions

- `listDynamicBundle2` → `PRICE_VIEW` (read) · staff
- `listDynamicBundle` → `PRICE_VIEW` (read) · staff
- `listDynamicBundleRule` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-188` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-188`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 1: Opens Dynamic Bundle Operations Command Center → Provide real-time visibility into the operational health of all active bundles.
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F159 branch at step 1 (expected): when Nothing has been set up on Dynamic Bundle Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F159 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-188?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-189`, `ADM-190`, `ADM-191`, `ADM-192`, `ADM-193`, `ADM-194`, `ADM-195`, `ADM-196`, `ADM-197`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-189` Component Inventory & Availability Matrix

**Provide one centralized matrix showing availability for every component within every active bundle.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `itemId` (navigation) |
| Route | `/commercial/component-inventory-availability-matrix-adm-189` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** One matrix of availability for every component of every active bundle.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listComponentInventoryAvailability return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listComponentInventoryAvailability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **matrix**: Bundles as rows, components as columns, availability in cells. *(source: contracts/satellite/promotions.yaml#listComponentInventoryAvailability / contracts/satellite/inventory.yaml#getInventoryKitDefinition)*

**Data it reads**: `listComponentInventoryAvailability` (onLoad, Component Inventory & Availability Matrix); `getInventoryKitDefinition` (onLoad, Show kit components)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listComponentInventoryAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The component inventory availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the component inventory availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No component inventory availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the component inventory availability are still there. The pack's own statuses are t ry ty le — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cell:
  bundle: Family Fun Bundle
  component: Kids T-shirt S
  available: 12
```

#### Permissions

- `listComponentInventoryAvailability` → `PRICE_VIEW` (read) · staff
- `getInventoryKitDefinition` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-189` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-189`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 2: Works in Component Inventory & Availability Matrix → Provide one centralized matrix showing availability for every component within every active bundle.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-189?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-190` Bundle Sellability & Dependency Rule Engine

**Determine whether the overall bundle can be sold based on the state of its underlying components.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-sellability-dependency-rule-engine-adm-190` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Partner component required. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether a bundle can be sold from the state of its components.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Partner component required.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-190; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listBundleSellabilityDependency return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBundleSellabilityDependency; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Partner component required (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **dependency rules**: Component states that stop the bundle. *(source: contracts/satellite/promotions.yaml#listBundleSellabilityDependency)*

**Data it reads**: `listBundleSellabilityDependency` (onLoad, Bundle Sellability & Dependency Rule Engine)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listBundleSellabilityDependency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle sellability dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle sellability dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle sellability dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle sellability dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: If lunch sells out, stop the bundle; if parking sells out, sell without it
```

#### Permissions

- `listBundleSellabilityDependency` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-190` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-190`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 4: Works in Bundle Sellability & Dependency Rule Engine → Determine whether the overall bundle can be sold based on the state of its underlying components.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-190?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Partner component required.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-191` Capacity Pool & Reservation Manager

**Manage how bundle sales consume capacity from underlying products. This is particularly important because a bundle must not create artificial inventory separate from the actual attraction/product capacity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bundleId` (navigation) |
| Route | `/commercial/capacity-pool-reservation-manager-adm-191` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How bundle sales draw on product capacity; a bundle never creates capacity of its own.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCapacityPoolReservation return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCapacityPoolReservation carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCapacityPoolReservation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Temporary reservation | select field | — | — | — | — | — | — |
| Hold duration | select field | — | — | — | — | — | — |
| Release timeout | select field | — | — | — | — | — | — |
| Hard allocation | select field | — | — | — | — | — | — |
| Soft allocation | select field | — | — | — | — | — | — |
| Overbooking policy | select field | — | — | — | — | — | — |
| Waitlist behavior | select field | — | — | — | — | — | — |

**Form: Save bundle capacity policy** (modal, opened by *Save bundle capacity policy*; *Save bundle capacity policy* calls `setBundleCapacityPolicy`, *Cancel* sends nothing)

**Collects what `setBundleCapacityPolicy` sends before it is called.** Required: `policies`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policies `policies` | repeatable rows | required | — | at most 200 | — | — | `setBundleCapacityPolicy` body |
| Bundle `policies[].bundleId` | picker: choose a bundle | required | — | — | shows names, sends the id | — | `setBundleCapacityPolicy` body |
| Channel `policies[].channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setBundleCapacityPolicy` body |
| Venue `policies[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Where the policy differs by venue for a multi-venue bundle. | `setBundleCapacityPolicy` body |
| Partner `policies[].partnerId` | picker: choose a partner | optional | — | — | shows names, sends the id | — | `setBundleCapacityPolicy` body |
| Capacity source `policies[].capacitySource` | select | required | — | Shared pool · Dedicated bundle allocation · Channel allocation · Partner allocation · Event capacity · Timeslot capacity · Seat inventory · Resource capacity | — | — | `setBundleCapacityPolicy` body |
| Allocation mode `policies[].allocationMode` | segmented control | optional | Hard | Hard · Soft | — | Hard allocation is ring-fenced for the bundle; soft is released back when unsold. | `setBundleCapacityPolicy` body |
| Capacity ceiling `policies[].capacityCeiling` | number field | optional | — | min 0 | — | — | `setBundleCapacityPolicy` body |
| Hold duration minutes `policies[].holdDurationMinutes` | number field (minutes) | optional | — | min 1 | — | How long a temporary reservation of the components lasts. | `setBundleCapacityPolicy` body |
| Booking cutoff minutes `policies[].bookingCutoffMinutes` | number field (minutes) | optional | — | min 0 | — | Minutes before the experience after which the bundle is no longer sold. | `setBundleCapacityPolicy` body |
| Allow overbooking `policies[].allowOverbooking` | toggle | optional | off | — | — | — | `setBundleCapacityPolicy` body |
| Allow waitlist `policies[].allowWaitlist` | toggle | optional | off | — | — | — | `setBundleCapacityPolicy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another bundle.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **capacity policy**: Per component, draw from the product's pool or a reserved share. *(source: contracts/satellite/promotions.yaml#setBundleCapacityPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle capacity policy** (data table, from `listBundleCapacityPolicies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Bundle | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Venue | the name it points at, never the id | Where the policy differs by venue for a multi-venue bundle. |
| Partner | the name it points at, never the id | — |
| Capacity source | chip: Shared pool, Dedicated bundle allocation, Channel allocation, Partner allocation … | — |
| Allocation mode | chip: Hard, Soft | Hard allocation is ring-fenced for the bundle; soft is released back when unsold. |
| Capacity ceiling | 1,234 | — |
| Hold duration minutes | 1,234 | How long a temporary reservation of the components lasts. |
| Booking cutoff minutes | 1,234 | Minutes before the experience after which the bundle is no longer sold. |
| Allow overbooking | yes / no (icon or chip) | — |
| Allow waitlist | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save bundle capacity policy (primary button) | `setBundleCapacityPolicy` PUT `/bundles/{bundleId}/capacity-policies` | inline | inline | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another … | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listCapacityPoolReservation` (onLoad, Capacity Pool & Reservation Manager); `listBundleCapacityPolicies` (onLoad, List a bundle's capacity policies)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listCapacityPoolReservation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity pool reservation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity pool reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity pool reservation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another bundle. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  component: Day Pass
  draw: shared pool
  reserved: 0
```

#### Permissions

- `listCapacityPoolReservation` → `PRICE_VIEW` (read) · staff
- `listBundleCapacityPolicies` → `PRODUCT_VIEW` (read) · staff
- `setBundleCapacityPolicy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-191` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-191`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 6: Works in Capacity Pool & Reservation Manager → Manage how bundle sales consume capacity from underlying products. This is particularly important because a bundle must not create artificial inventory separate from the actual attraction/product …

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-191?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save bundle capacity policy.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-192` Dynamic Component Substitution Engine

**Automatically replace unavailable bundle components according to predefined commercial rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each component define; Define whether substitute) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-component-substitution-engine-adm-192` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Replace unavailable components by predefined rules.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listDynamicComponentSubstitution return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDynamicComponentSubstitution carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listDynamicComponentSubstitution; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary component | select field | — | — | — | — | — | — |
| Alternative 1 | select field | — | — | — | — | — | — |
| Alternative 2 | select field | — | — | — | — | — | — |
| Alternative 3 | select field | — | — | — | — | — | — |
| Fallback action | select field | — | — | — | — | — | — |
| Maintains same bundle price | text field | — | — | — | — | — | — |
| Adds surcharge | select field | — | — | — | — | — | — |
| Reduces bundle price | select field | — | — | — | — | — | — |
| Requires customer approval | select field | — | — | — | — | — | — |
| Requires operator approval | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **substitutions**: Component, substitute, value limit. *(source: contracts/satellite/promotions.yaml#listDynamicComponentSubstitution)*

**Data it reads**: `listDynamicComponentSubstitution` (onLoad, Dynamic Component Substitution Engine)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listDynamicComponentSubstitution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic component substitution configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic component substitution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic component substitution configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
substitution:
  from: Planetarium
  to: Aquarium
  valueLimit: same price band
```

#### Permissions

- `listDynamicComponentSubstitution` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-192` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-192`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 8: Works in Dynamic Component Substitution Engine → Automatically replace unavailable bundle components according to predefined commercial rules.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-192?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-193` Dynamic Bundle Rule & Composition Engine

**Allow the actual composition of a bundle to change dynamically according to business and guest conditions. This builds upon the matrix requirement for dynamic bundles where guests select attractions, experiences, F&B, Retail, or services from predefined categories.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-bundle-rule-composition-engine-adm-193` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Bundle composition that changes with conditions (date, guest, availability); the price stays fixed (ADR-0019).

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listDynamicBundleRule return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDynamicBundleRule carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listDynamicBundleRule; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **composition rules**: Conditions to composition. *(source: contracts/satellite/promotions.yaml#listDynamicBundleRule / ADR-0019)*

**Data it reads**: `listDynamicBundleRule` (onLoad, Dynamic Bundle Rule & Composition Engine)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listDynamicBundleRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic bundle rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic bundle rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic bundle rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic bundle rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: On Fridays the show replaces the guided tour
```

#### Permissions

- `listDynamicBundleRule` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-193` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-193`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 10: Works in Dynamic Bundle Rule & Composition Engine → Allow the actual composition of a bundle to change dynamically according to business and guest conditions. This builds upon the matrix requirement for dynamic bundles where guests select attractions …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-193?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-194` Real-Time Availability & Checkout Validation

**Perform the final authoritative validation immediately before transaction confirmation. This is essential because availability may change between browsing and payment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Payment authorization/capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/real-time-availability-checkout-validation-adm-194` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The final availability check just before confirmation, because availability changes between browsing and paying.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRealTimeAvailability return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRealTimeAvailability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **validation results**: Checks with pass or fail. *(source: contracts/satellite/promotions.yaml#listRealTimeAvailability)*

**Data it reads**: `listRealTimeAvailability` (onLoad, Real-Time Availability & Checkout Validation)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listRealTimeAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time availability checkout configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time availability checkout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time availability checkout configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
check:
  basket: Family Fun Bundle x1
  result: passed 14:02:11
```

#### Permissions

- `listRealTimeAvailability` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-194` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-194`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 12: Works in Real-Time Availability & Checkout Validation → Perform the final authoritative validation immediately before transaction confirmation. This is essential because availability may change between browsing and payment.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-194?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-195` Bundle Availability by Channel, Venue & Partner

**Control where a bundle is sellable based on operational availability.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bundleId` (navigation) |
| Route | `/commercial/bundle-availability-by-channel-venue-partner-adm-195` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a bundle may be sold by channel, venue and partner.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listBundleAvailabilityChannel return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBundleAvailabilityChannel carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBundleAvailabilityChannel; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue-specific availability | select field | — | — | — | — | — | — |
| Attraction-specific availability | select field | — | — | — | — | — | — |
| Operating area | select field | — | — | — | — | — | — |
| Country/market | select field | — | — | — | — | — | — |
| Sales location | select field | — | — | — | — | — | — |

**Form: Save bundle capacity policy** (modal, opened by *Save bundle capacity policy*; *Save bundle capacity policy* calls `setBundleCapacityPolicy`, *Cancel* sends nothing)

**Collects what `setBundleCapacityPolicy` sends before it is called.** Required: `policies`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policies `policies` | repeatable rows | required | — | at most 200 | — | — | `setBundleCapacityPolicy` body |
| Bundle `policies[].bundleId` | picker: choose a bundle | required | — | — | shows names, sends the id | — | `setBundleCapacityPolicy` body |
| Channel `policies[].channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setBundleCapacityPolicy` body |
| Venue `policies[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Where the policy differs by venue for a multi-venue bundle. | `setBundleCapacityPolicy` body |
| Partner `policies[].partnerId` | picker: choose a partner | optional | — | — | shows names, sends the id | — | `setBundleCapacityPolicy` body |
| Capacity source `policies[].capacitySource` | select | required | — | Shared pool · Dedicated bundle allocation · Channel allocation · Partner allocation · Event capacity · Timeslot capacity · Seat inventory · Resource capacity | — | — | `setBundleCapacityPolicy` body |
| Allocation mode `policies[].allocationMode` | segmented control | optional | Hard | Hard · Soft | — | Hard allocation is ring-fenced for the bundle; soft is released back when unsold. | `setBundleCapacityPolicy` body |
| Capacity ceiling `policies[].capacityCeiling` | number field | optional | — | min 0 | — | — | `setBundleCapacityPolicy` body |
| Hold duration minutes `policies[].holdDurationMinutes` | number field (minutes) | optional | — | min 1 | — | How long a temporary reservation of the components lasts. | `setBundleCapacityPolicy` body |
| Booking cutoff minutes `policies[].bookingCutoffMinutes` | number field (minutes) | optional | — | min 0 | — | Minutes before the experience after which the bundle is no longer sold. | `setBundleCapacityPolicy` body |
| Allow overbooking `policies[].allowOverbooking` | toggle | optional | off | — | — | — | `setBundleCapacityPolicy` body |
| Allow waitlist `policies[].allowWaitlist` | toggle | optional | off | — | — | — | `setBundleCapacityPolicy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another bundle.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **capacity policy per channel**: Channels using vocabulary labels. *(source: contracts/satellite/promotions.yaml#setBundleCapacityPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle capacity policy** (data table, from `listBundleCapacityPolicies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Bundle | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Venue | the name it points at, never the id | Where the policy differs by venue for a multi-venue bundle. |
| Partner | the name it points at, never the id | — |
| Capacity source | chip: Shared pool, Dedicated bundle allocation, Channel allocation, Partner allocation … | — |
| Allocation mode | chip: Hard, Soft | Hard allocation is ring-fenced for the bundle; soft is released back when unsold. |
| Capacity ceiling | 1,234 | — |
| Hold duration minutes | 1,234 | How long a temporary reservation of the components lasts. |
| Booking cutoff minutes | 1,234 | Minutes before the experience after which the bundle is no longer sold. |
| Allow overbooking | yes / no (icon or chip) | — |
| Allow waitlist | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save bundle capacity policy (primary button) | `setBundleCapacityPolicy` PUT `/bundles/{bundleId}/capacity-policies` | inline | inline | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another … | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listBundleAvailabilityChannel` (onLoad, Bundle Availability by Channel, Venue & Partner); `listBundleCapacityPolicies` (onLoad, List a bundle's capacity policies)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listBundleAvailabilityChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle availability channel configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle availability channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle availability channel configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Two rows share a (channel, venueId, partnerId), there is no default row, or an `id` names a policy of another bundle. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channels:
  Website: true
  Klook: false
```

#### Permissions

- `listBundleAvailabilityChannel` → `PRICE_VIEW` (read) · staff
- `listBundleCapacityPolicies` → `PRODUCT_VIEW` (read) · staff
- `setBundleCapacityPolicy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-195` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-195`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 14: Works in Bundle Availability by Channel, Venue & Partner → Control where a bundle is sellable based on operational availability.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-195?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save bundle capacity policy.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-196` Bundle Availability Forecast, Alerts & Recovery

**Predict bundle availability problems before they affect sales.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-availability-forecast-alerts-recovery-adm-196` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Predict bundle availability problems and alert before sales stop.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listBundleAvailabilityForecast return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBundleAvailabilityForecast carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBundleAvailabilityForecast; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle availability forecast** (data table, from `listBundleAvailabilityForecast`)

| Shows | Format | Notes |
|---|---|---|
| Historical demand | text | Historical demand |
| Current booking velocity | text | Current booking velocity |
| Inventory | text | Inventory |
| Capacity | 1,234 | Capacity |
| Timeslot utilization | 1,234.5 | Timeslot utilization |
| Seasonality | text | Seasonality |
| Day of week | text | Day of week |
| Campaign activity | text | Campaign activity |
| Partner reservations | text | Partner reservations |

**The selected bundle availability forecast** (detail panel): The pack groups this record's detail under its own headings: “Alert Levels”, “AED 186,500”.

| Shows | Format | Notes |
|---|---|---|
| Historical demand | text | Historical demand |
| Current booking velocity | text | Current booking velocity |
| Inventory | text | Inventory |
| Capacity | 1,234 | Capacity |
| Timeslot utilization | 1,234.5 | Timeslot utilization |
| Seasonality | text | Seasonality |
| Day of week | text | Day of week |
| Campaign activity | text | Campaign activity |
| Partner reservations | text | Partner reservations |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **forecast alerts**: Bundle, date, risk, suggested recovery. *(source: contracts/satellite/promotions.yaml#listBundleAvailabilityForecast)*

**Data it reads**: `listBundleAvailabilityForecast` (onLoad, Bundle Availability Forecast, Alerts & Recovery)

**Where the user goes next**

- → `ADM-188` Dynamic Bundle Operations Command Center: *Returns to the board's landing screen*; calls `listBundleAvailabilityForecast`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle availability forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle availability forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle availability forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle availability forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alert:
  bundle: Family Fun Bundle
  date: Sat 29 Nov
  risk: lunch sells out by 11:00
```

#### Permissions

- `listBundleAvailabilityForecast` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-196` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-196`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 16: Works in Bundle Availability Forecast, Alerts & Recovery → Predict bundle availability problems before they affect sales.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-196?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-188`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-197` Dynamic Bundle Simulation & AI Optimization

**Test how a bundle behaves under different operational scenarios before activating dynamic rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-bundle-simulation-ai-optimization-adm-197` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): An operation that runs a dynamic bundle simulation from a scenario sent to it; the screen has only lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test dynamic bundle behaviour under scenarios before activating rules.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listDynamicBundle2, listDynamicBundle, listDynamicBundleRule return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDynamicBundle2, listDynamicBundle, listDynamicBundleRule carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listDynamicBundle2 / contracts/satellite/promotions.yaml#listDynamicBundle / contracts/satellite/promotions.yaml#listDynamicBundleRule; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The simulation is a list with no input. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every dynamic bundle simulation** (data table, from `listDynamicBundle2`)

| Shows | Format | Notes |
|---|---|---|
| Bundle status | 1,234 | Bundle status |
| Components selected | text | Components selected |
| Substitutions | 1,234 | Substitutions |
| Price impact | AED 1,234.50 | Price impact |
| Margin impact | 1,234.5 | Margin impact |
| Capacity impact | 1,234 | Capacity impact |
| Customer impact | text | Customer impact |
| Revenue impact | AED 1,234.50 | Revenue impact |

**The selected dynamic bundle simulation** (detail panel): The pack groups this record's detail under its own headings: “Scenario A”, “Scenario B”, “Scenario C”, “Scenario D”, “Scenario E”, “Photo”.

| Shows | Format | Notes |
|---|---|---|
| Bundle status | 1,234 | Bundle status |
| Components selected | text | Components selected |
| Substitutions | 1,234 | Substitutions |
| Price impact | AED 1,234.50 | Price impact |
| Margin impact | 1,234.5 | Margin impact |
| Capacity impact | 1,234 | Capacity impact |
| Customer impact | text | Customer impact |
| Revenue impact | AED 1,234.50 | Revenue impact |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scenario results**: Scenario and outcome per bundle. *(source: contracts/satellite/promotions.yaml#listDynamicBundle2)*

**Data it reads**: `listDynamicBundle2` (onLoad, Dynamic Bundle Simulation & AI Optimization); `listDynamicBundle` (onLoad, Dynamic Bundle Operations Command Center); `listDynamicBundleRule` (onLoad, Dynamic Bundle Rule & Composition Engine)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic bundle simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic bundle simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic bundle simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic bundle simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario: 'Planetarium closed: substitution applied to 38 bundles'
```

#### Permissions

- `listDynamicBundle2` → `PRICE_VIEW` (read) · staff
- `listDynamicBundle` → `PRICE_VIEW` (read) · staff
- `listDynamicBundleRule` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-197` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-197`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 6
- Flow F159 *Promotions Bundles Management board 6: Dynamic Bundle Operations Command Center*, step 18: Works in Dynamic Bundle Simulation & AI Optimization → Test how a bundle behaves under different operational scenarios before activating dynamic rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-197?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_VIEW`.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getInventoryKitDefinition": {"method":"GET","path":"/inventory-items/{itemId}/kit-definition","contract":"inventory","summary":"The components a kit item is made of","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InventoryKitDefinition"},
"listBundleAvailabilityChannel": {"method":"GET","path":"/bundle-availability-channel","contract":"promotions","summary":"Bundle Availability by Channel, Venue & Partner","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleAvailabilityByChannelVenuePartnerView"},
"listBundleAvailabilityForecast": {"method":"GET","path":"/bundle-availability-forecast","contract":"promotions","summary":"Bundle Availability Forecast, Alerts & Recovery","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BundleAvailabilityForecastAlertsRecoveryView"},
"listBundleCapacityPolicies": {"method":"GET","path":"/bundles/{bundleId}/capacity-policies","contract":"promotions","summary":"List a bundle's capacity policies","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBundleSellabilityDependency": {"method":"GET","path":"/bundle-sellability-dependency","contract":"promotions","summary":"Bundle Sellability & Dependency Rule Engine","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSellabilityDependencyRuleEngineView"},
"listCapacityPoolReservation": {"method":"GET","path":"/capacity-pool-reservation","contract":"promotions","summary":"Capacity Pool & Reservation Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CapacityPoolReservationManagerView"},
"listComponentInventoryAvailability": {"method":"GET","path":"/component-inventory-availability","contract":"promotions","summary":"Component Inventory & Availability Matrix","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ComponentInventoryAvailabilityMatrixView"},
"listDynamicBundle": {"method":"GET","path":"/dynamic-bundle","contract":"promotions","summary":"Dynamic Bundle Operations Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DynamicBundleOperationsCommandCenterView"},
"listDynamicBundle2": {"method":"GET","path":"/dynamic-bundle-2","contract":"promotions","summary":"Dynamic Bundle Simulation & AI Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DynamicBundleSimulationAiOptimizationView"},
"listDynamicBundleRule": {"method":"GET","path":"/dynamic-bundle-rule","contract":"promotions","summary":"Dynamic Bundle Rule & Composition Engine","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DynamicBundleRuleCompositionEngineView"},
"listDynamicComponentSubstitution": {"method":"GET","path":"/dynamic-component-substitution","contract":"promotions","summary":"Dynamic Component Substitution Engine","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DynamicComponentSubstitutionEngineView"},
"listRealTimeAvailability": {"method":"GET","path":"/real-time-availability","contract":"promotions","summary":"Real-Time Availability & Checkout Validation","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RealTimeAvailabilityCheckoutValidationView"},
"setBundleCapacityPolicy": {"method":"PUT","path":"/bundles/{bundleId}/capacity-policies","contract":"promotions","summary":"Set a bundle's capacity policies","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BundleAvailabilityByChannelVenuePartnerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Availability by Channel, Venue & Partner displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelsType":{"type":"string","enum":["b2c","b2b","pos","mobilePos","mobileApp","kiosk","callCenter","api","ota","reseller","partner"],"description":"Vocabulary listed under Channels."},"venueSpecificAvailability":{"type":"string","description":"Venue-specific availability"},"attractionSpecificAvailability":{"type":"string","description":"Attraction-specific availability"},"operatingArea":{"type":"string","description":"Operating area"},"countryMarket":{"type":"string","description":"Country/market"},"salesLocation":{"type":"string","description":"Sales location"},"dedicatedAllocation":{"type":"string","description":"Dedicated allocation"},"sharedAllocation":{"type":"string","description":"Shared allocation"},"capacityCeiling":{"type":"integer","description":"Capacity ceiling"},"bookingCutoff":{"type":"string","description":"Booking cutoff"}}},
"BundleAvailabilityForecastAlertsRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Availability Forecast, Alerts & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"historicalDemand":{"type":"string","description":"Historical demand"},"currentBookingVelocity":{"type":"string","description":"Current booking velocity"},"inventory":{"type":"string","description":"Inventory"},"capacity":{"type":"integer","description":"Capacity"},"timeslotUtilization":{"type":"number","description":"Timeslot utilization"},"seasonality":{"type":"string","description":"Seasonality"},"dayOfWeek":{"type":"string","description":"Day of week"},"campaignActivity":{"type":"string","description":"Campaign activity"},"partnerReservations":{"type":"string","description":"Partner reservations"},"levelsType":{"type":"string","enum":["information","warning","critical"],"description":"Vocabulary listed under Alert Levels."},"switchChoiceGroup":{"type":"string","description":"Switch choice group"},"restrictChannel":{"type":"string","description":"Restrict channel"},"reduceBundleAllocation":{"type":"string","description":"Reduce bundle allocation"},"increaseAlternativeInventory":{"type":"string","description":"Increase alternative inventory"},"recommendAnotherTimeslot":{"type":"string","description":"Recommend another timeslot"},"potentialRevenueRecoverableThroughSubstitution":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Potential Revenue Recoverable Through Substitution"}}},
"BundleCapacityPolicy": {"x-ticvai-persistence":"promotions.bundle_capacity_policy","type":"object","description":"How a bundle draws on capacity, per channel where it differs: the capacity source, dedicated or shared and hard or soft allocation, the ceiling, how long a hold lasts, the booking cut-off, and whether overbooking or a waitlist is allowed (Capacity Pool & Reservation Manager; Bundle Availability by Channel, Venue & Partner). The capacity itself is the catalogue's (`catalogue.channel_capacity`, `catalogue.inventory_hold`). A row with no channel is the bundle's default. (DM5, 29 September: data model for the agreed operations)\n**Written by setBundleCapacityPolicy; read by listBundleCapacityPolicies, listCapacityPoolReservation and listBundleAvailabilityChannel** (decided 29 September, writers pass).","required":["id","bundleId","capacitySource"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bundleId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the policy differs by venue for a multi-venue bundle."},"partnerId":{"type":"string","format":"uuid","nullable":true},"capacitySource":{"type":"string","enum":["sharedPool","dedicatedBundleAllocation","channelAllocation","partnerAllocation","eventCapacity","timeslotCapacity","seatInventory","resourceCapacity"]},"allocationMode":{"type":"string","enum":["hard","soft"],"default":"hard","description":"Hard allocation is ring-fenced for the bundle; soft is released back when unsold."},"capacityCeiling":{"type":"integer","minimum":0,"nullable":true},"holdDurationMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"How long a temporary reservation of the components lasts."},"bookingCutoffMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Minutes before the experience after which the bundle is no longer sold."},"allowOverbooking":{"type":"boolean","default":false},"allowWaitlist":{"type":"boolean","default":false}}},
"BundleSellabilityDependencyRuleEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Sellability & Dependency Rule Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dependencyRule":{"type":"string","enum":["allComponentsRequired","atLeastXOfY","atLeastOneFromCategory","optionalComponent","conditionalComponent","substituteAllowed","partnerComponentRequired"],"description":"The sellability rule."},"bundleId":{"type":"string","description":"Bundle ID"},"componentIds":{"type":"array","items":{"type":"string"},"description":"Components the rule covers"},"minimumCount":{"type":"integer","description":"For atLeastXOfY: X"}}},
"CapacityPoolReservationManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Capacity Pool & Reservation Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"temporaryReservation":{"type":"string","description":"Temporary reservation"},"holdDuration":{"type":"string","format":"date-time","description":"Hold duration"},"hardAllocation":{"type":"string","description":"Hard allocation"},"softAllocation":{"type":"string","description":"Soft allocation"},"overbookingPolicy":{"type":"string","description":"Overbooking policy"},"waitlistBehavior":{"type":"string","description":"Waitlist behavior"},"capacitySource":{"type":"string","enum":["sharedPool","dedicatedBundleAllocation","channelAllocation","partnerAllocation","eventCapacity","timeslotCapacity","seatInventory","resourceCapacity"],"description":"Capacity source."}}},
"ComponentInventoryAvailabilityMatrixView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Component Inventory & Availability Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"availabilitySource":{"type":"string","enum":["ticketInventory","attractionCapacity","eventCapacity","seatInventory","timeslots","fBAvailability","retailStock","resourceAvailability","parking","rental","externalPartnerApi"],"description":"Where the component's availability comes from."},"componentStatus":{"type":"string","enum":["available","limited","low","soldOut","closed","suspended","unpublished","apiUnavailable"],"description":"Component status."},"componentId":{"type":"string","description":"Component ID"},"componentName":{"type":"string","description":"Component"},"inventory":{"type":"integer","description":"Inventory"},"capacity":{"type":"integer","description":"Capacity"},"schedule":{"type":"string","description":"Schedule"}}},
"DynamicBundleOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Dynamic Bundle Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeDynamicBundles":{"type":"integer","description":"Active Dynamic Bundles"},"sellableBundles":{"type":"integer","description":"Sellable Bundles"},"partiallyAvailableBundles":{"type":"integer","description":"Partially Available Bundles"},"unavailableBundles":{"type":"integer","description":"Unavailable Bundles"},"bundlesWithLowCapacity":{"type":"integer","description":"Bundles with Low Capacity"},"componentsSoldOut":{"type":"string","description":"Components Sold Out"},"substitutionsTriggered":{"type":"string","description":"Substitutions Triggered"},"bundleSalesToday":{"type":"string","description":"Bundle Sales Today"},"failedBundleAttempts":{"type":"integer","description":"Failed Bundle Attempts"},"capacityReserved":{"type":"integer","description":"Capacity Reserved"},"revenueAtRisk":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue at Risk"},"recoveredRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recovered Revenue"},"unavailable":{"type":"string","description":"Unavailable"},"health":{"type":"string","enum":["healthy","warning","critical"],"description":"Bundle health."}}},
"DynamicBundleRuleCompositionEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Dynamic Bundle Rule & Composition Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"guestSegment":{"type":"string","description":"Guest segment"},"membership":{"type":"string","description":"Membership"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"purchaseHistory":{"type":"string","description":"Purchase history"},"numberOfGuests":{"type":"integer","description":"Number of guests"},"guestType":{"type":"string","description":"Guest type"},"salesChannel":{"type":"string","description":"Sales channel"},"venue":{"type":"string","description":"Venue"},"season":{"type":"string","description":"Season"},"day":{"type":"string","description":"Day"},"time":{"type":"string","format":"date-time","description":"Time"},"capacity":{"type":"integer","description":"Capacity"},"inventory":{"type":"string","description":"Inventory"},"campaign":{"type":"string","description":"Campaign"},"productPopularity":{"type":"string","description":"Product popularity"}}},
"DynamicBundleSimulationAiOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Dynamic Bundle Simulation & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bundleStatus":{"type":"integer","description":"Bundle status"},"componentsSelected":{"type":"string","description":"Components selected"},"substitutions":{"type":"integer","description":"Substitutions"},"priceImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price impact"},"marginImpact":{"type":"number","description":"Margin impact"},"capacityImpact":{"type":"integer","description":"Capacity impact"},"customerImpact":{"type":"string","description":"Customer impact"},"revenueImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue impact"}}},
"DynamicComponentSubstitutionEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Dynamic Component Substitution Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"primaryComponent":{"type":"string","description":"Primary component"},"alternative1":{"type":"string","description":"Alternative 1"},"alternative2":{"type":"string","description":"Alternative 2"},"alternative3":{"type":"string","description":"Alternative 3"},"fallbackAction":{"type":"string","description":"Fallback action"},"maintainsSameBundlePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maintains same bundle price"},"addsSurcharge":{"type":"string","description":"Adds surcharge"},"reducesBundlePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Reduces bundle price"},"requiresCustomerApproval":{"type":"string","description":"Requires customer approval"},"requiresOperatorApproval":{"type":"string","description":"Requires operator approval"},"substitutionTriggers":{"type":"array","items":{"type":"string","enum":["soldOut","capacityExhausted","productSuspended","venueClosed","externalApiUnavailable","inventoryBelowThreshold"]},"description":"When substitution may occur."}}},
"InventoryKitComponent": {"x-ticvai-persistence":"inventory.kit_component","type":"object","description":"4.4.20. One component of a kit and the quantity one kit consumes.","required":["componentItemId","quantity"],"properties":{"kitItemId":{"type":"string","format":"uuid","readOnly":true},"componentItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"unit":{"type":"string","nullable":true,"description":"The component's base unit where omitted."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the kit item's venue scope."}}},
"InventoryKitDefinition": {"x-ticvai-persistence":"none — composed of the item's inventory.kit_component rows","type":"object","description":"4.4.20. Also the `setInventoryKitDefinition` body.","required":["components"],"properties":{"kitItemId":{"type":"string","format":"uuid","readOnly":true},"components":{"type":"array","items":{"$ref":"#/components/schemas/InventoryKitComponent"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RealTimeAvailabilityCheckoutValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"failedChecks":{"type":"array","items":{"type":"string","enum":["productInactive","inventoryUnavailable","capacityUnavailable","timeslotUnavailable","resourceUnavailable","priceInvalid","promotionInvalid","partnerComponentInvalid","componentMappingInvalid"]},"description":"Checkout validations that failed; empty means the bundle is sellable."},"bundleId":{"type":"string","description":"Bundle ID"},"sellable":{"type":"boolean","description":"Whether the bundle can be sold now"}}}
}
```
