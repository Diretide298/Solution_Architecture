# WS182 — Upsell,CrossSellEngine board 3

**10 screens · 8 operations · 5 schemas · 3 permissions**

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
| `ADM-659` | Cross-Sell Command Center | C | 0 | 2 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-660` | Cross-Sell Relationship Builder | C | 0 | 21 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-661` | Product Affinity Matrix & Relationship Map | C | 2 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-662` | Frequently Bought Together & Basket Pattern Engine | C | 0 | 14 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-663` | Cross-Category Recommendation Manager | C | 0 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-664` | Multi-Attraction, Destination & Partner Cross-Sell | C | 0 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-665` | Basket-Aware Cross-Sell & Duplicate Prevention | C | 0 | 20 | 6 | 0 | 0 | 2 | — | notStarted (—) |
| `ADM-666` | Availability, Inventory & Capacity-Aware Cross-Sell | C | 4 | 20 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `ADM-667` | AI Cross-Sell Discovery, Scoring & Ranking Engine | C | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-668` | Cross-Sell Simulator & AI Opportunity Advisor | C | 0 | 46 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-661, ADM-662, ADM-663, ADM-664, ADM-665, ADM-667 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-659` Cross-Sell Command Center

**Provide centralized visibility into cross-sell relationships, recommendation performance, attach rates and commercial opportunities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-659 |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cross-sell-command-center-adm-659` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Cross-sell relationships and attach rates.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listUpsellCrossSell, getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listUpsellCrossSell, getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listUpsellCrossSell / contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Cross-Sell Relationships** (metric tile)

**AI-Discovered Relationships** (metric tile)

**Cross-Sell Recommendations** (metric tile)

**Recommendations Accepted** (metric tile)

**Cross-Sell Conversion** (metric tile)

**Cross-Sell Revenue** (metric tile)

**Estimated Incremental Revenue** (metric tile)

**Attach Rate** (metric tile)

**Items per Transaction** (metric tile)

**AOV Uplift** (metric tile)

**Cross-Category Revenue** (metric tile)

**Suppressed Recommendations** (metric tile)

**Every cross-sell** (data table)

| Shows | Format | Notes |
|---|---|---|
| Recommendations → acceptances → purchases → revenue | text | not in the schema: `Recommendations → Acceptances → Purchases → Revenue` |

**The selected cross-sell** (detail panel): The pack groups this record's detail under its own headings: “Break down by”, “Relationships classified”.

| Shows | Format | Notes |
|---|---|---|
| Recommendations → acceptances → purchases → revenue | text | not in the schema: `Recommendations → Acceptances → Purchases → Revenue` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **attach rates**: Base and attached product with rate. *(source: contracts/satellite/promotions.yaml#listUpsellCrossSell / contracts/satellite/promotions.yaml#getRecommendationPerformance)*

**Data it reads**: `listUpsellCrossSell` (onLoad, Upsell, Cross-Sell & Attach-Rate Analytics); `getRecommendationPerformance` (onLoad, Cross-sell performance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-660` Cross-Sell Relationship Builder: *Cross-Sell Relationship Builder*
- → `ADM-661` Product Affinity Matrix & Relationship Map: *Product Affinity Matrix & Relationship Map*
- → `ADM-662` Frequently Bought Together & Basket Pattern Engine: *Frequently Bought Together & Basket Pattern Engine*
- → `ADM-663` Cross-Category Recommendation Manager: *Cross-Category Recommendation Manager*
- → `ADM-664` Multi-Attraction, Destination & Partner Cross-Sell: *Multi-Attraction, Destination & Partner Cross-Sell*
- → `ADM-665` Basket-Aware Cross-Sell & Duplicate Prevention: *Basket-Aware Cross-Sell & Duplicate Prevention*
- → `ADM-666` Availability, Inventory & Capacity-Aware Cross-Sell: *Availability, Inventory & Capacity-Aware Cross-Sell*
- → `ADM-667` AI Cross-Sell Discovery, Scoring & Ranking Engine: *AI Cross-Sell Discovery, Scoring & Ranking Engine*
- → `ADM-668` Cross-Sell Simulator & AI Opportunity Advisor: *Cross-Sell Simulator & AI Opportunity Advisor*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-sell are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  base: Day Pass
  attached: Lunch combo
  rate: 22%
