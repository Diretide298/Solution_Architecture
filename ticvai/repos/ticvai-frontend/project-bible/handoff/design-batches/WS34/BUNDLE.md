# WS34 — Pricing   Revenue Management board 1

**10 screens · 15 operations · 23 schemas · 4 permissions**

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
| `ADM-048` | Commercial Pricing Command Center | B–D | 2 | 26 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-049` | Price List Master Configuration | B–D | 21 | 20 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-050` | Price Category & Rate Type Library | B | 12 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-051` | Rate Structure Builder | B–D | 0 | 12 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `ADM-052` | Product & Service Price Assignment | B–D | 0 | 2 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-053` | Package, Bundle & Add-On Pricing | B–D | 21 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-054` | Market, Venue & Currency Pricing Structure | B–D | 23 | 0 | 5 | 0 | 1 | 4 | — | notStarted (generated) |
| `ADM-055` | Price Hierarchy & Inheritance Configuration | B | 10 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-056` | Price List Templates, Clone & Reuse | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-057` | Commercial Pricing Structure Validation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-050, ADM-057 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-048` Commercial Pricing Command Center

**Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each price list should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/commercial-pricing-command-center-adm-048` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive. Each needs an …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The first page a revenue or pricing administrator sees in the pricing module (TICVAI Console, acting inside a tenant, PR-1): every price list and pricing structure with its status, plus structure validation and package pricing at a glance. The client described the pricing module as about seven sub-screens; this hub links them.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive. (CHG-MOV-008)
- List operation(s) listBundlePricingCommercial return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBundlePricingCommercial carry no identifier. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): listMembershipCommercialPricing needs PLATFORM_TENANT_VIEW at tenant scope while the rest of the hub is venue-scoped PRODUCT_VIEW. (CHG-MOV-007).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search commercial pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, brand, market, country, currency, product type and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country | text field | — | — | `listCommercialPricing` ?country |
| Product type | text field | — | — | `listCommercialPricing` ?productType |
| Price list type | select | — | Standard retail · Venue · Attraction · Event · Membership · Group · Corporate · B2B · Reseller · Ota · Internal · Special market | `listCommercialPricing` ?priceListType |
| Venue | text field | — | — | `listCommercialPricing` ?venue |
| Brand | text field | — | — | `listCommercialPricing` ?brand |
| Market | text field | — | — | `listCommercialPricing` ?market |
| Currency | text field | — | pattern `^[A-Z]{3}$` | `listCommercialPricing` ?currency |
| Owner | text field | — | — | `listCommercialPricing` ?owner |
| Status | select | — | Draft · Configured · Validated · Active · Inactive · Expired · Archived | `listCommercialPricing` ?status |
| Search | text field | — | — | `listCommercialPricing` ?search |
| Severity | segmented control | — | Critical · Warning · Information | `listCommercialPricingStructure` ?severity |
| Category | select | — | Price list · Rate structure · Product mapping · Package · Market · Hierarchy | `listCommercialPricingStructure` ?category |
| Price list | text field | — | — | `listCommercialPricingStructure` ?priceListId |

#### Outputs: what the screen shows and produces

**Shown**

**Total Price Lists** (metric tile)

**Active Price Lists** (metric tile)

**Draft Price Lists** (metric tile)

**Price Categories** (metric tile)

**Configured Rates** (metric tile)

**Products with Pricing** (metric tile)

**Products Missing Pricing** (metric tile)

**Markets** (metric tile)

**Currencies** (metric tile)

**Pricing Validation Issues** (metric tile)

**Recently Modified Price Lists** (metric tile)

**Upcoming Price Structures** (metric tile)

**Every commercial pricing** (data table, from `listCommercialPricing`)

| Shows | Format | Notes |
|---|---|---|
| Price list | text | Price List ID |
| Name | text | Name |
| Code | text | Code |
| Type | chip: Standard retail, Venue, Attraction, Event, Membership, Group… | Price List Type (the pack's Price List Types, pp.6-7) |
| Currency | text | Currency: ISO 4217 code of the default currency |
| Market | text | Market |
| Venue | text | Venue |
| Brand | text | Brand |
| Product count | 1,234 | Product Count |
| Rate count | 1,234 | Rate Count |
| Version | text | Version |
| Status | text | Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's |
| Owner | text | Owner |

**The selected commercial pricing** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Price list | text | Price List ID |
| Name | text | Name |
| Code | text | Code |
| Type | chip: Standard retail, Venue, Attraction, Event, Membership, Group… | Price List Type (the pack's Price List Types, pp.6-7) |
| Currency | text | Currency: ISO 4217 code of the default currency |
| Market | text | Market |
| Venue | text | Venue |
| Brand | text | Brand |
| Product count | 1,234 | Product Count |
| Rate count | 1,234 | Rate Count |
| Version | text | Version |
| Status | text | Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's |
| Owner | text | Owner |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View Pricing, Modify Pricing Structure. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Price List (primary button) | navigation or local | — | — | — | — |
| Duplicate (secondary button) | navigation or local | — | — | — | — |
| Open (secondary button) | navigation or local | — | — | — | — |
| Compare (secondary button) | navigation or local | — | — | — | — |
| Validate (secondary button) | navigation or local | — | — | — | — |
| View Dependencies (secondary button) | navigation or local | — | — | — | — |
| Export (secondary button) | navigation or local | — | — | — | — |
| Archive (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPI row**: Total, active, draft and expiring price lists; lists failing validation; each a filter. *(source: contracts/spine/catalogue.yaml#listCommercialPricing / DI-591)*
- **price list table**: Code, name, type, scope, currency (read-only, from the region), status, valid dates, owner, consuming modules. *(source: contracts/spine/catalogue.yaml#listCommercialPricing / ADR-0018)*

**Data it reads**: `listCommercialPricing` (onLoad, Commercial Pricing Command Center); `listCommercialPricingStructure` (onLoad, Commercial Pricing Structure Validation); `listBundlePricingCommercial` (onLoad, Bundle Pricing & Commercial Model)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-050` Price Category & Rate Type Library: *Works in Price Category & Rate Type Library*; calls `listCommercialPricing`
- → `ADM-052` Product & Service Price Assignment: *Works in Product & Service Price Assignment*; calls `listCommercialPricing`
- → `ADM-053` Package, Bundle & Add-On Pricing: *Works in Package, Bundle & Add-On Pricing*; calls `listCommercialPricing`
- → `ADM-054` Market, Venue & Currency Pricing Structure: *Works in Market, Venue & Currency Pricing Structure*; calls `listCommercialPricing`
- → `ADM-055` Price Hierarchy & Inheritance Configuration: *Works in Price Hierarchy & Inheritance Configuration*; calls `listCommercialPricing`
- → `ADM-056` Price List Templates, Clone & Reuse: *Works in Price List Templates, Clone & Reuse*; calls `listCommercialPricing`
- → `ADM-057` Commercial Pricing Structure Validation: *Works in Commercial Pricing Structure Validation*; calls `listCommercialPricing`
- → `ADM-049` Price List Master Configuration: *Works in Price List Master Configuration, a section of BO-009, which saves the record with createPriceList…*; calls `listCommercialPricing`
- → `ADM-051` Rate Structure Builder: *Works in Rate Structure Builder, a section of BO-009, which saves the record with setPrices (setRateStructure…*; carries `priceListId`; calls `listCommercialPricing`

**What opens over it**

- confirmDialog *Archive*: **Archive on a commercial pricing is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-009`: Same price list columns and status badges as the venue's pricing screen (PR-10).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  priceLists: 14
  active: 9
  draft: 3
  failingValidation: 1
```

#### Permissions

- `listCommercialPricing` → `PRODUCT_VIEW` (read) · staff
- `listCommercialPricingStructure` → `PRODUCT_VIEW` (read) · staff
- `listBundlePricingCommercial` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-048` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-048`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 1: Opens Commercial Pricing Command Center → Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F143 branch at step 1 (expected): when Nothing has been set up on Commercial Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F143 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive.
- [ ] Every transition is wired: `BO-100`, `ADM-050`, `ADM-052`, `ADM-053`, `ADM-054`, `ADM-055`, `ADM-056`, `ADM-057`, `ADM-049`, `ADM-051`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-049` Price List Master Configuration

**Create the master container that holds commercial rates. A Price List should be reusable across products and channels. (a section of BO-009 Pricing Rules since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/pricing-rules/price-list-master-configuration-adm-049` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setPriceListMaster` duplicated BO-009 Pricing Rules's createPriceList and updatePriceList, so it is removed from the contract (BC-008) and BO-009 saves this record. This id stays the anchor of its section of BO-009: nothing on it writes separately. **Merged into BO-009 Pricing Rules as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-009: it renders inside BO-009's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The price list master on the TICVAI Console: the container that holds rates, its type, scope, owner, defaults (rate category, rounding profile, price hierarchy) and what it allows (overrides, inheritance, product-specific rates). Duplicate creates a new list from an old one (UAE Standard 2026 into UAE Standard 2027). Approval and publication of a list belong to the governance board, not here.

**Fixed on main** (the package already carries these; draw what it says): setPriceListMaster takes a defaultCurrency, and creates price lists a second way beside createPriceList. (CHG-CLN-001); No read operation: the screen declares only setPriceListMaster and nothing that returns the current configuration. (CHG-WIR-025).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack-derived Commercial screens (ADM-048 to ADM-317, ADM-559 to ADM-698) live on the TICVAI Console but configure venue-scoped records that the venue also edits on P08 (BO-009, BO-010, BO-011). Who uses them: the venue's own commercial team, or TICVAI staff acting for a tenant?** → The 410 workshop-pack screens on the TICVAI Console (370 Commercial, 20 Catalogue lifecycle, 20 Rules and workflow) are venue screens: move them to Venue Management (P08) and merge them with BO-008 product, BO-009 price matrix, BO-010 promotions, BO-011 bundles and the rules/workflow screens, so one surface edits each record. TICVAI staff reach them only through a platform-staff grant (R098). *(decided by Chinmay, 2026-10-02; DEC-100 / CHG-NOTE-006)*
- **Which way does price list priority run (does the higher or the lower number win)?** → Drawn default stands (answer: "Default: higher number wins"): Label it "Higher number wins" and show the overlapping lists. *(decided by Chinmay, 2026-10-02; DEC-101 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Price List Name | select field | — | — | — | — | — | — |
| Price List Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Price List Type | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Default Rate Category | select field | — | — | — | — | — | — |
| Default Rounding Profile | select field | — | — | — | — | — | — |
| Default Price Hierarchy | select field | — | — | — | — | — | — |
| Allow Overrides | select field | — | — | — | — | — | — |
| Allow Inheritance | select field | — | — | — | — | — | — |
| Allow Multiple Currencies | select field | — | — | — | — | — | — |
| Allow Product-Specific Rates | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listPriceLists` ?channel |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scope and venue context**: Scope (global, country, market, brand, venue, event, business unit) decides which of market, country, brand and venue are asked; the tenant and venue come from the console context (PR-1). *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceListMasterConfigurationInput / R098)*
- **defaults**: Default rate category, rounding profile and price hierarchy are pickers of records from ADM-050, ADM-075 and ADM-055, never free codes. *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceListMasterConfigurationInput)*
- **status**: Only Draft, Configured, Inactive and Archived are set here; Validated comes from structure validation (ADM-057), Active and Expired from governance. Show the others read-only. *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceListMasterConfigurationInput)*

