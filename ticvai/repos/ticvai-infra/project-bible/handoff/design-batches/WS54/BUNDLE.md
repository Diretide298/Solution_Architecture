# WS54 — Promotions   Bundles Management board 10

**10 screens · 13 operations · 15 schemas · 1 permissions**

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
| `ADM-228` | Promotion Performance Command Center | C | 2 | 0 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-229` | Campaign & Promotion Performance Explorer | C | 4 | 5 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-230` | Redemption, Conversion & Funnel Analytics | C | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-231` | Discount, Margin & Profitability Analytics | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-232` | Bundle, BOGO & Advanced Offer Analytics | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-233` | Upsell, Cross-Sell & Attach-Rate Analytics | C | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-234` | Customer, Segment, Channel & Partner Analytics | C | 0 | 16 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-235` | Incrementality, Attribution & Cannibalization Analysis | C | 0 | 6 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `ADM-236` | AI Optimization & Next-Best-Action Center | C | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-237` | Executive Promotion Intelligence & Reporting Studio | C | 0 | 2 | 6 | 0 | 0 | 2 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-235, ADM-236 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-228` Promotion Performance Command Center

**Provide executives, Marketing, Commercial, Revenue, and Finance with the overall performance of promotions and bundles.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-228 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards; Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-performance-command-center-adm-228` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Overall performance of promotions and bundles for executives.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listPromotionPerformance, listPromotionHealthPerformance, listCampaignPromotionPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPromotionPerformance, listPromotionHealthPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listPromotionPerformance / contracts/satellite/promotions.yaml#listPromotionHealthPerformance / contracts/satellite/promotions.yaml#listCampaignPromotionPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search promotion performance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by date range, business entity, venue, attraction, campaign, promotion and 7 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date range | text field | — | — | `listPromotionPerformance` ?dateRange |
| Business entity | text field | — | — | `listPromotionPerformance` ?businessEntity |
| Venue | text field | — | — | `listPromotionPerformance` ?venue |
| Attraction | text field | — | — | `listPromotionPerformance` ?attraction |
| Campaign | text field | — | — | `listPromotionPerformance` ?campaign |
| Promotion | text field | — | — | `listPromotionPerformance` ?promotion |
| Bundle | text field | — | — | `listPromotionPerformance` ?bundle |
| Channel | text field | — | — | `listPromotionPerformance` ?channel |
| Customer segment | text field | — | — | `listPromotionPerformance` ?customerSegment |
| Product | text field | — | — | `listPromotionPerformance` ?product |
| Partner | text field | — | — | `listPromotionPerformance` ?partner |
| Market | text field | — | — | `listPromotionPerformance` ?market |
| Currency | text field | — | — | `listPromotionPerformance` ?currency |

#### Outputs: what the screen shows and produces

**Shown**

**Gross Sales** (metric tile)

**Promotion-Influenced Revenue** (metric tile)

**Estimated Incremental Revenue** (metric tile)

**Discount Granted** (metric tile)

**Net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Gross Margin** (metric tile)

**Promotion Cost** (metric tile)

**ROI** (metric tile)

**Transactions** (metric tile)

**Redemptions** (metric tile)

**Conversion Rate** (metric tile)

**Average Order Value** (metric tile)

**Revenue per Redemption** (metric tile)

**Active Campaigns** (metric tile)

