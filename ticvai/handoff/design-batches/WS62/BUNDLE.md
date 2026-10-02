# WS62 — Ticket Resale Marketplace board 1

**10 screens · 17 operations · 19 schemas · 3 permissions**

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
  `ORDER_CREATE, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-278` | Resale Marketplace Command Center | B–D | 2 | 48 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-279` | Resale Eligibility Rule Configuration | B–D | 13 | 0 | 5 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-280` | Resale Policy & Marketplace Settings | B–D | 54 | 16 | 5 | 0 | 0 | 5 | — | notStarted (generated) |
| `ADM-281` | Listing Creation & Seller Configuration | B–D | 17 | 20 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-282` | Resale Pricing & Price Guardrails | B–D | 48 | 16 | 5 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-283` | Resale Fees, Commission & Seller Proceeds | B–D | 8 | 0 | 5 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-284` | Listing Approval & Moderation | B–D | 0 | 40 | 6 | 0 | 1 | 3 | — | notStarted (generated) |
| `ADM-285` | Resale Inventory & Availability Management | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-286` | Listing Lifecycle, Expiry & Cancellation | B–D | 8 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-287` | AI Resale Configuration & Marketplace Recommendations | B–D | 8 | 20 | 5 | 1 | 0 | 5 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-285 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-278` Resale Marketplace Command Center

**Provide administrators with a centralized operational view of the TICVAI resale marketplace.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each listing should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-marketplace-command-center-adm-278` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The hub of the resale marketplace: listings, sales, payouts, policy at a glance, for a tenant (PR-1). Resale keeps the original virtual ticket id and changes only the owner and the media.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listResaleMarketplace, listTicketResaleMarketplace, listResalePolicyMarketplace, listOfficialResaleMarketplace return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listTicketResaleMarketplace, listResalePolicyMarketplace …** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listResaleMarketplace / contracts/spine/orders.yaml#listTicketResaleMarketplace / contracts/spine/orders.yaml#listResalePolicyMarketplace / …; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search resale marketplace | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, seller, date, listing status and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Event | text field | — | — | `listResaleMarketplace` ?event |
| Product | text field | — | — | `listResaleMarketplace` ?product |
| Date | text field | — | — | `listResaleMarketplace` ?date |
| Listing status | text field | — | — | `listResaleMarketplace` ?listingStatus |
| Price range | text field | — | — | `listResaleMarketplace` ?priceRange |
| Resale channel | text field | — | — | `listResaleMarketplace` ?resaleChannel |
| Risk level | text field | — | — | `listResaleMarketplace` ?riskLevel |
| Approval status | text field | — | — | `listResaleMarketplace` ?approvalStatus |
| Venue | text field | — | — | `listResaleMarketplace` ?venue |
| Seller | text field | — | — | `listResaleMarketplace` ?seller |

#### Outputs: what the screen shows and produces

**Shown**

**The resale marketplace config** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |

**Active Listings** (metric tile)

**Pending Approval** (metric tile)

**Tickets Available for Resale** (metric tile)

**Listings Sold Today** (metric tile)

**Expiring Listings** (metric tile)

**Suspended Listings** (metric tile)

**Rejected Listings** (metric tile)

**Average Resale Price** (metric tile)

**Gross Resale Value** (metric tile)

**Marketplace Fees** (metric tile)

**Seller Proceeds** (metric tile)

**Conversion Rate** (metric tile)

**Every resale marketplace** (data table, from `listResaleMarketplace`)

| Shows | Format | Notes |
|---|---|---|
| Listing | text | Listing ID |
| Original order ticket | text | Original Order/Ticket ID |
| Event product | text | Event/Product |
| Venue | text | Venue |
| Event date | 1 Oct 2026, 14:30 | Event Date |
| Section row seat | text | Section/Row/Seat |
| Seller | text | Seller |
| Original price | AED 1,234.50 | Original Price |
| Listed price | AED 1,234.50 | Listed Price |
| Price variance | 1,234.5 | Price Variance % |
| Marketplace fee | AED 1,234.50 | Marketplace Fee |
| Seller proceeds | 1,234 | Seller Proceeds |
| Listing date | 1 Oct 2026, 14:30 | Listing Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Status | 1,234 | Status |
| Risk indicator | text | Risk Indicator |

**The selected resale marketplace** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Listing | text | Listing ID |
| Original order ticket | text | Original Order/Ticket ID |
| Event product | text | Event/Product |
| Venue | text | Venue |
| Event date | 1 Oct 2026, 14:30 | Event Date |
| Section row seat | text | Section/Row/Seat |
| Seller | text | Seller |
| Original price | AED 1,234.50 | Original Price |
| Listed price | AED 1,234.50 | Listed Price |
| Price variance | 1,234.5 | Price Variance % |
| Marketplace fee | AED 1,234.50 | Marketplace Fee |
| Seller proceeds | 1,234 | Seller Proceeds |
| Listing date | 1 Oct 2026, 14:30 | Listing Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Status | 1,234 | Status |
| Risk indicator | text | Risk Indicator |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **marketplace KPIs**: Active listings, sold today, average resale vs face value, pending payouts. *(source: contracts/spine/orders.yaml#listResaleMarketplace / TRACKER Actions row 215)*

**Data it reads**: `listResaleMarketplace` (onLoad, Resale Marketplace Command Center); `listTicketResaleMarketplace` (onLoad, My Tickets & Resale Marketplace Entry); `listResalePolicyMarketplace` (onLoad, Resale Policy & Marketplace Settings); `listOfficialResaleMarketplace` (onLoad, Official Resale Marketplace & Buyer Discovery); `getResaleMarketplaceConfig` (onLoad, How the venue's resale marketplace runs)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-279` Resale Eligibility Rule Configuration: *Works in Resale Eligibility Rule Configuration*; calls `listResaleMarketplace`
- → `ADM-280` Resale Policy & Marketplace Settings: *Works in Resale Policy & Marketplace Settings*; calls `listResaleMarketplace`
- → `ADM-281` Listing Creation & Seller Configuration: *Works in Listing Creation & Seller Configuration*; calls `listResaleMarketplace`
- → `ADM-282` Resale Pricing & Price Guardrails: *Works in Resale Pricing & Price Guardrails*; calls `listResaleMarketplace`
- → `ADM-283` Resale Fees, Commission & Seller Proceeds: *Works in Resale Fees, Commission & Seller Proceeds*; calls `listResaleMarketplace`
- → `ADM-284` Listing Approval & Moderation: *Works in Listing Approval & Moderation*; calls `listResaleMarketplace`
- → `ADM-285` Resale Inventory & Availability Management: *Works in Resale Inventory & Availability Management*; calls `listResaleMarketplace`
- → `ADM-286` Listing Lifecycle, Expiry & Cancellation: *Works in Listing Lifecycle, Expiry & Cancellation*; calls `listResaleMarketplace`
- → `ADM-287` AI Resale Configuration & Marketplace Recommendations: *Works in AI Resale Configuration & Marketplace Recommendations*; calls `listResaleMarketplace`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale marketplace list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale marketplace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale marketplace yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale marketplace are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  listings: 214
  soldToday: 38
  avgVsFace: 104%
  pendingPayouts: AED 12,400.00
