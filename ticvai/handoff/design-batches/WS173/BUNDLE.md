# WS173 — Seat Management Venue Mapping Reference v1.0 board 9

**10 screens · 6 operations · 9 schemas · 3 permissions**

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
  `CAPACITY_CONFIGURE, ORDER_MODIFY, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-1033` | Recommendation Command Center | B–D | 0 | 15 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1034` | Best Seat Recommendations | B–D | 0 | 10 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-1035` | Best Value Recommendations | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1036` | Closest-to-Stage Recommendations | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1037` | Family Seating Recommendations | B–D | 0 | 10 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1038` | Accessibility Recommendations | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1039` | Seat Upgrade Recommendations | B–D | 0 | 20 | 6 | 20 | 0 | 6 | — | notStarted (—) |
| `BO-1040` | Alternatives & Reseating | B–D | 0 | 20 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-1041` | Scoring Rules & Model Governance | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1042` | Performance, Feedback & Audit | B–D | 0 | 15 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1034, BO-1035, BO-1036, BO-1037, BO-1038, BO-1039, BO-1040, BO-1041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1033` Recommendation Command Center

**Monitor recommendation demand, quality, conversion and risk. Show recommendations served, accepted, locked, purchased, revenue uplift, fallback and no-result rates. Compare use case, channel, venue, performance, model/version, guest type and time period. Surface data gaps, drift, declining acceptance, accessibility mismatch and model/service incidents. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/recommendation-command-center-bo-1033` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat recommendation performance: served, accepted, purchased, uplift, no-result rate.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations served** (metric tile): The pack asks for recommendations served; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Recommendations served | text | not in the schema: `Recommendations served` |

**Accepted** (metric tile): The pack asks for accepted; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Accepted | text | not in the schema: `Accepted` |

**Purchased** (metric tile): The pack asks for purchased; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Purchased | text | not in the schema: `Purchased` |

**Revenue uplift** (metric tile): The pack asks for revenue uplift; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Revenue uplift | text | not in the schema: `Revenue uplift` |

**Fallback / no-result rate** (metric tile): The pack asks for fallback / no-result rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Fallback / no result rate | text | not in the schema: `Fallback / no-result rate` |

**Recommendation profiles** (data table, from `getSeatRecommendationRules`): The only thing the bound read returns is configuration; the pack's metrics are all unbound.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |

