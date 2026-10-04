# WS48 — Promotions   Bundles Management board 4

**10 screens · 8 operations · 9 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-168` | Advanced Offer Command Center | B | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-169` | Buy X Get Y / BOGO Rule Builder | B–D | 15 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-170` | Multi-Buy & Quantity Offer Configurator | B | 3 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-171` | Cheapest / Lowest-Value Item Promotion | B | 7 | 0 | 5 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-172` | Fixed-Price & “N for X” Offer Builder | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-173` | Gift, Free Product & Added-Value Offer Builder | B–D | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-174` | Cross-Category Promotion Builder | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-175` | Reward Selection, Substitution & Customer Choice | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-176` | Advanced Offer Guardrails & Conflict Controls | B | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-177` | Offer Simulation, Basket Trace & AI Optimization | B | 15 | 0 | 6 | 18 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-170, ADM-174, ADM-175 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-168` Advanced Offer Command Center

**Provide the centralized management workspace for all advanced promotional mechanics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-168 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/advanced-offer-command-center-adm-168` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The hub of advanced offers (BOGO, gift with purchase, fixed price, cross-category): counts by state and type, redemptions, free items issued, discount, revenue and margin impact.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listAdvancedOffer, listAdvancedOfferGuardrail return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listAdvancedOffer, listAdvancedOfferGuardrail carry no identifier. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search advanced offer | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by buy x get x, buy x get y, buy n get x, buy n get multiple, cheapest item free, percentage off another product and 6 more — which are present is a decision the pack … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Buy x get x | text field | — | — | `listAdvancedOffer` ?buyXGetX |
| Buy x get y | text field | — | — | `listAdvancedOffer` ?buyXGetY |
| Buy n get x | text field | — | — | `listAdvancedOffer` ?buyNGetX |
| Buy n get multiple | text field | — | — | `listAdvancedOffer` ?buyNGetMultiple |
| Cheapest item free | text field | — | — | `listAdvancedOffer` ?cheapestItemFree |
| Percentage off another product | number field (%) | — | — | `listAdvancedOffer` ?percentageOffAnotherProduct |
| Amount off another product | text field | — | — | `listAdvancedOffer` ?amountOffAnotherProduct |
| Fixed bundle price | text field | — | — | `listAdvancedOffer` ?fixedBundlePrice |
| Gift with purchase | text field | — | — | `listAdvancedOffer` ?giftWithPurchase |
| Added value | text field | — | — | `listAdvancedOffer` ?addedValue |
| Cross category reward | text field | — | — | `listAdvancedOffer` ?crossCategoryReward |
| Upgrade offer | text field | — | — | `listAdvancedOffer` ?upgradeOffer |

#### Outputs: what the screen shows and produces

**Shown**

**Active Advanced Offers** (metric tile)

**Scheduled Offers** (metric tile)

**BOGO Campaigns** (metric tile)

**Gift-with-Purchase Offers** (metric tile)

**Fixed-Price Offers** (metric tile)

**Cross-Category Offers** (metric tile)

**Total Redemptions** (metric tile)

**Free Items Issued** (metric tile)

**Discount Granted** (metric tile)

**Revenue Generated** (metric tile)

**AOV Uplift** (metric tile)

