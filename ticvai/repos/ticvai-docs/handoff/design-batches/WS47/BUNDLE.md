# WS47 — Promotions   Bundles Management board 3

**10 screens · 12 operations · 16 schemas · 2 permissions**

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
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-158` | Coupon & Promo Code Command Center | B–D | 0 | 16 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-159` | Coupon & Promo Code Builder | B–D | 9 | 20 | 5 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-160` | Unique Code Generation & Batch Manager | B–D | 14 | 12 | 5 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-161` | Code Eligibility & Restriction Manager | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-162` | Usage, Capacity & Frequency Control | B–D | 0 | 8 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-163` | Validity, Date & Time Control | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-164` | Code Distribution & Assignment Manager | A | 0 | 36 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-165` | Redemption Monitor & Code Lookup | B–D | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-166` | Code Security, Fraud & Exception Center | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-167` | Redemption Analytics, Audit & AI Optimization | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-161, ADM-162, ADM-163, ADM-165, ADM-166 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-158` Coupon & Promo Code Command Center

**Provide the central operational dashboard for all coupon, promo-code, and promotional voucher activities. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `campaignId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/venue-operations/promotions-coupons/coupon-promo-code-command-center-adm-158` |

**What the spec says about it.** **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Draft, Pending Approval, Capacity Reached. Each needs an operation, or needs removing from the screen; this …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The hub of the coupon and promo-code board: campaigns, generated codes and their states (issued, assigned, redeemed, expired, voided).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Draft, Pending Approval, Capacity Reached. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Code Campaigns** (metric tile)

**Active Coupons** (metric tile)

**Unique Codes Issued** (metric tile)

**Codes Redeemed** (metric tile)

**Redemption Rate** (metric tile)

**Unused Codes** (metric tile)

**Expired Codes** (metric tile)

**Suspended Codes** (metric tile)

**Remaining Redemption Capacity** (metric tile)

**Discount Granted** (metric tile)

**Revenue Generated** (metric tile)

**Average Order Value** (metric tile)

**Fraud/Suspicious Usage Alerts** (metric tile)

**Every coupon promo code** (data table, from `listCouponCodes`)

| Shows | Format | Notes |
|---|---|---|
| Top performing codes | text | not in the schema: `Top-performing codes` |
| Redemption trend | text | not in the schema: `Redemption trend` |
| Redemption by channel | text | not in the schema: `Redemption by channel` |
| Redemption by venue | text | not in the schema: `Redemption by venue` |
| Redemption by partner | text | not in the schema: `Redemption by partner` |
| Redemption by customer segment | text | not in the schema: `Redemption by customer segment` |
| Discount exposure | text | not in the schema: `Discount exposure` |
| Campaign budget consumption | text | not in the schema: `Campaign budget consumption` |

**The selected coupon promo code** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Top performing codes | text | not in the schema: `Top-performing codes` |
| Redemption trend | text | not in the schema: `Redemption trend` |
| Redemption by channel | text | not in the schema: `Redemption by channel` |
| Redemption by venue | text | not in the schema: `Redemption by venue` |
| Redemption by partner | text | not in the schema: `Redemption by partner` |
| Redemption by customer segment | text | not in the schema: `Redemption by customer segment` |
| Discount exposure | text | not in the schema: `Discount exposure` |
| Campaign budget consumption | text | not in the schema: `Campaign budget consumption` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Draft (primary button) | navigation or local | — | — | — | — |
| Pending Approval (secondary button) | navigation or local | — | — | — | — |
| Capacity Reached (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **code state summary**: Counts by state per campaign; a code lookup box at the top. *(source: contracts/satellite/promotions.yaml#listCouponCodes / contracts/satellite/promotions.yaml#/components/schemas/CouponStatus)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-161` Code Eligibility & Restriction Manager: *Works in Code Eligibility & Restriction Manager*; calls `listCouponCodes`
- → `ADM-162` Usage, Capacity & Frequency Control: *Works in Usage, Capacity & Frequency Control*; calls `listCouponCodes`
- → `ADM-163` Validity, Date & Time Control: *Works in Validity, Date & Time Control*; calls `listCouponCodes`
- → `ADM-165` Redemption Monitor & Code Lookup: *Works in Redemption Monitor & Code Lookup*; calls `listCouponCodes`
- → `ADM-166` Code Security, Fraud & Exception Center: *Works in Code Security, Fraud & Exception Center*; calls `listCouponCodes`
- → `ADM-167` Redemption Analytics, Audit & AI Optimization: *Works in Redemption Analytics, Audit & AI Optimization*; calls `listCouponCodes`
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `campaignId`, `code`
- → `ADM-159` Coupon & Promo Code Builder: *Works in Coupon & Promo Code Builder, a section of BO-010, which saves the record with createCouponCampaign…*; calls `listCouponCodes`
- → `ADM-160` Unique Code Generation & Batch Manager: *Works in Unique Code Generation & Batch Manager*; carries `batchId`, `campaignId`; calls `listCouponCodes`
- → `ADM-164` Code Distribution & Assignment Manager: *Works in Code Distribution & Assignment Manager*; carries `campaignId`; calls `listCouponCodes`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The coupon promo code list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the coupon promo code untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No coupon promo code yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the coupon promo code are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  code: INSTA-DUNE
  issued: 5000
  assigned: 1200
  redeemed: 412
  voided: 3
