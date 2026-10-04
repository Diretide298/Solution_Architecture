# WS148 — Payment Payment Orchestration board 2

**10 screens · 9 operations · 8 schemas · 3 permissions**

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
  `PAYMENT_CONFIGURE, PAYMENT_PROVIDER_MANAGE, PAYMENT_VIEW`. A control nobody can use must say so,
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
| `ADM-569` | Payment Orchestration Command Center | C | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-570` | Gateway, PSP & Acquirer Directory | A | 25 | 44 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-571` | Provider Connection & Adapter Configuration | C | 0 | 41 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-572` | Gateway Capability & Payment Method Mapping | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-573` | Payment Routing Rule Builder | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-574` | Routing Strategy, Priority & Load Distribution | C | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-575` | Failover, Retry & Resilience Manager | C | 8 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-576` | Provider Health, SLA & Performance Monitor | C | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-577` | Provider Cost, Commercial & Routing Economics | C | 5 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-578` | Payment Routing Simulator, Decision Trace & AI Advisor | C | 0 | 24 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-572, ADM-578 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-569` Payment Orchestration Command Center

**Provide real-time operational visibility across all payment gateways, PSPs and acquirers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-569 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-orchestration-command-center-t27-adm-569` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Live view of gateways, PSPs and acquirers: authorisation rate, latency, availability.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Payment Orchestration Command Center\t27".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-569; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) getPaymentProviderHealth, listPaymentProviderConnections return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#getPaymentProviderHealth / contracts/satellite/payments.yaml#listPaymentProviderConnections; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentProviderHealth` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Payment Attempts** (metric tile)

**Successful Authorizations** (metric tile)

**Authorization Rate** (metric tile)

**Successful Captures** (metric tile)

**Declined Transactions** (metric tile)

**Technical Failures** (metric tile)

**Routed Transactions** (metric tile)

**Rerouted Transactions** (metric tile)

**Failover Transactions** (metric tile)

**Active Providers** (metric tile)

**Provider Incidents** (metric tile)

**Average Processing Time** (metric tile)

**Every payment orchestration \t27** (data table)

| Shows | Format | Notes |
|---|---|---|
| Attempted value | text | not in the schema: `Attempted Value` |
| Authorized value | text | not in the schema: `Authorized Value` |
| Captured value | text | not in the schema: `Captured Value` |
| Failed value | text | not in the schema: `Failed Value` |
| Rerouted value | text | not in the schema: `Rerouted Value` |

**The selected payment orchestration \t27** (detail panel): The pack groups this record's detail under its own headings: “Provider Value Success Status”, “Provider AED”, “Provider AED Warnin”.

