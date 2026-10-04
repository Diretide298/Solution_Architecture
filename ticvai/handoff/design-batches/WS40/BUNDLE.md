# WS40 — Pricing   Revenue Management board 7

**10 screens · 13 operations · 20 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-108` | Revenue Optimization Command Center | B | 0 | 22 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-109` | Pricing Simulation Studio | B | 0 | 12 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `ADM-110` | Scenario Modeling & What-If Analysis | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-111` | A/B Pricing Experiment Studio | B | 0 | 8 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `ADM-112` | Revenue & Demand Impact Forecasting | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `ADM-113` | AI Recommendation Review & Decision Queue | B | 5 | 22 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-114` | Automation Policy & Autonomous Pricing Orchestrator | B | 47 | 0 | 5 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-115` | Live Dynamic Price Execution & Deployment Monitor | B | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-116` | Dynamic Pricing Performance & Optimization Analytics | B | 0 | 36 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `ADM-117` | AI Learning, Model Performance & Optimization Feedback | B | 18 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-111, ADM-117 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-108` Revenue Optimization Command Center

**Provide Revenue Managers with the operational control center for all dynamic pricing simulations, AI recommendations, automated changes, experiments and revenue optimization activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29844 (VM-ADM-108) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each row displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/revenue-optimization-command-center-adm-108` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Run Simulation, Review Recommendations, Start Experiment, Approve Changes, Pause Automation, Open Execution …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The control centre for dynamic pricing simulations, AI recommendations, automated changes and experiments, with revenue outcomes.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Run Simulation, Review Recommendations, Start Experiment, Approve Changes, Pause Automation, Open Execution Monitor. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listRevenue` ?venue |
| Automation mode | radio group | — | Advisory · Human in the loop · Conditional autonomous · Autonomous | `listRevenue` ?automationMode |
| Urgency | radio group | — | Low · Medium · High · Critical | `listRevenue` ?urgency |
| Rank by | select | — | Revenue opportunity · Revenue risk · Event proximity · Confidence · Inventory position · Demand variance · Urgency | `listRevenue` ?rankBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Revenue Opportunity** (metric tile)

**Incremental Revenue Generated** (metric tile)

**Active Optimizations** (metric tile)

**Recommendations Awaiting Action** (metric tile)

**Pending Simulations** (metric tile)

**Auto-Executed Changes** (metric tile)

**Approval Required** (metric tile)

**Active A/B Tests** (metric tile)

**Pricing Exceptions** (metric tile)

**Revenue at Risk** (metric tile)

**Forecast Accuracy** (metric tile)

**Optimization Success Rate** (metric tile)

**Every revenue optimization** (data table, from `listRevenue`)

| Shows | Format | Notes |
|---|---|---|
| Venue | text | Venue |
| Event product | text | Event/Product |
| Performance | text | Performance |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Forecast revenue | AED 1,234.50 | Forecast Revenue |
| Expected uplift | 1,234.5 | Expected Uplift, percent |
| Confidence | 1,234.5 | Confidence, percent |
| Automation mode | chip: Advisory, Human in the loop, Conditional autonomous, Autonomous | Automation Mode in force for this scope |
| Approval status | text | Approval Status: notRequired, pending, approved or rejected |
| Execution status | text | Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack |

**The selected revenue optimization** (detail panel): The pack groups this record's detail under its own headings: “Event Action”, “AED”, “Attraction AED Simulat”, “B 220 e”.

| Shows | Format | Notes |
|---|---|---|
| Venue | text | Venue |
| Event product | text | Event/Product |
| Performance | text | Performance |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Forecast revenue | AED 1,234.50 | Forecast Revenue |
| Expected uplift | 1,234.5 | Expected Uplift, percent |
| Confidence | 1,234.5 | Confidence, percent |
| Automation mode | chip: Advisory, Human in the loop, Conditional autonomous, Autonomous | Automation Mode in force for this scope |
| Approval status | text | Approval Status: notRequired, pending, approved or rejected |
| Execution status | text | Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run Simulation (primary button) | navigation or local | — | — | — | — |
| Review Recommendations (secondary button) | navigation or local | — | — | — | — |
| Start Experiment (secondary button) | navigation or local | — | — | — | — |
| Approve Changes (secondary button) | navigation or local | — | — | — | — |
| Pause Automation (secondary button) | navigation or local | — | — | — | — |
| Open Execution Monitor (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **activity and outcomes**: KPI summary and the list of recent automated changes with their result. *(source: contracts/spine/catalogue.yaml#listRevenue)*

**Data it reads**: `listRevenue` (onLoad, Revenue Optimization Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-109` Pricing Simulation Studio: *Works in Pricing Simulation Studio*; calls `listRevenue`
- → `ADM-110` Scenario Modeling & What-If Analysis: *Works in Scenario Modeling & What-If Analysis*; calls `listRevenue`
- → `ADM-111` A/B Pricing Experiment Studio: *Works in A/B Pricing Experiment Studio*; calls `listRevenue`
- → `ADM-112` Revenue & Demand Impact Forecasting: *Works in Revenue & Demand Impact Forecasting*; calls `listRevenue`
- → `ADM-114` Automation Policy & Autonomous Pricing Orchestrator: *Works in Automation Policy & Autonomous Pricing Orchestrator*; calls `listRevenue`
- → `ADM-115` Live Dynamic Price Execution & Deployment Monitor: *Works in Live Dynamic Price Execution & Deployment Monitor*; calls `listRevenue`
- → `ADM-116` Dynamic Pricing Performance & Optimization Analytics: *Works in Dynamic Pricing Performance & Optimization Analytics*; calls `listRevenue`
- → `ADM-117` AI Learning, Model Performance & Optimization Feedback: *Works in AI Learning, Model Performance & Optimization Feedback*; calls `listRevenue`
- → `ADM-113` AI Recommendation Review & Decision Queue: *Works in AI Recommendation Review & Decision Queue*; carries `recommendationId`; calls `listRevenue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue optimization list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  automatedChanges7d: 42
  revenueUplift: +3.1%
```

#### Permissions

- `listRevenue` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.30 | System shall support revenue optimization. | Unified Operations Dashboard | CONTRACTED | `listRevenue` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-108` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-108`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 1: Opens Revenue Optimization Command Center → Provide Revenue Managers with the operational control center for all dynamic pricing simulations, AI recommendations, automated changes, experiments and revenue optimization activity.
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F149 branch at step 1 (expected): when Nothing has been set up on Revenue Optimization Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F149 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-108?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run Simulation, Review Recommendations, Start Experiment, Approve Changes, Pause Automation, Open Execution Monitor.
- [ ] Every transition is wired: `BO-100`, `ADM-109`, `ADM-110`, `ADM-111`, `ADM-112`, `ADM-114`, `ADM-115`, `ADM-116`, `ADM-117`, `ADM-113`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-109` Pricing Simulation Studio

**Allow any proposed dynamic-pricing change to be tested before affecting live customers. This should become the sandbox of the Dynamic Pricing Engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29750 (VM-ADM-109) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pricing-simulation-studio-adm-109` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Save Scenario, Compare Scenario, Send for Approval, Start Experiment, Discard. Each needs an operation, or … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of saved pricing scenarios; the simulation itself is a PUT named setPricing.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The sandbox for a proposed dynamic pricing change: pick the scope (venue, product, event, performance, slot, category, channel, segment, dates) and the source (manual change, rule, AI recommendation, new strategy) and see the simulated outcome before any guest is affected.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The simulation is a PUT named setPricing with every scope field a string, and channel uses the catalogue Channel enum while other simulations use SalesChannel. (CHG-MOV-008)
- No read operation: the screen declares only setPricing and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Save Scenario, Compare Scenario, Send for Approval, Start Experiment, Discard. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing simulation** (data table, from `setPricing`)

| Shows | Format | Notes |
|---|---|---|
| Simulation confidence | 1,234.5 | Simulation Confidence, percent |
| Data volume | 1,234 | Data Volume: transactions behind the simulation |
| Historical similarity | 1,234.5 | Historical Similarity, percent |
| Forecast confidence | 1,234.5 | Forecast Confidence, percent |
| Elasticity confidence | 1,234.5 | Elasticity Confidence, percent |
| External signal quality | 1,234.5 | External Signal Quality, percent |

**The selected pricing simulation** (detail panel): The pack groups this record's detail under its own headings: “A simulation can originate from”, “Calculate”, “Current Strategy”, “Before simulation completes, show”.

