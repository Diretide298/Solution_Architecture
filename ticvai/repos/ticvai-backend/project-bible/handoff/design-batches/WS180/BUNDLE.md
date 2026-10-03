# WS180 — Upsell,CrossSellEngine board 1

**10 screens · 8 operations · 4 schemas · 2 permissions**

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
| `ADM-639` | Recommendation Command Center | B–D | 0 | 40 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-640` | Recommendation Strategy Manager | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-641` | Recommendation Objective & KPI Configuration | B–D | 5 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-642` | Recommendation Type & Product Relationship Manager | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-643` | Recommendation Placement & Touchpoint Manager | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-644` | Channel & Journey Strategy Manager | B–D | 0 | 20 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-645` | Recommendation Priority, Ranking & Suppression Manager17 | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-646` | Recommendation Guardrails & Business Controls | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-647` | Recommendation Policy, AI Control & Governance | B–D | 22 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-648` | Recommendation Strategy Simulator & AI Advisor | B–D | 11 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-639, ADM-640, ADM-643, ADM-644, ADM-646, ADM-647 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-639` Recommendation Command Center

**Provide the central operational dashboard for the complete TICVAI Recommendation Engine. This becomes the entry point for Marketing, Commercial, Revenue, CRM and authorized operational users.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-command-center-adm-639` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The hub of the recommendation engine: strategies, placements and their performance; attributed and incremental revenue reported apart.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRecommendationStrategies, getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationStrategies / contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Active recommendation strategies | text | not in the schema: `Active Recommendation Strategies` |
| Active recommendation rules | text | not in the schema: `Active Recommendation Rules` |
| AI managed recommendations | text | not in the schema: `AI-Managed Recommendations` |
| Recommendation impressions | text | not in the schema: `Recommendation Impressions` |
| Recommendation clicks | text | not in the schema: `Recommendation Clicks` |
| Recommendation acceptance | text | not in the schema: `Recommendation Acceptance` |
| Recommendation conversion rate | text | not in the schema: `Recommendation Conversion Rate` |
| Upsell revenue | text | not in the schema: `Upsell Revenue` |
| Cross sell revenue | text | not in the schema: `Cross-Sell Revenue` |
| Incremental revenue | text | not in the schema: `Incremental Revenue` |
| Average basket uplift | text | not in the schema: `Average Basket Uplift` |
| Recommendation attach rate | text | not in the schema: `Recommendation Attach Rate` |
| Healthy | text | not in the schema: `Healthy` |
| Monitor | text | not in the schema: `Monitor` |
| Underperforming | text | not in the schema: `Underperforming` |
| Conflict | text | not in the schema: `Conflict` |
| Inventory issue | text | not in the schema: `Inventory Issue` |
| No eligible product | text | not in the schema: `No Eligible Product` |
| AI warning | text | not in the schema: `AI Warning` |
| Suspended | text | not in the schema: `Suspended` |

**The selected recommendation** (detail panel): The pack groups this record's detail under its own headings: “Break down by”.

| Shows | Format | Notes |
|---|---|---|
| Active recommendation strategies | text | not in the schema: `Active Recommendation Strategies` |
| Active recommendation rules | text | not in the schema: `Active Recommendation Rules` |
| AI managed recommendations | text | not in the schema: `AI-Managed Recommendations` |
| Recommendation impressions | text | not in the schema: `Recommendation Impressions` |
| Recommendation clicks | text | not in the schema: `Recommendation Clicks` |
| Recommendation acceptance | text | not in the schema: `Recommendation Acceptance` |
| Recommendation conversion rate | text | not in the schema: `Recommendation Conversion Rate` |
| Upsell revenue | text | not in the schema: `Upsell Revenue` |
| Cross sell revenue | text | not in the schema: `Cross-Sell Revenue` |
| Incremental revenue | text | not in the schema: `Incremental Revenue` |
| Average basket uplift | text | not in the schema: `Average Basket Uplift` |
| Recommendation attach rate | text | not in the schema: `Recommendation Attach Rate` |
| Healthy | text | not in the schema: `Healthy` |
| Monitor | text | not in the schema: `Monitor` |
| Underperforming | text | not in the schema: `Underperforming` |
| Conflict | text | not in the schema: `Conflict` |
| Inventory issue | text | not in the schema: `Inventory Issue` |
| No eligible product | text | not in the schema: `No Eligible Product` |
| AI warning | text | not in the schema: `AI Warning` |
| Suspended | text | not in the schema: `Suspended` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **performance**: Impressions, acceptance, attributed revenue and incremental lift as separate KPIs. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance / contracts/satellite/promotions.yaml#listRecommendationStrategies)*

**Data it reads**: `listRecommendationStrategies` (onLoad, Strategies in force); `getRecommendationPerformance` (onLoad, How they are doing)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-640` Recommendation Strategy Manager: *Recommendation Strategy Manager*; carries `strategyId`
- → `ADM-641` Recommendation Objective & KPI Configuration: *Recommendation Objective & KPI Configuration*; carries `strategyId`
- → `ADM-642` Recommendation Type & Product Relationship Manager: *Recommendation Type & Product Relationship Manager*
- → `ADM-643` Recommendation Placement & Touchpoint Manager: *Recommendation Placement & Touchpoint Manager*; carries `strategyId`
- → `ADM-644` Channel & Journey Strategy Manager: *Channel & Journey Strategy Manager*; carries `strategyId`
- → `ADM-645` Recommendation Priority, Ranking & Suppression Manager17: *Recommendation Priority, Ranking & Suppression Manager17*; carries `strategyId`
- → `ADM-646` Recommendation Guardrails & Business Controls: *Recommendation Guardrails & Business Controls*; carries `strategyId`
- → `ADM-647` Recommendation Policy, AI Control & Governance: *Recommendation Policy, AI Control & Governance*; carries `strategyId`
- → `ADM-648` Recommendation Strategy Simulator & AI Advisor: *Recommendation Strategy Simulator & AI Advisor*

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
  impressions: 182000
  acceptance: 7.4%
  attributed: AED 312,000.00
  incremental: AED 96,000.00
