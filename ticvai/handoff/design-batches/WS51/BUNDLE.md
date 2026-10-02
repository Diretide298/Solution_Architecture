# WS51 — Promotions   Bundles Management board 7

**10 screens · 9 operations · 9 schemas · 1 permissions**

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
| `ADM-198` | Targeting & Eligibility Command Center | B–D | 2 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-199` | Eligibility Rule Builder | A | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-200` | CRM & Customer Segment Manager | B–D | 0 | 16 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-201` | Membership, Loyalty & Guest Eligibility | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-202` | Behavioral & Transaction Targeting | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-203` | Context, Location, Channel & Time Targeting | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-204` | Partner, B2B & Payment Eligibility | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-205` | Audience Preview, Reach & Eligibility Simulator | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-206` | Targeting Conflict, Frequency & Exclusion Controls | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-207` | AI Audience Discovery & Targeting Optimization | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-199, ADM-200, ADM-201, ADM-203, ADM-204, ADM-207 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-198` Targeting & Eligibility Command Center

**Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Each rule shows) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/targeting-eligibility-command-center-adm-198` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All promotion audiences, eligibility rules and targeting strategies with performance.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listTargetingEligibility return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listTargetingEligibility carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listTargetingEligibility; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search targeting eligibility | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by guest type, crm segment, membership, loyalty, demographic, behavioral and 8 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Guest type | text field | — | — | `listTargetingEligibility` ?guestType |
| Crm segment | text field | — | — | `listTargetingEligibility` ?crmSegment |
| Membership | text field | — | — | `listTargetingEligibility` ?membership |
| Loyalty | text field | — | — | `listTargetingEligibility` ?loyalty |
| Demographic | text field | — | — | `listTargetingEligibility` ?demographic |
| Behavioral | text field | — | — | `listTargetingEligibility` ?behavioral |
| Transaction | text field | — | — | `listTargetingEligibility` ?transaction |
| Geographic | text field | — | — | `listTargetingEligibility` ?geographic |
| Channel | text field | — | — | `listTargetingEligibility` ?channel |
| Partner | text field | — | — | `listTargetingEligibility` ?partner |
| B2B | text field | — | — | `listTargetingEligibility` ?b2b |
| Payment | text field | — | — | `listTargetingEligibility` ?payment |
| Contextual | text field | — | — | `listTargetingEligibility` ?contextual |
| AI generated | text field | — | — | `listTargetingEligibility` ?aiGenerated |

#### Outputs: what the screen shows and produces

**Shown**

**Active Targeting Rules** (metric tile)

**Active Segments** (metric tile)

**Promotions Using Targeting** (metric tile)

**Bundles Using Targeting** (metric tile)

**Eligible Customers** (metric tile)

**Targeted Customers** (metric tile)

**Personalized Offers** (metric tile)

**Eligibility Pass Rate** (metric tile)

**Conversion Rate** (metric tile)

**Targeted Revenue** (metric tile)

**AOV Uplift** (metric tile)

**AI-Recommended Segments** (metric tile)

**Every targeting eligibility** (data table, from `listTargetingEligibility`)

| Shows | Format | Notes |
|---|---|---|
| Rule health | chip: Healthy, Warning, Conflict, No audience, Oversized audience, Expired… | Health of the targeting rule. |

**The selected targeting eligibility** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Rule health | chip: Healthy, Warning, Conflict, No audience, Oversized audience, Expired… | Health of the targeting rule. |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **targeting overview**: Audiences with size and the promotions using them. *(source: contracts/satellite/promotions.yaml#listTargetingEligibility)*

**Data it reads**: `listTargetingEligibility` (onLoad, Targeting & Eligibility Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-200` CRM & Customer Segment Manager: *Works in CRM & Customer Segment Manager*; calls `listTargetingEligibility`
- → `ADM-201` Membership, Loyalty & Guest Eligibility: *Works in Membership, Loyalty & Guest Eligibility*; calls `listTargetingEligibility`
- → `ADM-202` Behavioral & Transaction Targeting: *Works in Behavioral & Transaction Targeting*; calls `listTargetingEligibility`
- → `ADM-203` Context, Location, Channel & Time Targeting: *Works in Context, Location, Channel & Time Targeting*; calls `listTargetingEligibility`
- → `ADM-204` Partner, B2B & Payment Eligibility: *Works in Partner, B2B & Payment Eligibility*; calls `listTargetingEligibility`
- → `ADM-205` Audience Preview, Reach & Eligibility Simulator: *Works in Audience Preview, Reach & Eligibility Simulator*; calls `listTargetingEligibility`
- → `ADM-206` Targeting Conflict, Frequency & Exclusion Controls: *Works in Targeting Conflict, Frequency & Exclusion Controls*; calls `listTargetingEligibility`
- → `ADM-207` AI Audience Discovery & Targeting Optimization: *Works in AI Audience Discovery & Targeting Optimization*; calls `listTargetingEligibility`
- → `ADM-199` Eligibility Rule Builder: *Works in Eligibility Rule Builder, a section of BO-010, which saves the record with createPromotion…*; calls `listTargetingEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targeting eligibility list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targeting eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targeting eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the targeting eligibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
audience:
  name: Annual pass holders
  size: 18400
  promotions: 3
```