**Configuration in force** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |
| Scope path | text | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **performance**: By use case (best, value, closest, family, accessible). *(source: contracts/satellite/seating.yaml#getSeatRecommendationRules)*

**Data it reads**: `getSeatRecommendationRules` (onLoad, Scoring in force)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1034` Best Seat Recommendations: *Best Seat Recommendations*
- → `BO-1035` Best Value Recommendations: *Best Value Recommendations*
- → `BO-1036` Closest-to-Stage Recommendations: *Closest-to-Stage Recommendations*
- → `BO-1037` Family Seating Recommendations: *Family Seating Recommendations*
- → `BO-1038` Accessibility Recommendations: *Accessibility Recommendations*
- → `BO-1039` Seat Upgrade Recommendations: *Seat Upgrade Recommendations*; carries `performanceId`
- → `BO-1040` Alternatives & Reseating: *Alternatives & Reseating*; carries `performanceId`
- → `BO-1041` Scoring Rules & Model Governance: *Scoring Rules & Model Governance*
- → `BO-1042` Performance, Feedback & Audit: *Performance, Feedback & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  served: 12400
  accepted: 61%
  noResult: 3%
```

#### Permissions

- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1033` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1033`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 1: Opens Recommendation Command Center → Monitor recommendation demand, quality, conversion and risk. Show recommendations served, accepted, locked, purchased, revenue uplift, fallback and no-result rates. Compare use case, channel, venue …
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F282 branch at step 1 (expected): when Nothing has been set up on Recommendation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F282 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1034`, `BO-1035`, `BO-1036`, `BO-1037`, `BO-1038`, `BO-1039`, `BO-1040`, `BO-1041`, `BO-1042`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1034` Best Seat Recommendations

**Rank the strongest overall options for the requested quantity. Score view, distance, orientation, row, aisle, obstruction, amenities, demand and customer preference. Return valid seat groups with match score, total price, view summary, rationale and trade-offs. Support rule-based fallback when AI is unavailable or confidence falls below the configured threshold. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/best-seat-recommendations-bo-1034` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What "best seat" means at this venue (last row best vs first row best was the client's example): weighted factors and constraints.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRecommendationRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **weights**: Sliders per factor (view, distance, aisle, obstruction) with a live preview ranking on the map. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules / TRACKER Actions row 63)*

#### Outputs: what the screen shows and produces

**Shown**

**What "best" means at this venue** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Profiles | list or chips (count when long) | — |
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRecommendationRules` (onLoad, What "best" means at this venue)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The best seat recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the best seat recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No best seat recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the best seat recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
weights:
  view: 40
  distance: 30
  aisle: 10
  centre: 20
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Best-seat ranking (e.g. last-row-is-best vs. first-row-is-best, by venue sightlines) is configurable per seat map/event so the system recommends or auto-assigns the right best available seat. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-414)*
- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1034` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1034`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 2: Works in Best Seat Recommendations → Rank the strongest overall options for the requested quantity. Score view, distance, orientation, row, aisle, obstruction, amenities, demand and customer preference. Return valid seat groups with …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1035` Best Value Recommendations

**Balance quality and price to identify strong value options. Calculate value from price, view, distance, category, demand, historical preference and comparable inventory. Present a price-versus-quality matrix and explain why each option represents better value. Respect minimum/maximum budget, promotion eligibility, fee transparency and price-lock policy. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 38**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/best-value-recommendations-bo-1035` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Best value: balance of quality and price.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRecommendationRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **value scoring**: Same editor as BO-1034, value use case. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**What "best" means at this venue** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Profiles | list or chips (count when long) | — |
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRecommendationRules` (onLoad, What "best" means at this venue)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The best value recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the best value recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No best value recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the best value recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: 'Upper 204 row A: 82 quality points at AED 260.00'
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1035` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1035`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 4: Works in Best Value Recommendations → Balance quality and price to identify strong value options. Calculate value from price, view, distance, category, demand, historical preference and comparable inventory. Present a …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1036` Closest-to-Stage Recommendations

**Rank seats by meaningful proximity to the event focal point. Use configured stage/field/focal point, seat coordinates, orientation, level and route rather than row number alone. Show distance, section, row, elevation, obstruction and route information for each option. Support multiple focal points and event-specific stage layouts with the correct layout version. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/closest-to-stage-recommendations-bo-1036` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Closest to stage by true distance to the focal point, not row number.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRecommendationRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **proximity scoring**: Same editor, closest use case; uses the stage from BO-959. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**What "best" means at this venue** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Profiles | list or chips (count when long) | — |
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRecommendationRules` (onLoad, What "best" means at this venue)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The closest-to-stage recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the closest-to-stage recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No closest-to-stage recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the closest-to-stage recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: 'Floor row 1 centre: 6 m'
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1036` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1036`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 6: Works in Closest-to-Stage Recommendations → Rank seats by meaningful proximity to the event focal point. Use configured stage/field/focal point, seat coordinates, orientation, level and route rather than row number alone. Show distance …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1037` Family Seating Recommendations

**Find safe and practical seat groups for families. Prioritize contiguity, aisle preference, child-friendly areas, short routes and proximity to approved facilities. Consider adult/child ratio, age policy, stroller/service needs, family membership and budget. Explain splits or compromises and never separate minors contrary to configured policy. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/family-seating-recommendations-bo-1037` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Family seating: contiguity, aisle, child-friendly areas, short routes to facilities.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRecommendationRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **family scoring**: Same editor, family use case. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**What "best" means at this venue** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Profiles | list or chips (count when long) | — |
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRecommendationRules` (onLoad, What "best" means at this venue)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family seating recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family seating recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family seating recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the family seating recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: 4 together, aisle, 30 m from toilets
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1037` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1037`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 8: Works in Family Seating Recommendations → Find safe and practical seat groups for families. Prioritize contiguity, aisle preference, child-friendly areas, short routes and proximity to approved facilities. Consider adult/child ratio, age …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1038` Accessibility Recommendations