```

#### Permissions

- `listCouponCodes` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-158` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-158`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 1: Opens Coupon & Promo Code Command Center → Provide the central operational dashboard for all coupon, promo-code, and promotional voucher activities.
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F156 branch at step 1 (expected): when Nothing has been set up on Coupon & Promo Code Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F156 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-158?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Draft, Pending Approval, Capacity Reached.
- [ ] Every transition is wired: `BO-100`, `ADM-161`, `ADM-162`, `ADM-163`, `ADM-165`, `ADM-166`, `ADM-167`, `BO-010`, `ADM-159`, `ADM-160`, `ADM-164`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-159` Coupon & Promo Code Builder

**Create the commercial definition of a coupon or promo-code campaign. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/coupon-promo-code-builder-adm-159` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setCouponPromoCode` duplicated BO-010 Promotions & Coupons's createCouponCampaign and generateCouponCodes, so it is removed from the contract (BC-012) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The commercial definition of a code campaign: the kind of code (common promo code, unique codes, coupon, voucher, free-ticket code, partner, employee, influencer, compensation, bulk), what it grants, value, maximum discount, eligible products, channels and dates. The discount itself is calculated by the promotion engine, not duplicated here.

**Fixed on main** (the package already carries these; draw what it says): setCouponPromoCode duplicates createCouponCampaign and types campaign and eligibleProducts as plain strings. (CHG-CLN-001); No read operation: the screen declares only setCouponPromoCode and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Percentage discount | select field | — | — | — | — | — | — |
| Fixed-value discount | select field | — | — | — | — | — | — |
| Fixed promotional price | select field | — | — | — | — | — | — |
| Free product | select field | — | — | — | — | — | — |
| Free ticket | select field | — | — | — | — | — | — |
| Free add-on | select field | — | — | — | — | — | — |
| Upgrade | select field | — | — | — | — | — | — |
| Bundle benefit | select field | — | — | — | — | — | — |
| Added value | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **codeType**: Shown as cards with one line each; a common code asks for the code text, unique codes ask for a pattern (prefix and length). *(source: contracts/satellite/promotions.yaml#/components/schemas/CouponPromoCodeBuilderInput / DI-173)*
- **benefitValue**: A percentage or an amount depending on the benefit type; amount in the region's currency (PR-2). *(source: contracts/satellite/promotions.yaml#/components/schemas/CouponPromoCodeBuilderInput)*

#### Outputs: what the screen shows and produces

**Shown**

**Coupon campaigns** (data table, from `listCouponCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Kind | chip: Percentage, Fixed amount, Fixed price, Buy x get y, Free item, Tiered percentage | — |
| Percentage | 12.5% | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fixed price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Buy quantity | 1,234 | — |
| Get quantity | 1,234 | — |
| Get discount percentage | 1,234.5 | 100 makes the free items actually free; lower values give a partial discount. |
| Tiers | list or chips (count when long) | For `tieredPercentage` — more units, larger discount. |
| Max discount amount | AED 1,234.50 | Cap on a percentage discount. Prevents an unbounded discount on a large basket. |
| Reward variants | list or chips (count when long) | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` … |
| Max applications per basket | 1,234 | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (createPromotion; setFixedPriceOffer was … |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Variants | list or chips (count when long) | — |
| Product kinds | list or chips (count when long) | — |
| Categorys | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCouponCampaigns` (onLoad, The coupon campaigns, to open one in the builder)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*; carries `campaignId`
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `campaignId`, `code`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The coupon promo code configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the coupon promo code untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No coupon promo code configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-010`: Coupon campaigns on P08 are the same thing; same wording for shared vs unique codes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  codeType: influencerAffiliateCode
  code: SARA15
  benefit: 15% off
  maximumDiscount: AED 150.00
  channels:
  - Website
  - App
  valid: 2026-11-01 to 2026-12-31
```

#### Permissions

- `listCouponCampaigns` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-159` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-159`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 2: Works in Coupon & Promo Code Builder, a section of BO-010, which saves the record with createCouponCampaign and … → Create the commercial definition of a coupon or promo-code campaign.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-159?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-158`, `BO-010`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-160` Unique Code Generation & Batch Manager

**Generate and manage large quantities of secure unique promotional codes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Users define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `campaignId` (navigation), `batchId` (navigation) |
| Route | `/commercial/unique-code-generation-batch-manager-adm-160` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Unique Code Generation & Batch Manager declares no operation that writes anything** — its only declared call is `listUniqueCodeGeneration`, a read. The name promises authoring and the contract …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Batches of unique codes: how many, length, prefix and suffix, character set, case sensitivity, expiry, uses, distribution owner, and generated, remaining and redeemed per batch. Generation is asynchronous, up to 50,000 a time, delivered as a file.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listUniqueCodeGeneration return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): No write operation: a configuration screen (Unique Code Generation & Batch Manager) declares only reads (listUniqueCodeGeneration). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Campaign | select field | — | — | — | — | — | — |
| Number of codes | select field | — | — | — | — | — | — |
| Code length | select field | — | — | — | — | — | — |
| Prefix | select field | — | — | — | — | — | — |
| Suffix | select field | — | — | — | — | — | — |
| Character type | select field | — | — | — | — | — | — |
| Case sensitivity | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Number of uses | select field | — | — | — | — | — | — |
| Distribution owner | select field | — | — | — | — | — | — |

**Form: Generate codes** (modal, opened by *Generate codes*; *Generate codes* calls `generateCouponCodes`, *Cancel* sends nothing)

**Collects what `generateCouponCodes` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Quantity `quantity` | number field | required | — | min 1; max 50000 | — | — | `generateCouponCodes` body |
| Prefix `prefix` | text field | optional | — | max length 16 | — | — | `generateCouponCodes` body |
| Length `length` | stepper or slider | optional | 12 | min 6; max 32 | — | — | `generateCouponCodes` body |
| Assign to subjects `assignToSubjectIds` | multi-picker: choose assign to subjects | optional | — | at most 50000 | — | Personalised codes bound to named guests. Omit for anonymous codes. | `generateCouponCodes` body |

Errors to draw in the form: 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101)

#### Outputs: what the screen shows and produces

**Shown**

**Batch progress** (detail panel, from `getCouponCodeBatch`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The `batchId` that `generateCouponCodes` returned. |
| Campaign | the name it points at, never the id | — |
| Quantity | 1,234 | Codes requested. |
| Generated count | 1,234 | Codes generated so far. |
| Prefix | text | — |
| Length | 1,234 | — |
| Status | chip: Queued, Generating, Complete, Failed | — |
| Failure reason | text | Present only where status is `failed`. |
| Requested by principal | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Download URL | text | The exported file of the batch's codes. Signed and expiring, issued on each read, so it is not stored. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Generate codes (secondary button) | `generateCouponCodes` POST `/coupon-campaigns/{campaignId}/codes` | inline | inline | 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **batch list**: Batch, campaign, quantity, generated by and when, status (queued, generating, complete, failed), download when complete. *(source: contracts/satellite/promotions.yaml#listUniqueCodeGeneration / contracts/satellite/promotions.yaml#generateCouponCodes)*

**Data it reads**: `listUniqueCodeGeneration` (onLoad, Unique Code Generation & Batch Manager)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*; carries `campaignId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unique code generation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unique code generation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unique code generation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
batch:
  id: B-2026-118
  campaign: INSTA-DUNE
  quantity: 5000
  length: 8
  prefix: DUNE-
  generated: 2026-11-02 by Noura Saeed
  remaining: 3800
```

#### Permissions

- `listUniqueCodeGeneration` → `PRICE_VIEW` (read) · staff
- `generateCouponCodes` → `PRICE_CONFIGURE` (configure) · staff
- `getCouponCodeBatch` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.11 | The system should be able to have restrictions in Transaction level with respect to usage of promo codes to once per booking. | Admission and Access | CONTRACTED | `generateCouponCodes` |
| 3.6.13 | The system should be able to operate promo codes with these abilities: - Can be restricted to 1 use or multiple - Common/Unique code - Date limited - start and end date - Time duration specific - … | Admission and Access | CONTRACTED | `generateCouponCodes` |
| 3.6.24 | The system should be able to setup of promo codes to either be unique or common | Admission and Access | CONTRACTED | `generateCouponCodes` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-160` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-160`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 4: Works in Unique Code Generation & Batch Manager → Generate and manage large quantities of secure unique promotional codes.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-160?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Generate codes.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-161` Code Eligibility & Restriction Manager

**Determine where, when, by whom, and against what a code can be redeemed. The matrix explicitly requires promo codes to support restrictions for usage, dates, duration, capacity, frequency, location, group, partner, operating area, and sales channel.**

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
| Route | `/commercial/code-eligibility-restriction-manager-adm-161` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Code Eligibility & Restriction Manager declares no operation that writes anything** — its only declared call is `listCodeEligibilityRestriction`, a read. The name promises authoring and the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where, by whom and against what a code may be redeemed: partner, business entity, venue, location, operating area, products, customers, channels.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCodeEligibilityRestriction return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCodeEligibilityRestriction carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Code Eligibility & Restriction Manager) declares only reads (listCodeEligibilityRestriction). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **restriction summary**: The restrictions as a sentence per campaign. *(source: contracts/satellite/promotions.yaml#listCodeEligibilityRestriction)*

**Data it reads**: `listCodeEligibilityRestriction` (onLoad, Code Eligibility & Restriction Manager)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The code eligibility restriction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the code eligibility restriction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No code eligibility restriction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the code eligibility restriction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
restriction: 'INSTA-DUNE: Dune Park only, Website and App, Day Pass products, new guests'
```

#### Permissions

- `listCodeEligibilityRestriction` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-161` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-161`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 6: Works in Code Eligibility & Restriction Manager → Determine where, when, by whom, and against what a code can be redeemed. The matrix explicitly requires promo codes to support restrictions for usage, dates, duration, capacity, frequency, location …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-161?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-162` Usage, Capacity & Frequency Control

**Control exactly how frequently and how many times promotional codes may be redeemed.**

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
| Route | `/commercial/usage-capacity-frequency-control-adm-162` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listUsageCapacityFrequency lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How often codes may be redeemed: total, per customer, per account, per transaction, per day, per channel, per venue, with issued, redeemed, reserved pending and remaining.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listUsageCapacityFrequency return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listUsageCapacityFrequency carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Usage, Capacity & Frequency Control) declares only reads (listUsageCapacityFrequency). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every usage capacity frequency** (data table, from `listUsageCapacityFrequency`)

| Shows | Format | Notes |
|---|---|---|
| Issued | 1,234 | Codes issued |
| Redeemed | 1,234 | Codes redeemed |
| Reserved pending | 1,234 | Codes reserved or pending |
| Remaining | 1,234 | Codes remaining |

**The selected usage capacity frequency** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Issued | 1,234 | Codes issued |
| Redeemed | 1,234 | Codes redeemed |
| Reserved pending | 1,234 | Codes reserved or pending |
| Remaining | 1,234 | Codes remaining |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **limits with consumption**: Each limit with a consumption bar. *(source: contracts/satellite/promotions.yaml#listUsageCapacityFrequency)*

**Data it reads**: `listUsageCapacityFrequency` (onLoad, Usage, Capacity & Frequency Control)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage capacity frequency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage capacity frequency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage capacity frequency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the usage capacity frequency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
limits:
  total: 5000
  perCustomer: 1
  perDay: 300
  redeemed: 412
  reservedPending: 18
```

#### Permissions

- `listUsageCapacityFrequency` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-162` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-162`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 8: Works in Usage, Capacity & Frequency Control → Control exactly how frequently and how many times promotional codes may be redeemed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-162?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-163` Validity, Date & Time Control

**Control the temporal validity of coupons and codes.**

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
| Route | `/commercial/validity-date-time-control-adm-163` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listValidityDateTime lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When codes are valid: blackout dates, holidays, slots, events, seasonal calendars and the grace period after expiry.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listValidityDateTime return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listValidityDateTime carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Validity, Date & Time Control) declares only reads (listValidityDateTime). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **validity calendar**: Valid and blacked-out days on a month calendar. *(source: contracts/satellite/promotions.yaml#listValidityDateTime / DI-919)*

**Data it reads**: `listValidityDateTime` (onLoad, Validity, Date & Time Control)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validity date time list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validity date time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validity date time yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validity date time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
validity:
  blackout:
  - '2026-12-02'
  - '2026-12-31'
  gracePeriodHours: 24
```

#### Permissions

- `listValidityDateTime` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-163` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-163`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 10: Works in Validity, Date & Time Control → Control the temporal validity of coupons and codes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-163?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-164` Code Distribution & Assignment Manager

**Manage how promotional codes are allocated and distributed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-ADM-164 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/commercial/code-distribution-assignment-manager-adm-164` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How codes reach people: assign a batch or part of it to a customer, segment, membership account, company, reseller, travel agency, school, hotel, bank or partner, and send it through a channel (email, SMS, WhatsApp, app, CRM journey, portals, POS, call centre, API, exported batch). The funnel generated, assigned, sent, delivered, viewed, redeemed is the output.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The funnel counts generated, assigned, sent, delivered, viewed and redeemed are typed as strings. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setCodeDistributionManager and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Issued · Assigned · Redeemed · Expired · Voided | `listCouponCodes` ?status |
| Batch | picker: choose a batch | — | — | `listCouponCodes` ?batchId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **assignee**: Assignee type first, then a picker of that type's records; quantity cannot exceed unassigned codes in the batch. *(source: contracts/satellite/promotions.yaml#setCodeDistributionManager / R101)*

#### Outputs: what the screen shows and produces

**Shown**

**Every code distribution** (data table, from `setCodeDistributionManager`)

| Shows | Format | Notes |
|---|---|---|
| Generated | text | Generated |
| Assigned | text | Assigned |
| Sent | text | Sent |
| Delivered | text | Delivered |
| Viewed | text | Viewed where available |
| Redeemed | text | Redeemed |
| Expired | 1,234 | Expired |
| Cancelled | 1,234 | Cancelled |

**Codes** (data table, from `listCouponCodes`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Code | text | — |
| Campaign | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `generateCouponCodes` batch that issued this code. Null where no batch did. |
| Status | chip: Issued, Assigned, Redeemed, Expired, Voided | — |
| Assigned subject | the name it points at, never the id | — |
| Redemption count | 1,234 | — |
| Max redemptions | 1,234 | — |
| Discount | grouped details | — |
| Kind | chip: Percentage, Fixed amount, Fixed price, Buy x get y, Free item, Tiered percentage | — |
| Percentage | 12.5% | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fixed price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Buy quantity | 1,234 | — |
| Get quantity | 1,234 | — |
| Get discount percentage | 1,234.5 | 100 makes the free items actually free; lower values give a partial discount. |
| Tiers | list or chips (count when long) | For `tieredPercentage` — more units, larger discount. |
| Max discount amount | AED 1,234.50 | Cap on a percentage discount. Prevents an unbounded discount on a large basket. |
| Reward variants | list or chips (count when long) | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` … |
| Max applications per basket | 1,234 | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (createPromotion; setFixedPriceOffer was … |

**The selected code distribution** (detail panel): The pack groups this record's detail under its own headings: “Distribution Channels”, “Codes may be assigned to”, “External Partner Example”.

| Shows | Format | Notes |
|---|---|---|
| Generated | text | Generated |
| Assigned | text | Assigned |
| Sent | text | Sent |
| Delivered | text | Delivered |
| Viewed | text | Viewed where available |
| Redeemed | text | Redeemed |
| Expired | 1,234 | Expired |
| Cancelled | 1,234 | Cancelled |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **distribution funnel**: Generated, assigned, sent, delivered, viewed, redeemed, expired, cancelled as a horizontal funnel per batch. *(source: contracts/satellite/promotions.yaml#setCodeDistributionManager)*

**Data it reads**: `listCouponCodes` (onLoad, The campaign's codes and who each is assigned to)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*; carries `campaignId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The code distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the code distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No code distribution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the code distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
distribution:
  batch: INSTA-DUNE unique 5,000
  assignee: 'Segment: Annual pass holders'
  channel: email
  quantity: 1200
  delivered: 1164
  redeemed: 212
```

#### Permissions

- `setCodeDistributionManager` → `PRICE_CONFIGURE` (configure) · staff
- `listCouponCodes` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-164` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-164`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 12: Works in Code Distribution & Assignment Manager → Manage how promotional codes are allocated and distributed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-164?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-165` Redemption Monitor & Code Lookup

**Provide real-time operational visibility into coupon and promo-code redemption.**

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
| Route | `/commercial/redemption-monitor-code-lookup-adm-165` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Real-time redemptions and a lookup of any code: when, where, on what, original and final value, operator and device, and the validation result.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listRedemptionCodeLookup return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listRedemptionCodeLookup carry no identifier. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Promo code | text field | — | — | `listRedemptionCodeLookup` ?promoCode |
| Coupon | text field | — | — | `listRedemptionCodeLookup` ?couponId |
| Batch | text field | — | — | `listRedemptionCodeLookup` ?batchId |
| Transaction | text field | — | — | `listRedemptionCodeLookup` ?transaction |
| Booking | text field | — | — | `listRedemptionCodeLookup` ?booking |
| Customer | text field | — | — | `listRedemptionCodeLookup` ?customer |
| Partner | text field | — | — | `listRedemptionCodeLookup` ?partner |
| Campaign | text field | — | — | `listRedemptionCodeLookup` ?campaign |
| Customer account reference | text field | — | — | `listRedemptionCodeLookup` ?customerAccountReference |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every redemption code lookup** (data table, from `listRedemptionCodeLookup`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Code |
| Redemption date/time | text | not in the schema: `Redemption date/time` |
| Product | text | Product |
| Original value | text | Original value |
| Discount | AED 1,234.50 | Discount |
| Final value | text | Final value |
| Channel | text | Channel |
| Venue | text | Venue |
| Device POS | 1,234 | Device/POS |
| Operator | text | Operator |
| Validation result | chip: Valid, Redeemed, Expired, Not started, Usage limit reached, Invalid product… | Validation result of the redemption attempt |

**The selected redemption code lookup** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Code |
| Redemption date/time | text | not in the schema: `Redemption date/time` |
| Product | text | Product |
| Original value | text | Original value |
| Discount | AED 1,234.50 | Discount |
| Final value | text | Final value |
| Channel | text | Channel |
| Venue | text | Venue |
| Device POS | 1,234 | Device/POS |
| Operator | text | Operator |
| Validation result | chip: Valid, Redeemed, Expired, Not started, Usage limit reached, Invalid product… | Validation result of the redemption attempt |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Promo code, Coupon ID, Batch ID, Transaction, Booking, Customer, Partner, Campaign. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lookup result**: The code's state and every redemption attempt including rejections with the reason (expired, already redeemed, voided, not yet valid, wrong venue, conditions not met, not assigned to this guest). *(source: contracts/satellite/promotions.yaml#listRedemptionCodeLookup / contracts/satellite/promotions.yaml#/components/schemas/CouponCode)*

**Data it reads**: `listRedemptionCodeLookup` (onLoad, Redemption Monitor & Code Lookup)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption code lookup list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption code lookup untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption code lookup yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption code lookup are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lookup:
  code: DUNE-7KQ2M9XA
  result: 'Rejected: already redeemed 14 Nov 11:02 at Till 07'
```

#### Permissions

- `listRedemptionCodeLookup` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-165` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-165`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 14: Works in Redemption Monitor & Code Lookup → Provide real-time operational visibility into coupon and promo-code redemption.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-165?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-166` Code Security, Fraud & Exception Center

**Detect promo-code abuse, leakage, abnormal redemption, and suspicious campaign behavior.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/code-security-fraud-exception-center-adm-166` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promo-code abuse: leaked shared codes, abnormal redemption velocity, many accounts from one device, suspicious campaigns.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCodeSecurityFraud return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every code security fraud** (data table, from `listCodeSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Signal type | chip: Excessive redemption velocity, Repeated failed attempts, Multiple customers using … | The fraud signal monitored. |

**The selected code security fraud** (detail panel): The pack groups this record's detail under its own headings: “Risk Levels”.

| Shows | Format | Notes |
|---|---|---|
| Signal type | chip: Excessive redemption velocity, Repeated failed attempts, Multiple customers using … | The fraud signal monitored. |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Suspend individual code, Suspend batch, Suspend campaign, Block redemption, Reinstate code, Assign investigation, Add case note. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **signals**: Signal, level, code, detected at, details; actions void code or pause campaign go to the promotion screens. *(source: contracts/satellite/promotions.yaml#listCodeSecurityFraud)*

**Data it reads**: `listCodeSecurityFraud` (onLoad, Code Security, Fraud & Exception Center)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The code security fraud list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the code security fraud untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No code security fraud yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the code security fraud are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  level: high
  type: Shared code posted publicly
  code: STAFF50
  detected: 08:14
```

#### Permissions

- `listCodeSecurityFraud` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-166` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-166`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 16: Works in Code Security, Fraud & Exception Center → Detect promo-code abuse, leakage, abnormal redemption, and suspicious campaign behavior.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-166?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-167` Redemption Analytics, Audit & AI Optimization

**Provide complete performance analytics and governance for coupon and promo-code campaigns. Board 4 shall provide TICVAI with an enterprise-grade Advanced Promotion Mechanics Engine for promotions involving relationships between products, quantities, basket composition, rewards, and qualifying purchases. While Board 2 defines standard discounts and thresholds and Board 3 manages promo codes/coupons, Board 4 answers: “When the customer buys X, what exactly should TICVAI give them, discount, replace, upgrade, or add to the transaction?” The matrix requires mechanics such as Buy X Get X, Buy X Get Y, Buy N Get X, percentage/amount discounts on another product, cheapest-item-free, fixed-price combinations, cross-category F&B/Retail rewards, added-value gifts, and automatic cart-level promotion application. Board 4 shall contain 10 backend screens.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Performance KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/redemption-analytics-audit-ai-optimization-adm-167` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Coupon campaign analytics and audit: generated, distributed, redeemed, rates, revenue, discount, incremental revenue, cost per redemption, expired unused, and the audit events.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listRedemption return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listRedemption carry no identifier. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search redemption analytics audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by campaign, code, batch, product, venue, channel and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Campaign | text field | — | — | `listRedemption` ?campaign |
| Code | text field | — | — | `listRedemption` ?code |
| Batch | text field | — | — | `listRedemption` ?batch |
| Product | text field | — | — | `listRedemption` ?product |
| Venue | text field | — | — | `listRedemption` ?venue |
| Channel | text field | — | — | `listRedemption` ?channel |
| Customer segment | text field | — | — | `listRedemption` ?customerSegment |
| Partner | text field | — | — | `listRedemption` ?partner |

#### Outputs: what the screen shows and produces

**Shown**

**Codes generated** (metric tile)

**Codes distributed** (metric tile)

**Codes redeemed** (metric tile)

**Redemption rate** (metric tile)

**Conversion rate** (metric tile)

**Revenue generated** (metric tile)

**Discount granted** (metric tile)

**Incremental revenue** (metric tile)

**AOV uplift** (metric tile)

**Cost per redemption** (metric tile)

**Margin impact** (metric tile)

**Expired unused codes** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **funnel and audit**: Funnel from generated to redeemed; audit trail below. *(source: contracts/satellite/promotions.yaml#listRedemption)*

**Data it reads**: `listRedemption` (onLoad, Redemption Analytics, Audit & AI Optimization)

**Where the user goes next**

- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption analytics audit list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  code: INSTA-DUNE
  generated: 5000
  distributed: 1200
  redeemed: 412
  costPerRedemption: AED 30.00
```

#### Permissions

- `listRedemption` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-167` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-167`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 3
- Flow F156 *Promotions Bundles Management board 3: Coupon & Promo Code Command Center*, step 18: Works in Redemption Analytics, Audit & AI Optimization → Provide complete performance analytics and governance for coupon and promo-code campaigns. Board 4 shall provide TICVAI with an enterprise-grade Advanced Promotion Mechanics Engine for promotions …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-167?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-158`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"generateCouponCodes": {"method":"POST","path":"/coupon-campaigns/{campaignId}/codes","contract":"promotions","summary":"Generate codes in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getCouponCodeBatch": {"method":"GET","path":"/coupon-campaigns/{campaignId}/code-batches/{batchId}","contract":"promotions","summary":"Progress and export of a code batch","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CouponCodeBatch"},
"listCodeEligibilityRestriction": {"method":"GET","path":"/code-eligibility-restriction","contract":"promotions","summary":"Code Eligibility & Restriction Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CodeEligibilityRestrictionManagerView"},
"listCodeSecurityFraud": {"method":"GET","path":"/code-security-fraud","contract":"promotions","summary":"Code Security, Fraud & Exception Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CodeSecurityFraudExceptionCenterView"},
"listCouponCampaigns": {"method":"GET","path":"/coupon-campaigns","contract":"promotions","summary":"List coupon campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCouponCodes": {"method":"GET","path":"/coupon-campaigns/{campaignId}/codes","contract":"promotions","summary":"List generated codes","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"batchId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRedemption": {"method":"GET","path":"/redemption","contract":"promotions","summary":"Redemption Analytics, Audit & AI Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"campaign","in":"query","required":false},{"name":"code","in":"query","required":false},{"name":"batch","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"partner","in":"query","required":false}],"requestBody":null,"responds":"RedemptionAnalyticsAuditAiOptimizationView"},
"listRedemptionCodeLookup": {"method":"GET","path":"/redemption-code-lookup","contract":"promotions","summary":"Redemption Monitor & Code Lookup","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"promoCode","in":"query","required":false},{"name":"couponId","in":"query","required":false},{"name":"batchId","in":"query","required":false},{"name":"transaction","in":"query","required":false},{"name":"booking","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"customerAccountReference","in":"query","required":false}],"requestBody":null,"responds":"RedemptionMonitorCodeLookupView"},
"listUniqueCodeGeneration": {"method":"GET","path":"/unique-code-generation","contract":"promotions","summary":"Unique Code Generation & Batch Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"UniqueCodeGenerationBatchManagerView"},
"listUsageCapacityFrequency": {"method":"GET","path":"/usage-capacity-frequency","contract":"promotions","summary":"Usage, Capacity & Frequency Control","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UsageCapacityFrequencyControlView"},
"listValidityDateTime": {"method":"GET","path":"/validity-date-time","contract":"promotions","summary":"Validity, Date & Time Control","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ValidityDateTimeControlView"},
"setCodeDistributionManager": {"method":"PUT","path":"/code-distribution-manager","contract":"promotions","summary":"Code Distribution & Assignment Manager","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CodeDistributionAssignmentManagerInput","responds":"CodeDistributionAssignmentManagerView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CodeDistributionAssignmentManagerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Code Distribution & Assignment Manager submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channelsType":{"type":"string","enum":["email","sms","whatsapp","mobileApp","crmJourney","guestPortal","b2bPortal","partnerPortal","pos","callCenter","api","exportedBatch"],"description":"Vocabulary listed under Distribution Channels."},"assigneeType":{"type":"string","enum":["individualCustomer","customerSegment","membershipAccount","b2bCompany","reseller","travelAgency","school","hotel","bank","corporatePartner","marketingCampaign"],"description":"Who the codes are assigned to."},"batchId":{"type":"string","description":"Batch ID"},"assigneeReference":{"type":"string","description":"Customer, segment, account or partner the codes go to"},"quantity":{"type":"integer","description":"Codes to assign"}}},
"CodeDistributionAssignmentManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Code Distribution & Assignment Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelsType":{"type":"string","enum":["email","sms","whatsapp","mobileApp","crmJourney","guestPortal","b2bPortal","partnerPortal","pos","callCenter","api","exportedBatch"],"description":"Vocabulary listed under Distribution Channels."},"generated":{"type":"string","description":"Generated"},"assigned":{"type":"string","description":"Assigned"},"sent":{"type":"string","description":"Sent"},"delivered":{"type":"string","description":"Delivered"},"redeemed":{"type":"string","description":"Redeemed"},"expired":{"type":"integer","description":"Expired"},"cancelled":{"type":"integer","description":"Cancelled"},"viewed":{"type":"string","description":"Viewed where available"},"assigneeType":{"type":"string","enum":["individualCustomer","customerSegment","membershipAccount","b2bCompany","reseller","travelAgency","school","hotel","bank","corporatePartner","marketingCampaign"],"description":"Who the codes are assigned to."},"batchId":{"type":"string","description":"Batch ID"},"partner":{"type":"string","description":"Partner, for a partner batch"}}},
"CodeEligibilityRestrictionManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Code Eligibility & Restriction Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"location":{"type":"string","description":"Location"},"operatingArea":{"type":"string","description":"Operating area"},"productScopes":{"type":"array","items":{"type":"string","enum":["ticket","ticketType","product","productCategory","attraction","event","bundle","membership","fB","retail","addOn"]},"description":"Products the code is restricted to."},"customerScopes":{"type":"array","items":{"type":"string","enum":["guestType","crmSegment","loyaltyTier","b2bAccount","corporateGroup","b2b"]},"description":"Customers the code is restricted to."},"channels":{"type":"array","items":{"type":"string","enum":["b2c","pos","mobilePos","kiosk","mobileApp","callCenter","reseller","api"]},"description":"Channels the code is valid on."}}},
"CodeSecurityFraudExceptionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Code Security, Fraud & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"levelsType":{"type":"string","enum":["low","medium","high","critical"],"description":"Vocabulary listed under Risk Levels."},"signalType":{"type":"string","enum":["excessiveRedemptionVelocity","repeatedFailedAttempts","multipleCustomersUsingCustomerSpecificCode","unusualGeographicUsage","highVolumeRedemptionFromOneDevice","suspiciousPosOperatorActivity","codeEnumerationAttempts","partnerCodeLeakage","redemptionAboveExpectedCampaignPattern"],"description":"The fraud signal monitored."},"codeId":{"type":"string","description":"Code or batch ID"},"detectedAt":{"type":"string","format":"date-time","description":"When detected"},"details":{"type":"string","description":"What was observed"}}},
"CouponCampaign": {"x-ticvai-persistence":"promotions.coupon_campaign","allOf":[{"$ref":"#/components/schemas/CreateCouponCampaignRequest"},{"type":"object","required":["id","generatedCount","redeemedCount"],"properties":{"id":{"type":"string","format":"uuid"},"generatedCount":{"type":"integer"},"redeemedCount":{"type":"integer"},"isActive":{"type":"boolean"}}}]},
"CouponCode": {"x-ticvai-persistence":"promotions.coupon_code","type":"object","required":["code","campaignId","status"],"properties":{"code":{"type":"string"},"campaignId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"description":"The `generateCouponCodes` batch that issued this code. Null where no batch did."},"status":{"$ref":"#/components/schemas/CouponStatus"},"assignedSubjectId":{"type":"string","format":"uuid","nullable":true},"redemptionCount":{"type":"integer"},"maxRedemptions":{"type":"integer"},"discount":{"$ref":"#/components/schemas/Discount"},"invalidReason":{"type":"string","nullable":true,"description":"Why the code cannot be applied. A cashier reading `expired` to a guest is a very different conversation from reading `already used`.\n","enum":["expired","alreadyRedeemed","voided","notYetValid","wrongVenue","conditionsNotMet","notAssignedToGuest"]},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"redeemedOrderId":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CouponCodeBatch": {"x-ticvai-persistence":"promotions.coupon_code_batch","type":"object","description":"One run of `generateCouponCodes`. **The batch is a row** because its status is read after the request that queued it has returned, and its codes point back at it.\n","required":["id","campaignId","quantity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"The `batchId` that `generateCouponCodes` returned."},"campaignId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","description":"Codes requested."},"generatedCount":{"type":"integer","description":"Codes generated so far."},"prefix":{"type":"string","maxLength":16,"nullable":true},"length":{"type":"integer"},"status":{"type":"string","enum":["queued","generating","complete","failed"]},"failureReason":{"type":"string","nullable":true,"description":"Present only where status is `failed`."},"requestedByPrincipalId":{"type":"string","format":"uuid"},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"downloadUrl":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"The exported file of the batch's codes. Signed and expiring, issued on each read, so it is not stored. Present only while status is `complete`."}}},
"CouponStatus": {"type":"string","enum":["issued","assigned","redeemed","expired","voided"]},
"CreateCouponCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"isSingleUse":{"type":"boolean","default":true,"description":"True generates individually redeemable codes. False issues one shared code with a redemption limit.\n"},"maxRedemptionsPerCode":{"type":"integer","default":1},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) the codes are issued under, as the Coupon & Promo Code Builder names it. (DM5, 29 September: data model for the agreed operations)"}}},
"Discount": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","required":["kind"],"properties":{"kind":{"$ref":"#/components/schemas/DiscountKind"},"percentage":{"type":"number","minimum":0,"maximum":100},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fixedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"buyQuantity":{"type":"integer","minimum":1},"getQuantity":{"type":"integer","minimum":1},"getDiscountPercentage":{"type":"number","minimum":0,"maximum":100,"description":"100 makes the free items actually free; lower values give a partial discount."},"tiers":{"type":"array","description":"For `tieredPercentage` — more units, larger discount.","items":{"type":"object","required":["minQuantity","percentage"],"properties":{"minQuantity":{"type":"integer","minimum":1},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"maxDiscountAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Cap on a percentage discount. Prevents an unbounded discount on a large basket."},"rewardVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (createPromotion; the builders setGiftFreeProduct and setBuyGetBogo were retired in r2, CHG-CLN-001). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"},"maxApplicationsPerBasket":{"type":"integer","minimum":1,"nullable":true,"description":"How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (createPromotion; setFixedPriceOffer was retired in r2, CHG-CLN-001). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RedemptionAnalyticsAuditAiOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Redemption Analytics, Audit & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"codesGenerated":{"type":"string","description":"Codes generated"},"codesDistributed":{"type":"string","description":"Codes distributed"},"codesRedeemed":{"type":"string","description":"Codes redeemed"},"redemptionRate":{"type":"number","description":"Redemption rate"},"conversionRate":{"type":"number","description":"Conversion rate"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue generated"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount granted"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"aovUplift":{"type":"number","description":"AOV uplift"},"costPerRedemption":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost per redemption"},"marginImpact":{"type":"number","description":"Margin impact"},"expiredUnusedCodes":{"type":"integer","description":"Expired unused codes"},"user":{"type":"string","description":"User"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"previousValue":{"type":"string","description":"Previous value"},"newValue":{"type":"integer","description":"New value"},"reason":{"type":"string","description":"Reason"},"approvalReference":{"type":"string","description":"Approval reference"},"auditEvent":{"type":"string","enum":["created","modified","assigned","suspended","reactivated","cancelled"],"description":"Code audit event."}}},
"RedemptionMonitorCodeLookupView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Redemption Monitor & Code Lookup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promoCode":{"type":"string","description":"Promo code"},"code":{"type":"string","description":"Code"},"redemptionDate":{"type":"string","format":"date-time","description":"Redemption date"},"redemptionTime":{"type":"string","format":"date-time","description":"Redemption time"},"product":{"type":"string","description":"Product"},"originalValue":{"type":"string","description":"Original value"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"finalValue":{"type":"string","description":"Final value"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"devicePos":{"type":"integer","description":"Device/POS"},"operator":{"type":"string","description":"Operator"},"validationResult":{"type":"string","enum":["valid","redeemed","expired","notStarted","usageLimitReached","invalidProduct","invalidChannel","invalidLocation","invalidCustomer","suspended","cancelled"],"description":"Validation result of the redemption attempt"}}},
"UniqueCodeGenerationBatchManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Unique Code Generation & Batch Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"campaign":{"type":"string","description":"Campaign"},"numberOfCodes":{"type":"integer","description":"Number of codes"},"codeLength":{"type":"string","description":"Code length"},"prefix":{"type":"string","description":"Prefix"},"suffix":{"type":"string","description":"Suffix"},"characterType":{"type":"string","description":"Character type"},"caseSensitivity":{"type":"string","description":"Case sensitivity"},"expiration":{"type":"string","description":"Expiration"},"numberOfUses":{"type":"integer","description":"Number of uses"},"distributionOwner":{"type":"string","description":"Distribution owner"},"batchId":{"type":"string","description":"Batch ID"},"quantityGenerated":{"type":"integer","description":"Quantity generated"},"generatedBy":{"type":"string","description":"Generated by"},"generationDate":{"type":"string","format":"date-time","description":"Generation date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"assignedPartner":{"type":"string","description":"Assigned partner"},"distributionStatus":{"type":"string","description":"Distribution status"},"redeemedQuantity":{"type":"integer","description":"Redeemed quantity"},"remainingQuantity":{"type":"integer","description":"Remaining quantity"}}},
"UsageCapacityFrequencyControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Usage, Capacity & Frequency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumTotalRedemptions":{"type":"string","description":"Maximum total redemptions"},"maximumPerCustomer":{"type":"string","description":"Maximum per customer"},"maximumPerAccount":{"type":"string","description":"Maximum per account"},"maximumPerTransaction":{"type":"string","description":"Maximum per transaction"},"maximumPerDay":{"type":"string","description":"Maximum per day"},"maximumPerChannel":{"type":"string","description":"Maximum per channel"},"maximumPerVenue":{"type":"string","description":"Maximum per venue"},"usageType":{"type":"string","enum":["singleUse","multipleUse","unlimitedUse"],"description":"How often one code may be used."},"issued":{"type":"integer","description":"Codes issued"},"redeemed":{"type":"integer","description":"Codes redeemed"},"reservedPending":{"type":"integer","description":"Codes reserved or pending"},"remaining":{"type":"integer","description":"Codes remaining"}}},
"ValidityDateTimeControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Validity, Date & Time Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"blackoutDates":{"type":"string","description":"Blackout dates"},"holidays":{"type":"string","description":"Holidays"},"selectedTimeslots":{"type":"string","description":"Selected timeslots"},"selectedEvents":{"type":"string","description":"Selected events"},"seasonalCalendars":{"type":"string","description":"Seasonal calendars"},"expirationGracePeriod":{"type":"string","format":"date-time","description":"Expiration grace period"}}}
}
```