```

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-639` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-639`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 1: Opens Recommendation Command Center → Provide the central operational dashboard for the complete TICVAI Recommendation Engine. This becomes the entry point for Marketing, Commercial, Revenue, CRM and authorized operational users.
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F287 branch at step 1 (expected): when Nothing has been set up on Recommendation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F287 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-639?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-640`, `ADM-641`, `ADM-642`, `ADM-643`, `ADM-644`, `ADM-645`, `ADM-646`, `ADM-647`, `ADM-648`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-640` Recommendation Strategy Manager

**Define the commercial strategy TICVAI should use when generating recommendations. Instead of hard-coding recommendation behavior into B2C or POS, administrators configure reusable strategies centrally. Increase cross-attraction sales.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-strategy-manager-adm-640` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Recommendation Strategy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendation strategies configured centrally: objective, placements, ranking and guardrails stated together.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRecommendationStrategies return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationStrategies; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **strategy**: Objective and guardrail on the same panel; placements per channel. *(source: contracts/satellite/promotions.yaml#createRecommendationStrategy)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation strategy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation strategy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation strategy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-119`: Upsell rules on P08 (createUpsellRule) and strategies here overlap; one model should own "what is suggested with what".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strategy:
  name: Checkout add-ons
  objective: attach rate
  placements:
  - cart
  - checkout
  guardrail: max 3, never owned items
```

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff
- `createRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-640` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-640`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 2: Works in Recommendation Strategy Manager → Define the commercial strategy TICVAI should use when generating recommendations. Instead of hard-coding recommendation behavior into B2C or POS, administrators configure reusable strategies …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-640?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Cancel.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-641` Recommendation Objective & KPI Configuration

**Define exactly what the recommendation engine should optimize. This is important because the "best" recommendation depends on the business objective. Allow weighted objectives.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators may configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-objective-kpi-configuration-adm-641` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Revenue, Incremental revenue, Membership conversion, Capacity utilization, Inventory movement. Each needs …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What the engine optimises (revenue, margin, attach, satisfaction) with weights.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Revenue, Incremental revenue, Membership conversion, Capacity utilization, Inventory movement.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-641; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum margin | select field | — | — | — | — | — | — |
| Maximum discount | select field | — | — | — | — | — | — |
| Minimum relevance score | select field | — | — | — | — | — | — |
| Minimum inventory | select field | — | — | — | — | — | — |
| Maximum recommendation frequency | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **objectives**: Weighted sliders totalling 100. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy)*

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
| Net revenue (primary button) | navigation or local | — | — | — | — |
| Incremental revenue (secondary button) | navigation or local | — | — | — | — |
| Membership conversion (secondary button) | navigation or local | — | — | — | — |
| Capacity utilization (secondary button) | navigation or local | — | — | — | — |
| Inventory movement (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies this screen edits)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation objective kpi configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation objective kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation objective kpi configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
weights:
  margin: 50
  attach: 30
  satisfaction: 20
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-641` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-641`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 4: Works in Recommendation Objective & KPI Configuration → Define exactly what the recommendation engine should optimize. This is important because the "best" recommendation depends on the business objective.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-641?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Net revenue, Incremental revenue, Membership conversion, Capacity utilization, Inventory movement.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-642` Recommendation Type & Product Relationship Manager

**Define the commercial relationships from which recommendations can be generated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-type-product-relationship-manager-adm-642` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Ticket → Ticket, Ticket → Bundle, Ticket → F&B, Ticket → Retail, Ticket → Parking, Ticket → Locker, Ticket … **Recommendation Type & Product Relationship Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Declared product relationships: upgrade ladders, cross-sells, affinities, substitutes.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Ticket → Ticket, Ticket → Bundle, Ticket → F&B, Ticket → Retail, Ticket → Parking, Ticket → Locker, Ticket → Photo, Ticket → Rental ….** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-642; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listProductRelationships return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listProductRelationships; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductRelationships` ?productId |
| Kind | text field | — | — | `listProductRelationships` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **relationship**: From, kind, to; ladders ordered. *(source: contracts/satellite/promotions.yaml#setProductRelationships)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ticket → Ticket (primary button) | navigation or local | — | — | — | — |
| Ticket → Bundle (secondary button) | navigation or local | — | — | — | — |
| Ticket → F&B (secondary button) | navigation or local | — | — | — | — |
| Ticket → Retail (secondary button) | navigation or local | — | — | — | — |
| Ticket → Parking (secondary button) | navigation or local | — | — | — | — |
| Ticket → Locker (secondary button) | navigation or local | — | — | — | — |
| Ticket → Photo (secondary button) | navigation or local | — | — | — | — |
| Ticket → Rental (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listProductRelationships` (onLoad, Ladders and cross-sells)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation type product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation type product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation type product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation type product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
relationship:
  from: Day Pass
  kind: upgradeTo
  to: Annual Pass Gold