#### Permissions

- `listTargetingEligibility` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-198` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-198`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 1: Opens Targeting & Eligibility Command Center → Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F160 branch at step 1 (expected): when Nothing has been set up on Targeting & Eligibility Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F160 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-198?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-200`, `ADM-201`, `ADM-202`, `ADM-203`, `ADM-204`, `ADM-205`, `ADM-206`, `ADM-207`, `ADM-199`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-199` Eligibility Rule Builder

**Provide a no-code rule engine for determining promotion eligibility. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20657 (APP-SETUP-ADM-199) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/eligibility-rule-builder-adm-199` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setEligibilityRule` duplicated BO-010 Promotions & Coupons's createPromotion, so it is removed from the contract (BC-017) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Multiple condition sets. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who a promotion is for: guest type, segment, age category, membership, loyalty tier, purchase and visit history, basket value, product bought, channel, venue, partner, time, payment method, campaign, account attributes; groups of conditions combined, each group including or excluding. This is promotion eligibility, not product eligibility (BO-161).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Multiple condition sets. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): The screen also writes setResaleEligibilityRule (which tickets may enter resale) with ORDER_CREATE. (CHG-WIR-025); No read operation: the screen declares only setEligibilityRule, setResaleEligibilityRule and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **condition groups**: A query builder (field, operator, value) with AND inside a group and the group's effect (include or exclude); all criteria must match by default. *(source: contracts/satellite/promotions.yaml#/components/schemas/EligibilityRuleBuilderInput / R096)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Multiple condition sets (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The eligibility rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the eligibility rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No eligibility rule yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the eligibility rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  groups:
  - effect: include
    conditions:
    - loyalty tier is Gold or Platinum
    - channel is App
  - effect: exclude
    conditions:
    - guest type is Staff
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-010 Promotions & Coupons requires; this section has no operation of its own since its writer was retired, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-199` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-199`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 2: Works in Eligibility Rule Builder, a section of BO-010, which saves the record with createPromotion (setEligibilityRule … → Provide a no-code rule engine for determining promotion eligibility.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-199?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Multiple condition sets, Cancel.
- [ ] Every transition is wired: `ADM-198`, `BO-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-200` CRM & Customer Segment Manager

**Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.**

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
| Route | `/commercial/crm-customer-segment-manager-adm-200` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **CRM & Customer Segment Manager declares no operation that writes anything** — its only declared call is `listCrmCustomerSegment`, a read. The name promises authoring and the contract offers none …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promotion eligibility uses CRM segments rather than recreating CRM.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCrmCustomerSegment return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCrmCustomerSegment carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCrmCustomerSegment; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **No write operation: a configuration screen (CRM & Customer Segment Manager) declares only reads (listCrmCustomerSegment).** Why: Nothing it shows can be changed from it; either it is a view (and its edits happen on the record editor, which it should link to) or a write is missing. *(source: contracts/satellite/promotions.yaml#listCrmCustomerSegment; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every crm customer segment** (data table, from `listCrmCustomerSegment`)

| Shows | Format | Notes |
|---|---|---|
| Segment name | text | Segment name |
| Source | chip: Ticvai crm, Imported segment, External crm, External cdp, Membership, Loyalty… | Where the segment comes from. |
| Estimated audience | text | Estimated audience |
| Last refreshed | 1 Oct 2026, 14:30 | Last refreshed |
| Promotions using segment | text | Promotions using segment |
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Status | 1,234 | Status |

**The selected crm customer segment** (detail panel): The pack groups this record's detail under its own headings: “Segment Sources”.

| Shows | Format | Notes |
|---|---|---|
| Segment name | text | Segment name |
| Source | chip: Ticvai crm, Imported segment, External crm, External cdp, Membership, Loyalty… | Where the segment comes from. |
| Estimated audience | text | Estimated audience |
| Last refreshed | 1 Oct 2026, 14:30 | Last refreshed |
| Promotions using segment | text | Promotions using segment |
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Status | 1,234 | Status |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **segments**: CRM segments with size, linked promotions. *(source: contracts/satellite/promotions.yaml#listCrmCustomerSegment)*

**Data it reads**: `listCrmCustomerSegment` (onLoad, CRM & Customer Segment Manager)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listCrmCustomerSegment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The crm customer segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the crm customer segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No crm customer segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the crm customer segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-761`: Segments come from marketing (customer-marketing process).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment:
  name: Lapsed families 6 months
  size: 4210
```

#### Permissions

- `listCrmCustomerSegment` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-200` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-200`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 4: Works in CRM & Customer Segment Manager → Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-200?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-201` Membership, Loyalty & Guest Eligibility

**Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.**

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
| Route | `/commercial/membership-loyalty-guest-eligibility-adm-201` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Targeting by membership, loyalty status and guest category.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listMembershipLoyaltyGuest return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listMembershipLoyaltyGuest carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listMembershipLoyaltyGuest; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rules**: Membership and tier conditions. *(source: contracts/satellite/promotions.yaml#listMembershipLoyaltyGuest)*

**Data it reads**: `listMembershipLoyaltyGuest` (onLoad, Membership, Loyalty & Guest Eligibility)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listMembershipLoyaltyGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership loyalty guest list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership loyalty guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership loyalty guest yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership loyalty guest are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Gold and Platinum members
```

#### Permissions

- `listMembershipLoyaltyGuest` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-201` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-201`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 6: Works in Membership, Loyalty & Guest Eligibility → Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-201?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-202` Behavioral & Transaction Targeting

**Target promotions according to what the guest has previously purchased or done.**

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
| Route | `/commercial/behavioral-transaction-targeting-adm-202` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Targeting by what the guest bought or did before.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listBehavioralTransactionTargeting return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBehavioralTransactionTargeting carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBehavioralTransactionTargeting; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Last 7 days | select field | — | — | — | — | — | — |
| 30 days | select field | — | — | — | — | — | — |
| 90 days | select field | — | — | — | — | — | — |
| 12 months | select field | — | — | — | — | — | — |
| Lifetime | select field | — | — | — | — | — | — |
| Custom period | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **behaviour rules**: Condition and lookback window. *(source: contracts/satellite/promotions.yaml#listBehavioralTransactionTargeting)*

**Data it reads**: `listBehavioralTransactionTargeting` (onLoad, Behavioral & Transaction Targeting)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listBehavioralTransactionTargeting`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The behavioral transaction targeting configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the behavioral transaction targeting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No behavioral transaction targeting configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Bought a Day Pass in the last 90 days, no visit since
```

#### Permissions

- `listBehavioralTransactionTargeting` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-202` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-202`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 8: Works in Behavioral & Transaction Targeting → Target promotions according to what the guest has previously purchased or done.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-202?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-203` Context, Location, Channel & Time Targeting

**Determine promotion eligibility according to the customer's current commercial context.**

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
| Route | `/commercial/context-location-channel-time-targeting-adm-203` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Product currently viewed, Current booking. Each needs an operation, or needs removing from the screen; this … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Eligibility by current context: location, channel, time.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Product currently viewed, Current booking.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-203; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listContextLocationChannel return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listContextLocationChannel carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listContextLocationChannel; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product currently viewed (primary button) | navigation or local | — | — | — | — |
| Current booking (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **context rules**: Context conditions. *(source: contracts/satellite/promotions.yaml#listContextLocationChannel)*

**Data it reads**: `listContextLocationChannel` (onLoad, Context, Location, Channel & Time Targeting)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listContextLocationChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The context location channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the context location channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No context location channel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the context location channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: In the park, App, after 16:00
```

#### Permissions

- `listContextLocationChannel` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-203` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-203`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 10: Works in Context, Location, Channel & Time Targeting → Determine promotion eligibility according to the customer's current commercial context.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-203?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product currently viewed, Current booking.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-204` Partner, B2B & Payment Eligibility

**Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.**

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
| Route | `/commercial/partner-b2b-payment-eligibility-adm-204` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Eligibility for partner, corporate, reseller, B2B and payment campaigns.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listPartnerPaymentEligibility return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPartnerPaymentEligibility carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listPartnerPaymentEligibility; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **partner rules**: Partner and payment conditions. *(source: contracts/satellite/promotions.yaml#listPartnerPaymentEligibility)*

**Data it reads**: `listPartnerPaymentEligibility` (onLoad, Partner, B2B & Payment Eligibility)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listPartnerPaymentEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner b2b payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner b2b payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner b2b payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner b2b payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Emirates Bank Visa Infinite holders
```

#### Permissions

- `listPartnerPaymentEligibility` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-204` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-204`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 12: Works in Partner, B2B & Payment Eligibility → Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-204?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-205` Audience Preview, Reach & Eligibility Simulator

**Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Audience Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/audience-preview-reach-eligibility-simulator-adm-205` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who will qualify before a targeting rule goes live: reach and sample.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listAudiencePreviewReach return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listAudiencePreviewReach carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listAudiencePreviewReach; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Estimated audience** (metric tile)

**Percentage of customer base** (metric tile)

**Historical conversion** (metric tile)

**Historical AOV** (metric tile)

**Expected redemptions** (metric tile)

**Estimated promotion cost** (metric tile)

**Estimated revenue** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **reach**: Count, sample of profiles (masked), overlap with other promotions. *(source: contracts/satellite/promotions.yaml#listAudiencePreviewReach)*

**Data it reads**: `listAudiencePreviewReach` (onLoad, Audience Preview, Reach & Eligibility Simulator)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listAudiencePreviewReach`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience preview reach list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience preview reach untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience preview reach yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience preview reach are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reach:
  qualifying: 6120
  overlapWith: RESIDENT-15 (1,240)
```

#### Permissions

- `listAudiencePreviewReach` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-205` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-205`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 14: Works in Audience Preview, Reach & Eligibility Simulator → Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-205?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-206` Targeting Conflict, Frequency & Exclusion Controls

**Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.**

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
| Route | `/commercial/targeting-conflict-frequency-exclusion-controls-adm-206` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Existing member, Specific CRM segment, Partner restriction, Product ownership. Each needs an operation, or … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listTargetingConflictFrequency lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Frequency caps and exclusions so guests are not over-targeted.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Existing member, Specific CRM segment, Partner restriction, Product ownership.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-206; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listTargetingConflictFrequency return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listTargetingConflictFrequency carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listTargetingConflictFrequency; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Targeting Conflict, Frequency & Exclusion Controls) declares only reads (listTargetingConflictFrequency). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum offers per day | text field | — | — | — | — | — | — |
| Maximum offers per week | text field | — | — | — | — | — | — |
| Maximum campaigns per month | text field | — | — | — | — | — | — |
| Maximum redemptions | select field | — | — | — | — | — | — |
| Cooling-off period | select field | — | — | — | — | — | — |
| Repeat campaign restriction | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Existing member (primary button) | navigation or local | — | — | — | — |
| Specific CRM segment (secondary button) | navigation or local | — | — | — | — |
| Partner restriction (secondary button) | navigation or local | — | — | — | — |
| Product ownership (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **controls**: Caps per guest per period and exclusion lists. *(source: contracts/satellite/promotions.yaml#listTargetingConflictFrequency)*

**Data it reads**: `listTargetingConflictFrequency` (onLoad, Targeting Conflict, Frequency & Exclusion Controls)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listTargetingConflictFrequency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targeting conflict frequency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targeting conflict frequency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targeting conflict frequency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cap: At most 2 offers a week per guest
```

#### Permissions

- `listTargetingConflictFrequency` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-206` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-206`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 16: Works in Targeting Conflict, Frequency & Exclusion Controls → Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-206?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Existing member, Specific CRM segment, Partner restriction, Product ownership.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-207` AI Audience Discovery & Targeting Optimization

**Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined. Board 8 shall provide TICVAI with the centralized Promotion Decision Engine responsible for determining what happens when multiple promotions, discounts, coupons, bundles, loyalty benefits, membership benefits, payment offers, BOGO mechanics, partner offers, or special prices qualify for the same transaction. This is one of the most important boards in the Promotions module because the previous boards may all produce valid offers simultaneously. For example, a guest could qualify for: Annual Pass Holder — 15% discount SUMMER20 coupon — 20% discount Emirates NBD card — 10% discount Buy 4 Pay 3 — promotional mechanic Loyalty Gold — 5% benefit Can they combine? In what order? Which promotion wins? What is the maximum permitted benefit? The matrix explicitly requires configurable promotion hierarchy, stacking and conflict resolution, including scenarios where promotions are combined, mutually exclusive, or prioritized, with clear explanation of which promotion was applied and why. Board 8 shall contain 10 backend screens.**

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
| Route | `/commercial/ai-audience-discovery-targeting-optimization-adm-207` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI-discovered audiences and opportunities, decided by a person.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listAudienceDiscoveryTargeting return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listAudienceDiscoveryTargeting carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listAudienceDiscoveryTargeting; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Audience size: 126,500. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **suggestions**: Audience, size, rationale, confidence (DI-043). *(source: contracts/satellite/promotions.yaml#listAudienceDiscoveryTargeting / DI-043)*

**Data it reads**: `listAudienceDiscoveryTargeting` (onLoad, AI Audience Discovery & Targeting Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience discovery targeting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience discovery targeting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience discovery targeting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience discovery targeting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-761`: Same AI audience discovery.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
suggestion:
  audience: Weekday seniors
  size: 2100
  confidence: 0.72
```

#### Permissions

- `listAudienceDiscoveryTargeting` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.31 | System shall provide customer-segment-based discount recommendations. | Unified Operations Dashboard | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.11 | AI Audience Discovery | Marketing & CRM | CONTRACTED | `listAudienceDiscoveryTargeting` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-207` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-207`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 18: Works in AI Audience Discovery & Targeting Optimization → Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined. Board 8 shall provide TICVAI with the centralized Promotion …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-207?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
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
"listAudienceDiscoveryTargeting": {"method":"GET","path":"/audience-discovery-targeting","contract":"promotions","summary":"AI Audience Discovery & Targeting Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAudienceDiscoveryTargetingOptimizationView"},
"listAudiencePreviewReach": {"method":"GET","path":"/audience-preview-reach","contract":"promotions","summary":"Audience Preview, Reach & Eligibility Simulator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AudiencePreviewReachEligibilitySimulatorView"},
"listBehavioralTransactionTargeting": {"method":"GET","path":"/behavioral-transaction-targeting","contract":"promotions","summary":"Behavioral & Transaction Targeting","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BehavioralTransactionTargetingView"},
"listContextLocationChannel": {"method":"GET","path":"/context-location-channel","contract":"promotions","summary":"Context, Location, Channel & Time Targeting","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ContextLocationChannelTimeTargetingView"},
"listCrmCustomerSegment": {"method":"GET","path":"/crm-customer-segment","contract":"promotions","summary":"CRM & Customer Segment Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CrmCustomerSegmentManagerView"},
"listMembershipLoyaltyGuest": {"method":"GET","path":"/membership-loyalty-guest","contract":"promotions","summary":"Membership, Loyalty & Guest Eligibility","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MembershipLoyaltyGuestEligibilityView"},
"listPartnerPaymentEligibility": {"method":"GET","path":"/partner-payment-eligibility","contract":"promotions","summary":"Partner, B2B & Payment Eligibility","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PartnerB2bPaymentEligibilityView"},
"listTargetingConflictFrequency": {"method":"GET","path":"/targeting-conflict-frequency","contract":"promotions","summary":"Targeting Conflict, Frequency & Exclusion Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TargetingConflictFrequencyExclusionControlsView"},
"listTargetingEligibility": {"method":"GET","path":"/targeting-eligibility","contract":"promotions","summary":"Targeting & Eligibility Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"guestType","in":"query","required":false},{"name":"crmSegment","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"loyalty","in":"query","required":false},{"name":"demographic","in":"query","required":false},{"name":"behavioral","in":"query","required":false},{"name":"transaction","in":"query","required":false},{"name":"geographic","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"b2b","in":"query","required":false},{"name":"payment","in":"query","required":false},{"name":"contextual","in":"query","required":false},{"name":"aiGenerated","in":"query","required":false}],"requestBody":null,"responds":"TargetingEligibilityCommandCenterView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAudienceDiscoveryTargetingOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"narrowAudience":{"type":"string","description":"Narrow audience"},"expandAudience":{"type":"string","description":"Expand audience"},"excludeLowValueSegment":{"type":"string","description":"Exclude low-value segment"},"changeEligibility":{"type":"string","description":"Change eligibility"},"changeChannel":{"type":"string","description":"Change channel"},"changeTiming":{"type":"string","description":"Change timing"},"changePromotion":{"type":"string","description":"Change promotion"},"reduceFrequency":{"type":"string","description":"Reduce frequency"},"membershipTierEligibility":{"type":"string","description":"Membership/tier eligibility"},"membershipAndLoyaltyEligibility":{"type":"string","description":"Membership and loyalty eligibility"},"audienceName":{"type":"string","description":"Discovered audience"},"audienceSize":{"type":"integer","description":"Audience size"},"suggestedOffer":{"type":"string","description":"Suggested offer"},"predictedConversion":{"type":"number","description":"Predicted conversion, percent"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated incremental revenue"},"rationale":{"type":"string","description":"Why this audience (explainable factors)"}}},
"AudiencePreviewReachEligibilitySimulatorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Audience Preview, Reach & Eligibility Simulator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"estimatedAudience":{"type":"string","description":"Estimated audience"},"percentageOfCustomerBase":{"type":"number","description":"Percentage of customer base"},"historicalConversion":{"type":"number","description":"Historical conversion"},"historicalAov":{"type":"string","description":"Historical AOV"},"expectedRedemptions":{"type":"integer","description":"Expected redemptions"},"estimatedPromotionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated promotion cost"},"estimatedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated revenue"},"sampleProfileResult":{"type":"array","items":{"type":"string"},"description":"Sample profiles tested and whether each is eligible"}}},
"BehavioralTransactionTargetingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Behavioral & Transaction Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"previousProductPurchased":{"type":"string","description":"Previous product purchased"},"previousAttractionVisited":{"type":"string","description":"Previous attraction visited"},"visitFrequency":{"type":"string","description":"Visit frequency"},"daysSinceLastVisit":{"type":"string","description":"Days since last visit"},"previousPromotionRedemption":{"type":"string","description":"Previous promotion redemption"},"abandonedCart":{"type":"string","description":"Abandoned cart"},"bookingFrequency":{"type":"string","description":"Booking frequency"},"purchaseFrequency":{"type":"string","description":"Purchase frequency"},"averageTransactionValue":{"type":"number","description":"Average transaction value"},"totalCustomerValue":{"type":"integer","description":"Total customer value"},"productAffinity":{"type":"string","description":"Product affinity"},"lifetimeSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Lifetime spend"},"averageBasket":{"type":"number","description":"Average basket"},"numberOfTransactions":{"type":"integer","description":"Number of transactions"},"lastPurchase":{"type":"string","format":"date-time","description":"Last purchase"},"purchaseChannel":{"type":"string","description":"Purchase channel"},"productMix":{"type":"string","description":"Product mix"},"lifetime":{"type":"string","description":"Lifetime"},"lookbackPeriod":{"type":"string","enum":["last7Days","last30Days","last90Days","lastYear","customPeriod"],"description":"Look-back period for behavioural conditions"}}},
"ContextLocationChannelTimeTargetingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Context, Location, Channel & Time Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"attraction":{"type":"string","description":"Attraction"},"operatingArea":{"type":"string","description":"Operating area"},"marketCountry":{"type":"string","description":"Market/country"},"salesLocation":{"type":"string","description":"Sales location"},"purchaseDate":{"type":"string","format":"date-time","description":"Purchase date"},"visitDate":{"type":"string","format":"date-time","description":"Visit date"},"day":{"type":"string","description":"Day"},"time":{"type":"string","format":"date-time","description":"Time"},"season":{"type":"string","description":"Season"},"event":{"type":"string","description":"Event"},"holiday":{"type":"string","description":"Holiday"},"campaignPeriod":{"type":"string","format":"date-time","description":"Campaign period"},"currentBasket":{"type":"string","description":"Current basket"},"productCurrentlyViewed":{"type":"string","description":"Product currently viewed"},"currentBooking":{"type":"string","description":"Current booking"},"visitState":{"type":"string","description":"Visit state"},"inVenueState":{"type":"string","description":"In-venue state where available"},"channels":{"type":"array","items":{"type":"string","enum":["b2cWebsite","mobileApp","pos","mobilePos","kiosk","b2b","callCenter","api","ota","reseller","partner"]},"description":"Channels that qualify."}}},
"CrmCustomerSegmentManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What CRM & Customer Segment Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"segmentName":{"type":"string","description":"Segment name"},"estimatedAudience":{"type":"string","description":"Estimated audience"},"lastRefreshed":{"type":"string","format":"date-time","description":"Last refreshed"},"promotionsUsingSegment":{"type":"string","description":"Promotions using segment"},"conversion":{"type":"number","description":"Conversion"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"status":{"type":"integer","description":"Status"},"source":{"type":"string","enum":["ticvaiCrm","importedSegment","externalCrm","externalCdp","membership","loyalty","b2bAccounts","marketingAutomation"],"description":"Where the segment comes from."}}},
"MembershipLoyaltyGuestEligibilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Membership, Loyalty & Guest Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"membershipType":{"type":"string","description":"Membership type"},"membershipTier":{"type":"string","description":"Membership tier"},"membershipStatus":{"type":"string","description":"Membership status"},"membershipStartDate":{"type":"string","format":"date-time","description":"Membership start date"},"renewalStatus":{"type":"string","description":"Renewal status"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry date"},"membershipTenure":{"type":"string","description":"Membership tenure"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"pointsBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Points balance"},"pointsEarned":{"type":"string","description":"Points earned"},"pointsRedeemed":{"type":"string","description":"Points redeemed"},"loyaltyActivity":{"type":"string","description":"Loyalty activity"},"tierProgression":{"type":"string","description":"Tier progression"},"guestCategories":{"type":"array","items":{"type":"string","enum":["adult","child","senior","family","student","resident","tourist","group","vip"]},"description":"Guest categories that qualify."},"tierBenefits":{"type":"array","items":{"type":"string"},"description":"Benefit per loyalty tier, for example Bronze 5%, Silver 10%, Gold 15%"}}},
"PartnerB2bPaymentEligibilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Partner, B2B & Payment Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner"},"partnerCategory":{"type":"string","description":"Partner category"},"corporateAccount":{"type":"string","description":"Corporate account"},"employer":{"type":"string","description":"Employer"},"hotel":{"type":"string","description":"Hotel"},"travelAgency":{"type":"string","description":"Travel agency"},"tourOperator":{"type":"string","description":"Tour operator"},"school":{"type":"string","description":"School"},"governmentEntity":{"type":"string","description":"Government entity"},"bank":{"type":"string","description":"Bank"},"b2bAccount":{"type":"string","description":"B2B account"},"masterAccount":{"type":"string","description":"Master account"},"subAccount":{"type":"string","description":"Sub-account"},"contract":{"type":"string","description":"Contract"},"customerGroup":{"type":"string","description":"Customer group"},"market":{"type":"string","description":"Market"},"salesChannel":{"type":"string","description":"Sales channel"},"paymentMethod":{"type":"string","description":"Payment method"},"eligibleCardProgram":{"type":"string","description":"Eligible card program"},"wallet":{"type":"string","description":"Wallet"},"loyaltyPayment":{"type":"string","description":"Loyalty payment"},"giftCard":{"type":"string","description":"Gift card"},"approvedPaymentPartner":{"type":"integer","description":"Approved payment partner"}}},
"TargetingConflictFrequencyExclusionControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Targeting Conflict, Frequency & Exclusion Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumOffersPerDay":{"type":"string","description":"Maximum offers per day"},"maximumOffersPerWeek":{"type":"string","description":"Maximum offers per week"},"maximumCampaignsPerMonth":{"type":"string","description":"Maximum campaigns per month"},"maximumRedemptions":{"type":"string","description":"Maximum redemptions"},"coolingOffPeriod":{"type":"string","format":"date-time","description":"Cooling-off period"},"repeatCampaignRestriction":{"type":"string","description":"Repeat campaign restriction"},"alreadyPurchasedProduct":{"type":"string","description":"Already purchased product"},"alreadyRedeemedPromotion":{"type":"string","description":"Already redeemed promotion"},"existingMember":{"type":"string","description":"Existing member"},"employee":{"type":"string","description":"Employee"},"specificCrmSegment":{"type":"string","description":"Specific CRM segment"},"fraudRiskStatus":{"type":"string","description":"Fraud/risk status"},"accountType":{"type":"string","description":"Account type"},"partnerRestriction":{"type":"string","description":"Partner restriction"},"productOwnership":{"type":"string","description":"Product ownership"},"campaignExclusions":{"type":"string","description":"Campaign exclusions"},"partnerExclusions":{"type":"string","description":"Partner exclusions"},"operationalExclusions":{"type":"string","description":"Operational exclusions"}}},
"TargetingEligibilityCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Targeting & Eligibility Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeTargetingRules":{"type":"integer","description":"Active Targeting Rules"},"activeSegments":{"type":"integer","description":"Active Segments"},"promotionsUsingTargeting":{"type":"string","description":"Promotions Using Targeting"},"bundlesUsingTargeting":{"type":"string","description":"Bundles Using Targeting"},"eligibleCustomers":{"type":"integer","description":"Eligible Customers"},"targetedCustomers":{"type":"integer","description":"Targeted Customers"},"personalizedOffers":{"type":"integer","description":"Personalized Offers"},"eligibilityPassRate":{"type":"number","description":"Eligibility Pass Rate"},"conversionRate":{"type":"number","description":"Conversion Rate"},"targetedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Targeted Revenue"},"aovUplift":{"type":"number","description":"AOV Uplift"},"aiRecommendedSegments":{"type":"integer","description":"AI-Recommended Segments"},"ruleHealth":{"type":"string","enum":["healthy","warning","conflict","noAudience","oversizedAudience","expired","missingData"],"description":"Health of the targeting rule."}}}
}
```
