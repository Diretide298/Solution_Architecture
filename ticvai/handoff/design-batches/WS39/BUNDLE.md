# WS39 — Pricing   Revenue Management board 6

**10 screens · 13 operations · 17 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, PRICE_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-098` | AI Pricing Intelligence Command Center | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-099` | Internal Demand & Booking Signal Hub | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-100` | Weather Intelligence & Demand Impact Configuration | B–D | 24 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-101` | Nearby Event, Exhibition & Local Demand Intelligence | B–D | 46 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-102` | Competitor Pricing & Market Position Intelligence | B–D | 24 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-103` | Market, Tourism, Holiday & Contextual Signal Hub | B–D | 24 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-104` | AI Demand Forecasting & Booking Curve Studio | B–D | 0 | 12 | 6 | 3 | 1 | 6 | — | notStarted (generated) |
| `ADM-105` | Price Elasticity & Revenue Response Intelligence | B–D | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `ADM-106` | AI Pricing Recommendation & Explainability Center | B–D | 5 | 0 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `ADM-107` | AI Signal Registry, Data Quality & Model Governance | B–D | 18 | 48 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-099, ADM-102, ADM-103, ADM-104, ADM-105, ADM-106 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-098` AI Pricing Intelligence Command Center

**Provide Revenue Managers with a single operational view of all AI signals, forecasts, opportunities and risks influencing pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each opportunity displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-pricing-intelligence-command-center-adm-098` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All AI signals, forecasts, opportunities and risks influencing pricing in one view for revenue managers.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listPricing` ?venue |
| Urgency | radio group | — | Low · Medium · High · Critical | `listPricing` ?urgency |
| Risk | segmented control | — | Low · Medium · High | `listPricing` ?risk |
| Min confidence | number field | — | — | `listPricing` ?minConfidence |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active AI Recommendations** (metric tile)

**High-Priority Opportunities** (metric tile)

**Estimated Revenue Opportunity** (metric tile)

**Demand Surges Detected** (metric tile)

**Demand Risks Detected** (metric tile)

**External Signals Active** (metric tile)

**Nearby Events Detected** (metric tile)

**Weather Impacts** (metric tile)

**Competitor Movements** (metric tile)

**Forecast Accuracy** (metric tile)

**Average AI Confidence** (metric tile)

**Data Quality Issues** (metric tile)

**Every pricing intelligence** (data table, from `listPricing`)

| Shows | Format | Notes |
|---|---|---|
| Product event | text | Product/Event name the opportunity applies to |
| Venue | text | Venue name |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Adjustment | 1,234.5 | Adjustment % from current to recommended price, percent |
| Demand forecast | 1,234 | Demand Forecast: forecast demand (admissions) for the period |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |
| Confidence | 1,234.5 | AI confidence in the recommendation, 0-100, percent |
| Risk | chip: Low, Medium, High | Risk of acting on the recommendation |
| Urgency | chip: Low, Medium, High, Critical | Urgency (time to event and velocity) |

**The selected pricing intelligence** (detail panel): The pack groups this record's detail under its own headings: “Saturday Evening Admission”, “Drivers”.