```

#### Permissions

- `listProductRelationships` → `PRODUCT_VIEW` (read) · staff
- `setProductRelationships` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-642` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-642`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 6: Works in Recommendation Type & Product Relationship Manager → Define the commercial relationships from which recommendations can be generated.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-642?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ticket → Ticket, Ticket → Bundle, Ticket → F&B, Ticket → Retail, Ticket → Parking, Ticket → Locker, Ticket → Photo, Ticket → Rental.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-643` Recommendation Placement & Touchpoint Manager

**Define where in the customer journey recommendations are permitted to appear. This is a major requirement for the engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-placement-touchpoint-manager-adm-643` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Recommendation Placement & Touchpoint Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where in the journey recommendations may appear.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **placements**: Placements per channel as a matrix. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy / DI-961)*

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

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation placement touchpoint list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation placement touchpoint untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation placement touchpoint yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation placement touchpoint are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
placements:
  Website:
  - productPage
  - cart
  - checkout
  Point of sale:
  - posBasket
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-643` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-643`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 8: Works in Recommendation Placement & Touchpoint Manager → Define where in the customer journey recommendations are permitted to appear. This is a major requirement for the engine.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-643?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-644` Channel & Journey Strategy Manager

**Control recommendation behavior across TICVAI's omnichannel environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/channel-journey-strategy-manager-adm-644` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Channel & Journey Strategy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendation behaviour across channels and journeys.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel behaviour**: Per channel settings of the strategy. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy)*

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

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel journey strategy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel journey strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel journey strategy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel journey strategy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
setting:
  channel: Kiosk
  max: 1
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

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-644` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-644`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 10: Works in Channel & Journey Strategy Manager → Control recommendation behavior across TICVAI's omnichannel environment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-644?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-645` Recommendation Priority, Ranking & Suppression Manager17

**Define how multiple eligible recommendations are ranked before being presented. This is different from Promotion Board 8.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-priority-ranking-suppression-manager17-adm-645` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Revenue potential, Product affinity, Customer propensity, Inventory, Capacity, Commercial priority … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Ranking of eligible recommendations and suppression: fatigue limits, frequency caps, hard exclusions.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in "Manager17", a pack page number joined to the name.** Why: It would print on the title and navigation. *(source: screens/P08-venue-back-office.yaml#ADM-645; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: Revenue potential, Product affinity, Customer propensity, Inventory, Capacity, Commercial priority, Campaign priority.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-645; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setRecommendationSuppression, updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **suppression**: Caps per guest and period, exclusions list. *(source: contracts/satellite/promotions.yaml#setRecommendationSuppression)*

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
| Revenue potential (primary button) | navigation or local | — | — | — | — |
| Product affinity (secondary button) | navigation or local | — | — | — | — |
| Customer propensity (secondary button) | navigation or local | — | — | — | — |
| Inventory (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Commercial priority (secondary button) | navigation or local | — | — | — | — |
| Campaign priority (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies this screen edits)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation priority ranking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation priority ranking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation priority ranking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation priority ranking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cap: Same product at most twice a week per guest
```