```

#### Permissions

- `listUpsellCrossSell` → `PRICE_VIEW` (read) · staff
- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-659` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-659`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 1: Opens Cross-Sell Command Center → Provide centralized visibility into cross-sell relationships, recommendation performance, attach rates and commercial opportunities.
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F289 branch at step 1 (expected): when Nothing has been set up on Cross-Sell Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F289 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-659?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-660`, `ADM-661`, `ADM-662`, `ADM-663`, `ADM-664`, `ADM-665`, `ADM-666`, `ADM-667`, `ADM-668`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-660` Cross-Sell Relationship Builder

**Allow administrators to manually define governed complementary-product relationships.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-660 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cross-sell-relationship-builder-adm-660` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Experience Extension, Destination Extension, Service Add-On, Partner Product. Each needs an operation, or … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Cross-Sell Relationship Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Governed complementary-product relationships defined by hand.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Experience Extension, Destination Extension, Service Add-On, Partner Product.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-660; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setProductRelationships and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductRelationships` ?productId |
| Kind | text field | — | — | `listProductRelationships` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **cross-sell**: From, pairs with, strength. *(source: contracts/satellite/promotions.yaml#setProductRelationships)*

#### Outputs: what the screen shows and produces

**Shown**

**Every cross-sell relationship** (data table)

| Shows | Format | Notes |
|---|---|---|
| Manual | text | not in the schema: `Manual` |
| Historical data | text | not in the schema: `Historical Data` |
| AI discovered | text | not in the schema: `AI Discovered` |
| Campaign | text | not in the schema: `Campaign` |
| Partner | text | not in the schema: `Partner` |
| Imported | text | not in the schema: `Imported` |

**Relationships** (data table, from `listProductRelationships`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| From product | the name it points at, never the id | — |
| To product | the name it points at, never the id | — |
| Kind | chip: Upgrades to, Downgrades to, Cross sell, Accessory, Substitute, Requires… | — |
| Ladder position | 1,234 | For upgrade ladders only. Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*. |
| Source | chip: Declared, Measured, AI proposed | — |
| Strength | 1,234.5 | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |

**The selected cross-sell relationship** (detail panel): The pack groups this record's detail under its own headings: “Water Park Admission”, “Cross-Sell”, “For every relationship”, “One-Way”, “Two-Way”.

| Shows | Format | Notes |
|---|---|---|
| Manual | text | not in the schema: `Manual` |
| Historical data | text | not in the schema: `Historical Data` |
| AI discovered | text | not in the schema: `AI Discovered` |
| Campaign | text | not in the schema: `Campaign` |
| Partner | text | not in the schema: `Partner` |
| Imported | text | not in the schema: `Imported` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Experience Extension (primary button) | navigation or local | — | — | — | — |
| Destination Extension (secondary button) | navigation or local | — | — | — | — |
| Service Add-On (secondary button) | navigation or local | — | — | — | — |
| Partner Product (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listProductRelationships` (onLoad, The product relationships already declared)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell relationship list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell relationship untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell relationship yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-sell relationship are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
relationship:
  from: Cabana half day
  pairsWith: Poolside lunch