| Shows | Format | Notes |
|---|---|---|
| Attempted value | text | not in the schema: `Attempted Value` |
| Authorized value | text | not in the schema: `Authorized Value` |
| Captured value | text | not in the schema: `Captured Value` |
| Failed value | text | not in the schema: `Failed Value` |
| Rerouted value | text | not in the schema: `Rerouted Value` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **provider health**: Authorisation rate first, then latency and availability. *(source: contracts/satellite/payments.yaml#getPaymentProviderHealth)*

**Data it reads**: `getPaymentProviderHealth` (onLoad, Provider health); `listPaymentProviderConnections` (onLoad, Providers connected)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-570` Gateway, PSP & Acquirer Directory: *Gateway, PSP & Acquirer Directory\t28*
- → `ADM-571` Provider Connection & Adapter Configuration: *Provider Connection & Adapter Configuration\t29*; carries `connectionId`
- → `ADM-572` Gateway Capability & Payment Method Mapping: *Gateway Capability & Payment Method Mapping\t30*
- → `ADM-573` Payment Routing Rule Builder: *Payment Routing Rule Builder\t31*
- → `ADM-574` Routing Strategy, Priority & Load Distribution: *Routing Strategy, Priority & Load Distribution\t33*
- → `ADM-575` Failover, Retry & Resilience Manager: *Failover, Retry & Resilience Manager\t34*
- → `ADM-576` Provider Health, SLA & Performance Monitor: *Provider Health, SLA & Performance Monitor\t35*
- → `ADM-577` Provider Cost, Commercial & Routing Economics: *Provider Cost, Commercial & Routing Economics\t36*
- → `ADM-578` Payment Routing Simulator, Decision Trace & AI Advisor: *Payment Routing Simulator, Decision Trace & AI Advisor\t37*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment orchestration \t27 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment orchestration \t27 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment orchestration \t27 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment orchestration \t27 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
provider:
  name: Network International
  authRate: 95.1%
  p95: 820 ms
```

#### Permissions

- `getPaymentProviderHealth` → `PAYMENT_VIEW` (read) · staff
- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-569` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-569`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 1: Opens Payment Orchestration Command Center\t27 → Provide real-time operational visibility across all payment gateways, PSPs and acquirers.
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F257 branch at step 1 (expected): when Nothing has been set up on Payment Orchestration Command Center\t27 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F257 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-569?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-570`, `ADM-571`, `ADM-572`, `ADM-573`, `ADM-574`, `ADM-575`, `ADM-576`, `ADM-577`, `ADM-578`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-570` Gateway, PSP & Acquirer Directory

**Maintain the centralized directory of payment-processing providers connected to TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 1 · needs the `core` module |
| Block | Block A · ticket #28053 (APP-SETUP-ADM-570) |
| Who uses it | venue staff holding `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): The provider directory with the selected or new connection beside it (defined 4 October 2026 from PaymentProviderConnection, CHG-FXS-001). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/gateway-psp-acquirer-directory-t28-adm-570` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Defined 4 October 2026 from PaymentProviderConnection. The credential is written as a vault reference (credentialRef, write-only; agreed with contracts in the ledger), as setPaymentProvider already does, and read back only as its fingerprint** (CHG-FXS-001)

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The tenant's directory of payment providers (gateways, PSPs, acquirers, wallet and BNPL providers) and what each can do: methods, currencies, partial and multiple capture, refund windows. Capability mapping is the part that gets skipped and later causes an incident, so it is the centre of the screen. Credentials are written and never read back.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- listPaymentProviderConnections returns no described schema. (CHG-MOV-008)
- Pack actions with no operation: Payment Gateway, Wallet Provider, Alternative Payment Provider. (CHG-MOV-008)
- List operation(s) listPaymentProviderConnections return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): The screen name ends in an escaped tab and the pack page number: "Gateway, PSP & Acquirer Directory\t28". (CHG-MOV-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Code | text field | optional | — | — | — | — | `PaymentProviderConnection.code` |
| Name | text field | optional | — | — | — | — | `PaymentProviderConnection.name` |
| Kind | radio group | optional | — | Gateway · Psp · Acquirer · Wallet provider · Bnpl provider | — | Gateway, PSP, acquirer, wallet provider or BNPL provider (the pack's three buttons). | `PaymentProviderConnection.providerKind` |
| Environment | segmented control | optional | — | Sandbox · Production | — | Sandbox first; production after a passing test. | `PaymentProviderConnection.environment` |
| Merchant account | picker: choose a merchant account (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `PaymentProviderConnection.merchantAccountId` |
| Credential reference | text field | optional | — | — | — | The vault reference of the key, write-only; the key itself never passes through a screen (ADR-0020 as applied to payments). Agreed field, ledger. | `PaymentProviderConnection.credentialRef` |

**Sent by *Connect*** (`createPaymentProviderConnection`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createPaymentProviderConnection` body |
| Code `code` | text field | required | — | — | — | — | `createPaymentProviderConnection` body |
| Name `name` | text field | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Provider kind `providerKind` | radio group | required | — | Gateway · Psp · Acquirer · Wallet provider · Bnpl provider | — | — | `createPaymentProviderConnection` body |
| Environment `environment` | segmented control | optional | — | Sandbox · Production | — | — | `createPaymentProviderConnection` body |
| Capabilities `capabilities` | group | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Methods `capabilities.methods` | list of values (chips) | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Currencies `capabilities.currencies` | list of values (chips) | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Partial capture `capabilities.partialCapture` | toggle | optional | off | — | — | — | `createPaymentProviderConnection` body |
| Multiple capture `capabilities.multipleCapture` | toggle | optional | off | — | — | — | `createPaymentProviderConnection` body |
| Refund window days `capabilities.refundWindowDays` | number field (days) | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Tokenisation `capabilities.tokenisation` | toggle | optional | off | — | — | — | `createPaymentProviderConnection` body |
| Three d secure `capabilities.threeDSecure` | toggle | optional | off | — | — | — | `createPaymentProviderConnection` body |
| Card present `capabilities.cardPresent` | toggle | optional | off | — | — | — | `createPaymentProviderConnection` body |
| Merchant account `merchantAccountId` | picker: choose a merchant account | optional | — | — | shows names, sends the id | — | `createPaymentProviderConnection` body |
| Status `status` | radio group | optional | — | Draft · Testing · Active · Degraded · Disabled | — | — | `createPaymentProviderConnection` body |
| Last tested at `lastTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPaymentProviderConnection` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `createPaymentProviderConnection` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | Where the provider credential is kept (4 October 2026, CHG-FXC-010; ADM-570): the vault reference the credential was stored under, as `SetPaymentProviderRequest.credentialRef`. | `createPaymentProviderConnection` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **credentials**: Write-only fields; after save only the fingerprint shows ("key ending ...4f2a, set 1 Oct by Fatima"), with Replace credentials. *(source: contracts/satellite/payments.yaml#createPaymentProviderConnection)*
- **environment**: Sandbox and Production visibly distinct (badge and colour); a production connection starts in Testing until a successful test. *(source: contracts/satellite/payments.yaml#/components/schemas/PaymentProviderConnection)*

#### Outputs: what the screen shows and produces

**Shown**

**Connected providers** (data table, from `listPaymentProviderConnections`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Provider kind | chip: Gateway, Psp, Acquirer, Wallet provider, Bnpl provider | — |
| Environment | chip: Sandbox, Production | — |
| Status | chip: Draft, Testing, Active, Degraded, Disabled | — |
| Last tested at | 1 Oct 2026, 14:30 | — |

**Key in use** (detail panel, from `listPaymentProviderConnections`): The fingerprint, so a person can confirm which key is in use without reading it.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Provider kind | chip: Gateway, Psp, Acquirer, Wallet provider, Bnpl provider | — |
| Environment | chip: Sandbox, Production | — |
| Credential fingerprint | text | Written, never read back. Enough to confirm which key is in use without the key being retrievable from a screen. |
| Capabilities | grouped details | — |
| Methods | list or chips (count when long) | — |
| Currencies | list or chips (count when long) | — |
| Partial capture | yes / no (icon or chip) | — |
| Multiple capture | yes / no (icon or chip) | — |
| Refund window days | 1,234 | — |
| Tokenisation | yes / no (icon or chip) | — |
| Three d secure | yes / no (icon or chip) | — |
| Card present | yes / no (icon or chip) | — |
| Merchant account | the name it points at, never the id | — |
| Status | chip: Draft, Testing, Active, Degraded, Disabled | — |
| Last tested at | 1 Oct 2026, 14:30 | — |
| Credential ref | text | Where the provider credential is kept (4 October 2026, CHG-FXC-010; ADM-570): the vault reference the credential was stored under, as … |

**Capabilities** (detail panel, from `listPaymentProviderConnections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Provider kind | chip: Gateway, Psp, Acquirer, Wallet provider, Bnpl provider | — |
| Environment | chip: Sandbox, Production | — |
| Credential fingerprint | text | Written, never read back. Enough to confirm which key is in use without the key being retrievable from a screen. |
| Capabilities | grouped details | — |
| Methods | list or chips (count when long) | — |
| Currencies | list or chips (count when long) | — |
| Partial capture | yes / no (icon or chip) | — |
| Multiple capture | yes / no (icon or chip) | — |
| Refund window days | 1,234 | — |
| Tokenisation | yes / no (icon or chip) | — |
| Three d secure | yes / no (icon or chip) | — |
| Card present | yes / no (icon or chip) | — |
| Merchant account | the name it points at, never the id | — |
| Status | chip: Draft, Testing, Active, Degraded, Disabled | — |
| Last tested at | 1 Oct 2026, 14:30 | — |
| Credential ref | text | Where the provider credential is kept (4 October 2026, CHG-FXC-010; ADM-570): the vault reference the credential was stored under, as … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Connect a provider (primary button) | navigation or local | — | — | — | — |
| Connect (primary button) | `createPaymentProviderConnection` POST `/payment-providers` | PaymentProviderConnection | PaymentProviderConnection | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **capability matrix**: Providers as rows, capabilities as columns (card, Apple Pay, Google Pay, AED, OMR, partial capture, multi-capture, refund window) with ticks. *(source: contracts/satellite/payments.yaml#listPaymentProviderConnections)*

**Data it reads**: `listPaymentProviderConnections` (onLoad, The directory)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No providers connected yet. Carries Connect a provider. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gateway psp acquirer are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PAYMENT_VIEW`, which `listPaymentProviderConnections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PAYMENT_PROVIDER_MANAGE` for `createPaymentProviderConnection`. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
providers:
- code: NI-PROD
  name: Network International
  kind: gateway
  environment: production
  status: active
  fingerprint: …4f2a
- code: STRIPE-SBX
  name: Stripe
  kind: psp
  environment: sandbox
  status: testing
```

#### Permissions

- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff
- `createPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PAYMENT_VIEW`, which `listPaymentProviderConnections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PAYMENT_PROVIDER_MANAGE` for `createPaymentProviderConnection`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-570` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-570`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 2: Works in Gateway, PSP & Acquirer Directory\t28 → Maintain the centralized directory of payment-processing providers connected to TICVAI.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state.
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-570?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Connect a provider, Connect, Cancel.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-571` Provider Connection & Adapter Configuration

**Configure how TICVAI technically connects to each payment provider.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-571 |
| Who uses it | venue staff holding `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `connectionId` (navigation) |
| Route | `/commercial/provider-connection-adapter-configuration-t29-adm-571` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Technical connection to each provider, tested before anyone pays through it; credentials never read back.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Provider Connection & Adapter Configuration\t29".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-571; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-571; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createPaymentProviderConnection, testPaymentProviderConnection and nothing that returns the … (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every provider connection adapter** (data table)

| Shows | Format | Notes |
|---|---|---|
| TICVAI adapter | text | not in the schema: `TICVAI Adapter` |
| Adapter version | text | not in the schema: `Adapter Version` |
| Provider API version | text | not in the schema: `Provider API Version` |
| Deployment version | text | not in the schema: `Deployment Version` |
| Last certification/test | text | not in the schema: `Last Certification/Test` |
| Status | text | not in the schema: `Status` |
| Credential status | text | not in the schema: `Credential status` |
| Last rotation | text | not in the schema: `Last rotation` |
| Expiry | text | not in the schema: `Expiry` |
| Certificate expiry | text | not in the schema: `Certificate expiry` |
| Owner | text | not in the schema: `Owner` |

**Connections** (data table, from `listPaymentProviderConnections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Provider kind | chip: Gateway, Psp, Acquirer, Wallet provider, Bnpl provider | — |
| Environment | chip: Sandbox, Production | — |
| Credential fingerprint | text | Written, never read back. Enough to confirm which key is in use without the key being retrievable from a screen. |
| Capabilities | grouped details | — |
| Methods | list or chips (count when long) | — |
| Currencies | list or chips (count when long) | — |
| Partial capture | yes / no (icon or chip) | — |
| Multiple capture | yes / no (icon or chip) | — |
| Refund window days | 1,234 | — |
| Tokenisation | yes / no (icon or chip) | — |
| Three d secure | yes / no (icon or chip) | — |
| Card present | yes / no (icon or chip) | — |
| Merchant account | the name it points at, never the id | — |
| Status | chip: Draft, Testing, Active, Degraded, Disabled | — |
| Last tested at | 1 Oct 2026, 14:30 | — |
| Credential ref | text | Where the provider credential is kept (4 October 2026, CHG-FXC-010; ADM-570): the vault reference the credential was stored under, as … |

**The selected provider connection adapter** (detail panel): The pack groups this record's detail under its own headings: “Credential Management”, “Never expose full”, “Result”.

| Shows | Format | Notes |
|---|---|---|
| TICVAI adapter | text | not in the schema: `TICVAI Adapter` |
| Adapter version | text | not in the schema: `Adapter Version` |
| Provider API version | text | not in the schema: `Provider API Version` |
| Deployment version | text | not in the schema: `Deployment Version` |
| Last certification/test | text | not in the schema: `Last Certification/Test` |
| Status | text | not in the schema: `Status` |
| Credential status | text | not in the schema: `Credential status` |
| Last rotation | text | not in the schema: `Last rotation` |
| Expiry | text | not in the schema: `Expiry` |
| Certificate expiry | text | not in the schema: `Certificate expiry` |
| Owner | text | not in the schema: `Owner` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| API endpoint reference (primary button) | navigation or local | — | — | — | — |
| Webhook configuration (secondary button) | navigation or local | — | — | — | — |
| Callback configuration (secondary button) | navigation or local | — | — | — | — |
| Retry configuration (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Test connection**: Runs the test transactions; the result is stored with the time. *(source: contracts/satellite/payments.yaml#testPaymentProviderConnection)*

**Data it reads**: `listPaymentProviderConnections` (onLoad, The provider connections already configured)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider connection adapter list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider connection adapter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider connection adapter yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provider connection adapter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-570`: Same provider records.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
connection:
  provider: Stripe
  environment: sandbox
  test: passed 10:12
```

#### Permissions

- `createPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff
- `testPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff
- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-571` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-571`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 4: Works in Provider Connection & Adapter Configuration\t29 → Configure how TICVAI technically connects to each payment provider.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-571?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-572` Gateway Capability & Payment Method Mapping

**Map Board 1 payment methods to providers capable of processing them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-572 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/gateway-capability-payment-method-mapping-t30-adm-572` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which providers can process which methods and currencies.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Gateway Capability & Payment Method Mapping\t30".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-572; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listPaymentProviderConnections return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#listPaymentProviderConnections; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **capability matrix**: As ADM-570. *(source: contracts/satellite/payments.yaml#listPaymentProviderConnections)*

**Data it reads**: `listPaymentProviderConnections` (onLoad, Capability against method)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gateway capability payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gateway capability payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gateway capability payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gateway capability payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  method: Apple Pay
  providers:
  - Network International
  - Stripe
```

#### Permissions

- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-572` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-572`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 6: Works in Gateway Capability & Payment Method Mapping\t30 → Map Board 1 payment methods to providers capable of processing them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-572?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-573` Payment Routing Rule Builder

**Configure the rules that determine which provider should receive each payment transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-573 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-routing-rule-builder-t31-adm-573` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where … **Payment Routing Rule Builder\t31 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules deciding which provider takes each transaction (method, currency, venue, amount, cost, share).

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Payment Routing Rule Builder\t31".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-573; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where appropriate, Weighted distribution.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-573; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listPaymentRoutingRules return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#listPaymentRoutingRules; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **routing rules**: Ordered rules with conditions and target. *(source: contracts/satellite/payments.yaml#setPaymentRoutingRules)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Legal entity (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Payment method (secondary button) | navigation or local | — | — | — | — |
| Transaction amount (secondary button) | navigation or local | — | — | — | — |
| Transaction type (secondary button) | navigation or local | — | — | — | — |
| Customer type where appropriate (secondary button) | navigation or local | — | — | — | — |
| Weighted distribution (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentRoutingRules` (onLoad, Rules in force)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment routing rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment routing rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment routing rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment routing rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A rule routes to a provider that cannot take it |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: 'AED cards at Dune Park: Network International; foreign cards: Stripe'
```

#### Permissions

- `setPaymentRoutingRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `listPaymentRoutingRules` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-573` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-573`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 8: Works in Payment Routing Rule Builder\t31 → Configure the rules that determine which provider should receive each payment transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-573?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where appropriate, Weighted distribution.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-574` Routing Strategy, Priority & Load Distribution

**Manage how payment traffic is distributed when several valid providers are available.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-574 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§AED Card / B2C) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/routing-strategy-priority-load-distribution-t33-adm-574` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Priority and load distribution among valid providers; priority and share are different things.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Routing Strategy, Priority & Load Distribution\t33".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-574; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setPaymentRoutingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **distribution**: Priority order and percentage shares, shares totalling 100. *(source: contracts/satellite/payments.yaml#setPaymentRoutingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Provider A: 60%** (metric tile)

**Provider B: 30%** (metric tile)

**Provider C: 10%** (metric tile)

**Routing rules** (data table, from `listPaymentRoutingRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Priority | 1,234 | — |
| Conditions | grouped details | — |
| Methods | list or chips (count when long) | — |
| Currencies | list or chips (count when long) | — |
| Venues | list or chips (count when long) | — |
| Channels | list or chips (count when long) | — |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Card schemes | list or chips (count when long) | — |
| Card issuer countries | list or chips (count when long) | — |
| Targets | list or chips (count when long) | — |
| Connection | the name it points at, never the id | — |
| Share percent | 1,234 | — |
| Rank | 1,234 | — |
| Strategy | chip: Priority order, Load share, Lowest cost, Highest auth rate | — |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listPaymentRoutingRules` (onLoad, Which provider takes which transaction)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The routing strategy priority list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the routing strategy priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No routing strategy priority yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the routing strategy priority are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A rule routes to a provider that cannot take it |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
shares:
  Network International: 70%
  Stripe: 30%
```

#### Permissions

- `setPaymentRoutingRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `listPaymentRoutingRules` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-574` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-574`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 10: Works in Routing Strategy, Priority & Load Distribution\t33 → Manage how payment traffic is distributed when several valid providers are available.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-574?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-575` Failover, Retry & Resilience Manager

**Maintain payment availability when a provider experiences a technical problem. This is one of the most important screens in the Payment Orchestration module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-575 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/failover-retry-resilience-manager-t34-adm-575` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Failover, Retry & Resilience Manager\t34 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of the payment failover policy (setPaymentFailoverPolicy has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Failover when a provider fails; a declined card and a broken gateway need opposite responses.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Failover, Retry & Resilience Manager\t34".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-575; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setPaymentFailoverPolicy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary provider | select field | — | — | — | — | — | — |
| Secondary provider | select field | — | — | — | — | — | — |
| Tertiary provider | select field | — | — | — | — | — | — |
| Trigger condition | select field | — | — | — | — | — | — |
| Retry limit | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Cooldown | select field | — | — | — | — | — | — |
| Recovery behavior | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **failover**: Retry on technical failure only, never on a decline; stop conditions. *(source: contracts/satellite/payments.yaml#setPaymentFailoverPolicy)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The failover retry resilience configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the failover retry resilience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No failover retry resilience configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  retryOn:
  - timeout
  - 5xx
  neverRetry:
  - declined
  maxRetries: 1
```

#### Permissions

- `setPaymentFailoverPolicy` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-575` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-575`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 12: Works in Failover, Retry & Resilience Manager\t34 → Maintain payment availability when a provider experiences a technical problem. This is one of the most important screens in the Payment Orchestration module.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-575?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-576` Provider Health, SLA & Performance Monitor

**Monitor each provider's technical and transactional health.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-576 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Health Metrics) and a per-row directory (§Compare) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/provider-health-sla-performance-monitor-t35-adm-576` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Each provider's technical and transactional health against SLA.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Provider Health, SLA & Performance Monitor\t35".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-576; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) getPaymentProviderHealth return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#getPaymentProviderHealth; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentProviderHealth` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Availability** (metric tile)

**Authorization rate** (metric tile)

**Capture rate** (metric tile)

**Decline rate** (metric tile)

**Technical error rate** (metric tile)

**Timeout rate** (metric tile)

**Average latency** (metric tile)

**95th and 99th percentile latency where available** (metric tile)

**Webhook delay** (metric tile)

**Refund API health** (metric tile)

**Every provider health sla** (data table)

| Shows | Format | Notes |
|---|---|---|
| Today | text | not in the schema: `Today` |
| Yesterday | text | not in the schema: `Yesterday` |
| 7 days | text | not in the schema: `7 Days` |
| 30 days | text | not in the schema: `30 Days` |
| Historical baseline | text | not in the schema: `Historical baseline` |

**The selected provider health sla** (detail panel): The pack groups this record's detail under its own headings: “Health State”, “Authorization Rate”, “Normal Baseline”, “Change”.

| Shows | Format | Notes |
|---|---|---|
| Today | text | not in the schema: `Today` |
| Yesterday | text | not in the schema: `Yesterday` |
| 7 days | text | not in the schema: `7 Days` |
| 30 days | text | not in the schema: `30 Days` |
| Historical baseline | text | not in the schema: `Historical baseline` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **health**: Authorisation rate, latency, availability over time. *(source: contracts/satellite/payments.yaml#getPaymentProviderHealth)*

**Data it reads**: `getPaymentProviderHealth` (onLoad, Authorisation rate and latency)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider health sla list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider health sla untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider health sla yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provider health sla are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sla:
  provider: Stripe
  availability: 99.97%
```

#### Permissions

- `getPaymentProviderHealth` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-576` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-576`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 14: Works in Provider Health, SLA & Performance Monitor\t35 → Monitor each provider's technical and transactional health.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-576?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-577` Provider Cost, Commercial & Routing Economics

**Allow TICVAI to understand the commercial cost of routing transactions through different providers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-577 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator may define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/provider-cost-commercial-routing-economics-t36-adm-577` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What each provider actually costs per transaction (scheme fees, interchange, acquirer margin); a routing input.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Provider Cost, Commercial & Routing Economics\t36".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-577; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) getPaymentProviderEconomics return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#getPaymentProviderEconomics; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximize Authorization | select field | — | — | — | — | — | — |
| Minimize Cost | select field | — | — | — | — | — | — |
| Minimize Latency | select field | — | — | — | — | — | — |
| Balanced | select field | — | — | — | — | — | — |
| Custom Governed Strategy | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getPaymentProviderEconomics` ?from |
| To | date picker | — | — | `getPaymentProviderEconomics` ?to |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **economics**: Cost per transaction by provider and method. *(source: contracts/satellite/payments.yaml#getPaymentProviderEconomics)*

**Data it reads**: `getPaymentProviderEconomics` (onLoad, What each provider costs)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider cost commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider cost commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider cost commercial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cost:
  provider: Network International
  perTransaction: AED 1.84
```

#### Permissions

- `getPaymentProviderEconomics` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-577` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-577`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 16: Works in Provider Cost, Commercial & Routing Economics\t36 → Allow TICVAI to understand the commercial cost of routing transactions through different providers.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-577?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-578` Payment Routing Simulator, Decision Trace & AI Advisor

**Allow administrators to test exactly how a payment will be routed before deploying routing changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-578 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Credit Card can route through) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-routing-simulator-decision-trace-ai-advisor-t37-adm-578` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a transaction would go and why, including the rules that did not match.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Payment Routing Simulator, Decision Trace & AI Advisor\t37".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-578; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only simulatePaymentRouting and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment routing simulator** (data table)

| Shows | Format | Notes |
|---|---|---|
| Provider a | text | not in the schema: `Provider A` |
| Provider b | text | not in the schema: `Provider B` |
| Provider c | text | not in the schema: `Provider C` |

**Routing rules** (data table, from `listPaymentRoutingRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Priority | 1,234 | — |
| Conditions | grouped details | — |
| Methods | list or chips (count when long) | — |
| Currencies | list or chips (count when long) | — |
| Venues | list or chips (count when long) | — |
| Channels | list or chips (count when long) | — |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Card schemes | list or chips (count when long) | — |
| Card issuer countries | list or chips (count when long) | — |
| Targets | list or chips (count when long) | — |
| Connection | the name it points at, never the id | — |
| Share percent | 1,234 | — |
| Rank | 1,234 | — |
| Strategy | chip: Priority order, Load share, Lowest cost, Highest auth rate | — |
| Is active | yes / no (icon or chip) | — |

**The selected payment routing simulator** (detail panel): The pack groups this record's detail under its own headings: “AED 720”, “Provider A”, “Provider B”, “Provider C”, “Payment Request”, “Payment Method”.

| Shows | Format | Notes |
|---|---|---|
| Provider a | text | not in the schema: `Provider A` |
| Provider b | text | not in the schema: `Provider B` |
| Provider c | text | not in the schema: `Provider C` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate route**: Decision trace rule by rule. *(source: contracts/satellite/payments.yaml#simulatePaymentRouting)*

**Data it reads**: `listPaymentRoutingRules` (onLoad, The routing rules the simulation runs against)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment routing simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment routing simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment routing simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment routing simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trace:
- 'Rule 1 foreign cards: no match'
- 'Rule 2 AED cards: matched, Network International'
```

#### Permissions

- `simulatePaymentRouting` → `PAYMENT_VIEW` (read) · staff
- `listPaymentRoutingRules` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-578` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-578`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 18: Works in Payment Routing Simulator, Decision Trace & AI Advisor\t37 → Allow administrators to test exactly how a payment will be routed before deploying routing changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-578?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createPaymentProviderConnection": {"method":"POST","path":"/payment-providers","contract":"payments","summary":"Connect a provider","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PaymentProviderConnection","responds":"PaymentProviderConnection"},
"getPaymentProviderEconomics": {"method":"GET","path":"/payment-providers/economics","contract":"payments","summary":"What each provider actually costs","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ProviderEconomics"},
"getPaymentProviderHealth": {"method":"GET","path":"/payment-providers/health","contract":"payments","summary":"Authorisation rate, latency and availability, per provider","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"ProviderHealth"},
"listPaymentProviderConnections": {"method":"GET","path":"/payment-providers","contract":"payments","summary":"Gateways, PSPs and acquirers, and what each can do","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PaymentProviderConnection"},
"listPaymentRoutingRules": {"method":"GET","path":"/payment-routing-rules","contract":"payments","summary":"Which provider takes which transaction","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PaymentRoutingRule"},
"setPaymentFailoverPolicy": {"method":"PUT","path":"/payment-failover-policy","contract":"payments","summary":"What happens when a provider fails, and when to stop trying","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentFailoverPolicy","responds":"PaymentFailoverPolicy"},
"setPaymentRoutingRules": {"method":"PUT","path":"/payment-routing-rules","contract":"payments","summary":"Route by method, currency, venue, amount, cost or share","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentRoutingRule"},
"simulatePaymentRouting": {"method":"POST","path":"/payment-routing/simulate","contract":"payments","summary":"Where would this transaction go, and why","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"RoutingDecision"},
"testPaymentProviderConnection": {"method":"POST","path":"/payment-providers/{connectionId}/test","contract":"payments","summary":"Prove the connection works before anybody pays through it","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProviderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"PaymentFailoverPolicy": {"type":"object","x-ticvai-persistence":"payments.failover_policy","description":"Board 2.7. **A decline is final; a timeout is not. Retrying the first is how a guest gets charged twice.**\n","properties":{"retryableOutcomes":{"type":"array","items":{"type":"string","enum":["timeout","connectionRefused","providerError5xx","rateLimited","issuerUnavailable"]},"description":"**Explicit, rather than \"anything that was not a success\".**"},"maxAttempts":{"type":"integer","default":2},"backoffMs":{"type":"integer","default":500},"failoverToNextProvider":{"type":"boolean","default":true},"circuitBreaker":{"type":"object","description":"**A hundred tills each discovering an outage independently is a hundred queues.**\n","properties":{"failureThresholdPercent":{"type":"number","default":25},"windowSeconds":{"type":"integer","default":60},"minimumSample":{"type":"integer","default":20},"openForSeconds":{"type":"integer","default":300},"alertOnOpen":{"type":"boolean","default":true}}},"scopePath":{"type":"string"}}},
"PaymentProviderConnection": {"type":"object","x-ticvai-persistence":"payments.provider_connection","description":"Boards 2.2 and 2.4. **Capability mapping is the part that gets skipped.**","required":["code","providerKind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"providerKind":{"type":"string","enum":["gateway","psp","acquirer","walletProvider","bnplProvider"]},"environment":{"type":"string","enum":["sandbox","production"]},"credentialFingerprint":{"type":"string","readOnly":true,"description":"**Written, never read back.** Enough to confirm which key is in use without the key being retrievable from a screen.\n"},"capabilities":{"type":"object","properties":{"methods":{"type":"array","items":{"type":"string"}},"currencies":{"type":"array","items":{"type":"string"}},"partialCapture":{"type":"boolean","default":false},"multipleCapture":{"type":"boolean","default":false},"refundWindowDays":{"type":"integer","nullable":true},"tokenisation":{"type":"boolean","default":false},"threeDSecure":{"type":"boolean","default":false},"cardPresent":{"type":"boolean","default":false}}},"merchantAccountId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","testing","active","degraded","disabled"]},"lastTestedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"},"credentialRef":{"type":"string","writeOnly":true,"description":"**Where the provider credential is kept** (4 October 2026, CHG-FXC-010; ADM-570): the vault reference the credential was stored under, as `SetPaymentProviderRequest.credentialRef`. Sent on create, never returned; `credentialFingerprint` is what reads show."}}},
"PaymentRoutingRule": {"type":"object","x-ticvai-persistence":"payments.routing_rule","description":"Boards 2.5 and 2.6. **Priority and distribution are both needed.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"priority":{"type":"integer","default":0},"conditions":{"type":"object","properties":{"methodIds":{"type":"array","items":{"type":"string","format":"uuid"}},"currencies":{"type":"array","items":{"type":"string"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"channels":{"type":"array","items":{"type":"string"}},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"cardSchemes":{"type":"array","items":{"type":"string"}},"cardIssuerCountries":{"type":"array","items":{"type":"string"}}}},"targets":{"type":"array","items":{"type":"object","properties":{"connectionId":{"type":"string","format":"uuid"},"sharePercent":{"type":"integer","nullable":true},"rank":{"type":"integer"}}}},"strategy":{"type":"string","enum":["priorityOrder","loadShare","lowestCost","highestAuthRate"],"default":"priorityOrder"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ProviderEconomics": {"type":"object","description":"Board 2.9. **Cost per transaction is a routing input.**","properties":{"connectionId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"transactions":{"type":"integer"},"grossVolume":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"schemeFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"interchange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerMargin":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fxSpread":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargebackCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"effectiveRatePercent":{"type":"number"}}},
"ProviderHealth": {"type":"object","description":"Board 2.8. **Authorisation rate is the number, and it is not uptime.**","properties":{"connectionId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"transactions":{"type":"integer"},"authorisationRate":{"type":"number"},"baselineAuthorisationRate":{"type":"number","nullable":true},"declineRate":{"type":"number"},"errorRate":{"type":"number"},"p50LatencyMs":{"type":"integer"},"p95LatencyMs":{"type":"integer"},"circuitState":{"type":"string","enum":["closed","open","halfOpen"]},"status":{"type":"string","enum":["healthy","degraded","failing","disabled"]}}},
"ProviderTestResult": {"type":"object","description":"Board 3.10. **A provider configured and never tested fails on the first real transaction.**\n","properties":{"connectionId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["credentials","authorise","capture","refund","void","tokenise","webhook"]},"passed":{"type":"boolean"},"latencyMs":{"type":"integer","nullable":true},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}},
"RoutingDecision": {"type":"object","description":"Board 2.10. **Includes the rules that did not match**, because routing that is subtly wrong still succeeds.\n","properties":{"chosenConnectionId":{"type":"string","format":"uuid","nullable":true},"chosenProviderName":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"trace":{"type":"array","items":{"type":"object","properties":{"ruleCode":{"type":"string"},"matched":{"type":"boolean"},"skippedBecause":{"type":"string","nullable":true},"candidateConnectionId":{"type":"string","format":"uuid","nullable":true}}}},"fallbackChain":{"type":"array","items":{"type":"string","format":"uuid"}}}}
}
```