#### Permissions

- `setRecommendationSuppression` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-645` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-645`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 12: Works in Recommendation Priority, Ranking & Suppression Manager17 → Define how multiple eligible recommendations are ranked before being presented. This is different from Promotion Board 8.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-645?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Revenue potential, Product affinity, Customer propensity, Inventory, Capacity, Commercial priority, Campaign priority.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-646` Recommendation Guardrails & Business Controls

**Protect the business and customer experience from inappropriate AI or rule- generated recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-guardrails-business-controls-adm-646` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Guardrails so AI or rules never recommend something inappropriate (owned items, ineligible products, unsafe combinations).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **guardrails**: Hard rules listed separately from ranking. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy / DI-959)*

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

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation guardrails business list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation guardrails business untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation guardrails business yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation guardrails business are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guardrail: Never suggest alcohol-adjacent offers to under-21 profiles
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-646` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-646`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 14: Works in Recommendation Guardrails & Business Controls → Protect the business and customer experience from inappropriate AI or rule- generated recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-646?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-647` Recommendation Policy, AI Control & Governance

**Define how much authority the TICVAI AI layer has over recommendation decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-policy-ai-control-governance-adm-647` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How much authority the AI layer has over recommendations.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRecommendationStrategies return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationStrategies; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No write operation: a configuration screen (Recommendation Policy, AI Control & Governance) declares only reads … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

**Form: Save policy** (modal, opened by *Save policy*; *Save policy* calls `updateRecommendationStrategy`, *Cancel* sends nothing)

**Collects what `updateRecommendationStrategy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateRecommendationStrategy` body |
| Code `code` | text field | required | — | — | — | — | `updateRecommendationStrategy` body |
| Name `name` | text field | required | — | — | — | — | `updateRecommendationStrategy` body |
| Objective `objective` | select | required | — | Attach revenue · Average order value · Upgrade rate · Visit frequency · Inventory balance · Guest satisfaction | — | — | `updateRecommendationStrategy` body |
| Kinds `kinds` | multi-select chips | optional | — | Upsell · Upgrade · Cross sell · Bundle · Next best offer · Reactivation | — | — | `updateRecommendationStrategy` body |
| Item kinds `itemKinds` | multi-select chips | optional | Product | Product · Offer · Reward · Challenge | — | What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour … | `updateRecommendationStrategy` body |
| Placements `placements` | multi-select chips | optional | — | Product page · Cart · Checkout · Post purchase · Pre visit email · In venue app · Kiosk · POS · Signage · Call centre · Homepage · Loyalty | — | `homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills. | `updateRecommendationStrategy` body |
| Channels `channels` | list of values (chips) | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Max recommendations `maxRecommendations` | number field | optional | 3 | — | — | A guardrail before it is a layout choice. Nine upsells at checkout is not a denser page, it is an abandoned basket. | `updateRecommendationStrategy` body |
| Min confidence `minConfidence` | number field | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Ranking weights `rankingWeights` | key and value settings | optional | — | — | — | Propensity, margin, inventory pressure, affinity, recency. | `updateRecommendationStrategy` body |
| Require availability `requireAvailability` | toggle | optional | on | — | — | — | `updateRecommendationStrategy` body |
| Exclude in basket `excludeInBasket` | toggle | optional | on | — | — | — | `updateRecommendationStrategy` body |
| Guardrails `guardrails` | group | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Max discount percent `guardrails.maxDiscountPercent` | number field | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Min margin percent `guardrails.minMarginPercent` | number field | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Never recommend categorys `guardrails.neverRecommendCategoryIds` | multi-picker: choose never recommend categorys | optional | — | — | — | — | `updateRecommendationStrategy` body |
| Require human approval `guardrails.requireHumanApproval` | toggle | optional | off | — | — | — | `updateRecommendationStrategy` body |
| Status `status` | radio group | optional | — | Draft · Active · Paused · Retired | — | — | `updateRecommendationStrategy` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateRecommendationStrategy` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateRecommendationStrategy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `updateRecommendationStrategy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save policy (secondary button) | `updateRecommendationStrategy` PUT `/recommendation-strategies/{strategyId}` | RecommendationStrategy | RecommendationStrategy | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **authority per strategy**: Rules only, AI-ranked within rules, AI-selected. *(source: contracts/satellite/promotions.yaml#listRecommendationStrategies)*

**Data it reads**: `listRecommendationStrategies` (onLoad, Policy and governance)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation policy governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation policy governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation policy governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation policy governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  strategy: Checkout add-ons
  mode: AI ranked within rules
```

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff
- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-647` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-647`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 16: Works in Recommendation Policy, AI Control & Governance → Define how much authority the TICVAI AI layer has over recommendation decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-647?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save policy.
- [ ] Every transition is wired: `ADM-639`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-648` Recommendation Strategy Simulator & AI Advisor

**Allow administrators to test recommendation strategies before activating them. This should become the final validation screen for Board 1. ↓ Board 2 shall provide TICVAI with the specialized Upsell & Upgrade Recommendation Engine responsible for identifying when a customer can be moved from their current product, ticket, experience, membership, bundle, or service to a higher-value or more valuable alternative. Board 1 established the overall recommendation strategy, placements, ranking, guardrails, and AI governance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-strategy-simulator-ai-advisor-adm-648` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Replay a strategy against history before it goes live.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only simulateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer profile | select field | — | — | — | — | — | — |
| Customer segment | select field | — | — | — | — | — | — |
| Basket | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Journey stage | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Loyalty | select field | — | — | — | — | — | — |
| Inventory conditions | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

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

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate**: Expected acceptance and revenue against the current strategy. *(source: contracts/satellite/promotions.yaml#simulateRecommendationStrategy)*

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies a simulation can replay)