**Margin Impact** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPI and state counts**: Counts by state as filter chips (draft to archived). *(source: contracts/satellite/promotions.yaml#listAdvancedOffer)*

**Data it reads**: `listAdvancedOffer` (onLoad, Advanced Offer Command Center); `listAdvancedOfferGuardrail` (onLoad, Advanced Offer Guardrails & Conflict Controls)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-170` Multi-Buy & Quantity Offer Configurator: *Works in Multi-Buy & Quantity Offer Configurator*; calls `listAdvancedOffer`
- → `ADM-171` Cheapest / Lowest-Value Item Promotion: *Works in Cheapest / Lowest-Value Item Promotion*; calls `listAdvancedOffer`
- → `ADM-175` Reward Selection, Substitution & Customer Choice: *Works in Reward Selection, Substitution & Customer Choice*; calls `listAdvancedOffer`
- → `ADM-176` Advanced Offer Guardrails & Conflict Controls: *Works in Advanced Offer Guardrails & Conflict Controls*; calls `listAdvancedOffer`
- → `ADM-177` Offer Simulation, Basket Trace & AI Optimization: *Works in Offer Simulation, Basket Trace & AI Optimization*; calls `listAdvancedOffer`
- → `ADM-169` Buy X Get Y / BOGO Rule Builder: *Works in Buy X Get Y / BOGO Rule Builder, a section of BO-010, which saves the record with createPromotion…*; calls `listAdvancedOffer`
- → `ADM-172` Fixed-Price & “N for X” Offer Builder: *Works in Fixed-Price & “N for X” Offer Builder, a section of BO-010, which saves the record with…*; calls `listAdvancedOffer`
- → `ADM-173` Gift, Free Product & Added-Value Offer Builder: *Works in Gift, Free Product & Added-Value Offer Builder, a section of BO-010, which saves the record with…*; calls `listAdvancedOffer`
- → `ADM-174` Cross-Category Promotion Builder: *Works in Cross-Category Promotion Builder, a section of BO-010, which saves the record with createPromotion…*; calls `listAdvancedOffer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced offer list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced offer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the advanced offer are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  active: 9
  bogo: 3
  freeItemsIssued: 2140
  marginImpact: -2.1 pts
```

#### Permissions

- `listAdvancedOffer` → `PRICE_VIEW` (read) · staff
- `listAdvancedOfferGuardrail` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-168` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-168`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 1: Opens Advanced Offer Command Center → Provide the centralized management workspace for all advanced promotional mechanics.
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F157 branch at step 1 (expected): when Nothing has been set up on Advanced Offer Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F157 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-168?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-170`, `ADM-171`, `ADM-175`, `ADM-176`, `ADM-177`, `ADM-169`, `ADM-172`, `ADM-173`, `ADM-174`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-169` Buy X Get Y / BOGO Rule Builder

**Configure the fundamental qualifier → reward relationship. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/buy-x-get-y-bogo-rule-builder-adm-169` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setBuyGetBogo` duplicated BO-010 Promotions & Coupons's createPromotion, so it is removed from the contract (BC-013) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The qualifier-to-reward relationship of Buy X Get Y offers: what qualifies (product, category, ticket type, quantity, minimum spend, segment, channel, venue, time) and what is rewarded (same or different product; free, percentage, fixed off or fixed price). The discounted item is added to the basket automatically.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product | select field | — | — | — | — | — | — |
| Product category | select field | — | — | — | — | — | — |
| Ticket type | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Minimum spend | select field | — | — | — | — | — | — |
| Customer segment | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Same product | select field | — | — | — | — | — | — |
| Different product | select field | — | — | — | — | — | — |
| Free | select field | — | — | — | — | — | — |
| Percentage discount | select field | — | — | — | — | — | — |
| Fixed discount | select field | — | — | — | — | — | — |
| Fixed reward price | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **qualifier and reward**: A sentence builder ("Buy 2 Day Pass Adult, get 1 Day Pass Child at 100% off") rather than separate fields; same vs different product as a switch. *(source: contracts/satellite/promotions.yaml#/components/schemas/BuyXGetYBogoRuleBuilderInput / DI-174 / DI-600)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The buy get bogo configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the buy get bogo untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved yet. The create action is BO-010's (createPromotion); this section offers none of its own. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  buy: 2 x Day Pass Adult
  get: 1 x Day Pass Child
  reward: 100% off
  channels:
  - Website
  - Point of sale
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-169` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-169`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 2: Works in Buy X Get Y / BOGO Rule Builder, a section of BO-010, which saves the record with createPromotion … → Configure the fundamental qualifier → reward relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-169?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`, `BO-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-170` Multi-Buy & Quantity Offer Configurator

**Configure advanced quantity relationships that go beyond simple BOGO.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-170 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/multi-buy-quantity-offer-configurator-adm-170` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Multi-Buy & Quantity Offer Configurator declares no operation that writes anything** — its only declared call is `listMultiBuyQuantity`, a read. The name promises authoring and the contract offers … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listMultiBuyQuantity lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion; see the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Quantity offers beyond BOGO: minimum, exact or range quantities, multiples of X, one or several free, percentage or amount off, fixed total, repeat automatically up to N times.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listMultiBuyQuantity return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listMultiBuyQuantity carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Multi-Buy & Quantity Offer Configurator) declares only reads (listMultiBuyQuantity). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Apply once | select field | — | — | — | — | — | — |
| Repeat automatically | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **offer sentence**: Each offer rendered as a sentence ("Every 3 attractions: the 3rd free, up to 2 times"). *(source: contracts/satellite/promotions.yaml#listMultiBuyQuantity)*

**Data it reads**: `listMultiBuyQuantity` (onLoad, Multi-Buy & Quantity Offer Configurator)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listMultiBuyQuantity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-buy quantity offer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-buy quantity offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-buy quantity offer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer: Buy 4 Day Passes, pay for 3; repeats up to 2 times
```

#### Permissions

- `listMultiBuyQuantity` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-170` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-170`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 4: Works in Multi-Buy & Quantity Offer Configurator → Configure advanced quantity relationships that go beyond simple BOGO.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-170?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-171` Cheapest / Lowest-Value Item Promotion

**Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying items within the same transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-171 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cheapest-lowest-value-item-promotion-adm-171` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Offers where the cheapest qualifying item is free or discounted ("buy 3, cheapest free"), with the maximum free value and repetitions.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCheapestLowestValue return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCheapestLowestValue carry no identifier. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Eligible products | select field | — | — | — | — | — | — |
| Eligible categories | select field | — | — | — | — | — | — |
| Minimum quantity | select field | — | — | — | — | — | — |
| Number of free items | text field | — | — | — | — | — | — |
| Cheapest/lowest-priced selection | select field | — | — | — | — | — | — |
| Maximum free-item value | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cheapest item free (primary button) | navigation or local | — | — | — | — |
| Cheapest item 50% off (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **worked basket**: Show which line the rule would pick in a sample basket. *(source: contracts/satellite/promotions.yaml#listCheapestLowestValue / DI-357)*

**Data it reads**: `listCheapestLowestValue` (onLoad, Cheapest / Lowest-Value Item Promotion)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listCheapestLowestValue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cheapest lowest-value item configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cheapest lowest-value item untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cheapest lowest-value item configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  rule: Buy 3 attractions, cheapest free
  maxFreeValue: AED 120.00
```

#### Permissions

- `listCheapestLowestValue` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-171` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-171`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 6: Works in Cheapest / Lowest-Value Item Promotion → Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-171?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cheapest item free, Cheapest item 50% off.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-172` Fixed-Price & “N for X” Offer Builder

**Configure promotions where a qualifying collection of products is sold for a fixed promotional total. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/fixed-price-n-for-x-offer-builder-adm-172` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setFixedPriceOffer` duplicated BO-010 Promotions & Coupons's createPromotion, so it is removed from the contract (BC-014) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Offers where a qualifying set sells for a fixed total ("any 3 attractions for AED 300"), with mix-and-match, maximum repetitions and minimum or maximum product values.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Required quantity | select field | — | — | — | — | — | — |
| Required products | select field | — | — | — | — | — | — |
| Product category | select field | — | — | — | — | — | — |
| Mix-and-match allowed | select field | — | — | — | — | — | — |
| Fixed promotional price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |
| Minimum/maximum product values | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **fixedPromotionalPrice**: In the region's currency (PR-2) with the saving shown against the cheapest and dearest qualifying combination. *(source: contracts/satellite/promotions.yaml#/components/schemas/FixedPriceNForXOfferBuilderInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fixed-price for offer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fixed-price for offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved yet. The create action is BO-010's (createPromotion); this section offers none of its own. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  name: Any 3 attractions
  requiredQuantity: 3
  mixAndMatch: true
  price: AED 300.00
  maximumRepetitions: 2
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-172` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-172`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 8: Works in Fixed-Price & “N for X” Offer Builder, a section of BO-010, which saves the record with createPromotion … → Configure promotions where a qualifying collection of products is sold for a fixed promotional total.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-172?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`, `BO-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-173` Gift, Free Product & Added-Value Offer Builder

**Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free pencil.” (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/gift-free-product-added-value-offer-builder-adm-173` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setGiftFreeProduct` duplicated BO-010 Promotions & Coupons's createPromotion, so it is removed from the contract (BC-015) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Offers where a purchase earns something extra rather than a lower price ("spend more than AED 200 and get a free pencil"): the trigger, the reward type, where it is fulfilled, what happens when the reward is out of stock (substitute, do not offer, alternative reward, fulfil later).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Do not offer promotion | text field | — | — | — | — | — | — |
| Provide alternative reward | select field | — | — | — | — | — | — |
| Issue voucher | select field | — | — | — | — | — | — |
| Allow later fulfillment | select field | — | — | — | — | — | — |
| Escalate to operator | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **out-of-stock behaviour**: One choice among substitute, do not offer the promotion, provide an alternative reward, allow later fulfilment, with the alternative picked when chosen. *(source: contracts/satellite/promotions.yaml#/components/schemas/GiftFreeProductAddedValueOfferBuilderInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift free product configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift free product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved yet. The create action is BO-010's (createPromotion); this section offers none of its own. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  trigger: basket over AED 200.00
  reward: freeRetailProduct
  item: Dune Park pencil set
  fulfilment: Main Gate shop
  outOfStock: 'alternative: keyring'
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-173` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-173`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 10: Works in Gift, Free Product & Added-Value Offer Builder, a section of BO-010, which saves the record with … → Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-173?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`, `BO-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-174` Cross-Category Promotion Builder

**Create promotions spanning different TICVAI commercial domains. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/cross-category-promotion-builder-adm-174` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setCrossCategoryPromotion` duplicated BO-010 Promotions & Coupons's createPromotion, so it is removed from the contract (BC-016) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promotions spanning commercial domains (ticketing, attractions, events, F&B, retail, membership, experiences, add-ons, parking, services): buy in one, benefit in another.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **domains**: Draw as two columns, "Buy from" and "Get in", each a domain picker followed by a product picker of that domain. *(source: contracts/satellite/promotions.yaml#/components/schemas/CrossCategoryPromotionBuilderInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-category promotion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-category promotion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved yet. The create action is BO-010's (createPromotion); this section offers none of its own. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-category promotion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  buyFrom: 'Ticketing: Day Pass Adult'
  getIn: 'F&B: Harbour Kitchen meal 20% off'
  validity: same day
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-174` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-174`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 12: Works in Cross-Category Promotion Builder, a section of BO-010, which saves the record with createPromotion … → Create promotions spanning different TICVAI commercial domains.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-174?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-168`, `BO-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-175` Reward Selection, Substitution & Customer Choice

**Control situations where the customer can choose between multiple promotional rewards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-175 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/reward-selection-substitution-customer-choice-adm-175` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When a guest may choose between rewards, and what substitutes apply when a reward is unavailable, with a maximum substitute value.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listRewardSelectionSubstitution return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **reward options**: Options as cards with the selection model (guest chooses, system picks) and substitutes. *(source: contracts/satellite/promotions.yaml#listRewardSelectionSubstitution)*

**Data it reads**: `listRewardSelectionSubstitution` (onLoad, Reward Selection, Substitution & Customer Choice)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listRewardSelectionSubstitution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reward selection substitution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reward selection substitution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reward selection substitution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reward selection substitution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  rewards:
  - Free cap
  - Free water bottle
  selection: guest chooses
  substitute: keyring, up to AED 25.00
```

#### Permissions

- `listRewardSelectionSubstitution` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-175` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-175`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 14: Works in Reward Selection, Substitution & Customer Choice → Control situations where the customer can choose between multiple promotional rewards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-175?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-176` Advanced Offer Guardrails & Conflict Controls

**Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-176 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define preliminary behavior; Prevent configurations such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/advanced-offer-guardrails-conflict-controls-adm-176` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listAdvancedOfferGuardrail lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Safeguards on advanced offers: maximum free items and reward value, maximum discount, applications per basket and customer, daily and campaign redemptions, minimum transaction value and margin, inventory requirement, combination behaviour. Cross-promotion stacking stays on the stacking board.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listAdvancedOfferGuardrail return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listAdvancedOfferGuardrail carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Advanced Offer Guardrails & Conflict Controls) declares only reads (listAdvancedOfferGuardrail). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Can combine | select field | — | — | — | — | — | — |
| Cannot combine | select field | — | — | — | — | — | — |
| Exclusive | select field | — | — | — | — | — | — |
| Defer to central stacking engine | text field | — | — | — | — | — | — |
| Product A gives Product B free | text field | — | — | — | — | — | — |
| Product B gives Product A free | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **safeguards**: Each limit with its value per offer. *(source: contracts/satellite/promotions.yaml#listAdvancedOfferGuardrail)*

**Data it reads**: `listAdvancedOfferGuardrail` (onLoad, Advanced Offer Guardrails & Conflict Controls)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listAdvancedOfferGuardrail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced offer guardrails configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced offer guardrails untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced offer guardrails configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-156`: Same guardrail layout as discount guardrails.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guardrails:
  maximumFreeItems: 2
  maximumRewardValue: AED 150.00
  minimumMargin: 35%
```

#### Permissions

- `listAdvancedOfferGuardrail` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-176` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-176`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 16: Works in Advanced Offer Guardrails & Conflict Controls → Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-176?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-177` Offer Simulation, Basket Trace & AI Optimization

**Test complex promotion mechanics before publication.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-ADM-177 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `promotionId` (navigation) |
| Route | `/commercial/offer-simulation-basket-trace-ai-optimization-adm-177` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Single transaction, Historical transaction replay, Sample customer segment, Forecast simulation, Bulk … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test complex offers before publication on a sample basket and see the trace: lines, qualifiers matched, rewards, guardrails passed, original total, promotion amount, final total.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Single transaction, Historical transaction replay, Sample customer segment, Forecast simulation, Bulk scenario testing. (CHG-MOV-008)
- List operation(s) listOfferBasketTrace return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listOfferBasketTrace carry no identifier. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): The simulation is a GET list with no input; a basket to test cannot be sent. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Mode | radio group | — | Single transaction · Historical transaction replay · Sample customer segment · Forecast simulation · Bulk scenario testing | `listOfferBasketTrace` ?mode |

**Form: Test a basket** (modal, opened by *Test a basket*; *Test a basket* calls `evaluatePromotions`, *Cancel* sends nothing)

**Collects what `evaluatePromotions` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary. | `evaluatePromotions` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Membership tier `membershipTierId` | picker: choose a membership tier | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Coupon codes `couponCodes` | list of values (chips) | optional | — | — | — | — | `evaluatePromotions` body |
| Evaluate at `evaluateAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For back-office testing of a rule before publishing. | `evaluatePromotions` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one … | `evaluatePromotions` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `evaluatePromotions` body |
| Line `lines[].lineId` | text field | required | — | — | — | — | `evaluatePromotions` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `evaluatePromotions` body |
| Unit price `lines[].unitPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluatePromotions` body |

Errors to draw in the form: 400 Validation failed

**Form: Replay history** (modal, opened by *Replay history*; *Replay history* calls `simulatePromotion`, *Cancel* sends nothing)

**Collects what `simulatePromotion` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period from `periodFrom` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |
| Period to `periodTo` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single transaction (primary button) | navigation or local | — | — | — | — |
| Historical transaction replay (secondary button) | navigation or local | — | — | — | — |
| Sample customer segment (secondary button) | navigation or local | — | — | — | — |
| Forecast simulation (secondary button) | navigation or local | — | — | — | — |
| Bulk scenario testing (secondary button) | navigation or local | — | — | — | — |
| Test a basket (secondary button) | `evaluatePromotions` POST `/promotions/evaluate` | EvaluatePromotionsRequest | PromotionEvaluation | 400 Validation failed | opens modal first |
| Replay history (secondary button) | `simulatePromotion` POST `/promotions/{promotionId}/simulate` | inline | inline | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **basket trace**: Each basket line with the qualifier and reward it took part in, as a trace. *(source: contracts/satellite/promotions.yaml#listOfferBasketTrace)*

**Data it reads**: `listOfferBasketTrace` (onLoad, Offer Simulation, Basket Trace & AI Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offer simulation basket list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offer simulation basket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offer simulation basket yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offer simulation basket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trace:
  lines:
  - 3 x Day Pass Adult AED 885.00
  reward: 1 free (AED 295.00)
  final: AED 590.00
```

#### Permissions

- `listOfferBasketTrace` → `PRICE_VIEW` (read) · staff
- `evaluatePromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `simulatePromotion` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.11 | - Discounts | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.12 | - Dynamic promotions | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.13 | - Coupons | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.8.5 | The system should allow call center agents to apply promotions, discounts, up-sales and offers configured in the system. Application of discount coupons via a code supplied (on the phone) by the … | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 3.5.9 | System shall automatically present bundle offers based on configurable conditions such as number of tickets purchased, guest type, loyalty tier, membership status, sales channel, season, location, or … | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.16 | The system should allow creation of promotion on a bundle: “buy x, get x free”, or “buy a ticket and a catalogue and get 10% off or get AED 10 discount” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.17 | The system should allow creation of added value: “Buy for more than 200 AED and get a free pencil” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.32 | Discounts can be under conditions (dynamic discounts): - early birds, - subject to volume (buy one get one, 4 for 3 …), - subject to the type of tickets or - subject to the customer segment. | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.34 | Cart-level promotions & bundle logic (e.g., “Buy 4 Pay 3”, multi-park family packs) applied automatically at checkout, without new SKUs | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 4.1.7 | The system should be able to accept promotions linked with admission tickets and/or vouchers. | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.9 | The system should be able to apply BOGO based promotion offers based on purchased product types and/or product count | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.10 | The system should be able to allow: - Buy X product and get X product for free. - Buy X product and get Y product for free. - Buy N number of products and Get X product for free. - Buy N number of … | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-177` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-177`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 18: Works in Offer Simulation, Basket Trace & AI Optimization → Test complex promotion mechanics before publication.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-177?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single transaction, Historical transaction replay, Sample customer segment, Forecast simulation, Bulk scenario testing, Test a basket, Replay history.
- [ ] No transition is declared; back returns where the user came from.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"evaluatePromotions": {"method":"POST","path":"/promotions/evaluate","contract":"promotions","summary":"Evaluate promotions against a cart","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EvaluatePromotionsRequest","responds":"PromotionEvaluation"},
"listAdvancedOffer": {"method":"GET","path":"/advanced-offer","contract":"promotions","summary":"Advanced Offer Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"buyXGetX","in":"query","required":false},{"name":"buyXGetY","in":"query","required":false},{"name":"buyNGetX","in":"query","required":false},{"name":"buyNGetMultiple","in":"query","required":false},{"name":"cheapestItemFree","in":"query","required":false},{"name":"percentageOffAnotherProduct","in":"query","required":false},{"name":"amountOffAnotherProduct","in":"query","required":false},{"name":"fixedBundlePrice","in":"query","required":false},{"name":"giftWithPurchase","in":"query","required":false},{"name":"addedValue","in":"query","required":false},{"name":"crossCategoryReward","in":"query","required":false},{"name":"upgradeOffer","in":"query","required":false}],"requestBody":null,"responds":"AdvancedOfferCommandCenterView"},
"listAdvancedOfferGuardrail": {"method":"GET","path":"/advanced-offer-guardrail","contract":"promotions","summary":"Advanced Offer Guardrails & Conflict Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AdvancedOfferGuardrailsConflictControlsView"},
"listCheapestLowestValue": {"method":"GET","path":"/cheapest-lowest-value","contract":"promotions","summary":"Cheapest / Lowest-Value Item Promotion","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CheapestLowestValueItemPromotionView"},
"listMultiBuyQuantity": {"method":"GET","path":"/multi-buy-quantity","contract":"promotions","summary":"Multi-Buy & Quantity Offer Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MultiBuyQuantityOfferConfiguratorView"},
"listOfferBasketTrace": {"method":"GET","path":"/offer-basket-trace","contract":"promotions","summary":"Offer Simulation, Basket Trace & AI Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mode","in":"query","required":false}],"requestBody":null,"responds":"OfferSimulationBasketTraceAiOptimizationView"},
"listRewardSelectionSubstitution": {"method":"GET","path":"/reward-selection-substitution","contract":"promotions","summary":"Reward Selection, Substitution & Customer Choice","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RewardSelectionSubstitutionCustomerChoiceView"},
"simulatePromotion": {"method":"POST","path":"/promotions/{promotionId}/simulate","contract":"promotions","summary":"What this promotion would have cost on real history","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AdvancedOfferCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Advanced Offer Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeAdvancedOffers":{"type":"integer","description":"Active Advanced Offers"},"scheduledOffers":{"type":"integer","description":"Scheduled Offers"},"bogoCampaigns":{"type":"integer","description":"BOGO Campaigns"},"giftWithPurchaseOffers":{"type":"integer","description":"Gift-with-Purchase Offers"},"fixedPriceOffers":{"type":"integer","description":"Fixed-Price Offers"},"crossCategoryOffers":{"type":"integer","description":"Cross-Category Offers"},"totalRedemptions":{"type":"integer","description":"Total Redemptions"},"freeItemsIssued":{"type":"string","description":"Free Items Issued"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Granted"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Generated"},"aovUplift":{"type":"number","description":"AOV Uplift"},"marginImpact":{"type":"number","description":"Margin Impact"},"draft":{"type":"string","description":"Draft"},"pendingValidation":{"type":"integer","description":"Pending Validation"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduled":{"type":"string","format":"date-time","description":"Scheduled"},"active":{"type":"integer","description":"Active"},"paused":{"type":"string","description":"Paused"},"suspended":{"type":"string","description":"Suspended"},"expired":{"type":"integer","description":"Expired"},"archived":{"type":"string","description":"Archived"}}},
"AdvancedOfferGuardrailsConflictControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Advanced Offer Guardrails & Conflict Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumFreeItems":{"type":"string","description":"Maximum free items"},"maximumRewardValue":{"type":"string","description":"Maximum reward value"},"maximumDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount"},"maximumApplicationsPerBasket":{"type":"string","description":"Maximum applications per basket"},"maximumApplicationsPerCustomer":{"type":"string","description":"Maximum applications per customer"},"maximumDailyRedemptions":{"type":"string","description":"Maximum daily redemptions"},"maximumCampaignRedemptions":{"type":"string","description":"Maximum campaign redemptions"},"minimumTransactionValue":{"type":"string","description":"Minimum transaction value"},"minimumMargin":{"type":"number","description":"Minimum margin"},"inventoryRequirement":{"type":"string","description":"Inventory requirement"},"combinationBehavior":{"type":"string","enum":["canCombine","cannotCombine","exclusive","deferToCentralStackingEngine"],"description":"Preliminary combination behaviour; the central stacking engine has the final say."}}},
"CheapestLowestValueItemPromotionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Cheapest / Lowest-Value Item Promotion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eligibleProducts":{"type":"string","description":"Eligible products"},"eligibleCategories":{"type":"string","description":"Eligible categories"},"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"numberOfFreeItems":{"type":"integer","description":"Number of free items"},"cheapestLowestPricedSelection":{"type":"string","description":"Cheapest/lowest-priced selection"},"maximumFreeItemValue":{"type":"string","description":"Maximum free-item value"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"},"cheapestItemFree":{"type":"string","description":"Cheapest item free"},"nCheapestItemsFree":{"type":"string","description":"N cheapest items free"}}},
"EvaluatePromotionsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","channel","lines"],"properties":{"venueId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"},"subjectId":{"type":"string","format":"uuid"},"membershipTierId":{"type":"string","format":"uuid"},"couponCodes":{"type":"array","items":{"type":"string"}},"evaluateAt":{"type":"string","format":"date-time","description":"For back-office testing of a rule before publishing."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["lineId","variantId","quantity","unitPrice"],"properties":{"lineId":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"MultiBuyQuantityOfferConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Multi-Buy & Quantity Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"exactQuantity":{"type":"integer","description":"Exact quantity"},"quantityRange":{"type":"integer","description":"Quantity range"},"multiplesOfX":{"type":"string","description":"Multiples of X"},"oneFree":{"type":"string","description":"One free"},"multipleFree":{"type":"string","description":"Multiple free"},"percentageOff":{"type":"number","description":"Percentage off"},"amountOff":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount off"},"fixedTotalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed total price"},"repeatAutomatically":{"type":"string","description":"Repeat automatically"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"}}},
"OfferSimulationBasketTraceAiOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Offer Simulation, Basket Trace & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basketLines":{"type":"array","items":{"type":"string"},"description":"Basket lines evaluated"},"qualifiers":{"type":"array","items":{"type":"string"},"description":"Qualifier conditions met"},"rewards":{"type":"array","items":{"type":"string"},"description":"Rewards granted"},"guardrailsPassed":{"type":"array","items":{"type":"string"},"description":"Guardrails checked and passed"},"originalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original total"},"promotionAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion amount"},"finalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final total"}}},
"PromotionEvaluation": {"x-ticvai-persistence":"none — computed","type":"object","required":["totalDiscount","lines","applied","rejected"],"properties":{"totalDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["lineId","originalPrice","discountedPrice","discount"],"properties":{"lineId":{"type":"string"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"applied":{"type":"array","items":{"type":"object","required":["promotionId","promotionCode","discount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"couponCode":{"type":"string","nullable":true}}}},"rejected":{"type":"array","description":"Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n","items":{"type":"object","required":["promotionCode","reason"],"properties":{"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"reason":{"type":"string","enum":["conditionsNotMet","supersededByBetterOffer","exclusivePromotionApplied","redemptionLimitReached","budgetExhausted","outsideValidPeriod","wrongChannel","membershipRequired","couponRequired"]},"detail":{"type":"string"}}}}}},
"RewardSelectionSubstitutionCustomerChoiceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Reward Selection, Substitution & Customer Choice displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"offerId":{"type":"string","description":"Offer ID"},"rewardOptions":{"type":"array","items":{"type":"string"},"description":"Rewards the guest may choose ONE of"},"selectionModel":{"type":"string","enum":["automatic","customerChoice","operatorChoice","aiRecommended"],"description":"Who picks the reward: the system, the guest from configured options, the POS or call-centre operator, or an AI recommendation"},"substitutes":{"type":"array","items":{"type":"string"},"description":"Ordered substitutes when a reward is unavailable"},"maximumSubstituteValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Value protection: the most a substitute may be worth"}}}
}
```