```

#### Permissions

- `setProductRelationships` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductRelationships` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-660` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-660`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 2: Works in Cross-Sell Relationship Builder → Allow administrators to manually define governed complementary-product relationships.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-660?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Experience Extension, Destination Extension, Service Add-On, Partner Product.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-661` Product Affinity Matrix & Relationship Map

**Provide a visual representation of how strongly products and categories relate to one another.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-661 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/product-affinity-matrix-relationship-map-adm-661` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How strongly products relate, measured from baskets, as a visual map.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getProductAffinity return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getProductAffinity; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product affinity relationship | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product, category, segment, channel, season and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getProductAffinity` ?productId |
| Min lift | number field | 1.2 | — | `getProductAffinity` ?minLift |
| Window days | number field (days) | 90 | — | `getProductAffinity` ?windowDays |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **affinity map**: Nodes and weighted links; measured, not declared. *(source: contracts/satellite/promotions.yaml#getProductAffinity)*

**Data it reads**: `getProductAffinity` (onLoad, The affinity matrix, measured)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product affinity relationship list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product affinity relationship untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product affinity relationship yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product affinity relationship are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
affinity:
  a: Day Pass Child
  b: Kids meal
  lift: 2.4
```

#### Permissions

- `getProductAffinity` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.5.13 | System shall recommend bundle combinations based on historical sales, guest behavior, demographics, seasonality, attraction popularity, and purchasing trends. | Admission and Access | CONTRACTED_PARTIAL | `getProductAffinity` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-661` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-661`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 4: Works in Product Affinity Matrix & Relationship Map → Provide a visual representation of how strongly products and categories relate to one another.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-661?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-662` Frequently Bought Together & Basket Pattern Engine

**Analyze transaction baskets to discover products commonly purchased together.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-662 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/frequently-bought-together-basket-pattern-engine-adm-662` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Products commonly bought together, discovered from baskets.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getProductAffinity return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getProductAffinity; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getProductAffinity` ?productId |
| Min lift | number field | 1.2 | — | `getProductAffinity` ?minLift |
| Window days | number field (days) | 90 | — | `getProductAffinity` ?windowDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every frequently bought together** (data table)

| Shows | Format | Notes |
|---|---|---|
| Product pairs | text | not in the schema: `Product pairs` |
| Product triplets | text | not in the schema: `Product triplets` |
| Category relationships | text | not in the schema: `Category relationships` |
| Sequential purchases | text | not in the schema: `Sequential purchases` |
| Same visit purchases | text | not in the schema: `Same-visit purchases` |
| Pre visit purchases | text | not in the schema: `Pre-visit purchases` |
| Post purchase additions | text | not in the schema: `Post-purchase additions` |

**The selected frequently bought together** (detail panel): The pack groups this record's detail under its own headings: “Water Park Admission”, “Purchase Rate”, “Photo”, “Package”, “Suggested new relationship”.

| Shows | Format | Notes |
|---|---|---|
| Product pairs | text | not in the schema: `Product pairs` |
| Product triplets | text | not in the schema: `Product triplets` |
| Category relationships | text | not in the schema: `Category relationships` |
| Sequential purchases | text | not in the schema: `Sequential purchases` |
| Same visit purchases | text | not in the schema: `Same-visit purchases` |
| Pre visit purchases | text | not in the schema: `Pre-visit purchases` |
| Post purchase additions | text | not in the schema: `Post-purchase additions` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **patterns**: Pairs and triples with support and lift. *(source: contracts/satellite/promotions.yaml#getProductAffinity)*

**Data it reads**: `getProductAffinity` (onLoad, Frequently bought together, with lift)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The frequently bought together list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the frequently bought together untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No frequently bought together yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the frequently bought together are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pattern:
  items:
  - Day Pass
  - Locker
  - Towel
  support: 6%
```

#### Permissions

