# WS38 — Pricing   Revenue Management board 5

**10 screens · 14 operations · 19 schemas · 4 permissions**

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
  `PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-088` | Dynamic Pricing Strategy Command Center | B | 2 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-089` | Dynamic Pricing Strategy Builder | B | 24 | 20 | 5 | 2 | 1 | 0 | — | notStarted (generated) |
| `ADM-090` | Demand, Occupancy & Availability Rule Builder | B | 0 | 20 | 6 | 5 | 0 | 0 | — | notStarted (generated) |
| `ADM-091` | Booking Velocity & Time-to-Event Rule Builder | B | 0 | 20 | 6 | 1 | 0 | 6 | — | notStarted (generated) |
| `ADM-092` | Seasonal, Calendar, Day & Timeslot Dynamic Rules | B | 26 | 20 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-093` | Channel, Customer Segment & Location Dynamic Rules | B | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-094` | Dynamic Price Bands, Ladders & Adjustment Matrix | B | 24 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-095` | Dynamic Pricing Guardrails & Commercial Protection | B | 47 | 0 | 5 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-096` | Dynamic Pricing Automation Policy & Control | B | 50 | 0 | 5 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-097` | Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-090, ADM-093 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-088` Dynamic Pricing Strategy Command Center

**Provide the central backend workspace for creating, monitoring, and managing all dynamic- pricing strategies. This should be the primary operational screen for Revenue Managers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-088 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each strategy should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/dynamic-pricing-strategy-command-center-adm-088` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **BO-528 Dynamic Pricing & AI Recommendation merged in (2 October 2026, duplicate rule; CHG-SBO-021):** the rental view of dynamic pricing is this strategy list filtered to rental resources; activate, pause, resume and retire come with it.

**Known gaps.** **The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Demand Based, Inventory Based, Booking Velocity, Timeslot, Channel, Create Strategy, Duplicate, Open …. …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The revenue manager's workspace for dynamic pricing strategies: status, scope, current price movement; activate, pause, resume, retire.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Demand Based, Inventory Based, Booking Velocity, Timeslot, Channel, Create Strategy, Duplicate, Open …. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Strategy type | select | — | Demand based · Occupancy based · Availability based · Inventory based · Booking velocity · Time to event · Seasonal · Day of week · Timeslot · Channel · Segment · Location … | `listDynamicPricingStrategy` ?strategyType |
| Status | select | — | Draft · Testing · Ready · Scheduled · Active · Paused · Frozen · Expired · Retired | `listDynamicPricingStrategy` ?status |
| Automation mode | radio group | — | Monitor · Recommend · Prepare change · Auto execute within guardrails | `listDynamicPricingStrategy` ?automationMode |
| Venue | text field | — | — | `listDynamicPricingStrategy` ?venue |
| Search | text field | — | — | `listDynamicPricingStrategy` ?search |

**Form: Transition dynamic pricing strategy** (modal, opened by *Transition dynamic pricing strategy*; *Transition dynamic pricing strategy* calls `transitionDynamicPricingStrategy`, *Cancel* sends nothing)

**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Activate · Pause · Resume · Retire | — | — | `transitionDynamicPricingStrategy` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `transitionDynamicPricingStrategy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`.

#### Outputs: what the screen shows and produces

**Shown**

**Active Strategies** (metric tile)

**Draft Strategies** (metric tile)

**Products Under Dynamic Pricing** (metric tile)

**Events Under Dynamic Pricing** (metric tile)

**Performances Under Dynamic Pricing** (metric tile)

**Rules Active** (metric tile)

**Current Price Adjustments** (metric tile)

**Prices at Maximum Guardrail** (metric tile)

**Prices at Minimum Guardrail** (metric tile)

**Rule Conflicts** (metric tile)

**Frozen Strategies** (metric tile)

**Upcoming Activations** (metric tile)

**Every dynamic pricing strategy** (data table, from `listDynamicPricingStrategy`)

| Shows | Format | Notes |
|---|---|---|
| Strategy name | text | Strategy Name |
| Strategy type | chip: Demand based, Occupancy based, Availability based, Inventory based, Booking … | Strategy Type (pack pp.75-76) |
| Venue | text | Venue |
| Base price source | text | Base price source: the Board 1 price list and rate the strategy moves from, e.g. |
| Current price | AED 1,234.50 | Current resolved dynamic price (for a single-price scope) |
| Status | text | Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired |

**The selected dynamic pricing strategy** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Strategy name | text | Strategy Name |
| Strategy type | chip: Demand based, Occupancy based, Availability based, Inventory based, Booking … | Strategy Type (pack pp.75-76) |
| Venue | text | Venue |
| Base price source | text | Base price source: the Board 1 price list and rate the strategy moves from, e.g. |
| Current price | AED 1,234.50 | Current resolved dynamic price (for a single-price scope) |
| Rule count | 1,234 | Rule Count |
| Automation mode | chip: Monitor, Recommend, Prepare change, Auto execute within guardrails | Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default |
| Status | text | Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Demand Based (primary button) | navigation or local | — | — | — | — |
| Inventory Based (secondary button) | navigation or local | — | — | — | — |
| Booking Velocity (secondary button) | navigation or local | — | — | — | — |
| Timeslot (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Create Strategy (secondary button) | navigation or local | — | — | — | — |
| Duplicate (secondary button) | navigation or local | — | — | — | — |
| Open (secondary button) | navigation or local | — | — | — | — |
| Transition dynamic pricing strategy (secondary button) | `transitionDynamicPricingStrategy` POST `/dynamic-pricing-strategies/{strategyId}/lifecycle` | inline | DynamicPricingStrategy | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`. | gated `PRICE_CONFIGURE`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Activate**: Refused while the strategy has no price ladder or rule ("strategy incomplete"), naming what is missing. *(source: contracts/spine/catalogue.yaml#transitionDynamicPricingStrategy)*

**Data it reads**: `listDynamicPricingStrategy` (onLoad, Dynamic Pricing Strategy Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-090` Demand, Occupancy & Availability Rule Builder: *Works in Demand, Occupancy & Availability Rule Builder*; calls `listDynamicPricingStrategy`
- → `ADM-091` Booking Velocity & Time-to-Event Rule Builder: *Works in Booking Velocity & Time-to-Event Rule Builder*; calls `listDynamicPricingStrategy`
- → `ADM-092` Seasonal, Calendar, Day & Timeslot Dynamic Rules: *Works in Seasonal, Calendar, Day & Timeslot Dynamic Rules*; calls `listDynamicPricingStrategy`
- → `ADM-093` Channel, Customer Segment & Location Dynamic Rules: *Works in Channel, Customer Segment & Location Dynamic Rules*; calls `listDynamicPricingStrategy`
- → `ADM-095` Dynamic Pricing Guardrails & Commercial Protection: *Works in Dynamic Pricing Guardrails & Commercial Protection*; calls `listDynamicPricingStrategy`
- → `ADM-096` Dynamic Pricing Automation Policy & Control: *Works in Dynamic Pricing Automation Policy & Control*; calls `listDynamicPricingStrategy`
- → `ADM-097` Rule Priority, Conflict Resolution & Dynamic Pricing Test Console: *Works in Rule Priority, Conflict Resolution & Dynamic Pricing Test Console*; calls `listDynamicPricingStrategy`
- → `BO-441` Price Priority & Conflict Rules: *Works in Rule Priority, Conflict Resolution & Dynamic Pricing Test Console*; calls `listDynamicPricingStrategy`
- → `ADM-089` Dynamic Pricing Strategy Builder: *Works in Dynamic Pricing Strategy Builder*; carries `strategyId`; calls `listDynamicPricingStrategy`
- → `ADM-094` Dynamic Price Bands, Ladders & Adjustment Matrix: *Works in Dynamic Price Bands, Ladders & Adjustment Matrix*; carries `strategyId`; calls `listDynamicPricingStrategy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing strategy list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing strategy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic pricing strategy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `illegalTransition`.; 422 `strategyIncomplete`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strategies:
- code: WKND-OCC
  name: Weekend occupancy
  type: occupancyBased
  status: active
```

#### Permissions

- `listDynamicPricingStrategy` → `PRODUCT_VIEW` (read) · staff
- `transitionDynamicPricingStrategy` → `PRICE_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-088` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-088`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 1: Opens Dynamic Pricing Strategy Command Center → Provide the central backend workspace for creating, monitoring, and managing all dynamic- pricing strategies. This should be the primary operational screen for Revenue Managers.
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F147 branch at step 1 (expected): when Nothing has been set up on Dynamic Pricing Strategy Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F147 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-088?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Demand Based, Inventory Based, Booking Velocity, Timeslot, Channel, Create Strategy, Duplicate, Open, Transition dynamic pricing strategy.
- [ ] Every transition is wired: `BO-100`, `ADM-090`, `ADM-091`, `ADM-092`, `ADM-093`, `ADM-095`, `ADM-096`, `ADM-097`, `BO-441`, `ADM-089`, `ADM-094`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-089` Dynamic Pricing Strategy Builder

**Create the master dynamic-pricing strategy and define what commercial objects it controls.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-089 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether a strategy) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/dynamic-pricing-strategy-builder-adm-089` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Create a dynamic pricing strategy and what it controls: type, scope (product, family, event, performances, venue, slots, price categories), base price source, evaluation frequency, how it combines with others, effective dates.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Owner, market, venue, product and event are strings in the builder, while the strategy record carries ids. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setDynamicPricingStrategy, transitionDynamicPricingStrategy and nothing that returns the … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Strategy Name | select field | — | — | — | — | — | — |
| Strategy Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Strategy Type | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Timeslot | select field | — | — | — | — | — | — |
| Price Category | select field | — | — | — | — | — | — |
| Base Price Source | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Evaluation Frequency | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Operates Independently | select field | — | — | — | — | — | — |
| Can Combine with Other Strategies | text field | — | — | — | — | — | — |
| Has Exclusive Control | select field | — | — | — | — | — | — |
| Acts as Fallback | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Strategy type | select | — | Demand based · Occupancy based · Availability based · Inventory based · Booking velocity · Time to event · Seasonal · Day of week · Timeslot · Channel · Segment · Location … | `listDynamicPricingStrategy` ?strategyType |
| Status | select | — | Draft · Testing · Ready · Scheduled · Active · Paused · Frozen · Expired · Retired | `listDynamicPricingStrategy` ?status |
| Automation mode | radio group | — | Monitor · Recommend · Prepare change · Auto execute within guardrails | `listDynamicPricingStrategy` ?automationMode |
| Venue | text field | — | — | `listDynamicPricingStrategy` ?venue |
| Search | text field | — | — | `listDynamicPricingStrategy` ?search |

**Form: Transition dynamic pricing strategy** (modal, opened by *Transition dynamic pricing strategy*; *Transition dynamic pricing strategy* calls `transitionDynamicPricingStrategy`, *Cancel* sends nothing)

**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Activate · Pause · Resume · Retire | — | — | `transitionDynamicPricingStrategy` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `transitionDynamicPricingStrategy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scope**: Scope type first, then the matching picker. *(source: contracts/spine/catalogue.yaml#setDynamicPricingStrategy)*

#### Outputs: what the screen shows and produces

**Shown**

**Strategies** (detail panel, from `listDynamicPricingStrategy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Strategy | text | Strategy ID |
| Strategy name | text | Strategy Name |
| Strategy type | chip: Demand based, Occupancy based, Availability based, Inventory based, Booking … | Strategy Type (pack pp.75-76) |
| Product event | text | Product or event the strategy controls |
| Venue | text | Venue |
| Base price source | text | Base price source: the Board 1 price list and rate the strategy moves from, e.g. |
| Current price | AED 1,234.50 | Current resolved dynamic price (for a single-price scope) |
| Adjustment range | grouped details | Adjustment range allowed by the strategy |
| Min percent | 1,234.5 | Lowest adjustment from base, percent |
| Max percent | 1,234.5 | Highest adjustment from base, percent |
| Rule count | 1,234 | Rule Count |
| Effective period | grouped details | Effective period |
| From | 1 Oct 2026, 14:30 | Effective from |
| To | 1 Oct 2026, 14:30 | Effective to; empty for open-ended |
| Automation mode | chip: Monitor, Recommend, Prepare change, Auto execute within guardrails | Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default |
| Status | text | Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired |
| Owner | text | Owner |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Transition dynamic pricing strategy (secondary button) | `transitionDynamicPricingStrategy` POST `/dynamic-pricing-strategies/{strategyId}/lifecycle` | inline | DynamicPricingStrategy | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDynamicPricingStrategy` (onLoad, The dynamic pricing strategies, to open one in the builder)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `setDynamicPricingStrategy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing strategy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing strategy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `illegalTransition`.; 422 `strategyIncomplete`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strategy:
  name: Festival early bird
  type: timeToEvent
  scope: event
  event: Dune Nights Festival 2026
  frequency: daily
```

#### Permissions

- `setDynamicPricingStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `transitionDynamicPricingStrategy` → `PRICE_CONFIGURE` (configure) · staff
- `listDynamicPricingStrategy` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.1 | System shall support dynamic ticket pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPricingStrategy` |
| 21.11.1 | Dynamic Seat Pricing | Seat Management & Venue Mapping | CONTRACTED | `setDynamicPricingStrategy` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-089` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-089`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 2: Works in Dynamic Pricing Strategy Builder → Create the master dynamic-pricing strategy and define what commercial objects it controls.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-089?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Transition dynamic pricing strategy.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-090` Demand, Occupancy & Availability Rule Builder

**Configure price movements driven by actual demand and capacity consumption. This directly covers the fundamental matrix requirements for: Demand-Based Pricing Occupancy-Based Pricing Availability-Based Pricing Inventory-Based Pricing**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-090 |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/demand-occupancy-availability-rule-builder-adm-090` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules that move a price with occupancy, remaining inventory, availability or a demand index, as tiers of a threshold matrix with hysteresis (exit offset), a minimum duration and a cooldown, inside a strategy and within the guardrails of ADM-095.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setDemandOccupancyAvailability and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **tiers**: Non-overlapping bands (0-50% no change, 50-75% +10%, 75-90% +20%, over 90% +30%) drawn as a stepped chart above the table. *(source: contracts/spine/catalogue.yaml#setDemandOccupancyAvailability / DI-600)*
- **demandIndexDefinition**: Required only when the input metric is current demand; the pack requires the formula to be stated. *(source: contracts/spine/catalogue.yaml#setDemandOccupancyAvailability)*
- **exit offset, minimum duration, cooldown**: Defaults 2, 15 minutes and 60 minutes, shown as such. *(source: contracts/spine/catalogue.yaml#setDemandOccupancyAvailability)*

#### Outputs: what the screen shows and produces

**Shown**

**Dynamic rules** (data table, from `listDynamicPriceRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Pricing rule code | text | — |
| Name | text | — |
| Product | the name it points at, never the id | — |
| Price list | the name it points at, never the id | — |
| Channel | the name it points at, never the id | — |
| Priority | 1,234 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Dynamic pricing strategy | the name it points at, never the id | The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). |
| Rule type | text | Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`. |
| Input metric | text | — |
| Condition logic | chip: All, Any | — |
| Cooldown minutes | 1,234 | — |
| Minimum duration minutes | 1,234 | — |
| Exit threshold offset | 1,234.5 | — |
| Range min percent | 1,234.5 | — |
| Range max percent | 1,234.5 | — |
| Is protected | yes / no (icon or chip) | A protected segment or channel: dynamic adjustments never apply. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDynamicPriceRules` (onLoad, The dynamic price rules already in force)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `setDemandOccupancyAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demand occupancy availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demand occupancy availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demand occupancy availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demand occupancy availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-095`: Show the guardrails in force for the strategy beside the tiers.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Weekend occupancy uplift
  kind: occupancy
  metric: occupancyPercent
  tiers:
  - '50-75%: +10%'
  - '75-90%: +20%'
  - '90-100%: +30%'
  cooldownMinutes: 60
  priority: 2
```

#### Permissions

- `setDemandOccupancyAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `listDynamicPriceRules` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.2 | System shall support demand-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDemandOccupancyAvailability` |
| 8.5.3 | System shall support occupancy-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDemandOccupancyAvailability` |
| 8.5.4 | System shall support availability-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDemandOccupancyAvailability` |
| 8.5.12 | System shall support inventory-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDemandOccupancyAvailability` |
| 2.1.23 | POS shall retrieve real-time prices from the Dynamic Pricing Engine based on date, timeslot, demand, capacity, promotions, customer segment, and channel. | Ticketing Sales | CONTRACTED | `listDynamicPriceRules` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-090` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-090`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 4: Works in Demand, Occupancy & Availability Rule Builder → Configure price movements driven by actual demand and capacity consumption. This directly covers the fundamental matrix requirements for: Demand-Based Pricing Occupancy-Based Pricing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-090?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-091` Booking Velocity & Time-to-Event Rule Builder

**Control price movement based on how quickly inventory is selling and how much time remains before the event or visit date. This is critical because occupancy alone is insufficient for effective revenue management.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-091 |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/booking-velocity-time-to-event-rule-builder-adm-091` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Sales per Hour, Sales per Day, Sales per Week, Current Booking Pace, Expected Booking Pace, Historical … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Price movement from booking pace against expectation and from time remaining before the visit: early-bird phases, last-minute, decay and escalation. Pace is measured against a configured target until a historical booking curve exists.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Sales per Hour, Sales per Day, Sales per Week, Current Booking Pace, Expected Booking Pace, Historical Booking Curve, Remaining Inventory. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setBookingVelocityTime and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **expectedPaceSource**: Configured target (with expected sales per day) by default; historical curve offered only when one exists. *(source: contracts/spine/catalogue.yaml#setBookingVelocityTime)*
- **timeToEventSchedule**: A timeline of steps ("more than 60 days: -20% for the first 200; 30-60 days: -10% for the next 100; then base") matching the client's early-bird example with quota per phase. *(source: contracts/spine/catalogue.yaml#setBookingVelocityTime / DI-600)*
- **conditionLogic**: All by default, Any as the alternative, shown as "when all of" / "when any of". *(source: contracts/spine/catalogue.yaml#setBookingVelocityTime)*

#### Outputs: what the screen shows and produces

**Shown**

**Dynamic rules** (data table, from `listDynamicPriceRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Pricing rule code | text | — |
| Name | text | — |
| Product | the name it points at, never the id | — |
| Price list | the name it points at, never the id | — |
| Channel | the name it points at, never the id | — |
| Priority | 1,234 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Dynamic pricing strategy | the name it points at, never the id | The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). |
| Rule type | text | Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`. |
| Input metric | text | — |
| Condition logic | chip: All, Any | — |
| Cooldown minutes | 1,234 | — |
| Minimum duration minutes | 1,234 | — |
| Exit threshold offset | 1,234.5 | — |
| Range min percent | 1,234.5 | — |
| Range max percent | 1,234.5 | — |
| Is protected | yes / no (icon or chip) | A protected segment or channel: dynamic adjustments never apply. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sales per Hour (primary button) | navigation or local | — | — | — | — |
| Sales per Day (secondary button) | navigation or local | — | — | — | — |
| Sales per Week (secondary button) | navigation or local | — | — | — | — |
| Current Booking Pace (secondary button) | navigation or local | — | — | — | — |
| Expected Booking Pace (secondary button) | navigation or local | — | — | — | — |
| Historical Booking Curve (secondary button) | navigation or local | — | — | — | — |
| Remaining Inventory (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDynamicPriceRules` (onLoad, The dynamic price rules already in force)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `setBookingVelocityTime`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking velocity time-to-event list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking velocity time-to-event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking velocity time-to-event yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the booking velocity time-to-event are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Festival early bird
  kind: earlyBird
  base: AED 200.00
  phases:
  - first 200 of 500 at 20% off
  - next 100 at 10% off
  - rest at base
```

#### Permissions

- `setBookingVelocityTime` → `PRODUCT_CONFIGURE` (configure) · staff
- `listDynamicPriceRules` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.23 | POS shall retrieve real-time prices from the Dynamic Pricing Engine based on date, timeslot, demand, capacity, promotions, customer segment, and channel. | Ticketing Sales | CONTRACTED | `listDynamicPriceRules` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-091` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-091`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 6: Works in Booking Velocity & Time-to-Event Rule Builder → Control price movement based on how quickly inventory is selling and how much time remains before the event or visit date. This is critical because occupancy alone is insufficient for effective …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-091?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sales per Hour, Sales per Day, Sales per Week, Current Booking Pace, Expected Booking Pace, Historical Booking Curve, Remaining Inventory.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-092` Seasonal, Calendar, Day & Timeslot Dynamic Rules

**Configure dynamic pricing behavior according to temporal commercial patterns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-092 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `signalId` (navigation) |
| Route | `/commercial/seasonal-calendar-day-timeslot-dynamic-rules-adm-092` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Dynamic pricing by temporal pattern (season, calendar, day, slot) and the calendar signals entered by hand (Ramadan, Eid, school breaks).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| View: day, week or month | select field | — | — | — | — | **Every calendar has day, week and month views, and the day view is broken into hours from the venue's day start hour** (17 September minutes, M17-03). Built on the shared calendar view … | — |
| Category | multi select | — | — | — | — | **Filtered by category, so a team sees only what is theirs** (M17-03). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Dimension | select | — | Season · Month · Week · Date range · Public holiday · School holiday · Day of week · Weekend · Time of day · Timeslot · Performance · Special date | `listSeasonalCalendarDay` ?dimension |
| Strategy | text field | — | — | `listSeasonalCalendarDay` ?strategyId |
| Season | text field | — | — | `listSeasonalCalendarDay` ?season |
| From | date picker | — | — | `listSeasonalCalendarDay` ?from |
| To | date picker | — | — | `listSeasonalCalendarDay` ?to |

**Form: Save demand signal configuration** (modal, opened by *Save demand signal configuration*; *Save demand signal configuration* calls `setDemandSignalConfiguration`, *Cancel* sends nothing)

**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

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

- **calendar signal**: Name, period, expected impact range; entered by the tenant. *(source: contracts/spine/catalogue.yaml#setDemandSignalConfiguration / DI-369)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Calendar** (calendar view, from `listSeasonalCalendarDay`): Entries of the view in force, placed by date and hour.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Season | text | Season name (e.g. |
| Month | 1,234 | Month 1-12 |
| Week | 1,234 | ISO week 1-53 |
| Date range | grouped details | Date range |
| From | 1 Oct 2026 | From |
| To | 1 Oct 2026 | To |
| Days of week | list or chips (count when long) | Days of week; saturday+sunday for weekend |
| Time of day | grouped details | Time-of-day window |
| From | text | From, HH:mm |
| To | text | To, HH:mm |
| Timeslots | list or chips (count when long) | Timeslot IDs |
| Performances | list or chips (count when long) | Performance IDs |
| Special calendar entry | text | Special-calendar entry (public/school holiday, Ramadan, Eid, custom), maintained as tenant data |
| Rule | text | Rule ID |
| Rule name | text | Rule name |
| Strategy | text | Strategy the rule belongs to |
| Dimension | chip: Season, Month, Week, Date range, Public holiday, School holiday… | Supported Dimension (pack p.81) |
| Dynamic range min percent | 1,234.5 | Dynamic range low end in percent of base, e.g. |
| Dynamic range max percent | 1,234.5 | Dynamic range high end in percent of base, e.g. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save demand signal configuration (primary button) | `setDemandSignalConfiguration` PUT `/demand-signals/{signalId}` | DemandSignal | DemandSignal | 409 `feedSignal`.; 422 `invalidPeriod`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listSeasonalCalendarDay` (onLoad, Seasonal, Calendar, Day & Timeslot Dynamic Rules)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `listSeasonalCalendarDay`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seasonal calendar day list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seasonal calendar day untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seasonal calendar day yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seasonal calendar day are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `feedSignal`.; 422 `invalidPeriod`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  name: Eid Al Adha 2027
  period: 2027-05-16 to 2027-05-19
  impact: +15% to +25%
```

#### Permissions

- `listSeasonalCalendarDay` → `PRODUCT_VIEW` (read) · staff
- `setDemandSignalConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Dynamic pricing in two phases: first rule-based by time and capacity (e.g. +20% once capacity reaches 70%, early-booking discounts); factor-based (weather/AI-driven) later, scoped separately. *(agreed · MoM 19 Aug 2026, 4.10 Workshop Planning & Remaining Scope; 5. Key Decisions · DI-369)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-092` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-092`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 8: Works in Seasonal, Calendar, Day & Timeslot Dynamic Rules → Configure dynamic pricing behavior according to temporal commercial patterns.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-092?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save demand signal configuration.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-093` Channel, Customer Segment & Location Dynamic Rules

**Allow dynamic-pricing behavior to differ according to commercial context.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-093 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-customer-segment-location-dynamic-rules-adm-093` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: POS, Call Center, API. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Dynamic pricing that differs by channel, customer segment and location.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: POS, Call Center, API. (CHG-MOV-008)
- No write operation: a configuration screen (Channel, Customer Segment & Location Dynamic Rules) declares only reads (listChannelCustomerSegment). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Dimension | segmented control | — | Channel · Customer segment · Location | `listChannelCustomerSegment` ?dimension |
| Strategy | text field | — | — | `listChannelCustomerSegment` ?strategyId |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listChannelCustomerSegment` ?channel |
| Customer segment | select | — | Standard customer · Member · Loyalty tier · Resident · Vip · Corporate · Group · B2B · Custom segment | `listChannelCustomerSegment` ?customerSegment |
| Location level | select | — | Country · Market · Venue · Attraction · Zone · Event location | `listChannelCustomerSegment` ?locationLevel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| POS (primary button) | navigation or local | — | — | — | — |
| Call Center (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **context rules**: Rules as rows by context. *(source: contracts/spine/catalogue.yaml#listChannelCustomerSegment)*

**Data it reads**: `listChannelCustomerSegment` (onLoad, Channel, Customer Segment & Location Dynamic Rules)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `listChannelCustomerSegment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel customer segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel customer segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel customer segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel customer segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  context: App, Gold members
  effect: dynamic uplift capped at +5%
```

#### Permissions

- `listChannelCustomerSegment` → `PRODUCT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-093` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-093`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 10: Works in Channel, Customer Segment & Location Dynamic Rules → Allow dynamic-pricing behavior to differ according to commercial context.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-093?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: POS, Call Center, API.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-094` Dynamic Price Bands, Ladders & Adjustment Matrix

**Define the controlled monetary steps through which prices can move. This is preferable to allowing unrestricted price generation for many products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-094 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/dynamic-price-bands-ladders-adjustment-matrix-adm-094` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The controlled steps a dynamic price moves through: bands or a ladder, base band, minimum and maximum, step size, movement limits, cooldown and reversal rule.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum Bands per Movement | text field | — | — | — | — | — | — |
| Minimum Time Between Movements | text field | — | — | — | — | — | — |
| Upward Movement | select field | — | — | — | — | — | — |
| Downward Movement | select field | — | — | — | — | — | — |
| Reversal Rules | select field | — | — | — | — | — | — |
| Cooldown Period | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Strategy | text field | — | — | `listDynamicPriceBand` ?strategyId |
| Adjustment model | radio group | — | Fixed price bands · Percentage bands · Fixed amount steps · Derived bands · Continuous range | `listDynamicPriceBand` ?adjustmentModel |

**Form: Save price ladder matrix** (modal, opened by *Save price ladder matrix*; *Save price ladder matrix* calls `setPriceLadderMatrix`, *Cancel* sends nothing)

**Collects what `setPriceLadderMatrix` sends before it is called.** Required: `dynamicPricingStrategyId`, `adjustmentModel`. Optional: `basePriceSource`, `bands`, `baseBandCode`, `stepAmount`, `minimumPrice`, `basePrice`, `maximumPrice`, `allowUpward`, `allowDownward`, `maxIncreasePercentPerAdjustment`, `maxDecreasePercentPerAdjustment`, `maximumBandsPerMovement` and 4 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Dynamic pricing strategy `dynamicPricingStrategyId` | picker: choose a dynamic pricing strategy | required | — | — | shows names, sends the id | — | `setPriceLadderMatrix` body |
| Base price source `basePriceSource` | text field | optional | — | max length 100 | — | — | `setPriceLadderMatrix` body |
| Adjustment model `adjustmentModel` | radio group | required | — | Fixed price bands · Percentage bands · Fixed amount steps · Derived bands · Continuous range | — | — | `setPriceLadderMatrix` body |
| Bands `bands` | key and value settings | optional | — | — | — | `[{code, price, percent}]`, ascending. | `setPriceLadderMatrix` body |
| Base band code `baseBandCode` | text field | optional | — | max length 40 | — | — | `setPriceLadderMatrix` body |
| Step amount `stepAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPriceLadderMatrix` body |
| Minimum price `minimumPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPriceLadderMatrix` body |
| Base price `basePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPriceLadderMatrix` body |
| Maximum price `maximumPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPriceLadderMatrix` body |
| Allow upward `allowUpward` | toggle | optional | on | — | — | — | `setPriceLadderMatrix` body |
| Allow downward `allowDownward` | toggle | optional | on | — | — | — | `setPriceLadderMatrix` body |
| Max increase percent per adjustment `maxIncreasePercentPerAdjustment` | number field | optional | — | — | — | — | `setPriceLadderMatrix` body |
| Max decrease percent per adjustment `maxDecreasePercentPerAdjustment` | number field | optional | — | — | — | — | `setPriceLadderMatrix` body |
| Maximum bands per movement `maximumBandsPerMovement` | number field | optional | — | min 1 | — | — | `setPriceLadderMatrix` body |
| Minimum minutes between movements `minimumMinutesBetweenMovements` | number field (minutes) | optional | — | min 0 | — | — | `setPriceLadderMatrix` body |
| Cooldown minutes `cooldownMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setPriceLadderMatrix` body |
| Reversal rule `reversalRule` | segmented control | optional | After cooldown | Allowed · After cooldown · Not allowed | — | — | `setPriceLadderMatrix` body |
| Allowed endpoints `allowedEndpoints` | list of values (chips) | optional | — | — | — | Psychological price endings, e.g. `.99`, `.00`. | `setPriceLadderMatrix` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `strategyActive`.; 422 `invalidBands` or `guardrailBreached`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **ladder**: A vertical ladder of bands with the base marked; movement limits beside it. *(source: contracts/spine/catalogue.yaml#setPriceLadderMatrix)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed Price Bands (primary button) | navigation or local | — | — | — | — |
| Continuous Range where permitted (secondary button) | navigation or local | — | — | — | — |
| Save price ladder matrix (secondary button) | `setPriceLadderMatrix` PUT `/dynamic-pricing-strategies/{strategyId}/price-ladder` | PriceLadder | PriceLadder | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `strategyActive`.; 422 `invalidBands` or `guardrailBreached`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDynamicPriceBand` (onLoad, Dynamic Price Bands, Ladders & Adjustment Matrix)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; carries `strategyId`; calls `listDynamicPriceBand`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic price bands configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic price bands untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic price bands configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `strategyActive`.; 422 `invalidBands` or `guardrailBreached`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ladder:
  model: fixedPriceBands
  bands:
  - AED 249.00
  - AED 279.00
  - AED 295.00 (base)
  - AED 319.00
  - AED 349.00
  cooldownMinutes: 120
```

#### Permissions

- `listDynamicPriceBand` → `PRODUCT_VIEW` (read) · staff
- `setPriceLadderMatrix` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*
- Dynamic pricing in two phases: first rule-based by time and capacity (e.g. +20% once capacity reaches 70%, early-booking discounts); factor-based (weather/AI-driven) later, scoped separately. *(agreed · MoM 19 Aug 2026, 4.10 Workshop Planning & Remaining Scope; 5. Key Decisions · DI-369)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-094` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-094`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 12: Works in Dynamic Price Bands, Ladders & Adjustment Matrix → Define the controlled monetary steps through which prices can move. This is preferable to allowing unrestricted price generation for many products.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-094?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed Price Bands, Continuous Range where permitted, Save price ladder matrix.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-095` Dynamic Pricing Guardrails & Commercial Protection

**Establish the non-negotiable boundaries for every dynamic-pricing strategy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-095 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-pricing-guardrails-commercial-protection-adm-095` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The non-negotiable boundaries of dynamic pricing at a scope: floor and ceiling, margin, rate-of-change limits, protected rate types, freeze and kill switch, automation level and its authority tiers, circuit breakers and what happens on failure. No strategy may produce a price outside them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Absolute Minimum Price | select field | — | — | — | — | — | — |
| Absolute Maximum Price | select field | — | — | — | — | — | — |
| Minimum Margin | select field | — | — | — | — | — | — |
| Maximum Uplift % | select field | — | — | — | — | — | — |
| Maximum Reduction % | select field | — | — | — | — | — | — |
| Maximum Single Change | select field | — | — | — | — | — | — |
| Maximum Daily Change | select field | — | — | — | — | — | — |
| Maximum Weekly Change | select field | — | — | — | — | — | — |
| Minimum Change Interval | select field | — | — | — | — | — | — |
| Maximum Changes per Day | text field | — | — | — | — | — | — |
| Minimum Inventory | select field | — | — | — | — | — | — |
| Maximum Occupancy Trigger | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope level | select | — | Global · Strategy · Venue · Product · Event · Performance | `listDynamicPricingGuardrail` ?scopeLevel |
| Scope | text field | — | — | `listDynamicPricingGuardrail` ?scopeId |

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

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kill switch and freeze**: At the top of the screen, red and separate from the form, each with a confirmation naming the scope; the kill switch stops every automatic change in scope at once. *(source: contracts/spine/catalogue.yaml#setDynamicPricingGuardrailPolicy)*
- **automationLevel**: Advisory, Human in the loop, Conditionally autonomous, Autonomous, as a stepped scale with what each permits; authority tiers appear for the last two. *(source: contracts/spine/catalogue.yaml#/components/schemas/DynamicPricingControl)*
- **protectedRateTypes**: Contract, membership, corporate, promotional locked, regulatory and complimentary rates as checkboxes; excluded from automation by default. *(source: contracts/spine/catalogue.yaml#/components/schemas/DynamicPricingControl)*
- **activeOverride**: Who, why, price, start, expiry and what happens after; shown as a banner while active. *(source: contracts/spine/catalogue.yaml#/components/schemas/DynamicPricingControl)*

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Freeze Product, Freeze Event, Freeze Performance, Freeze Strategy, Freeze Venue, Return to Base Price. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save dynamic pricing guardrail policy (primary button) | `setDynamicPricingGuardrailPolicy` PUT `/dynamic-pricing-controls` | DynamicPricingControl | DynamicPricingControl | 422 `invalidRange` or `scopeIdRequired`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDynamicPricingGuardrail` (onLoad, Dynamic Pricing Guardrails & Commercial Protection)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; calls `listDynamicPricingGuardrail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing guardrails configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing guardrails untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing guardrails configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `invalidRange` or `scopeIdRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guardrail:
  scope: 'venue: Dune Park'
  floor: AED 199.00
  ceiling: AED 399.00
  maxSingleChange: 10%
  maxChangesPerDay: 4
  automationLevel: humanInTheLoop
  safeFailure: holdLastPrice
```

#### Permissions

- `listDynamicPricingGuardrail` → `PRODUCT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-095` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-095`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 14: Works in Dynamic Pricing Guardrails & Commercial Protection → Establish the non-negotiable boundaries for every dynamic-pricing strategy.

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-095?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save dynamic pricing guardrail policy.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-096` Dynamic Pricing Automation Policy & Control

**Define how much authority the pricing engine has to act on a calculated dynamic price. This is different from Board 4's approval workflow. Board 5 determines whether the engine may act automatically. Board 4 handles governance when formal approval is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-096 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure independently by; Configure; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/dynamic-pricing-automation-policy-control-adm-096` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How much authority the pricing engine has to act on a calculated price (advisory, human in the loop, conditional, autonomous), as distinct from the approval workflow of governed changes.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Strategy | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Maximum Automatic Changes / Day | text field | — | — | — | — | — | — |
| Minimum Time Between Changes | text field | — | — | — | — | — | — |
| No-Change Windows | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Override Price | select field | — | — | — | — | — | — |
| Start | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Return Behavior | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope level | select | — | Product · Event · Venue · Strategy · Channel · Market | `listDynamicPricingAutomation` ?scopeLevel |
| Automation mode | radio group | — | Monitor · Recommend · Prepare change · Auto execute within guardrails | `listDynamicPricingAutomation` ?automationMode |

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

**Data it reads**: `listDynamicPricingAutomation` (onLoad, Dynamic Pricing Automation Policy & Control)

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Returns to the board's landing screen*; calls `listDynamicPricingAutomation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing automation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing automation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `invalidRange` or `scopeIdRequired`. |

#### Consistency with other screens

- Match `ADM-095`: The same record (setDynamicPricingGuardrailPolicy); automation level and guardrails are two tabs of one form.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  scope: 'venue: Dune Park'
  automationLevel: conditionalAutonomous
  maxAdjustment: 8%
  minAiConfidence: 0.8
```

#### Permissions

- `listDynamicPricingAutomation` → `PRODUCT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-096` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-096`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 16: Works in Dynamic Pricing Automation Policy & Control → Define how much authority the pricing engine has to act on a calculated dynamic price. This is different from Board 4's approval workflow. Board 5 determines whether the engine may act automatically. …

#### Acceptance for the design

- [ ] Every input above is drawn (50), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-096?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save dynamic pricing guardrail policy.
- [ ] Every transition is wired: `ADM-088`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-097` Rule Priority, Conflict Resolution & Dynamic Pricing Test Console

**Determine the final dynamic price when multiple strategies and rules are simultaneously applicable. This is the final and most important control screen of Board 5. (merged into BO-441 Price Priority & Conflict Rules).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/rule-priority-conflict-resolution-dynamic-pricing-test-c-adm-097` |

**What the spec says about it.** **Merged into BO-441 Price Priority & Conflict Rules** (decided 2 October 2026, Chinmay: DEC-100 and the pre-apply round, "duplicate screens: merge as proposed"; CHG-MOV-002). On one platform it declared the same operations as BO-441 (check-screen-wiring S-DUP-SCREEN). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-441, and nothing on it is built separately. **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The final dynamic price when several strategies apply: priority order, resolution method and a test console.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Contradictory rules** (metric tile)

**Same priority** (metric tile)

**Impossible condition** (metric tile)

**Overlapping strategy** (metric tile)

**Circular dependency** (metric tile)

**Missing fallback** (metric tile)

**Guardrail conflict** (metric tile)

**Every rule priority conflict** (data table)

| Shows | Format | Notes |
|---|---|---|
| Calculation path | list or chips (count when long) | Explainability: the complete calculation path, one step per line |

**The selected rule priority conflict** (detail panel): The pack groups this record's detail under its own headings: “For one Saturday evening ticket”, “Priority Matrix”, “Commercial Protection”, “Contract/Member Protection”, “Event-Specific Strategy”, “Inventory/Occupancy”.

| Shows | Format | Notes |
|---|---|---|
| Calculation path | list or chips (count when long) | Explainability: the complete calculation path, one step per line |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Most Specific Rule Wins (primary button) | navigation or local | — | — | — | — |
| Stop Processing (destructive button) | navigation or local | — | — | — | — |
| Run Test (primary button) | navigation or local | — | — | — | — |
| Save Case (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-088` Dynamic Pricing Strategy Command Center: *Dynamic Pricing Strategy Command Center*
- → `BO-441` Price Priority & Conflict Rules: *Open Price Priority & Conflict Rules*

**What opens over it**

- confirmDialog *Stop Processing*: **Stop Processing on a rule priority conflict is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule priority conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule priority conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule priority conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule priority conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-441 Price Priority & Conflict Rules requires; this id has no operation of its own since the merge, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-441`: Same operation and component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  scenario: Sat 20:00 slot, 85% sold, 3 days out
  result: AED 349.00 (occupancy tier capped by ceiling)
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-441 Price Priority & Conflict Rules requires; this id has no operation of its own since the merge, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-097` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-097`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-097?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Most Specific Rule Wins, Stop Processing, Run Test, Save Case.
- [ ] Every transition is wired: `ADM-088`, `BO-441`.
- [ ] Sign-in is asked only where the spec asks for it.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listChannelCustomerSegment": {"method":"GET","path":"/channel-customer-segment","contract":"catalogue","summary":"Channel, Customer Segment & Location Dynamic Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dimension","in":"query","required":false},{"name":"strategyId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"locationLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPriceBand": {"method":"GET","path":"/dynamic-price-band","contract":"catalogue","summary":"Dynamic Price Bands, Ladders & Adjustment Matrix","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"strategyId","in":"query","required":false},{"name":"adjustmentModel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPriceRules": {"method":"GET","path":"/pricing/dynamic-rules","contract":"catalogue","summary":"Dynamic pricing rules","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PricingDynamicPriceRule"},
"listDynamicPricingAutomation": {"method":"GET","path":"/dynamic-pricing-automation","contract":"catalogue","summary":"Dynamic Pricing Automation Policy & Control","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopeLevel","in":"query","required":false},{"name":"automationMode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPricingGuardrail": {"method":"GET","path":"/dynamic-pricing-guardrail","contract":"catalogue","summary":"Dynamic Pricing Guardrails & Commercial Protection","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopeLevel","in":"query","required":false},{"name":"scopeId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPricingStrategy": {"method":"GET","path":"/dynamic-pricing-strategy","contract":"catalogue","summary":"Dynamic Pricing Strategy Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"strategyType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"automationMode","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeasonalCalendarDay": {"method":"GET","path":"/seasonal-calendar-day","contract":"catalogue","summary":"Seasonal, Calendar, Day & Timeslot Dynamic Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dimension","in":"query","required":false},{"name":"strategyId","in":"query","required":false},{"name":"season","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setBookingVelocityTime": {"method":"PUT","path":"/booking-velocity-time","contract":"catalogue","summary":"Booking Velocity & Time-to-Event Rule Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BookingVelocityTimeToEventRuleBuilderInput","responds":"BookingVelocityTimeToEventRuleBuilderView"},
"setDemandOccupancyAvailability": {"method":"PUT","path":"/demand-occupancy-availability","contract":"catalogue","summary":"Demand, Occupancy & Availability Rule Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DemandOccupancyAvailabilityRuleBuilderInput","responds":"DemandOccupancyAvailabilityRuleBuilderView"},
"setDemandSignalConfiguration": {"method":"PUT","path":"/demand-signals/{signalId}","contract":"catalogue","summary":"Enter a calendar signal or configure how a demand signal is used","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DemandSignal","responds":"DemandSignal"},
"setDynamicPricingGuardrailPolicy": {"method":"PUT","path":"/dynamic-pricing-controls","contract":"catalogue","summary":"Set the guardrails and automation level of dynamic pricing at one scope","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicPricingControl","responds":"DynamicPricingControl"},
"setDynamicPricingStrategy": {"method":"PUT","path":"/dynamic-pricing-strategy-2","contract":"catalogue","summary":"Dynamic Pricing Strategy Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicPricingStrategyBuilderInput","responds":"DynamicPricingStrategyBuilderView"},
"setPriceLadderMatrix": {"method":"PUT","path":"/dynamic-pricing-strategies/{strategyId}/price-ladder","contract":"catalogue","summary":"Set a strategy's price ladder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceLadder","responds":"PriceLadder"},
"transitionDynamicPricingStrategy": {"method":"POST","path":"/dynamic-pricing-strategies/{strategyId}/lifecycle","contract":"catalogue","summary":"Activate, pause, resume or retire a dynamic pricing strategy","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DynamicPricingStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BookingVelocityTimeToEventRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Booking Velocity & Time-to-Event Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"ruleId":{"type":"string","description":"Rule ID; empty on create","nullable":true},"strategyId":{"type":"string","description":"Strategy the rule belongs to"},"ruleName":{"type":"string","description":"Rule name"},"ruleKind":{"type":"string","enum":["bookingVelocity","earlyBird","lastMinute","combined","decayEscalation"],"description":"Rule family (pack pp.80-81)"},"expectedPaceSource":{"type":"string","enum":["historicalBookingCurve","configuredTarget"],"description":"What pace variance is measured against; defaults to configuredTarget until a historical curve exists (decided 29 September, readiness close-out)"},"expectedSalesPerDay":{"type":"integer","description":"Expected sales per day when expectedPaceSource is configuredTarget","nullable":true},"conditions":{"type":"array","items":{"type":"object","properties":{"metric":{"type":"string","enum":["salesPerHour","salesPerDay","salesPerWeek","currentBookingPace","paceVariancePercent","remainingInventory","daysToEvent","occupancyPercent"],"description":"Input evaluated (pack p.80; daysToEvent 0 = same day)"},"operator":{"type":"string","enum":["lt","lte","gt","gte","eq","between"],"description":"Comparison"},"value":{"type":"number","description":"Threshold value (percent for percentages, count for counts, days for time-to-event)"},"valueTo":{"type":"number","description":"Upper value when operator is between","nullable":true}},"description":"One condition; persisted as a PricingDynamicPriceCondition"},"description":"Conditions (all must hold unless conditionLogic is any)"},"conditionLogic":{"type":"string","enum":["all","any"],"description":"How conditions combine; defaults to all (decided 29 September, readiness close-out)"},"timeToEventSchedule":{"type":"array","items":{"type":"object","properties":{"daysBefore":{"type":"integer","description":"Days before the event/visit (T-180 ... T-1; 0 = same day); custom intervals allowed"},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"The price action; the result still passes through the price ladder and the guardrails"}},"description":"One time-to-event step, e.g. T-90 -> -15%"},"description":"Time-to-event steps (early-bird, decay/escalation); empty for condition-only rules"},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"Action when the conditions hold (for condition rules)","nullable":true},"priority":{"type":"integer","description":"Priority within the strategy; lower wins"},"enabled":{"type":"boolean","description":"Enabled"}}},
"BookingVelocityTimeToEventRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Booking Velocity & Time-to-Event Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID; empty on create","nullable":true},"strategyId":{"type":"string","description":"Strategy the rule belongs to"},"ruleName":{"type":"string","description":"Rule name"},"ruleKind":{"type":"string","enum":["bookingVelocity","earlyBird","lastMinute","combined","decayEscalation"],"description":"Rule family (pack pp.80-81)"},"expectedPaceSource":{"type":"string","enum":["historicalBookingCurve","configuredTarget"],"description":"What pace variance is measured against; defaults to configuredTarget until a historical curve exists (decided 29 September, readiness close-out)"},"expectedSalesPerDay":{"type":"integer","description":"Expected sales per day when expectedPaceSource is configuredTarget","nullable":true},"conditions":{"type":"array","items":{"type":"object","properties":{"metric":{"type":"string","enum":["salesPerHour","salesPerDay","salesPerWeek","currentBookingPace","paceVariancePercent","remainingInventory","daysToEvent","occupancyPercent"],"description":"Input evaluated (pack p.80; daysToEvent 0 = same day)"},"operator":{"type":"string","enum":["lt","lte","gt","gte","eq","between"],"description":"Comparison"},"value":{"type":"number","description":"Threshold value (percent for percentages, count for counts, days for time-to-event)"},"valueTo":{"type":"number","description":"Upper value when operator is between","nullable":true}},"description":"One condition; persisted as a PricingDynamicPriceCondition"},"description":"Conditions (all must hold unless conditionLogic is any)"},"conditionLogic":{"type":"string","enum":["all","any"],"description":"How conditions combine; defaults to all (decided 29 September, readiness close-out)"},"timeToEventSchedule":{"type":"array","items":{"type":"object","properties":{"daysBefore":{"type":"integer","description":"Days before the event/visit (T-180 ... T-1; 0 = same day); custom intervals allowed"},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"The price action; the result still passes through the price ladder and the guardrails"}},"description":"One time-to-event step, e.g. T-90 -> -15%"},"description":"Time-to-event steps (early-bird, decay/escalation); empty for condition-only rules"},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"Action when the conditions hold (for condition rules)","nullable":true},"priority":{"type":"integer","description":"Priority within the strategy; lower wins"},"enabled":{"type":"boolean","description":"Enabled"}}},
"ChannelCustomerSegmentLocationDynamicRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel, Customer Segment & Location Dynamic Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID"},"strategyId":{"type":"string","description":"Strategy the rule belongs to; empty for a tenant-wide rule","nullable":true},"dimension":{"type":"string","enum":["channel","customerSegment","location"],"description":"Rule dimension"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Channel (B2C = guestWeb, Mobile App = guestApp, Reseller = partner)"},"customerSegment":{"type":"string","enum":["standardCustomer","member","loyaltyTier","resident","vip","corporate","group","b2b","customSegment"],"description":"Customer segment (pack p.83)","nullable":true},"segmentRef":{"type":"string","description":"Loyalty tier or custom segment ID","nullable":true},"locationLevel":{"type":"string","enum":["country","market","venue","attraction","zone","eventLocation"],"description":"Location level (pack pp.83-84)","nullable":true},"locationId":{"type":"string","description":"Country, market, venue, attraction, zone or event location ID","nullable":true},"dynamicPricingEnabled":{"type":"boolean","description":"Whether dynamic pricing applies in this context"},"rangeMinPercent":{"type":"number","description":"Lowest adjustment from base in percent","nullable":true},"rangeMaxPercent":{"type":"number","description":"Highest adjustment from base in percent (maximum uplift)","nullable":true},"protected":{"type":"boolean","description":"Protected segment: always receives its protected rate and is excluded from dynamic adjustment"}}},
"DemandOccupancyAvailabilityRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Demand, Occupancy & Availability Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"ruleId":{"type":"string","description":"Rule ID; empty on create","nullable":true},"strategyId":{"type":"string","description":"Strategy the rule belongs to"},"ruleName":{"type":"string","description":"Rule name"},"ruleKind":{"type":"string","enum":["occupancy","inventory","availability","demand"],"description":"Rule family (pack p.78-79)"},"inputMetric":{"type":"string","enum":["ticketsSold","currentDemand","occupancyPercent","remainingCapacity","remainingInventory","availableSeats","capacityUtilization","salesPace"],"description":"Supported Input evaluated (pack p.78)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromValue":{"type":"number","description":"From (inclusive)"},"toValue":{"type":"number","description":"To (inclusive); empty for no upper bound","nullable":true},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"The price action; the result still passes through the price ladder and the guardrails"}},"description":"One step of the matrix, e.g. occupancy 81-90% -> +10%"},"description":"Threshold matrix; tiers must not overlap"},"demandIndexDefinition":{"type":"string","description":"Required when inputMetric is currentDemand: how the demand index is calculated (the pack requires it to be explicitly configured and documented)","nullable":true},"exitThresholdOffset":{"type":"number","description":"Exit threshold: how far the metric must fall back below a tier's entry before the price reverses; defaults to 2 (points or units of the metric) (decided 29 September, readiness close-out)"},"minimumDurationMinutes":{"type":"integer","description":"Minimum duration a threshold must hold before the price moves; defaults to 15 (decided 29 September, readiness close-out)"},"cooldownMinutes":{"type":"integer","description":"Cooldown after a movement before the next; defaults to 60 (decided 29 September, readiness close-out)"},"priority":{"type":"integer","description":"Priority within the strategy; lower wins"},"enabled":{"type":"boolean","description":"Enabled"}}},
"DemandOccupancyAvailabilityRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Demand, Occupancy & Availability Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID; empty on create","nullable":true},"strategyId":{"type":"string","description":"Strategy the rule belongs to"},"ruleName":{"type":"string","description":"Rule name"},"ruleKind":{"type":"string","enum":["occupancy","inventory","availability","demand"],"description":"Rule family (pack p.78-79)"},"inputMetric":{"type":"string","enum":["ticketsSold","currentDemand","occupancyPercent","remainingCapacity","remainingInventory","availableSeats","capacityUtilization","salesPace"],"description":"Supported Input evaluated (pack p.78)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromValue":{"type":"number","description":"From (inclusive)"},"toValue":{"type":"number","description":"To (inclusive); empty for no upper bound","nullable":true},"action":{"type":"object","properties":{"actionType":{"type":"string","enum":["percentAdjustment","fixedAmountAdjustment","moveToBand","returnToBase"],"description":"What the rule does to the current price"},"percent":{"type":"number","description":"Adjustment in percent (negative lowers the price) when actionType is percentAdjustment","nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Signed amount when actionType is fixedAmountAdjustment","nullable":true},"bandCode":{"type":"string","description":"Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand","nullable":true}},"description":"The price action; the result still passes through the price ladder and the guardrails"}},"description":"One step of the matrix, e.g. occupancy 81-90% -> +10%"},"description":"Threshold matrix; tiers must not overlap"},"demandIndexDefinition":{"type":"string","description":"Required when inputMetric is currentDemand: how the demand index is calculated (the pack requires it to be explicitly configured and documented)","nullable":true},"exitThresholdOffset":{"type":"number","description":"Exit threshold: how far the metric must fall back below a tier's entry before the price reverses; defaults to 2 (points or units of the metric) (decided 29 September, readiness close-out)"},"minimumDurationMinutes":{"type":"integer","description":"Minimum duration a threshold must hold before the price moves; defaults to 15 (decided 29 September, readiness close-out)"},"cooldownMinutes":{"type":"integer","description":"Cooldown after a movement before the next; defaults to 60 (decided 29 September, readiness close-out)"},"priority":{"type":"integer","description":"Priority within the strategy; lower wins"},"enabled":{"type":"boolean","description":"Enabled"}}},
"DemandSignal": {"type":"object","x-ticvai-persistence":"catalogue.demand_signal","description":"**An external or calendar signal that moves demand** (29 September, data model DM3). Merges weather (ADM-101), nearby events (ADM-102), competitor prices (ADM-103), tourism, holiday and market signals (ADM-104) and the tenant's special calendar (Ramadan, Eid, school breaks) used by temporal rules. `signalKind` says which; the readings specific to a kind are in `reading`, and a venue's sensitivity settings in `configuration`. A signal informs forecasts and recommendations; it never sets a price.","required":["id","scopePath","signalKind","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"signalKind":{"type":"string","enum":["weather","nearbyEvent","competitorPrice","calendar","tourism","transport","market"]},"signalType":{"type":"string","maxLength":60,"nullable":true,"description":"E.g. `publicHoliday`, `ramadan`, an event type, a weather condition."},"name":{"type":"string","maxLength":200,"nullable":true},"source":{"type":"string","maxLength":100,"description":"Provider, feed or `tenant` for manual entries."},"venueId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Competitor observations: the comparable TICVAI product."},"geography":{"type":"string","maxLength":100,"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"periodStart":{"type":"string","format":"date-time","nullable":true},"periodEnd":{"type":"string","format":"date-time","nullable":true},"currentValue":{"type":"number","nullable":true},"unit":{"type":"string","maxLength":20,"nullable":true},"reading":{"type":"object","additionalProperties":true,"nullable":true,"description":"Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices."},"configuration":{"type":"object","additionalProperties":true,"nullable":true,"description":"Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`."},"weight":{"type":"number","nullable":true},"reliability":{"type":"number","nullable":true,"minimum":0,"maximum":1},"historicalCorrelation":{"type":"number","nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"impactMinPercent":{"type":"number","nullable":true},"impactMaxPercent":{"type":"number","nullable":true},"refreshFrequency":{"type":"string","enum":["realTime","hourly","daily","weekly","manual",null],"nullable":true},"isApproved":{"type":"boolean","default":false,"description":"Competitor sources and comparability approved for use."},"isActive":{"type":"boolean","default":true},"observedAt":{"type":"string","format":"date-time","nullable":true},"lastUpdatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicPriceBandsLaddersAdjustmentMatrixView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Price Bands, Ladders & Adjustment Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumBandsPerMovement":{"type":"integer","description":"Maximum bands per movement; defaults to 1 (decided 29 September, readiness close-out)"},"minimumTimeBetweenMovements":{"type":"integer","description":"Minimum minutes between movements; defaults to 60 (decided 29 September, readiness close-out)"},"reversalRules":{"type":"string","enum":["allowed","afterCooldown","notAllowed"],"description":"Whether a movement may be reversed; defaults to afterCooldown (decided 29 September, readiness close-out)"},"cooldownPeriod":{"type":"integer","description":"Cooldown in minutes after a movement; defaults to 60 (decided 29 September, readiness close-out)"},"ladderId":{"type":"string","description":"Ladder ID"},"strategyId":{"type":"string","description":"Strategy the ladder belongs to"},"basePriceSource":{"type":"string","description":"Board 1 rate the ladder is built around"},"adjustmentModel":{"type":"string","enum":["fixedPriceBands","percentageBands","fixedAmountSteps","derivedBands","continuousRange"],"description":"Adjustment Model (pack p.85)"},"bands":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"Band code, e.g. P4"},"price":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Band price (fixed and derived bands)","nullable":true},"percent":{"type":"number","description":"Band offset from base in percent (percentage bands)","nullable":true}},"description":"One band"},"description":"Bands, lowest first"},"baseBandCode":{"type":"string","description":"Band holding the base price, e.g. P3"},"stepAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Step for fixedAmountSteps","nullable":true},"allowUpward":{"type":"boolean","description":"Upward movement allowed"},"allowDownward":{"type":"boolean","description":"Downward movement allowed"},"maxIncreasePercentPerAdjustment":{"type":"number","description":"Asymmetric movement: maximum increase per adjustment in percent","nullable":true},"maxDecreasePercentPerAdjustment":{"type":"number","description":"Asymmetric movement: maximum decrease per adjustment in percent","nullable":true},"allowedEndpoints":{"type":"array","items":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},"description":"Psychological pricing: governed endpoints (e.g. AED 249, 259, 279) a price may land on"},"minimumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Preview: lowest price on the ladder"},"basePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Preview: base price"},"maximumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Preview: highest price on the ladder"}}},
"DynamicPricingAutomationPolicyControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Automation Policy & Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumAutomaticChangesDay":{"type":"integer","description":"Maximum automatic changes per day; defaults to 4 (decided 29 September, readiness close-out)"},"minimumTimeBetweenChanges":{"type":"integer","description":"Minimum minutes between automatic changes; defaults to 60 (decided 29 September, readiness close-out)"},"noChangeWindows":{"type":"array","items":{"type":"object","properties":{"anchor":{"type":"string","enum":["gatesOpening","eventStart","clockTime"],"description":"What the window is measured from"},"minutesBefore":{"type":"integer","description":"Minutes before the anchor","nullable":true},"minutesAfter":{"type":"integer","description":"Minutes after the anchor","nullable":true},"clockFrom":{"type":"string","description":"HH:mm when anchor is clockTime","nullable":true},"clockTo":{"type":"string","description":"HH:mm","nullable":true}},"description":"One window"},"description":"No-Change Windows, e.g. 30 minutes before gates open"},"policyId":{"type":"string","description":"Policy ID"},"scopeLevel":{"type":"string","enum":["product","event","venue","strategy","channel","market"],"description":"Automation Scope (pack p.88)"},"scopeId":{"type":"string","description":"ID of the product, event, venue, strategy, channel or market"},"automationMode":{"type":"string","enum":["monitor","recommend","prepareChange","autoExecuteWithinGuardrails"],"description":"Automation mode; defaults to recommend (decided 29 September, readiness close-out)"},"authorityTiers":{"type":"array","items":{"type":"object","properties":{"maxAdjustmentPercent":{"type":"number","description":"Applies to adjustments up to this percent (absolute)","nullable":true},"action":{"type":"string","enum":["autoExecute","autoExecuteIfConfident","revenueManager","commercialDirector","board4Governance"],"description":"Who acts"},"confidenceThreshold":{"type":"number","description":"Confidence percent required for autoExecuteIfConfident","nullable":true}},"description":"One tier"},"description":"Authority policy, smallest adjustment first; empty means every change needs a Revenue Manager (decided 29 September, readiness close-out)"},"safeFailureBehavior":{"type":"string","enum":["holdLastPrice","returnToBase","freeze","requestReview"],"description":"Safe Failure when inputs are unavailable; defaults to holdLastPrice (decided 29 September, readiness close-out)"},"activeOverride":{"type":"object","properties":{"user":{"type":"string","description":"User"},"reason":{"type":"string","description":"Reason"},"overridePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Override price"},"start":{"type":"string","format":"date-time","description":"Start"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"returnBehavior":{"type":"string","enum":["resumeEngine","returnToBase","holdOverridePrice"],"description":"What happens at expiry"}},"description":"Manual override in force, if any","nullable":true}}},
"DynamicPricingControl": {"type":"object","x-ticvai-persistence":"catalogue.dynamic_pricing_control","description":"**The limits and the autonomy of dynamic pricing at one scope** (29 September, data model DM3). Merges guardrails (ADM-093) and automation policy (ADM-094, ADM-113): both are per-scope controls a price change must pass, and they share the rate-of-change limits. The most specific scope wins; guardrails are re-checked at execution (`createLiveDynamicPrice`). `automationLevel` is the one vocabulary: the strategy screen's `monitor`/`recommend` read as `advisory`, `prepareChange` as `humanInTheLoop`, `autoExecuteWithinGuardrails` as `conditionalAutonomous`.","required":["id","scopePath","scopeLevel","automationLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"scopeLevel":{"type":"string","enum":["global","market","venue","strategy","product","event","performance","channel"]},"scopeId":{"type":"string","format":"uuid","nullable":true,"description":"Null at `global`."},"absoluteMinimumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"absoluteMaximumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"minimumMarginPercent":{"type":"number","nullable":true},"maximumUpliftPercent":{"type":"number","nullable":true,"minimum":0},"maximumReductionPercent":{"type":"number","nullable":true,"minimum":0},"maximumSingleChangePercent":{"type":"number","nullable":true,"minimum":0},"maximumDailyChangePercent":{"type":"number","nullable":true,"minimum":0},"maximumWeeklyChangePercent":{"type":"number","nullable":true,"minimum":0},"minimumChangeIntervalMinutes":{"type":"integer","nullable":true,"minimum":0},"maximumChangesPerDay":{"type":"integer","nullable":true,"minimum":0},"minimumInventory":{"type":"integer","nullable":true,"minimum":0},"maximumOccupancyTriggerPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100},"protectedRateTypes":{"type":"array","items":{"type":"string","enum":["contractRates","membershipRates","corporateRates","promotionalLockedRates","regulatoryPrices","complimentaryRates"]}},"isFrozen":{"type":"boolean","default":false},"isKillSwitchActive":{"type":"boolean","default":false,"description":"Stops every automatic change in scope at once."},"automationLevel":{"type":"string","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"],"default":"advisory"},"authorityTiers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{maxAdjustmentPercent, action, confidenceThreshold}]`."},"maxAdjustmentPercent":{"type":"number","nullable":true,"minimum":0},"minAiConfidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"minRevenueUpliftPercent":{"type":"number","nullable":true},"evaluationFrequencyMinutes":{"type":"integer","nullable":true,"minimum":1},"executionFrequencyMinutes":{"type":"integer","nullable":true,"minimum":1},"quietPeriodMinutes":{"type":"integer","nullable":true,"minimum":0},"noChangeWindows":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{anchor, minutesBefore, minutesAfter, clockFrom, clockTo}]`."},"circuitBreakers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{trigger, threshold, enabled, tripped}]`."},"requireGuardrailsPassed":{"type":"boolean","default":true},"excludeProtectedRates":{"type":"boolean","default":true},"requireHealthyForecastData":{"type":"boolean","default":true},"safeFailureBehavior":{"type":"string","enum":["holdLastPrice","returnToBase","freeze","requestReview"],"default":"holdLastPrice"},"activeOverride":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{user, reason, overridePrice, start, expiry, returnBehavior}`."},"isPaused":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicPricingGuardrailsCommercialProtectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Guardrails & Commercial Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"absoluteMinimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Absolute Minimum Price"},"absoluteMaximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Absolute Maximum Price"},"minimumMargin":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Minimum contribution margin per unit; the price never falls below cost plus this margin","nullable":true},"maximumUplift":{"type":"number","description":"Maximum uplift from base in percent"},"maximumReduction":{"type":"number","description":"Maximum reduction from base in percent"},"maximumSingleChange":{"type":"number","description":"Maximum single change in percent"},"maximumDailyChange":{"type":"number","description":"Maximum change within 24 hours in percent"},"maximumWeeklyChange":{"type":"number","description":"Maximum change within 7 days in percent","nullable":true},"minimumChangeInterval":{"type":"integer","description":"Minimum minutes between changes"},"maximumChangesPerDay":{"type":"integer","description":"Maximum changes per day"},"minimumInventory":{"type":"integer","description":"Below this remaining inventory no downward adjustment is made (decided 29 September, readiness close-out)","nullable":true},"maximumOccupancyTrigger":{"type":"number","description":"Occupancy percent above which no further uplift is triggered (decided 29 September, readiness close-out)","nullable":true},"guardrailId":{"type":"string","description":"Guardrail set ID"},"scopeLevel":{"type":"string","enum":["global","strategy","venue","product","event","performance"],"description":"Scope the guardrails apply to; the narrowest scope wins, and a narrower set can only tighten a wider one (decided 29 September, readiness close-out)"},"scopeId":{"type":"string","description":"Strategy, venue, product, event or performance ID; empty for global","nullable":true},"protectedRateTypes":{"type":"array","items":{"type":"string","enum":["contractRates","membershipRates","corporateRates","promotionalLockedRates","regulatoryPrices","complimentaryRates"]},"description":"Commercial Protection: rate types dynamic pricing never moves; all six by default (decided 29 September, readiness close-out)"},"frozen":{"type":"boolean","description":"Frozen: the engine holds the current price in this scope"},"killSwitchActive":{"type":"boolean","description":"Global kill switch: dynamic pricing suspended tenant-wide"}}},
"DynamicPricingStrategy": {"type":"object","x-ticvai-persistence":"catalogue.dynamic_pricing_strategy","description":"**A dynamic pricing strategy: what it prices, from which base and how often** (29 September, data model DM3). ADM-088 and ADM-089. Its rules are `pricing.dynamic_price_rule` rows naming it; its ladder `catalogue.price_ladder`; its limits and automation `catalogue.dynamic_pricing_control`. **Rules-based now; AI factors inform, never replace, the rules** (MoM 19 Aug 2026).","required":["id","scopePath","code","name","strategyType","scopeType","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"]},"scopeType":{"type":"string","enum":["singleProduct","productFamily","event","multiplePerformances","venue","selectedTimeslots","selectedPriceCategories"]},"venueId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"productFamily":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"timeslotIds":{"type":"array","items":{"type":"string","format":"uuid"}},"priceCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"basePriceSource":{"type":"string","maxLength":100,"description":"The price list or rate the adjustments start from."},"evaluationFrequency":{"type":"string","enum":["every15Minutes","every30Minutes","hourly","daily","onInventoryChange","onThresholdTrigger"],"default":"hourly"},"combinationMode":{"type":"string","enum":["independent","combinable","exclusive","fallback"],"default":"independent"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"clonedFromStrategyId":{"type":"string","format":"uuid","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","active","paused","frozen","expired","retired"],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicPricingStrategyBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Dynamic Pricing Strategy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"strategyName":{"type":"string","description":"Strategy Name"},"strategyCode":{"type":"string","description":"Strategy Code"},"description":{"type":"string","description":"Description"},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"],"description":"Strategy Type"},"owner":{"type":"string","description":"Owner"},"businessUnit":{"type":"string","description":"Business Unit"},"market":{"type":"string","description":"Market","nullable":true},"venue":{"type":"string","description":"Venue","nullable":true},"product":{"type":"string","description":"Product","nullable":true},"event":{"type":"string","description":"Event","nullable":true},"performances":{"type":"array","items":{"type":"string"},"description":"Performances in scope (one or many)"},"timeslots":{"type":"array","items":{"type":"string"},"description":"Timeslots in scope; empty for all"},"priceCategories":{"type":"array","items":{"type":"string"},"description":"Price categories in scope; empty for all"},"basePriceSource":{"type":"string","description":"Board 1 price-list rate ID the strategy moves from; a strategy never holds its own base amount"},"effectiveFrom":{"type":"string","format":"date-time","description":"Effective from"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to; empty for open-ended","nullable":true},"evaluationFrequency":{"type":"string","enum":["every15Minutes","every30Minutes","hourly","daily","onInventoryChange","onThresholdTrigger"],"description":"Evaluation frequency; defaults to hourly (decided 29 September, readiness close-out)"},"productFamily":{"type":"string","description":"Product family (for scopeType productFamily)","nullable":true},"scopeType":{"type":"string","enum":["singleProduct","productFamily","event","multiplePerformances","venue","selectedTimeslots","selectedPriceCategories"],"description":"Scope Assignment (pack p.77)"},"combinationMode":{"type":"string","enum":["independent","combinable","exclusive","fallback"],"description":"Strategy Combination: independent, combinable with other strategies, exclusive control, or fallback; defaults to independent (decided 29 September, readiness close-out)"},"clonedFromStrategyId":{"type":"string","description":"Strategy this one was cloned from (inherits its rules)","nullable":true}}},
"DynamicPricingStrategyBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Strategy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"strategyName":{"type":"string","description":"Strategy Name"},"strategyCode":{"type":"string","description":"Strategy Code"},"description":{"type":"string","description":"Description"},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"],"description":"Strategy Type"},"owner":{"type":"string","description":"Owner"},"businessUnit":{"type":"string","description":"Business Unit"},"market":{"type":"string","description":"Market","nullable":true},"venue":{"type":"string","description":"Venue","nullable":true},"product":{"type":"string","description":"Product","nullable":true},"event":{"type":"string","description":"Event","nullable":true},"performances":{"type":"array","items":{"type":"string"},"description":"Performances in scope (one or many)"},"timeslots":{"type":"array","items":{"type":"string"},"description":"Timeslots in scope; empty for all"},"priceCategories":{"type":"array","items":{"type":"string"},"description":"Price categories in scope; empty for all"},"basePriceSource":{"type":"string","description":"Board 1 price-list rate ID the strategy moves from; a strategy never holds its own base amount"},"effectiveFrom":{"type":"string","format":"date-time","description":"Effective from"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to; empty for open-ended","nullable":true},"evaluationFrequency":{"type":"string","enum":["every15Minutes","every30Minutes","hourly","daily","onInventoryChange","onThresholdTrigger"],"description":"Evaluation frequency; defaults to hourly (decided 29 September, readiness close-out)"},"status":{"type":"string","description":"Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired; draft on create"},"productFamily":{"type":"string","description":"Product family (for scopeType productFamily)","nullable":true},"scopeType":{"type":"string","enum":["singleProduct","productFamily","event","multiplePerformances","venue","selectedTimeslots","selectedPriceCategories"],"description":"Scope Assignment (pack p.77)"},"combinationMode":{"type":"string","enum":["independent","combinable","exclusive","fallback"],"description":"Strategy Combination: independent, combinable with other strategies, exclusive control, or fallback; defaults to independent (decided 29 September, readiness close-out)"},"clonedFromStrategyId":{"type":"string","description":"Strategy this one was cloned from (inherits its rules)","nullable":true}}},
"DynamicPricingStrategyCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Dynamic Pricing Strategy Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeStrategies":{"type":"integer","description":"Active Strategies"},"draftStrategies":{"type":"integer","description":"Draft Strategies"},"productsUnderDynamicPricing":{"type":"integer","description":"Products Under Dynamic Pricing"},"eventsUnderDynamicPricing":{"type":"integer","description":"Events Under Dynamic Pricing"},"performancesUnderDynamicPricing":{"type":"integer","description":"Performances Under Dynamic Pricing"},"rulesActive":{"type":"integer","description":"Rules Active"},"currentPriceAdjustments":{"type":"integer","description":"Current Price Adjustments"},"pricesAtMaximumGuardrail":{"type":"integer","description":"Prices at Maximum Guardrail"},"pricesAtMinimumGuardrail":{"type":"integer","description":"Prices at Minimum Guardrail"},"ruleConflicts":{"type":"integer","description":"Rule Conflicts"},"frozenStrategies":{"type":"integer","description":"Frozen Strategies"},"upcomingActivations":{"type":"integer","description":"Upcoming Activations: strategies scheduled to activate within 7 days (decided 29 September, readiness close-out)"},"operationalAlerts":{"type":"array","items":{"type":"string"},"description":"Operational Alerts (pack p.76), e.g. performances at their upper band, strategies with unresolved conflicts, strategies activating within 48 hours"}}},
"DynamicPricingStrategyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"strategyId":{"type":"string","description":"Strategy ID"},"strategyName":{"type":"string","description":"Strategy Name"},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"],"description":"Strategy Type (pack pp.75-76)"},"productEvent":{"type":"string","description":"Product or event the strategy controls"},"venue":{"type":"string","description":"Venue"},"basePriceSource":{"type":"string","description":"Base price source: the Board 1 price list and rate the strategy moves from, e.g. UAE Standard Admission -> Adult"},"currentPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Current resolved dynamic price (for a single-price scope)","nullable":true},"adjustmentRange":{"type":"object","properties":{"minPercent":{"type":"number","description":"Lowest adjustment from base, percent"},"maxPercent":{"type":"number","description":"Highest adjustment from base, percent"}},"description":"Adjustment range allowed by the strategy"},"ruleCount":{"type":"integer","description":"Rule Count"},"effectivePeriod":{"type":"object","properties":{"from":{"type":"string","format":"date-time","description":"Effective from"},"to":{"type":"string","format":"date-time","description":"Effective to; empty for open-ended","nullable":true}},"description":"Effective period"},"automationMode":{"type":"string","enum":["monitor","recommend","prepareChange","autoExecuteWithinGuardrails"],"description":"Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default"},"status":{"type":"string","description":"Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired"},"owner":{"type":"string","description":"Owner"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceLadder": {"type":"object","x-ticvai-persistence":"catalogue.price_ladder","description":"**The bands a dynamic price may move between, and how fast** (29 September, data model DM3). ADM-092. A strategy's adjustment lands on a band, never between them.","required":["id","scopePath","dynamicPricingStrategyId","adjustmentModel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"dynamicPricingStrategyId":{"type":"string","format":"uuid"},"basePriceSource":{"type":"string","maxLength":100,"nullable":true},"adjustmentModel":{"type":"string","enum":["fixedPriceBands","percentageBands","fixedAmountSteps","derivedBands","continuousRange"]},"bands":{"type":"object","additionalProperties":true,"description":"`[{code, price, percent}]`, ascending."},"baseBandCode":{"type":"string","maxLength":40,"nullable":true},"stepAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"minimumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"basePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"maximumPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"allowUpward":{"type":"boolean","default":true},"allowDownward":{"type":"boolean","default":true},"maxIncreasePercentPerAdjustment":{"type":"number","nullable":true},"maxDecreasePercentPerAdjustment":{"type":"number","nullable":true},"maximumBandsPerMovement":{"type":"integer","nullable":true,"minimum":1},"minimumMinutesBetweenMovements":{"type":"integer","nullable":true,"minimum":0},"cooldownMinutes":{"type":"integer","nullable":true,"minimum":0},"reversalRule":{"type":"string","enum":["allowed","afterCooldown","notAllowed"],"default":"afterCooldown"},"allowedEndpoints":{"type":"array","items":{"type":"string"},"description":"Psychological price endings, e.g. `.99`, `.00`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PricingDynamicPriceRule": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_rule","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule.","required":["pricingRuleCode","name","priority","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"pricingRuleCode":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"integer"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"dynamicPricingStrategyId":{"type":"string","format":"uuid","nullable":true,"description":"The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). Null for a static pricing rule."},"ruleType":{"type":"string","maxLength":40,"nullable":true,"description":"Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`."},"inputMetric":{"type":"string","maxLength":40,"nullable":true},"conditionLogic":{"type":"string","enum":["all","any"],"default":"all"},"cooldownMinutes":{"type":"integer","nullable":true,"minimum":0},"minimumDurationMinutes":{"type":"integer","nullable":true,"minimum":0},"exitThresholdOffset":{"type":"number","nullable":true},"rangeMinPercent":{"type":"number","nullable":true},"rangeMaxPercent":{"type":"number","nullable":true},"isProtected":{"type":"boolean","default":false,"description":"A protected segment or channel: dynamic adjustments never apply."}}},
"SeasonalCalendarDayTimeslotDynamicRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Seasonal, Calendar, Day & Timeslot Dynamic Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"season":{"type":"string","description":"Season name (e.g. Low Season, Peak Season)","nullable":true},"month":{"type":"integer","description":"Month 1-12","nullable":true},"week":{"type":"integer","description":"ISO week 1-53","nullable":true},"dateRange":{"type":"object","properties":{"from":{"type":"string","format":"date","description":"From"},"to":{"type":"string","format":"date","description":"To"}},"description":"Date range","nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]},"description":"Days of week; saturday+sunday for weekend"},"timeOfDay":{"type":"object","properties":{"from":{"type":"string","description":"From, HH:mm"},"to":{"type":"string","description":"To, HH:mm"}},"description":"Time-of-day window","nullable":true},"timeslotIds":{"type":"array","items":{"type":"string"},"description":"Timeslot IDs"},"performanceIds":{"type":"array","items":{"type":"string"},"description":"Performance IDs"},"specialCalendarEntry":{"type":"string","description":"Special-calendar entry (public/school holiday, Ramadan, Eid, custom), maintained as tenant data","nullable":true},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule name"},"strategyId":{"type":"string","description":"Strategy the rule belongs to"},"dimension":{"type":"string","enum":["season","month","week","dateRange","publicHoliday","schoolHoliday","dayOfWeek","weekend","timeOfDay","timeslot","performance","specialDate"],"description":"Supported Dimension (pack p.81)"},"dynamicRangeMinPercent":{"type":"number","description":"Dynamic range low end in percent of base, e.g. -15"},"dynamicRangeMaxPercent":{"type":"number","description":"Dynamic range high end in percent of base, e.g. +20"},"assignedStrategyId":{"type":"string","description":"Strategy applied in this window (Timeslot Rules: 09:00-12:00 -> Off-Peak Strategy)","nullable":true},"overlapsWith":{"type":"array","items":{"type":"string"},"description":"Rule IDs this rule overlaps (Overlap Detection)"},"enabled":{"type":"boolean","description":"Enabled"}}}
}
```
