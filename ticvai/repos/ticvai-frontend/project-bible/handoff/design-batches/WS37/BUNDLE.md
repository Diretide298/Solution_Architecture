# WS37 — Pricing   Revenue Management board 4

**10 screens · 16 operations · 21 schemas · 5 permissions**

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
  `APPROVAL_CONFIGURE, PRICE_CONFIGURE, PRODUCT_APPROVE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-078` | Pricing Governance Command Center | B–D | 4 | 260 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-079` | Pricing Change Request & Workspace | B–D | 17 | 0 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `ADM-080` | Bulk Pricing Update, Import & Mass Maintenance | B–D | 0 | 8 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-081` | Pricing Version & Baseline Management | B–D | 0 | 26 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-082` | Pricing Change Impact Analysis | B–D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-083` | Pricing Approval Workflow & Authority Matrix | B–D | 4 | 20 | 5 | 1 | 1 | 3 | — | notStarted (generated) |
| `ADM-084` | Pricing Publication & Effective-Date Scheduler | B–D | 1 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-085` | Pricing Distribution, Synchronization & Publication Monitor | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-086` | Pricing Rollback & Emergency Control Center | B–D | 22 | 0 | 6 | 1 | 1 | 2 | — | notStarted (generated) |
| `ADM-087` | Pricing History, Audit & Compliance Explorer | B–D | 2 | 0 | 6 | 1 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-081, ADM-082, ADM-085 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-078` Pricing Governance Command Center

**Provide Commercial, Revenue, Finance, and authorized management with one operational view of all pricing changes and governance activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `changeId` (navigation) |
| Route | `/commercial/pricing-governance-command-center-adm-078` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Create Pricing Change, Bulk Update, Import Changes, Review Impact, Approve, Schedule Publication, View …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every pricing change and governance activity in one place: change requests by state, waiting approvals, scheduled publications, rollbacks; approvers decide here.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Create Pricing Change, Bulk Update, Import Changes, Review Impact, Approve, Schedule Publication, View Rollbacks. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search pricing governance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by price list, product, venue, market, channel, legal entity and 6 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Price list | text field | — | — | `listPricingGovernance` ?priceList |
| Product | text field | — | — | `listPricingGovernance` ?product |
| Venue | text field | — | — | `listPricingGovernance` ?venue |
| Market | text field | — | — | `listPricingGovernance` ?market |
| Channel | text field | — | — | `listPricingGovernance` ?channel |
| Legal entity | text field | — | — | `listPricingGovernance` ?legalEntity |
| Owner | text field | — | — | `listPricingGovernance` ?owner |
| Change type | select | — | Price change · New rate · Rate removal · Price list change · Eligibility rule change · Tax change · Fee change · Formula change · Currency rounding change · Emergency change | `listPricingGovernance` ?changeType |
| Approver | text field | — | — | `listPricingGovernance` ?approver |
| Risk level | radio group | — | Low · Medium · High · Critical | `listPricingGovernance` ?riskLevel |
| Status | select | — | Draft · Pending validation · Pending approval · Returned for modification · Approved · Scheduled · Published · Publication failed · Rejected · Cancelled · Rolled back | `listPricingGovernance` ?status |
| Effective from | date picker | — | — | `listPricingGovernance` ?effectiveFrom |
| Effective to | date picker | — | — | `listPricingGovernance` ?effectiveTo |

**Sent by *Approve*** (`decidePricingChangeRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject · Return for modification | — | — | `decidePricingChangeRequest` body |
| Comment `comment` | text area | optional | — | max length 2000 | — | Required for reject and returnForModification. | `decidePricingChangeRequest` body |

#### Outputs: what the screen shows and produces

**Shown**