| Shows | Format | Notes |
|---|---|---|
| Simulation confidence | 1,234.5 | Simulation Confidence, percent |
| Data volume | 1,234 | Data Volume: transactions behind the simulation |
| Historical similarity | 1,234.5 | Historical Similarity, percent |
| Forecast confidence | 1,234.5 | Forecast Confidence, percent |
| Elasticity confidence | 1,234.5 | Elasticity Confidence, percent |
| External signal quality | 1,234.5 | External Signal Quality, percent |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Scenario (primary button) | navigation or local | — | — | — | — |
| Compare Scenario (secondary button) | navigation or local | — | — | — | — |
| Send for Approval (secondary button) | navigation or local | — | — | — | — |
| Start Experiment (secondary button) | navigation or local | — | — | — | — |
| Discard (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **simulated outcome**: Baseline vs simulated price, volume, revenue and margin with confidence; nothing is published from here. *(source: contracts/spine/catalogue.yaml#setPricing / DI-601)*

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `setPricing`

**What opens over it**

- confirmDialog *Discard*: **Discard on a pricing simulation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation:
  scope: Dune Park, Day Pass, Website, Sat 22 Nov
  trigger: aiRecommendation
  change: +8%
  revenue: +AED 14,200.00
  volume: -3%
```

#### Permissions

- `setPricing` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.14 | System shall support automatic pricing simulations. | Unified Operations Dashboard | CONTRACTED | `setPricing` |
| 8.5.16 | System shall support projected revenue simulations. | Unified Operations Dashboard | CONTRACTED | `setPricing` |
| 8.5.17 | System shall support projected demand simulations. | Unified Operations Dashboard | CONTRACTED | `setPricing` |
| 8.5.44 | System shall support simulation of pricing scenarios before activation. | Unified Operations Dashboard | CONTRACTED | `setPricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting recommends pricing/promotional action ahead of demand shifts (e.g. forecast rain > recommend a discount); a simulation tool previews the likely impact of a price change before it goes live. *(client request · MoM 1 Sep 2026, 4.8 AI Demand Forecasting & Pricing Simulation · DI-601)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-109` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-109`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 2: Works in Pricing Simulation Studio → Allow any proposed dynamic-pricing change to be tested before affecting live customers. This should become the sandbox of the Dynamic Pricing Engine.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-109?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Scenario, Compare Scenario, Send for Approval, Start Experiment, Discard.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-110` Scenario Modeling & What-If Analysis

**Model how prices, demand and inventory would respond to a pricing change before it is made.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29766 (VM-ADM-110) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/scenario-modeling-what-if-analysis-adm-110` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 1 operation.** Unserved: Low Demand, Expected Demand, High Demand, Competitor Price Drop, Competitor Price Increase, Inventory … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Compare scenarios side by side (price, demand, capacity assumptions) and their projected outcomes.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Low Demand, Expected Demand, High Demand, Competitor Price Drop, Competitor Price Increase, Inventory Reduction, Custom Scenario, Save …. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): The purpose repeats the screen name and nothing creates a scenario. (CHG-WIR-026).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scenario type | select | — | Low demand · Expected demand · High demand · Sell out · Competitor price drop · Competitor price increase · Extreme weather · Rain · Nearby exhibition · Major concert · Tourism surge · Cancellation surge … | `listScenarioModelingWhat` ?scenarioType |
| Venue | text field | — | — | `listScenarioModelingWhat` ?venue |
| Search | text field | — | — | `listScenarioModelingWhat` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Low Demand (primary button) | navigation or local | — | — | — | — |
| Expected Demand (secondary button) | navigation or local | — | — | — | — |
| High Demand (secondary button) | navigation or local | — | — | — | — |
| Competitor Price Drop (secondary button) | navigation or local | — | — | — | — |
| Competitor Price Increase (secondary button) | navigation or local | — | — | — | — |
| Inventory Reduction (secondary button) | navigation or local | — | — | — | — |
| Custom Scenario (secondary button) | navigation or local | — | — | — | — |
| Save (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scenario comparison**: Scenarios as columns, outcomes as rows, best value highlighted per row. *(source: contracts/spine/catalogue.yaml#listScenarioModelingWhat / DI-943)*

**Data it reads**: `listScenarioModelingWhat` (onLoad, Scenario Modeling & What-If Analysis)

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `listScenarioModelingWhat`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scenario modeling what-if list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scenario modeling what-if untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scenario modeling what-if yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the scenario modeling what-if are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenarios:
- name: Hold price
  revenue: AED 1.20m
- name: -10% weekdays
  revenue: AED 1.26m
```

#### Permissions

- `listScenarioModelingWhat` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.15 | System shall support pricing scenario modeling. | Unified Operations Dashboard | CONTRACTED | `listScenarioModelingWhat` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-110` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-110`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 4: Works in Scenario Modeling & What-If Analysis → Scenario Modeling & What-If Analysis

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-110?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Low Demand, Expected Demand, High Demand, Competitor Price Drop, Competitor Price Increase, Inventory Reduction, Custom Scenario, Save.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-111` A/B Pricing Experiment Studio

**Allow TICVAI to scientifically test different pricing strategies using controlled customer groups. This is essential because AI should learn from actual customer behavior, not only historical assumptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29751 (VM-ADM-111) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/a-b-pricing-experiment-studio-adm-111` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of pricing experiments (setPricingExperiment has no get or list).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Controlled pricing experiments: objective, product, channel, segment, dates, variants and traffic split, so the AI learns from behaviour, not assumptions.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setPricingExperiment and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **traffic split**: Variants' shares must total 100%; the split is by a stable hash of the guest so one guest sees one price. *(source: contracts/spine/catalogue.yaml#setPricingExperiment / contracts/satellite/promotions.yaml#setPromotionVariants)*

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing experiment** (data table, from `setPricingExperiment`)

| Shows | Format | Notes |
|---|---|---|
| Sample size | 1,234 | Sample Size reached |
| Confidence level | 1,234.5 | Target Confidence Level; default 95 (decided 29 September, readiness close-out), percent |
| Experiment duration | 1,234 | Experiment Duration, days |
| Statistical significance | yes / no (icon or chip) | Statistical Significance reached at the target confidence level |

**The selected pricing experiment** (detail panel): The pack groups this record's detail under its own headings: “AED 250”, “Variant B”, “AED 265”, “Experiments must respect”, “Winner”.

| Shows | Format | Notes |
|---|---|---|
| Sample size | 1,234 | Sample Size reached |
| Confidence level | 1,234.5 | Target Confidence Level; default 95 (decided 29 September, readiness close-out), percent |
| Experiment duration | 1,234 | Experiment Duration, days |
| Statistical significance | yes / no (icon or chip) | Statistical Significance reached at the target confidence level |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `setPricingExperiment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing experiment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing experiment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing experiment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing experiment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experiment:
  name: Weekend price test
  product: Day Pass Adult
  variants:
  - AED 295.00 (50%)
  - AED 309.00 (50%)
  dates: 1-30 Nov
```

#### Permissions

- `setPricingExperiment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.43 | System shall support A/B testing of pricing strategies. | Unified Operations Dashboard | CONTRACTED | `setPricingExperiment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-111` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-111`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 6: Works in A/B Pricing Experiment Studio → Allow TICVAI to scientifically test different pricing strategies using controlled customer groups. This is essential because AI should learn from actual customer behavior, not only historical …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-111?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-112` Revenue & Demand Impact Forecasting

**Provide a dedicated commercial impact assessment before a dynamic-pricing action is approved or executed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29767 (VM-ADM-112) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Forecast; Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/revenue-demand-impact-forecasting-adm-112` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Commercial impact of a dynamic pricing action before it is approved or executed: revenue, demand, margin, channel effects, with confidence.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Recommendation | text field | — | — | `listRevenueDemandImpact` ?recommendationId |
| Simulation | text field | — | — | `listRevenueDemandImpact` ?simulationId |
| Venue | text field | — | — | `listRevenueDemandImpact` ?venue |
| Event | text field | — | — | `listRevenueDemandImpact` ?event |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Forecast net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Demand** (metric tile)

**Attendance** (metric tile)

**Occupancy** (metric tile)

**Conversion** (metric tile)

**Margin** (metric tile)

**ASP** (metric tile)

**Sell-Through** (metric tile)

**Sell-Out Probability** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **impact card**: Revenue and volume deltas with confidence band and drivers. *(source: contracts/spine/catalogue.yaml#listRevenueDemandImpact / DI-943)*

**Data it reads**: `listRevenueDemandImpact` (onLoad, Revenue & Demand Impact Forecasting)

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `listRevenueDemandImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue demand impact list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue demand impact untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue demand impact yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue demand impact are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
impact:
  action: +8% Sat online
  revenue: +AED 14,200.00
  confidence: 0.78
```

#### Permissions

- `listRevenueDemandImpact` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.45 | System shall support revenue impact forecasting for pricing changes. | Unified Operations Dashboard | CONTRACTED | `listRevenueDemandImpact` |
| 8.5.46 | System shall support demand impact forecasting for pricing changes. | Unified Operations Dashboard | CONTRACTED | `listRevenueDemandImpact` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-112` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-112`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 8: Works in Revenue & Demand Impact Forecasting → Provide a dedicated commercial impact assessment before a dynamic-pricing action is approved or executed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-112?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-113` AI Recommendation Review & Decision Queue

**Provide the human decision workspace for recommendations produced by Board 6. This should be the Revenue Manager's inbox.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29756 (VM-ADM-113) |
| Who uses it | venue staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `recommendationId` (navigation) |
| Route | `/commercial/ai-recommendation-review-decision-queue-adm-113` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The revenue manager's inbox of AI pricing recommendations: accept, modify, reject (with a reason), schedule or send for approval; the record keeps who decided what and when.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listRecommendationReviewDecision` ?venue |
| Event | text field | — | — | `listRecommendationReviewDecision` ?event |
| Urgency | radio group | — | Low · Medium · High · Critical | `listRecommendationReviewDecision` ?urgency |
| Decision | select | — | Pending · Accepted · Rejected · Modified · Scheduled · Sent for approval | `listRecommendationReviewDecision` ?decision |
| Governance level | text field | — | — | `listRecommendationReviewDecision` ?governanceLevel |

**Sent by *Accept*** (`decidePricingRecommendation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Accept · Modify · Reject · Schedule · Send for approval | — | — | `decidePricingRecommendation` body |
| Rejection reason `rejectionReason` | select | optional | — | Commercial judgment · Brand positioning · Customer sensitivity · Event strategy · Incorrect signal · Data concern · Other | — | Required for reject. | `decidePricingRecommendation` body |
| Rejection note `rejectionNote` | text area | optional | — | max length 2000 | — | — | `decidePricingRecommendation` body |
| Human selected price `humanSelectedPrice` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Required for modify; must sit inside the strategy's guardrails. | `decidePricingRecommendation` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Required for schedule; in the future. | `decidePricingRecommendation` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rejection reason**: Required on reject from the list (commercial judgment, brand positioning, customer sensitivity, event strategy, incorrect signal, data concern, other with note). *(source: contracts/spine/catalogue.yaml#decidePricingRecommendation / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation review decision** (data table, from `listRecommendationReviewDecision`)

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | Recommendation title |
| Venue | text | Venue |
| Event | text | Event |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Change | 1,234.5 | Change %, percent |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |
| Demand impact | 1,234.5 | Demand Impact, percent |
| Confidence | 1,234.5 | AI Confidence, percent |
| Urgency | chip: Low, Medium, High, Critical | Urgency |
| Governance level | text | Governance Level: approval level required, from the configured approval matrix |

**The selected recommendation review decision** (detail panel): The pack groups this record's detail under its own headings: “Simulation Result”, “Simulation Revenue Uplift”, “Demand Impact”, “AED 265”, “Feedback Loop”, “Human Selected AED 265”.

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | Recommendation title |
| Venue | text | Venue |
| Event | text | Event |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Change | 1,234.5 | Change %, percent |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |
| Demand impact | 1,234.5 | Demand Impact, percent |
| Confidence | 1,234.5 | AI Confidence, percent |
| Urgency | chip: Low, Medium, High, Critical | Urgency |
| Governance level | text | Governance Level: approval level required, from the configured approval matrix |

**Permissions this screen separates** (banner): **The pack separates these permissions; since 29 September the decision buttons are `decidePricingRecommendation` (AI_APPROVE)** — earlier text: Accept, Reject, Modify, Simulate Again, Schedule, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept (primary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | — |
| Modify (secondary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | — |
| Reject (secondary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | — |
| Schedule (secondary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | — |
| Send for approval (secondary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | — |

**Data it reads**: `listRecommendationReviewDecision` (onLoad, AI Recommendation Review & Decision Queue)

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `listRecommendationReviewDecision`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation review decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation review decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation review decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation review decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired (`recommendationExpired`).; 422 `rejectionReasonRequired`, `humanSelectedPriceRequired`, `guardrailBreached` or `scheduledForInPast`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
- recommendation: Balcony +8% Desert Symphony
  impact: +AED 22,000.00
  confidence: 0.77
  age: 2 h
```

#### Permissions

- `listRecommendationReviewDecision` → `PRODUCT_VIEW` (read) · staff
- `decidePricingRecommendation` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-113` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-113`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 10: Works in AI Recommendation Review & Decision Queue → Provide the human decision workspace for recommendations produced by Board 6. This should be the Revenue Manager's inbox.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-113?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept, Modify, Reject, Schedule, Send for approval.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-114` Automation Policy & Autonomous Pricing Orchestrator

**Control when TICVAI is allowed to execute pricing changes automatically. Board 5 defines the strategy-level automation permission. This screen manages operational autonomous execution at scale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29747 (VM-ADM-114) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/automation-policy-autonomous-pricing-orchestrator-adm-114` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When the engine may execute pricing changes on its own at scale: automation level per scope, authority tiers, circuit breakers, no-change windows. Strategy-level permission is set on ADM-096.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Strategy | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Date/Time | select field | — | — | — | — | — | — |
| Evaluation Frequency | select field | — | — | — | — | — | — |
| Execution Frequency | select field | — | — | — | — | — | — |
| Minimum Time Between Changes | text field | — | — | — | — | — | — |
| Maximum Changes per Day | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAutomationPolicyAutonomous` ?venue |
| Automation level | radio group | — | Advisory · Human in the loop · Conditional autonomous · Autonomous | `listAutomationPolicyAutonomous` ?automationLevel |
| Strategy | text field | — | — | `listAutomationPolicyAutonomous` ?strategy |
| Paused | toggle | — | — | `listAutomationPolicyAutonomous` ?paused |

**Form: Save dynamic pricing guardrail policy** (modal, opened by *Save dynamic pricing guardrail policy*; *Save dynamic pricing guardrail policy* calls `setDynamicPricingGuardrailPolicy`, *Cancel* sends nothing)

**Collects what `setDynamicPricingGuardrailPolicy` sends before it is called.** Required: `scopeLevel`, `automationLevel`. Optional: `scopeId`, `absoluteMinimumPrice`, `absoluteMaximumPrice`, `minimumMarginPercent`, `maximumUpliftPercent`, `maximumReductionPercent`, `maximumSingleChangePercent`, `maximumDailyChangePercent`, `maximumWeeklyChangePercent`, `minimumChangeIntervalMinutes`, `maximumChangesPerDay`, `minimumInventory` and 21 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope level `scopeLevel` | select | required | — | Global · Market · Venue · Strategy · Product · Event · Performance · Channel | — | — | `setDynamicPricingGuardrailPolicy` body |
| Scope `scopeId` | picker: choose a scope | optional | — | — | shows names, sends the id | Null at `global`. | `setDynamicPricingGuardrailPolicy` body |
| Absolute minimum price `absoluteMinimumPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setDynamicPricingGuardrailPolicy` body |
| Absolute maximum price `absoluteMaximumPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setDynamicPricingGuardrailPolicy` body |
| Minimum margin percent `minimumMarginPercent` | number field | optional | — | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum uplift percent `maximumUpliftPercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum reduction percent `maximumReductionPercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum single change percent `maximumSingleChangePercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum daily change percent `maximumDailyChangePercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum weekly change percent `maximumWeeklyChangePercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Minimum change interval minutes `minimumChangeIntervalMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum changes per day `maximumChangesPerDay` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Minimum inventory `minimumInventory` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Maximum occupancy trigger percent `maximumOccupancyTriggerPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Protected rate types `protectedRateTypes` | multi-select chips | optional | — | Contract rates · Membership rates · Corporate rates · Promotional locked rates · Regulatory prices · Complimentary rates | — | — | `setDynamicPricingGuardrailPolicy` body |
| Is frozen `isFrozen` | toggle | optional | off | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Is kill switch active `isKillSwitchActive` | toggle | optional | off | — | — | Stops every automatic change in scope at once. | `setDynamicPricingGuardrailPolicy` body |
| Automation level `automationLevel` | radio group | required | Advisory | Advisory · Human in the loop · Conditional autonomous · Autonomous | — | — | `setDynamicPricingGuardrailPolicy` body |
| Authority tiers `authorityTiers` | key and value settings | optional | — | — | — | `[{maxAdjustmentPercent, action, confidenceThreshold}]`. | `setDynamicPricingGuardrailPolicy` body |
| Max adjustment percent `maxAdjustmentPercent` | number field | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Min AI confidence `minAiConfidence` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Min revenue uplift percent `minRevenueUpliftPercent` | number field | optional | — | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Evaluation frequency minutes `evaluationFrequencyMinutes` | number field (minutes) | optional | — | min 1 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Execution frequency minutes `executionFrequencyMinutes` | number field (minutes) | optional | — | min 1 | — | — | `setDynamicPricingGuardrailPolicy` body |
| Quiet period minutes `quietPeriodMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setDynamicPricingGuardrailPolicy` body |
| No change windows `noChangeWindows` | key and value settings | optional | — | — | — | `[{anchor, minutesBefore, minutesAfter, clockFrom, clockTo}]`. | `setDynamicPricingGuardrailPolicy` body |
| Circuit breakers `circuitBreakers` | key and value settings | optional | — | — | — | `[{trigger, threshold, enabled, tripped}]`. | `setDynamicPricingGuardrailPolicy` body |
| Require guardrails passed `requireGuardrailsPassed` | toggle | optional | on | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Exclude protected rates `excludeProtectedRates` | toggle | optional | on | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Require healthy forecast data `requireHealthyForecastData` | toggle | optional | on | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Safe failure behavior `safeFailureBehavior` | radio group | optional | Hold last price | Hold last price · Return to base · Freeze · Request review | — | — | `setDynamicPricingGuardrailPolicy` body |
| Active override `activeOverride` | key and value settings | optional | — | — | — | `{user, reason, overridePrice, start, expiry, returnBehavior}`. | `setDynamicPricingGuardrailPolicy` body |
| Is paused `isPaused` | toggle | optional | off | — | — | — | `setDynamicPricingGuardrailPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDynamicPricingGuardrailPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDynamicPricingGuardrailPolicy` body |

Errors to draw in the form: 422 `invalidRange` or `scopeIdRequired`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save dynamic pricing guardrail policy (primary button) | `setDynamicPricingGuardrailPolicy` PUT `/dynamic-pricing-controls` | DynamicPricingControl | DynamicPricingControl | 422 `invalidRange` or `scopeIdRequired`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listAutomationPolicyAutonomous` (onLoad, Automation Policy & Autonomous Pricing Orchestrator)

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `listAutomationPolicyAutonomous`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automation policy autonomous configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automation policy autonomous untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automation policy autonomous configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `invalidRange` or `scopeIdRequired`. |

#### Consistency with other screens

- Match `ADM-095`: Same record (setDynamicPricingGuardrailPolicy); keep one form with tabs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  scope: Coastal Aqua
  automation: conditionalAutonomous
  circuitBreaker: 3 changes in 1 h trips
  noChange: 2 h before opening
```

#### Permissions

- `listAutomationPolicyAutonomous` → `PRODUCT_VIEW` (read) · staff
- `setDynamicPricingGuardrailPolicy` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.19 | System shall support pricing thresholds. | Unified Operations Dashboard | CONTRACTED | `setDynamicPricingGuardrailPolicy` |
| 8.5.20 | System shall support minimum pricing rules. | Unified Operations Dashboard | CONTRACTED | `setDynamicPricingGuardrailPolicy` |
| 8.5.21 | System shall support maximum pricing rules. | Unified Operations Dashboard | CONTRACTED | `setDynamicPricingGuardrailPolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-114` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-114`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 12: Works in Automation Policy & Autonomous Pricing Orchestrator → Control when TICVAI is allowed to execute pricing changes automatically. Board 5 defines the strategy-level automation permission. This screen manages operational autonomous execution at scale.

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-114?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save dynamic pricing guardrail policy.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-115` Live Dynamic Price Execution & Deployment Monitor

**Monitor pricing actions as they are executed across TICVAI's selling ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29748 (VM-ADM-115) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each execution shows) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/live-dynamic-price-execution-deployment-monitor-adm-115` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Retry, Hold, Revert, Escalate, Freeze Channel. Each needs an operation, or needs removing from the screen … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read lists live dynamic price executions and their deployment state.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Dynamic price changes as they are executed across channels: what changed, from what source (manual, human approved, scheduled, autonomous), and whether every channel received it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The monitor's only operation creates a live price (createLiveDynamicPrice) and there is no read of executions. (CHG-WIR-027)
- No read operation: the screen declares only createLiveDynamicPrice and nothing that returns the current configuration. (CHG-MOV-008)
- Pack actions with no operation: Retry, Hold, Revert, Escalate, Freeze Channel. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every live dynamic price** (data table, from `createLiveDynamicPrice`)

| Shows | Format | Notes |
|---|---|---|
| Timestamp | 1 Oct 2026, 14:30 | Timestamp |
| Product | text | Product id |
| Event | text | Event id |
| Previous price | AED 1,234.50 | Previous Price |
| New price | AED 1,234.50 | New Price |
| Trigger | text | not in the schema: `Trigger` |
| Strategy | text | Strategy id |
| AI recommendation | text | Recommendation id the change came from |
| Approval | text | Approval reference; empty only for policy-permitted automatic execution |
| Execution source | chip: Manual, Human approved, Scheduled, Conditional autonomous, Autonomous | Execution Source |
| Status | text | Status: queued, processing, live, partial, failed or rolledBack |

**The selected live dynamic price** (detail panel): The pack groups this record's detail under its own headings: “Dubai Indoor Attraction”, “Trigger”, “Monitor propagation to”, “Alert”, “Display every live movement”, “Board 4 Integration”.

| Shows | Format | Notes |
|---|---|---|
| Timestamp | 1 Oct 2026, 14:30 | Timestamp |
| Product | text | Product id |
| Event | text | Event id |
| Previous price | AED 1,234.50 | Previous Price |
| New price | AED 1,234.50 | New Price |
| Trigger | text | not in the schema: `Trigger` |
| Strategy | text | Strategy id |
| AI recommendation | text | Recommendation id the change came from |
| Approval | text | Approval reference; empty only for policy-permitted automatic execution |
| Execution source | chip: Manual, Human approved, Scheduled, Conditional autonomous, Autonomous | Execution Source |
| Status | text | Status: queued, processing, live, partial, failed or rolledBack |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Hold (secondary button) | navigation or local | — | — | — | — |
| Revert (secondary button) | navigation or local | — | — | — | — |
| Escalate (secondary button) | navigation or local | — | — | — | — |
| Freeze Channel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **execution log**: Time, product, old and new price, source, approval, channels delivered. *(source: contracts/spine/catalogue.yaml#createLiveDynamicPrice)*

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `createLiveDynamicPrice`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live dynamic price list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live dynamic price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live dynamic price yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live dynamic price are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
execution:
  at: '14:05'
  product: Day Pass Adult
  from: AED 295.00
  to: AED 309.00
  executedBy: conditionalAutonomous
  delivered: Website, App
```

#### Permissions

- `createLiveDynamicPrice` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-115` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-115`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 14: Works in Live Dynamic Price Execution & Deployment Monitor → Monitor pricing actions as they are executed across TICVAI's selling ecosystem.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-115?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Hold, Revert, Escalate, Freeze Channel.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-116` Dynamic Pricing Performance & Optimization Analytics

**Determine whether dynamic pricing actually improves TICVAI's commercial performance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29768 (VM-ADM-116) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Measure) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-pricing-performance-optimization-analytics-adm-116` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Strategy vs Strategy, Venue vs Venue, Event vs Event, Channel vs Channel. Each needs an operation, or needs …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether dynamic pricing actually improves results: revenue, yield and occupancy against a baseline and control.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Strategy vs Strategy, Venue vs Venue, Event vs Event, Channel vs Channel. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Level | select | — | Market · Venue · Event · Performance · Product · Price category · Channel | `listDynamicPricingPerformance` ?level |
| Market | text field | — | — | `listDynamicPricingPerformance` ?market |
| Venue | text field | — | — | `listDynamicPricingPerformance` ?venue |
| Event | text field | — | — | `listDynamicPricingPerformance` ?event |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDynamicPricingPerformance` ?channel |
| Compare by | select | — | Dynamic vs fixed · AI vs rules · AI vs human · Strategy vs strategy · Venue vs venue · Event vs event · Channel vs channel · Current vs previous period | `listDynamicPricingPerformance` ?compareBy |
| Date from | date picker | — | — | `listDynamicPricingPerformance` ?dateFrom |
| Date to | date picker | — | — | `listDynamicPricingPerformance` ?dateTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every dynamic pricing performance** (data table, from `listDynamicPricingPerformance`)

| Shows | Format | Notes |
|---|---|---|
| Incremental revenue | AED 1,234.50 | Incremental Revenue |
| Revenue uplift | 1,234.5 | Revenue Uplift, percent |
| Margin uplift | 1,234.5 | Margin Uplift, percent |
| Average selling price | AED 1,234.50 | Average Selling Price |
| Conversion | 1,234.5 | Conversion, percent |
| Attendance | 1,234 | Attendance |
| Occupancy | 1,234.5 | Occupancy, percent |
| Sell through | 1,234.5 | Sell-Through, percent |
| Revenue per available capacity | AED 1,234.50 | Revenue per Available Capacity |
| Number of price changes | 1,234 | Number of Price Changes |
| Strategy roi | 1,234.5 | Strategy ROI, percent |
| Recommendations generated | 1,234 | Recommendations Generated |
| Accepted | 1,234 | Accepted |
| Rejected | 1,234 | Rejected |
| Modified | 1,234 | Modified |
| Auto executed | 1,234 | Auto-Executed |
| Successful | 1,234 | Successful |
| Negative outcome | 1,234 | Negative Outcome |

**The selected dynamic pricing performance** (detail panel): The pack groups this record's detail under its own headings: “Revenue”, “ASP”, “Conversion”, “Attendance”, “Margin”, “Price”.

| Shows | Format | Notes |
|---|---|---|
| Incremental revenue | AED 1,234.50 | Incremental Revenue |
| Revenue uplift | 1,234.5 | Revenue Uplift, percent |
| Margin uplift | 1,234.5 | Margin Uplift, percent |
| Average selling price | AED 1,234.50 | Average Selling Price |
| Conversion | 1,234.5 | Conversion, percent |
| Attendance | 1,234 | Attendance |
| Occupancy | 1,234.5 | Occupancy, percent |
| Sell through | 1,234.5 | Sell-Through, percent |
| Revenue per available capacity | AED 1,234.50 | Revenue per Available Capacity |
| Number of price changes | 1,234 | Number of Price Changes |
| Strategy roi | 1,234.5 | Strategy ROI, percent |
| Recommendations generated | 1,234 | Recommendations Generated |
| Accepted | 1,234 | Accepted |
| Rejected | 1,234 | Rejected |
| Modified | 1,234 | Modified |
| Auto executed | 1,234 | Auto-Executed |
| Successful | 1,234 | Successful |
| Negative outcome | 1,234 | Negative Outcome |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Strategy vs Strategy (primary button) | navigation or local | — | — | — | — |
| Venue vs Venue (secondary button) | navigation or local | — | — | — | — |
| Event vs Event (secondary button) | navigation or local | — | — | — | — |
| Channel vs Channel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **performance**: Uplift vs baseline with significance. *(source: contracts/spine/catalogue.yaml#listDynamicPricingPerformance)*

**Data it reads**: `listDynamicPricingPerformance` (onLoad, Dynamic Pricing Performance & Optimization Analytics)

**Where the user goes next**

- → `ADM-108` Revenue Optimization Command Center: *Returns to the board's landing screen*; calls `listDynamicPricingPerformance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic pricing performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  period: October 2026
  uplift: +3.4% revenue
  occupancy: -0.6 pts
```

#### Permissions

- `listDynamicPricingPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.27 | System shall provide pricing analytics dashboards. | Unified Operations Dashboard | CONTRACTED | `listDynamicPricingPerformance` |
| 8.5.28 | System shall provide pricing performance reporting. | Unified Operations Dashboard | CONTRACTED | `listDynamicPricingPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-116` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-116`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 16: Works in Dynamic Pricing Performance & Optimization Analytics → Determine whether dynamic pricing actually improves TICVAI's commercial performance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-116?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Strategy vs Strategy, Venue vs Venue, Event vs Event, Channel vs Channel.
- [ ] Every transition is wired: `ADM-108`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-117` AI Learning, Model Performance & Optimization Feedback

**Close the intelligence loop by comparing AI predictions and recommendations with actual commercial outcomes. This is what allows the system to improve over time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29757 (VM-ADM-117) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast; Track; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-learning-model-performance-optimization-feedback-adm-117` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI predictions and recommendations compared with outcomes, per model, and the trust level of each model.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Model name | text field | — | — | `listLearningModelPerformance` ?modelName |
| Venue | text field | — | — | `listLearningModelPerformance` ?venue |
| Product | text field | — | — | `listLearningModelPerformance` ?product |
| Event type | text field | — | — | `listLearningModelPerformance` ?eventType |
| Season | text field | — | — | `listLearningModelPerformance` ?season |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listLearningModelPerformance` ?channel |
| Market | text field | — | — | `listLearningModelPerformance` ?market |
| Forecast horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listLearningModelPerformance` ?forecastHorizon |

**Form: Save signal registry policy** (modal, opened by *Save signal registry policy*; *Save signal registry policy* calls `setSignalRegistryPolicy`, *Cancel* sends nothing)

**Collects what `setSignalRegistryPolicy` sends before it is called.** Required: `registryKind`, `name`, `trustLevel`. Optional: `category`, `provider`, `source`, `internalExternal`, `marketCode`, `refreshFrequency`, `aiUsePermissions`, `fallbackPolicy`, `status`, `ownerPrincipalId`, `purpose`, `deployedAt` and 5 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Registry kind `registryKind` | segmented control | required | — | Signal · Model | — | — | `setSignalRegistryPolicy` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setSignalRegistryPolicy` body |
| Category `category` | select | optional | — | Internal sales · Inventory · Weather · Nearby events · Competitor · Tourism · Calendar · Transport · Market · Other | — | — | `setSignalRegistryPolicy` body |
| Provider `provider` | text field | optional | — | max length 100 | — | — | `setSignalRegistryPolicy` body |
| Source `source` | text field | optional | — | max length 100 | — | — | `setSignalRegistryPolicy` body |
| Internal external `internalExternal` | segmented control | optional | — | Internal · External | — | — | `setSignalRegistryPolicy` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setSignalRegistryPolicy` body |
| Refresh frequency `refreshFrequency` | select | optional | — | Real time · Minutes10 · Hourly · Daily · Weekly · Manual | — | — | `setSignalRegistryPolicy` body |
| Trust level `trustLevel` | radio group | required | Experimental | Approved · Experimental · Advisory only · Blocked | — | — | `setSignalRegistryPolicy` body |
| AI use permissions `aiUsePermissions` | multi-select chips | optional | — | Forecasting · Recommendations · Simulation · Automated pricing | — | — | `setSignalRegistryPolicy` body |
| Fallback policy `fallbackPolicy` | radio group | optional | — | Use historical value · Ignore · Substitute · Reduce confidence · Stop AI recommendation | — | — | `setSignalRegistryPolicy` body |
| Status `status` | text field | optional | — | max length 40 | — | — | `setSignalRegistryPolicy` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setSignalRegistryPolicy` body |
| Version `version` | text field | optional | — | max length 40 | — | Models. | `setSignalRegistryPolicy` body |
| Purpose `purpose` | text field | optional | — | — | — | — | `setSignalRegistryPolicy` body |
| Deployed at `deployedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setSignalRegistryPolicy` body |
| Training window `trainingWindow` | text field | optional | — | max length 60 | — | — | `setSignalRegistryPolicy` body |
| Validation result `validationResult` | text field | optional | — | — | — | — | `setSignalRegistryPolicy` body |

Errors to draw in the form: 422 `trustTooLow`.

#### Outputs: what the screen shows and produces

**Shown**

**Every learning model performance** (data table, from `listLearningModelPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Demand forecast accuracy | 1,234.5 | Demand Forecast Accuracy, percent |
| Revenue forecast accuracy | 1,234.5 | Revenue Forecast Accuracy, percent |
| Elasticity accuracy | 1,234.5 | Elasticity Accuracy, percent |
| Recommendation success | 1,234.5 | Recommendation Success, percent |
| Confidence calibration | 1,234.5 | Confidence Calibration: how closely stated confidence matched realised accuracy, percent |
| False positive rate | 12.5% | False Positive Rate, percent |
| Revenue uplift | 1,234.5 | Revenue Uplift, percent |

**The selected learning model performance** (detail panel): The pack groups this record's detail under its own headings: “Situation”, “Signals”, “Human/Automation Decision”, “Actual Price”, “Actual Demand”, “Actual Revenue”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Demand forecast accuracy | 1,234.5 | Demand Forecast Accuracy, percent |
| Revenue forecast accuracy | 1,234.5 | Revenue Forecast Accuracy, percent |
| Elasticity accuracy | 1,234.5 | Elasticity Accuracy, percent |
| Recommendation success | 1,234.5 | Recommendation Success, percent |
| Confidence calibration | 1,234.5 | Confidence Calibration: how closely stated confidence matched realised accuracy, percent |
| False positive rate | 12.5% | False Positive Rate, percent |
| Revenue uplift | 1,234.5 | Revenue Uplift, percent |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save signal registry policy (primary button) | `setSignalRegistryPolicy` PUT `/signal-registry` | SignalRegistryEntry | SignalRegistryEntry | 422 `trustTooLow`. | gated `AI_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **model performance**: Error, accuracy and drift per model; low performers flagged with a link to set trust lower. *(source: contracts/spine/catalogue.yaml#listLearningModelPerformance / contracts/spine/catalogue.yaml#setSignalRegistryPolicy)*

**Data it reads**: `listLearningModelPerformance` (onLoad, AI Learning, Model Performance & Optimization Feedback)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The learning model performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the learning model performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No learning model performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the learning model performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `trustTooLow`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
model:
  name: Demand forecast v3
  mape: 9.1%
  trust: approved
```

#### Permissions

- `listLearningModelPerformance` → `PRODUCT_VIEW` (read) · staff
- `setSignalRegistryPolicy` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-117` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-117`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 7
- Flow F149 *Pricing Revenue Management board 7: Revenue Optimization Command Center*, step 18: Works in AI Learning, Model Performance & Optimization Feedback → Close the intelligence loop by comparing AI predictions and recommendations with actual commercial outcomes. This is what allows the system to improve over time.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-117?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save signal registry policy.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `PRODUCT_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createLiveDynamicPrice": {"method":"POST","path":"/live-dynamic-price","contract":"catalogue","summary":"Live Dynamic Price Execution & Deployment Monitor","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LiveDynamicPriceExecutionDeploymentMonitorInput","responds":"LiveDynamicPriceExecutionDeploymentMonitorView"},
"decidePricingRecommendation": {"method":"POST","path":"/recommendation-review-decision/{recommendationId}/decision","contract":"catalogue","summary":"Record a human decision on an AI pricing recommendation","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingRecommendationDecisionInput","responds":"PricingRecommendationDecision"},
"listAutomationPolicyAutonomous": {"method":"GET","path":"/automation-policy-autonomou","contract":"catalogue","summary":"Automation Policy & Autonomous Pricing Orchestrator","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"automationLevel","in":"query","required":false},{"name":"strategy","in":"query","required":false},{"name":"paused","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPricingPerformance": {"method":"GET","path":"/dynamic-pricing-performance","contract":"catalogue","summary":"Dynamic Pricing Performance & Optimization Analytics","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"level","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"compareBy","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLearningModelPerformance": {"method":"GET","path":"/learning-model-performance","contract":"catalogue","summary":"AI Learning, Model Performance & Optimization Feedback","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"modelName","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"eventType","in":"query","required":false},{"name":"season","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"forecastHorizon","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecommendationReviewDecision": {"method":"GET","path":"/recommendation-review-decision","contract":"catalogue","summary":"AI Recommendation Review & Decision Queue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"urgency","in":"query","required":false},{"name":"decision","in":"query","required":false},{"name":"governanceLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRevenue": {"method":"GET","path":"/revenue","contract":"catalogue","summary":"Revenue Optimization Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"automationMode","in":"query","required":false},{"name":"urgency","in":"query","required":false},{"name":"rankBy","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRevenueDemandImpact": {"method":"GET","path":"/revenue-demand-impact","contract":"catalogue","summary":"Revenue & Demand Impact Forecasting","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"recommendationId","in":"query","required":false},{"name":"simulationId","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScenarioModelingWhat": {"method":"GET","path":"/scenario-modeling-what","contract":"catalogue","summary":"Scenario Modeling & What-If Analysis","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scenarioType","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setDynamicPricingGuardrailPolicy": {"method":"PUT","path":"/dynamic-pricing-controls","contract":"catalogue","summary":"Set the guardrails and automation level of dynamic pricing at one scope","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicPricingControl","responds":"DynamicPricingControl"},
"setPricing": {"method":"PUT","path":"/pricing-2","contract":"catalogue","summary":"Pricing Simulation Studio","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingSimulationStudioInput","responds":"PricingSimulationStudioView"},
"setPricingExperiment": {"method":"PUT","path":"/pricing-experiment","contract":"catalogue","summary":"A/B Pricing Experiment Studio","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ABPricingExperimentStudioInput","responds":"ABPricingExperimentStudioView"},
"setSignalRegistryPolicy": {"method":"PUT","path":"/signal-registry","contract":"catalogue","summary":"Register a signal or model and set how far AI may trust it","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SignalRegistryEntry","responds":"SignalRegistryEntry"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ABPricingExperimentStudioInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 5%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What A/B Pricing Experiment Studio submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"experimentName":{"type":"string","description":"Experiment Name"},"objective":{"type":"string","description":"Objective"},"product":{"type":"string","description":"Product id"},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"customerSegment":{"type":"string","description":"Customer segment","nullable":true},"startDate":{"type":"string","description":"Start Date","format":"date"},"endDate":{"type":"string","description":"End Date","format":"date"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum Price no variant may go below"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum Price no variant may exceed"},"variants":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string","description":"Variant label (A = control)"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Variant price"},"trafficSharePercent":{"type":"number","description":"Share of traffic, percent; variants sum to 100"}}},"description":"Variant Configuration: control plus 1-3 variants (decided 29 September, readiness close-out)"},"successMetrics":{"type":"array","items":{"type":"string","enum":["revenue","conversion","averageSellingPrice","margin","sellThrough","occupancy","revenuePerVisitor"]},"description":"Success Metrics"},"targetConfidenceLevel":{"type":"number","description":"Target confidence level, percent; default 95 (decided 29 September, readiness close-out)"}}},
"ABPricingExperimentStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What A/B Pricing Experiment Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"experimentName":{"type":"string","description":"Experiment Name"},"objective":{"type":"string","description":"Objective"},"product":{"type":"string","description":"Product id"},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"customerSegment":{"type":"string","description":"Customer segment","nullable":true},"startDate":{"type":"string","description":"Start Date","format":"date"},"endDate":{"type":"string","description":"End Date","format":"date"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum Price no variant may go below"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum Price no variant may exceed"},"sampleSize":{"type":"integer","description":"Sample Size reached"},"confidenceLevel":{"type":"number","description":"Target Confidence Level; default 95 (decided 29 September, readiness close-out), percent"},"experimentDuration":{"type":"integer","description":"Experiment Duration, days"},"statisticalSignificance":{"type":"boolean","description":"Statistical Significance reached at the target confidence level"},"experimentId":{"type":"string","description":"Experiment id"},"variants":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string","description":"Variant label (A = control)"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Variant price"},"trafficSharePercent":{"type":"number","description":"Share of traffic, percent; variants sum to 100"}}},"description":"Variant Configuration: control plus 1-3 variants (decided 29 September, readiness close-out)"},"successMetrics":{"type":"array","items":{"type":"string","enum":["revenue","conversion","averageSellingPrice","margin","sellThrough","occupancy","revenuePerVisitor"]},"description":"Success Metrics"},"guardrailChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["minimumPrice","maximumPrice","contractRates","membershipRates","regulatoryRequirements"],"description":"Guardrail"},"passed":{"type":"boolean","description":"Pass / fail"}}},"description":"Guardrails the experiment must respect"},"variantResults":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string","description":"Variant"},"revenueChangePercent":{"type":"number","description":"Revenue change vs control, percent"},"conversionChangePercent":{"type":"number","description":"Conversion change vs control, percent"},"aspChangePercent":{"type":"number","description":"ASP change vs control, percent"},"confidence":{"type":"number","description":"Statistical confidence, percent"}}},"description":"Results per variant"},"recommendedWinner":{"type":"string","description":"Statistically preferred variant label, advisory","nullable":true},"experimentStage":{"type":"string","description":"Stage: draft, pendingApproval, running, completed or stopped (decided 29 September, readiness close-out)"}}},
"AiLearningModelPerformanceOptimizationFeedbackView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Learning, Model Performance & Optimization Feedback displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"forecastError":{"type":"number","description":"Mean forecast error (actual vs forecast demand), percent"},"demandForecastAccuracy":{"type":"number","description":"Demand Forecast Accuracy, percent"},"revenueForecastAccuracy":{"type":"number","description":"Revenue Forecast Accuracy, percent"},"elasticityAccuracy":{"type":"number","description":"Elasticity Accuracy, percent"},"recommendationSuccess":{"type":"number","description":"Recommendation Success, percent"},"confidenceCalibration":{"type":"number","description":"Confidence Calibration: how closely stated confidence matched realised accuracy, percent"},"falsePositiveRate":{"type":"number","description":"False Positive Rate, percent"},"revenueUplift":{"type":"number","description":"Revenue Uplift, percent"},"venue":{"type":"string","description":"Venue","nullable":true},"product":{"type":"string","description":"Product","nullable":true},"eventType":{"type":"string","description":"Event type","nullable":true},"season":{"type":"string","description":"Season","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"market":{"type":"string","description":"Market","nullable":true},"forecastHorizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"modelName":{"type":"string","description":"Model name"},"modelVersion":{"type":"string","description":"Model version"},"lifecycleStage":{"type":"string","description":"Model lifecycle: candidate, validation, approved, production, monitored or retired"},"accuracyChange30d":{"type":"number","description":"Model Drift: accuracy change over the last 30 days, percent"},"signalEffectiveness":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal"},"forecastContribution":{"type":"string","enum":["low","medium","high"],"description":"Forecast contribution"},"reliability":{"type":"number","description":"Reliability, percent"}}},"description":"Signal Effectiveness"},"humanOverrideRate":{"type":"number","description":"Share of AI recommendations modified by Revenue Managers, percent"},"overrideOutcomeDelta":{"type":"number","description":"Revenue outcome of overridden vs unmodified recommendations, percent"},"optimizationSuggestions":{"type":"array","items":{"type":"string"},"description":"AI Optimization Recommendations; adopting one requires governance. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"}}},
"AiRecommendationReviewDecisionQueueView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Recommendation Review & Decision Queue displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"recommendation":{"type":"string","description":"Recommendation title"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended Price"},"change":{"type":"number","description":"Change %, percent"},"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"demandImpact":{"type":"number","description":"Demand Impact, percent"},"confidence":{"type":"number","description":"AI Confidence, percent"},"urgency":{"type":"string","description":"Urgency","enum":["low","medium","high","critical"]},"governanceLevel":{"type":"string","description":"Governance Level: approval level required, from the configured approval matrix"},"simulationRevenueUplift":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Simulation Revenue Uplift (Board 7)"},"recommendationId":{"type":"string","description":"Recommendation id"},"drivers":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category behind the driver"},"direction":{"type":"string","enum":["up","down"],"description":"Whether the driver pushes the price up or down"},"explanation":{"type":"string","description":"Business-language evidence, e.g. booking velocity 31% above forecast"}}},"description":"Primary drivers of the recommendation (pack's up/down driver list); explanatory, not literal model weights"},"guardrailsPassed":{"type":"boolean","description":"Guardrails passed"},"decision":{"type":"string","description":"Decision: pending, accepted, rejected, modified, scheduled or sentForApproval; every item starts pending"},"rejectionReason":{"type":"string","description":"Rejection Reason","enum":["commercialJudgment","brandPositioning","customerSensitivity","eventStrategy","incorrectSignal","dataConcern","other"],"nullable":true},"rejectionNote":{"type":"string","description":"Free-text note, required when reason is other","nullable":true},"humanSelectedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price the Revenue Manager chose when modifying"},"scheduledFor":{"type":"string","description":"When a scheduled change should execute","format":"date-time","nullable":true},"decidedBy":{"type":"string","description":"User who decided","nullable":true},"decidedAt":{"type":"string","description":"When decided","format":"date-time","nullable":true},"actualRevenueResultPercent":{"type":"number","description":"Feedback Loop: actual revenue result after execution; empty until measured, percent"}}},
"AutomationPolicyAutonomousPricingOrchestratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Automation Policy & Autonomous Pricing Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tenant":{"type":"string","description":"Tenant"},"venue":{"type":"string","description":"Venue","nullable":true},"product":{"type":"string","description":"Product","nullable":true},"event":{"type":"string","description":"Event","nullable":true},"strategy":{"type":"string","description":"Dynamic pricing strategy (Board 5)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"market":{"type":"string","description":"Market","nullable":true},"effectiveFrom":{"type":"string","description":"Effective from","format":"date-time"},"evaluationFrequency":{"type":"integer","description":"Evaluation Frequency, minutes; default 60 (decided 29 September, readiness close-out)"},"executionFrequency":{"type":"integer","description":"Execution Frequency, minutes; default 240 (decided 29 September, readiness close-out)"},"minimumTimeBetweenChanges":{"type":"integer","description":"Minimum Time Between Changes, minutes; default 240 (decided 29 September, readiness close-out)"},"maximumChangesPerDay":{"type":"integer","description":"Maximum Changes per Day; default 3 (decided 29 September, readiness close-out)"},"requireGuardrailsPassed":{"type":"boolean","description":"Auto-execute only if guardrails passed; always true, cannot be switched off"},"excludeProtectedRates":{"type":"boolean","description":"Auto-execute only if no protected (contract/member) rate is affected; default true (decided 29 September, readiness close-out)"},"requireHealthyForecastData":{"type":"boolean","description":"Auto-execute only if forecast data is healthy; default true (decided 29 September, readiness close-out)"},"policyId":{"type":"string","description":"Policy id"},"effectiveTo":{"type":"string","description":"Effective to","format":"date-time","nullable":true},"automationLevel":{"type":"string","description":"Automation Level; default advisory (decided 29 September, readiness close-out)","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"]},"maxAdjustmentPercent":{"type":"number","description":"Auto-execute only if adjustment is at or below this, percent; default 5 (decided 29 September, readiness close-out)"},"minAiConfidence":{"type":"number","description":"Auto-execute only if AI confidence is at or above this, percent; default 90 (decided 29 September, readiness close-out)"},"minRevenueUpliftPercent":{"type":"number","description":"Auto-execute only if expected uplift is at or above this, percent; default 2 (decided 29 September, readiness close-out)"},"quietPeriodMinutes":{"type":"integer","description":"Quiet Period: no automated change within this many minutes of event start; default 60 (decided 29 September, readiness close-out)"},"circuitBreakers":{"type":"array","items":{"type":"object","properties":{"trigger":{"type":"string","enum":["dataQualityFalls","modelConfidenceDrops","conversionDropsAbnormally","priceVolatilityExceedsThreshold","revenueFalls","integrationFails"],"description":"Circuit breaker"},"threshold":{"type":"number","description":"Trigger threshold, in the trigger's unit"},"enabled":{"type":"boolean","description":"Enabled; all enabled by default"},"tripped":{"type":"boolean","description":"Currently tripped"}}},"description":"Circuit Breakers (decided 29 September, readiness close-out)"},"paused":{"type":"boolean","description":"Paused by PAUSE ALL AUTONOMOUS PRICING or a tripped breaker"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"DynamicPricingControl": {"type":"object","x-ticvai-persistence":"catalogue.dynamic_pricing_control","description":"**The limits and the autonomy of dynamic pricing at one scope** (29 September, data model DM3). Merges guardrails (ADM-093) and automation policy (ADM-094, ADM-113): both are per-scope controls a price change must pass, and they share the rate-of-change limits. The most specific scope wins; guardrails are re-checked at execution (`createLiveDynamicPrice`). `automationLevel` is the one vocabulary: the strategy screen's `monitor`/`recommend` read as `advisory`, `prepareChange` as `humanInTheLoop`, `autoExecuteWithinGuardrails` as `conditionalAutonomous`.","required":["id","scopePath","scopeLevel","automationLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"scopeLevel":{"type":"string","enum":["global","market","venue","strategy","product","event","performance","channel"]},"scopeId":{"type":"string","format":"uuid","nullable":true,"description":"Null at `global`."},"absoluteMinimumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"absoluteMaximumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"minimumMarginPercent":{"type":"number","nullable":true},"maximumUpliftPercent":{"type":"number","nullable":true,"minimum":0},"maximumReductionPercent":{"type":"number","nullable":true,"minimum":0},"maximumSingleChangePercent":{"type":"number","nullable":true,"minimum":0},"maximumDailyChangePercent":{"type":"number","nullable":true,"minimum":0},"maximumWeeklyChangePercent":{"type":"number","nullable":true,"minimum":0},"minimumChangeIntervalMinutes":{"type":"integer","nullable":true,"minimum":0},"maximumChangesPerDay":{"type":"integer","nullable":true,"minimum":0},"minimumInventory":{"type":"integer","nullable":true,"minimum":0},"maximumOccupancyTriggerPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100},"protectedRateTypes":{"type":"array","items":{"type":"string","enum":["contractRates","membershipRates","corporateRates","promotionalLockedRates","regulatoryPrices","complimentaryRates"]}},"isFrozen":{"type":"boolean","default":false},"isKillSwitchActive":{"type":"boolean","default":false,"description":"Stops every automatic change in scope at once."},"automationLevel":{"type":"string","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"],"default":"advisory"},"authorityTiers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{maxAdjustmentPercent, action, confidenceThreshold}]`."},"maxAdjustmentPercent":{"type":"number","nullable":true,"minimum":0},"minAiConfidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"minRevenueUpliftPercent":{"type":"number","nullable":true},"evaluationFrequencyMinutes":{"type":"integer","nullable":true,"minimum":1},"executionFrequencyMinutes":{"type":"integer","nullable":true,"minimum":1},"quietPeriodMinutes":{"type":"integer","nullable":true,"minimum":0},"noChangeWindows":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{anchor, minutesBefore, minutesAfter, clockFrom, clockTo}]`."},"circuitBreakers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{trigger, threshold, enabled, tripped}]`."},"requireGuardrailsPassed":{"type":"boolean","default":true},"excludeProtectedRates":{"type":"boolean","default":true},"requireHealthyForecastData":{"type":"boolean","default":true},"safeFailureBehavior":{"type":"string","enum":["holdLastPrice","returnToBase","freeze","requestReview"],"default":"holdLastPrice"},"activeOverride":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{user, reason, overridePrice, start, expiry, returnBehavior}`."},"isPaused":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicPricingPerformanceOptimizationAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Performance & Optimization Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental Revenue"},"revenueUplift":{"type":"number","description":"Revenue Uplift, percent"},"marginUplift":{"type":"number","description":"Margin Uplift, percent"},"averageSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Average Selling Price"},"conversion":{"type":"number","description":"Conversion, percent"},"attendance":{"type":"integer","description":"Attendance"},"occupancy":{"type":"number","description":"Occupancy, percent"},"sellThrough":{"type":"number","description":"Sell-Through, percent"},"revenuePerAvailableCapacity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Available Capacity"},"numberOfPriceChanges":{"type":"integer","description":"Number of Price Changes"},"strategyRoi":{"type":"number","description":"Strategy ROI, percent"},"recommendationsGenerated":{"type":"integer","description":"Recommendations Generated"},"accepted":{"type":"integer","description":"Accepted"},"rejected":{"type":"integer","description":"Rejected"},"modified":{"type":"integer","description":"Modified"},"autoExecuted":{"type":"integer","description":"Auto-Executed"},"successful":{"type":"integer","description":"Successful"},"negativeOutcome":{"type":"integer","description":"Negative Outcome"},"level":{"type":"string","description":"Drilldown level of this row","enum":["market","venue","event","performance","product","priceCategory","channel"]},"key":{"type":"string","description":"Id of the market/venue/event/... at that level"},"label":{"type":"string","description":"Display name"},"comparisonGroup":{"type":"string","description":"Side of the comparison this row is, e.g. dynamic / fixed, AI / rules","nullable":true},"opportunityLost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Opportunity Lost: estimated revenue not captured through rejected recommendations (analytical estimate)"},"priceTimeline":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time","description":"Moment of the price movement"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"demand":{"type":"integer","description":"Demand"},"occupancy":{"type":"number","description":"Occupancy, percent"},"conversion":{"type":"number","description":"Conversion, percent"},"bookingVelocity":{"type":"number","description":"Booking velocity vs forecast, percent"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"}}},"description":"Price Timeline overlay"}}},
"LiveDynamicPriceExecutionDeploymentMonitorInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Live Dynamic Price Execution & Deployment Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","description":"Product id"},"event":{"type":"string","description":"Event id","nullable":true},"newPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"New Price"},"strategy":{"type":"string","description":"Strategy id","nullable":true},"aiRecommendation":{"type":"string","description":"Recommendation id","nullable":true},"approval":{"type":"string","description":"Approval reference; required unless the automation policy permits automatic execution","nullable":true},"executionSource":{"type":"string","description":"Execution Source","enum":["manual","humanApproved","scheduled","conditionalAutonomous","autonomous"]},"performance":{"type":"string","description":"Performance id","nullable":true},"trigger":{"type":"string","description":"Trigger","nullable":true},"channels":{"type":"array","items":{"type":"string","enum":["b2c","mobileApp","pos","kiosk","callCenter","b2b","reseller","ota","api"]},"description":"Channels to deploy to; default all channels the product is sold on (decided 29 September, readiness close-out)"},"scheduledFor":{"type":"string","description":"Execute at; empty = now","format":"date-time","nullable":true}}},
"LiveDynamicPriceExecutionDeploymentMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Live Dynamic Price Execution & Deployment Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"timestamp":{"type":"string","description":"Timestamp","format":"date-time"},"product":{"type":"string","description":"Product id"},"event":{"type":"string","description":"Event id","nullable":true},"previousPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Previous Price"},"newPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"New Price"},"strategy":{"type":"string","description":"Strategy id","nullable":true},"aiRecommendation":{"type":"string","description":"Recommendation id the change came from","nullable":true},"approval":{"type":"string","description":"Approval reference; empty only for policy-permitted automatic execution","nullable":true},"executionSource":{"type":"string","description":"Execution Source","enum":["manual","humanApproved","scheduled","conditionalAutonomous","autonomous"]},"status":{"type":"string","description":"Status: queued, processing, live, partial, failed or rolledBack"},"executionId":{"type":"string","description":"Execution id"},"trigger":{"type":"string","description":"Trigger, e.g. booking velocity + occupancy","nullable":true},"aiConfidence":{"type":"number","description":"AI confidence at execution, percent"},"channelDeployments":{"type":"array","items":{"type":"object","properties":{"channel":{"type":"string","enum":["b2c","mobileApp","pos","kiosk","callCenter","b2b","reseller","ota","api"],"description":"Channel"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price live on the channel"},"consistent":{"type":"boolean","description":"Channel shows the new price"},"deploymentStatus":{"type":"string","description":"queued, processing, live, failed or rolledBack"}}},"description":"Channel Deployment"},"priceInconsistency":{"type":"boolean","description":"Price inconsistency detected across channels"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PricingRecommendationDecision": {"type":"object","x-ticvai-persistence":"catalogue.pricing_recommendation_decision","description":"**One human decision on one AI pricing recommendation** (decided 29 September, readiness close-out). New table: the queue row `AiRecommendationReviewDecisionQueueView` reads its decision fields from here. Written once by `decidePricingRecommendation` and never edited; a changed mind is a new recommendation.\n","required":["id","recommendationId","decision","decidedByPrincipalId","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"recommendationId":{"type":"string","format":"uuid","description":"A `catalogue.pricing_recommendation` (29 September, data model DM3)."},"decision":{"type":"string","enum":["accept","modify","reject","schedule","sendForApproval"]},"rejectionReason":{"type":"string","nullable":true,"enum":["commercialJudgment","brandPositioning","customerSensitivity","eventStrategy","incorrectSignal","dataConcern","other",null]},"rejectionNote":{"type":"string","nullable":true},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"humanSelectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The approvals request opened by `sendForApproval`."},"executionId":{"type":"string","nullable":true,"readOnly":true,"description":"The `createLiveDynamicPrice` execution that carried it out, once it has."},"decidedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"decidedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"PricingRecommendationDecisionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `decidePricingRecommendation` takes (decided 29 September, readiness close-out).","required":["decision"],"properties":{"decision":{"type":"string","enum":["accept","modify","reject","schedule","sendForApproval"]},"rejectionReason":{"type":"string","enum":["commercialJudgment","brandPositioning","customerSensitivity","eventStrategy","incorrectSignal","dataConcern","other"],"description":"Required for reject."},"rejectionNote":{"type":"string","maxLength":2000},"humanSelectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Required for modify; must sit inside the strategy's guardrails."},"scheduledFor":{"type":"string","format":"date-time","description":"Required for schedule; in the future."}}},
"PricingSimulationStudioInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Pricing Simulation Studio submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venue":{"type":"string","description":"Scope: venue id","nullable":true},"product":{"type":"string","description":"Scope: product id","nullable":true},"event":{"type":"string","description":"Scope: event id","nullable":true},"performance":{"type":"string","description":"Scope: performance id","nullable":true},"timeslot":{"type":"string","description":"Scope: timeslot","nullable":true},"priceCategory":{"type":"string","description":"Scope: price category","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Scope: channel"},"customerSegment":{"type":"string","description":"Scope: customer segment","nullable":true},"dateFrom":{"type":"string","description":"Scope: first date","format":"date"},"dateTo":{"type":"string","description":"Scope: last date","format":"date"},"simulationSource":{"type":"string","description":"Simulation Source","enum":["manualPriceChange","dynamicRule","aiRecommendation","newDynamicStrategy","strategyModification","bulkPriceChange"]},"sourceReference":{"type":"string","description":"Id of the rule, recommendation or strategy the simulation came from","nullable":true},"proposedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed price (single-price change)"},"proposedAdjustmentPercent":{"type":"number","description":"Proposed adjustment, percent (bulk change or strategy)","nullable":true}}},
"PricingSimulationStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Simulation Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"expectedDemand":{"type":"integer","description":"Expected Demand"},"expectedConversion":{"type":"number","description":"Expected Conversion, percent"},"expectedAttendance":{"type":"integer","description":"Expected Attendance"},"expectedOccupancy":{"type":"number","description":"Expected Occupancy, percent"},"expectedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected Revenue"},"expectedMargin":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected Margin"},"expectedSellThrough":{"type":"number","description":"Expected Sell-Through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time","format":"date-time","nullable":true},"averageSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Average Selling Price"},"simulationConfidence":{"type":"number","description":"Simulation Confidence, percent"},"dataVolume":{"type":"integer","description":"Data Volume: transactions behind the simulation"},"historicalSimilarity":{"type":"number","description":"Historical Similarity, percent"},"forecastConfidence":{"type":"number","description":"Forecast Confidence, percent"},"elasticityConfidence":{"type":"number","description":"Elasticity Confidence, percent"},"externalSignalQuality":{"type":"number","description":"External Signal Quality, percent"},"simulationId":{"type":"string","description":"Simulation id (saved scenarios keep it)"},"simulationSource":{"type":"string","description":"Simulation Source","enum":["manualPriceChange","dynamicRule","aiRecommendation","newDynamicStrategy","strategyModification","bulkPriceChange"]},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current price"},"proposedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed price"},"baselineRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current strategy: expected revenue"},"baselineDemand":{"type":"integer","description":"Current strategy: expected demand"},"baselineOccupancy":{"type":"number","description":"Current strategy: expected occupancy, percent"},"guardrailChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["commercialGuardrail","contractProtection","priceLadder","approvalThreshold"],"description":"Guardrail"},"passed":{"type":"boolean","description":"Pass / fail"},"message":{"type":"string","description":"Why it failed, or the approval level required"}}},"description":"Guardrail Check shown before the simulation completes"}}},
"RevenueDemandImpactForecastingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Revenue & Demand Impact Forecasting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed: expected revenue"},"demand":{"type":"integer","description":"Proposed: expected demand"},"attendance":{"type":"integer","description":"Proposed: attendance"},"occupancy":{"type":"number","description":"Proposed: occupancy, percent"},"conversion":{"type":"number","description":"Proposed: conversion, percent"},"margin":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed: margin"},"asp":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed: average selling price"},"sellThrough":{"type":"number","description":"Proposed: sell-through, percent"},"sellOutProbability":{"type":"number","description":"Proposed: sell-out probability, percent"},"assessmentId":{"type":"string","description":"Assessment id"},"recommendationId":{"type":"string","description":"Recommendation assessed","nullable":true},"simulationId":{"type":"string","description":"Simulation assessed","nullable":true},"baselineRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Without change: expected revenue"},"baselineDemand":{"type":"integer","description":"Without change: expected demand"},"baselineOccupancy":{"type":"number","description":"Without change: expected occupancy, percent"},"revenueChange":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Impact: revenue"},"revenueChangePercent":{"type":"number","description":"Impact: revenue, percent"},"demandChange":{"type":"integer","description":"Impact: demand"},"demandChangePercent":{"type":"number","description":"Impact: demand, percent"},"marginChange":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Impact: margin"},"customerImpacts":{"type":"array","items":{"type":"object","properties":{"group":{"type":"string","enum":["member","resident","tourist","family","b2b"],"description":"Customer group"},"demandChangePercent":{"type":"number","description":"Estimated demand change, percent"},"note":{"type":"string","description":"Explanation"}}},"description":"Customer Impact, where supported"},"cannibalization":{"type":"array","items":{"type":"object","properties":{"toProduct":{"type":"string","description":"Product demand shifts toward"},"demandShiftPercent":{"type":"number","description":"Share of demand shifting, percent"}}},"description":"Cannibalization"},"bestCaseRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sensitivity: best case revenue"},"worstCaseRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sensitivity: worst case revenue"}}},
"RevenueOptimizationCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Revenue Optimization Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"incrementalRevenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental Revenue Generated"},"activeOptimizations":{"type":"integer","description":"Active Optimizations"},"recommendationsAwaitingAction":{"type":"integer","description":"Recommendations Awaiting Action"},"pendingSimulations":{"type":"integer","description":"Pending Simulations"},"autoExecutedChanges":{"type":"integer","description":"Auto-Executed Changes"},"approvalRequired":{"type":"integer","description":"Approval Required: changes waiting for an approver"},"activeABTests":{"type":"integer","description":"Active A/B Tests"},"pricingExceptions":{"type":"integer","description":"Pricing Exceptions"},"revenueAtRisk":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue at Risk"},"forecastAccuracy":{"type":"number","description":"Forecast Accuracy over the last 30 days (decided 29 September, readiness close-out), percent"},"optimizationSuccessRate":{"type":"number","description":"Optimization Success Rate: executed changes with a positive measured outcome, percent"},"aiRevenueBrief":{"type":"array","items":{"type":"string"},"description":"AI Revenue Brief, e.g. AED 284,000 of opportunity in the next seven days. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"}}},
"RevenueOptimizationCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Revenue Optimization Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue"},"eventProduct":{"type":"string","description":"Event/Product"},"performance":{"type":"string","description":"Performance","nullable":true},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended Price"},"forecastRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast Revenue"},"expectedUplift":{"type":"number","description":"Expected Uplift, percent"},"confidence":{"type":"number","description":"Confidence, percent"},"automationMode":{"type":"string","description":"Automation Mode in force for this scope","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"]},"approvalStatus":{"type":"string","description":"Approval Status: notRequired, pending, approved or rejected"},"executionStatus":{"type":"string","description":"Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack"},"revenueRisk":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Risk if no action is taken"},"eventProximity":{"type":"integer","description":"Event Proximity: days until the event"},"inventoryPosition":{"type":"number","description":"Inventory Position: remaining inventory, percent"},"demandVariance":{"type":"number","description":"Demand Variance against forecast, percent"},"urgency":{"type":"string","description":"Urgency","enum":["low","medium","high","critical"]},"optimizationId":{"type":"string","description":"Optimisation id"},"recommendationId":{"type":"string","description":"Recommendation id","nullable":true},"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"priorityRank":{"type":"integer","description":"Priority rank (1 = act first)"},"nextAction":{"type":"string","description":"Suggested next action (the pack's Action column)","enum":["review","simulate","approve"]}}},
"ScenarioModelingWhatIfAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Scenario Modeling & What-If Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"demand":{"type":"number","description":"Demand adjustment (+/-), percent"},"occupancy":{"type":"number","description":"Occupancy, percent"},"inventory":{"type":"integer","description":"Inventory available"},"bookingVelocity":{"type":"number","description":"Booking velocity adjustment, percent"},"weatherImpact":{"type":"number","description":"Weather impact on demand, percent"},"nearbyEventImpact":{"type":"number","description":"Nearby event impact on demand, percent"},"competitorPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Competitor price"},"conversion":{"type":"number","description":"Conversion, percent"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"eventProximity":{"type":"integer","description":"Event proximity, days"},"remainingCapacity":{"type":"number","description":"Remaining Capacity, percent"},"scenarioId":{"type":"string","description":"Scenario id"},"name":{"type":"string","description":"Scenario name"},"scenarioTypes":{"type":"array","items":{"type":"string","enum":["lowDemand","expectedDemand","highDemand","sellOut","competitorPriceDrop","competitorPriceIncrease","extremeWeather","rain","nearbyExhibition","majorConcert","tourismSurge","cancellationSurge","inventoryReduction","customScenario"]},"description":"Scenario Library entries combined"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event","nullable":true},"strategyResults":{"type":"array","items":{"type":"object","properties":{"strategy":{"type":"string","enum":["fixedPrice","ruleBased","aiRecommendation","custom"],"description":"Strategy compared"},"averagePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Avg. price"},"demand":{"type":"integer","description":"Demand"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"occupancy":{"type":"number","description":"Occupancy, percent"},"margin":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Margin"}}},"description":"Results per strategy"},"reviewStage":{"type":"string","description":"Review stage: draft, submittedForReview or reviewed (decided 29 September, readiness close-out)"},"createdBy":{"type":"string","description":"Author user id"},"updatedAt":{"type":"string","description":"Last saved","format":"date-time"}}},
"SignalRegistryEntry": {"type":"object","x-ticvai-persistence":"catalogue.signal_registry","description":"**The registry of AI signals and models, with their trust and quality** (29 September, data model DM3). ADM-106 and ADM-118. A signal or model not `approved` for a use in `aiUsePermissions` is not used for it.","required":["id","scopePath","registryKind","name","trustLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"registryKind":{"type":"string","enum":["signal","model"]},"name":{"type":"string","maxLength":200},"category":{"type":"string","enum":["internalSales","inventory","weather","nearbyEvents","competitor","tourism","calendar","transport","market","other",null],"nullable":true},"provider":{"type":"string","maxLength":100,"nullable":true},"source":{"type":"string","maxLength":100,"nullable":true},"internalExternal":{"type":"string","enum":["internal","external",null],"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"refreshFrequency":{"type":"string","enum":["realTime","minutes10","hourly","daily","weekly","manual",null],"nullable":true},"trustLevel":{"type":"string","enum":["approved","experimental","advisoryOnly","blocked"],"default":"experimental"},"aiUsePermissions":{"type":"array","items":{"type":"string","enum":["forecasting","recommendations","simulation","automatedPricing"]}},"fallbackPolicy":{"type":"string","enum":["useHistoricalValue","ignore","substitute","reduceConfidence","stopAiRecommendation",null],"nullable":true},"status":{"type":"string","maxLength":40,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"version":{"type":"string","maxLength":40,"nullable":true,"description":"Models."},"purpose":{"type":"string","nullable":true},"deployedAt":{"type":"string","format":"date-time","nullable":true},"trainingWindow":{"type":"string","maxLength":60,"nullable":true},"validationResult":{"type":"string","nullable":true},"lastUpdateAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"qualityCounts":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Signals: `{missingData, delayedData, outliers, invalidValues, unexpectedChanges, sourceFailure, duplicateData}`."},"performance":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Models: `{forecastAccuracy, bias, recommendationAccuracy, revenuePerformance, drift}` and the per-segment learning metrics."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}
}
```