**Match stated access needs to verified accessible inventory and routes. Use wheelchair, companion, transfer, aisle, step-free, hearing, vision and service-animal attributes. Show companion pairing, accessible route, distance to entrance/facilities and any assistance requirement. Protect sensitive preference data, allow human-assisted review and prevent inappropriate release of protected inventory. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accessibility-recommendations-bo-1038` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Accessible recommendations matching stated needs to verified accessible seats and routes.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **accessible scoring**: Same editor, accessible use case; only seats with an accessible route qualify. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules / contracts/satellite/seating.yaml#getAccessibleSeating)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getAccessibleSeating` (onLoad, The accessible inventory)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accessibility recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accessibility recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accessibility recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accessibility recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: W-1 with companion W-2, step-free from Gate 2
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1038` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1038`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 10: Works in Accessibility Recommendations → Match stated access needs to verified accessible inventory and routes. Use wheelchair, companion, transfer, aisle, step-free, hearing, vision and service-animal attributes. Show companion pairing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1039` Seat Upgrade Recommendations

**Offer an eligible higher-value alternative before or after purchase. Compare current and candidate seat on view, distance, level, amenities, accessibility and price difference. Apply membership, loyalty, promotion, exchange, refund, fee and event cutoff rules. Show expected value and acquire new inventory before releasing the original seat through a safe exchange flow. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 39**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/seat-upgrade-recommendations-bo-1039` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** An eligible better seat offered before or after purchase, with the price difference.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only recommendSeats and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat status for a performance** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **upgrade option**: Current vs candidate seat and the difference to pay. *(source: contracts/satellite/seating.yaml#recommendSeats)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat upgrade recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat upgrade recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat upgrade recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat upgrade recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
upgrade:
  from: Upper 204 C-4
  to: Lower 102 F-8
  pay: AED 120.00
```

#### Permissions

- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.10 | The system should provide the option to enable or disable seat reservation for any type of event ticket. Guests shall be able to reserve a seat from a GUI when they purchase a ticket. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 1.3.11 | The system should offer assigned seating with multiple options for seat selection such as “pick a seat” or “best seat available.” Assigned seating should be made available both online and at the POS. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 21.5.1 | Choose My Seats | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.2 | Find Seats For Me | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.16 | Best Available Seat Selection | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.7.5 | Accessibility Rules | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.8.4 | Accessible Seat Filters | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.1 | Best Seat Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.2 | Best Value Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.3 | Closest-to-Stage Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.5 | Accessibility Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.7 | Alternative Seat Suggestions | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1039` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1039`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 12: Works in Seat Upgrade Recommendations → Offer an eligible higher-value alternative before or after purchase. Compare current and candidate seat on view, distance, level, amenities, accessibility and price difference. Apply membership …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1040` Alternatives & Reseating

**Provide comparable options when selected or issued seats become unavailable. Rank same-price, better-price, better-view, same-section, accessible and adjacent alternatives. Support operational reseating for layout changes, maintenance, production blocks and customer requests. Explain impact, require approval/acceptance where applicable and preserve original-to-new seat lineage. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/alternatives-reseating-bo-1040` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Move a booked party when seats become unavailable, and tell them.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only reassignSeats and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat status for a performance** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Reseat**: Comparable alternatives ranked; the party is moved and notified. *(source: contracts/satellite/seating.yaml#reassignSeats)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The alternatives reseating list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the alternatives reseating untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No alternatives reseating yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the alternatives reseating are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reseat:
  party: Order DP-2026-104882
  from: Lower 104 K-7..8
  to: Lower 104 J-7..8
  reason: broken seat
```

#### Permissions

- `reassignSeats` → `ORDER_MODIFY` (operate) · staff
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.4 | Seat Reservation Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.5 | Seat Sales Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.5.13 | Real-Time Seat Availability | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1040` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1040`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 14: Works in Alternatives & Reseating → Provide comparable options when selected or issued seats become unavailable. Rank same-price, better-price, better-view, same-section, accessible and adjacent alternatives. Support operational …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1041` Scoring Rules & Model Governance

**Configure recommendation objectives, constraints and AI controls. Set weighted factors, hard constraints, tie-breakers, minimum score, fallback, audience and use-case priority. Manage model/version, training/evaluation metadata, approval, effective dates and rollback. Run test personas, backtests, bias/accessibility checks and scenario comparison before publication. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/scoring-rules-model-governance-bo-1041` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendation objectives and constraints: weights, hard constraints, tie-breakers, minimum score, fallback.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRecommendationRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **constraints**: Hard constraints listed separately from weights. *(source: contracts/satellite/seating.yaml#setSeatRecommendationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**What "best" means at this venue** (detail panel, from `getSeatRecommendationRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Profiles | list or chips (count when long) | — |
| Kind | chip: Best seat, Best value, Closest to stage, Family together, Accessible, Upgrade | — |
| Weights | grouped details | Sightline, distance, centrality, row, price, availability, aisle proximity, legroom. |
| Preferred sections | list or chips (count when long) | — |
| Avoid sections | list or chips (count when long) | — |
| Contiguity weight | 1,234.5 | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRecommendationRules` (onLoad, What "best" means at this venue)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scoring rules model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scoring rules model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scoring rules model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the scoring rules model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
constraint: Never split a party of 4 or fewer
```

#### Permissions

- `setSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1041` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1041`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 16: Works in Scoring Rules & Model Governance → Configure recommendation objectives, constraints and AI controls. Set weighted factors, hard constraints, tie-breakers, minimum score, fallback, audience and use-case priority. Manage model/version …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1042` Performance, Feedback & Audit

**Measure realized recommendation quality and accountability. Report acceptance, conversion, revenue, upgrade, abandonment, no-result and downstream satisfaction. Capture accept/reject, reason, user feedback, actual purchase and post-event outcome for learning. Monitor drift and disparity and retain inputs, candidates, scores, explanation, model/version and human decisions. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 40 Board 10 - Seat Revenue Management & Forecasting Figure 10. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 41**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/performance-feedback-audit-bo-1042` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Realised recommendation quality and the audit of accepted and rejected suggestions.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Acceptance rate** (metric tile): The pack asks for acceptance rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Acceptance rate | text | not in the schema: `Acceptance rate` |

**Conversion** (metric tile): The pack asks for conversion; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Conversion | text | not in the schema: `Conversion` |

**Upgrade rate** (metric tile): The pack asks for upgrade rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Upgrade rate | text | not in the schema: `Upgrade rate` |

**No-result rate** (metric tile): The pack asks for no-result rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| No result rate | text | not in the schema: `No-result rate` |

**Recommendation decisions** (data table): The retained inputs, candidates, scores, explanation and human decision; no operation returns them.

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | not in the schema: `Recommendation` |
| Guest action (accept / reject) | text | not in the schema: `Guest action (accept / reject)` |
| Reason | text | not in the schema: `Reason` |
| User feedback | text | not in the schema: `User feedback` |
| Actual purchase | text | not in the schema: `Actual purchase` |
| Model / version | text | not in the schema: `Model / version` |
| Score | text | not in the schema: `Score` |

**Scoring configuration at the time** (detail panel, from `getSeatRecommendationRules`): Current configuration only; the contract keeps no history of it.

| Shows | Format | Notes |
|---|---|---|
| Profiles | list or chips (count when long) | — |
| Reverse row order | yes / no (icon or chip) | Last-row-is-best against first-row-is-best, which the minute names as the worked example and which differs by venue sightline. |
| Explain to guest | yes / no (icon or chip) | — |
| Scope path | text | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **outcomes**: Acceptance and conversion by use case. *(source: contracts/satellite/seating.yaml#getSeatRecommendationRules)*

**Data it reads**: `getSeatRecommendationRules` (onLoad, Performance and feedback)

**Where the user goes next**

- → `BO-1033` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The performance feedback audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the performance feedback audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No performance feedback audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the performance feedback audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outcome:
  useCase: family
  acceptance: 68%
```

#### Permissions

- `getSeatRecommendationRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1042` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1042`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 9
- Flow F282 *Seat Management Venue Mapping Reference v1.0 board 9: Recommendation Command …*, step 18: Works in Performance, Feedback & Audit → Measure realized recommendation quality and accountability. Report acceptance, conversion, revenue, upgrade, abandonment, no-result and downstream satisfaction. Capture accept/reject, reason, user …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1033`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAccessibleSeating": {"method":"GET","path":"/accessible-seating","contract":"seating","summary":"Accessible seats, their routes and who may buy them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"seatMapId","in":"query","required":true}],"requestBody":null,"responds":"AccessibleSeating"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getSeatRecommendationRules": {"method":"GET","path":"/seat-recommendation-rules","contract":"seating","summary":"What \"best\" means at this venue","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatRecommendationRules"},
"reassignSeats": {"method":"POST","path":"/seat-reassignment","contract":"seating","summary":"Move a booked party, and tell them","permission":"ORDER_MODIFY","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatReassignment"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"setSeatRecommendationRules": {"method":"PUT","path":"/seat-recommendation-rules","contract":"seating","summary":"Scoring for best seat, best value, closest, family and accessible","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRules","responds":"SeatRecommendationRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibleSeating": {"type":"object","x-ticvai-persistence":"seating.accessible","description":"Boards 7.6 to 7.8. **An accessible seat with no accessible route is not an accessible seat.**\n","properties":{"seatMapId":{"type":"string","format":"uuid"},"spaces":{"type":"array","items":{"type":"object","properties":{"seatId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["wheelchairSpace","transferSeat","ambulant","easyAccess","assistanceDog","hearingLoop","visuallyImpaired"]},"routeDescription":{"type":"string","nullable":true},"stepFree":{"type":"boolean","default":true},"nearestAccessibleWc":{"type":"string","nullable":true}}}},"eligibility":{"type":"string","enum":["open","selfDeclared","verifiedOnce","verifiedEachTime"],"default":"selfDeclared","description":"**Contested in both directions.** Open sale leaves none for the guests who need them; hard gating turns people away at the door.\n"},"minimumProvisionPercent":{"type":"number","nullable":true},"scopePath":{"type":"string"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatReassignment": {"type":"object","x-ticvai-persistence":"seating.reassignment","description":"Board 9.8. **Never silently downgrades.**","properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true},"fromSeatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"toSeatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string"},"priceDifference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundIssued":{"type":"boolean","default":false},"guestNotifiedAt":{"type":"string","format":"date-time","nullable":true},"performedBy":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationRules": {"type":"object","x-ticvai-persistence":"seating.recommendation_rules","description":"Board 9, and the 21 August minute: *\"best-seat ranking… must be configurable per seat map/event.\"* **Five kinds, one scoring model** — five algorithms would eventually contradict each other.\n","properties":{"seatMapId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"profiles":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["bestSeat","bestValue","closestToStage","familyTogether","accessible","upgrade"]},"weights":{"type":"object","additionalProperties":{"type":"number"},"description":"Sightline, distance, centrality, row, price, availability, aisle proximity, legroom.\n"},"preferredSectionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"avoidSectionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"contiguityWeight":{"type":"number","nullable":true}}}},"reverseRowOrder":{"type":"boolean","default":false,"description":"**Last-row-is-best against first-row-is-best**, which the minute names as the worked example and which differs by venue sightline.\n"},"explainToGuest":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]}
}
```