#### Outputs: what the screen shows and produces

**Shown**

**List price lists** (data table, from `listPriceLists`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Channels | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Priority | 1,234 | Where lists overlap, higher priority wins. |
| Description | text | Price list master fields (29 September, data model DM3), set with `createPriceList` and `updatePriceList` since setPriceListMaster was … |
| Price list type | chip: Standard retail, Venue, Attraction, Event, Membership, Group… | — |
| Status | chip: Draft, Active, Inactive, Retired | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and … |
| Owner principal | the name it points at, never the id | — |
| Tags | list or chips (count when long) | — |
| Legal entity | the name it points at, never the id | — |
| Brand | text | — |
| Business unit | text | — |
| Country code | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **consuming modules**: The modules that use this list (ticketing, B2C, POS, kiosk, B2B, group sales, membership, F&B, retail, rental) as chips, so a change's reach is visible. *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceListMasterConfigurationInput)*
- **Where this screen lives**: A venue screen: it moves to Venue Management (P08) and merges with BO-008 product, BO-009 price matrix, BO-010 promotions and BO-011 bundles, so one surface edits each record. TICVAI staff reach it only under a platform-staff grant (R098). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-006))*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Duplicate**: New draft list with "copied from" set; the user is asked for the new code and validity. *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceListMasterConfigurationInput / DI-592)*

**Data it reads**: `listPriceLists` (onLoad, List price lists)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*
- → `BO-009` Pricing Rules: *Open Pricing Rules*; carries `priceListId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price list master configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price list master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price list master configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-009`: The venue's price lists on P08 are the same concept; same columns, badges and wording (PR-10).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
list:
  code: UAE-STD-2027
  name: UAE Standard 2027
  nameAr: الأسعار القياسية الإمارات 2027
  type: venue
  scope: venue
  venue: Dune Park
  owner: Revenue manager
  clonedFrom: UAE-STD-2026
  consumingModules:
  - ticketing
  - b2c
  - pos
  - kiosk
```

#### Permissions

- `listPriceLists` → `PRICE_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-049` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-049`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 2: Works in Price List Master Configuration, a section of BO-009, which saves the record with createPriceList and … → Create the master container that holds commercial rates. A Price List should be reusable across products and channels.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-049?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-048`, `BO-009`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-050` Price Category & Rate Type Library

**Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task APP-SETUP-ADM-050 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-category-rate-type-library-adm-050` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The tenant's standard library of price categories (who is priced: Adult, Child, Resident) and rate types (how: Standard, Peak, Member), so venues stop inventing "Adult Standard" and "Normal Adult". Standard entries ship with the tenant and can be deactivated, never deleted.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The list operation is venue-scoped (PRODUCT_VIEW) while the write is tenant-scoped (PRICE_CONFIGURE). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Entry kind | segmented control | — | Price category · Rate type | `listPriceCategoryRate` ?entryKind |
| Category family | text field | — | — | `listPriceCategoryRate` ?categoryFamily |
| Active | toggle | — | — | `listPriceCategoryRate` ?active |
| Search | text field | — | — | `listPriceCategoryRate` ?search |

**Form: Save price category rate type** (modal, opened by *Save price category rate type*; *Save price category rate type* calls `setPriceCategoryRateType`, *Cancel* sends nothing)

**Collects what `setPriceCategoryRateType` sends before it is called.** Required: `entryKind`, `code`, `name`, `isActive`. Optional: `description`, `categoryFamily`, `displayName`, `localizedDisplayNames`, `iconLabel`, `parentId`, `isStandard`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entry kind `entryKind` | segmented control | required | — | Price category · Rate type | — | — | `setPriceCategoryRateType` body |
| Code `code` | text field | required | — | max length 40 | — | Unique per `entryKind` within the tenant. | `setPriceCategoryRateType` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setPriceCategoryRateType` body |
| Description `description` | text area | optional | — | — | — | — | `setPriceCategoryRateType` body |
| Category family `categoryFamily` | text field | optional | — | max length 60 | — | — | `setPriceCategoryRateType` body |
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `setPriceCategoryRateType` body |
| Localized display names `localizedDisplayNames` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setPriceCategoryRateType` body |
| Icon label `iconLabel` | text field | optional | — | max length 40 | — | — | `setPriceCategoryRateType` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | A parent `catalogue.price_category` of the same `entryKind`. | `setPriceCategoryRateType` body |
| Is standard `isStandard` | toggle | optional | off | — | — | Shipped with the tenant; may be deactivated, not deleted. | `setPriceCategoryRateType` body |
| Sort order `sortOrder` | number field | optional | 100 | — | — | — | `setPriceCategoryRateType` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setPriceCategoryRateType` body |