| Shows | Format | Notes |
|---|---|---|
| Product event | text | Product/Event name the opportunity applies to |
| Venue | text | Venue name |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Adjustment | 1,234.5 | Adjustment % from current to recommended price, percent |
| Demand forecast | 1,234 | Demand Forecast: forecast demand (admissions) for the period |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |
| Confidence | 1,234.5 | AI confidence in the recommendation, 0-100, percent |
| Risk | chip: Low, Medium, High | Risk of acting on the recommendation |
| Urgency | chip: Low, Medium, High, Critical | Urgency (time to event and velocity) |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **signals and recommendations**: KPI summary on top, paged list of pricing signals, each with confidence and the recommended action. *(source: contracts/spine/catalogue.yaml#listPricing / DI-043)*

**Data it reads**: `listPricing` (onLoad, AI Pricing Intelligence Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-099` Internal Demand & Booking Signal Hub: *Works in Internal Demand & Booking Signal Hub*; calls `listPricing`
- → `ADM-100` Weather Intelligence & Demand Impact Configuration: *Works in Weather Intelligence & Demand Impact Configuration*; calls `listPricing`
- → `ADM-101` Nearby Event, Exhibition & Local Demand Intelligence: *Works in Nearby Event, Exhibition & Local Demand Intelligence*; calls `listPricing`
- → `ADM-102` Competitor Pricing & Market Position Intelligence: *Works in Competitor Pricing & Market Position Intelligence*; calls `listPricing`
- → `ADM-103` Market, Tourism, Holiday & Contextual Signal Hub: *Works in Market, Tourism, Holiday & Contextual Signal Hub*; calls `listPricing`
- → `ADM-104` AI Demand Forecasting & Booking Curve Studio: *Works in AI Demand Forecasting & Booking Curve Studio*; calls `listPricing`
- → `ADM-105` Price Elasticity & Revenue Response Intelligence: *Works in Price Elasticity & Revenue Response Intelligence*; calls `listPricing`
- → `ADM-106` AI Pricing Recommendation & Explainability Center: *Works in AI Pricing Recommendation & Explainability Center*; carries `recommendationId`; calls `listPricing`
- → `ADM-107` AI Signal Registry, Data Quality & Model Governance: *Works in AI Signal Registry, Data Quality & Model Governance*; calls `listPricing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  product: Day Pass
  signal: Forecast rain Sat
  recommendation: -10% Sat online
  confidence: 0.74
```

#### Permissions

- `listPricing` → `PRODUCT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-098` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-098`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 1: Opens AI Pricing Intelligence Command Center → Provide Revenue Managers with a single operational view of all AI signals, forecasts, opportunities and risks influencing pricing.
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F148 branch at step 1 (expected): when Nothing has been set up on AI Pricing Intelligence Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F148 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-098?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-099`, `ADM-100`, `ADM-101`, `ADM-102`, `ADM-103`, `ADM-104`, `ADM-105`, `ADM-106`, `ADM-107`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-099` Internal Demand & Booking Signal Hub

**Centralize the internal TICVAI signals used by forecasting and AI pricing models. These are generally the highest-confidence signals because they come directly from TICVAI transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/internal-demand-booking-signal-hub-adm-099` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Internal signals (sales pace, bookings, cancellations, occupancy, attendance) feeding forecasting and AI pricing; the highest-confidence signals.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Granularity | select | — | Tenant · Market · Venue · Event · Performance · Product · Price category · Channel · Timeslot | `listInternalDemandBooking` ?granularity |
| Venue | text field | — | — | `listInternalDemandBooking` ?venue |
| Event | text field | — | — | `listInternalDemandBooking` ?event |
| Performance | text field | — | — | `listInternalDemandBooking` ?performance |
| Product | text field | — | — | `listInternalDemandBooking` ?product |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listInternalDemandBooking` ?channel |
| Date from | date picker | — | — | `listInternalDemandBooking` ?dateFrom |
| Date to | date picker | — | — | `listInternalDemandBooking` ?dateTo |
| Compare to | select | — | Yesterday · Previous week · Same day last year · Previous event · Similar event · Forecast baseline | `listInternalDemandBooking` ?compareTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **signal list**: Signal, current value, trend, freshness. *(source: contracts/spine/catalogue.yaml#listInternalDemandBooking)*

**Data it reads**: `listInternalDemandBooking` (onLoad, Internal Demand & Booking Signal Hub)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listInternalDemandBooking`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The internal demand booking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the internal demand booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No internal demand booking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the internal demand booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  name: Bookings last 24 h
  value: 1840
  trend: +12%
```

#### Permissions

- `listInternalDemandBooking` → `PRODUCT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-099` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-099`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 2: Works in Internal Demand & Booking Signal Hub → Centralize the internal TICVAI signals used by forecasting and AI pricing models. These are generally the highest-confidence signals because they come directly from TICVAI transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-099?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-100` Weather Intelligence & Demand Impact Configuration

**Allow TICVAI to understand how weather conditions affect demand for different venues and experiences. This should be much more sophisticated than simply connecting a weather API.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `signalId` (navigation) |
| Route | `/commercial/weather-intelligence-demand-impact-configuration-adm-100` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How weather affects demand per venue and experience, and how the weather signal is used.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listWeatherDemandImpact` ?venue |
| Venue exposure | segmented control | — | Indoor · Outdoor · Mixed | `listWeatherDemandImpact` ?venueExposure |
| Forecast horizon | radio group | — | Today · Hours24 · Days3 · Days7 · Custom | `listWeatherDemandImpact` ?forecastHorizon |

**Form: Save demand signal configuration** (modal, opened by *Save demand signal configuration*; *Save demand signal configuration* calls `setDemandSignalConfiguration`, *Cancel* sends nothing)

**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `id`, `scopePath`, `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Signal kind `signalKind` | select | required | — | Weather · Nearby event · Competitor price · Calendar · Tourism · Transport · Market | — | — | `setDemandSignalConfiguration` body |
| Signal type `signalType` | text field | optional | — | max length 60 | — | E.g. `publicHoliday`, `ramadan`, an event type, a weather condition. | `setDemandSignalConfiguration` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setDemandSignalConfiguration` body |
| Source `source` | text field | required | — | max length 100 | — | Provider, feed or `tenant` for manual entries. | `setDemandSignalConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setDemandSignalConfiguration` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Competitor observations: the comparable TICVAI product. | `setDemandSignalConfiguration` body |
| Geography `geography` | text field | optional | — | max length 100 | — | — | `setDemandSignalConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setDemandSignalConfiguration` body |
| Period start `periodStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Period end `periodEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Current value `currentValue` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Unit `unit` | text field | optional | — | max length 20 | — | — | `setDemandSignalConfiguration` body |
| Reading `reading` | key and value settings | optional | — | — | — | Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices. | `setDemandSignalConfiguration` body |
| Configuration `configuration` | key and value settings | optional | — | — | — | Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`. | `setDemandSignalConfiguration` body |
| Weight `weight` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Reliability `reliability` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Historical correlation `historicalCorrelation` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Confidence `confidence` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Impact min percent `impactMinPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Impact max percent `impactMaxPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Refresh frequency `refreshFrequency` | radio group | optional | — | Real time · Hourly · Daily · Weekly · Manual | — | — | `setDemandSignalConfiguration` body |
| Is approved `isApproved` | toggle | optional | off | — | — | Competitor sources and comparability approved for use. | `setDemandSignalConfiguration` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setDemandSignalConfiguration` body |
| Observed at `observedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |

Errors to draw in the form: 409 `feedSignal`.; 422 `invalidPeriod`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **weather signal configuration**: Impact range per condition (rain, heat over 42 degrees) and weight. *(source: contracts/spine/catalogue.yaml#setDemandSignalConfiguration)*

#### Outputs: what the screen shows and produces

**Shown**

**Weather Forecast Confidence: 93%** (metric tile)

**Estimated Demand Impact: +8–12%** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Hourly Forecast (primary button) | navigation or local | — | — | — | — |
| Daily Forecast (secondary button) | navigation or local | — | — | — | — |
| Save demand signal configuration (secondary button) | `setDemandSignalConfiguration` PUT `/demand-signals/{signalId}` | DemandSignal | DemandSignal | 409 `feedSignal`.; 422 `invalidPeriod`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listWeatherDemandImpact` (onLoad, Weather Intelligence & Demand Impact Configuration)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listWeatherDemandImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The weather intelligence demand list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the weather intelligence demand untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No weather intelligence demand yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the weather intelligence demand are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `feedSignal`.; 422 `invalidPeriod`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
impact:
  venue: Coastal Aqua
  rain: -35%
  heat42: -20%
```

#### Permissions

- `listWeatherDemandImpact` → `PRODUCT_VIEW` (read) · staff
- `setDemandSignalConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-100` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-100`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 4: Works in Weather Intelligence & Demand Impact Configuration → Allow TICVAI to understand how weather conditions affect demand for different venues and experiences. This should be much more sophisticated than simply connecting a weather API.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-100?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Hourly Forecast, Daily Forecast, Save demand signal configuration.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-101` Nearby Event, Exhibition & Local Demand Intelligence

**Detect external events around TICVAI venues that could materially affect visitor demand. This directly addresses the exhibition-near-the-venue scenario.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Detect/configure; Capture; Configure per TICVAI venue) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `signalId` (navigation) |
| Route | `/commercial/nearby-event-exhibition-local-demand-intelligence-adm-101` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** External events near the venues that could change demand (an exhibition next door), with their expected impact.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Exhibition | select field | — | — | — | — | — | — |
| Conference | select field | — | — | — | — | — | — |
| Concert | select field | — | — | — | — | — | — |
| Sports Event | select field | — | — | — | — | — | — |
| Festival | select field | — | — | — | — | — | — |
| Trade Show | select field | — | — | — | — | — | — |
| Convention | select field | — | — | — | — | — | — |
| Public Celebration | select field | — | — | — | — | — | — |
| Major Attraction Event | select field | — | — | — | — | — | — |
| School Event | select field | — | — | — | — | — | — |
| Custom Local Event | select field | — | — | — | — | — | — |
| Event Name | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Distance from TICVAI Venue | text field | — | — | — | — | — | — |
| Start/End Date | select field | — | — | — | — | — | — |
| Start/End Time | select field | — | — | — | — | — | — |
| Expected Attendance | select field | — | — | — | — | — | — |
| Event Type | select field | — | — | — | — | — | — |
| Audience Type | select field | — | — | — | — | — | — |
| Source | select field | — | — | — | — | — | — |
| Confidence | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticvai venue | text field | — | — | `listNearbyEventExhibition` ?ticvaiVenue |
| Event type | select | — | Exhibition · Conference · Concert · Sports event · Festival · Trade show · Convention · Public celebration · Major attraction event · School event · Custom local event | `listNearbyEventExhibition` ?eventType |
| Radius km | number field | — | — | `listNearbyEventExhibition` ?radiusKm |
| Date from | date picker | — | — | `listNearbyEventExhibition` ?dateFrom |
| Date to | date picker | — | — | `listNearbyEventExhibition` ?dateTo |

**Form: Save demand signal configuration** (modal, opened by *Save demand signal configuration*; *Save demand signal configuration* calls `setDemandSignalConfiguration`, *Cancel* sends nothing)

**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `id`, `scopePath`, `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Signal kind `signalKind` | select | required | — | Weather · Nearby event · Competitor price · Calendar · Tourism · Transport · Market | — | — | `setDemandSignalConfiguration` body |
| Signal type `signalType` | text field | optional | — | max length 60 | — | E.g. `publicHoliday`, `ramadan`, an event type, a weather condition. | `setDemandSignalConfiguration` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setDemandSignalConfiguration` body |
| Source `source` | text field | required | — | max length 100 | — | Provider, feed or `tenant` for manual entries. | `setDemandSignalConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setDemandSignalConfiguration` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Competitor observations: the comparable TICVAI product. | `setDemandSignalConfiguration` body |
| Geography `geography` | text field | optional | — | max length 100 | — | — | `setDemandSignalConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setDemandSignalConfiguration` body |
| Period start `periodStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Period end `periodEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Current value `currentValue` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Unit `unit` | text field | optional | — | max length 20 | — | — | `setDemandSignalConfiguration` body |
| Reading `reading` | key and value settings | optional | — | — | — | Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices. | `setDemandSignalConfiguration` body |
| Configuration `configuration` | key and value settings | optional | — | — | — | Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`. | `setDemandSignalConfiguration` body |
| Weight `weight` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Reliability `reliability` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Historical correlation `historicalCorrelation` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Confidence `confidence` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Impact min percent `impactMinPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Impact max percent `impactMaxPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Refresh frequency `refreshFrequency` | radio group | optional | — | Real time · Hourly · Daily · Weekly · Manual | — | — | `setDemandSignalConfiguration` body |
| Is approved `isApproved` | toggle | optional | off | — | — | Competitor sources and comparability approved for use. | `setDemandSignalConfiguration` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setDemandSignalConfiguration` body |
| Observed at `observedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |

Errors to draw in the form: 409 `feedSignal`.; 422 `invalidPeriod`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save demand signal configuration (primary button) | `setDemandSignalConfiguration` PUT `/demand-signals/{signalId}` | DemandSignal | DemandSignal | 409 `feedSignal`.; 422 `invalidPeriod`. | gated `PRICE_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **nearby events**: Event, distance, dates, expected impact. *(source: contracts/spine/catalogue.yaml#listNearbyEventExhibition)*

**Data it reads**: `listNearbyEventExhibition` (onLoad, Nearby Event, Exhibition & Local Demand Intelligence)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listNearbyEventExhibition`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The nearby event exhibition configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the nearby event exhibition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No nearby event exhibition configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `feedSignal`.; 422 `invalidPeriod`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  name: Big Boat Show
  distance: 4 km
  dates: 12-16 Nov
  impact: +8%
```

#### Permissions

- `listNearbyEventExhibition` → `PRODUCT_VIEW` (read) · staff
- `setDemandSignalConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-101` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-101`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 6: Works in Nearby Event, Exhibition & Local Demand Intelligence → Detect external events around TICVAI venues that could materially affect visitor demand. This directly addresses the exhibition-near-the-venue scenario.

#### Acceptance for the design

- [ ] Every input above is drawn (46), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-101?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save demand signal configuration.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-102` Competitor Pricing & Market Position Intelligence

**Allow TICVAI to understand its commercial position relative to relevant competitors.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `signalId` (navigation) |
| Route | `/commercial/competitor-pricing-market-position-intelligence-adm-102` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Position against competitors' prices.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Competitor | text field | — | — | `listCompetitorPricingMarket` ?competitor |
| Market | text field | — | — | `listCompetitorPricingMarket` ?market |
| Comparable ticvai product | text field | — | — | `listCompetitorPricingMarket` ?comparableTicvaiProduct |
| Date from | date picker | — | — | `listCompetitorPricingMarket` ?dateFrom |
| Date to | date picker | — | — | `listCompetitorPricingMarket` ?dateTo |

**Form: Save demand signal configuration** (modal, opened by *Save demand signal configuration*; *Save demand signal configuration* calls `setDemandSignalConfiguration`, *Cancel* sends nothing)

**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `id`, `scopePath`, `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Signal kind `signalKind` | select | required | — | Weather · Nearby event · Competitor price · Calendar · Tourism · Transport · Market | — | — | `setDemandSignalConfiguration` body |
| Signal type `signalType` | text field | optional | — | max length 60 | — | E.g. `publicHoliday`, `ramadan`, an event type, a weather condition. | `setDemandSignalConfiguration` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setDemandSignalConfiguration` body |
| Source `source` | text field | required | — | max length 100 | — | Provider, feed or `tenant` for manual entries. | `setDemandSignalConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setDemandSignalConfiguration` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Competitor observations: the comparable TICVAI product. | `setDemandSignalConfiguration` body |
| Geography `geography` | text field | optional | — | max length 100 | — | — | `setDemandSignalConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setDemandSignalConfiguration` body |
| Period start `periodStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Period end `periodEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Current value `currentValue` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Unit `unit` | text field | optional | — | max length 20 | — | — | `setDemandSignalConfiguration` body |
| Reading `reading` | key and value settings | optional | — | — | — | Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices. | `setDemandSignalConfiguration` body |
| Configuration `configuration` | key and value settings | optional | — | — | — | Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`. | `setDemandSignalConfiguration` body |
| Weight `weight` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Reliability `reliability` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Historical correlation `historicalCorrelation` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Confidence `confidence` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Impact min percent `impactMinPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Impact max percent `impactMaxPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Refresh frequency `refreshFrequency` | radio group | optional | — | Real time · Hourly · Daily · Weekly · Manual | — | — | `setDemandSignalConfiguration` body |
| Is approved `isApproved` | toggle | optional | off | — | — | Competitor sources and comparability approved for use. | `setDemandSignalConfiguration` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setDemandSignalConfiguration` body |
| Observed at `observedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |

Errors to draw in the form: 409 `feedSignal`.; 422 `invalidPeriod`.

#### Outputs: what the screen shows and produces

**Shown**

**Every competitor pricing market** (data table, from `listCompetitorPricingMarket`)

| Shows | Format | Notes |
|---|---|---|
| Published price | AED 1,234.50 | Published Price |
| Promotional price | AED 1,234.50 | Promotional Price |
| Weekend price | AED 1,234.50 | Weekend Price |
| Peak price | AED 1,234.50 | Peak Price |
| Resident price | AED 1,234.50 | Resident Price |
| Member price where publicly available | AED 1,234.50 | Member Price where publicly available |
| Availability | chip: Available, Limited, Sold out, Unknown | Availability as published |
| Date | 1 Oct 2026 | Date the price applies to |
| Timeslot | text | Timeslot |

**The selected competitor pricing market** (detail panel): The pack groups this record's detail under its own headings: “AED 275”, “Comparable Product Mapping”, “General Admission”, “Historical Correlation”, “Ethical/Legal Controls”.

| Shows | Format | Notes |
|---|---|---|
| Published price | AED 1,234.50 | Published Price |
| Promotional price | AED 1,234.50 | Promotional Price |
| Weekend price | AED 1,234.50 | Weekend Price |
| Peak price | AED 1,234.50 | Peak Price |
| Resident price | AED 1,234.50 | Resident Price |
| Member price where publicly available | AED 1,234.50 | Member Price where publicly available |
| Availability | chip: Available, Limited, Sold out, Unknown | Availability as published |
| Date | 1 Oct 2026 | Date the price applies to |
| Timeslot | text | Timeslot |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save demand signal configuration (primary button) | `setDemandSignalConfiguration` PUT `/demand-signals/{signalId}` | DemandSignal | DemandSignal | 409 `feedSignal`.; 422 `invalidPeriod`. | gated `PRICE_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **competitor table**: Competitor, product compared, their price, our price, gap. *(source: contracts/spine/catalogue.yaml#listCompetitorPricingMarket)*

**Data it reads**: `listCompetitorPricingMarket` (onLoad, Competitor Pricing & Market Position Intelligence)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listCompetitorPricingMarket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The competitor pricing market list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the competitor pricing market untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No competitor pricing market yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the competitor pricing market are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `feedSignal`.; 422 `invalidPeriod`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  competitor: Competitor water park A
  product: Day pass adult
  theirs: AED 299.00
  ours: AED 295.00
```

#### Permissions

- `listCompetitorPricingMarket` → `PRODUCT_VIEW` (read) · staff
- `setDemandSignalConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-102` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-102`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 8: Works in Competitor Pricing & Market Position Intelligence → Allow TICVAI to understand its commercial position relative to relevant competitors.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-102?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save demand signal configuration.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-103` Market, Tourism, Holiday & Contextual Signal Hub

**Capture broader external factors that may affect visitor demand beyond weather and nearby events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `signalId` (navigation) |
| Route | `/commercial/market-tourism-holiday-contextual-signal-hub-adm-103` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Broader external signals: tourism, holidays, school breaks, transport, market.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | radio group | — | Calendar · Tourism · Transport · Market | `listMarketTourismHoliday` ?category |
| Signal type | select | — | Public holiday · School holiday · Ramadan · Eid · Christmas · New year · Long weekend · Visitor arrivals · Tourism demand · Hotel occupancy · Hotel rates · Destination demand … | `listMarketTourismHoliday` ?signalType |
| Geography | text field | — | — | `listMarketTourismHoliday` ?geography |
| Active | toggle | — | — | `listMarketTourismHoliday` ?active |

**Form: Save demand signal configuration** (modal, opened by *Save demand signal configuration*; *Save demand signal configuration* calls `setDemandSignalConfiguration`, *Cancel* sends nothing)

**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `id`, `scopePath`, `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Signal kind `signalKind` | select | required | — | Weather · Nearby event · Competitor price · Calendar · Tourism · Transport · Market | — | — | `setDemandSignalConfiguration` body |
| Signal type `signalType` | text field | optional | — | max length 60 | — | E.g. `publicHoliday`, `ramadan`, an event type, a weather condition. | `setDemandSignalConfiguration` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setDemandSignalConfiguration` body |
| Source `source` | text field | required | — | max length 100 | — | Provider, feed or `tenant` for manual entries. | `setDemandSignalConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setDemandSignalConfiguration` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Competitor observations: the comparable TICVAI product. | `setDemandSignalConfiguration` body |
| Geography `geography` | text field | optional | — | max length 100 | — | — | `setDemandSignalConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setDemandSignalConfiguration` body |
| Period start `periodStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Period end `periodEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |
| Current value `currentValue` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Unit `unit` | text field | optional | — | max length 20 | — | — | `setDemandSignalConfiguration` body |
| Reading `reading` | key and value settings | optional | — | — | — | Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices. | `setDemandSignalConfiguration` body |
| Configuration `configuration` | key and value settings | optional | — | — | — | Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`. | `setDemandSignalConfiguration` body |
| Weight `weight` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Reliability `reliability` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Historical correlation `historicalCorrelation` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Confidence `confidence` | stepper or slider | optional | — | min 0; max 1 | — | — | `setDemandSignalConfiguration` body |
| Impact min percent `impactMinPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Impact max percent `impactMaxPercent` | number field | optional | — | — | — | — | `setDemandSignalConfiguration` body |
| Refresh frequency `refreshFrequency` | radio group | optional | — | Real time · Hourly · Daily · Weekly · Manual | — | — | `setDemandSignalConfiguration` body |
| Is approved `isApproved` | toggle | optional | off | — | — | Competitor sources and comparability approved for use. | `setDemandSignalConfiguration` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setDemandSignalConfiguration` body |
| Observed at `observedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDemandSignalConfiguration` body |

Errors to draw in the form: 409 `feedSignal`.; 422 `invalidPeriod`.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save demand signal configuration (primary button) | `setDemandSignalConfiguration` PUT `/demand-signals/{signalId}` | DemandSignal | DemandSignal | 409 `feedSignal`.; 422 `invalidPeriod`. | gated `PRICE_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **contextual signals**: Calendar of signals with source and reliability. *(source: contracts/spine/catalogue.yaml#listMarketTourismHoliday / DI-942)*

**Data it reads**: `listMarketTourismHoliday` (onLoad, Market, Tourism, Holiday & Contextual Signal Hub)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listMarketTourismHoliday`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The market tourism holiday list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the market tourism holiday untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No market tourism holiday yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the market tourism holiday are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `feedSignal`.; 422 `invalidPeriod`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  name: UAE school winter break
  from: '2026-12-14'
  to: '2027-01-03'
  reliability: 0.95
```

#### Permissions

- `listMarketTourismHoliday` → `PRODUCT_VIEW` (read) · staff
- `setDemandSignalConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Forecast signal configuration defines which data sources and coverage periods the AI may use, e.g. historical sales over the last 36 months, real-time bookings and attendance history; seasonality, festivities and weather (e.g. forecast rain) are factored in. *(client request · MoM 18 Sep 2026, 4.9 AI Forecasting — Model Strategies & Signal Configuration · DI-942)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-103` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-103`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 10: Works in Market, Tourism, Holiday & Contextual Signal Hub → Capture broader external factors that may affect visitor demand beyond weather and nearby events.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-103?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save demand signal configuration.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-104` AI Demand Forecasting & Booking Curve Studio

**Predict future demand at a granular commercial level. This is the core predictive engine behind intelligent dynamic pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-demand-forecasting-booking-curve-studio-adm-104` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Event Horizon. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **AI Demand Forecasting & Booking Curve Studio declares no operation that writes anything** — its only declared call is `listDemandBookingCurve`, a read. The name promises authoring and the contract …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Granular demand forecasts with booking curves: pace, forecast and remaining opportunity by channel, with drivers and confidence, and a what-if simulator.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Event Horizon. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every demand forecasting booking** (data table, from `listDemandBookingCurve`)

| Shows | Format | Notes |
|---|---|---|
| Confidence | 1,234.5 | Forecast Confidence, percent |
| Confidence reasons | list or chips (count when long) | Reasons behind the forecast confidence |
| Mape | 1,234.5 | MAPE over closed forecasts at this level, percent |
| Forecast bias | 1,234.5 | Forecast Bias (positive = over-forecast), percent |
| Over forecast | 1,234.5 | Share of closed forecasts that over-forecast, percent |
| Under forecast | 1,234.5 | Share of closed forecasts that under-forecast, percent |

**The selected demand forecasting booking** (detail panel): The pack groups this record's detail under its own headings: “Historical Expected Curve”, “Current Actual Curve”, “Saturday Performance”, “Actual”, “Provide”, “Clearly show which signals contributed”.

| Shows | Format | Notes |
|---|---|---|
| Confidence | 1,234.5 | Forecast Confidence, percent |
| Confidence reasons | list or chips (count when long) | Reasons behind the forecast confidence |
| Mape | 1,234.5 | MAPE over closed forecasts at this level, percent |
| Forecast bias | 1,234.5 | Forecast Bias (positive = over-forecast), percent |
| Over forecast | 1,234.5 | Share of closed forecasts that over-forecast, percent |
| Under forecast | 1,234.5 | Share of closed forecasts that under-forecast, percent |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event Horizon (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **booking curve**: Actual vs forecast by days to visit, confidence band, by channel. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve / DI-943)*

**Data it reads**: `listDemandBookingCurve` (onLoad, AI Demand Forecasting & Booking Curve Studio)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listDemandBookingCurve`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demand forecasting booking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demand forecasting booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demand forecasting booking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demand forecasting booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  product: Day Pass
  date: Sat 22 Nov
  forecast: 6100
  capacity: 6500
  confidence: 0.82
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-104` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-104`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 12: Works in AI Demand Forecasting & Booking Curve Studio → Predict future demand at a granular commercial level. This is the core predictive engine behind intelligent dynamic pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-104?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event Horizon.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-105` Price Elasticity & Revenue Response Intelligence

**Estimate how customers are likely to respond to different prices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-elasticity-revenue-response-intelligence-adm-105` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How guests respond to price: elasticity per product and segment, revenue response curve.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Weekday weekend | segmented control | — | Weekday · Weekend | `listPriceElasticityRevenue` ?weekdayWeekend |
| Peak off peak | segmented control | — | Peak · Off peak | `listPriceElasticityRevenue` ?peakOffPeak |
| Event proximity | number field | — | — | `listPriceElasticityRevenue` ?eventProximity |
| Season | text field | — | — | `listPriceElasticityRevenue` ?season |
| Venue | text field | — | — | `listPriceElasticityRevenue` ?venue |
| Product | text field | — | — | `listPriceElasticityRevenue` ?product |
| Customer segment | text field | — | — | `listPriceElasticityRevenue` ?customerSegment |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listPriceElasticityRevenue` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every price elasticity revenue** (data table, from `listPriceElasticityRevenue`)

| Shows | Format | Notes |
|---|---|---|
| Price | AED 1,234.50 | Price tested on the curve |
| Demand | 1,234 | Expected demand at this price |
| Conversion | 1,234.5 | Expected conversion, percent |
| Revenue | AED 1,234.50 | Expected revenue |
| Margin | AED 1,234.50 | Expected margin |
| Occupancy | 1,234.5 | Expected occupancy, percent |
| Customer segment | text | Customer segment (e.g. |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Channel |
| Time | text | Time context of the curve: weekday/weekend, peak/off-peak or season label |
| Product | text | Product id |

**The selected price elasticity revenue** (detail panel): The pack groups this record's detail under its own headings: “Elasticity answers”, “AED AED”, “Analyze differences by”, “Where insufficient data exists”.

| Shows | Format | Notes |
|---|---|---|
| Price | AED 1,234.50 | Price tested on the curve |
| Demand | 1,234 | Expected demand at this price |
| Conversion | 1,234.5 | Expected conversion, percent |
| Revenue | AED 1,234.50 | Expected revenue |
| Margin | AED 1,234.50 | Expected margin |
| Occupancy | 1,234.5 | Expected occupancy, percent |
| Customer segment | text | Customer segment (e.g. |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Channel |
| Time | text | Time context of the curve: weekday/weekend, peak/off-peak or season label |
| Product | text | Product id |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **elasticity**: Curve of price vs expected volume and revenue with the revenue-maximising point marked. *(source: contracts/spine/catalogue.yaml#listPriceElasticityRevenue)*

**Data it reads**: `listPriceElasticityRevenue` (onLoad, Price Elasticity & Revenue Response Intelligence)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listPriceElasticityRevenue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price elasticity revenue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price elasticity revenue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price elasticity revenue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price elasticity revenue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
elasticity:
  product: Day Pass Adult
  elasticity: -1.4
  optimum: AED 285.00
```

#### Permissions

- `listPriceElasticityRevenue` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.18 | System shall support price elasticity analysis. | Unified Operations Dashboard | CONTRACTED | `listPriceElasticityRevenue` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-105` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-105`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 14: Works in Price Elasticity & Revenue Response Intelligence → Estimate how customers are likely to respond to different prices.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-105?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-106` AI Pricing Recommendation & Explainability Center

**Convert all intelligence generated by Board 6 into actionable pricing recommendations. This is the central AI recommendation screen.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `recommendationId` (navigation) |
| Route | `/commercial/ai-pricing-recommendation-explainability-center-adm-106` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Actionable AI pricing recommendations with their explanation, impact and confidence; a person decides.

**Fixed on main** (the package already carries these; draw what it says): No operation accepts or dismisses a recommendation. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listPricingRecommendationExplainability` ?venue |
| Event | text field | — | — | `listPricingRecommendationExplainability` ?event |
| Review outcome | select | — | Pending · Accepted · Rejected · Modified · Ignored · Sent to simulation · Sent for approval | `listPricingRecommendationExplainability` ?reviewOutcome |
| Min confidence | number field | — | — | `listPricingRecommendationExplainability` ?minConfidence |
| Recommendation type | radio group | — | Standard · Early bird · Last minute · Volume discount · Conversion | `listPricingRecommendationExplainability` ?recommendationType |
| Objective | segmented control | — | Revenue · Occupancy · Conversion | `listPricingRecommendationExplainability` ?objective |
| Price category | picker: choose a price category | — | — | `listPricingRecommendationExplainability` ?priceCategory |

**Form: Decide** (modal, opened by *Decide*; *Decide* calls `decidePricingRecommendation`, *Cancel* sends nothing)

**Collects what `decidePricingRecommendation` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Accept · Modify · Reject · Schedule · Send for approval | — | — | `decidePricingRecommendation` body |
| Rejection reason `rejectionReason` | select | optional | — | Commercial judgment · Brand positioning · Customer sensitivity · Event strategy · Incorrect signal · Data concern · Other | — | Required for reject. | `decidePricingRecommendation` body |
| Rejection note `rejectionNote` | text area | optional | — | max length 2000 | — | — | `decidePricingRecommendation` body |
| Human selected price `humanSelectedPrice` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Required for modify; must sit inside the strategy's guardrails. | `decidePricingRecommendation` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Required for schedule; in the future. | `decidePricingRecommendation` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired (`recommendationExpired`).; 422 `rejectionReasonRequired`, `humanSelectedPriceRequired`, `guardrailBreached` or `scheduledForInPast`.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Accept, Reject, Modify, Send to Simulation, Send for Approval, Ignore, Add Comment. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide (secondary button) | `decidePricingRecommendation` POST `/recommendation-review-decision/{recommendationId}/decision` | PricingRecommendationDecisionInput | PricingRecommendationDecision | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **recommendation card**: Framing, recommendation, impact ("+12%"), confidence, drivers, then Accept or Dismiss, as DI-043. *(source: contracts/spine/catalogue.yaml#listPricingRecommendationExplainability / DI-043 / DI-601)*

**Data it reads**: `listPricingRecommendationExplainability` (onLoad, AI Pricing Recommendation & Explainability Center)

**Where the user goes next**

- → `ADM-098` AI Pricing Intelligence Command Center: *Returns to the board's landing screen*; calls `listPricingRecommendationExplainability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing recommendation explainability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing recommendation explainability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing recommendation explainability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing recommendation explainability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The recommendation is no longer `pending` or `sentToSimulation` (`alreadyDecided`) or has expired (`recommendationExpired`).; 422 `rejectionReasonRequired`, `humanSelectedPriceRequired`, `guardrailBreached` or `scheduledForInPast`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recommendation:
  text: Increase Desert Symphony balcony seats by 8%
  impact: +AED 22,000.00
  confidence: 0.77
```

#### Permissions

- `listPricingRecommendationExplainability` → `PRODUCT_VIEW` (read) · staff
- `decidePricingRecommendation` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.27 | Dynamic Pricing Recommendations Based on historical event data, AI can: Suggest optimal pricing per seat category. Identify high-demand areas. Recommend premium pricing for preferred seats. Generate … | Ticketing Catalogue | CONTRACTED | `listPricingRecommendationExplainability` |
| 2.9.18 | System shall recommend pricing adjustments based on demand forecasts, occupancy levels, sales performance, seasonality, holidays, weather conditions, and revenue optimization goals. | Ticketing Sales | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.13 | System shall support AI-generated pricing recommendations. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.29 | System shall expose pricing recommendations through APIs. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.34 | System shall support AI-generated seasonal pricing recommendations. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.35 | System shall support AI-generated event-based pricing recommendations. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.36 | System shall support AI-generated occupancy-based pricing recommendations. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.38 | System shall support AI-generated pricing recommendations based on weather conditions. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.39 | System shall support AI-generated pricing recommendations based on public events. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.40 | System shall support AI-generated pricing recommendations based on market trends. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.41 | System shall support AI-generated pricing recommendations based on competitor pricing. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |
| 8.5.42 | System shall support AI-generated pricing recommendations based on booking velocity. | Unified Operations Dashboard | CONTRACTED | `listPricingRecommendationExplainability` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting recommends pricing/promotional action ahead of demand shifts (e.g. forecast rain > recommend a discount); a simulation tool previews the likely impact of a price change before it goes live. *(client request · MoM 1 Sep 2026, 4.8 AI Demand Forecasting & Pricing Simulation · DI-601)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-106` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-106`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 16: Works in AI Pricing Recommendation & Explainability Center → Convert all intelligence generated by Board 6 into actionable pricing recommendations. This is the central AI recommendation screen.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-106?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide.
- [ ] Every transition is wired: `ADM-098`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-107` AI Signal Registry, Data Quality & Model Governance

**Govern the complete data and intelligence ecosystem behind AI pricing. This is critical. Without this screen, Development team could connect many external sources without giving TICVAI proper control over them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Monitor; Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-signal-registry-data-quality-model-governance-adm-107` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Governance of the signals and models behind AI pricing: provider, refresh, trust level (approved, experimental, advisory only, blocked), what AI may use each for, and what happens when a signal fails.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Registry kind | segmented control | — | Signal · Model | `listSignalDataQuality` ?registryKind |
| Internal external | segmented control | — | Internal · External | `listSignalDataQuality` ?internalExternal |
| Trust level | radio group | — | Approved · Experimental · Advisory only · Blocked | `listSignalDataQuality` ?trustLevel |
| Search | text field | — | — | `listSignalDataQuality` ?search |

**Form: Save signal registry policy** (modal, opened by *Save signal registry policy*; *Save signal registry policy* calls `setSignalRegistryPolicy`, *Cancel* sends nothing)

**Collects what `setSignalRegistryPolicy` sends before it is called.** Required: `id`, `scopePath`, `registryKind`, `name`, `trustLevel`. Optional: `category`, `provider`, `source`, `internalExternal`, `marketCode`, `refreshFrequency`, `aiUsePermissions`, `fallbackPolicy`, `status`, `ownerPrincipalId`, `purpose`, `deployedAt` and 5 more. Dismissing sends nothing; the screen behind is unchanged.

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

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **trustLevel and aiUsePermissions**: Blocked removes every use; advisory only allows forecasting and recommendations but not automated pricing. *(source: contracts/spine/catalogue.yaml#setSignalRegistryPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every signal registry data** (data table, from `listSignalDataQuality`)

| Shows | Format | Notes |
|---|---|---|
| Signal | text | Signal name (signal rows) |
| Category | chip: Internal sales, Inventory, Weather, Nearby events, Competitor, Tourism… | Category |
| Provider | text | Provider name (vendor-neutral, data) |
| Source | text | Source / feed name |
| Internal external | chip: Internal, External | Internal/External |
| Market | text | Market |
| Refresh frequency | chip: Real time, Minutes10, Hourly, Daily, Weekly, Manual | Refresh Frequency |
| Last update | 1 Oct 2026, 14:30 | Last Update |
| Freshness | text | Freshness, e.g. |
| Reliability | 1,234.5 | Reliability, percent |
| Historical correlation | 1,234.5 | Historical correlation with demand, -1..1 |
| Status | text | Status: healthy, delayed, failed or disabled for signals; candidate, validation, approved, production, monitored or retired for models |
| Missing data | 1,234 | Missing Data issues in the last 24 hours |
| Delayed data | 1,234 | Delayed Data issues in the last 24 hours |
| Outliers | 1,234 | Outliers in the last 24 hours |
| Duplicate data | text | not in the schema: `Duplicate Data` |
| Invalid values | 1,234 | Invalid Values in the last 24 hours |
| Unexpected changes | 1,234 | Unexpected Changes in the last 24 hours |
| Source failure | 1,234 | Source Failures in the last 24 hours |
| Forecast accuracy | 1,234.5 | Forecast Accuracy, percent |
| Bias | 1,234.5 | Bias, percent |
| Recommendation accuracy | 1,234.5 | Recommendation Accuracy, percent |
| Revenue performance | AED 1,234.50 | Revenue Performance attributed to the model's accepted recommendations |
| Drift | 1,234.5 | Drift: change in accuracy over the last 30 days, percent |

**The selected signal registry data** (detail panel): The pack groups this record's detail under its own headings: “Signal Status”, “Health”, “Delaye”, “Hotel Health”, “For example”, “For each signal”.

| Shows | Format | Notes |
|---|---|---|
| Signal | text | Signal name (signal rows) |
| Category | chip: Internal sales, Inventory, Weather, Nearby events, Competitor, Tourism… | Category |
| Provider | text | Provider name (vendor-neutral, data) |
| Source | text | Source / feed name |
| Internal external | chip: Internal, External | Internal/External |
| Market | text | Market |
| Refresh frequency | chip: Real time, Minutes10, Hourly, Daily, Weekly, Manual | Refresh Frequency |
| Last update | 1 Oct 2026, 14:30 | Last Update |
| Freshness | text | Freshness, e.g. |
| Reliability | 1,234.5 | Reliability, percent |
| Historical correlation | 1,234.5 | Historical correlation with demand, -1..1 |
| Status | text | Status: healthy, delayed, failed or disabled for signals; candidate, validation, approved, production, monitored or retired for models |
| Missing data | 1,234 | Missing Data issues in the last 24 hours |
| Delayed data | 1,234 | Delayed Data issues in the last 24 hours |
| Outliers | 1,234 | Outliers in the last 24 hours |
| Duplicate data | text | not in the schema: `Duplicate Data` |
| Invalid values | 1,234 | Invalid Values in the last 24 hours |
| Unexpected changes | 1,234 | Unexpected Changes in the last 24 hours |
| Source failure | 1,234 | Source Failures in the last 24 hours |
| Forecast accuracy | 1,234.5 | Forecast Accuracy, percent |
| Bias | 1,234.5 | Bias, percent |
| Recommendation accuracy | 1,234.5 | Recommendation Accuracy, percent |
| Revenue performance | AED 1,234.50 | Revenue Performance attributed to the model's accepted recommendations |
| Drift | 1,234.5 | Drift: change in accuracy over the last 30 days, percent |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Forecasting, Recommendations, Simulation, Automated Pricing. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save signal registry policy (primary button) | `setSignalRegistryPolicy` PUT `/signal-registry` | SignalRegistryEntry | SignalRegistryEntry | 422 `trustTooLow`. | gated `AI_CONFIGURE`; opens modal first |

**Data it reads**: `listSignalDataQuality` (onLoad, AI Signal Registry, Data Quality & Model Governance)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The signal registry data list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the signal registry data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No signal registry data yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the signal registry data are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `trustTooLow`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  name: Weather provider
  trust: approved
  uses:
  - forecasting
  - recommendations
  fallback: reduceConfidence
```

#### Permissions

- `listSignalDataQuality` → `PRODUCT_VIEW` (read) · staff
- `setSignalRegistryPolicy` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Forecast signal configuration defines which data sources and coverage periods the AI may use, e.g. historical sales over the last 36 months, real-time bookings and attendance history; seasonality, festivities and weather (e.g. forecast rain) are factored in. *(client request · MoM 18 Sep 2026, 4.9 AI Forecasting — Model Strategies & Signal Configuration · DI-942)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-107` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-107`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 6
- Flow F148 *Pricing Revenue Management board 6: AI Pricing Intelligence Command Center*, step 18: Works in AI Signal Registry, Data Quality & Model Governance → Govern the complete data and intelligence ecosystem behind AI pricing. This is critical. Without this screen, Development team could connect many external sources without giving TICVAI proper control …

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-107?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save signal registry policy.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `PRODUCT_VIEW`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decidePricingRecommendation": {"method":"POST","path":"/recommendation-review-decision/{recommendationId}/decision","contract":"catalogue","summary":"Record a human decision on an AI pricing recommendation","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingRecommendationDecisionInput","responds":"PricingRecommendationDecision"},
"listCompetitorPricingMarket": {"method":"GET","path":"/competitor-pricing-market","contract":"catalogue","summary":"Competitor Pricing & Market Position Intelligence","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"competitor","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"comparableTicvaiProduct","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInternalDemandBooking": {"method":"GET","path":"/internal-demand-booking","contract":"catalogue","summary":"Internal Demand & Booking Signal Hub","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"granularity","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"compareTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMarketTourismHoliday": {"method":"GET","path":"/market-tourism-holiday","contract":"catalogue","summary":"Market, Tourism, Holiday & Contextual Signal Hub","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":false},{"name":"signalType","in":"query","required":false},{"name":"geography","in":"query","required":false},{"name":"active","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listNearbyEventExhibition": {"method":"GET","path":"/nearby-event-exhibition","contract":"catalogue","summary":"Nearby Event, Exhibition & Local Demand Intelligence","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ticvaiVenue","in":"query","required":false},{"name":"eventType","in":"query","required":false},{"name":"radiusKm","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceElasticityRevenue": {"method":"GET","path":"/price-elasticity-revenue","contract":"catalogue","summary":"Price Elasticity & Revenue Response Intelligence","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"weekdayWeekend","in":"query","required":false},{"name":"peakOffPeak","in":"query","required":false},{"name":"eventProximity","in":"query","required":false},{"name":"season","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricing": {"method":"GET","path":"/pricing","contract":"catalogue","summary":"AI Pricing Intelligence Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"urgency","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"minConfidence","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingRecommendationExplainability": {"method":"GET","path":"/pricing-recommendation-explainability","contract":"catalogue","summary":"AI Pricing Recommendation & Explainability Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"reviewOutcome","in":"query","required":false},{"name":"minConfidence","in":"query","required":false},{"name":"recommendationType","in":"query","required":false},{"name":"objective","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSignalDataQuality": {"method":"GET","path":"/signal-data-quality","contract":"catalogue","summary":"AI Signal Registry, Data Quality & Model Governance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"registryKind","in":"query","required":false},{"name":"internalExternal","in":"query","required":false},{"name":"trustLevel","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWeatherDemandImpact": {"method":"GET","path":"/weather-demand-impact","contract":"catalogue","summary":"Weather Intelligence & Demand Impact Configuration","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"venueExposure","in":"query","required":false},{"name":"forecastHorizon","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setDemandSignalConfiguration": {"method":"PUT","path":"/demand-signals/{signalId}","contract":"catalogue","summary":"Enter a calendar signal or configure how a demand signal is used","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DemandSignal","responds":"DemandSignal"},
"setSignalRegistryPolicy": {"method":"PUT","path":"/signal-registry","contract":"catalogue","summary":"Register a signal or model and set how far AI may trust it","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SignalRegistryEntry","responds":"SignalRegistryEntry"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"AiPricingIntelligenceCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on AI Pricing Intelligence Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeAiRecommendations":{"type":"integer","description":"Active AI Recommendations"},"highPriorityOpportunities":{"type":"integer","description":"High-Priority Opportunities"},"estimatedRevenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Revenue Opportunity"},"demandSurgesDetected":{"type":"integer","description":"Demand Surges Detected: granules forecast materially above baseline"},"demandRisksDetected":{"type":"integer","description":"Demand Risks Detected: granules forecast materially below baseline"},"externalSignalsActive":{"type":"integer","description":"External Signals Active"},"nearbyEventsDetected":{"type":"integer","description":"Nearby Events Detected within the configured monitoring radius"},"weatherImpacts":{"type":"integer","description":"Weather Impacts"},"competitorMovements":{"type":"integer","description":"Competitor Movements"},"forecastAccuracy":{"type":"number","description":"Forecast Accuracy (100 - MAPE over the last 30 days (decided 29 September, readiness close-out)), percent"},"averageAiConfidence":{"type":"number","description":"Average AI Confidence across active recommendations, percent"},"dataQualityIssues":{"type":"integer","description":"Data Quality Issues"},"aiSummary":{"type":"array","items":{"type":"string"},"description":"AI Summary (pack p.95), e.g. demand forecast 19% above baseline and its drivers. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"}}},
"AiPricingIntelligenceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Pricing Intelligence Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"productEvent":{"type":"string","description":"Product/Event name the opportunity applies to"},"venue":{"type":"string","description":"Venue name"},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended Price"},"adjustment":{"type":"number","description":"Adjustment % from current to recommended price, percent"},"demandForecast":{"type":"integer","description":"Demand Forecast: forecast demand (admissions) for the period"},"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"confidence":{"type":"number","description":"AI confidence in the recommendation, 0-100, percent"},"risk":{"type":"string","description":"Risk of acting on the recommendation","enum":["low","medium","high"]},"urgency":{"type":"string","description":"Urgency (time to event and velocity)","enum":["low","medium","high","critical"]},"recommendationId":{"type":"string","description":"Recommendation id; drill-down key into listPricingRecommendationExplainability"},"drivers":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category behind the driver"},"direction":{"type":"string","enum":["up","down"],"description":"Whether the driver pushes the price up or down"},"explanation":{"type":"string","description":"Business-language evidence, e.g. booking velocity 31% above forecast"}}},"description":"Primary drivers of the recommendation (pack's up/down driver list); explanatory, not literal model weights"}}},
"AiPricingRecommendationExplainabilityCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Pricing Recommendation & Explainability Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"expectedRevenueImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected Revenue Impact"},"expectedOccupancy":{"type":"number","description":"Expected Occupancy, percent"},"confidence":{"type":"number","description":"Overall confidence, percent"},"recommendationId":{"type":"string","description":"Recommendation id"},"productEvent":{"type":"string","description":"Product/event/performance the card applies to"},"venue":{"type":"string","description":"Venue"},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"AI Recommended Price"},"adjustmentPercent":{"type":"number","description":"Change from current price, percent"},"demandImpact":{"type":"number","description":"Demand Impact, percent"},"drivers":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","conversionRate","other"],"description":"Signal category behind the driver; `conversionRate` (carts reaching the price against orders placed) added 29 September for `objective` `conversion` (build pass, group G2; 8.5.37)"},"direction":{"type":"string","enum":["up","down"],"description":"Whether the driver pushes the price up or down"},"explanation":{"type":"string","description":"Business-language evidence, e.g. booking velocity 31% above forecast"}}},"description":"Primary drivers of the recommendation (pack's up/down driver list); explanatory, not literal model weights"},"counterfactuals":{"type":"array","items":{"type":"object","properties":{"condition":{"type":"string","description":"e.g. if the nearby exhibition were not occurring"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price the model would recommend then"}}},"description":"Counterfactual Explanation"},"confidenceBreakdown":{"type":"object","properties":{"dataQuality":{"type":"number","description":"Data Quality, percent"},"forecastConfidence":{"type":"number","description":"Forecast Confidence, percent"},"elasticityConfidence":{"type":"number","description":"Elasticity Confidence, percent"},"externalSignalConfidence":{"type":"number","description":"External Signal Confidence, percent"}},"description":"Confidence Breakdown"},"explanation":{"type":"string","description":"Natural-language explanation in business language (advisory)","nullable":true},"reviewOutcome":{"type":"string","description":"Where the human decision on the card stands; every card starts pending (decided 29 September, readiness close-out)","enum":["pending","accepted","rejected","modified","ignored","sentToSimulation","sentForApproval"]},"modelVersion":{"type":"string","description":"Model version (auditability chain)"},"generatedAt":{"type":"string","description":"When the recommendation was generated","format":"date-time"},"priceCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The price (seat) category the card is for, `PricingRecommendation.priceCategoryId`; null for a product priced without categories (29 September, build pass, group G2; 1.4.27)"},"priceCategory":{"type":"string","nullable":true,"description":"The price category's name, for the card"},"recommendationType":{"type":"string","enum":["standard","earlyBird","lastMinute","volumeDiscount","conversion"],"description":"`PricingRecommendation.recommendationType` (29 September, build pass, group G2; 8.5.31 to 8.5.33, 8.5.37)"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"quantityTier":{"type":"object","nullable":true,"properties":{"minQuantity":{"type":"integer"},"maxQuantity":{"type":"integer","nullable":true}}},"objective":{"type":"string","enum":["revenue","occupancy","conversion"]}}},
"AiSignalRegistryDataQualityModelGovernanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Signal Registry, Data Quality & Model Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"signal":{"type":"string","description":"Signal name (signal rows)","nullable":true},"category":{"type":"string","description":"Category","enum":["internalSales","inventory","weather","nearbyEvents","competitor","tourism","calendar","transport","market","other"]},"provider":{"type":"string","description":"Provider name (vendor-neutral, data)","nullable":true},"source":{"type":"string","description":"Source / feed name","nullable":true},"internalExternal":{"type":"string","description":"Internal/External","enum":["internal","external"]},"market":{"type":"string","description":"Market","nullable":true},"refreshFrequency":{"type":"string","description":"Refresh Frequency","enum":["realTime","minutes10","hourly","daily","weekly","manual"]},"lastUpdate":{"type":"string","description":"Last Update","format":"date-time","nullable":true},"freshness":{"type":"string","description":"Freshness, e.g. live, 10 min, 8 hr","nullable":true},"reliability":{"type":"number","description":"Reliability, percent"},"historicalCorrelation":{"type":"number","description":"Historical correlation with demand, -1..1","nullable":true},"status":{"type":"string","description":"Status: healthy, delayed, failed or disabled for signals; candidate, validation, approved, production, monitored or retired for models"},"missingData":{"type":"integer","description":"Missing Data issues in the last 24 hours"},"delayedData":{"type":"integer","description":"Delayed Data issues in the last 24 hours"},"outliers":{"type":"integer","description":"Outliers in the last 24 hours"},"invalidValues":{"type":"integer","description":"Invalid Values in the last 24 hours"},"unexpectedChanges":{"type":"integer","description":"Unexpected Changes in the last 24 hours"},"sourceFailure":{"type":"integer","description":"Source Failures in the last 24 hours"},"modelName":{"type":"string","description":"Model Name (model rows)","nullable":true},"version":{"type":"string","description":"Version (model rows)","nullable":true},"purpose":{"type":"string","description":"Purpose (model rows)","nullable":true},"deploymentDate":{"type":"string","description":"Deployment Date","format":"date","nullable":true},"trainingWindow":{"type":"string","description":"Training Window, e.g. 24 months to 2026-08-31","nullable":true},"validationResult":{"type":"string","description":"Validation Result summary","nullable":true},"owner":{"type":"string","description":"Owner (user id)","nullable":true},"forecastAccuracy":{"type":"number","description":"Forecast Accuracy, percent"},"bias":{"type":"number","description":"Bias, percent"},"recommendationAccuracy":{"type":"number","description":"Recommendation Accuracy, percent"},"revenuePerformance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Performance attributed to the model's accepted recommendations"},"drift":{"type":"number","description":"Drift: change in accuracy over the last 30 days, percent"},"registryId":{"type":"string","description":"Registry entry id"},"registryKind":{"type":"string","description":"Signal or model row","enum":["signal","model"]},"duplicateData":{"type":"integer","description":"Duplicate Data issues in the last 24 hours"},"trustLevel":{"type":"string","description":"Signal Trust; external signals default advisoryOnly (decided 29 September, readiness close-out)","enum":["approved","experimental","advisoryOnly","blocked"]},"aiUsePermissions":{"type":"array","items":{"type":"string","enum":["forecasting","recommendations","simulation","automatedPricing"]},"description":"AI Use Permission; automatedPricing is never granted by default (decided 29 September, readiness close-out)"},"fallbackPolicy":{"type":"string","description":"Fallback Policy; default reduceConfidence (decided 29 September, readiness close-out)","enum":["useHistoricalValue","ignore","substitute","reduceConfidence","stopAiRecommendation"]}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CompetitorPricingMarketPositionIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Competitor Pricing & Market Position Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"competitor":{"type":"string","description":"Competitor name"},"market":{"type":"string","description":"Market"},"venueProduct":{"type":"string","description":"Competitor venue/product"},"comparableTicvaiProduct":{"type":"string","description":"Comparable TICVAI product id"},"source":{"type":"string","description":"Source name (vendor-neutral: website, feed or partner, as data)"},"currency":{"type":"string","description":"Currency, ISO 4217"},"collectionMethod":{"type":"string","description":"Collection Method (decided 29 September, readiness close-out)","enum":["manualEntry","dataFeed","publishedWebsite","partnerSupplied"]},"refreshFrequency":{"type":"string","description":"Refresh Frequency","enum":["realTime","hourly","daily","weekly","manual"]},"reliability":{"type":"number","description":"Reliability of the source, percent"},"publishedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Published Price"},"promotionalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotional Price"},"weekendPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Weekend Price"},"peakPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Peak Price"},"residentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resident Price"},"memberPriceWherePubliclyAvailable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Member Price where publicly available"},"availability":{"type":"string","description":"Availability as published","enum":["available","limited","soldOut","unknown"]},"date":{"type":"string","description":"Date the price applies to","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"observationId":{"type":"string","description":"Observation id"},"observedAt":{"type":"string","description":"When the price was collected","format":"date-time"},"marketMedianPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Market median price for the comparable set"},"positionVsMedian":{"type":"number","description":"TICVAI position against the market median (-9.1 = below), percent"},"movementPercent":{"type":"number","description":"Competitor Movement: change against the previous observation, percent"},"historicalCorrelation":{"type":"object","properties":{"demand":{"type":"number","description":"Correlation with TICVAI demand, -1..1"},"conversion":{"type":"number","description":"Correlation with TICVAI conversion, -1..1"},"priceSensitivity":{"type":"number","description":"Correlation with TICVAI price sensitivity, -1..1"}},"description":"Historical Correlation of competitor changes with TICVAI outcomes"},"comparabilityApproved":{"type":"boolean","description":"An administrator confirmed the products are genuinely comparable"},"sourceApproved":{"type":"boolean","description":"Source approved as legally permissible; unapproved sources are ignored by AI"}}},
"DemandSignal": {"type":"object","x-ticvai-persistence":"catalogue.demand_signal","description":"**An external or calendar signal that moves demand** (29 September, data model DM3). Merges weather (ADM-101), nearby events (ADM-102), competitor prices (ADM-103), tourism, holiday and market signals (ADM-104) and the tenant's special calendar (Ramadan, Eid, school breaks) used by temporal rules. `signalKind` says which; the readings specific to a kind are in `reading`, and a venue's sensitivity settings in `configuration`. A signal informs forecasts and recommendations; it never sets a price.","required":["id","scopePath","signalKind","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"signalKind":{"type":"string","enum":["weather","nearbyEvent","competitorPrice","calendar","tourism","transport","market"]},"signalType":{"type":"string","maxLength":60,"nullable":true,"description":"E.g. `publicHoliday`, `ramadan`, an event type, a weather condition."},"name":{"type":"string","maxLength":200,"nullable":true},"source":{"type":"string","maxLength":100,"description":"Provider, feed or `tenant` for manual entries."},"venueId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Competitor observations: the comparable TICVAI product."},"geography":{"type":"string","maxLength":100,"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"periodStart":{"type":"string","format":"date-time","nullable":true},"periodEnd":{"type":"string","format":"date-time","nullable":true},"currentValue":{"type":"number","nullable":true},"unit":{"type":"string","maxLength":20,"nullable":true},"reading":{"type":"object","additionalProperties":true,"nullable":true,"description":"Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices."},"configuration":{"type":"object","additionalProperties":true,"nullable":true,"description":"Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`."},"weight":{"type":"number","nullable":true},"reliability":{"type":"number","nullable":true,"minimum":0,"maximum":1},"historicalCorrelation":{"type":"number","nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"impactMinPercent":{"type":"number","nullable":true},"impactMaxPercent":{"type":"number","nullable":true},"refreshFrequency":{"type":"string","enum":["realTime","hourly","daily","weekly","manual",null],"nullable":true},"isApproved":{"type":"boolean","default":false,"description":"Competitor sources and comparability approved for use."},"isActive":{"type":"boolean","default":true},"observedAt":{"type":"string","format":"date-time","nullable":true},"lastUpdatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"InternalDemandBookingSignalHubView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Internal Demand & Booking Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketsSold":{"type":"integer","description":"Tickets Sold"},"orders":{"type":"integer","description":"Orders"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"averageSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Average Selling Price"},"conversionRate":{"type":"number","description":"Conversion Rate, percent"},"cartAbandonment":{"type":"number","description":"Cart Abandonment rate, percent"},"searchToPurchaseConversion":{"type":"number","description":"Search-to-Purchase Conversion, percent"},"capacity":{"type":"integer","description":"Capacity"},"remainingInventory":{"type":"integer","description":"Remaining Inventory (units)"},"availability":{"type":"number","description":"Availability: remaining inventory as a share of capacity, percent"},"occupancy":{"type":"number","description":"Occupancy, percent"},"seatZoneAvailability":{"type":"array","items":{"type":"object","properties":{"zone":{"type":"string","description":"Seat zone / section"},"available":{"type":"integer","description":"Seats available"}}},"description":"Seat/Zone Availability; empty for unseated products"},"salesPerHour":{"type":"number","description":"Sales per Hour (tickets)"},"salesPerDay":{"type":"number","description":"Sales per Day (tickets)"},"bookingVelocity":{"type":"number","description":"Booking Velocity against forecast (+31 = 31% above), percent"},"revenueVelocity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Velocity: revenue per hour over the last hour"},"accelerationDeceleration":{"type":"number","description":"Acceleration/Deceleration: change in booking velocity against the previous window, percent"},"repeatPurchase":{"type":"number","description":"Repeat Purchase rate, percent"},"leadTime":{"type":"number","description":"Lead Time: average days between purchase and visit"},"cancellation":{"type":"integer","description":"Cancellations"},"noShow":{"type":"integer","description":"No-Shows"},"reschedule":{"type":"integer","description":"Reschedules"},"granularity":{"type":"string","description":"Level of this row in the signal granularity hierarchy (pack p.97)","enum":["tenant","market","venue","event","performance","product","priceCategory","channel","timeslot"]},"venue":{"type":"string","description":"Venue id"},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"product":{"type":"string","description":"Product id","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"date":{"type":"string","description":"Business date","format":"date"},"refunds":{"type":"integer","description":"Refunds"},"customerMix":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["segment","membership","geography"],"description":"Customer dimension"},"value":{"type":"string","description":"Segment / membership tier / geography"},"share":{"type":"number","description":"Share of tickets sold, percent"}}},"description":"Customer signals: Segment, Membership, Geography mix"},"comparison":{"type":"object","properties":{"basis":{"type":"string","enum":["yesterday","previousWeek","sameDayLastYear","previousEvent","similarEvent","forecastBaseline"],"description":"Comparison basis (compareTo)"},"ticketsSoldChange":{"type":"number","description":"Change in tickets sold, percent"},"revenueChange":{"type":"number","description":"Change in revenue, percent"},"conversionChange":{"type":"number","description":"Change in conversion, percentage points"},"bookingVelocityChange":{"type":"number","description":"Change in booking velocity, percent"}},"description":"Historical Comparison against the basis chosen in compareTo"},"anomalies":{"type":"array","items":{"type":"string"},"description":"Anomaly Detection, e.g. booking velocity increased 47% during the last 90 minutes. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"},"lastUpdated":{"type":"string","description":"When the signal was last refreshed","format":"date-time"}}},
"MarketTourismHolidayContextualSignalHubView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Market, Tourism, Holiday & Contextual Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"source":{"type":"string","description":"Source name (vendor-neutral)"},"geography":{"type":"string","description":"Geography the signal covers"},"refreshFrequency":{"type":"string","description":"Refresh Frequency","enum":["realTime","hourly","daily","weekly","manual"]},"weight":{"type":"number","description":"Weight given to the signal in forecasting, 0-1; default 0.5 (decided 29 September, readiness close-out)"},"reliability":{"type":"number","description":"Reliability, percent"},"historicalCorrelation":{"type":"number","description":"Historical correlation with venue demand, -1..1"},"active":{"type":"boolean","description":"Active/Inactive; new external sources start inactive (decided 29 September, readiness close-out)"},"currentEstimatedImpact":{"type":"number","description":"Current Estimated Impact on venue demand, percent"},"signalId":{"type":"string","description":"Signal id"},"category":{"type":"string","description":"Signal Category","enum":["calendar","tourism","transport","market"]},"signalType":{"type":"string","description":"Signal","enum":["publicHoliday","schoolHoliday","ramadan","eid","christmas","newYear","longWeekend","visitorArrivals","tourismDemand","hotelOccupancy","hotelRates","destinationDemand","flightArrivals","airportPassengerVolume","publicTransportDemand","trafficConditions","consumerDemandTrends","searchTrends","destinationPopularity","marketActivity"]},"currentValue":{"type":"number","description":"Current reading, e.g. hotel occupancy 92","nullable":true},"unit":{"type":"string","description":"Unit of currentValue (percent, count, currency...)","nullable":true},"periodStart":{"type":"string","description":"Calendar signals: first day","format":"date","nullable":true},"periodEnd":{"type":"string","description":"Calendar signals: last day","format":"date","nullable":true},"lastUpdated":{"type":"string","description":"Last refresh","format":"date-time"}}},
"NearbyEventExhibitionLocalDemandIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Nearby Event, Exhibition & Local Demand Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventName":{"type":"string","description":"Event Name"},"venue":{"type":"string","description":"External venue hosting the event"},"location":{"type":"string","description":"Location (address or area)"},"distanceKm":{"type":"number","description":"Distance from the TICVAI venue, km"},"expectedAttendance":{"type":"integer","description":"Expected Attendance"},"eventType":{"type":"string","description":"Event Type","enum":["exhibition","conference","concert","sportsEvent","festival","tradeShow","convention","publicCelebration","majorAttractionEvent","schoolEvent","customLocalEvent"]},"audienceType":{"type":"string","description":"Audience Type (decided 29 September, readiness close-out)","enum":["family","business","youth","general","tourist","other"]},"source":{"type":"string","description":"Source: name of the event feed or 'manual' (vendor-neutral)"},"confidence":{"type":"number","description":"Confidence that the event and its attendance are accurate, percent"},"externalEventId":{"type":"string","description":"External event id"},"ticvaiVenue":{"type":"string","description":"TICVAI venue whose monitoring radius the event falls in"},"monitoringRadiusKm":{"type":"number","description":"Geographic Radius configured for that venue: 1, 3, 5, 10 or custom km; default 5 (decided 29 September, readiness close-out)"},"startDate":{"type":"string","description":"Start date","format":"date"},"endDate":{"type":"string","description":"End date","format":"date"},"startTime":{"type":"string","description":"Start time (HH:mm)","nullable":true},"endTime":{"type":"string","description":"End time (HH:mm)","nullable":true},"historicalCorrelation":{"type":"number","description":"Historical correlation: demand change seen at the venue for similar past events, percent"},"predictedImpactMin":{"type":"number","description":"Predicted demand impact, low end, percent"},"predictedImpactMax":{"type":"number","description":"Predicted demand impact, high end, percent"},"impactWindows":{"type":"array","items":{"type":"string","enum":["beforeEvent","duringEvent","lunchPeriod","afterEvent","evening","followingDay"]},"description":"Timing Intelligence: when the impact is expected"},"audienceMatch":{"type":"string","description":"Audience Matching between the event and the TICVAI venue","enum":["low","medium","high"]}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceElasticityRevenueResponseIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Elasticity & Revenue Response Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price tested on the curve"},"demand":{"type":"integer","description":"Expected demand at this price"},"conversion":{"type":"number","description":"Expected conversion, percent"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected revenue"},"margin":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected margin"},"occupancy":{"type":"number","description":"Expected occupancy, percent"},"customerSegment":{"type":"string","description":"Customer segment (e.g. tourist, resident, family, VIP)","nullable":true},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"time":{"type":"string","description":"Time context of the curve: weekday/weekend, peak/off-peak or season label"},"product":{"type":"string","description":"Product id"},"venue":{"type":"string","description":"Venue id"},"priceSensitivity":{"type":"string","description":"Price sensitivity of the segment","enum":["low","medium","high"]},"elasticityCoefficient":{"type":"number","description":"Estimated price elasticity of demand (negative)","nullable":true},"elasticityConfidence":{"type":"string","description":"Elasticity Confidence","enum":["low","medium","high"]},"inRecommendedRevenueZone":{"type":"boolean","description":"Price lies inside the Recommended Revenue Zone"},"revenueZoneMin":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Optimal revenue range, low end"},"revenueZoneMax":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Optimal revenue range, high end"}}},
"PricingRecommendationDecision": {"type":"object","x-ticvai-persistence":"catalogue.pricing_recommendation_decision","description":"**One human decision on one AI pricing recommendation** (decided 29 September, readiness close-out). New table: the queue row `AiRecommendationReviewDecisionQueueView` reads its decision fields from here. Written once by `decidePricingRecommendation` and never edited; a changed mind is a new recommendation.\n","required":["id","recommendationId","decision","decidedByPrincipalId","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"recommendationId":{"type":"string","format":"uuid","description":"A `catalogue.pricing_recommendation` (29 September, data model DM3)."},"decision":{"type":"string","enum":["accept","modify","reject","schedule","sendForApproval"]},"rejectionReason":{"type":"string","nullable":true,"enum":["commercialJudgment","brandPositioning","customerSensitivity","eventStrategy","incorrectSignal","dataConcern","other",null]},"rejectionNote":{"type":"string","nullable":true},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"humanSelectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The approvals request opened by `sendForApproval`."},"executionId":{"type":"string","nullable":true,"readOnly":true,"description":"The `createLiveDynamicPrice` execution that carried it out, once it has."},"decidedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"decidedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"PricingRecommendationDecisionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `decidePricingRecommendation` takes (decided 29 September, readiness close-out).","required":["decision"],"properties":{"decision":{"type":"string","enum":["accept","modify","reject","schedule","sendForApproval"]},"rejectionReason":{"type":"string","enum":["commercialJudgment","brandPositioning","customerSensitivity","eventStrategy","incorrectSignal","dataConcern","other"],"description":"Required for reject."},"rejectionNote":{"type":"string","maxLength":2000},"humanSelectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Required for modify; must sit inside the strategy's guardrails."},"scheduledFor":{"type":"string","format":"date-time","description":"Required for schedule; in the future."}}},
"SignalRegistryEntry": {"type":"object","x-ticvai-persistence":"catalogue.signal_registry","description":"**The registry of AI signals and models, with their trust and quality** (29 September, data model DM3). ADM-106 and ADM-118. A signal or model not `approved` for a use in `aiUsePermissions` is not used for it.","required":["id","scopePath","registryKind","name","trustLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"registryKind":{"type":"string","enum":["signal","model"]},"name":{"type":"string","maxLength":200},"category":{"type":"string","enum":["internalSales","inventory","weather","nearbyEvents","competitor","tourism","calendar","transport","market","other",null],"nullable":true},"provider":{"type":"string","maxLength":100,"nullable":true},"source":{"type":"string","maxLength":100,"nullable":true},"internalExternal":{"type":"string","enum":["internal","external",null],"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"refreshFrequency":{"type":"string","enum":["realTime","minutes10","hourly","daily","weekly","manual",null],"nullable":true},"trustLevel":{"type":"string","enum":["approved","experimental","advisoryOnly","blocked"],"default":"experimental"},"aiUsePermissions":{"type":"array","items":{"type":"string","enum":["forecasting","recommendations","simulation","automatedPricing"]}},"fallbackPolicy":{"type":"string","enum":["useHistoricalValue","ignore","substitute","reduceConfidence","stopAiRecommendation",null],"nullable":true},"status":{"type":"string","maxLength":40,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"version":{"type":"string","maxLength":40,"nullable":true,"description":"Models."},"purpose":{"type":"string","nullable":true},"deployedAt":{"type":"string","format":"date-time","nullable":true},"trainingWindow":{"type":"string","maxLength":60,"nullable":true},"validationResult":{"type":"string","nullable":true},"lastUpdateAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"qualityCounts":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Signals: `{missingData, delayedData, outliers, invalidValues, unexpectedChanges, sourceFailure, duplicateData}`."},"performance":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Models: `{forecastAccuracy, bias, recommendationAccuracy, revenuePerformance, drift}` and the per-segment learning metrics."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WeatherIntelligenceDemandImpactConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Weather Intelligence & Demand Impact Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"temperature":{"type":"number","description":"Temperature, degrees C"},"feelsLikeTemperature":{"type":"number","description":"Feels-Like Temperature, degrees C"},"rain":{"type":"number","description":"Rain, mm in the last hour"},"rainProbability":{"type":"number","description":"Rain Probability, percent"},"humidity":{"type":"number","description":"Humidity, percent"},"wind":{"type":"number","description":"Wind speed, km/h"},"visibility":{"type":"number","description":"Visibility, km"},"storm":{"type":"boolean","description":"Storm warning in force"},"extremeHeat":{"type":"boolean","description":"Extreme Heat: temperature at or above the venue's configured heat threshold"},"currentConditions":{"type":"string","description":"Current Conditions summary as reported by the source"},"hourlyForecast":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time","description":"Hour"},"temperature":{"type":"number","description":"Degrees C"},"rainProbability":{"type":"number","description":"Percent"},"conditions":{"type":"string","description":"Conditions"}}},"description":"Hourly Forecast"},"dailyForecast":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date","description":"Day"},"minTemperature":{"type":"number","description":"Degrees C"},"maxTemperature":{"type":"number","description":"Degrees C"},"rainProbability":{"type":"number","description":"Percent"},"conditions":{"type":"string","description":"Conditions"}}},"description":"Daily Forecast"},"weatherForecastConfidence":{"type":"number","description":"Weather Forecast Confidence, percent"},"estimatedDemandImpactMin":{"type":"number","description":"Estimated Demand Impact, low end of the range, percent"},"venue":{"type":"string","description":"TICVAI venue id"},"venueExposure":{"type":"string","description":"Venue Sensitivity: Indoor / Outdoor / Mixed","enum":["indoor","outdoor","mixed"]},"weatherSensitivity":{"type":"string","description":"Weather sensitivity of the venue; default medium (decided 29 September, readiness close-out)","enum":["low","medium","high"]},"airQualityIndex":{"type":"integer","description":"Air quality index where available","nullable":true},"conditionImpacts":{"type":"array","items":{"type":"object","properties":{"condition":{"type":"string","enum":["temperature","feelsLikeTemperature","rain","rainProbability","humidity","wind","visibility","storm","extremeHeat","airQuality","heavyRain","highTemperature"],"description":"Weather condition"},"threshold":{"type":"number","nullable":true,"description":"Threshold in the condition's unit, e.g. 42 (degrees C)"},"demandImpactPercent":{"type":"number","description":"Modelled demand impact, e.g. +8 indoor / -17 outdoor"}}},"description":"Weather Impact Model: condition -> demand impact rules for this venue"},"estimatedDemandImpactMax":{"type":"number","description":"Estimated Demand Impact, high end of the range, percent"},"forecastHorizon":{"type":"string","description":"Forecast Horizon","enum":["today","hours24","days3","days7","custom"]},"forecastWindowDays":{"type":"integer","description":"Configurable future window in days when forecastHorizon is custom; max 14 (decided 29 September, readiness close-out)","nullable":true},"dataFailurePolicy":{"type":"string","description":"What happens when weather data is unavailable; default reduceConfidence (decided 29 September, readiness close-out)","enum":["useLastValidSignal","useHistoricalBaseline","reduceConfidence","ignoreWeather","suspendWeatherDrivenRecommendation"]},"historicalInsights":{"type":"array","items":{"type":"string"},"description":"Historical Learning, e.g. similar weather historically gave +11% indoor demand. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"},"weatherSource":{"type":"string","description":"Name of the configured weather data source (vendor-neutral: the provider is data in the signal registry)"},"lastUpdated":{"type":"string","description":"When the source last refreshed","format":"date-time"}}}
}
```