- `getProductAffinity` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.5.13 | System shall recommend bundle combinations based on historical sales, guest behavior, demographics, seasonality, attraction popularity, and purchasing trends. | Admission and Access | CONTRACTED_PARTIAL | `getProductAffinity` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-662` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-662`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 6: Works in Frequently Bought Together & Basket Pattern Engine → Analyze transaction baskets to discover products commonly purchased together.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-662?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-663` Cross-Category Recommendation Manager

**Manage recommendations across TICVAI's different commercial modules. This is especially important because TICVAI is not only a ticketing platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-663 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cross-category-recommendation-manager-adm-663` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Cross-Category Recommendation Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendations across commercial modules (ticketing to F&B, retail, rentals).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setProductRelationships and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductRelationships` ?productId |
| Kind | text field | — | — | `listProductRelationships` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **cross-module relationship**: From and to across modules. *(source: contracts/satellite/promotions.yaml#setProductRelationships)*

#### Outputs: what the screen shows and produces

**Shown**

**Relationships** (data table, from `listProductRelationships`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| From product | the name it points at, never the id | — |
| To product | the name it points at, never the id | — |
| Kind | chip: Upgrades to, Downgrades to, Cross sell, Accessory, Substitute, Requires… | — |
| Ladder position | 1,234 | For upgrade ladders only. Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*. |
| Source | chip: Declared, Measured, AI proposed | — |
| Strength | 1,234.5 | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product relationships (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listProductRelationships` (onLoad, The product relationships already declared)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-category recommendation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-category recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-category recommendation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-category recommendation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
relationship:
  from: Desert Symphony ticket
  to: Harbour Kitchen pre-show dinner
```

#### Permissions

- `setProductRelationships` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductRelationships` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-663` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-663`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 8: Works in Cross-Category Recommendation Manager → Manage recommendations across TICVAI's different commercial modules. This is especially important because TICVAI is not only a ticketing platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-663?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product relationships, Cancel.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-664` Multi-Attraction, Destination & Partner Cross-Sell