**Pricing Changes in Draft** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Pending Validation** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Pending Approval** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Approved Changes** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Scheduled Publications** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Published today** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Failed Publications** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Emergency Changes** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Rollbacks** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Expiring prices** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Governance exceptions** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**High risk changes** (metric tile, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**Every pricing governance** (data table, from `listPricingGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Change | text | Change request ID |
| Change name | text | Change name, e.g. |
| Change type | chip: Price change, New rate, Rate removal, Price list change, Eligibility rule change … | Change Type (pack p.59) |
| Scope | text | Scope summary, e.g. |
| Revenue impact | AED 1,234.50 | Estimated revenue impact from the impact analysis; empty when not monetary (e.g. |
| Impact note | text | Impact label when not monetary, e.g. |
| Requested by | text | Requested by (user or team) |
| Owner | text | Owner |
| Approver | text | Current approver (role or user) awaited |
| Risk level | chip: Low, Medium, High, Critical | Risk score from the impact analysis (pack p.64) |
| Status | text | Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected … |
| Effective date | 1 Oct 2026, 14:30 | Effective date requested |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Pricing Governance Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Pricing changes in draft | 1,234 | Pricing Changes in Draft |
| Pending validation | 1,234 | Pending Validation |
| Pending approval | 1,234 | Pending Approval |
| Approved changes | 1,234 | Approved Changes |

**The selected pricing governance** (detail panel): The pack groups this record's detail under its own headings: “Change Scope Impact Status”, “VAT Update UAE Finance Scheduled”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Pricing Change (primary button) | navigation or local | — | — | — | — |
| Bulk Update (secondary button) | navigation or local | — | — | — | — |
| Import Changes (secondary button) | navigation or local | — | — | — | — |
| Review Impact (secondary button) | navigation or local | — | — | — | — |
| Approve (secondary button) | `decidePricingChangeRequest` POST `/pricing-change-request/{changeId}/decision` | PricingChangeRequestDecisionInput | PricingChangeRequestWorkspaceView | 403 `selfApproval` (the requester cannot approve their own change) or `outsideAuthority` (the change is above the caller's approval tier).; 404 The resource does not exist, or is outside the caller's scope. This … | — |
| Schedule Publication (secondary button) | navigation or local | — | — | — | — |
| View Rollbacks (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Approve / Reject / Return**: Comment required for reject and return; the decision lands on the change request's approval record so the inbox and this screen agree. *(source: contracts/spine/catalogue.yaml#decidePricingChangeRequest)*

**Data it reads**: `listPricingGovernance` (onLoad, Pricing Governance Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-080` Bulk Pricing Update, Import & Mass Maintenance: *Works in Bulk Pricing Update, Import & Mass Maintenance*; calls `listPricingGovernance`
- → `ADM-081` Pricing Version & Baseline Management: *Works in Pricing Version & Baseline Management*; calls `listPricingGovernance`
- → `ADM-082` Pricing Change Impact Analysis: *Works in Pricing Change Impact Analysis*; calls `listPricingGovernance`
- → `ADM-083` Pricing Approval Workflow & Authority Matrix: *Works in Pricing Approval Workflow & Authority Matrix*; calls `listPricingGovernance`
- → `ADM-084` Pricing Publication & Effective-Date Scheduler: *Works in Pricing Publication & Effective-Date Scheduler*; calls `listPricingGovernance`
- → `ADM-085` Pricing Distribution, Synchronization & Publication Monitor: *Works in Pricing Distribution, Synchronization & Publication Monitor*; calls `listPricingGovernance`
- → `ADM-086` Pricing Rollback & Emergency Control Center: *Works in Pricing Rollback & Emergency Control Center*; calls `listPricingGovernance`
- → `ADM-087` Pricing History, Audit & Compliance Explorer: *Works in Pricing History, Audit & Compliance Explorer*; calls `listPricingGovernance`
- → `ADM-079` Pricing Change Request & Workspace: *Works in Pricing Change Request & Workspace*; carries `changeId`; calls `listPricingGovernance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is not `pendingApproval` (`notPendingApproval`).; 422 `comment` missing on reject or return (`commentRequired`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
- change: Annual price review 2027
  state: pendingApproval
  approver: Finance manager
  impact: +6.2% avg
```

#### Permissions

- `listPricingGovernance` → `PRODUCT_VIEW` (read) · staff
- `decidePricingChangeRequest` → `PRODUCT_APPROVE` (operate) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-078` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-078`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 1: Opens Pricing Governance Command Center → Provide Commercial, Revenue, Finance, and authorized management with one operational view of all pricing changes and governance activities.
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F146 branch at step 1 (expected): when Nothing has been set up on Pricing Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F146 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (260 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-078?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Pricing Change, Bulk Update, Import Changes, Review Impact, Approve, Schedule Publication, View Rollbacks.
- [ ] Every transition is wired: `BO-100`, `ADM-080`, `ADM-081`, `ADM-082`, `ADM-083`, `ADM-084`, `ADM-085`, `ADM-086`, `ADM-087`, `ADM-079`.
- [ ] Every gated control is gated: `PRODUCT_APPROVE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-079` Pricing Change Request & Workspace

**Provide a governed workspace for creating individual or structured pricing changes before modifying production pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_APPROVE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `changeId` (navigation) |
| Route | `/commercial/pricing-change-request-workspace-adm-079` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Price Change, Price List Change, Eligibility Rule Change, Tax Change, Fee Change, Formula Change … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of a pricing change request (setPricingChangeRequest, submitPricingChangeRequest and decidePricingChangeRequest have no get or list).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a pricing change is prepared before production is touched: type, reason, effective and expiry dates, priority, lines, attachments; then submitted for validation and approval.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setPricingChangeRequest, submitPricingChangeRequest, decidePricingChangeRequest and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Price Change, Price List Change, Eligibility Rule Change, Tax Change, Fee Change, Formula Change, Currency/Rounding Change, Emergency Change. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Change ID | select field | — | — | — | — | — | — |
| Change Name | select field | — | — | — | — | — | — |
| Change Type | select field | — | — | — | — | — | — |
| Business Reason | select field | — | — | — | — | — | — |
| Requested By | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |
| Expiry Date | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Supporting Notes | select field | — | — | — | — | — | — |
| Attachments | select field | — | — | — | — | — | — |

**Sent by *Approve, reject or return*** (`decidePricingChangeRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject · Return for modification | — | — | `decidePricingChangeRequest` body |
| Comment `comment` | text area | optional | — | max length 2000 | — | Required for reject and returnForModification. | `decidePricingChangeRequest` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Price Change (primary button) | navigation or local | — | — | — | — |
| Price List Change (secondary button) | navigation or local | — | — | — | — |
| Eligibility Rule Change (secondary button) | navigation or local | — | — | — | — |
| Tax Change (secondary button) | navigation or local | — | — | — | — |
| Fee Change (secondary button) | navigation or local | — | — | — | — |
| Formula Change (secondary button) | navigation or local | — | — | — | — |
| Currency/Rounding Change (secondary button) | navigation or local | — | — | — | — |
| Emergency Change (secondary button) | navigation or local | — | — | — | — |
| Submit (primary button) | `submitPricingChangeRequest` POST `/pricing-change-request/{changeId}/submit` | — | PricingChangeRequestWorkspaceView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The request is not `draft` or `returnedForModification` (`notSubmittable`).; 422 Validation failed (`noLines` … | — |
| Approve, reject or return (secondary button) | `decidePricingChangeRequest` POST `/pricing-change-request/{changeId}/decision` | PricingChangeRequestDecisionInput | PricingChangeRequestWorkspaceView | 403 `selfApproval` (the requester cannot approve their own change) or `outsideAuthority` (the change is above the caller's approval tier).; 404 The resource does not exist, or is outside the caller's scope. This … | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Submit**: Moves a draft to validation; on success to approval; failed checks return it to the author with the reasons. *(source: contracts/spine/catalogue.yaml#submitPricingChangeRequest)*

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; carries `changeId`; calls `setPricingChangeRequest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing change request configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing change request untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing change request configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is not `draft` or `returnedForModification` (`notSubmittable`).; 409 The request is not `pendingApproval` (`notPendingApproval`).; 422 Validation failed (`noLines`, `retroactiveEffectiveDate`, `unknownObject`); the request stays `draft`.; 422 `comment` missing on reject or return (`commentRequired`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
change:
  name: Annual price review 2027
  type: priceChange
  reason: annualPriceReview
  effective: '2027-01-01'
  lines: 214
```

#### Permissions

- `setPricingChangeRequest` → `PRODUCT_CONFIGURE` (configure) · staff
- `submitPricingChangeRequest` → `PRODUCT_CONFIGURE` (configure) · staff
- `decidePricingChangeRequest` → `PRODUCT_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.22 | System shall support pricing approval workflows. | Unified Operations Dashboard | CONTRACTED | `submitPricingChangeRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-079` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-079`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 2: Works in Pricing Change Request & Workspace → Provide a governed workspace for creating individual or structured pricing changes before modifying production pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-079?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Price Change, Price List Change, Eligibility Rule Change, Tax Change, Fee Change, Formula Change, Currency/Rounding Change, Emergency Change, Submit, Approve, reject or return.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_APPROVE`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-080` Bulk Pricing Update, Import & Mass Maintenance

**Allow large pricing portfolios to be updated efficiently without manually editing hundreds or thousands of records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bulk-pricing-update-import-mass-maintenance-adm-080` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 1 operation.** Unserved: Increase by %, Decrease by %, Increase Fixed Amount, Decrease Fixed Amount, Replace Amount, Copy Rate …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Update large portfolios at once: percentage across a category, file import, mass maintenance; every bulk change goes through a change request and version control (AED 100 > 110 > 120 as versions 1.0, 1.1, 1.2).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Increase by %, Decrease by %, Increase Fixed Amount, Decrease Fixed Amount, Replace Amount, Copy Rate, Change Currency, Set Effective Dates …. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Job kind | segmented control | — | Bulk operation · Import | `listBulkPricingUpdate` ?jobKind |
| Operation | select | — | Increase percent · Decrease percent · Increase fixed amount · Decrease fixed amount · Replace amount · Copy rate · Change currency · Apply rounding · Set effective dates · Activate deactivate · Clone for new season | `listBulkPricingUpdate` ?operation |
| Status | select | — | Draft · Validating · Validation failed · Ready to submit · Submitted · Cancelled | `listBulkPricingUpdate` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every bulk pricing update** (data table, from `listBulkPricingUpdate`)

| Shows | Format | Notes |
|---|---|---|
| Records read | 1,234 | Records read (import preview) |
| Valid records | 1,234 | Valid records |
| Warning count | 1,234 | Records with warnings |
| Error count | 1,234 | Records with errors; the job cannot be submitted while above zero |

**The selected bulk pricing update** (detail panel): The pack groups this record's detail under its own headings: “Preview”, “Before committing”, “Export”.

| Shows | Format | Notes |
|---|---|---|
| Records read | 1,234 | Records read (import preview) |
| Valid records | 1,234 | Valid records |
| Warning count | 1,234 | Records with warnings |
| Error count | 1,234 | Records with errors; the job cannot be submitted while above zero |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Increase by % (primary button) | navigation or local | — | — | — | — |
| Decrease by % (secondary button) | navigation or local | — | — | — | — |
| Increase Fixed Amount (secondary button) | navigation or local | — | — | — | — |
| Decrease Fixed Amount (secondary button) | navigation or local | — | — | — | — |
| Replace Amount (secondary button) | navigation or local | — | — | — | — |
| Copy Rate (secondary button) | navigation or local | — | — | — | — |
| Change Currency (secondary button) | navigation or local | — | — | — | — |
| Set Effective Dates (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **bulk jobs**: Job, scope, rows, status, linked change request. *(source: contracts/spine/catalogue.yaml#listBulkPricingUpdate / DI-599)*

**Data it reads**: `listBulkPricingUpdate` (onLoad, Bulk Pricing Update, Import & Mass Maintenance)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `listBulkPricingUpdate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bulk pricing update list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bulk pricing update untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bulk pricing update yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bulk pricing update are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  scope: All F&B items, Harbour Kitchen
  change: +5%
  rows: 128
  status: pendingApproval
```

#### Permissions

- `listBulkPricingUpdate` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-080` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-080`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 4: Works in Bulk Pricing Update, Import & Mass Maintenance → Allow large pricing portfolios to be updated efficiently without manually editing hundreds or thousands of records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-080?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Increase by %, Decrease by %, Increase Fixed Amount, Decrease Fixed Amount, Replace Amount, Copy Rate, Change Currency, Set Effective Dates.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-081` Pricing Version & Baseline Management

**Maintain immutable versions of pricing configuration so TICVAI always knows what configuration existed at a particular time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Compare; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pricing-version-baseline-management-adm-081` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Immutable versions of pricing configuration so it is always known what applied at a time; a baseline to compare and roll back to.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Price list | text field | — | — | `listPricingVersionBaseline` ?priceList |
| Status | select | — | Draft · Candidate · Approved · Scheduled · Active · Superseded · Rolled back · Archived | `listPricingVersionBaseline` ?status |
| Compare to | text field | — | — | `listPricingVersionBaseline` ?compareTo |
| Effective on | date and time picker | — | — | `listPricingVersionBaseline` ?effectiveOn |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing version baseline** (data table, from `listPricingVersionBaseline`)

| Shows | Format | Notes |
|---|---|---|
| Version | text | Version number, e.g. |
| Price list | text | Price list name |
| Created date | 1 Oct 2026, 14:30 | Created date |
| Effective date | 1 Oct 2026, 14:30 | Effective date |
| Created by | text | Created by |
| Change request | text | Change request ID that produced the version |
| Product count | 1,234 | Product Count |
| Change count | 1,234 | Change Count |
| Status | text | Status: draft, candidate, approved, scheduled, active, superseded, rolledBack or archived |
| Added | 1,234 | Rates added compared with the compareTo version (default: the commercial baseline) |
| Removed | 1,234 | Rates removed compared with the compareTo version |
| Modified | 1,234 | Rates modified compared with the compareTo version |
| Unchanged | 1,234 | Rates unchanged compared with the compareTo version |

**The selected pricing version baseline** (detail panel): The pack groups this record's detail under its own headings: “Version States”, “Differen”, “AED AED”, “Senio AED AED”, “Baseline”, “Commercial Baseline”.

| Shows | Format | Notes |
|---|---|---|
| Version | text | Version number, e.g. |
| Price list | text | Price list name |
| Created date | 1 Oct 2026, 14:30 | Created date |
| Effective date | 1 Oct 2026, 14:30 | Effective date |
| Created by | text | Created by |
| Change request | text | Change request ID that produced the version |
| Product count | 1,234 | Product Count |
| Change count | 1,234 | Change Count |
| Status | text | Status: draft, candidate, approved, scheduled, active, superseded, rolledBack or archived |
| Added | 1,234 | Rates added compared with the compareTo version (default: the commercial baseline) |
| Removed | 1,234 | Rates removed compared with the compareTo version |
| Modified | 1,234 | Rates modified compared with the compareTo version |
| Unchanged | 1,234 | Rates unchanged compared with the compareTo version |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **version list**: Version, published, by, effective from, baseline flag; compare two versions. *(source: contracts/spine/catalogue.yaml#listPricingVersionBaseline)*

**Data it reads**: `listPricingVersionBaseline` (onLoad, Pricing Version & Baseline Management)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `listPricingVersionBaseline`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing version baseline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing version baseline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing version baseline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing version baseline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- v: '1.2'
  effective: '2027-01-01'
  baseline: false
- v: '1.1'
  effective: '2026-06-15'
  baseline: true
```

#### Permissions

- `listPricingVersionBaseline` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.25 | System shall maintain pricing history. | Unified Operations Dashboard | CONTRACTED | `listPricingVersionBaseline` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-081` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-081`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 6: Works in Pricing Version & Baseline Management → Maintain immutable versions of pricing configuration so TICVAI always knows what configuration existed at a particular time.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-081?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-082` Pricing Change Impact Analysis

**Determine the commercial and operational consequences of a pricing change before approval and publication. This is one of the most important screens in Board 4.**

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
| Route | `/commercial/pricing-change-impact-analysis-adm-082` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Consequences of a pricing change before approval: revenue, margin, bookings, reservations and promotions affected.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listChangeImpactAnalysis return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Change request | text field | — | — | `listPricingChangeImpact` ?changeRequestId |
| Risk level | radio group | — | Low · Medium · High · Critical | `listPricingChangeImpact` ?riskLevel |
| Change request | picker: choose a change request | — | — | `listChangeImpactAnalysis` ?changeRequestId |
| Product | picker: choose a product | — | — | `listChangeImpactAnalysis` ?productId |
| Area | select | — | Future orders · Reservations · Issued tickets · Capacity · Pricing · Tax · Promotions · Membership · Entitlements · Access control · Sales channels · B2B partners … | `listChangeImpactAnalysis` ?area |
| Min risk | radio group | — | Low · Medium · High · Critical | `listChangeImpactAnalysis` ?minRisk |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing change impact** (data table, from `listPricingChangeImpact`)

| Shows | Format | Notes |
|---|---|---|
| Products | 1,234 | Affected products (count) |
| Events | 1,234 | Affected events (count) |
| Performances | 1,234 | Affected performances (count) |
| Venues | 1,234 | Affected venues (count) |
| Markets | 1,234 | Affected markets (count) |
| Channels | 1,234 | Affected channels (count) |
| B2B partners | 1,234 | Affected b2bPartners (count) |
| Memberships | 1,234 | Affected memberships (count) |
| Packages | 1,234 | Affected packages (count) |
| Existing reservations | 1,234 | Existing reservations affected; normally 0 because changes never reach already-sold tickets (MoM 31 Aug §4.10) |
| Future reservations | 1,234 | Affected futureReservations (count) |
| Apis | 1,234 | Affected apis (count) |
| Integrations | 1,234 | Affected integrations (count) |

**The selected pricing change impact** (detail panel): The pack groups this record's detail under its own headings: “Estimate”, “Proposed change”, “Affected”, “Estimated annual revenue impact”, “Show whether changes affect”, “Existing Booking Protection”.

| Shows | Format | Notes |
|---|---|---|
| Products | 1,234 | Affected products (count) |
| Events | 1,234 | Affected events (count) |
| Performances | 1,234 | Affected performances (count) |
| Venues | 1,234 | Affected venues (count) |
| Markets | 1,234 | Affected markets (count) |
| Channels | 1,234 | Affected channels (count) |
| B2B partners | 1,234 | Affected b2bPartners (count) |
| Memberships | 1,234 | Affected memberships (count) |
| Packages | 1,234 | Affected packages (count) |
| Existing reservations | 1,234 | Existing reservations affected; normally 0 because changes never reach already-sold tickets (MoM 31 Aug §4.10) |
| Future reservations | 1,234 | Affected futureReservations (count) |
| Apis | 1,234 | Affected apis (count) |
| Integrations | 1,234 | Affected integrations (count) |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **impact**: Numbers first (bookings affected, revenue change), then the lists. *(source: contracts/spine/catalogue.yaml#listPricingChangeImpact / contracts/spine/catalogue.yaml#listChangeImpactAnalysis)*

**Data it reads**: `listPricingChangeImpact` (onLoad, Pricing Change Impact Analysis); `listChangeImpactAnalysis` (onLoad, Change Impact Analysis)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `listPricingChangeImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing change impact list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing change impact untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing change impact yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing change impact are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
impact:
  change: Annual price review 2027
  revenue: +AED 1.8m a year
  bookingsAffected: 0
  promotionsAffected: 3
```

#### Permissions

- `listPricingChangeImpact` → `PRODUCT_VIEW` (read) · staff
- `listChangeImpactAnalysis` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-082` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-082`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 8: Works in Pricing Change Impact Analysis → Determine the commercial and operational consequences of a pricing change before approval and publication. This is one of the most important screens in Board 4.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-082?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-083` Pricing Approval Workflow & Authority Matrix

**Configure who must approve pricing changes based on their commercial risk and scope.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `PRODUCT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pricing-approval-workflow-authority-matrix-adm-083` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who must approve a pricing change by risk and scope: tiers of thresholds to approvers, the creator never giving final approval, expected hours, reminders, escalation.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approvePricingWorkflowAuthority and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Expected Approval Time | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Reminder | select field | — | — | — | — | — | — |
| Alternate Approver | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **tiers**: Rows of threshold to approver role; "creator cannot give final approval" on by default. *(source: contracts/spine/catalogue.yaml#approvePricingWorkflowAuthority)*

#### Outputs: what the screen shows and produces

**Shown**

**Authority matrix** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalMatrices` (onLoad, What requires approval, and at which authority level)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `approvePricingWorkflowAuthority`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing approval workflow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing approval workflow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiers:
- 'up to 5%: Revenue manager'
- '5-15%: Commercial director'
- 'over 15%: CFO'
```

#### Permissions

- `approvePricingWorkflowAuthority` → `PRODUCT_CONFIGURE` (configure) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.23 | System shall support multi-level pricing approvals. | Unified Operations Dashboard | CONTRACTED | `approvePricingWorkflowAuthority` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-083` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-083`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 10: Works in Pricing Approval Workflow & Authority Matrix → Configure who must approve pricing changes based on their commercial risk and scope.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-083?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-084` Pricing Publication & Effective-Date Scheduler

**Control exactly when approved pricing becomes commercially effective.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares a publishing operation over fields the pack configures |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pricing-publication-effective-date-scheduler-adm-084` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Scheduled Publication, Staged Publication. Each needs an operation, or needs removing from the screen; this … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of scheduled pricing publications (publishPricingEffectiveDate has no list).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When approved pricing becomes effective: immediately, scheduled, from a future date or staged by market, venue or channel; never retroactive.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only publishPricingEffectiveDate and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Scheduled Publication, Staged Publication. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 1 March 02:00 | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Immediately (primary button) | navigation or local | — | — | — | — |
| Scheduled Publication (secondary button) | navigation or local | — | — | — | — |
| Staged Publication (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `publishPricingEffectiveDate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing publication effective-date configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing publication effective-date untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing publication effective-date configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-443`: Same scheduler and pre-publication checks.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
schedule:
  version: '1.2'
  mode: staged
  stages:
  - Dune Park 1 Jan
  - Coastal Aqua 15 Jan
```

#### Permissions

- `publishPricingEffectiveDate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-084` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-084`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 12: Works in Pricing Publication & Effective-Date Scheduler → Control exactly when approved pricing becomes commercially effective.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-084?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Immediately, Scheduled Publication, Staged Publication, What publishing changes.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-085` Pricing Distribution, Synchronization & Publication Monitor

**Ensure published pricing reaches every TICVAI channel and dependent system consistently.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pricing-distribution-synchronization-publication-monitor-adm-085` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether published pricing reached every channel and dependent system: per channel, version received, when, errors.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Publication version | text field | — | — | `listPricingDistributionSynchronization` ?publicationVersion |
| Target | select | — | B2C · Mobile app · POS · Mobile POS · Kiosk · Call center · B2B · Reseller · Ota · API · Cache cdn · External system | `listPricingDistributionSynchronization` ?target |
| Status | select | — | Pending · Publishing · Synchronized · Warning · Failed · Suspended | `listPricingDistributionSynchronization` ?status |
| Out of sync only | toggle | — | — | `listPricingDistributionSynchronization` ?outOfSyncOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing distribution synchronization** (data table, from `listPricingDistributionSynchronization`)

| Shows | Format | Notes |
|---|---|---|
| Target | chip: B2C, Mobile app, POS, Mobile POS, Kiosk, Call center… | Distribution Target (pack p.68) |
| Publication started | 1 Oct 2026, 14:30 | Publication started |
| Last updated | 1 Oct 2026, 14:30 | Last updated |
| Records published | 1,234 | Records published |
| Records failed | 1,234 | Records failed |
| Latency | 1,234.5 | Latency in seconds from publication start to confirmation |
| Target version | text | Pricing version the target currently serves |

**The selected pricing distribution synchronization** (detail panel): The pack groups this record's detail under its own headings: “For each target”, “For failed publication”, “Consistency Check”, “Alerts”.

| Shows | Format | Notes |
|---|---|---|
| Target | chip: B2C, Mobile app, POS, Mobile POS, Kiosk, Call center… | Distribution Target (pack p.68) |
| Publication started | 1 Oct 2026, 14:30 | Publication started |
| Last updated | 1 Oct 2026, 14:30 | Last updated |
| Records published | 1,234 | Records published |
| Records failed | 1,234 | Records failed |
| Latency | 1,234.5 | Latency in seconds from publication start to confirmation |
| Target version | text | Pricing version the target currently serves |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **distribution matrix**: Systems as rows, versions and status as cells; tills show the catalogue release that carries the prices. *(source: contracts/spine/catalogue.yaml#listPricingDistributionSynchronization / contracts/spine/catalogue.yaml#publishBundle)*

**Data it reads**: `listPricingDistributionSynchronization` (onLoad, Pricing Distribution, Synchronization & Publication Monitor)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `listPricingDistributionSynchronization`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing distribution synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing distribution synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing distribution synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing distribution synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  channel: Point of sale
  version: '1.2'
  status: 38 of 41 tills
```

#### Permissions

- `listPricingDistributionSynchronization` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-085` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-085`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 14: Works in Pricing Distribution, Synchronization & Publication Monitor → Ensure published pricing reaches every TICVAI channel and dependent system consistently.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-085?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-086` Pricing Rollback & Emergency Control Center

**Provide controlled recovery when a pricing publication is incorrect or creates unacceptable commercial impact.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation) |
| Route | `/commercial/pricing-rollback-emergency-control-center-adm-086` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 9 actions on this screen; 8 are served since the writers pass (29 September): Previous Version, Selected Version, Previous Price, Commercial Baseline, Selected Products, Selected … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recovery when published pricing is wrong: roll back to a version, freeze a list, product or venue pricing, stop a scheduled publication or distribution, restore last known good. Recorded first, approved where required.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action type | select | — | Rollback · Freeze price list · Freeze product pricing · Freeze venue pricing · Stop scheduled publication · Stop distribution · Restore last known good | `listPricingRollbackEmergency` ?actionType |
| Status | select | — | Previewed · Executed · Awaiting retrospective approval · Approved · Failed · Released | `listPricingRollbackEmergency` ?status |
| From | date picker | — | — | `listPricingRollbackEmergency` ?from |
| To | date picker | — | — | `listPricingRollbackEmergency` ?to |

**Form: Request pricing rollback** (modal, opened by *Request pricing rollback*; *Request pricing rollback* calls `requestPricingRollback`, *Cancel* sends nothing)

**Collects what `requestPricingRollback` sends before it is called.** Required: `subject`, `actionType`, `reason`, `status`. Optional: `productId`, `priceListId`, `fromVersion`, `toVersion`, `productScope`, `rollbackTarget`, `rollbackScope`, `scopeIds`, `dependencies`, `executionMode`, `isEmergency`, `scheduledAt` and 6 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `requestedAt`, `requestedByPrincipalId`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subject` | segmented control | required | — | Product · Pricing | — | — | `requestPricingRollback` body |
| Action type `actionType` | select | required | — | Rollback · Freeze price list · Freeze product pricing · Freeze venue pricing · Stop scheduled publication · Stop distribution · Restore last known good | — | Product rollbacks are `rollback`. | `requestPricingRollback` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `requestPricingRollback` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `requestPricingRollback` body |
| From version `fromVersion` | number field | optional | — | — | — | — | `requestPricingRollback` body |
| To version `toVersion` | number field | optional | — | — | — | — | `requestPricingRollback` body |
| Product scope `productScope` | multi-select chips | optional | — | Entire product · Pricing association · Channel association · Validity configuration · Media · Policy · Entitlement configuration | — | Product rollbacks: which parts are restored. | `requestPricingRollback` body |
| Rollback target `rollbackTarget` | radio group | optional | — | Previous version · Selected version · Previous price · Commercial baseline | — | — | `requestPricingRollback` body |
| Rollback scope `rollbackScope` | radio group | optional | — | Selected products · Selected venue · Selected market · Selected channel · Entire publication | — | — | `requestPricingRollback` body |
| Scopes `scopeIds` | multi-picker: choose scopes | optional | — | — | — | — | `requestPricingRollback` body |
| Dependencies `dependencies` | list of values (chips) | optional | — | — | — | Product rollbacks: the dependent objects reviewed before executing. | `requestPricingRollback` body |
| Reason `reason` | text area | required | — | — | — | — | `requestPricingRollback` body |
| Execution mode `executionMode` | segmented control | optional | Immediate | Immediate · Scheduled | — | — | `requestPricingRollback` body |
| Is emergency `isEmergency` | toggle | optional | off | — | — | — | `requestPricingRollback` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `requestPricingRollback` body |
| Incident reference `incidentReference` | text field | optional | — | max length 200 | — | — | `requestPricingRollback` body |
| Authorised role `authorisedRole` | text field | optional | — | max length 100 | — | — | `requestPricingRollback` body |
| Retrospective approval required `retrospectiveApprovalRequired` | toggle | optional | off | — | — | — | `requestPricingRollback` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | — | `requestPricingRollback` body |
| Change request `changeRequestId` | picker: choose a change request | optional | — | — | shows names, sends the id | The change request whose publication is being rolled back. | `requestPricingRollback` body |
| Status `status` | select | required | Requested | Requested · Scheduled · Executing · Completed · Failed · Cancelled | — | — | `requestPricingRollback` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `rollbackTargetRequired`, `scheduledAtInPast` or `incidentReferenceRequired`.

**Sent by *Cancel pricing rollback*** (`cancelPricingRollback`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 500 | — | — | `cancelPricingRollback` body |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Freeze Price List, Freeze Product Pricing, Freeze Venue Pricing, Stop Scheduled Publication, Stop Distribution, Restore Last Known Good Version. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Previous Version (primary button) | navigation or local | — | — | — | — |
| Selected Version (secondary button) | navigation or local | — | — | — | — |
| Previous Price (secondary button) | navigation or local | — | — | — | — |
| Commercial Baseline (secondary button) | navigation or local | — | — | — | — |
| Selected Products (secondary button) | navigation or local | — | — | — | — |
| Selected Venue (secondary button) | navigation or local | — | — | — | — |
| Selected Market (secondary button) | navigation or local | — | — | — | — |
| Selected Channel (secondary button) | navigation or local | — | — | — | — |
| Request pricing rollback (secondary button) | `requestPricingRollback` POST `/pricing-rollback-emergency` | CatalogueRollbackAction | CatalogueRollbackAction | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `rollbackTargetRequired`, `scheduledAtInPast` or `incidentReferenceRequired`. | gated `PRICE_CONFIGURE`; opens modal first |
| Cancel pricing rollback (destructive button) | `cancelPricingRollback` POST `/pricing-rollback-emergency/{actionId}/cancel` | inline | CatalogueRollbackAction | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyExecuting` or `alreadyFinished`. | gated `PRICE_CONFIGURE` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Request rollback or emergency action**: Action type, scope and target version; creates the action, raises an approval where required, and shows its state. *(source: contracts/spine/catalogue.yaml#requestPricingRollback)*
- **Cancel**: Only before it runs; one executing cannot be cancelled. *(source: contracts/spine/catalogue.yaml#cancelPricingRollback)*

**Data it reads**: `listPricingRollbackEmergency` (onLoad, Pricing Rollback & Emergency Control Center)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Returns to the board's landing screen*; calls `listPricingRollbackEmergency`

**What opens over it**

- confirmDialog *Cancel pricing rollback*: **Names what `cancelPricingRollback` changes and what it leaves alone**, in the consequence rather than the verb. A catalogue rollback action this affects should be identified in the dialog, not just counted. **Collects what `cancelPricingRollback` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing rollback emergency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing rollback emergency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing rollback emergency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing rollback emergency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyExecuting` or `alreadyFinished`.; 422 `rollbackTargetRequired`, `scheduledAtInPast` or `incidentReferenceRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action:
  type: rollback
  scope: Dune Park, Website
  from: '1.2'
  to: '1.1'
  reason: Child price published at adult rate
```

#### Permissions

- `listPricingRollbackEmergency` → `PRODUCT_VIEW` (read) · staff
- `requestPricingRollback` → `PRICE_CONFIGURE` (configure) · staff
- `cancelPricingRollback` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.26 | System shall support rollback of pricing changes. | Unified Operations Dashboard | CONTRACTED | `requestPricingRollback` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-086` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-086`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 16: Works in Pricing Rollback & Emergency Control Center → Provide controlled recovery when a pricing publication is incorrect or creates unacceptable commercial impact.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-086?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Previous Version, Selected Version, Previous Price, Commercial Baseline, Selected Products, Selected Venue, Selected Market, Selected Channel, Request pricing rollback, Cancel pricing rollback.
- [ ] Every transition is wired: `ADM-078`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-087` Pricing History, Audit & Compliance Explorer

**Provide complete forensic traceability for every pricing configuration and change. Enable TICVAI revenue administrators to configure dynamic-pricing strategies using real-time commercial conditions such as: Demand + Occupancy + Availability + Inventory + Booking Velocity + Time-to- Event + Season + Day + Timeslot + Channel + Customer Segment + Location The engine converts those conditions into controlled price movements while always respecting commercial guardrails.**

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
| Route | `/commercial/pricing-history-audit-compliance-explorer-adm-087` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Board 5 — Dynamic Pricing, Revenue. Each needs an operation, or needs removing from the screen; this is the … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Forensic history of every pricing configuration and change: who, what, when, before and after, approval.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Board 5 — Dynamic Pricing, Revenue. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search pricing history audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by price list, rate, product, user, change request, version and 6 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Price list | text field | — | — | `listPricingCompliance` ?priceList |
| Rate | number field | — | — | `listPricingCompliance` ?rate |
| Product | text field | — | — | `listPricingCompliance` ?product |
| User | text field | — | — | `listPricingCompliance` ?user |
| Change request | text field | — | — | `listPricingCompliance` ?changeRequest |
| Version | text field | — | — | `listPricingCompliance` ?version |
| Venue | text field | — | — | `listPricingCompliance` ?venue |
| Market | text field | — | — | `listPricingCompliance` ?market |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPricingCompliance` ?channel |
| Date from | date picker | — | — | `listPricingCompliance` ?dateFrom |
| Date to | date picker | — | — | `listPricingCompliance` ?dateTo |
| Transaction | text field | — | — | `listPricingCompliance` ?transaction |
| Approval | text field | — | — | `listPricingCompliance` ?approval |
| Audit type | select | — | Configuration · Approval · Publication · Synchronization · Override · Rollback · Emergency action | `listPricingCompliance` ?auditType |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** “Who approved the Dubai summer pricing?”. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Board 5 — Dynamic Pricing, Revenue (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **audit explorer**: Filter by object, user, date; before and after side by side. *(source: contracts/spine/catalogue.yaml#listPricingCompliance / DI-599)*

**Data it reads**: `listPricingCompliance` (onLoad, Pricing History, Audit & Compliance Explorer)

**Where the user goes next**

- → `ADM-078` Pricing Governance Command Center: *Pricing Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing history audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing history audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing history audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing history audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  object: Day Pass Adult, B2C
  from: AED 295.00
  to: AED 310.00
  by: Revenue manager
  approved: CFO, 2026-11-28
```

#### Permissions

- `listPricingCompliance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.24 | System shall maintain pricing audit logs. | Unified Operations Dashboard | CONTRACTED | `listPricingCompliance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-087` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-087`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 4
- Flow F146 *Pricing Revenue Management board 4: Pricing Governance Command Center*, step 18: Works in Pricing History, Audit & Compliance Explorer → Provide complete forensic traceability for every pricing configuration and change. Enable TICVAI revenue administrators to configure dynamic-pricing strategies using real-time commercial conditions …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-087?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Board 5 — Dynamic Pricing, Revenue.
- [ ] Every transition is wired: `ADM-078`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approvePricingWorkflowAuthority": {"method":"PUT","path":"/pricing-workflow-authority","contract":"catalogue","summary":"Pricing Approval Workflow & Authority Matrix","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingApprovalWorkflowAuthorityMatrixInput","responds":"PricingApprovalWorkflowAuthorityMatrixView"},
"cancelPricingRollback": {"method":"POST","path":"/pricing-rollback-emergency/{actionId}/cancel","contract":"catalogue","summary":"Cancel a rollback that has not started","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CatalogueRollbackAction"},
"decidePricingChangeRequest": {"method":"POST","path":"/pricing-change-request/{changeId}/decision","contract":"catalogue","summary":"Approve, reject or return a pricing change request","permission":"PRODUCT_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingChangeRequestDecisionInput","responds":"PricingChangeRequestWorkspaceView"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listBulkPricingUpdate": {"method":"GET","path":"/bulk-pricing-update","contract":"catalogue","summary":"Bulk Pricing Update, Import & Mass Maintenance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"jobKind","in":"query","required":false},{"name":"operation","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChangeImpactAnalysis": {"method":"GET","path":"/change-impact-analysi","contract":"catalogue","summary":"Change Impact Analysis","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"changeRequestId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"area","in":"query","required":false},{"name":"minRisk","in":"query","required":false}],"requestBody":null,"responds":"ChangeImpactAnalysisView"},
"listPricingChangeImpact": {"method":"GET","path":"/pricing-change-impact","contract":"catalogue","summary":"Pricing Change Impact Analysis","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"changeRequestId","in":"query","required":false},{"name":"riskLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingCompliance": {"method":"GET","path":"/pricing-compliance","contract":"catalogue","summary":"Pricing History, Audit & Compliance Explorer","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"priceList","in":"query","required":false},{"name":"rate","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"user","in":"query","required":false},{"name":"changeRequest","in":"query","required":false},{"name":"version","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"transaction","in":"query","required":false},{"name":"approval","in":"query","required":false},{"name":"auditType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingDistributionSynchronization": {"method":"GET","path":"/pricing-distribution-synchronization","contract":"catalogue","summary":"Pricing Distribution, Synchronization & Publication Monitor","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"publicationVersion","in":"query","required":false},{"name":"target","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"outOfSyncOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingGovernance": {"method":"GET","path":"/pricing-governance","contract":"catalogue","summary":"Pricing Governance Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"priceList","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"legalEntity","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"changeType","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"riskLevel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"effectiveFrom","in":"query","required":false},{"name":"effectiveTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingRollbackEmergency": {"method":"GET","path":"/pricing-rollback-emergency","contract":"catalogue","summary":"Pricing Rollback & Emergency Control Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"actionType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingVersionBaseline": {"method":"GET","path":"/pricing-version-baseline","contract":"catalogue","summary":"Pricing Version & Baseline Management","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"priceList","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"compareTo","in":"query","required":false},{"name":"effectiveOn","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishPricingEffectiveDate": {"method":"PUT","path":"/pricing-effective-date","contract":"catalogue","summary":"Pricing Publication & Effective-Date Scheduler","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingPublicationEffectiveDateSchedulerInput","responds":"PricingPublicationEffectiveDateSchedulerView"},
"requestPricingRollback": {"method":"POST","path":"/pricing-rollback-emergency","contract":"catalogue","summary":"Roll pricing back, or take an emergency pricing action","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueRollbackAction","responds":"CatalogueRollbackAction"},
"setPricingChangeRequest": {"method":"PUT","path":"/pricing-change-request","contract":"catalogue","summary":"Pricing Change Request & Workspace","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingChangeRequestWorkspaceInput","responds":"PricingChangeRequestWorkspaceView"},
"submitPricingChangeRequest": {"method":"POST","path":"/pricing-change-request/{changeId}/submit","contract":"catalogue","summary":"Submit a draft pricing change for validation and approval","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PricingChangeRequestWorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"BulkPricingUpdateImportMassMaintenanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Bulk Pricing Update, Import & Mass Maintenance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"selectBy":{"type":"string","enum":["priceList","product","productFamily","category","venue","market","currency","rateType","channel","effectivePeriod"],"description":"Vocabulary listed under Select by."},"recordsRead":{"type":"integer","description":"Records read (import preview)","nullable":true},"validRecords":{"type":"integer","description":"Valid records","nullable":true},"warningCount":{"type":"integer","description":"Records with warnings","nullable":true},"errorCount":{"type":"integer","description":"Records with errors; the job cannot be submitted while above zero","nullable":true},"jobId":{"type":"string","description":"Bulk job ID"},"jobKind":{"type":"string","enum":["bulkOperation","import"],"description":"Bulk operation on selected records, or spreadsheet import (CSV/XLSX)"},"selectionValues":{"type":"array","items":{"type":"string"},"description":"IDs selected under selectBy (e.g. the price lists or products)"},"effectivePeriodFrom":{"type":"string","format":"date","description":"Selection: effective period from","nullable":true},"effectivePeriodTo":{"type":"string","format":"date","description":"Selection: effective period to","nullable":true},"recordsSelected":{"type":"integer","description":"Records selected, e.g. 428 admission rates"},"operation":{"type":"string","enum":["increasePercent","decreasePercent","increaseFixedAmount","decreaseFixedAmount","replaceAmount","copyRate","changeCurrency","applyRounding","setEffectiveDates","activateDeactivate","cloneForNewSeason"],"description":"Bulk Operation (pack p.60)","nullable":true},"adjustmentPercent":{"type":"number","description":"Percent for increasePercent / decreasePercent","nullable":true},"adjustmentAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Amount for fixed-amount and replace operations","nullable":true},"targetCurrency":{"type":"string","description":"ISO 4217 currency for changeCurrency","nullable":true},"currentPortfolioValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Preview: current portfolio value","nullable":true},"proposedPortfolioValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Preview: proposed portfolio value","nullable":true},"fileName":{"type":"string","description":"Imported file name","nullable":true},"columnMappings":{"type":"array","items":{"type":"object","properties":{"sourceColumn":{"type":"string","description":"Column in the file"},"targetField":{"type":"string","description":"TICVAI field, e.g. rateAmount"},"suggestedByAi":{"type":"boolean","description":"Suggested by AI mapping"},"confirmed":{"type":"boolean","description":"Confirmed by the administrator; unconfirmed mappings block validation"}},"description":"Column mapping"},"description":"Import column mappings"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["invalidProduct","unknownRateCode","duplicateRecord","unsupportedCurrency","missingMandatoryField","invalidDate","invalidAmount"],"description":"Import Validation check (pack p.61)"},"rowNumber":{"type":"integer","description":"File row","nullable":true},"severity":{"type":"string","enum":["warning","error"],"description":"Errors block submission"},"message":{"type":"string","description":"Message"}},"description":"One issue"},"description":"Validation issues found before commit"},"changeRequestId":{"type":"string","description":"Change request the job was submitted as","nullable":true},"status":{"type":"string","description":"Status: draft, validating, validationFailed, readyToSubmit, submitted or cancelled"},"createdBy":{"type":"string","description":"Created by"},"createdAt":{"type":"string","format":"date-time","description":"Created at"}}},
"CatalogueRollbackAction": {"type":"object","x-ticvai-persistence":"catalogue.rollback_action","description":"**A rollback or emergency action on a product or on pricing** (29 September, data model DM3). Merges product rollback (ADM-133) and the pricing rollback and emergency centre (ADM-086). A rollback restores an earlier `catalogue.product_version` or `catalogue.price_list_version` as a new version; nothing is edited in place. Emergency actions may run before approval and then need `retrospectiveApprovalRequired`.","required":["id","scopePath","subject","actionType","reason","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"subject":{"type":"string","enum":["product","pricing"]},"actionType":{"type":"string","enum":["rollback","freezePriceList","freezeProductPricing","freezeVenuePricing","stopScheduledPublication","stopDistribution","restoreLastKnownGood"],"description":"Product rollbacks are `rollback`."},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"fromVersion":{"type":"integer","nullable":true},"toVersion":{"type":"integer","nullable":true},"productScope":{"type":"array","items":{"type":"string","enum":["entireProduct","pricingAssociation","channelAssociation","validityConfiguration","media","policy","entitlementConfiguration"]},"description":"Product rollbacks: which parts are restored."},"rollbackTarget":{"type":"string","enum":["previousVersion","selectedVersion","previousPrice","commercialBaseline",null],"nullable":true},"rollbackScope":{"type":"string","enum":["selectedProducts","selectedVenue","selectedMarket","selectedChannel","entirePublication",null],"nullable":true},"scopeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"dependencies":{"type":"array","items":{"type":"string"},"description":"Product rollbacks: the dependent objects reviewed before executing."},"reason":{"type":"string"},"executionMode":{"type":"string","enum":["immediate","scheduled"],"default":"immediate"},"isEmergency":{"type":"boolean","default":false},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"incidentReference":{"type":"string","maxLength":200,"nullable":true},"authorisedRole":{"type":"string","maxLength":100,"nullable":true},"retrospectiveApprovalRequired":{"type":"boolean","default":false},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"changeRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The change request whose publication is being rolled back."},"status":{"type":"string","enum":["requested","scheduled","executing","completed","failed","cancelled"],"default":"requested"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ChangeImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"area":{"type":"string","enum":["futureOrders","reservations","issuedTickets","capacity","pricing","tax","promotions","membership","entitlements","accessControl","salesChannels","b2bPartners","otas","pos","b2c","kiosk","media","finance","reporting"],"description":"Impact area (pack p.21-22)"},"changeRequestId":{"type":"string","description":"Change request analysed","format":"uuid"},"affectedCount":{"type":"integer","description":"How many items in this area are affected (orders, reservations, agreements, channels...)"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk classification"},"explanation":{"type":"string","description":"AI explanation in business language; advisory","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PricingApprovalWorkflowAuthorityMatrixInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Pricing Approval Workflow & Authority Matrix submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Every approval action records* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"venue":{"type":"string","description":"Scope: venue; empty for all","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"legalEntity":{"type":"string","description":"Scope: legal entity; empty for all","nullable":true},"policyId":{"type":"string","description":"Authority policy ID; empty on create","nullable":true},"policyName":{"type":"string","description":"Policy name"},"tiers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["changePercent","monetaryImpact","revenueImpact","priceList","product","venue","market","legalEntity","channel","taxChange","feeChange","emergencyStatus"],"description":"Approval Rules dimension (pack pp.64-65)"},"minValue":{"type":"number","description":"Lower bound (exclusive) for numeric dimensions, e.g. 5 for >5%","nullable":true},"maxValue":{"type":"number","description":"Upper bound (inclusive), e.g. 10 for up to 10%","nullable":true},"matchValue":{"type":"string","description":"Matching value for non-numeric dimensions (a price list, venue, channel...); taxChange/feeChange/emergencyStatus match true","nullable":true},"approvalLevels":{"type":"array","items":{"type":"object","properties":{"sequence":{"type":"integer","description":"Order in the multi-level workflow, 1 first"},"approverRole":{"type":"string","description":"Role that must approve, e.g. Pricing Manager, Commercial Director, Finance"},"approverUserId":{"type":"string","description":"Named approver instead of the role","nullable":true}},"description":"One approval step"},"description":"Approvers in sequence"}},"description":"One row of the authority matrix"},"description":"Authority matrix: the first matching row applies; when several dimensions match, all their approval levels are required (decided 29 September, readiness close-out)"},"creatorCannotGiveFinalApproval":{"type":"boolean","description":"Segregation of duties: the user who created a change cannot give final approval; defaults to true (decided 29 September, readiness close-out)"},"expectedApprovalHours":{"type":"integer","description":"Approval SLA: expected approval time in hours; defaults to 48 (decided 29 September, readiness close-out)"},"reminderAfterHours":{"type":"integer","description":"Reminder sent to the pending approver after this many hours; defaults to 24 (decided 29 September, readiness close-out)"},"escalateAfterHours":{"type":"integer","description":"Escalation after this many hours; defaults to 72 (decided 29 September, readiness close-out)"},"escalateToRole":{"type":"string","description":"Role escalated to","nullable":true},"alternateApproverRole":{"type":"string","description":"Alternate approver role when the approver is unavailable or delegates","nullable":true}},"x-ticvai-record-definition":"Every approval action records"},
"PricingApprovalWorkflowAuthorityMatrixView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Approval Workflow & Authority Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Scope: venue; empty for all","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"legalEntity":{"type":"string","description":"Scope: legal entity; empty for all","nullable":true},"policyId":{"type":"string","description":"Authority policy ID; empty on create","nullable":true},"policyName":{"type":"string","description":"Policy name"},"tiers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["changePercent","monetaryImpact","revenueImpact","priceList","product","venue","market","legalEntity","channel","taxChange","feeChange","emergencyStatus"],"description":"Approval Rules dimension (pack pp.64-65)"},"minValue":{"type":"number","description":"Lower bound (exclusive) for numeric dimensions, e.g. 5 for >5%","nullable":true},"maxValue":{"type":"number","description":"Upper bound (inclusive), e.g. 10 for up to 10%","nullable":true},"matchValue":{"type":"string","description":"Matching value for non-numeric dimensions (a price list, venue, channel...); taxChange/feeChange/emergencyStatus match true","nullable":true},"approvalLevels":{"type":"array","items":{"type":"object","properties":{"sequence":{"type":"integer","description":"Order in the multi-level workflow, 1 first"},"approverRole":{"type":"string","description":"Role that must approve, e.g. Pricing Manager, Commercial Director, Finance"},"approverUserId":{"type":"string","description":"Named approver instead of the role","nullable":true}},"description":"One approval step"},"description":"Approvers in sequence"}},"description":"One row of the authority matrix"},"description":"Authority matrix: the first matching row applies; when several dimensions match, all their approval levels are required (decided 29 September, readiness close-out)"},"creatorCannotGiveFinalApproval":{"type":"boolean","description":"Segregation of duties: the user who created a change cannot give final approval; defaults to true (decided 29 September, readiness close-out)"},"expectedApprovalHours":{"type":"integer","description":"Approval SLA: expected approval time in hours; defaults to 48 (decided 29 September, readiness close-out)"},"reminderAfterHours":{"type":"integer","description":"Reminder sent to the pending approver after this many hours; defaults to 24 (decided 29 September, readiness close-out)"},"escalateAfterHours":{"type":"integer","description":"Escalation after this many hours; defaults to 72 (decided 29 September, readiness close-out)"},"escalateToRole":{"type":"string","description":"Role escalated to","nullable":true},"alternateApproverRole":{"type":"string","description":"Alternate approver role when the approver is unavailable or delegates","nullable":true}}},
"PricingChangeImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"products":{"type":"integer","description":"Affected products (count)"},"events":{"type":"integer","description":"Affected events (count)"},"performances":{"type":"integer","description":"Affected performances (count)"},"venues":{"type":"integer","description":"Affected venues (count)"},"markets":{"type":"integer","description":"Affected markets (count)"},"channels":{"type":"integer","description":"Affected channels (count)"},"b2bPartners":{"type":"integer","description":"Affected b2bPartners (count)"},"memberships":{"type":"integer","description":"Affected memberships (count)"},"packages":{"type":"integer","description":"Affected packages (count)"},"existingReservations":{"type":"integer","description":"Existing reservations affected; normally 0 because changes never reach already-sold tickets (MoM 31 Aug §4.10)"},"futureReservations":{"type":"integer","description":"Affected futureReservations (count)"},"apis":{"type":"integer","description":"Affected apis (count)"},"integrations":{"type":"integer","description":"Affected integrations (count)"},"currentRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Revenue"},"projectedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Projected Revenue"},"averagePriceChange":{"type":"number","description":"Average price change in percent"},"maximumChange":{"type":"number","description":"Largest single price change in percent"},"minimumChange":{"type":"number","description":"Smallest single price change in percent"},"marginImpact":{"type":"number","description":"Margin impact in percentage points"},"customerExposure":{"type":"integer","description":"Customers or tickets exposed per year at current volumes (decided 29 September, readiness close-out)"},"transactionVolume":{"type":"integer","description":"Transactions per year affected at current volumes (decided 29 September, readiness close-out)"},"derivedRates":{"type":"integer","description":"Dependency impact: derivedRates affected (count)"},"contractRates":{"type":"integer","description":"Dependency impact: contractRates affected (count)"},"membershipRates":{"type":"integer","description":"Dependency impact: membershipRates affected (count)"},"groupRates":{"type":"integer","description":"Dependency impact: groupRates affected (count)"},"promotions":{"type":"integer","description":"Dependency impact: promotions affected (count)"},"dynamicPricingGuardrails":{"type":"integer","description":"Dependency impact: dynamicPricingGuardrails affected (count)"},"changeRequestId":{"type":"string","description":"Change request analysed"},"changeName":{"type":"string","description":"Change name"},"analysedAt":{"type":"string","format":"date-time","description":"When the analysis was computed"},"revenueImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Projected minus current revenue (annualised)"},"affectsExistingOrders":{"type":"boolean","description":"Whether the change affects existing orders; always false for price changes (never retroactive)"},"affectsExistingReservations":{"type":"boolean","description":"Whether the change affects existing reservations"},"affectsFutureUnsoldInventory":{"type":"boolean","description":"Whether the change affects future unsold inventory"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk score, classified by the tenant's configurable criteria"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI summary lines for this record: advisory only, never approves, publishes or changes a price"}}},
"PricingChangeRequestDecisionInput": {"type":"object","x-ticvai-persistence":"none — request only; the decision is recorded on the approvals request","description":"What `decidePricingChangeRequest` takes (decided 29 September, readiness close-out).","required":["decision"],"properties":{"decision":{"type":"string","enum":["approve","reject","returnForModification"]},"comment":{"type":"string","maxLength":2000,"description":"Required for reject and returnForModification."}}},
"PricingChangeRequestWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.entitlement_template at 3%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Pricing Change Request & Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"changeId":{"type":"string","description":"Change ID; empty on create (the server assigns it), set to update a draft","nullable":true},"changeName":{"type":"string","description":"Change Name"},"changeType":{"type":"string","enum":["priceChange","newRate","rateRemoval","priceListChange","eligibilityRuleChange","taxChange","feeChange","formulaChange","currencyRoundingChange","emergencyChange"],"description":"Change Type (pack p.59)"},"businessReason":{"type":"string","description":"Business reason in the requester's words"},"owner":{"type":"string","description":"Owner"},"businessUnit":{"type":"string","description":"Business unit","nullable":true},"legalEntity":{"type":"string","description":"Legal entity","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"venue":{"type":"string","description":"Venue","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Effective date and time requested; must be in the future, never retroactive (MoM 31 Aug §4.10)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry date and time; empty for open-ended","nullable":true},"priority":{"type":"string","enum":["low","normal","high","urgent"],"description":"Priority; defaults to normal (decided 29 September, readiness close-out)"},"supportingNotes":{"type":"string","description":"Supporting notes","nullable":true},"attachments":{"type":"array","items":{"type":"string"},"description":"Attachment document IDs"},"reasonCode":{"type":"string","enum":["annualPriceReview","newSeason","commercialStrategy","contractUpdate","regulatoryChange","costIncrease","marketAdjustment","correction","emergency"],"description":"Vocabulary listed under Standard reasons."},"lines":{"type":"array","items":{"type":"object","properties":{"objectType":{"type":"string","enum":["product","rate","priceList","eligibilityRule","tax","fee","formula","currencyRounding"],"description":"What this line changes"},"objectId":{"type":"string","description":"ID of the product, rate, price list, rule, tax, fee or formula"},"venue":{"type":"string","description":"Venue the line applies to; empty for all in scope","nullable":true},"market":{"type":"string","description":"Market the line applies to; empty for all in scope","nullable":true},"proposedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Proposed amount for a monetary line; empty for removals and non-monetary changes","nullable":true},"proposedValue":{"type":"string","description":"Proposed value for a non-monetary line (rule, formula, rounding), as the target screen's own format","nullable":true},"remove":{"type":"boolean","description":"True when the line removes the rate or object (Rate Removal)"}},"description":"One changed object"},"description":"Change lines: one request may cover many products, rates, venues and markets"}}},
"PricingChangeRequestWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Change Request & Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"changeId":{"type":"string","description":"Change ID; empty on create (the server assigns it), set to update a draft","nullable":true},"changeName":{"type":"string","description":"Change Name"},"changeType":{"type":"string","enum":["priceChange","newRate","rateRemoval","priceListChange","eligibilityRuleChange","taxChange","feeChange","formulaChange","currencyRoundingChange","emergencyChange"],"description":"Change Type (pack p.59)"},"businessReason":{"type":"string","description":"Business reason in the requester's words"},"requestedBy":{"type":"string","description":"Requested by: the user who created the request (server-set)"},"owner":{"type":"string","description":"Owner"},"businessUnit":{"type":"string","description":"Business unit","nullable":true},"legalEntity":{"type":"string","description":"Legal entity","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"venue":{"type":"string","description":"Venue","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Effective date and time requested; must be in the future, never retroactive (MoM 31 Aug §4.10)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry date and time; empty for open-ended","nullable":true},"priority":{"type":"string","enum":["low","normal","high","urgent"],"description":"Priority; defaults to normal (decided 29 September, readiness close-out)"},"supportingNotes":{"type":"string","description":"Supporting notes","nullable":true},"attachments":{"type":"array","items":{"type":"string"},"description":"Attachment document IDs"},"reasonCode":{"type":"string","enum":["annualPriceReview","newSeason","commercialStrategy","contractUpdate","regulatoryChange","costIncrease","marketAdjustment","correction","emergency"],"description":"Vocabulary listed under Standard reasons."},"lines":{"type":"array","items":{"type":"object","properties":{"objectType":{"type":"string","enum":["product","rate","priceList","eligibilityRule","tax","fee","formula","currencyRounding"],"description":"What this line changes"},"objectId":{"type":"string","description":"ID of the product, rate, price list, rule, tax, fee or formula"},"venue":{"type":"string","description":"Venue the line applies to; empty for all in scope","nullable":true},"market":{"type":"string","description":"Market the line applies to; empty for all in scope","nullable":true},"proposedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Proposed amount for a monetary line; empty for removals and non-monetary changes","nullable":true},"proposedValue":{"type":"string","description":"Proposed value for a non-monetary line (rule, formula, rounding), as the target screen's own format","nullable":true},"remove":{"type":"boolean","description":"True when the line removes the rate or object (Rate Removal)"},"currentAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Current live amount (Before)","nullable":true},"differenceAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Proposed minus current","nullable":true},"differencePercent":{"type":"number","description":"Difference in percent of the current amount","nullable":true}},"description":"One changed object with before/after"},"description":"Change lines: one request may cover many products, rates, venues and markets"},"status":{"type":"string","description":"Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected, cancelled or rolledBack; saving leaves it draft"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals.ApprovalRequest` opened by `submitPricingChangeRequest`; null while the request is a draft (decided 29 September, readiness close-out)."},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI summary lines for this record: advisory only, never approves, publishes or changes a price"}}},
"PricingDistributionSynchronizationPublicationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Distribution, Synchronization & Publication Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publicationStarted":{"type":"string","format":"date-time","description":"Publication started"},"lastUpdated":{"type":"string","format":"date-time","description":"Last updated"},"recordsPublished":{"type":"integer","description":"Records published"},"recordsFailed":{"type":"integer","description":"Records failed"},"latency":{"type":"number","description":"Latency in seconds from publication start to confirmation","nullable":true},"targetVersion":{"type":"string","description":"Pricing version the target currently serves"},"publicationVersion":{"type":"string","description":"Version being published"},"target":{"type":"string","enum":["b2c","mobileApp","pos","mobilePos","kiosk","callCenter","b2b","reseller","ota","api","cacheCdn","externalSystem"],"description":"Distribution Target (pack p.68)"},"targetName":{"type":"string","description":"Named target where there are several, e.g. OTA A","nullable":true},"status":{"type":"string","description":"Status: pending, publishing, synchronized, warning, failed or suspended"},"currentProductionVersion":{"type":"string","description":"Current production version"},"inSync":{"type":"boolean","description":"Consistency check: targetVersion equals currentProductionVersion"},"failureReason":{"type":"string","description":"Failure reason","nullable":true}}},
"PricingGovernanceCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Pricing Governance Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"pricingChangesInDraft":{"type":"integer","description":"Pricing Changes in Draft"},"pendingValidation":{"type":"integer","description":"Pending Validation"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"approvedChanges":{"type":"integer","description":"Approved Changes"},"scheduledPublications":{"type":"integer","description":"Scheduled Publications"},"publishedToday":{"type":"integer","description":"Published Today: change requests published since 00:00 venue time"},"failedPublications":{"type":"integer","description":"Failed Publications"},"emergencyChanges":{"type":"integer","description":"Emergency Changes"},"rollbacks":{"type":"integer","description":"Rollbacks"},"expiringPrices":{"type":"integer","description":"Expiring Prices: rates whose expiry falls within the next 30 days (decided 29 September, readiness close-out)"},"governanceExceptions":{"type":"integer","description":"Governance Exceptions: changes that breached a configured threshold, bypassed a step under emergency override, or await retrospective approval (decided 29 September, readiness close-out)"},"highRiskChanges":{"type":"integer","description":"High-Risk Changes: open changes whose risk score is high or critical"},"governanceAlerts":{"type":"array","items":{"type":"string"},"description":"Governance Alerts (pack p.58), e.g. changes activating within 24 hours, changes over the configured commercial-change threshold, failed channel synchronizations"},"aiSummary":{"type":"array","items":{"type":"string"},"description":"AI Governance Assistant summary lines: advisory only"}}},
"PricingGovernanceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"changeId":{"type":"string","description":"Change request ID"},"changeName":{"type":"string","description":"Change name, e.g. Summer Admission 2027"},"changeType":{"type":"string","enum":["priceChange","newRate","rateRemoval","priceListChange","eligibilityRuleChange","taxChange","feeChange","formulaChange","currencyRoundingChange","emergencyChange"],"description":"Change Type (pack p.59)"},"scope":{"type":"string","description":"Scope summary, e.g. \"24 products\", \"8 partners\", \"UAE\""},"revenueImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Estimated revenue impact from the impact analysis; empty when not monetary (e.g. a regulatory VAT change)","nullable":true},"impactNote":{"type":"string","description":"Impact label when not monetary, e.g. Regulatory","nullable":true},"requestedBy":{"type":"string","description":"Requested by (user or team)"},"owner":{"type":"string","description":"Owner"},"approver":{"type":"string","description":"Current approver (role or user) awaited","nullable":true},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk score from the impact analysis (pack p.64)"},"status":{"type":"string","description":"Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected, cancelled or rolledBack"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective date requested"}}},
"PricingHistoryAuditComplianceExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing History, Audit & Compliance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"changedBy":{"type":"string","description":"Changed by (user, or the system actor)"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"reason":{"type":"string","description":"Reason","nullable":true},"source":{"type":"string","enum":["backOffice","bulkImport","api","dynamicPricingEngine","rollback","emergencyAction"],"description":"Source of the change (decided 29 September, readiness close-out)"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective date","nullable":true},"publication":{"type":"string","description":"Publication ID","nullable":true},"auditId":{"type":"string","description":"Audit entry ID"},"auditType":{"type":"string","enum":["configuration","approval","publication","synchronization","override","rollback","emergencyAction"],"description":"Audit Type (pack p.71)"},"entityType":{"type":"string","description":"What changed: price list, rate, rule, tax, fee, formula, strategy, guardrail..."},"entityId":{"type":"string","description":"ID of what changed"},"field":{"type":"string","description":"Field changed","nullable":true},"oldValue":{"type":"string","description":"Old value","nullable":true},"newValue":{"type":"string","description":"New value","nullable":true},"changeRequestId":{"type":"string","description":"Change request","nullable":true},"approvalId":{"type":"string","description":"Approval","nullable":true},"version":{"type":"string","description":"Pricing version","nullable":true},"rollbackId":{"type":"string","description":"Rollback, if applicable","nullable":true}}},
"PricingPublicationEffectiveDateSchedulerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Pricing Publication & Effective-Date Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"version":{"type":"string","description":"Approved pricing version to publish"},"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"}}},
"PricingPublicationEffectiveDateSchedulerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Publication & Effective-Date Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"version":{"type":"string","description":"Approved pricing version to publish"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"},"prePublicationChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["approvalComplete","validationPassed","noCriticalConflicts","dependenciesAvailable","channelsReady","effectiveDatesValid"],"description":"Pre-Publication Check (pack p.67)"},"passed":{"type":"boolean","description":"Passed"},"message":{"type":"string","description":"Detail, e.g. the colliding version","nullable":true}},"description":"One check"},"description":"Pre-publication check results"},"collisions":{"type":"array","items":{"type":"string"},"description":"Other versions scheduled to become effective for the same object and date"},"status":{"type":"string","description":"Status: scheduled, blocked, published, cancelled or failed"}}},
"PricingRollbackEmergencyControlCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Rollback & Emergency Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"productsAffected":{"type":"integer","description":"Products affected"},"channelsAffected":{"type":"integer","description":"Channels affected"},"transactionsSinceActivation":{"type":"integer","description":"Transactions since the faulty version activated"},"revenueExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Revenue exposure"},"existingOrders":{"type":"integer","description":"Existing orders in scope; kept at the price they were sold at"},"futureSales":{"type":"integer","description":"Future sales (unsold inventory) whose price the action changes"},"reason":{"type":"string","description":"Reason"},"authorizedRole":{"type":"string","description":"Role under which the action was authorised"},"incidentReference":{"type":"string","description":"Incident reference","nullable":true},"timestamp":{"type":"string","format":"date-time","description":"When the action was executed","nullable":true},"actionId":{"type":"string","description":"Action ID"},"actionType":{"type":"string","enum":["rollback","freezePriceList","freezeProductPricing","freezeVenuePricing","stopScheduledPublication","stopDistribution","restoreLastKnownGood"],"description":"Rollback or Emergency Freeze control (pack pp.69-70)"},"rollbackTarget":{"type":"string","enum":["previousVersion","selectedVersion","previousPrice","commercialBaseline"],"description":"Rollback to","nullable":true},"rollbackScope":{"type":"string","enum":["selectedProducts","selectedVenue","selectedMarket","selectedChannel","entirePublication"],"description":"Rollback scope","nullable":true},"scopeIds":{"type":"array","items":{"type":"string"},"description":"Products, venue, market or channel in scope"},"fromVersion":{"type":"string","description":"Version in force before the action","nullable":true},"toVersion":{"type":"string","description":"Version restored","nullable":true},"performedBy":{"type":"string","description":"User who performed the action"},"retrospectiveApprovalRequired":{"type":"boolean","description":"Retrospective approval required; true by default for emergency actions (decided 29 September, readiness close-out)"},"status":{"type":"string","description":"Status: previewed, executed, awaitingRetrospectiveApproval, approved, failed or released"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI summary lines for this record: advisory only, never approves, publishes or changes a price"}}},
"PricingVersionBaselineManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Version & Baseline Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"version":{"type":"string","description":"Version number, e.g. 5.3"},"priceList":{"type":"string","description":"Price list name"},"createdDate":{"type":"string","format":"date-time","description":"Created date"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective date","nullable":true},"createdBy":{"type":"string","description":"Created by"},"changeRequest":{"type":"string","description":"Change request ID that produced the version","nullable":true},"productCount":{"type":"integer","description":"Product Count"},"changeCount":{"type":"integer","description":"Change Count"},"status":{"type":"string","description":"Status: draft, candidate, approved, scheduled, active, superseded, rolledBack or archived"},"added":{"type":"integer","description":"Rates added compared with the compareTo version (default: the commercial baseline)"},"removed":{"type":"integer","description":"Rates removed compared with the compareTo version"},"modified":{"type":"integer","description":"Rates modified compared with the compareTo version"},"unchanged":{"type":"integer","description":"Rates unchanged compared with the compareTo version"},"isCommercialBaseline":{"type":"boolean","description":"Designated as the commercial baseline for its price list"}}}
}
```