Errors to draw in the form: 409 `inUse`.; 422 `invalidParent`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **entryKind and code**: Two tabs, Price categories and Rate types; code unique within its kind in the tenant, at most 40. *(source: contracts/spine/catalogue.yaml#setPriceCategoryRateType)*
- **parentId**: A parent of the same kind only (Child under Youth), shown as a tree. *(source: contracts/spine/catalogue.yaml#setPriceCategoryRateType)*
- **localizedDisplayNames**: The guest-facing name per language; the internal name stays English (PR-8). *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceCategory)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save price category rate type (primary button) | `setPriceCategoryRateType` PUT `/price-categories` | PriceCategory | PriceCategory | 409 `inUse`.; 422 `invalidParent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceCategoryRate` (onLoad, Price Category & Rate Type Library)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPriceCategoryRate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price category rate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price category rate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price category rate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price category rate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `inUse`.; 422 `invalidParent`. |

#### Edge cases to draw

- **Deactivate a standard entry in use**: Allowed, with the number of rates and ticket types using it shown first; delete is not offered for standard entries. *(source: contracts/spine/catalogue.yaml#/components/schemas/PriceCategory)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
priceCategories:
- code: ADULT
  name: Adult
  nameAr: بالغ
  standard: true
- code: CHILD
  name: Child (3-11)
  nameAr: طفل (3-11)
  standard: true
- code: RESIDENT
  name: UAE resident
  nameAr: مقيم في الإمارات
rateTypes:
- code: STD
  name: Standard
- code: PEAK
  name: Peak
- code: MEMBER
  name: Member
```

#### Permissions

- `listPriceCategoryRate` → `PRODUCT_VIEW` (read) · staff
- `setPriceCategoryRateType` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-050` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-050`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 4: Works in Price Category & Rate Type Library → Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save price category rate type.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-051` Rate Structure Builder

**Define the actual monetary rates contained within a price list. This is the core commercial configuration screen. (a section of BO-009 Pricing Rules since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | `priceListId` (navigation) |
| Route | `/venue-operations/pricing-rules/rate-structure-builder-adm-051` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setRateStructure` duplicated BO-009 Pricing Rules's setPrices, so it is removed from the contract (BC-009) and BO-009 saves this record. This id stays the anchor of its section of BO-009: nothing on it writes separately. **Merged into BO-009 Pricing Rules as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-009: it renders inside BO-009's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Per Ticket, Per Resource, Per Package, Per Membership Period. Each needs an operation, or needs removing …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The core commercial configuration: the monetary rates inside a price list, as a matrix of price category by rate type with a unit basis (per ticket, per person, per hour, per performance, per package, per membership period). Derived rates (Child = Adult minus 25%, VIP = Standard plus AED 200) are relationships, not dynamic pricing. Validation on save: duplicates, missing amounts, unsupported currency, invalid or circular derived rates.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Rates are written by setRateStructure here and by setPrices on BO-009, two writers for the price of one ticket type. (CHG-MOV-008)
- Pack actions with no operation: Per Ticket, Per Resource, Per Package, Per Membership Period. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setRateStructure and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **amount or derivedFrom**: A cell holds either an amount or a derivation (base rate and adjustment); a derived cell shows its computed amount greyed with the formula on hover; amount is ignored when derived. *(source: contracts/spine/catalogue.yaml#/components/schemas/RateStructureBuilderInput)*
- **precision**: 0 to 3 decimals, the third kept where the currency needs it. *(source: contracts/spine/catalogue.yaml#/components/schemas/RateStructureBuilderInput / DI-598)*

#### Outputs: what the screen shows and produces

**Shown**

**Every rate structure** (data table)

| Shows | Format | Notes |
|---|---|---|
| Duplicate rates | text | not in the schema: `Duplicate Rates` |
| Validation issues | list or chips (count when long) | Validation (pp.12-13): problems found on this rate; read-only |

**List prices in a list** (data table, from `listPrices`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Price list | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax code | the name it points at, never the id | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected rate structure** (detail panel): The pack groups this record's detail under its own headings: “Adult”, “Child Reduced”, “Senior Reduced”, “Resident Reduced”, “Group Group”, “Each rate should contain”.

| Shows | Format | Notes |
|---|---|---|
| Duplicate rates | text | not in the schema: `Duplicate Rates` |
| Validation issues | list or chips (count when long) | Validation (pp.12-13): problems found on this rate; read-only |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Per Ticket (primary button) | navigation or local | — | — | — | — |
| Per Resource (secondary button) | navigation or local | — | — | — | — |
| Per Package (secondary button) | navigation or local | — | — | — | — |
| Per Membership Period (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Matrix actions**: Add rate, Duplicate, Edit, Disable, Sort, Copy across categories, Compare, as buttons on the matrix. *(source: contracts/spine/catalogue.yaml#/components/schemas/RateStructureBuilderInput)*

**Data it reads**: `listPrices` (onLoad, List prices in a list)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*
- → `BO-009` Pricing Rules: *Open Pricing Rules*; carries `priceListId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rate structure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rate structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rate structure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rate structure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Circular derived rates (Adult from Child, Child from Adult)**: Refused on save with the cycle drawn. *(source: contracts/spine/catalogue.yaml#/components/schemas/RateStructureBuilderInput)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rates:
- category: Adult
  type: Standard
  basis: perTicket
  amount: AED 295.00
- category: Child
  type: Standard
  derivedFrom: Adult -25%
  amount: AED 221.25
- category: Adult
  type: Peak
  derivedFrom: Standard +AED 40.00
```

#### Permissions

- `listPrices` → `PRICE_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.22 | Dynamic Pricing Display - System shall display dynamic pricing. | Guest Mobile App & Branding | CONTRACTED | `listPrices` |
| 2.9.8 | The system should be able to regroup prices by category: Full price / reduced price / complimentary. | Ticketing Sales | CONTRACTED | `listPrices` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-051` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-051`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 6: Works in Rate Structure Builder, a section of BO-009, which saves the record with setPrices (setRateStructure retired … → Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Per Ticket, Per Resource, Per Package, Per Membership Period.
- [ ] Every transition is wired: `ADM-048`, `BO-009`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-052` Product & Service Price Assignment

**Connect commercial rates to the actual products and services being sold. (a section of BO-009 Pricing Rules since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Product configuration should display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/pricing-rules/product-service-price-assignment-adm-052` |

**What the spec says about it.** **Merged into BO-009 Pricing Rules as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-009: it renders inside BO-009's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Event, Venue. Each needs an operation, or needs removing from the screen; this is the Phase 3 … Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the product and service price assignments that setProductServicePrice writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Connect rates to what is sold: assign a price list's category rates to products, ticket types, events, performances, memberships, add-ons, F&B, retail, rentals and services, at the right level. The client's reference is one matrix of channel by variant (adult/child by onsite/online/kiosk); match or improve on it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setProductServicePrice and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Ticket Type, Event, Venue. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **assignment**: Object type, then the objects, then the scope (product, ticket type, event, performance, venue); category rates as a matrix of price category by channel. *(source: contracts/spine/catalogue.yaml#setProductServicePrice / DI-582)*

#### Outputs: what the screen shows and produces

**Shown**

**Every product service price** (data table, from `setProductServicePrice`)

| Shows | Format | Notes |
|---|---|---|
| Pricing source: UAE standard admission 2027 | text | not in the schema: `Pricing Source: UAE Standard Admission 2027` |

**The selected product service price** (detail panel): The pack groups this record's detail under its own headings: “Pricing can be assigned to”, “Dependency View”.

| Shows | Format | Notes |
|---|---|---|
| Pricing source: UAE standard admission 2027 | text | not in the schema: `Pricing Source: UAE Standard Admission 2027` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product Level (primary button) | navigation or local | — | — | — | — |
| Product Variant (secondary button) | navigation or local | — | — | — | — |
| Ticket Type (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setProductServicePrice`
- → `BO-009` Pricing Rules: *Open Pricing Rules*; carries `priceListId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product service price list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product service price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product service price yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product service price are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-009`: The venue price matrix is the same picture; one component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
  product: Day Pass
  rows:
  - Adult
  - Child
  columns:
  - Onsite
  - Online
  - Kiosk
  values:
  - - AED 310.00
    - AED 295.00
    - AED 299.00
  - - AED 260.00
    - AED 245.00
    - AED 249.00
```

#### Permissions

- `setProductServicePrice` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*
- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-052` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-052`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 8: Works in Product & Service Price Assignment → Connect commercial rates to the actual products and services being sold.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product Level, Product Variant, Ticket Type, Event, Venue.
- [ ] Every transition is wired: `ADM-048`, `BO-009`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-053` Package, Bundle & Add-On Pricing

**Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. Pricing defines how that bundle is priced. (a section of BO-011 Packages & Bundles since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure pricing for; Configure whether the customer sees) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/packages-bundles/package-bundle-add-on-pricing-adm-053` |

**What the spec says about it.** **Merged into BO-011 Packages & Bundles as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-011: it renders inside BO-011's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How packages, bundles and add-ons are priced: fixed package price, sum of components, discounted sum or component override, and what the guest sees (total only, components, or component and saving). Composition is defined in the catalogue; pricing here.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fast Track | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Meal | select field | — | — | — | — | — | — |
| Photo | select field | — | — | — | — | — | — |
| Equipment | select field | — | — | — | — | — | — |
| Upgrade | select field | — | — | — | — | — | — |
| Additional Session | select field | — | — | — | — | — | — |
| Premium Access | select field | — | — | — | — | — | — |
| Package Total Only | select field | — | — | — | — | — | — |
| Individual Components | select field | — | — | — | — | — | — |
| Component + Package Saving | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Record kind | segmented control | — | Package · Bundle · Add on | `listPackageBundleAdd` ?recordKind |
| Pricing model | radio group | — | Fixed package price · Sum of components · Discounted component sum · Component override | `listPackageBundleAdd` ?pricingModel |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listPackageBundleAdd` ?status |
| Search | text field | — | — | `listPackageBundleAdd` ?search |

**Form: Save package pricing definition** (modal, opened by *Save package pricing definition*; *Save package pricing definition* calls `setPackagePricingDefinition`, *Cancel* sends nothing)

**Collects what `setPackagePricingDefinition` sends before it is called.** Required: `productId`, `recordKind`, `pricingModel`, `status`. Optional: `name`, `priceListId`, `addOnType`, `packagePrice`, `components`, `componentPriceVisibility`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Record kind `recordKind` | segmented control | required | — | Package · Bundle · Add on | — | — | `setPackagePricingDefinition` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setPackagePricingDefinition` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Pricing model `pricingModel` | radio group | required | — | Fixed package price · Sum of components · Discounted component sum · Component override | — | — | `setPackagePricingDefinition` body |
| Add on type `addOnType` | select | optional | — | Fast track · Parking · Meal · Photo · Equipment · Upgrade · Additional performance · Premium access · Other | — | — | `setPackagePricingDefinition` body |
| Package price `packagePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPackagePricingDefinition` body |
| Components `components` | key and value settings | optional | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | `setPackagePricingDefinition` body |
| Component price visibility `componentPriceVisibility` | segmented control | optional | Package total only | Package total only · Individual components · Component and saving | — | — | `setPackagePricingDefinition` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setPackagePricingDefinition` body |

Errors to draw in the form: 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **pricingModel**: Four models as cards with a worked example; component prices appear only for component override. *(source: contracts/spine/catalogue.yaml#setPackagePricingDefinition)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed Package Price (primary button) | navigation or local | — | — | — | — |
| Component Override (secondary button) | navigation or local | — | — | — | — |
| Save package pricing definition (secondary button) | `setPackagePricingDefinition` PUT `/package-pricing` | PackagePricing | PackagePricing | 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPackageBundleAdd` (onLoad, Package, Bundle & Add-On Pricing)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPackageBundleAdd`
- → `BO-011` Packages & Bundles: *Open Packages & Bundles*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The package bundle add-on configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the package bundle add-on untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No package bundle add-on configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`. |

#### Consistency with other screens

- Match `BO-011`: The venue screen saves the same package pricing record.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package:
  product: Family Fun Bundle
  model: discountedComponentSum
  discount: 15%
  visibility: componentAndSaving
```

#### Permissions

- `listPackageBundleAdd` → `PRODUCT_VIEW` (read) · staff
- `setPackagePricingDefinition` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-053` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-053`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 10: Works in Package, Bundle & Add-On Pricing → Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-053?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed Package Price, Component Override, Save package pricing definition.
- [ ] Every transition is wired: `ADM-048`, `BO-011`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-054` Market, Venue & Currency Pricing Structure

**Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; FX-Assisted Setup) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/market-venue-currency-pricing-structure-adm-054` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The pricing structure across global, country, region, market and venue: which price list and rounding profile each node uses and whether it inherits from its parent.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The node carries a base and a selling currency and an FX reference rate. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Region | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| AED 250 ≈ SAR 255 | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Hierarchy level | radio group | — | Global · Country · Region · Market · Venue | `listMarketVenueCurrency` ?hierarchyLevel |
| Country | text field | — | — | `listMarketVenueCurrency` ?country |
| Market | text field | — | — | `listMarketVenueCurrency` ?market |
| Venue | text field | — | — | `listMarketVenueCurrency` ?venue |
| Legal entity | text field | — | — | `listMarketVenueCurrency` ?legalEntity |
| Currency | text field | — | pattern `^[A-Z]{3}$` | `listMarketVenueCurrency` ?currency |

**Form: Save market pricing configuration** (modal, opened by *Save market pricing configuration*; *Save market pricing configuration* calls `setMarketPricingConfiguration`, *Cancel* sends nothing)

**Collects what `setMarketPricingConfiguration` sends before it is called.** Required: `hierarchyLevel`. Optional: `parentId`, `countryCode`, `marketCode`, `region`, `venueId`, `brand`, `legalEntityId`, `baseCurrency`, `sellingCurrency`, `roundingProfileId`, `displayFormat`, `priceListId` and 2 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Hierarchy level `hierarchyLevel` | radio group | required | — | Global · Country · Region · Market · Venue | — | — | `setMarketPricingConfiguration` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | The parent `catalogue.pricing_market`. | `setMarketPricingConfiguration` body |
| Country code `countryCode` | text field | optional | — | max length 2; pattern `^[A-Z]{2}$` | — | — | `setMarketPricingConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setMarketPricingConfiguration` body |
| Region `region` | text field | optional | — | max length 100 | — | — | `setMarketPricingConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Brand `brand` | text field | optional | — | max length 100 | — | — | `setMarketPricingConfiguration` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Base currency `baseCurrency` | text field | optional | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setMarketPricingConfiguration` body |
| Selling currency `sellingCurrency` | text field | optional | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setMarketPricingConfiguration` body |
| Rounding profile `roundingProfileId` | picker: choose a rounding profile | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Display format `displayFormat` | text field | optional | — | max length 40 | — | — | `setMarketPricingConfiguration` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Inherits from parent `inheritsFromParent` | toggle | optional | on | — | — | — | `setMarketPricingConfiguration` body |
| FX reference rate `fxReferenceRate` | number field (%) | optional | — | — | — | Reference only; FX supplies inputs, it never decides a price. | `setMarketPricingConfiguration` body |

Errors to draw in the form: 422 `currencyNotVenueCurrency` or `invalidParent`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **node**: A tree; each node shows Inherited or Set here (PR-4), its price list and rounding profile. *(source: contracts/spine/catalogue.yaml#setMarketPricingConfiguration / ADR-0018)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save market pricing configuration (primary button) | `setMarketPricingConfiguration` PUT `/pricing-markets` | PricingMarket | PricingMarket | 422 `currencyNotVenueCurrency` or `invalidParent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listMarketVenueCurrency` (onLoad, Market, Venue & Currency Pricing Structure)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listMarketVenueCurrency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The market venue currency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the market venue currency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No market venue currency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `currencyNotVenueCurrency` or `invalidParent`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree:
- Global
- UAE (AED)
- Dubai market
- 'Dune Park venue: price list UAE-STD-2027'
```

#### Permissions

- `listMarketVenueCurrency` → `PRODUCT_VIEW` (read) · staff
- `setMarketPricingConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-054` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-054`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 12: Works in Market, Venue & Currency Pricing Structure → Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-054?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save market pricing configuration.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-055` Price Hierarchy & Inheritance Configuration

**Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task APP-SETUP-ADM-055 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators configure; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-hierarchy-inheritance-configuration-adm-055` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the price hierarchy and inheritance configuration that setPriceHierarchyInheritance writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a price comes from when several layers could supply it (global, market, venue, event, product, channel, segment): an ordered list of levels saved as a whole, so two sources can never sit at equal priority. The client decided the hierarchy decides; there is no lowest-price default.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setPriceHierarchyInheritance and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Hierarchy Level | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Inheritance | select field | — | — | — | — | — | — |
| Override Permission | select field | — | — | — | — | — | — |
| Fallback Behavior | select field | — | — | — | — | — | — |
| Override Allowed | select field | — | — | — | — | — | — |
| Override Requires Reason | select field | — | — | — | — | — | — |
| Maximum Override Range | select field | — | — | — | — | — | — |
| Override Expiry | select field | — | — | — | — | — | — |
| Return to Parent Price | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **levels**: Drag-to-order list with a "falls back to" arrow between levels; saving sends the whole order. *(source: contracts/spine/catalogue.yaml#setPriceHierarchyInheritance / DI-592 / DI-595)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **worked example**: Pick a product and channel and see which level supplied its price today ("Dune Park venue list, because no event price exists"). *(source: designer default)*

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setPriceHierarchyInheritance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price hierarchy inheritance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price hierarchy inheritance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price hierarchy inheritance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-441`: Rule priority (which adjustment wins) is a separate screen; name both clearly so they are not confused.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
hierarchy:
  name: UAE default
  levels:
  - Contract / corporate rate
  - Event price
  - Venue price list
  - Market price list
  - Global base
```

#### Permissions

- `setPriceHierarchyInheritance` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- When several rules apply to one sale (e.g. summer rate plus school-group discount) the configurable pricing hierarchy decides; there is no automatic lowest-price-wins default. *(agreed · MoM 1 Sep 2026, 4.4 Seasonal & Date-Based Pricing; Rule Priority · DI-595)*
- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-055` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-055`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 14: Works in Price Hierarchy & Inheritance Configuration → Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-055?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-056` Price List Templates, Clone & Reuse

**Accelerate commercial setup across new venues, events, seasons and markets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-list-templates-clone-reuse-adm-056` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure. Each …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Templates for products and price lists, and cloning one into a new venue, event, season or market, choosing what is copied and which fields must be reviewed (dates, prices, venue, capacity, tax, channels).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☑ Copy categories | select field | — | — | — | — | — | — |
| ☑ Copy rate structure | text field | — | — | — | — | — | — |
| ☑ Copy product mapping | text field | — | — | — | — | — | — |
| ☐ Copy monetary values | text field | — | — | — | — | — | — |
| ☑ Increase values by 5% | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template type | text field | — | — | `listPriceListTemplate` ?templateType |
| Status | segmented control | — | Draft · Active · Archived | `listPriceListTemplate` ?status |
| Search | text field | — | — | `listPriceListTemplate` ?search |

**Form: Save configuration template** (modal, opened by *Save configuration template*; *Save configuration template* calls `setConfigurationTemplate`, *Cancel* sends nothing)

**Collects what `setConfigurationTemplate` sends before it is called.** Required: `subject`, `name`, `status`. Optional: `description`, `templateKind`, `productKind`, `venueId`, `sourceProductId`, `sourcePriceListId`, `includedComponents`, `reviewFields`, `isAiDrafted`, `ownerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subject` | segmented control | required | — | Product · Price list | — | — | `setConfigurationTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setConfigurationTemplate` body |
| Description `description` | text area | optional | — | — | — | — | `setConfigurationTemplate` body |
| Template kind `templateKind` | text field | optional | — | max length 60 | — | Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`. | `setConfigurationTemplate` body |
| Product kind `productKind` | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `setConfigurationTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source product `sourceProductId` | picker: choose a source product | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source price list `sourcePriceListId` | picker: choose a source price list | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Included components `includedComponents` | list of values (chips) | optional | — | — | — | Product or price-list component names, per `subject`. | `setConfigurationTemplate` body |
| Review fields `reviewFields` | multi-select chips | optional | — | Dates · Prices · Venue · Capacity · Event · Tax · Channels | — | — | `setConfigurationTemplate` body |
| Is AI drafted `isAiDrafted` | toggle | optional | off | — | — | — | `setConfigurationTemplate` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setConfigurationTemplate` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |

Errors to draw in the form: 422 `sourceRequired`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **reviewFields**: After a clone the listed fields are highlighted for review and the clone cannot be activated until each is confirmed. *(source: contracts/spine/catalogue.yaml#setConfigurationTemplate)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Complete Price List (primary button) | navigation or local | — | — | — | — |
| Rate Structure Only (secondary button) | navigation or local | — | — | — | — |
| Selected Categories (secondary button) | navigation or local | — | — | — | — |
| Product Assignments (secondary button) | navigation or local | — | — | — | — |
| Market Structure (secondary button) | navigation or local | — | — | — | — |
| Save configuration template (secondary button) | `setConfigurationTemplate` PUT `/configuration-templates` | ConfigurationTemplate | ConfigurationTemplate | 422 `sourceRequired`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceListTemplate` (onLoad, Price List Templates, Clone & Reuse)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPriceListTemplate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price list templates configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price list templates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price list templates configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `sourceRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
template:
  name: Water park admission 2027
  subject: priceList
  includes:
  - rates
  - categories
  review:
  - dates
  - prices
```

#### Permissions

- `listPriceListTemplate` → `PRODUCT_VIEW` (read) · staff
- `setConfigurationTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-056` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-056`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 16: Works in Price List Templates, Clone & Reuse → Accelerate commercial setup across new venues, events, seasons and markets.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-056?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure, Save configuration template.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-057` Commercial Pricing Structure Validation

**Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns approval and publication. Board 1 defined what the commercial prices are and how they are structured.**

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
| Route | `/commercial/commercial-pricing-structure-validation-adm-057` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Checks that the pricing foundation is complete before rules, governance or publication: missing rates, unsupported currency, invalid derived rates, lists without categories. Not the publication screen.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | segmented control | — | Critical · Warning · Information | `listCommercialPricingStructure` ?severity |
| Category | select | — | Price list · Rate structure · Product mapping · Package · Market · Hierarchy | `listCommercialPricingStructure` ?category |
| Price list | text field | — | — | `listCommercialPricingStructure` ?priceListId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **checks**: Per price list, each check passed or failed with a link to fix it; a list moves to Validated only when all pass. *(source: contracts/spine/catalogue.yaml#listCommercialPricingStructure / DI-592)*

**Data it reads**: `listCommercialPricingStructure` (onLoad, Commercial Pricing Structure Validation)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial pricing structure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial pricing structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial pricing structure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial pricing structure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  list: UAE-STD-2027
  passed: 11
  failed:
  - Child rate missing for Twilight Ticket
```

#### Permissions

- `listCommercialPricingStructure` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-057` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-057`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 18: Works in Commercial Pricing Structure Validation → Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
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

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBundlePricingCommercial": {"method":"GET","path":"/bundle-pricing-commercial","contract":"promotions","summary":"Bundle Pricing & Commercial Model","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundlePricingCommercialModelView"},
"listCommercialPricing": {"method":"GET","path":"/commercial-pricing","contract":"catalogue","summary":"Commercial Pricing Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"country","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"priceListType","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCommercialPricingStructure": {"method":"GET","path":"/commercial-pricing-structure","contract":"catalogue","summary":"Commercial Pricing Structure Validation","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"priceListId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMarketVenueCurrency": {"method":"GET","path":"/market-venue-currency","contract":"catalogue","summary":"Market, Venue & Currency Pricing Structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"hierarchyLevel","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"legalEntity","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPackageBundleAdd": {"method":"GET","path":"/package-bundle-add","contract":"catalogue","summary":"Package, Bundle & Add-On Pricing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"recordKind","in":"query","required":false},{"name":"pricingModel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceCategoryRate": {"method":"GET","path":"/price-category-rate","contract":"catalogue","summary":"Price Category & Rate Type Library","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"entryKind","in":"query","required":false},{"name":"categoryFamily","in":"query","required":false},{"name":"active","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceListTemplate": {"method":"GET","path":"/price-list-template","contract":"catalogue","summary":"Price List Templates, Clone & Reuse","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceLists": {"method":"GET","path":"/price-lists","contract":"catalogue","summary":"List price lists","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrices": {"method":"GET","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"List prices in a list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setConfigurationTemplate": {"method":"PUT","path":"/configuration-templates","contract":"catalogue","summary":"Create or update a product or price-list template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationTemplate","responds":"ConfigurationTemplate"},
"setMarketPricingConfiguration": {"method":"PUT","path":"/pricing-markets","contract":"catalogue","summary":"Create or update a node of the market pricing structure","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingMarket","responds":"PricingMarket"},
"setPackagePricingDefinition": {"method":"PUT","path":"/package-pricing","contract":"catalogue","summary":"Set how a package, bundle or add-on is priced","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackagePricing","responds":"PackagePricing"},
"setPriceCategoryRateType": {"method":"PUT","path":"/price-categories","contract":"catalogue","summary":"Create or update a price category or rate type","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceCategory","responds":"PriceCategory"},
"setPriceHierarchyInheritance": {"method":"PUT","path":"/price-hierarchy-inheritance","contract":"catalogue","summary":"Price Hierarchy & Inheritance Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceHierarchyInheritanceConfigurationInput","responds":"PriceHierarchyInheritanceConfigurationView"},
"setProductServicePrice": {"method":"PUT","path":"/product-service-price","contract":"catalogue","summary":"Product & Service Price Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductServicePriceAssignmentInput","responds":"ProductServicePriceAssignmentView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BundlePricingCommercialModelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Pricing & Commercial Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Base price"},"currency":{"type":"string","description":"Currency"},"discount":{"type":"number","description":"Discount %"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount amount"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum price"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum price"},"priceFloor":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price floor"},"marginFloor":{"type":"number","description":"Margin floor"},"guestSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guest-specific price"},"channelSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Channel-specific price"},"pricingModel":{"type":"string","enum":["fixedBundlePrice","sumMinusDiscount","componentPricing","startingFrom","tieredBundlePrice","dynamicBundlePrice"],"description":"How the bundle is priced; a dynamic bundle price is calculated by the pricing engine"},"upgradeCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Surcharge when the guest picks a premium option"}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CommercialPricingCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Commercial Pricing Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalPriceLists":{"type":"integer","description":"Total Price Lists"},"activePriceLists":{"type":"integer","description":"Active Price Lists"},"draftPriceLists":{"type":"integer","description":"Draft Price Lists"},"priceCategories":{"type":"integer","description":"Price Categories"},"configuredRates":{"type":"integer","description":"Configured Rates"},"productsWithPricing":{"type":"integer","description":"Products with Pricing: sellable products that reference at least one active price list rate"},"productsMissingPricing":{"type":"integer","description":"Products Missing Pricing: active sellable products with no price list rate"},"markets":{"type":"integer","description":"Markets"},"currencies":{"type":"integer","description":"Currencies"},"pricingValidationIssues":{"type":"integer","description":"Pricing Validation Issues"},"recentlyModifiedPriceLists":{"type":"integer","description":"Recently Modified Price Lists: price lists changed in the last 7 days (decided 29 September, readiness close-out)"},"upcomingPriceStructures":{"type":"integer","description":"Upcoming Price Structures: price lists whose effective-from date is in the future"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"CommercialPricingCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Commercial Pricing Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceListId":{"type":"string","description":"Price List ID"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"type":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"description":"Price List Type (the pack's Price List Types, pp.6-7)"},"currency":{"type":"string","description":"Currency: ISO 4217 code of the default currency","pattern":"^[A-Z]{3}$"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"productCount":{"type":"integer","description":"Product Count"},"rateCount":{"type":"integer","description":"Rate Count"},"version":{"type":"string","description":"Version"},"status":{"type":"string","description":"Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's"},"owner":{"type":"string","description":"Owner"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From (the first half of the pack's Effective Period)"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"CommercialPricingStructureValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Commercial Pricing Structure Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"findingId":{"type":"string","description":"Finding ID"},"category":{"type":"string","enum":["priceList","rateStructure","productMapping","package","market","hierarchy"],"description":"Validation Category (pp.19-20)"},"check":{"type":"string","enum":["requiredFieldsComplete","currencyDefined","ownershipAssigned","categoriesConfigured","monetaryValuesValid","derivedRelationshipsValid","requiredProductsPriced","noOrphanAssignments","componentPricingValid","currencyAndVenueConfigurationValid","noConflictingSourcePriority","fallbackConfigured"],"description":"The check that failed"},"severity":{"type":"string","enum":["critical","warning","information"],"description":"Validation Results: critical (sale cannot proceed), warning (review), information (optimization suggestion)"},"message":{"type":"string","description":"What was found, e.g. \"7 active ticket products have no Adult rate\""},"subjectType":{"type":"string","enum":["priceList","rate","priceCategory","product","package","venue","market","hierarchy"],"description":"What the finding is about"},"subjectId":{"type":"string","description":"ID of that record"},"aiGenerated":{"type":"boolean","description":"Raised by AI QA rather than a rule; advisory"}}},
"ConfigurationTemplate": {"type":"object","x-ticvai-persistence":"catalogue.configuration_template","description":"**A reusable starting point for a product or a price list** (29 September, data model DM3). Merges the product duplication and template library (ADM-126) and price list templates (ADM-063). `subject` says which; a template copies the listed components and marks `reviewFields` for the operator to confirm.","required":["id","scopePath","subject","name","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"subject":{"type":"string","enum":["product","priceList"]},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"templateKind":{"type":"string","maxLength":60,"nullable":true,"description":"Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`."},"productKind":{"allOf":[{"$ref":"#/components/schemas/ProductKind"}],"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceProductId":{"type":"string","format":"uuid","nullable":true},"sourcePriceListId":{"type":"string","format":"uuid","nullable":true},"includedComponents":{"type":"array","items":{"type":"string"},"description":"Product or price-list component names, per `subject`."},"reviewFields":{"type":"array","items":{"type":"string","enum":["dates","prices","venue","capacity","event","tax","channels"]}},"isAiDrafted":{"type":"boolean","default":false},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MarketVenueCurrencyPricingStructureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Market, Venue & Currency Pricing Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"country":{"type":"string","description":"Country"},"market":{"type":"string","description":"Market"},"region":{"type":"string","description":"Region"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"legalEntity":{"type":"string","description":"Legal Entity"},"baseCurrency":{"type":"string","description":"Base Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"sellingCurrency":{"type":"string","description":"Selling Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"currencyPrecision":{"type":"integer","description":"Currency Precision: decimal places, 0 to 3","minimum":0,"maximum":3},"rounding":{"type":"string","description":"Rounding: code of the currency rounding rule (ADM-075)"},"displayFormat":{"type":"string","description":"Display Format: e.g. \"AED 1,250.00\" or \"1.250,00 EUR\""},"structureId":{"type":"string","description":"Pricing structure node ID"},"hierarchyLevel":{"type":"string","enum":["global","country","region","market","venue"],"description":"Level of this node in the Market Hierarchy (p.15)"},"parentStructureId":{"type":"string","nullable":true,"description":"Parent node; empty for Global"},"priceListId":{"type":"string","nullable":true,"description":"Price list governing this node; empty when it inherits"},"inheritsFromParent":{"type":"boolean","description":"Venue Overrides (p.16): true when the node uses its parent's prices (Abu Dhabi Venue -> inherit AED 250)"},"fxReferenceRate":{"type":"number","nullable":true,"description":"FX-Assisted Setup: reference rate base -> selling currency shown during setup; advisory"}}},
"PackageBundleAddOnPricingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Package, Bundle & Add-On Pricing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"packagePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Package Price: the fixed or derived price charged for the package (AED 850 in the example)"},"pricingId":{"type":"string","description":"Package / add-on pricing ID"},"recordKind":{"type":"string","enum":["package","bundle","addOn"],"description":"What is priced"},"productId":{"type":"string","description":"The catalogue package, bundle or add-on product"},"name":{"type":"string","description":"Name"},"priceListId":{"type":"string","description":"Price list the pricing belongs to"},"pricingModel":{"type":"string","enum":["fixedPackagePrice","sumOfComponents","discountedComponentSum","componentOverride"],"description":"Package Pricing Model (p.14)","nullable":true},"addOnType":{"type":"string","enum":["fastTrack","parking","meal","photo","equipment","upgrade","additionalPerformance","premiumAccess","other"],"description":"Add-On Pricing kind (p.15); additionalPerformance is the design's \"additional session\"; empty for a package","nullable":true},"components":{"type":"array","items":{"type":"object","properties":{"productId":{"type":"string"},"quantity":{"type":"integer"},"role":{"type":"string","enum":["included","requiredPaid","optionalPaid"]},"componentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"description":"Components with their role (Required vs Optional, p.15) and the price each contributes"},"normalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Normal Total: sum of the components at their own rates; read-only"},"packageSaving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial package saving: normal total less package price; read-only"},"componentPriceVisibility":{"type":"string","enum":["packageTotalOnly","individualComponents","componentAndSaving"],"description":"Component Price Visibility (p.15): what the customer sees"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"validationIssues":{"type":"array","description":"Bundle Price Integrity (p.15)","items":{"type":"object","properties":{"code":{"type":"string","enum":["componentPriceChanged","missingComponentRate","packageAboveNormalTotal"]},"message":{"type":"string"}}}}}},
"PackagePricing": {"type":"object","x-ticvai-persistence":"catalogue.package_pricing","description":"**How a package, bundle or add-on is priced from its components** (29 September, data model DM3). ADM-062. The bundle's composition for sale stays `catalogue.published_bundle`; this row is its pricing model. `normalTotal` and `packageSaving` are computed on read from the component rates.","required":["id","scopePath","productId","recordKind","pricingModel","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"productId":{"type":"string","format":"uuid"},"recordKind":{"type":"string","enum":["package","bundle","addOn"]},"name":{"type":"string","maxLength":200,"nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"pricingModel":{"type":"string","enum":["fixedPackagePrice","sumOfComponents","discountedComponentSum","componentOverride"]},"addOnType":{"type":"string","enum":["fastTrack","parking","meal","photo","equipment","upgrade","additionalPerformance","premiumAccess","other",null],"nullable":true},"packagePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"components":{"type":"object","additionalProperties":true,"description":"`[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`."},"componentPriceVisibility":{"type":"string","enum":["packageTotalOnly","individualComponents","componentAndSaving"],"default":"packageTotalOnly"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Price": {"x-ticvai-persistence":"catalogue.price","type":"object","required":["priceListId","variantId","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"priceListId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true}}},
"PriceCategory": {"type":"object","x-ticvai-persistence":"catalogue.price_category","description":"**The library of price categories and rate types** (29 September, data model DM3). ADM-059. A price category is who or what is priced (Adult, Child, Resident ...); a rate type is how (Standard, Peak, Member ...). Both are rows here, `entryKind` says which. Distinct from `catalogue.product_category`, which groups merchandise.","required":["id","scopePath","entryKind","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"entryKind":{"type":"string","enum":["priceCategory","rateType"]},"code":{"type":"string","maxLength":40,"description":"Unique per `entryKind` within the tenant."},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"categoryFamily":{"type":"string","maxLength":60,"nullable":true},"displayName":{"type":"string","maxLength":200,"nullable":true},"localizedDisplayNames":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"iconLabel":{"type":"string","maxLength":40,"nullable":true},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"A parent `catalogue.price_category` of the same `entryKind`."},"isStandard":{"type":"boolean","default":false,"description":"Shipped with the tenant; may be deactivated, not deleted."},"sortOrder":{"type":"integer","default":100},"isActive":{"type":"boolean","default":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PriceCategoryRateTypeLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Category & Rate Type Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"categoryId":{"type":"string","description":"Category ID"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"description":{"type":"string","description":"Description"},"categoryFamily":{"type":"string","description":"Category Family: e.g. Visitor or Member (Parent/Child Structure, p.10)"},"displayName":{"type":"string","description":"Display Name"},"iconLabel":{"type":"string","description":"Icon/Label"},"active":{"type":"boolean","description":"Active/Inactive: true when the category can be used on new rates"},"entryKind":{"type":"string","enum":["priceCategory","rateType"],"description":"Whether the row is a price category (who the price represents) or a rate type (how the rate behaves: standard, reduced, contract, negotiated, complimentary, fixed, derived, package, add-on), p.10"},"standard":{"type":"boolean","description":"A TICVAI standard category (Adult, Child, Junior, Senior, Student, Resident, Non-Resident, Member, VIP, Group, Corporate, B2B, Complimentary, Staff, Promotional) rather than a custom one"},"sortOrder":{"type":"integer","description":"Sort Order"},"parentCategoryId":{"type":"string","nullable":true,"description":"Parent category (Parent/Child Structure: Visitor -> Adult, Member -> Gold); empty for a top-level category"},"localizedDisplayNames":{"type":"object","additionalProperties":{"type":"string"},"description":"Display name per language code, at least en and ar (Localization, p.11)"},"possibleDuplicateOf":{"type":"array","items":{"type":"string"},"description":"AI Standardization: ids of categories that appear to mean the same thing (Kids / Child / Children Rate); advisory"}}},
"PriceHierarchyInheritanceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 17%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Price Hierarchy & Inheritance Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"hierarchyId":{"type":"string","description":"Price hierarchy ID; empty on create"},"name":{"type":"string","description":"Hierarchy name"},"levels":{"type":"array","items":{"type":"object","properties":{"hierarchyLevel":{"type":"string","enum":["globalMaster","country","market","venue","product","approvedOverride"],"description":"Hierarchy Level (Example Hierarchy, p.17)"},"priority":{"type":"integer","description":"Priority; the lower number is the more general level, the most specific existing price wins"},"inheritance":{"type":"boolean","description":"Inheritance: the level takes its parent's price when it has none of its own"},"overrideAllowed":{"type":"boolean","description":"Override Permission / Override Allowed"},"overrideRequiresReason":{"type":"boolean","description":"Override Requires Reason"},"maximumOverrideRangePercent":{"type":"number","nullable":true,"description":"Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"},"overrideExpiryDays":{"type":"integer","nullable":true,"description":"Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"},"returnToParentPrice":{"type":"boolean","description":"Return to Parent Price when an override expires"},"fallbackBehavior":{"type":"string","enum":["useParent","useDefault","blockSale"],"description":"Fallback (p.18): what happens when a child rate does not exist"}}},"description":"Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"}}},
"PriceHierarchyInheritanceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Hierarchy & Inheritance Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"hierarchyId":{"type":"string","description":"Price hierarchy ID; empty on create"},"name":{"type":"string","description":"Hierarchy name"},"levels":{"type":"array","items":{"type":"object","properties":{"hierarchyLevel":{"type":"string","enum":["globalMaster","country","market","venue","product","approvedOverride"],"description":"Hierarchy Level (Example Hierarchy, p.17)"},"priority":{"type":"integer","description":"Priority; the lower number is the more general level, the most specific existing price wins"},"inheritance":{"type":"boolean","description":"Inheritance: the level takes its parent's price when it has none of its own"},"overrideAllowed":{"type":"boolean","description":"Override Permission / Override Allowed"},"overrideRequiresReason":{"type":"boolean","description":"Override Requires Reason"},"maximumOverrideRangePercent":{"type":"number","nullable":true,"description":"Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"},"overrideExpiryDays":{"type":"integer","nullable":true,"description":"Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"},"returnToParentPrice":{"type":"boolean","description":"Return to Parent Price when an override expires"},"fallbackBehavior":{"type":"string","enum":["useParent","useDefault","blockSale"],"description":"Fallback (p.18): what happens when a child rate does not exist"}}},"description":"Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"},"validationIssues":{"type":"array","description":"Conflict Detection (p.18); read-only","items":{"type":"object","properties":{"code":{"type":"string","enum":["equalPriority","missingFallback","circularInheritance"]},"message":{"type":"string"}}}}}},
"PriceList": {"x-ticvai-persistence":"catalogue.price_list","type":"object","required":["id","code","name","venueId","currency","currencyScale","channels"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"priority":{"type":"integer","description":"Where lists overlap, higher priority wins."},"description":{"type":"string","nullable":true,"description":"Price list master fields (29 September, data model DM3), set with `createPriceList` and `updatePriceList` since setPriceListMaster was retired in r2 (BC-008, CHG-CLN-001)."},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"default":"standardRetail"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"scopeLevel":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"default":"venue"},"defaultPriceCategoryId":{"type":"string","format":"uuid","nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"priceResolutionPolicyId":{"type":"string","format":"uuid","nullable":true},"allowOverrides":{"type":"boolean","default":false},"allowInheritance":{"type":"boolean","default":true},"allowMultipleCurrencies":{"type":"boolean","default":false},"allowProductSpecificRates":{"type":"boolean","default":true},"clonedFromPriceListId":{"type":"string","format":"uuid","nullable":true},"currentVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The active `catalogue.price_list_version`."}}},
"PriceListTemplatesCloneReuseView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price List Templates, Clone & Reuse displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Template ID"},"name":{"type":"string","description":"Template name, e.g. Theme Park Pricing"},"templateType":{"type":"string","description":"Template Library type: standardAttraction, themePark, museum, concert, sports, membership, group, corporate, b2b, rental or custom (p.18)"},"description":{"type":"string","description":"Description"},"components":{"type":"array","items":{"type":"string","enum":["priceCategories","rateTypes","rateMatrixStructure","currencyStructure","hierarchy","productMappingPattern","packagePricingPattern"]},"description":"Template Components the template carries (p.18)"},"sourcePriceListId":{"type":"string","nullable":true,"description":"Price list the template was taken from; empty when built directly"},"aiDrafted":{"type":"boolean","description":"Drafted by AI-assisted template generation and awaiting administrator review"},"status":{"type":"string","description":"Status: draft, active or archived"},"owner":{"type":"string","description":"Owner"}}},
"PricingMarket": {"type":"object","x-ticvai-persistence":"catalogue.pricing_market","description":"**A node of the market pricing structure: global, country, region, market or venue** (29 September, data model DM3). ADM-064. Says which price list and rounding a market uses and whether it inherits from its parent. **At venue level the selling currency is the venue's trading currency** and cannot differ from it (ADR-0018, frozen once the venue has traded); above venue level the currencies are reporting and base currencies.","required":["id","scopePath","hierarchyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"hierarchyLevel":{"type":"string","enum":["global","country","region","market","venue"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"The parent `catalogue.pricing_market`."},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"region":{"type":"string","maxLength":100,"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"baseCurrency":{"type":"string","maxLength":3,"nullable":true,"pattern":"^[A-Z]{3}$"},"sellingCurrency":{"type":"string","maxLength":3,"nullable":true,"pattern":"^[A-Z]{3}$"},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"displayFormat":{"type":"string","maxLength":40,"nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"inheritsFromParent":{"type":"boolean","default":true},"fxReferenceRate":{"type":"number","nullable":true,"description":"Reference only; FX supplies inputs, it never decides a price."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductServicePriceAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Product & Service Price Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"assignmentId":{"type":"string","description":"Assignment ID; empty on create"},"objectType":{"type":"string","enum":["ticketProduct","ticketType","admission","event","performance","membership","annualPass","addOn","fnbItem","retailProduct","rentalItem","resource","reservationService","experience","otherSellableService"],"description":"Supported Commercial Objects (p.13): the kind of sellable object being priced"},"objectIds":{"type":"array","items":{"type":"string"},"description":"The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"},"assignmentScope":{"type":"string","enum":["productLevel","productVariant","ticketType","event","performance","venue"],"description":"Assignment Scope (p.14): the level at which the assignment holds"},"scopeRefId":{"type":"string","nullable":true,"description":"The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"},"priceListId":{"type":"string","description":"The price list assigned"},"categoryRates":{"type":"array","items":{"type":"object","properties":{"priceCategory":{"type":"string"},"rateId":{"type":"string"}}},"description":"Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"}}},
"ProductServicePriceAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product & Service Price Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"assignmentId":{"type":"string","description":"Assignment ID; empty on create"},"objectType":{"type":"string","enum":["ticketProduct","ticketType","admission","event","performance","membership","annualPass","addOn","fnbItem","retailProduct","rentalItem","resource","reservationService","experience","otherSellableService"],"description":"Supported Commercial Objects (p.13): the kind of sellable object being priced"},"objectIds":{"type":"array","items":{"type":"string"},"description":"The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"},"assignmentScope":{"type":"string","enum":["productLevel","productVariant","ticketType","event","performance","venue"],"description":"Assignment Scope (p.14): the level at which the assignment holds"},"scopeRefId":{"type":"string","nullable":true,"description":"The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"},"priceListId":{"type":"string","description":"The price list assigned"},"categoryRates":{"type":"array","items":{"type":"object","properties":{"priceCategory":{"type":"string"},"rateId":{"type":"string"}}},"description":"Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"},"pricingSource":{"type":"string","description":"Price Source Visibility (p.14): the name shown on the product, e.g. UAE Standard Admission 2027; read-only"}}}
}
```