**Support cross-selling beyond the original venue or attraction. This addresses the matrix requirements around multi-destination and external product combinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-664 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/multi-attraction-destination-partner-cross-sell-adm-664` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Cross-selling beyond the venue: other attractions, destinations, partners.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setProductRelationships and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductRelationships` ?productId |
| Kind | text field | — | — | `listProductRelationships` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **partner relationship**: Partner products as targets. *(source: contracts/satellite/promotions.yaml#setProductRelationships)*

#### Outputs: what the screen shows and produces

**Shown**

**Relationships** (data table, from `listProductRelationships`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| From product | the name it points at, never the id | — |
| To product | the name it points at, never the id | — |
| Kind | chip: Upgrades to, Downgrades to, Cross sell, Accessory, Substitute, Requires… | — |
| Ladder position | 1,234 | For upgrade ladders only. Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*. |
| Source | chip: Declared, Measured, AI proposed | — |
| Strength | 1,234.5 | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product relationships (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listProductRelationships` (onLoad, The product relationships already declared)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-attraction destination partner list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-attraction destination partner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-attraction destination partner yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-attraction destination partner are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
relationship:
  from: Dune Park Day Pass
  to: Coastal Aqua Day Pass (sister venue)
```

#### Permissions

- `setProductRelationships` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductRelationships` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-664` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-664`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 10: Works in Multi-Attraction, Destination & Partner Cross-Sell → Support cross-selling beyond the original venue or attraction. This addresses the matrix requirements around multi-destination and external product combinations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-664?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product relationships, Cancel.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-665` Basket-Aware Cross-Sell & Duplicate Prevention

**Make cross-selling aware of the customer's complete current basket. This is critical because basic recommendation engines often recommend something the customer already owns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-665 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/basket-aware-cross-sell-duplicate-prevention-adm-665` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Cross-selling aware of the whole basket; never suggest what the guest already owns.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **duplicate prevention**: On by default and not switchable. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy / DI-959)*

#### Outputs: what the screen shows and produces

**Shown**

**Strategies** (data table, from `listRecommendationStrategies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Objective | chip: Attach revenue, Average order value, Upgrade rate, Visit frequency, Inventory … | — |
| Kinds | list or chips (count when long) | — |
| Item kinds | list or chips (count when long) | What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18) … |
| Placements | list or chips (count when long) | `homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements … |
| Channels | list or chips (count when long) | — |
| Max recommendations | 1,234 | A guardrail before it is a layout choice. Nine upsells at checkout is not a denser page, it is an abandoned basket. |
| Min confidence | 1,234.5 | — |
| Ranking weights | grouped details | Propensity, margin, inventory pressure, affinity, recency. |
| Require availability | yes / no (icon or chip) | — |
| Exclude in basket | yes / no (icon or chip) | — |
| Guardrails | grouped details | — |
| Max discount percent | 1,234.5 | — |
| Min margin percent | 1,234.5 | — |
| Never recommend categorys | list or chips (count when long) | — |
| Require human approval | yes / no (icon or chip) | — |
| Status | chip: Draft, Active, Paused, Retired | — |
| Effective from | 1 Oct 2026 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies this screen edits)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The basket-aware cross-sell duplicate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the basket-aware cross-sell duplicate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No basket-aware cross-sell duplicate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the basket-aware cross-sell duplicate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Annual pass holders are never offered a Day Pass
```

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-665` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-665`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 12: Works in Basket-Aware Cross-Sell & Duplicate Prevention → Make cross-selling aware of the customer's complete current basket. This is critical because basic recommendation engines often recommend something the customer already owns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-665?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-666` Availability, Inventory & Capacity-Aware Cross-Sell

**Ensure recommendations reflect actual operational availability.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-666 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/availability-inventory-capacity-aware-cross-sell-adm-666` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendations reflect real availability and capacity.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Continue recommending | select field | — | — | — | — | — | — |
| Reduce ranking | select field | — | — | — | — | — | — |
| Suppress | select field | — | — | — | — | — | — |
| Recommend substitute | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **availability awareness**: Minimum availability threshold before a product is suggested. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy)*

#### Outputs: what the screen shows and produces

**Shown**

**Strategies** (data table, from `listRecommendationStrategies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Objective | chip: Attach revenue, Average order value, Upgrade rate, Visit frequency, Inventory … | — |
| Kinds | list or chips (count when long) | — |
| Item kinds | list or chips (count when long) | What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18) … |
| Placements | list or chips (count when long) | `homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements … |
| Channels | list or chips (count when long) | — |
| Max recommendations | 1,234 | A guardrail before it is a layout choice. Nine upsells at checkout is not a denser page, it is an abandoned basket. |
| Min confidence | 1,234.5 | — |
| Ranking weights | grouped details | Propensity, margin, inventory pressure, affinity, recency. |
| Require availability | yes / no (icon or chip) | — |
| Exclude in basket | yes / no (icon or chip) | — |
| Guardrails | grouped details | — |
| Max discount percent | 1,234.5 | — |
| Min margin percent | 1,234.5 | — |
| Never recommend categorys | list or chips (count when long) | — |
| Require human approval | yes / no (icon or chip) | — |
| Status | chip: Draft, Active, Paused, Retired | — |
| Effective from | 1 Oct 2026 | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies this screen edits)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability inventory capacity-aware configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability inventory capacity-aware untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability inventory capacity-aware configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Do not suggest a slot under 10% remaining
```

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-666` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-666`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 14: Works in Availability, Inventory & Capacity-Aware Cross-Sell → Ensure recommendations reflect actual operational availability.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-666?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-667` AI Cross-Sell Discovery, Scoring & Ranking Engine

**Use AI to discover and rank the strongest complementary products for the current customer/context.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-667 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-cross-sell-discovery-scoring-ranking-engine-adm-667` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI discovery and ranking of complementary products for the context.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getProductAffinity return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getProductAffinity; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getProductAffinity` ?productId |
| Min lift | number field | 1.2 | — | `getProductAffinity` ?minLift |
| Window days | number field (days) | 90 | — | `getProductAffinity` ?windowDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **ranked candidates**: Candidates with score and reason. *(source: contracts/satellite/promotions.yaml#getProductAffinity)*

**Data it reads**: `getProductAffinity` (onLoad, Discovery and scoring)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell discovery scoring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell discovery scoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell discovery scoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-sell discovery scoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
candidate:
  product: Photo package
  score: 0.64
```

#### Permissions

- `getProductAffinity` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.5.13 | System shall recommend bundle combinations based on historical sales, guest behavior, demographics, seasonality, attraction popularity, and purchasing trends. | Admission and Access | CONTRACTED_PARTIAL | `getProductAffinity` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-667` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-667`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 16: Works in AI Cross-Sell Discovery, Scoring & Ranking Engine → Use AI to discover and rank the strongest complementary products for the current customer/context.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-667?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-668` Cross-Sell Simulator & AI Opportunity Advisor

**Allow administrators to test cross-sell strategies and AI recommendations before activation. ↓**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-668 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cross-sell-simulator-ai-opportunity-advisor-adm-668` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test cross-sell strategies before activation.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only simulateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cross-sell simulator opportunity** (data table)

| Shows | Format | Notes |
|---|---|---|
| Recommendation generated | text | not in the schema: `Recommendation generated` |
| Product | text | not in the schema: `Product` |
| Target product | text | not in the schema: `Target product` |
| Customer/session where permitted | text | not in the schema: `Customer/session where permitted` |
| Channel | text | not in the schema: `Channel` |
| Placement | text | not in the schema: `Placement` |
| Rank | text | not in the schema: `Rank` |
| Impression | text | not in the schema: `Impression` |
| Click/select | text | not in the schema: `Click/select` |
| Add to cart | text | not in the schema: `Add to cart` |
| Purchase | text | not in the schema: `Purchase` |
| Redemption | text | not in the schema: `Redemption` |
| Revenue | text | not in the schema: `Revenue` |

**Strategies** (data table, from `listRecommendationStrategies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Objective | chip: Attach revenue, Average order value, Upgrade rate, Visit frequency, Inventory … | — |
| Kinds | list or chips (count when long) | — |
| Item kinds | list or chips (count when long) | What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18) … |
| Placements | list or chips (count when long) | `homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements … |
| Channels | list or chips (count when long) | — |
| Max recommendations | 1,234 | A guardrail before it is a layout choice. Nine upsells at checkout is not a denser page, it is an abandoned basket. |
| Min confidence | 1,234.5 | — |
| Ranking weights | grouped details | Propensity, margin, inventory pressure, affinity, recency. |
| Require availability | yes / no (icon or chip) | — |
| Exclude in basket | yes / no (icon or chip) | — |
| Guardrails | grouped details | — |
| Max discount percent | 1,234.5 | — |
| Min margin percent | 1,234.5 | — |
| Never recommend categorys | list or chips (count when long) | — |
| Require human approval | yes / no (icon or chip) | — |
| Status | chip: Draft, Active, Paused, Retired | — |
| Effective from | 1 Oct 2026 | — |

**The selected cross-sell simulator opportunity** (detail panel): The pack groups this record's detail under its own headings: “Basket”, “Candidate Results”, “Expected Incremental Value”, “Maximum Expected Incremental Revenue”, “Current Basket”, “Potential Cross-Sell Products”.

| Shows | Format | Notes |
|---|---|---|
| Recommendation generated | text | not in the schema: `Recommendation generated` |
| Product | text | not in the schema: `Product` |
| Target product | text | not in the schema: `Target product` |
| Customer/session where permitted | text | not in the schema: `Customer/session where permitted` |
| Channel | text | not in the schema: `Channel` |
| Placement | text | not in the schema: `Placement` |
| Rank | text | not in the schema: `Rank` |
| Impression | text | not in the schema: `Impression` |
| Click/select | text | not in the schema: `Click/select` |
| Add to cart | text | not in the schema: `Add to cart` |
| Purchase | text | not in the schema: `Purchase` |
| Redemption | text | not in the schema: `Redemption` |
| Revenue | text | not in the schema: `Revenue` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create relationship, Edit relationship, Activate relationship, Approve AI relationship, Enable partner relationship, Change affinity threshold, Change category permissions, Override suppression, Import relationships. Each needs attaching to the control it gates, or the screen needs the control.

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate**: As ADM-648. *(source: contracts/satellite/promotions.yaml#simulateRecommendationStrategy)*

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies a simulation can replay)

**Where the user goes next**

- → `ADM-659` Cross-Sell Command Center: *Back to Cross-Sell Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell simulator opportunity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell simulator opportunity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell simulator opportunity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-sell simulator opportunity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  attach: 24% vs 22%
```

#### Permissions

- `simulateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-668` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-668`
- Workshop pack: Upsell,CrossSellEngine.pdf board 3
- Flow F289 *Upsell,CrossSellEngine board 3: Cross-Sell Command Center*, step 18: Works in Cross-Sell Simulator & AI Opportunity Advisor → Allow administrators to test cross-sell strategies and AI recommendations before activation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-668?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-659`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
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
"getProductAffinity": {"method":"GET","path":"/product-affinity","contract":"promotions","summary":"What is actually bought together","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null},{"name":"minLift","in":"query","required":null},{"name":"windowDays","in":"query","required":null}],"requestBody":null,"responds":"ProductAffinity"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"listProductRelationships": {"method":"GET","path":"/product-relationships","contract":"promotions","summary":"Upgrade ladders, cross-sells, affinities and substitutes","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"ProductRelationship"},
"listRecommendationStrategies": {"method":"GET","path":"/recommendation-strategies","contract":"promotions","summary":"The strategies deciding what gets offered where","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"placement","in":"query","required":null}],"requestBody":null,"responds":"RecommendationStrategy"},
"listUpsellCrossSell": {"method":"GET","path":"/upsell-cross-sell","contract":"promotions","summary":"Upsell, Cross-Sell & Attach-Rate Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UpsellCrossSellAttachRateAnalyticsView"},
"setProductRelationships": {"method":"PUT","path":"/product-relationships","contract":"promotions","summary":"Declare what upgrades to, pairs with or replaces what","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductRelationship"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ProductAffinity": {"type":"object","description":"Upsell boards 3.3 and 3.4. **Support and lift together**, because high support with no lift is two popular products rather than a relationship.\n","properties":{"fromProductId":{"type":"string","format":"uuid"},"toProductId":{"type":"string","format":"uuid"},"basketsTogether":{"type":"integer"},"support":{"type":"number"},"confidence":{"type":"number"},"lift":{"type":"number"},"windowDays":{"type":"integer"},"computedAt":{"type":"string","format":"date-time"}}},
"ProductRelationship": {"type":"object","x-ticvai-persistence":"promotions.product_relationship","description":"Upsell boards 2.2 and 3.2. **Declared, and distinguishable from measured affinity.**","required":["fromProductId","toProductId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"fromProductId":{"type":"string","format":"uuid"},"toProductId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["upgradesTo","downgradesTo","crossSell","accessory","substitute","requires","incompatibleWith"]},"ladderPosition":{"type":"integer","nullable":true,"description":"**For upgrade ladders only.** Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*.\n"},"source":{"type":"string","enum":["declared","measured","aiProposed"],"default":"declared"},"strength":{"type":"number","nullable":true},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"UpsellCrossSellAttachRateAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Upsell, Cross-Sell & Attach-Rate Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"crossSellRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cross-Sell Revenue"},"upsellRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Upsell Revenue"},"attachRate":{"type":"number","description":"Attach Rate"},"itemsPerTransaction":{"type":"string","description":"Items per Transaction"},"revenuePerTransaction":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Transaction"},"recommendedOfferAcceptance":{"type":"string","description":"Recommended Offer Acceptance"},"incrementalBasketValue":{"type":"string","description":"Incremental Basket Value"},"crossCategoryConversion":{"type":"number","description":"Cross-Category Conversion"},"ticketTicket":{"type":"string","description":"Ticket → Ticket"},"ticketFB":{"type":"string","description":"Ticket → F&B"},"ticketRetail":{"type":"string","description":"Ticket → Retail"},"ticketExperience":{"type":"string","description":"Ticket → Experience"},"ticketMembership":{"type":"string","description":"Ticket → Membership"},"fBRetail":{"type":"string","description":"F&B → Retail"},"retailFB":{"type":"string","description":"Retail → F&B"},"membershipExperience":{"type":"string","description":"Membership → Experience"}}}
}
```