**Net revenue vs discount cost vs incremental net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPIs**: Promotion-influenced revenue, incremental revenue, discount granted, ROI with deltas. *(source: contracts/satellite/promotions.yaml#listPromotionPerformance / DI-041)*

**Data it reads**: `listPromotionPerformance` (onLoad, Promotion Performance Command Center); `listPromotionHealthPerformance` (onLoad, Promotion Health & Performance Monitor); `listCampaignPromotionPerformance` (onLoad, Campaign & Promotion Performance Explorer)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-229` Campaign & Promotion Performance Explorer: *Works in Campaign & Promotion Performance Explorer*; calls `listPromotionPerformance`
- → `ADM-230` Redemption, Conversion & Funnel Analytics: *Works in Redemption, Conversion & Funnel Analytics*; calls `listPromotionPerformance`
- → `ADM-231` Discount, Margin & Profitability Analytics: *Works in Discount, Margin & Profitability Analytics*; calls `listPromotionPerformance`
- → `ADM-232` Bundle, BOGO & Advanced Offer Analytics: *Works in Bundle, BOGO & Advanced Offer Analytics*; calls `listPromotionPerformance`
- → `ADM-233` Upsell, Cross-Sell & Attach-Rate Analytics: *Works in Upsell, Cross-Sell & Attach-Rate Analytics*; calls `listPromotionPerformance`
- → `ADM-234` Customer, Segment, Channel & Partner Analytics: *Works in Customer, Segment, Channel & Partner Analytics*; calls `listPromotionPerformance`
- → `ADM-235` Incrementality, Attribution & Cannibalization Analysis: *Works in Incrementality, Attribution & Cannibalization Analysis*; calls `listPromotionPerformance`
- → `ADM-236` AI Optimization & Next-Best-Action Center: *Works in AI Optimization & Next-Best-Action Center*; calls `listPromotionPerformance`
- → `ADM-237` Executive Promotion Intelligence & Reporting Studio: *Works in Executive Promotion Intelligence & Reporting Studio*; calls `listPromotionPerformance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  influencedRevenue: AED 1.4m
  roi: 3.2x
```

#### Permissions

- `listPromotionPerformance` → `PRICE_VIEW` (read) · staff
- `listPromotionHealthPerformance` → `PRICE_VIEW` (read) · staff
- `listCampaignPromotionPerformance` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-228` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-228`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 1: Opens Promotion Performance Command Center → Provide executives, Marketing, Commercial, Revenue, and Finance with the overall performance of promotions and bundles.
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F163 branch at step 1 (expected): when Nothing has been set up on Promotion Performance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F163 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-228?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-229`, `ADM-230`, `ADM-231`, `ADM-232`, `ADM-233`, `ADM-234`, `ADM-235`, `ADM-236`, `ADM-237`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-229` Campaign & Promotion Performance Explorer

**Allow users to compare every promotion and campaign using consistent commercial KPIs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-229 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/campaign-promotion-performance-explorer-adm-229` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Compare every promotion and campaign with the same KPIs.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCampaignPromotionPerformance, listPromotionPerformance, listPromotionCampaign return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPromotionPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCampaignPromotionPerformance / contracts/satellite/promotions.yaml#listPromotionPerformance / contracts/satellite/promotions.yaml#listPromotionCampaign; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date range | text field | — | — | `listPromotionPerformance` ?dateRange |
| Business entity | text field | — | — | `listPromotionPerformance` ?businessEntity |
| Venue | text field | — | — | `listPromotionPerformance` ?venue |
| Attraction | text field | — | — | `listPromotionPerformance` ?attraction |
| Campaign | text field | — | — | `listPromotionPerformance` ?campaign |
| Promotion | text field | — | — | `listPromotionPerformance` ?promotion |
| Bundle | text field | — | — | `listPromotionPerformance` ?bundle |
| Channel | text field | — | — | `listPromotionPerformance` ?channel |
| Customer segment | text field | — | — | `listPromotionPerformance` ?customerSegment |
| Product | text field | — | — | `listPromotionPerformance` ?product |
| Partner | text field | — | — | `listPromotionPerformance` ?partner |
| Market | text field | — | — | `listPromotionPerformance` ?market |
| Currency | text field | — | — | `listPromotionPerformance` ?currency |
| Promotion type | text field | — | — | `listPromotionCampaign` ?promotionType |
| Campaign | text field | — | — | `listPromotionCampaign` ?campaign |
| Product | text field | — | — | `listPromotionCampaign` ?product |
| … 16 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **comparison table**: Sortable by ROI, margin, conversion. *(source: contracts/satellite/promotions.yaml#listCampaignPromotionPerformance)*

**Data it reads**: `listCampaignPromotionPerformance` (onLoad, Campaign & Promotion Performance Explorer); `listPromotionPerformance` (onLoad, Promotion Performance Command Center); `listPromotionCampaign` (onLoad, Promotion & Campaign Directory); `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listCampaignPromotionPerformance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign promotion performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign promotion performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign promotion performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign promotion performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  promotion: SUMMER-BOGO
  roi: 2.1x
  margin: -3 pts
```

#### Permissions

- `listCampaignPromotionPerformance` → `PRICE_VIEW` (read) · staff
- `listPromotionPerformance` → `PRICE_VIEW` (read) · staff
- `listPromotionCampaign` → `PRICE_VIEW` (read) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-229` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-229`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 2: Works in Campaign & Promotion Performance Explorer → Allow users to compare every promotion and campaign using consistent commercial KPIs.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-229?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-230` Redemption, Conversion & Funnel Analytics

**Measure how effectively offers move customers from exposure to purchase and redemption.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-230 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/redemption-conversion-funnel-analytics-adm-230` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How offers move guests from exposure to purchase and redemption.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRedemptionConversionFunnel return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listRedemptionConversionFunnel carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRedemptionConversionFunnel; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search redemption conversion funnel | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by channel, customer segment, membership tier, product, venue, campaign and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listRedemptionConversionFunnel` ?channel |
| Customer segment | text field | — | — | `listRedemptionConversionFunnel` ?customerSegment |
| Membership tier | text field | — | — | `listRedemptionConversionFunnel` ?membershipTier |
| Product | text field | — | — | `listRedemptionConversionFunnel` ?product |
| Venue | text field | — | — | `listRedemptionConversionFunnel` ?venue |
| Campaign | text field | — | — | `listRedemptionConversionFunnel` ?campaign |
| Promotion type | text field | — | — | `listRedemptionConversionFunnel` ?promotionType |
| Day time | text field | — | — | `listRedemptionConversionFunnel` ?dayTime |

#### Outputs: what the screen shows and produces

**Shown**

**Exposure rate** (metric tile)

**Engagement rate** (metric tile)

**Cart rate** (metric tile)

**Conversion rate** (metric tile)

**Redemption rate** (metric tile)

**Abandonment** (metric tile)

**Unused promotion rate** (metric tile)

**Expired benefit rate** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **funnel**: Exposure, click, basket, purchase, redemption. *(source: contracts/satellite/promotions.yaml#listRedemptionConversionFunnel)*

**Data it reads**: `listRedemptionConversionFunnel` (onLoad, Redemption, Conversion & Funnel Analytics)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listRedemptionConversionFunnel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption conversion funnel list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption conversion funnel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption conversion funnel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption conversion funnel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
funnel:
- 12000
- 3100
- 1400
- 980
- 940
```

#### Permissions

- `listRedemptionConversionFunnel` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-230` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-230`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 4: Works in Redemption, Conversion & Funnel Analytics → Measure how effectively offers move customers from exposure to purchase and redemption.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-230?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-231` Discount, Margin & Profitability Analytics

**Determine whether promotions are commercially profitable rather than merely generating sales.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-231 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Core Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/discount-margin-profitability-analytics-adm-231` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether promotions are profitable, not just selling.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listDiscountMarginProfitability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDiscountMarginProfitability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listDiscountMarginProfitability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Gross sales** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Discount Value** (metric tile)

**Net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Product Cost** (metric tile)

**Promotion Cost** (metric tile)

**Gross Profit** (metric tile)

**Gross Margin %** (metric tile)

**Margin Change** (metric tile)

**Revenue Uplift** (metric tile)

**Profit Uplift** (metric tile)

**ROI** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **margin view**: Discount vs margin per promotion. *(source: contracts/satellite/promotions.yaml#listDiscountMarginProfitability)*

**Data it reads**: `listDiscountMarginProfitability` (onLoad, Discount, Margin & Profitability Analytics)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listDiscountMarginProfitability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount margin profitability list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount margin profitability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount margin profitability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the discount margin profitability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  promotion: RESIDENT-15
  margin: +1.4 pts
```

#### Permissions

- `listDiscountMarginProfitability` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-231` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-231`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 6: Works in Discount, Margin & Profitability Analytics → Determine whether promotions are commercially profitable rather than merely generating sales.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-231?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-232` Bundle, BOGO & Advanced Offer Analytics

**Measure performance specifically for the commercial mechanics created in Boards 4–6.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-232 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Bundle KPIs; BOGO Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-bogo-advanced-offer-analytics-adm-232` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Performance of bundles, BOGO and advanced offers.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listBundleBogoAdvanced return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBundleBogoAdvanced carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBundleBogoAdvanced; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Bundle Sales** (metric tile)

**Bundle Revenue** (metric tile)

**Bundle Conversion** (metric tile)

**Bundle AOV** (metric tile)

**Component Attach Rate** (metric tile)

**Component Redemption** (metric tile)

**Bundle Margin** (metric tile)

**Bundle vs Standalone Revenue** (metric tile)

**Substitution Rate** (metric tile)

**Availability Failure Rate** (metric tile)

**BOGO transactions** (metric tile)

**Free items issued** (metric tile)

**Average reward value** (metric tile)

**Incremental units** (metric tile)

**Incremental revenue** (metric tile)

**Margin impact** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **mechanics analytics**: By mechanic type. *(source: contracts/satellite/promotions.yaml#listBundleBogoAdvanced)*

**Data it reads**: `listBundleBogoAdvanced` (onLoad, Bundle, BOGO & Advanced Offer Analytics)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listBundleBogoAdvanced`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle bogo advanced list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle bogo advanced untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle bogo advanced yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle bogo advanced are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  mechanic: BOGO
  freeItems: 2140
  revenue: AED 410,000.00
```

#### Permissions

- `listBundleBogoAdvanced` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-232` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-232`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 8: Works in Bundle, BOGO & Advanced Offer Analytics → Measure performance specifically for the commercial mechanics created in Boards 4–6.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-232?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-233` Upsell, Cross-Sell & Attach-Rate Analytics

**Measure whether promotions and bundles successfully increase the customer's basket beyond the original purchase. This screen is particularly important for the cross-sale metrics you originally raised.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-233 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Analyze) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upsell-cross-sell-attach-rate-analytics-adm-233` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether promotions and bundles grow the basket: attach rates.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listUpsellCrossSell return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listUpsellCrossSell carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listUpsellCrossSell; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Cross-Sell Revenue** (metric tile)

**Upsell Revenue** (metric tile)

**Attach Rate** (metric tile)

**Items per Transaction** (metric tile)

**Revenue per Transaction** (metric tile)

**Upgrade Conversion** (metric tile)

**Recommended Offer Acceptance** (metric tile)

**Incremental Basket Value** (metric tile)

**Cross-Category Conversion** (metric tile)

**Every upsell cross-sell attach-rate** (data table, from `listUpsellCrossSell`)

| Shows | Format | Notes |
|---|---|---|
| Ticket ticket | text | Ticket → Ticket |
| Ticket FB | text | Ticket → F&B |
| Ticket retail | text | Ticket → Retail |
| Ticket experience | text | Ticket → Experience |
| Ticket membership | text | Ticket → Membership |
| F b retail | text | F&B → Retail |
| Retail FB | text | Retail → F&B |
| Membership experience | text | Membership → Experience |

**The selected upsell cross-sell attach-rate** (detail panel): The pack groups this record's detail under its own headings: “Important Scope Boundary”.

| Shows | Format | Notes |
|---|---|---|
| Ticket ticket | text | Ticket → Ticket |
| Ticket FB | text | Ticket → F&B |
| Ticket retail | text | Ticket → Retail |
| Ticket experience | text | Ticket → Experience |
| Ticket membership | text | Ticket → Membership |
| F b retail | text | F&B → Retail |
| Retail FB | text | Retail → F&B |
| Membership experience | text | Membership → Experience |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **attach rates**: Base product, attached product, attach rate. *(source: contracts/satellite/promotions.yaml#listUpsellCrossSell)*

**Data it reads**: `listUpsellCrossSell` (onLoad, Upsell, Cross-Sell & Attach-Rate Analytics)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listUpsellCrossSell`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upsell cross-sell attach-rate list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upsell cross-sell attach-rate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upsell cross-sell attach-rate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upsell cross-sell attach-rate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  base: Day Pass
  attached: Fast Track
  rate: 18%
```

#### Permissions

- `listUpsellCrossSell` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-233` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-233`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 10: Works in Upsell, Cross-Sell & Attach-Rate Analytics → Measure whether promotions and bundles successfully increase the customer's basket beyond the original purchase. This screen is particularly important for the cross-sale metrics you originally raised.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-233?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-234` Customer, Segment, Channel & Partner Analytics

**Determine which audiences and distribution channels respond best to promotions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-234 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Customer/Segment KPIs) and a per-row directory (§Compare; Measure) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-segment-channel-partner-analytics-adm-234` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): listChannelCustomerSegment is the dynamic pricing rules view (catalogue), not promotion analytics (design-notes correction ticketing-backoffice ADM-234)

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which audiences and channels respond best to promotions.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCustomerSegmentChannel return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCustomerSegmentChannel carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCustomerSegmentChannel; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): The screen also reads the dynamic pricing rules view (listChannelCustomerSegment) as analytics. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Customers reached** (metric tile)

**New customers** (metric tile)

**Returning customers** (metric tile)

**Conversion** (metric tile)

**Net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Discount** (metric tile)

**AOV** (metric tile)

**Margin** (metric tile)

**Repeat purchase** (metric tile)

**Redemption** (metric tile)

**Every customer segment channel** (data table, from `listCustomerSegmentChannel`)

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: B2C, Mobile app, POS, Kiosk, B2B, Call center… | Channel compared. |
| Partner revenue | AED 1,234.50 | Partner revenue |
| Partner redemptions | 1,234 | Partner redemptions |
| Discount cost | AED 1,234.50 | Discount cost |
| Commission | AED 1,234.50 | Commission |
| Net contribution | text | Net contribution |
| Conversion | 1,234.5 | Conversion |
| Campaign roi | text | Campaign ROI |

**The selected customer segment channel** (detail panel): The pack groups this record's detail under its own headings: “AOV ROI”.

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: B2C, Mobile app, POS, Kiosk, B2B, Call center… | Channel compared. |
| Partner revenue | AED 1,234.50 | Partner revenue |
| Partner redemptions | 1,234 | Partner redemptions |
| Discount cost | AED 1,234.50 | Discount cost |
| Commission | AED 1,234.50 | Commission |
| Net contribution | text | Net contribution |
| Conversion | 1,234.5 | Conversion |
| Campaign roi | text | Campaign ROI |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **response by audience**: Segment and channel response rates. *(source: contracts/satellite/promotions.yaml#listCustomerSegmentChannel)*

**Data it reads**: `listCustomerSegmentChannel` (onLoad, Customer, Segment, Channel & Partner Analytics)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listCustomerSegmentChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer segment channel list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer segment channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer segment channel yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer segment channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  segment: Families
  channel: App
  response: 12%
```

#### Permissions

- `listCustomerSegmentChannel` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-234` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-234`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 12: Works in Customer, Segment, Channel & Partner Analytics → Determine which audiences and distribution channels respond best to promotions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-234?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-235` Incrementality, Attribution & Cannibalization Analysis

**Incrementality, Attribution & Cannibalization Analysis**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-235 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/incrementality-attribution-cannibalization-analysis-adm-235` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Incrementality, attribution and cannibalisation: how much of the discount went to guests who would have bought anyway.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listIncrementalityAttributionCannibalization return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listIncrementalityAttributionCannibalization carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listIncrementalityAttributionCannibalization; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every incrementality attribution cannibalization** (data table, from `listIncrementalityAttributionCannibalization`)

| Shows | Format | Notes |
|---|---|---|
| Full price customers moving to discounted products | text | not in the schema: `Full-price customers moving to discounted products` |
| Cannibalization type | chip: Standard ticket discounted ticket, Higher margin bundle lower margin promotion … | Cannibalisation detected. |
| Existing member purchase replaced by unnecessary discount | text | not in the schema: `Existing member purchase replaced by unnecessary discount` |

**The selected incrementality attribution cannibalization** (detail panel): The pack groups this record's detail under its own headings: “Answer the difficult question”, “Where sufficient data exists, support”, “Promotion-influenced revenue”, “Estimated baseline revenue”, “Estimated incremental revenue”, “AED 650K”.

| Shows | Format | Notes |
|---|---|---|
| Full price customers moving to discounted products | text | not in the schema: `Full-price customers moving to discounted products` |
| Cannibalization type | chip: Standard ticket discounted ticket, Higher margin bundle lower margin promotion … | Cannibalisation detected. |
| Existing member purchase replaced by unnecessary discount | text | not in the schema: `Existing member purchase replaced by unnecessary discount` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **incrementality**: Incremental vs cannibalised revenue. *(source: contracts/satellite/promotions.yaml#listIncrementalityAttributionCannibalization / contracts/satellite/promotions.yaml#simulatePromotion)*

**Data it reads**: `listIncrementalityAttributionCannibalization` (onLoad, Incrementality, Attribution & Cannibalization Analysis)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listIncrementalityAttributionCannibalization`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incrementality attribution cannibalization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incrementality attribution cannibalization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No incrementality attribution cannibalization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the incrementality attribution cannibalization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  incremental: AED 84,000.00
  cannibalised: AED 22,000.00
```

#### Permissions

- `listIncrementalityAttributionCannibalization` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.24 | AI Revenue Attribution Insights | Marketing & CRM | CONTRACTED | `listIncrementalityAttributionCannibalization` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-235` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-235`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 14: Works in Incrementality, Attribution & Cannibalization Analysis → Incrementality, Attribution & Cannibalization Analysis

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-235?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-236` AI Optimization & Next-Best-Action Center

**Turn analytics into actionable commercial recommendations. This should be one of the strongest AI screens in the Promotions module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-236 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-optimization-next-best-action-center-adm-236` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Analytics turned into recommended next actions, decided by a person.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listNextBestAction return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listNextBestAction carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listNextBestAction; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Review, Accept as Draft, Simulate, Send for Approval, Dismiss, Snooze. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **next best actions**: Cards with impact and confidence (DI-043). *(source: contracts/satellite/promotions.yaml#listNextBestAction / DI-043)*

**Data it reads**: `listNextBestAction` (onLoad, AI Optimization & Next-Best-Action Center)

**Where the user goes next**

- → `ADM-228` Promotion Performance Command Center: *Returns to the board's landing screen*; calls `listNextBestAction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimization next-best-action list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimization next-best-action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimization next-best-action yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimization next-best-action are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action: 'End RESIDENT-15 on weekends: +AED 9,000.00 margin'
```

#### Permissions

- `listNextBestAction` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.40 | System shall recommend optimal promotion structures, discount percentages, validity periods, target audiences, and campaign timing based on historical performance and business objectives. | Admission and Access | CONTRACTED | `listNextBestAction` |
| 4.1.18 | Generate promotion recommendations automatically. | Bundles and Promotions | CONTRACTED | `listNextBestAction` |
| 8.6.35 | System shall provide campaign-specific discount recommendations. | Unified Operations Dashboard | CONTRACTED | `listNextBestAction` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-236` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-236`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 16: Works in AI Optimization & Next-Best-Action Center → Turn analytics into actionable commercial recommendations. This should be one of the strongest AI screens in the Promotions module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-236?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-228`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-237` Executive Promotion Intelligence & Reporting Studio

**Provide executive reporting and configurable analytics output across the complete Promotions & Bundles module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-237 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Promotion Attribution & KPI Engine; Metric Governance) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/executive-promotion-intelligence-reporting-studio-adm-237` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Filter, Commercial, Revenue Management, Finance, Venue Management, Data Analyst. Each needs an operation, or … **Executive Promotion Intelligence & Reporting Studio declares no operation that writes anything** — its only declared call is `listExecutivePromotionReporting`, a read. The name promises authoring …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Executive reporting across promotions and bundles: configurable outputs and exports.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Filter, Commercial, Revenue Management, Finance, Venue Management, Data Analyst.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-237; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listExecutivePromotionReporting return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listExecutivePromotionReporting carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listExecutivePromotionReporting; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Metric | text field | — | — | `listExecutivePromotionReporting` ?metric |
| Dimension | text field | — | — | `listExecutivePromotionReporting` ?dimension |
| Date | text field | — | — | `listExecutivePromotionReporting` ?date |
| Comparison period | text field | — | — | `listExecutivePromotionReporting` ?comparisonPeriod |
| Grouping | text field | — | — | `listExecutivePromotionReporting` ?grouping |
| Format | radio group | — | Json · Excel · Csv · Pdf | `listExecutivePromotionReporting` ?format |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every executive promotion intelligence** (data table, from `listExecutivePromotionReporting`)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected executive promotion intelligence** (detail panel): The pack groups this record's detail under its own headings: “Promotion ROI”, “Cross-Sell Revenue”, “Upsell Revenue”, “Top Campaigns”, “Underperformers”, “Reporting Data Architecture”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Excel, CSV, PDF, Power BI, API, Scheduled report. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Filter (primary button) | navigation or local | — | — | — | — |
| Commercial (secondary button) | navigation or local | — | — | — | — |
| Revenue Management (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Venue Management (secondary button) | navigation or local | — | — | — | — |
| Data Analyst (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **report studio**: Saved report tiles with period selector (DI-041); export PDF or Excel. *(source: contracts/satellite/promotions.yaml#listExecutivePromotionReporting / DI-041)*

**Data it reads**: `listExecutivePromotionReporting` (onLoad, Executive Promotion Intelligence & Reporting Studio)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The executive promotion intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the executive promotion intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No executive promotion intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the executive promotion intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
report:
  name: Monthly promotions pack
  period: October 2026
```

#### Permissions

- `listExecutivePromotionReporting` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-237` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS115 Promotions   Bundles Management Board 10.dc.html#adm-237`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 10
- Flow F163 *Promotions Bundles Management board 10: Promotion Performance Command Center*, step 18: Works in Executive Promotion Intelligence & Reporting Studio → Provide executive reporting and configurable analytics output across the complete Promotions & Bundles module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-237?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Filter, Commercial, Revenue Management, Finance, Venue Management, Data Analyst.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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
"listBundleBogoAdvanced": {"method":"GET","path":"/bundle-bogo-advanced","contract":"promotions","summary":"Bundle, BOGO & Advanced Offer Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BundleBogoAdvancedOfferAnalyticsView"},
"listCampaignPromotionPerformance": {"method":"GET","path":"/campaign-promotion-performance","contract":"promotions","summary":"Campaign & Promotion Performance Explorer","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CampaignPromotionPerformanceExplorerView"},
"listCommercialCampaigns": {"method":"GET","path":"/commercial-campaigns","contract":"promotions","summary":"List commercial campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":"ownerPrincipalId","in":"query","required":null},{"name":"q","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerSegmentChannel": {"method":"GET","path":"/customer-segment-channel","contract":"promotions","summary":"Customer, Segment, Channel & Partner Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomerSegmentChannelPartnerAnalyticsView"},
"listDiscountMarginProfitability": {"method":"GET","path":"/discount-margin-profitability","contract":"promotions","summary":"Discount, Margin & Profitability Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DiscountMarginProfitabilityAnalyticsView"},
"listExecutivePromotionReporting": {"method":"GET","path":"/executive-promotion-reporting","contract":"promotions","summary":"Executive Promotion Intelligence & Reporting Studio","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"metric","in":"query","required":false},{"name":"dimension","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"comparisonPeriod","in":"query","required":false},{"name":"grouping","in":"query","required":false},{"name":"format","in":"query","required":false}],"requestBody":null,"responds":"ExecutivePromotionIntelligenceReportingStudioView"},
"listIncrementalityAttributionCannibalization": {"method":"GET","path":"/incrementality-attribution-cannibalization","contract":"promotions","summary":"Incrementality, Attribution & Cannibalization Analysis","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IncrementalityAttributionCannibalizationAnalysisView"},
"listNextBestAction": {"method":"GET","path":"/next-best-action","contract":"promotions","summary":"AI Optimization & Next-Best-Action Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiOptimizationNextBestActionCenterView"},
"listPromotionCampaign": {"method":"GET","path":"/promotion-campaign","contract":"promotions","summary":"Promotion & Campaign Directory","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"promotionType","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"productCategory","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"fnb","in":"query","required":false},{"name":"retail","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"approvalState","in":"query","required":false},{"name":"promotionValue","in":"query","required":false},{"name":"budgetStatus","in":"query","required":false}],"requestBody":null,"responds":"PromotionCampaignDirectoryView"},
"listPromotionHealthPerformance": {"method":"GET","path":"/promotion-health-performance","contract":"promotions","summary":"Promotion Health & Performance Monitor","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PromotionHealthPerformanceMonitorView"},
"listPromotionPerformance": {"method":"GET","path":"/promotion-performance","contract":"promotions","summary":"Promotion Performance Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"dateRange","in":"query","required":false},{"name":"businessEntity","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"promotion","in":"query","required":false},{"name":"bundle","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"currency","in":"query","required":false}],"requestBody":null,"responds":"PromotionPerformanceCommandCenterView"},
"listRedemptionConversionFunnel": {"method":"GET","path":"/redemption-conversion-funnel","contract":"promotions","summary":"Redemption, Conversion & Funnel Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"membershipTier","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"promotionType","in":"query","required":false},{"name":"dayTime","in":"query","required":false}],"requestBody":null,"responds":"RedemptionConversionFunnelAnalyticsView"},
"listUpsellCrossSell": {"method":"GET","path":"/upsell-cross-sell","contract":"promotions","summary":"Upsell, Cross-Sell & Attach-Rate Analytics","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UpsellCrossSellAttachRateAnalyticsView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiOptimizationNextBestActionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What AI Optimization & Next-Best-Action Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"recommendation":{"type":"string","enum":["increaseDiscount","reduceDiscount","changeMechanic","endPromotion","changeThreshold","expandSegment","narrowSegment","excludeSegment","changeBundlePrice","expandChannel","restrictChannel","reallocateCampaignBudget","changeDay","changeTime","reduceCampaignDuration"],"description":"Recommended action."},"revenueImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected revenue impact"},"grossProfitImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected gross profit impact"},"rationale":{"type":"string","description":"Why"}}},
"BundleBogoAdvancedOfferAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle, BOGO & Advanced Offer Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bundleSales":{"type":"integer","description":"Bundle Sales"},"bundleRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Bundle Revenue"},"bundleConversion":{"type":"number","description":"Bundle Conversion"},"bundleAov":{"type":"string","description":"Bundle AOV"},"componentAttachRate":{"type":"number","description":"Component Attach Rate"},"componentRedemption":{"type":"string","description":"Component Redemption"},"bundleMargin":{"type":"number","description":"Bundle Margin"},"bundleVsStandaloneRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Bundle vs Standalone Revenue"},"substitutionRate":{"type":"number","description":"Substitution Rate"},"availabilityFailureRate":{"type":"number","description":"Availability Failure Rate"},"bogoTransactions":{"type":"integer","description":"BOGO transactions"},"freeItemsIssued":{"type":"string","description":"Free items issued"},"averageRewardValue":{"type":"number","description":"Average reward value"},"incrementalUnits":{"type":"integer","description":"Incremental units"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"marginImpact":{"type":"number","description":"Margin impact"},"componentAttachRates":{"type":"array","items":{"type":"string"},"description":"Attach rate per bundle component"}}},
"CampaignBudget": {"x-ticvai-persistence":"promotions.campaign_budget","type":"object","description":"One budget line of a commercial campaign (setCampaignBudgetFinancial): what kind of spend it caps, who funds it, what it covers, and what happens as it is consumed. **Consumed, committed and reserved are not stored**: consumed is the discount given on orders (`orders.discount`, `promotions.promotion.discount_given`), committed and reserved are priced carts not yet paid, all worked out on read so they cannot drift from the orders they summarise. (DM5, 29 September: data model for the agreed operations)","required":["budgetType","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"budgetType":{"type":"string","enum":["total","discount","reward","freeProduct"],"description":"The spend this line caps (total campaign, discount, reward or free-product budget)."},"fundingSource":{"type":"string","nullable":true,"enum":["venue","department","marketing","partner"],"description":"Who pays for it; `partner` is a co-funded (e.g. bank or partner-funded) line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scope":{"type":"string","enum":["entireCampaign","promotion","product","channel","partner","customerSegment"],"default":"entireCampaign","description":"What the line covers."},"scopeRef":{"type":"string","nullable":true,"description":"The promotion, product, partner or segment id, or the SalesChannel value, that `scope` names. Null for `entireCampaign`."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The budget owner."},"costCentre":{"type":"string","maxLength":64,"nullable":true},"department":{"type":"string","maxLength":100,"nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"thresholdPolicy":{"$ref":"#/components/schemas/BudgetThresholdPolicy"}}},
"CampaignPromotionPerformanceExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign & Promotion Performance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"transactions":{"type":"string","description":"Transactions"},"units":{"type":"string","description":"Units"},"redemptions":{"type":"string","description":"Redemptions"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"margin":{"type":"number","description":"Margin"},"conversion":{"type":"number","description":"Conversion"},"aov":{"type":"string","description":"AOV"},"roi":{"type":"string","description":"ROI"},"customerAcquisition":{"type":"string","description":"Customer acquisition"},"repeatPurchase":{"type":"string","description":"Repeat purchase"},"marginRisk":{"type":"number","description":"Margin Risk"},"classification":{"type":"string","enum":["excellent","healthy","monitor","underperforming","critical"],"description":"AI/system classification."},"campaignId":{"type":"string","description":"Campaign ID"},"campaignName":{"type":"string","description":"Campaign"}}},
"CommercialCampaign": {"x-ticvai-persistence":"promotions.campaign + promotions.campaign_budget","type":"object","description":"A commercial campaign: the grouping of promotions, coupon campaigns and bundles that share an owner, a business entity, dates and a budget. **Not `marketing.campaign`**, which is the CRM send campaign in another service. The header is saved with its budget lines by setCampaignBudgetFinancial (the budget screen is where the pack captures campaign, owner, business entity and effective dates), and on its own by createCommercialCampaign and updateCommercialCampaign; listCommercialCampaigns lists it (decided 29 September, writers pass); promotions, coupon campaigns and bundles point at it by `campaignId`. No status of its own: a campaign is live while its promotions are, and a threshold action that stops it pauses them. (DM5, 29 September: data model for the agreed operations)","required":["id","venueId","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"budgets":{"type":"array","description":"The rows of `promotions.campaign_budget`, one per budget line.","items":{"$ref":"#/components/schemas/CampaignBudget"}}}},
"CustomerSegmentChannelPartnerAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Customer, Segment, Channel & Partner Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customersReached":{"type":"string","description":"Customers reached"},"newCustomers":{"type":"integer","description":"New customers"},"returningCustomers":{"type":"integer","description":"Returning customers"},"conversion":{"type":"number","description":"Conversion"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"aov":{"type":"string","description":"AOV"},"margin":{"type":"number","description":"Margin"},"repeatPurchase":{"type":"string","description":"Repeat purchase"},"redemption":{"type":"string","description":"Redemption"},"partnerRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner revenue"},"partnerRedemptions":{"type":"integer","description":"Partner redemptions"},"discountCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount cost"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"netContribution":{"type":"string","description":"Net contribution"},"campaignRoi":{"type":"string","description":"Campaign ROI"},"channel":{"type":"string","enum":["b2c","mobileApp","pos","kiosk","b2b","callCenter","ota","reseller","api"],"description":"Channel compared."},"segment":{"type":"string","description":"Customer segment"}}},
"DiscountMarginProfitabilityAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Discount, Margin & Profitability Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Revenue"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Value"},"netRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Revenue"},"productCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Product Cost"},"promotionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion Cost"},"grossProfit":{"type":"string","description":"Gross Profit"},"grossMargin":{"type":"number","description":"Gross Margin %"},"marginChange":{"type":"number","description":"Margin Change"},"revenueUplift":{"type":"number","description":"Revenue Uplift"},"profitUplift":{"type":"number","description":"Profit Uplift"},"roi":{"type":"string","description":"ROI"},"quadrant":{"type":"string","enum":["highRevenueHighMargin","highRevenueLowMargin","lowRevenueHighMargin","lowRevenueLowMargin"],"description":"Revenue and margin quadrant."}}},
"ExecutivePromotionIntelligenceReportingStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Executive Promotion Intelligence & Reporting Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"profit":{"type":"string","description":"Profit"},"roi":{"type":"string","description":"ROI"},"conversion":{"type":"number","description":"Conversion"},"aov":{"type":"string","description":"AOV"},"campaign":{"type":"string","description":"Campaign"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"attentionReason":{"type":"string","enum":["negativeMarginImpact","lowConversion","highDiscountCost","lowIncrementality"],"description":"Why the campaign needs attention, if it does"}}},
"IncrementalityAttributionCannibalizationAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Incrementality, Attribution & Cannibalization Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"attributionMethod":{"type":"string","enum":["directAttribution","promotionCodeAttribution","campaignAttribution","controlGroupComparison","aBTestAttribution","prePostComparison","matchedAudienceAnalysis","aiEstimatedIncrementality"],"description":"Attribution method used."},"cannibalizationType":{"type":"string","enum":["standardTicketDiscountedTicket","higherMarginBundleLowerMarginPromotion","channelMigrationCausedByDiscounting"],"description":"Cannibalisation detected."},"totalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total promotion-influenced revenue"},"baselineRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Baseline revenue"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PromotionCampaignDirectoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion & Campaign Directory displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promotionId":{"type":"string","description":"Promotion ID"},"promotionName":{"type":"string","description":"Promotion Name"},"promotionType":{"type":"string","description":"Promotion Type"},"campaign":{"type":"string","description":"Campaign"},"status":{"type":"string","description":"Status"},"businessEntity":{"type":"string","description":"Business Entity"},"venue":{"type":"string","description":"Venue"},"product":{"type":"string","description":"Product"},"targetSegment":{"type":"string","description":"Target Segment"},"channel":{"type":"string","description":"Channel"},"startDate":{"type":"string","format":"date-time","description":"Start Date"},"endDate":{"type":"string","format":"date-time","description":"End Date"},"discountType":{"type":"string","description":"Discount Type"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Value"},"budget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Budget"},"redemptionCount":{"type":"integer","description":"Redemption Count"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Generated"},"owner":{"type":"string","description":"Owner"},"approvalStatus":{"type":"string","description":"Approval Status"},"version":{"type":"string","description":"Version"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"statusesType":{"type":"string","enum":["draft","configurationIncomplete","simulationRequired","pendingApproval","approved","scheduled","active","paused","suspended","budgetExhausted","expired","cancelled","archived"],"description":"Vocabulary listed under Supported Statuses."}}},
"PromotionHealthPerformanceMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Health & Performance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"impressions":{"type":"integer","description":"Impressions"},"promotionViews":{"type":"integer","description":"Promotion views"},"eligibleTransactions":{"type":"integer","description":"Eligible transactions"},"promotionApplications":{"type":"integer","description":"Promotion applications"},"redemptions":{"type":"integer","description":"Redemptions"},"redemptionRate":{"type":"number","description":"Redemption rate"},"conversionRate":{"type":"number","description":"Conversion rate"},"grossSales":{"type":"integer","description":"Gross sales"},"netSales":{"type":"integer","description":"Net sales"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount granted"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"aovUplift":{"type":"number","description":"AOV uplift"},"margin":{"type":"number","description":"Margin"},"costPerRedemption":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost per redemption"},"budgetConsumed":{"type":"string","description":"Budget consumed"},"budgetRemaining":{"type":"string","description":"Budget remaining"},"promotionVsBaseline":{"type":"string","description":"Promotion vs baseline"},"promotionVsPreviousCampaign":{"type":"string","description":"Promotion vs previous campaign"},"promotionVsAiForecast":{"type":"string","description":"Promotion vs AI forecast"},"promotionVsControlGroup":{"type":"string","description":"Promotion vs control group"},"channelVsChannel":{"type":"string","description":"Channel vs channel"},"venueVsVenue":{"type":"string","description":"Venue vs venue"}}},
"PromotionPerformanceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Performance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossSales":{"type":"integer","description":"Gross Sales"},"promotionInfluencedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion-Influenced Revenue"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Incremental Revenue"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Granted"},"netRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Revenue"},"grossMargin":{"type":"number","description":"Gross Margin"},"promotionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion Cost"},"roi":{"type":"string","description":"ROI"},"transactions":{"type":"integer","description":"Transactions"},"redemptions":{"type":"integer","description":"Redemptions"},"conversionRate":{"type":"number","description":"Conversion Rate"},"averageOrderValue":{"type":"number","description":"Average Order Value"},"revenuePerRedemption":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Redemption"},"activeCampaigns":{"type":"integer","description":"Active Campaigns"}}},
"RedemptionConversionFunnelAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Redemption, Conversion & Funnel Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"exposureRate":{"type":"number","description":"Exposure rate"},"engagementRate":{"type":"number","description":"Engagement rate"},"cartRate":{"type":"number","description":"Cart rate"},"conversionRate":{"type":"number","description":"Conversion rate"},"redemptionRate":{"type":"number","description":"Redemption rate"},"abandonment":{"type":"string","description":"Abandonment"},"unusedPromotionRate":{"type":"number","description":"Unused promotion rate"},"expiredBenefitRate":{"type":"integer","description":"Expired benefit rate"}}},
"UpsellCrossSellAttachRateAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Upsell, Cross-Sell & Attach-Rate Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"crossSellRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cross-Sell Revenue"},"upsellRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Upsell Revenue"},"attachRate":{"type":"number","description":"Attach Rate"},"itemsPerTransaction":{"type":"string","description":"Items per Transaction"},"revenuePerTransaction":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Transaction"},"recommendedOfferAcceptance":{"type":"string","description":"Recommended Offer Acceptance"},"incrementalBasketValue":{"type":"string","description":"Incremental Basket Value"},"crossCategoryConversion":{"type":"number","description":"Cross-Category Conversion"},"ticketTicket":{"type":"string","description":"Ticket → Ticket"},"ticketFB":{"type":"string","description":"Ticket → F&B"},"ticketRetail":{"type":"string","description":"Ticket → Retail"},"ticketExperience":{"type":"string","description":"Ticket → Experience"},"ticketMembership":{"type":"string","description":"Ticket → Membership"},"fBRetail":{"type":"string","description":"F&B → Retail"},"retailFB":{"type":"string","description":"Retail → F&B"},"membershipExperience":{"type":"string","description":"Membership → Experience"}}}
}
```