**Where the user goes next**

- → `ADM-639` Recommendation Command Center: *Back to Recommendation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation strategy simulator configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation strategy simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation strategy simulator configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  acceptance: 8.1% vs 7.4%
  incremental: +AED 6,200.00 a week
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-648` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-648`
- Workshop pack: Upsell,CrossSellEngine.pdf board 1
- Flow F287 *Upsell,CrossSellEngine board 1: Recommendation Command Center*, step 18: Works in Recommendation Strategy Simulator & AI Advisor → Allow administrators to test recommendation strategies before activating them. This should become the final validation screen for Board 1.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-648?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-639`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createRecommendationStrategy": {"method":"POST","path":"/recommendation-strategies","contract":"promotions","summary":"Define objective, placements, ranking and guardrails","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"listProductRelationships": {"method":"GET","path":"/product-relationships","contract":"promotions","summary":"Upgrade ladders, cross-sells, affinities and substitutes","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"ProductRelationship"},
"listRecommendationStrategies": {"method":"GET","path":"/recommendation-strategies","contract":"promotions","summary":"The strategies deciding what gets offered where","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"placement","in":"query","required":null}],"requestBody":null,"responds":"RecommendationStrategy"},
"setProductRelationships": {"method":"PUT","path":"/product-relationships","contract":"promotions","summary":"Declare what upgrades to, pairs with or replaces what","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductRelationship"},
"setRecommendationSuppression": {"method":"PUT","path":"/recommendation-suppressions","contract":"promotions","summary":"Fatigue limits, frequency caps and hard exclusions","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecommendationSuppression","responds":"RecommendationSuppression"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ProductRelationship": {"type":"object","x-ticvai-persistence":"promotions.product_relationship","description":"Upsell boards 2.2 and 3.2. **Declared, and distinguishable from measured affinity.**","required":["fromProductId","toProductId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"fromProductId":{"type":"string","format":"uuid"},"toProductId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["upgradesTo","downgradesTo","crossSell","accessory","substitute","requires","incompatibleWith"]},"ladderPosition":{"type":"integer","nullable":true,"description":"**For upgrade ladders only.** Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*.\n"},"source":{"type":"string","enum":["declared","measured","aiProposed"],"default":"declared"},"strength":{"type":"number","nullable":true},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationSuppression": {"type":"object","x-ticvai-persistence":"promotions.recommendation_suppression","description":"Boards 1.7 and 5.7. **Fatigue is why a good recommender stops working.**","properties":{"scopePath":{"type":"string"},"maxImpressionsPerProductPerDay":{"type":"integer","nullable":true},"maxImpressionsPerGuestPerSession":{"type":"integer","nullable":true},"cooldownAfterDismissDays":{"type":"integer","nullable":true},"cooldownAfterAcceptDays":{"type":"integer","nullable":true},"hardExclusions":{"type":"array","items":{"type":"object","properties":{"segmentId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string"}}}}}}
}
```