```

#### Permissions

- `listResaleMarketplace` → `ORDER_VIEW` (read) · staff
- `listTicketResaleMarketplace` → `ORDER_VIEW` (read) · staff
- `listResalePolicyMarketplace` → `ORDER_VIEW` (read) · staff
- `listOfficialResaleMarketplace` → `ORDER_VIEW` (read) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-278` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-278`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 1: Opens Resale Marketplace Command Center → Provide administrators with a centralized operational view of the TICVAI resale marketplace.
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F171 branch at step 1 (expected): when Nothing has been set up on Resale Marketplace Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F171 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-278?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-279`, `ADM-280`, `ADM-281`, `ADM-282`, `ADM-283`, `ADM-284`, `ADM-285`, `ADM-286`, `ADM-287`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-279` Resale Eligibility Rule Configuration

**Define whether a ticket is allowed to enter the resale marketplace. Not every TICVAI ticket should automatically be resellable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators can define eligibility by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-eligibility-rule-configuration-adm-279` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Identity verification requirement, Membership restriction. Each needs an operation, or needs removing from … Removed 2 October 2026 (CHG-WIR-025): The Resale Eligibility Rule Configuration also wrote setEligibilityRule, the promotion eligibility rule; promotion eligibility is a different concept and is … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of resale eligibility rules (setResaleEligibilityRule has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which tickets may enter resale: product, ticket type, event, status, payment, ownership, windows, limits, and the conditions a ticket must meet (fully paid, not scanned, not expired, event not started, not refunded, complimentary, staff or disputed).

**Known correction pending (do not draw the wrong version)**

- **priceCategory is typed Money and ownership period a date-time.** Why: A category is an id; a period is a duration. *(source: contracts/spine/orders.yaml#setResaleEligibilityRule; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: Identity verification requirement, Membership restriction.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-279; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): The screen also writes the promotion eligibility rule (setEligibilityRule). (CHG-WIR-025); No read operation: the screen declares only setResaleEligibilityRule, setEligibilityRule and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product | select field | — | — | — | — | — | — |
| Ticket type | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Membership type | select field | — | — | — | — | — | — |
| Sales channel | select field | — | — | — | — | — | — |
| Customer segment | select field | — | — | — | — | — | — |
| Price category | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Ticket status | select field | — | — | — | — | — | — |
| Payment status | select field | — | — | — | — | — | — |
| Ticket ownership status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **requiredConditions**: Checkboxes, all ticked by default. *(source: contracts/spine/orders.yaml#setResaleEligibilityRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Identity verification requirement (primary button) | navigation or local | — | — | — | — |
| Membership restriction (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `setResaleEligibilityRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale eligibility rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale eligibility rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale eligibility rule configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  product: Desert Symphony
  conditions:
  - fullyPaid
  - notScanned
  - eventNotStarted
  maxListingsPerCustomer: 4
```

#### Permissions

- `setResaleEligibilityRule` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-279` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-279`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 2: Works in Resale Eligibility Rule Configuration → Define whether a ticket is allowed to enter the resale marketplace. Not every TICVAI ticket should automatically be resellable.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-279?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Identity verification requirement, Membership restriction.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-280` Resale Policy & Marketplace Settings

**Configure the overall business policies governing a resale marketplace.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators can define; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-policy-marketplace-settings-adm-280` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How the marketplace runs: pricing mode and guardrails, moderation, listing limits, deployment.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listResalePolicyMarketplace return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listResalePolicyMarketplace carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listResalePolicyMarketplace; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Marketplace name | select field | — | — | — | — | — | — |
| Marketplace status | select field | — | — | — | — | — | — |
| Applicable organization | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Time zone | select field | — | — | — | — | — | — |
| Supported language | select field | — | — | — | — | — | — |
| Marketplace sales channel | select field | — | — | — | — | — | — |
| Customer terms | select field | — | — | — | — | — | — |
| Seller terms | select field | — | — | — | — | — | — |
| Seller verification | select field | — | — | — | — | — | — |
| Identity requirements | select field | — | — | — | — | — | — |
| Bank/payout information | select field | — | — | — | — | — | — |
| Seller terms acceptance | select field | — | — | — | — | — | — |
| Listing confirmation | select field | — | — | — | — | — | — |
| Seller notifications | select field | — | — | — | — | — | — |
| Buyer terms | select field | — | — | — | — | — | — |
| Marketplace disclosures | select field | — | — | — | — | — | — |
| Resale ticket labeling | select field | — | — | — | — | — | — |
| Refund conditions | select field | — | — | — | — | — | — |
| Service fees | select field | — | — | — | — | — | — |
| Purchase limits | select field | — | — | — | — | — | — |

**Form: Save resale marketplace config** (modal, opened by *Save resale marketplace config*; *Save resale marketplace config* calls `setResaleMarketplaceConfig`, *Cancel* sends nothing)

**Collects what `setResaleMarketplaceConfig` sends before it is called.** Required: `id`, `marketplaceName`, `pricingMode`, `moderationMode`, `isActive`. Optional: `maximumDiscountPercent`, `sellerCanEditPrice`, `maximumPriceChanges`, `minimumMinutesBetweenPriceChanges`, `reviewTriggers`, `expiryRule`, `expiryOffset`, `withdrawalPolicy`, `maximumWithdrawals`, `cancellationFee`, `checkoutHoldMinutes`, `buyerIdentityVerificationRequired` and 16 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Marketplace name `marketplaceName` | text field | required | — | max length 150 | — | — | `setResaleMarketplaceConfig` body |
| Pricing mode `pricingMode` | select | required | — | Face value only · Fixed price · Seller selected price · Capped price · Operator controlled · AI recommended price | — | — | `setResaleMarketplaceConfig` body |
| Maximum discount percent `maximumDiscountPercent` | stepper or slider | optional | — | min 0; max 100 | — | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. | `setResaleMarketplaceConfig` body |
| Seller can edit price `sellerCanEditPrice` | toggle | optional | on | — | — | — | `setResaleMarketplaceConfig` body |
| Maximum price changes `maximumPriceChanges` | number field | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Minimum minutes between price changes `minimumMinutesBetweenPriceChanges` | number field (minutes) | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Moderation mode `moderationMode` | segmented control | required | Automatic | Automatic · Risk based · Manual | — | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. | `setResaleMarketplaceConfig` body |
| Review triggers `reviewTriggers` | multi-select chips | optional | — | High resale price · Unusual discount · High value ticket · Vip ticket · Seller risk · New seller · Multiple listings · Identity issue · Payment issue · Ticket ownership concern · Fraud indicator | — | — | `setResaleMarketplaceConfig` body |
| Expiry rule `expiryRule` | radio group | optional | At event start | X minutes before event · X hours before event · At event start · At configured date | — | — | `setResaleMarketplaceConfig` body |
| Expiry offset `expiryOffset` | number field | optional | — | min 0 | — | Minutes or hours, per `expiryRule`. | `setResaleMarketplaceConfig` body |
| Withdrawal policy `withdrawalPolicy` | segmented control | optional | Seller cannot withdraw while reserved | Seller can withdraw anytime · Seller cannot withdraw while reserved | — | — | `setResaleMarketplaceConfig` body |
| Maximum withdrawals `maximumWithdrawals` | number field | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Cancellation fee `cancellationFee` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setResaleMarketplaceConfig` body |
| Checkout hold minutes `checkoutHoldMinutes` | number field (minutes) | optional | 10 | min 1 | — | How long a listing stays `reserved` for one buyer in checkout. | `setResaleMarketplaceConfig` body |
| Buyer identity verification required `buyerIdentityVerificationRequired` | toggle | optional | off | — | — | — | `setResaleMarketplaceConfig` body |
| Settlement timing `settlementTiming` | select | optional | After access validation | Immediately after resale · X days after resale · After event completion · X days after event · After access validation · Operator defined settlement cycle | — | Default `afterAccessValidation`: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`). | `setResaleMarketplaceConfig` body |
| Settlement delay days `settlementDelayDays` | number field (days) | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Minimum payout threshold `minimumPayoutThreshold` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setResaleMarketplaceConfig` body |
| Customer terms `customerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Seller terms `sellerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Buyer terms `buyerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Terms version `termsVersion` | text field | optional | — | max length 20 | — | The version a seller accepts at listing. | `setResaleMarketplaceConfig` body |
| Disclosures `disclosures` | text area | optional | — | max length 4000 | — | — | `setResaleMarketplaceConfig` body |
| Resale ticket label `resaleTicketLabel` | text field | optional | — | max length 60 | — | — | `setResaleMarketplaceConfig` body |
| Deployment model `deploymentModel` | segmented control | optional | Ticvai hosted white label | Embedded white label · Ticvai hosted white label · Headless API | — | — | `setResaleMarketplaceConfig` body |
| Navigation `navigation` | multi-select chips | optional | — | My tickets · Sell · Buy · My listings · Transactions | — | — | `setResaleMarketplaceConfig` body |
| Authentication method `authenticationMethod` | radio group | optional | Customer account | Customer account · Sso · Passwordless login · OTP · App authentication | — | — | `setResaleMarketplaceConfig` body |
| Branding `branding` | group | optional | — | — | — | Logo, colours, typography, support contact and legal links for the marketplace pages. | `setResaleMarketplaceConfig` body |
| Domain `domain` | text field | optional | — | max length 253 | — | — | `setResaleMarketplaceConfig` body |
| Languages `languages` | list of values (chips) | optional | — | — | — | — | `setResaleMarketplaceConfig` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setResaleMarketplaceConfig` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **marketplace config**: One configuration per venue; sections for pricing, moderation, limits. *(source: contracts/spine/orders.yaml#setResaleMarketplaceConfig)*

#### Outputs: what the screen shows and produces

**Shown**

**The resale marketplace config** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resale marketplace config (primary button) | `setResaleMarketplaceConfig` PUT `/resale-marketplace-config` | ResaleMarketplaceConfig | ResaleMarketplaceConfig | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listResalePolicyMarketplace` (onLoad, Resale Policy & Marketplace Settings); `getResaleMarketplaceConfig` (onLoad, How the venue's resale marketplace runs)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `listResalePolicyMarketplace`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale policy marketplace configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale policy marketplace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale policy marketplace configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  pricing: face value to 120%
  moderation: automatic
  listingLimit: 4
```

#### Permissions

- `listResalePolicyMarketplace` → `ORDER_VIEW` (read) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff
- `setResaleMarketplaceConfig` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-280` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-280`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 4: Works in Resale Policy & Marketplace Settings → Configure the overall business policies governing a resale marketplace.

#### Acceptance for the design

- [ ] Every input above is drawn (54), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-280?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resale marketplace config.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-281` Listing Creation & Seller Configuration

**Define how eligible ticket holders create resale listings.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether seller may; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/listing-creation-seller-configuration-adm-281` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Single ticket listing, Multiple ticket listing. Each needs an operation, or needs removing from the screen …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How ticket holders create listings: what they choose, what is fixed.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Single ticket listing, Multiple ticket listing.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-281; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createListingSeller and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Choose selling price | select field | — | — | — | — | — | — |
| Accept recommended price | select field | — | — | — | — | — | — |
| Edit active listing | select field | — | — | — | — | — | — |
| Withdraw listing | select field | — | — | — | — | — | — |
| Relist expired listing | select field | — | — | — | — | — | — |
| Change price | select field | — | — | — | — | — | — |
| Select payout method | select field | — | — | — | — | — | — |
| Listing ID | select field | — | — | — | — | — | — |
| Ticket ID | select field | — | — | — | — | — | — |
| Seller | select field | — | — | — | — | — | — |
| Listing price | select field | — | — | — | — | — | — |
| Original price | select field | — | — | — | — | — | — |
| Fee | select field | — | — | — | — | — | — |
| Estimated proceeds | select field | — | — | — | — | — | — |
| Listing date | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Seller terms acceptance | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Marketplace settings** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |
| Settlement timing | chip: Immediately after resale, X days after resale, After event completion, X days after … | Default `afterAccessValidation`: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`). |
| Settlement delay days | 1,234 | — |
| Minimum payout threshold | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Customer terms | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single ticket listing (primary button) | navigation or local | — | — | — | — |
| Multiple ticket listing (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **listing form preview**: The seller's form as the guest sees it. *(source: contracts/spine/orders.yaml#createListingSeller)*

**Data it reads**: `getResaleMarketplaceConfig` (onLoad, How the venue's resale marketplace runs, listing rules …)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `createListingSeller`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The listing creation seller configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the listing creation seller untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No listing creation seller configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listing:
  ticket: Desert Symphony Lower 101 C-14
  price: AED 480.00
```

#### Permissions

- `createListingSeller` → `ORDER_CREATE` (operate) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-281` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-281`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 6: Works in Listing Creation & Seller Configuration → Define how eligible ticket holders create resale listings.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-281?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single ticket listing, Multiple ticket listing.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-282` Resale Pricing & Price Guardrails

**Control the permitted resale price while protecting the operator, seller and buyer.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configured resale policy) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-pricing-price-guardrails-adm-282` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The permitted resale price range protecting operator, seller and buyer; often regulated.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listResalePricingPrice return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listResalePricingPrice carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listResalePricingPrice; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Face-value only | select field | — | — | — | — | — | — |
| Minimum resale price | select field | — | — | — | — | — | — |
| Maximum resale price | select field | — | — | — | — | — | — |
| Maximum markup % | select field | — | — | — | — | — | — |
| Maximum discount % | select field | — | — | — | — | — | — |
| Fixed resale price | select field | — | — | — | — | — | — |
| Dynamic permitted range | select field | — | — | — | — | — | — |
| Event-specific range | select field | — | — | — | — | — | — |
| Product-specific range | select field | — | — | — | — | — | — |
| Seller can edit price | text field | — | — | — | — | — | — |
| Number of price changes | text field | — | — | — | — | — | — |
| Minimum interval between changes | text field | — | — | — | — | — | — |
| Automatic price reduction | select field | — | — | — | — | — | — |
| Freeze price after reservation | text field | — | — | — | — | — | — |
| Price adjustment cutoff | select field | — | — | — | — | — | — |
| Minimum: AED 160 | select field | — | — | — | — | — | — |
| Maximum: AED 240 | select field | — | — | — | — | — | — |

**Form: Save resale marketplace config** (modal, opened by *Save resale marketplace config*; *Save resale marketplace config* calls `setResaleMarketplaceConfig`, *Cancel* sends nothing)

**Collects what `setResaleMarketplaceConfig` sends before it is called.** Required: `id`, `marketplaceName`, `pricingMode`, `moderationMode`, `isActive`. Optional: `maximumDiscountPercent`, `sellerCanEditPrice`, `maximumPriceChanges`, `minimumMinutesBetweenPriceChanges`, `reviewTriggers`, `expiryRule`, `expiryOffset`, `withdrawalPolicy`, `maximumWithdrawals`, `cancellationFee`, `checkoutHoldMinutes`, `buyerIdentityVerificationRequired` and 16 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Marketplace name `marketplaceName` | text field | required | — | max length 150 | — | — | `setResaleMarketplaceConfig` body |
| Pricing mode `pricingMode` | select | required | — | Face value only · Fixed price · Seller selected price · Capped price · Operator controlled · AI recommended price | — | — | `setResaleMarketplaceConfig` body |
| Maximum discount percent `maximumDiscountPercent` | stepper or slider | optional | — | min 0; max 100 | — | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. | `setResaleMarketplaceConfig` body |
| Seller can edit price `sellerCanEditPrice` | toggle | optional | on | — | — | — | `setResaleMarketplaceConfig` body |
| Maximum price changes `maximumPriceChanges` | number field | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Minimum minutes between price changes `minimumMinutesBetweenPriceChanges` | number field (minutes) | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Moderation mode `moderationMode` | segmented control | required | Automatic | Automatic · Risk based · Manual | — | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. | `setResaleMarketplaceConfig` body |
| Review triggers `reviewTriggers` | multi-select chips | optional | — | High resale price · Unusual discount · High value ticket · Vip ticket · Seller risk · New seller · Multiple listings · Identity issue · Payment issue · Ticket ownership concern · Fraud indicator | — | — | `setResaleMarketplaceConfig` body |
| Expiry rule `expiryRule` | radio group | optional | At event start | X minutes before event · X hours before event · At event start · At configured date | — | — | `setResaleMarketplaceConfig` body |
| Expiry offset `expiryOffset` | number field | optional | — | min 0 | — | Minutes or hours, per `expiryRule`. | `setResaleMarketplaceConfig` body |
| Withdrawal policy `withdrawalPolicy` | segmented control | optional | Seller cannot withdraw while reserved | Seller can withdraw anytime · Seller cannot withdraw while reserved | — | — | `setResaleMarketplaceConfig` body |
| Maximum withdrawals `maximumWithdrawals` | number field | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Cancellation fee `cancellationFee` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setResaleMarketplaceConfig` body |
| Checkout hold minutes `checkoutHoldMinutes` | number field (minutes) | optional | 10 | min 1 | — | How long a listing stays `reserved` for one buyer in checkout. | `setResaleMarketplaceConfig` body |
| Buyer identity verification required `buyerIdentityVerificationRequired` | toggle | optional | off | — | — | — | `setResaleMarketplaceConfig` body |
| Settlement timing `settlementTiming` | select | optional | After access validation | Immediately after resale · X days after resale · After event completion · X days after event · After access validation · Operator defined settlement cycle | — | Default `afterAccessValidation`: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`). | `setResaleMarketplaceConfig` body |
| Settlement delay days `settlementDelayDays` | number field (days) | optional | — | min 0 | — | — | `setResaleMarketplaceConfig` body |
| Minimum payout threshold `minimumPayoutThreshold` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setResaleMarketplaceConfig` body |
| Customer terms `customerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Seller terms `sellerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Buyer terms `buyerTerms` | text area | optional | — | max length 20000 | — | — | `setResaleMarketplaceConfig` body |
| Terms version `termsVersion` | text field | optional | — | max length 20 | — | The version a seller accepts at listing. | `setResaleMarketplaceConfig` body |
| Disclosures `disclosures` | text area | optional | — | max length 4000 | — | — | `setResaleMarketplaceConfig` body |
| Resale ticket label `resaleTicketLabel` | text field | optional | — | max length 60 | — | — | `setResaleMarketplaceConfig` body |
| Deployment model `deploymentModel` | segmented control | optional | Ticvai hosted white label | Embedded white label · Ticvai hosted white label · Headless API | — | — | `setResaleMarketplaceConfig` body |
| Navigation `navigation` | multi-select chips | optional | — | My tickets · Sell · Buy · My listings · Transactions | — | — | `setResaleMarketplaceConfig` body |
| Authentication method `authenticationMethod` | radio group | optional | Customer account | Customer account · Sso · Passwordless login · OTP · App authentication | — | — | `setResaleMarketplaceConfig` body |
| Branding `branding` | group | optional | — | — | — | Logo, colours, typography, support contact and legal links for the marketplace pages. | `setResaleMarketplaceConfig` body |
| Domain `domain` | text field | optional | — | max length 253 | — | — | `setResaleMarketplaceConfig` body |
| Languages `languages` | list of values (chips) | optional | — | — | — | — | `setResaleMarketplaceConfig` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setResaleMarketplaceConfig` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **price guardrails**: Minimum and maximum as a percentage of face value, with a worked example. *(source: contracts/spine/orders.yaml#setResaleMarketplaceConfig)*

#### Outputs: what the screen shows and produces

**Shown**

**The resale marketplace config** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resale marketplace config (primary button) | `setResaleMarketplaceConfig` PUT `/resale-marketplace-config` | ResaleMarketplaceConfig | ResaleMarketplaceConfig | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listResalePricingPrice` (onLoad, Resale Pricing & Price Guardrails); `getResaleMarketplaceConfig` (onLoad, How the venue's resale marketplace runs)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `listResalePricingPrice`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale pricing price configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale pricing price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale pricing price configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guardrail:
  min: 80% of face
  max: 120% of face
  face: AED 450.00
  range: AED 360.00 to AED 540.00
```

#### Permissions

- `listResalePricingPrice` → `ORDER_VIEW` (read) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff
- `setResaleMarketplaceConfig` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-282` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-282`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 8: Works in Resale Pricing & Price Guardrails → Control the permitted resale price while protecting the operator, seller and buyer.

#### Acceptance for the design

- [ ] Every input above is drawn (48), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-282?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resale marketplace config.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-283` Resale Fees, Commission & Seller Proceeds

**Configure the commercial model of the resale marketplace.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-fees-commission-seller-proceeds-adm-283` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Seller fee, Buyer fee, Flat transaction fee, Percentage fee, Payment processing fee, Administrative fee …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Resale commission and the price cap: seller fee, buyer fee and proceeds.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Seller fee, Buyer fee, Flat transaction fee, Percentage fee, Payment processing fee, Administrative fee, Venue fee, Tax on fee.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-283; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listResaleFeeCommission, listFeeSellerProceed return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listResaleFeeCommission, listFeeSellerProceed carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listResaleFeeCommission / contracts/spine/orders.yaml#listFeeSellerProceed; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Seller type | select field | — | — | — | — | — | — |
| Buyer type | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **fees and cap**: Seller and buyer fee percentages and the cap; regulated in several jurisdictions, so a note shows where. *(source: contracts/spine/orders.yaml#setResaleFeePolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Seller fee (primary button) | navigation or local | — | — | — | — |
| Buyer fee (secondary button) | navigation or local | — | — | — | — |
| Flat transaction fee (secondary button) | navigation or local | — | — | — | — |
| Percentage fee (secondary button) | navigation or local | — | — | — | — |
| Payment processing fee (secondary button) | navigation or local | — | — | — | — |
| Administrative fee (secondary button) | navigation or local | — | — | — | — |
| Venue fee (secondary button) | navigation or local | — | — | — | — |
| Tax on fee (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listResaleFeeCommission` (onLoad, Resale Fees, Commission & Seller Proceeds); `listFeeSellerProceed` (onLoad, Fees, Seller Proceeds & Listing Confirmation); `getResaleFeePolicy` (onLoad, The resale fee and price-cap policy in force)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `listResaleFeeCommission`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale fees commission configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale fees commission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale fees commission configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fees:
  seller: 10%
  buyer: 5%
  cap: 120%
  proceedsOn: 'AED 480.00 sale: AED 432.00'
```

#### Permissions

- `listResaleFeeCommission` → `ORDER_VIEW` (read) · staff
- `listFeeSellerProceed` → `ORDER_VIEW` (read) · staff
- `getResaleFeePolicy` → `ORDER_VIEW` (read) · staff
- `setResaleFeePolicy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-283` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-283`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 10: Works in Resale Fees, Commission & Seller Proceeds → Configure the commercial model of the resale marketplace.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-283?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Seller fee, Buyer fee, Flat transaction fee, Percentage fee, Payment processing fee, Administrative fee, Venue fee, Tax on fee.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-284` Listing Approval & Moderation

**Determine whether listings are published automatically or require operator review.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/listing-approval-moderation-adm-284` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether listings publish automatically or need review, and the moderation queue.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveListingModeration and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **moderation**: Automatic or review; decision approve or reject with reason. *(source: contracts/spine/orders.yaml#approveListingModeration)*

#### Outputs: what the screen shows and produces

**Shown**

**Every listing approval moderation** (data table, from `approveListingModeration`)

| Shows | Format | Notes |
|---|---|---|
| Listing | text | Listing |
| Seller | text | Seller |
| Ticket | text | Ticket |
| Event | text | Event |
| Original price | AED 1,234.50 | Original price |
| Listing price | AED 1,234.50 | Listing price |
| Price variance | AED 1,234.50 | Price variance |
| Risk score | 1,234.5 | Risk score |
| Trigger reason | text | not in the schema: `Trigger reason` |
| Submitted date | 1 Oct 2026, 14:30 | Submitted date |

**Moderation settings** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |
| Settlement timing | chip: Immediately after resale, X days after resale, After event completion, X days after … | Default `afterAccessValidation`: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`). |
| Settlement delay days | 1,234 | — |
| Minimum payout threshold | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Customer terms | text | — |

**The selected listing approval moderation** (detail panel): The pack groups this record's detail under its own headings: “Automatic Approval”, “Manual Approval”, “Risk-Based Approval”.

| Shows | Format | Notes |
|---|---|---|
| Listing | text | Listing |
| Seller | text | Seller |
| Ticket | text | Ticket |
| Event | text | Event |
| Original price | AED 1,234.50 | Original price |
| Listing price | AED 1,234.50 | Listing price |
| Price variance | AED 1,234.50 | Price variance |
| Risk score | 1,234.5 | Risk score |
| Trigger reason | text | not in the schema: `Trigger reason` |
| Submitted date | 1 Oct 2026, 14:30 | Submitted date |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Reject, Request Information, Suspend, Escalate, Add Internal Note. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getResaleMarketplaceConfig` (onLoad, The moderation settings as saved)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `approveListingModeration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The listing approval moderation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the listing approval moderation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No listing approval moderation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the listing approval moderation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  pending: 6
  oldest: 2 h
```

#### Permissions

- `approveListingModeration` → `ORDER_CREATE` (operate) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-284` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-284`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 12: Works in Listing Approval & Moderation → Determine whether listings are published automatically or require operator review.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 412).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-284?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-285` Resale Inventory & Availability Management

**Maintain an accurate, synchronized view of tickets currently available through resale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-inventory-availability-management-adm-285` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Tickets currently available through resale, kept in step with primary inventory.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listResaleInventoryAvailability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listResaleInventoryAvailability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listResaleInventoryAvailability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **resale inventory**: Per event and section, listed and sold. *(source: contracts/spine/orders.yaml#listResaleInventoryAvailability)*

**Data it reads**: `listResaleInventoryAvailability` (onLoad, Resale Inventory & Availability Management)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `listResaleInventoryAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale inventory availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale inventory availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale inventory availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale inventory availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
inventory:
  event: Desert Symphony 22 Nov
  listed: 48
  sold: 21
```

#### Permissions

- `listResaleInventoryAvailability` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-285` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-285`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 14: Works in Resale Inventory & Availability Management → Maintain an accurate, synchronized view of tickets currently available through resale.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-285?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-286` Listing Lifecycle, Expiry & Cancellation

**Control the full lifecycle of a resale listing from creation until sale, withdrawal or expiry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether the ticket) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/listing-lifecycle-expiry-cancellation-adm-286` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A listing's life from creation to sale, withdrawal or expiry.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listListingLifecycleExpiry return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listListingLifecycleExpiry; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Seller can withdraw anytime | text field | — | — | — | — | — | — |
| Seller cannot withdraw while reserved | text field | — | — | — | — | — | — |
| Cancellation cutoff | select field | — | — | — | — | — | — |
| Cancellation fee | select field | — | — | — | — | — | — |
| Maximum withdrawals | select field | — | — | — | — | — | — |
| Returns to customer as normal ticket | text field | — | — | — | — | — | — |
| Can be relisted | select field | — | — | — | — | — | — |
| Requires operator action | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lifecycle**: Listings by state with expiry. *(source: contracts/spine/orders.yaml#listListingLifecycleExpiry)*

**Data it reads**: `listListingLifecycleExpiry` (onLoad, Listing Lifecycle, Expiry & Cancellation)

**Where the user goes next**

- → `ADM-278` Resale Marketplace Command Center: *Returns to the board's landing screen*; calls `listListingLifecycleExpiry`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The listing lifecycle expiry configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the listing lifecycle expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No listing lifecycle expiry configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listing:
  state: listed
  expires: 2 h before event
```

#### Permissions

- `listListingLifecycleExpiry` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-286` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-286`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 16: Works in Listing Lifecycle, Expiry & Cancellation → Control the full lifecycle of a resale listing from creation until sale, withdrawal or expiry.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-286?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-278`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-287` AI Resale Configuration & Marketplace Recommendations

**Provide TICVAI's AI intelligence layer for optimizing resale configuration while keeping commercial control with the operator. Board 2 manages what happens once a resale listing attracts a buyer and enters the transaction stage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration; AI Resale Configuration & Marketplace) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-resale-configuration-marketplace-recommendations-adm-287` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI suggestions for resale configuration; the operator decides.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setResaleMarketplaceRecommendation and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pricing recommendations | select field | — | — | — | — | — | — |
| Demand prediction | select field | — | — | — | — | — | — |
| Listing recommendations | select field | — | — | — | — | — | — |
| Seller risk recommendations | select field | — | — | — | — | — | — |
| Expiry recommendations | select field | — | — | — | — | — | — |
| Marketplace optimization | select field | — | — | — | — | — | — |
| Anomaly detection | select field | — | — | — | — | — | — |
| 3.1.10 AI optimization | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Current configuration** (detail panel, from `getResaleMarketplaceConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Marketplace name | text | — |
| Pricing mode | chip: Face value only, Fixed price, Seller selected price, Capped price, Operator … | — |
| Maximum discount percent | 1,234.5 | The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it. |
| Seller can edit price | yes / no (icon or chip) | — |
| Maximum price changes | 1,234 | — |
| Minimum minutes between price changes | 1,234 | — |
| Moderation mode | chip: Automatic, Risk based, Manual | `reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing. |
| Review triggers | list or chips (count when long) | — |
| Expiry rule | chip: X minutes before event, X hours before event, At event start, At configured date | — |
| Expiry offset | 1,234 | Minutes or hours, per `expiryRule`. |
| Withdrawal policy | chip: Seller can withdraw anytime, Seller cannot withdraw while reserved | — |
| Maximum withdrawals | 1,234 | — |
| Cancellation fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Checkout hold minutes | 1,234 | How long a listing stays `reserved` for one buyer in checkout. |
| Buyer identity verification required | yes / no (icon or chip) | — |
| Settlement timing | chip: Immediately after resale, X days after resale, After event completion, X days after … | Default `afterAccessValidation`: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`). |
| Settlement delay days | 1,234 | — |
| Minimum payout threshold | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Customer terms | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **recommendations**: Recommendation, impact, accept or dismiss. *(source: contracts/spine/orders.yaml#setResaleMarketplaceRecommendation / DI-043)*

**Data it reads**: `getResaleMarketplaceConfig` (onLoad, The marketplace configuration the recommendations apply to)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale marketplace recommendations configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale marketplace recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale marketplace recommendations configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recommendation: 'Raise the cap to 125% for sold-out Fridays: +AED 3,200.00 fees'
```

#### Permissions

- `setResaleMarketplaceRecommendation` → `ORDER_CREATE` (operate) · staff
- `getResaleMarketplaceConfig` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.6.19 | AI shall recommend resale opportunities, pricing recommendations, demand forecasts, and inventory optimization suggestions based on marketplace activity. | Ticketing Catalogue | CONTRACTED | `setResaleMarketplaceRecommendation` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-287` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS168 Ticket Resale Marketplace Board 1.dc.html#adm-287`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 1
- Flow F171 *Ticket Resale Marketplace board 1: Resale Marketplace Command Center*, step 18: Works in AI Resale Configuration & Marketplace Recommendations → Provide TICVAI's AI intelligence layer for optimizing resale configuration while keeping commercial control with the operator. Board 2 manages what happens once a resale listing attracts a buyer and …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (403, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-287?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveListingModeration": {"method":"PUT","path":"/listing-moderation","contract":"orders","summary":"Listing Approval & Moderation","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ListingApprovalModerationInput","responds":"ListingApprovalModerationView"},
"createListingSeller": {"method":"POST","path":"/listing-seller","contract":"orders","summary":"Listing Creation & Seller Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ListingCreationSellerConfigurationInput","responds":"ListingCreationSellerConfigurationView"},
"getResaleFeePolicy": {"method":"GET","path":"/resale-fee-policy","contract":"orders","summary":"The commission and price cap a resale listing is created under","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResaleFeePolicy"},
"getResaleMarketplaceConfig": {"method":"GET","path":"/resale-marketplace-config","contract":"orders","summary":"How the venue's resale marketplace runs","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResaleMarketplaceConfig"},
"listFeeSellerProceed": {"method":"GET","path":"/fee-seller-proceed","contract":"orders","summary":"Fees, Seller Proceeds & Listing Confirmation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeesSellerProceedsListingConfirmationView"},
"listListingLifecycleExpiry": {"method":"GET","path":"/listing-lifecycle-expiry","contract":"orders","summary":"Listing Lifecycle, Expiry & Cancellation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ListingLifecycleExpiryCancellationView"},
"listOfficialResaleMarketplace": {"method":"GET","path":"/official-resale-marketplace","contract":"orders","summary":"Official Resale Marketplace & Buyer Discovery","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfficialResaleMarketplaceBuyerDiscoveryView"},
"listResaleFeeCommission": {"method":"GET","path":"/resale-fee-commission","contract":"orders","summary":"Resale Fees, Commission & Seller Proceeds","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleFeesCommissionSellerProceedsView"},
"listResaleInventoryAvailability": {"method":"GET","path":"/resale-inventory-availability","contract":"orders","summary":"Resale Inventory & Availability Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleInventoryAvailabilityManagementView"},
"listResaleMarketplace": {"method":"GET","path":"/resale-marketplace","contract":"orders","summary":"Resale Marketplace Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"listingStatus","in":"query","required":false},{"name":"priceRange","in":"query","required":false},{"name":"resaleChannel","in":"query","required":false},{"name":"riskLevel","in":"query","required":false},{"name":"approvalStatus","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"seller","in":"query","required":false}],"requestBody":null,"responds":"ResaleMarketplaceCommandCenterView"},
"listResalePolicyMarketplace": {"method":"GET","path":"/resale-policy-marketplace","contract":"orders","summary":"Resale Policy & Marketplace Settings","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResalePolicyMarketplaceSettingsView"},
"listResalePricingPrice": {"method":"GET","path":"/resale-pricing-price","contract":"orders","summary":"Resale Pricing & Price Guardrails","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResalePricingPriceGuardrailsView"},
"listTicketResaleMarketplace": {"method":"GET","path":"/ticket-resale-marketplace","contract":"orders","summary":"My Tickets & Resale Marketplace Entry","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MyTicketsResaleMarketplaceEntryView"},
"setResaleEligibilityRule": {"method":"PUT","path":"/resale-eligibility-rule","contract":"orders","summary":"Resale Eligibility Rule Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResaleEligibilityRuleConfigurationInput","responds":"ResaleEligibilityRuleConfigurationView"},
"setResaleFeePolicy": {"method":"PUT","path":"/resale-fee-policy","contract":"orders","summary":"Set resale commission and the price ceiling","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResaleFeePolicy","responds":"ResaleFeePolicy"},
"setResaleMarketplaceConfig": {"method":"PUT","path":"/resale-marketplace-config","contract":"orders","summary":"Set how the venue's resale marketplace runs","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResaleMarketplaceConfig","responds":"ResaleMarketplaceConfig"},
"setResaleMarketplaceRecommendation": {"method":"PUT","path":"/resale-marketplace-recommendation","contract":"orders","summary":"AI Resale Configuration & Marketplace Recommendations","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AiResaleConfigurationMarketplaceRecommendationsInput","responds":"AiResaleConfigurationMarketplaceRecommendationsView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiResaleConfigurationMarketplaceRecommendationsInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.resale_recommendation` (DM5, 29 September)","description":"**What AI Resale Configuration & Marketplace Recommendations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"pricingRecommendations":{"type":"string","description":"Pricing recommendations"},"demandPrediction":{"type":"string","description":"Demand prediction"},"listingRecommendations":{"type":"string","description":"Listing recommendations"},"sellerRiskRecommendations":{"type":"string","description":"Seller risk recommendations"},"expiryRecommendations":{"type":"string","format":"date-time","description":"Expiry recommendations"},"marketplaceOptimization":{"type":"string","description":"Marketplace optimization"},"anomalyDetection":{"type":"string","description":"Anomaly detection"},"decision":{"type":"string","enum":["accept","modify","ignore"],"description":"What the administrator does with the recommendation"}}},
"AiResaleConfigurationMarketplaceRecommendationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What AI Resale Configuration & Marketplace Recommendations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"pricingRecommendations":{"type":"string","description":"Pricing recommendations"},"demandPrediction":{"type":"string","description":"Demand prediction"},"listingRecommendations":{"type":"string","description":"Listing recommendations"},"sellerRiskRecommendations":{"type":"string","description":"Seller risk recommendations"},"expiryRecommendations":{"type":"string","format":"date-time","description":"Expiry recommendations"},"marketplaceOptimization":{"type":"string","description":"Marketplace optimization"},"anomalyDetection":{"type":"string","description":"Anomaly detection"},"decision":{"type":"string","enum":["accept","modify","ignore"],"description":"What the administrator does with the recommendation"}}},
"FeesSellerProceedsListingConfirmationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Fees, Seller Proceeds & Listing Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"marketplaceTerms":{"type":"integer","description":"Marketplace Terms"},"sellerTerms":{"type":"integer","description":"Seller Terms"},"cancellationPolicy":{"type":"string","description":"Cancellation Policy"},"settlementConditions":{"type":"integer","description":"Settlement Conditions"},"eventCancellationTreatment":{"type":"string","description":"Event Cancellation Treatment"},"applicablePrivacyNotice":{"type":"string","description":"Applicable privacy notice"},"sellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Selling price"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"estimatedProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated seller proceeds"},"termsVersion":{"type":"string","description":"Terms version the seller accepts; stored with the acceptance"}}},
"ListingApprovalModerationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in the moderation columns of `orders.resale_listing` (DM5, 29 September)","description":"**What Listing Approval & Moderation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"reviewReasons":{"type":"array","items":{"type":"string","enum":["highResalePrice","unusualDiscount","highValueTicket","vipTicket","sellerRisk","newSeller","multipleListings","identityIssue","paymentIssue","ticketOwnershipConcern","fraudIndicator"]},"description":"Why the listing is under review."},"decision":{"type":"string","enum":["approve","reject","requestInformation"],"description":"Moderation decision"},"reason":{"type":"string","description":"Reason"}}},
"ListingApprovalModerationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Listing Approval & Moderation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"listing":{"type":"string","description":"Listing"},"seller":{"type":"string","description":"Seller"},"ticket":{"type":"string","description":"Ticket"},"event":{"type":"string","description":"Event"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original price"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listing price"},"priceVariance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price variance"},"riskScore":{"type":"number","description":"Risk score"},"submittedDate":{"type":"string","format":"date-time","description":"Submitted date"},"reviewReasons":{"type":"array","items":{"type":"string","enum":["highResalePrice","unusualDiscount","highValueTicket","vipTicket","sellerRisk","newSeller","multipleListings","identityIssue","paymentIssue","ticketOwnershipConcern","fraudIndicator"]},"description":"Why the listing is under review."},"decision":{"type":"string","enum":["approve","reject","requestInformation"],"description":"Moderation decision"}}},
"ListingCreationSellerConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Listing Creation & Seller Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"ticketType":{"type":"string","description":"Ticket type"},"section":{"type":"string","description":"Section"},"row":{"type":"string","description":"Row"},"seat":{"type":"string","description":"Seat"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original price"},"ticketStatus":{"type":"string","description":"Ticket status"},"listingId":{"type":"string","description":"Listing ID"},"ticketId":{"type":"string","description":"Ticket ID"},"seller":{"type":"string","description":"Seller"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listing price"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"estimatedProceeds":{"type":"string","description":"Estimated proceeds"},"listingDate":{"type":"string","format":"date-time","description":"Listing date"},"expiration":{"type":"string","description":"Expiration"},"sellerTermsAcceptance":{"type":"string","description":"Seller terms acceptance"},"listingType":{"type":"string","enum":["singleTicketListing","multipleTicketListing","adjacentSeatGroup"],"description":"What is listed."}}},
"ListingCreationSellerConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Listing Creation & Seller Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"ticketType":{"type":"string","description":"Ticket type"},"section":{"type":"string","description":"Section"},"row":{"type":"string","description":"Row"},"seat":{"type":"string","description":"Seat"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original price"},"ticketStatus":{"type":"string","description":"Ticket status"},"listingId":{"type":"string","description":"Listing ID"},"ticketId":{"type":"string","description":"Ticket ID"},"seller":{"type":"string","description":"Seller"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listing price"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"estimatedProceeds":{"type":"string","description":"Estimated proceeds"},"listingDate":{"type":"string","format":"date-time","description":"Listing date"},"expiration":{"type":"string","description":"Expiration"},"sellerTermsAcceptance":{"type":"string","description":"Seller terms acceptance"},"listingType":{"type":"string","enum":["singleTicketListing","multipleTicketListing","adjacentSeatGroup"],"description":"What is listed."}}},
"ListingLifecycleExpiryCancellationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Listing Lifecycle, Expiry & Cancellation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"cancellationCutoff":{"type":"string","description":"Cancellation cutoff"},"cancellationFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cancellation fee"},"maximumWithdrawals":{"type":"string","description":"Maximum withdrawals"},"closure":{"type":"string","enum":["rejected","suspended","withdrawn","cancelled","expired"],"description":"How the listing left the market: moderation outcome, or the resale-listing state it ended in (states/resale-listing.yaml)."},"expiryRule":{"type":"string","enum":["xMinutesBeforeEvent","xHoursBeforeEvent","atEventStart","atConfiguredDate"],"description":"When the listing expires."},"withdrawalPolicy":{"type":"string","enum":["sellerCanWithdrawAnytime","sellerCannotWithdrawWhileReserved"],"description":"When the seller may withdraw."},"autoCancellationReason":{"type":"string","enum":["ticketBecomesInvalid","eventIsCancelled","eventChangesMaterially","ticketIsRefunded","ticketIsTransferred","paymentIsReversed","eligibilityChanges","fraudIsDetected"],"description":"Why the listing was cancelled automatically."},"expiryOffset":{"type":"integer","description":"Minutes or hours for the xMinutes/xHours rules"},"listingId":{"type":"string","description":"Listing ID"}}},
"MyTicketsResaleMarketplaceEntryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What My Tickets & Resale Marketplace Entry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventProduct":{"type":"string","description":"Event/Product"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/Time"},"ticketType":{"type":"string","description":"Ticket Type"},"sectionRowSeat":{"type":"string","description":"Section/Row/Seat"},"ticketHolder":{"type":"string","description":"Ticket Holder"},"virtualTicketIdReference":{"type":"string","description":"Virtual Ticket ID reference"},"ticketStatus":{"type":"string","description":"Ticket Status"},"resaleStatus":{"type":"string","description":"Resale Status"},"availableActions":{"type":"string","description":"Available Actions"},"clientLogo":{"type":"string","description":"Client logo"},"brand":{"type":"string","description":"Brand"},"colors":{"type":"string","description":"Colors"},"typography":{"type":"string","description":"Typography"},"language":{"type":"string","description":"Language"},"supportDetails":{"type":"string","description":"Support details"},"marketplaceName":{"type":"string","description":"Marketplace name"},"authenticationMethod":{"type":"string","enum":["customerAccount","sso","passwordlessLogin","otp","appAuthentication"],"description":"How the guest signs in to the marketplace"}}},
"OfficialResaleMarketplaceBuyerDiscoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Official Resale Marketplace & Buyer Discovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"date":{"type":"string","format":"date-time","description":"Date"},"performance":{"type":"string","description":"Performance"},"ticketType":{"type":"string","description":"Ticket Type"},"section":{"type":"string","description":"Section"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"quantity":{"type":"integer","description":"Quantity"},"accessibility":{"type":"string","description":"Accessibility"},"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"address":{"type":"string","description":"Address"},"paymentInformation":{"type":"string","description":"Payment information"},"inventoryFilter":{"type":"string","enum":["officialTicketsOfficialResale","resaleOnly","primaryOnly"],"description":"Which inventory the buyer sees."}}},
"ResaleEligibilityRuleConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.resale_eligibility_rule` (DM5, 29 September)","description":"**What Resale Eligibility Rule Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"performance":{"type":"string","description":"Performance"},"membershipType":{"type":"string","description":"Membership type"},"salesChannel":{"type":"string","description":"Sales channel"},"customerSegment":{"type":"string","description":"Customer segment"},"priceCategory":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price category"},"promotion":{"type":"string","description":"Promotion"},"ticketStatus":{"type":"string","description":"Ticket status"},"paymentStatus":{"type":"string","description":"Payment status"},"ticketOwnershipStatus":{"type":"string","description":"Ticket ownership status"},"specificResaleStartEndDate":{"type":"string","format":"date-time","description":"Specific resale start/end date"},"blackoutPeriod":{"type":"string","format":"date-time","description":"Blackout period"},"maximumResaleAttempts":{"type":"integer","description":"Maximum resale attempts"},"maximumListingsPerCustomer":{"type":"string","description":"Maximum listings per customer"},"minimumOwnershipPeriod":{"type":"string","format":"date-time","description":"Minimum ownership period"},"identityVerificationRequirement":{"type":"string","description":"Identity verification requirement"},"originalPurchaserOnly":{"type":"string","description":"Original purchaser only"},"membershipRestriction":{"type":"string","description":"Membership restriction"},"resaleImmediatelyAfterPurchase":{"type":"boolean","description":"Allow resale immediately after purchase"},"requiredConditions":{"type":"array","items":{"type":"string","enum":["fullyPaid","notScanned","notExpired","eventNotStarted","notRefunded","notComplimentary","notStaff","notInternal","notBlocked","notUnderDispute"]},"description":"Conditions a ticket must meet to be listed."}}},
"ResaleEligibilityRuleConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Eligibility Rule Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"performance":{"type":"string","description":"Performance"},"membershipType":{"type":"string","description":"Membership type"},"salesChannel":{"type":"string","description":"Sales channel"},"customerSegment":{"type":"string","description":"Customer segment"},"priceCategory":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price category"},"promotion":{"type":"string","description":"Promotion"},"ticketStatus":{"type":"string","description":"Ticket status"},"paymentStatus":{"type":"string","description":"Payment status"},"ticketOwnershipStatus":{"type":"string","description":"Ticket ownership status"},"specificResaleStartEndDate":{"type":"string","format":"date-time","description":"Specific resale start/end date"},"blackoutPeriod":{"type":"string","format":"date-time","description":"Blackout period"},"maximumResaleAttempts":{"type":"integer","description":"Maximum resale attempts"},"maximumListingsPerCustomer":{"type":"string","description":"Maximum listings per customer"},"minimumOwnershipPeriod":{"type":"string","format":"date-time","description":"Minimum ownership period"},"identityVerificationRequirement":{"type":"string","description":"Identity verification requirement"},"originalPurchaserOnly":{"type":"string","description":"Original purchaser only"},"membershipRestriction":{"type":"string","description":"Membership restriction"},"resaleImmediatelyAfterPurchase":{"type":"boolean","description":"Allow resale immediately after purchase"},"requiredConditions":{"type":"array","items":{"type":"string","enum":["fullyPaid","notScanned","notExpired","eventNotStarted","notRefunded","notComplimentary","notStaff","notInternal","notBlocked","notUnderDispute"]},"description":"Conditions a ticket must meet to be listed."}}},
"ResaleFeePolicy": {"type":"object","x-ticvai-persistence":"orders.resale_fee_policy","description":"**What a resale costs and how high it may be priced.** The listing snapshots these onto itself at creation; this is where they come from.\n**A rule and its snapshot are two rows on purpose.** `payments.fee_rule` and `orders.order_fee` already work this way — changing a commission must not restate what somebody already sold at.","required":["sellerFeePercent","buyerFeePercent","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The narrowest match wins.** Null is the venue default; a policy naming an event overrides it for that event, because a final and a Tuesday fixture do not resell on the same terms."},"productId":{"type":"string","format":"uuid","nullable":true},"sellerFeePercent":{"type":"number","description":"Deducted from the seller's proceeds."},"buyerFeePercent":{"type":"number","description":"Added to what the buyer pays."},"priceCapPercent":{"type":"number","nullable":true,"description":"**A ceiling as a percentage of face value.** Null means uncapped, which stays a venue decision rather than a default — the wording `ResaleListing.priceCapPercent` already uses, kept identical so the snapshot and its source cannot drift apart in meaning.\n**Anti-scalping limits are regulated in several jurisdictions**; whether they bind in the UAE and Oman is recorded as a research item on the resale backlog entry and is not settled here."},"minimumAskPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feesShownToSeller":{"type":"boolean","description":"**Whether the seller sees the deduction before listing.** A seller who learns the commission at payout is a complaint, and `ListingCreationSellerConfiguration` already draws an `estimatedProceeds` that needs this to be true to mean anything."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"ResaleFeesCommissionSellerProceedsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Fees, Commission & Seller Proceeds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tenant":{"type":"string","description":"Tenant"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"product":{"type":"string","description":"Product"},"sellerType":{"type":"string","description":"Seller type"},"buyerType":{"type":"string","description":"Buyer type"},"channel":{"type":"string","description":"Channel"},"currency":{"type":"string","description":"Currency"},"feeType":{"type":"string","enum":["sellerFee","buyerFee","marketplaceCommission","flatTransactionFee","percentageFee","paymentProcessingFee","administrativeFee","venueFee","taxOnFee"],"description":"Fee type."},"rate":{"type":"number","description":"Percentage rate, where the fee is a percentage"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed amount, where the fee is flat"},"payer":{"type":"string","enum":["seller","buyer"],"description":"Who pays the fee"}}},
"ResaleInventoryAvailabilityManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Inventory & Availability Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"product":{"type":"string","description":"Product"},"section":{"type":"string","description":"Section"},"row":{"type":"string","description":"Row"},"seat":{"type":"string","description":"Seat"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"listingStatus":{"type":"integer","description":"Listing status"}}},
"ResaleMarketplaceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Marketplace Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeListings":{"type":"integer","description":"Active Listings"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"ticketsAvailableForResale":{"type":"string","description":"Tickets Available for Resale"},"listingsSoldToday":{"type":"string","description":"Listings Sold Today"},"expiringListings":{"type":"integer","description":"Expiring Listings"},"suspendedListings":{"type":"integer","description":"Suspended Listings"},"rejectedListings":{"type":"integer","description":"Rejected Listings"},"averageResalePrice":{"type":"number","description":"Average Resale Price"},"grossResaleValue":{"type":"string","description":"Gross Resale Value"},"marketplaceFees":{"type":"integer","description":"Marketplace Fees"},"sellerProceeds":{"type":"integer","description":"Seller Proceeds"},"conversionRate":{"type":"number","description":"Conversion Rate"},"listingId":{"type":"string","description":"Listing ID"},"originalOrderTicketId":{"type":"string","description":"Original Order/Ticket ID"},"eventProduct":{"type":"string","description":"Event/Product"},"venue":{"type":"string","description":"Venue"},"eventDate":{"type":"string","format":"date-time","description":"Event Date"},"sectionRowSeat":{"type":"string","description":"Section/Row/Seat"},"seller":{"type":"string","description":"Seller"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original Price"},"listedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listed Price"},"priceVariance":{"type":"number","description":"Price Variance %"},"marketplaceFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Marketplace Fee"},"listingDate":{"type":"string","format":"date-time","description":"Listing Date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"status":{"type":"integer","description":"Status"},"riskIndicator":{"type":"string","description":"Risk Indicator"}}},
"ResaleMarketplaceConfig": {"type":"object","x-ticvai-persistence":"orders.resale_marketplace_config","description":"**How a venue's resale marketplace runs: terms, pricing mode and guardrails, moderation, listing lifecycle, buyer checkout hold, seller settlement timing, and the white-label deployment** (DM5, 29 September: data model for the agreed operations; MoM 1 Sep 4.14: admin-configured resale price range; own B2C site, hosted white-label portal, or API).\n**One row per venue.** The resale model is four tables and they do not overlap: what a resale costs is `orders.resale_fee_policy` (narrowable by event and product), which tickets may be resold is `orders.resale_eligibility_rule` (narrowable the same way), how the marketplace behaves is this row, and what each seller is owed is `orders.resale_settlement`. The listing snapshots what it needs at creation.\n**Written by `setResaleMarketplaceConfig` and read by `getResaleMarketplaceConfig`** (decided 29 September, writers pass).","required":["id","marketplaceName","pricingMode","moderationMode","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"marketplaceName":{"type":"string","maxLength":150},"pricingMode":{"type":"string","enum":["faceValueOnly","fixedPrice","sellerSelectedPrice","cappedPrice","operatorControlled","aiRecommendedPrice"]},"maximumDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"description":"The floor below face value, beside `ResaleFeePolicy.priceCapPercent` above it."},"sellerCanEditPrice":{"type":"boolean","default":true},"maximumPriceChanges":{"type":"integer","nullable":true,"minimum":0},"minimumMinutesBetweenPriceChanges":{"type":"integer","nullable":true,"minimum":0},"moderationMode":{"type":"string","default":"automatic","description":"`reviewTriggers` sends a listing to `pendingReview` when `moderationMode` is `riskBased`; `manual` reviews every listing.","enum":["automatic","riskBased","manual"]},"reviewTriggers":{"type":"array","items":{"type":"string","enum":["highResalePrice","unusualDiscount","highValueTicket","vipTicket","sellerRisk","newSeller","multipleListings","identityIssue","paymentIssue","ticketOwnershipConcern","fraudIndicator"]}},"expiryRule":{"type":"string","default":"atEventStart","enum":["xMinutesBeforeEvent","xHoursBeforeEvent","atEventStart","atConfiguredDate"]},"expiryOffset":{"type":"integer","nullable":true,"minimum":0,"description":"Minutes or hours, per `expiryRule`."},"withdrawalPolicy":{"type":"string","default":"sellerCannotWithdrawWhileReserved","enum":["sellerCanWithdrawAnytime","sellerCannotWithdrawWhileReserved"]},"maximumWithdrawals":{"type":"integer","nullable":true,"minimum":0},"cancellationFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"checkoutHoldMinutes":{"type":"integer","minimum":1,"default":10,"description":"How long a listing stays `reserved` for one buyer in checkout."},"buyerIdentityVerificationRequired":{"type":"boolean","default":false},"settlementTiming":{"type":"string","default":"afterAccessValidation","description":"**Default `afterAccessValidation`**: the seller is paid after the buyer is admitted, not after they pay (`ResaleListing.payoutStatus`).","enum":["immediatelyAfterResale","xDaysAfterResale","afterEventCompletion","xDaysAfterEvent","afterAccessValidation","operatorDefinedSettlementCycle"]},"settlementDelayDays":{"type":"integer","nullable":true,"minimum":0},"minimumPayoutThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"customerTerms":{"type":"string","maxLength":20000,"nullable":true},"sellerTerms":{"type":"string","maxLength":20000,"nullable":true},"buyerTerms":{"type":"string","maxLength":20000,"nullable":true},"termsVersion":{"type":"string","maxLength":20,"nullable":true,"description":"The version a seller accepts at listing."},"disclosures":{"type":"string","maxLength":4000,"nullable":true},"resaleTicketLabel":{"type":"string","maxLength":60,"nullable":true},"deploymentModel":{"type":"string","default":"ticvaiHostedWhiteLabel","enum":["embeddedWhiteLabel","ticvaiHostedWhiteLabel","headlessApi"]},"navigation":{"type":"array","items":{"type":"string","enum":["myTickets","sell","buy","myListings","transactions"]}},"authenticationMethod":{"type":"string","default":"customerAccount","enum":["customerAccount","sso","passwordlessLogin","otp","appAuthentication"]},"branding":{"type":"object","nullable":true,"description":"Logo, colours, typography, support contact and legal links for the marketplace pages. **A hosted white-label marketplace takes the venue's white-label theme when this is null**, so a venue sets it only to differ."},"domain":{"type":"string","maxLength":253,"nullable":true},"languages":{"type":"array","items":{"type":"string","maxLength":10}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ResalePolicyMarketplaceSettingsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Policy & Marketplace Settings displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"marketplaceName":{"type":"string","description":"Marketplace name"},"marketplaceStatus":{"type":"string","description":"Marketplace status"},"applicableOrganization":{"type":"string","description":"Applicable organization"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"currency":{"type":"string","description":"Currency"},"timeZone":{"type":"string","format":"date-time","description":"Time zone"},"supportedLanguage":{"type":"string","description":"Supported language"},"marketplaceSalesChannel":{"type":"string","description":"Marketplace sales channel"},"customerTerms":{"type":"string","description":"Customer terms"},"sellerTerms":{"type":"string","description":"Seller terms"},"sellerVerification":{"type":"string","description":"Seller verification"},"identityRequirements":{"type":"string","description":"Identity requirements"},"bankPayoutInformation":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Bank/payout information"},"sellerTermsAcceptance":{"type":"string","description":"Seller terms acceptance"},"listingConfirmation":{"type":"string","description":"Listing confirmation"},"sellerNotifications":{"type":"string","description":"Seller notifications"},"buyerTerms":{"type":"string","description":"Buyer terms"},"marketplaceDisclosures":{"type":"string","description":"Marketplace disclosures"},"resaleTicketLabeling":{"type":"string","description":"Resale ticket labeling"},"serviceFees":{"type":"string","description":"Service fees"},"purchaseLimits":{"type":"string","description":"Purchase limits"},"pricingMode":{"type":"string","enum":["sellerSelectsPermittedPrice","operatorDeterminesPrice"],"description":"Seller picks within the configured range (MoM 1 Sep: e.g. 10-20% below original) or the operator sets the price"}}},
"ResalePricingPriceGuardrailsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Pricing & Price Guardrails displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"faceValueOnly":{"type":"string","description":"Face-value only"},"minimumResalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum resale price"},"maximumResalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum resale price"},"maximumDiscount":{"type":"number","description":"Maximum discount %"},"fixedResalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed resale price"},"dynamicPermittedRange":{"type":"string","description":"Dynamic permitted range"},"eventSpecificRange":{"type":"string","description":"Event-specific range"},"productSpecificRange":{"type":"string","description":"Product-specific range"},"sellerCanEditPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Seller can edit price"},"numberOfPriceChanges":{"type":"integer","description":"Number of price changes"},"minimumIntervalBetweenChanges":{"type":"string","description":"Minimum interval between changes"},"automaticPriceReduction":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Automatic price reduction"},"priceAdjustmentCutoff":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price adjustment cutoff"},"originalFaceValue":{"type":"string","description":"Original face value"},"originalPaidPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original paid price"},"currentSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current selling price"},"currentDynamicPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current dynamic price"},"eventPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Event price"},"priceCategory":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price category"},"maximumMarkupPercent":{"type":"number","description":"Maximum markup, percent"}}}
}
```
