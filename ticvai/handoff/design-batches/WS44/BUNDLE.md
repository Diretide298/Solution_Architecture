# WS44 — Product Lifecycle   Catalogue Governance board 2

**10 screens · 15 operations · 27 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_APPROVE, APPROVAL_CONFIGURE, APPROVAL_VIEW, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-128` | Product Governance Command Center | B | 6 | 228 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `ADM-129` | Approval Workflow Designer | B | 18 | 20 | 5 | 0 | 2 | 3 | — | notStarted (generated) |
| `ADM-130` | Approval Review & Decision Workspace | B | 0 | 20 | 6 | 7 | 1 | 3 | — | notStarted (generated) |
| `ADM-131` | Product Version Management | B | 0 | 0 | 6 | 4 | 2 | 0 | — | notStarted (generated) |
| `ADM-132` | Rollback & Recovery Management | B | 21 | 0 | 6 | 1 | 2 | 0 | — | notStarted (generated) |
| `ADM-133` | Change Impact Analysis | B | 6 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-134` | Change Propagation & Dependency Control | B | 6 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-135` | Product Retirement, Suspension & Archive | B | 9 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-136` | Product Audit Trail & Change History | B | 16 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-137` | Governance Risk, AI Monitoring & Control Center | B | 4 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-130, ADM-132, ADM-133, ADM-134, ADM-137 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-128` Product Governance Command Center

**Provide management and administrators with a single control center for all product governance activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-128 |
| Who uses it | venue staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The dashboard shall display; Each record should display) and no metric row |
| Offline | online only |
| Opens with | `findingId` (navigation) |
| Route | `/catalogue/product-governance-command-center-adm-128` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All product governance in one control centre: counts by status, pending approvals, versions, rollbacks and AI findings with their human decision.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product governance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product type, owner, department, status, risk and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product type | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProductGovernance` ?productType |
| Owner | text field | — | — | `listProductGovernance` ?owner |
| Department | text field | — | — | `listProductGovernance` ?department |
| Status | text field | — | — | `listProductGovernance` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listProductGovernance` ?risk |
| Change type | select | — | New product · Description · Price · Validity · Capacity · Entitlement · Eligibility · Tax · Channel · Media · Policy · Relationship … | `listProductGovernance` ?changeType |
| Approver | text field | — | — | `listProductGovernance` ?approver |
| Effective from | date picker | — | — | `listProductGovernance` ?effectiveFrom |
| Effective to | date picker | — | — | `listProductGovernance` ?effectiveTo |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listProductGovernance` ?channel |

**Form: Decide catalogue AI finding** (modal, opened by *Decide catalogue AI finding*; *Decide catalogue AI finding* calls `decideCatalogueAiFinding`, *Cancel* sends nothing)

**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Acknowledge · Accept · Dismiss · Resolve | — | — | `decideCatalogueAiFinding` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideCatalogueAiFinding` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `decideCatalogueAiFinding` body |
| Due date `dueDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideCatalogueAiFinding` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`.

#### Outputs: what the screen shows and produces

**Shown**

**Products awaiting approval** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Changes awaiting approval** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Rejected changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with governance warnings** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Scheduled changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with unpublished changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with dependency conflicts** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products approaching retirement** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Recently published versions** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**High risk configuration changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every product governance** (data table, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Failed publications/rollbacks | text | not in the schema: `Failed publications/rollbacks` |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |

**The selected product governance** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Failed publications/rollbacks | text | not in the schema: `Failed publications/rollbacks` |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide catalogue AI finding (primary button) | `decideCatalogueAiFinding` POST `/ai-findings/{findingId}/decision` | inline | CatalogueAiFinding | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`. | gated `AI_APPROVE`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Decide an AI finding**: Acknowledge, accept, dismiss or resolve, with owner; the finding moves state. *(source: contracts/spine/catalogue.yaml#decideCatalogueAiFinding)*

**Data it reads**: `listProductGovernance` (onLoad, Product Governance Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-131` Product Version Management: *Product Version Management*; carries `productId`
- → `ADM-129` Approval Workflow Designer: *Works in Approval Workflow Designer*; calls `listProductGovernance`
- → `ADM-130` Approval Review & Decision Workspace: *Works in Approval Review & Decision Workspace*; calls `listProductGovernance`
- → `ADM-132` Rollback & Recovery Management: *Works in Rollback & Recovery Management*; calls `listProductGovernance`
- → `ADM-135` Product Retirement, Suspension & Archive: *Works in Product Retirement, Suspension & Archive*; calls `listProductGovernance`
- → `ADM-136` Product Audit Trail & Change History: *Works in Product Audit Trail & Change History*; calls `listProductGovernance`
- → `ADM-133` Change Impact Analysis: *Works in Change Impact Analysis*; carries `productId`; calls `listProductGovernance`
- → `ADM-134` Change Propagation & Dependency Control: *Works in Change Propagation & Dependency Control*; carries `productId`; calls `listProductGovernance`
- → `ADM-137` Governance Risk, AI Monitoring & Control Center: *Works in Governance Risk, AI Monitoring & Control Center*; carries `findingId`; calls `listProductGovernance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyClosed`.; 422 `commentRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
findings:
- type: Price below cost
  product: Kids Meal Combo
  severity: high
```

#### Permissions

- `listProductGovernance` → `PRODUCT_VIEW` (read) · staff
- `decideCatalogueAiFinding` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-128` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-128`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 1: Opens Product Governance Command Center → Provide management and administrators with a single control center for all product governance activities.
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F153 branch at step 1 (expected): when Nothing has been set up on Product Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F153 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (228 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-128?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide catalogue AI finding.
- [ ] Every transition is wired: `BO-100`, `ADM-131`, `ADM-129`, `ADM-130`, `ADM-132`, `ADM-135`, `ADM-136`, `ADM-133`, `ADM-134`, `ADM-137`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-129` Approval Workflow Designer

**Configure reusable approval workflows governing product creation and modification.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-129 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `PRODUCT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each workflow can define; Tax configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/approval-workflow-designer-adm-129` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Approval workflows for product creation and change, as on BO-637.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveWorkflow and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow name | select field | — | — | — | — | — | — |
| Applicable product types | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Change type | select field | — | — | — | — | — | — |
| Approval stages | select field | — | — | — | — | — | — |
| Approver role | select field | — | — | — | — | — | — |
| Specific approver | select field | — | — | — | — | — | — |
| Approval group | select field | — | — | — | — | — | — |
| Sequential/parallel approval | select field | — | — | — | — | — | — |
| Mandatory/optional stage | select field | — | — | — | — | — | — |
| SLA | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Delegation | select field | — | — | — | — | — | — |
| Reminder frequency | select field | — | — | — | — | — | — |
| Rejection behavior | select field | — | — | — | — | — | — |
| Resubmission behavior | select field | — | — | — | — | — | — |
| → Finance | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

#### Outputs: what the screen shows and produces

**Shown**

**Approval routes** (data table, from `listApprovalMatrices`)

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

**Data it reads**: `listApprovalMatrices` (onLoad, The approval routes already configured)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `approveWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow designer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow designer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-637`: Same operation and editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workflow:
  name: New product
  stages:
  - Product manager
  - Commercial manager
  - Finance
```

#### Permissions

- `approveWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-129` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-129`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 2: Works in Approval Workflow Designer → Configure reusable approval workflows governing product creation and modification.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-129?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-130` Approval Review & Decision Workspace

**Give approvers a clear interface for reviewing a proposed product or product change before making a decision.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-130 |
| Who uses it | venue staff holding `APPROVAL_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/approval-review-decision-workspace-adm-130` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The approver's view of a proposed product or change: what changes (before and after), the previews (B2C card, PDF ticket, wallet pass), impact, and the decision.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveReviewDecision and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **decision**: Approve, reject, request changes, reassign, delegate, escalate; comment required except approve. *(source: contracts/spine/catalogue.yaml#approveReviewDecision / DI-444)*

#### Outputs: what the screen shows and produces

**Shown**

**Requests to review** (data table, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Reroute on no approver | yes / no (icon or chip) | BL-154. An approver on leave is an approval that waits for them to come back. |
| Out of office delegate | the name it points at, never the id | — |
| Allow email approval | yes / no (icon or chip) | Approving from an email link with no second factor is the weakest path in the system, so it is off by default and available only below a … |
| Reopened from | the name it points at, never the id | Reopening a decided approval creates a new one that points back. Editing a decision in place destroys the record of what was originally … |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Subject contract | text | — |
| Subject type | text | — |
| Subject | text | — |
| Summary | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Justification | text | — |
| Requested by principal | the name it points at, never the id | — |
| Matrix version | 1,234 | — |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Current level | 1,234 | — |
| Total levels | 1,234 | — |
| Pending approvers | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalRequests` (onLoad, Requests awaiting a decision, or already decided)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `approveReviewDecision`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval review decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval review decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval review decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval review decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  product: Twilight Ticket
  change: new product
  previews:
  - B2C card
  - PDF ticket
  - Apple Wallet
```

#### Permissions

- `approveReviewDecision` → `PRODUCT_CONFIGURE` (configure) · staff
- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-130` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-130`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 4: Works in Approval Review & Decision Workspace → Give approvers a clear interface for reviewing a proposed product or product change before making a decision.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-130?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Cancel.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-131` Product Version Management

**Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions. (a section of BO-008 Product Detail & Variants since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-131 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/venue-operations/product-detail-variants/product-version-management-adm-131` |

**What the spec says about it.** **Merged into BO-008 Product Detail & Variants as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-008: it renders inside BO-008's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Basic product information, Pricing, Capacity, Entitlements, Channels. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Versions of every governed product, with restore creating a new version.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Basic product information, Pricing, Capacity, Entitlements, Channels. (CHG-MOV-008)
- List operation(s) listProductVersions return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Version 4.2 ↔ Version 4.1 (primary button) | navigation or local | — | — | — | — |
| Basic product information (secondary button) | navigation or local | — | — | — | — |
| Pricing (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Entitlements (secondary button) | navigation or local | — | — | — | — |
| Channels (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductVersions`
- → `BO-008` Product Detail & Variants: *Open Product Detail & Variants*; carries `productId`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product version yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-008`: Same version list as the product configuration.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- v: 9
  at: '2026-11-02'
  by: Layla Hassan
  change: price
```

#### Permissions

- `listProductVersions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.9 | System shall maintain version history of all product configurations including pricing, rules, entitlements and capacities. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 1.4.10 | System shall allow authorized users to restore a previous version of a product configuration. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 1.4.11 | System shall support duplication of products including all associated configurations, rules, pricing and entitlements. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 2.9.7 | The system should guarantee the integrity of all pre-existing revenue by ensuring that when an amount is amended, the value of prior sales is not modified. | Ticketing Sales | CONTRACTED | `listProductVersions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-131` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-131`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 6: Works in Product Version Management → Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-131?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Version 4.2 ↔ Version 4.1, Basic product information, Pricing, Capacity, Entitlements, Channels.
- [ ] Every transition is wired: `ADM-128`, `BO-008`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-132` Rollback & Recovery Management

**Safely restore an earlier product configuration when a newly published configuration causes an issue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-132 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/rollback-recovery-management-adm-132` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Restore an earlier product configuration safely when a publication causes trouble; sold tickets are untouched.

**Fixed on main** (the package already carries these; draw what it says): The screen lists rollbacks but declares no write; requestPricingRollback handles subject product as well. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listRollbackRecovery` ?productId |
| Status | text field | — | — | `listRollbackRecovery` ?status |
| Scope | select | — | Entire product · Pricing association · Channel association · Validity configuration · Media · Policy · Entitlement configuration | `listRollbackRecovery` ?scope |
| Emergency | toggle | — | — | `listRollbackRecovery` ?emergency |

**Form: Roll back** (modal, opened by *Roll back*; *Roll back* calls `requestPricingRollback`, *Cancel* sends nothing)

**Collects what `requestPricingRollback` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Roll back (secondary button) | `requestPricingRollback` POST `/pricing-rollback-emergency` | CatalogueRollbackAction | CatalogueRollbackAction | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `rollbackTargetRequired`, `scheduledAtInPast` or `incidentReferenceRequired`. | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rollback candidates**: Version, what it restores, affected scope. *(source: contracts/spine/catalogue.yaml#listRollbackRecovery)*

**Data it reads**: `listRollbackRecovery` (onLoad, Rollback & Recovery Management)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listRollbackRecovery`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rollback recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rollback recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rollback recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rollback recovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `rollbackTargetRequired`, `scheduledAtInPast` or `incidentReferenceRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rollback:
  product: Day Pass
  to: version 8
  reason: Child age range published wrongly
```

#### Permissions

- `listRollbackRecovery` → `PRODUCT_VIEW` (read) · staff
- `requestPricingRollback` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.26 | System shall support rollback of pricing changes. | Unified Operations Dashboard | CONTRACTED | `requestPricingRollback` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-132` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-132`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 8: Works in Rollback & Recovery Management → Safely restore an earlier product configuration when a newly published configuration causes an issue.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-132?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Roll back.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-133` Change Impact Analysis

**Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are published.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-133 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/catalogue/change-impact-analysis-adm-133` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What a product change will affect before it is approved: bookings, reservations, promotions, linked products, integrations; and the product's dependency links.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listChangeImpactAnalysis return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Change request | picker: choose a change request | — | — | `listChangeImpactAnalysis` ?changeRequestId |
| Product | picker: choose a product | — | — | `listChangeImpactAnalysis` ?productId |
| Area | select | — | Future orders · Reservations · Issued tickets · Capacity · Pricing · Tax · Promotions · Membership · Entitlements · Access control · Sales channels · B2B partners … | `listChangeImpactAnalysis` ?area |
| Min risk | radio group | — | Low · Medium · High · Critical | `listChangeImpactAnalysis` ?minRisk |

**Sent by *Save product links*** (`setProductLinks`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source product `sourceProductId` | picker: choose a source product | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Dependency type `dependencyType` | select | required | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | — | — | `setProductLinks` body |
| Linked object `linkedObjectId` | picker: choose a linked object | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Linked object name `linkedObjectName` | text field | optional | — | max length 200 | — | — | `setProductLinks` body |
| Propagates changes `propagatesChanges` | toggle | optional | on | — | — | — | `setProductLinks` body |
| Overridden fields `overriddenFields` | list of values (chips) | optional | — | — | — | — | `setProductLinks` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product links (primary button) | `setProductLinks` PUT `/products/{productId}/links` | ProductLink[] | ProductLink[] | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `circularDependency` or `duplicateLink`. | gated `PRODUCT_CONFIGURE` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **impact**: Numbers first, then lists, then whether each dependent propagates. *(source: contracts/spine/catalogue.yaml#listChangeImpactAnalysis / contracts/spine/catalogue.yaml#assessProductChange / DI-579)*

**Data it reads**: `listChangeImpactAnalysis` (onLoad, Change Impact Analysis)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listChangeImpactAnalysis`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change impact analysis list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change impact analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change impact analysis yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change impact analysis are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `circularDependency` or `duplicateLink`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
impact:
  bookings: 1840
  promotions: 2
  linkedProducts:
  - Family Fun Bundle
```

#### Permissions

- `listChangeImpactAnalysis` → `PRODUCT_VIEW` (read) · staff
- `setProductLinks` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-133` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-133`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 10: Works in Change Impact Analysis → Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-133?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product links.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-134` Change Propagation & Dependency Control

**Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-134 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/catalogue/change-propagation-dependency-control-adm-134` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether approved changes propagate to related products and configurations, per dependency.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listChangePropagationDependency` ?productId |
| Change request | picker: choose a change request | — | — | `listChangePropagationDependency` ?changeRequestId |
| Dependency type | select | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | `listChangePropagationDependency` ?dependencyType |
| Conflicts only | toggle | — | — | `listChangePropagationDependency` ?conflictsOnly |

**Sent by *Save product links*** (`setProductLinks`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source product `sourceProductId` | picker: choose a source product | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Dependency type `dependencyType` | select | required | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | — | — | `setProductLinks` body |
| Linked object `linkedObjectId` | picker: choose a linked object | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Linked object name `linkedObjectName` | text field | optional | — | max length 200 | — | — | `setProductLinks` body |
| Propagates changes `propagatesChanges` | toggle | optional | on | — | — | — | `setProductLinks` body |
| Overridden fields `overriddenFields` | list of values (chips) | optional | — | — | — | — | `setProductLinks` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **links**: Each dependent with its dependency type and a propagate switch; saved whole per source product. *(source: contracts/spine/catalogue.yaml#setProductLinks)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product links (primary button) | `setProductLinks` PUT `/products/{productId}/links` | ProductLink[] | ProductLink[] | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `circularDependency` or `duplicateLink`. | gated `PRODUCT_CONFIGURE` |

**Data it reads**: `listChangePropagationDependency` (onLoad, Change Propagation & Dependency Control)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listChangePropagationDependency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change propagation dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change propagation dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change propagation dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change propagation dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `circularDependency` or `duplicateLink`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
links:
- dependent: Family Fun Bundle
  type: component
  propagate: true
```

#### Permissions

- `listChangePropagationDependency` → `PRODUCT_VIEW` (read) · staff
- `setProductLinks` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-134` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-134`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 12: Works in Change Propagation & Dependency Control → Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-134?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product links.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-135` Product Retirement, Suspension & Archive

**Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-135 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-retirement-suspension-archive-adm-135` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Suspend Sales, Temporarily Disable, End Sale, Archive. Each needs an operation, or needs removing from the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** End of life: suspend, withdraw, retire or archive a product without affecting tickets already sold.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Suspend Sales, Temporarily Disable, End Sale, Archive. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retirement date | select field | — | — | — | — | — | — |
| End-of-sale date | select field | — | — | — | — | — | — |
| Channels | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Replacement product | select field | — | — | — | — | — | — |
| Existing reservation treatment | select field | — | — | — | — | — | — |
| Existing ticket treatment | select field | — | — | — | — | — | — |
| Communication requirements | select field | — | — | — | — | — | — |
| Reporting treatment | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action | radio group | — | Suspend sales · Temporarily disable · End sale · Retire · Archive | `listProductRetirementSuspension` ?action |
| Lifecycle state | select | — | Draft · In review · Approved · Live · Withdrawn · Archived | `listProductRetirementSuspension` ?lifecycleState |
| Search | text field | — | — | `listProductRetirementSuspension` ?search |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Suspend Sales (destructive button) | navigation or local | — | — | — | — |
| Temporarily Disable (secondary button) | navigation or local | — | — | — | — |
| End Sale (destructive button) | navigation or local | — | — | — | — |
| Retire (secondary button) | navigation or local | — | — | — | — |
| Archive (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **end-of-life list**: Product, state, sold tickets still valid, scheduled end. *(source: contracts/spine/catalogue.yaml#listProductRetirementSuspension)*

**Data it reads**: `listProductRetirementSuspension` (onLoad, Product Retirement, Suspension & Archive)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductRetirementSuspension`

**What opens over it**

- confirmDialog *Suspend Sales*: **Suspend Sales on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End Sale*: **End Sale on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Archive*: **Archive on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product retirement suspension configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product retirement suspension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product retirement suspension configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  product: Summer Splash Pass
  state: Withdrawn
  validTicketsOutstanding: 412
```

#### Permissions

- `listProductRetirementSuspension` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-135` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-135`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 14: Works in Product Retirement, Suspension & Archive → Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-135?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Suspend Sales, Temporarily Disable, End Sale, Retire, Archive.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-136` Product Audit Trail & Change History

**Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-136 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each entry should capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-audit-trail-change-history-adm-136` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Immutable history of product configuration and governance activity with timestamps and users.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product audit trail | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by product, user, date, action, version, configuration area and 4 more — which are present is a decision the pack already made. | — |
| Date/time | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Role | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Version | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Configuration area | select field | — | — | — | — | — | — |
| Previous value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval reference | select field | — | — | — | — | — | — |
| Source channel | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| IP/device metadata where applicable | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductTrailChange` ?productId |
| User | picker: choose an user | — | — | `listProductTrailChange` ?userId |
| From | date and time picker | — | — | `listProductTrailChange` ?from |
| To | date and time picker | — | — | `listProductTrailChange` ?to |
| Action | select | — | Created · Updated · Submitted · Approved · Rejected · Changes requested · Scheduled · Published · Rolled back · Suspended · Retired · Archived … | `listProductTrailChange` ?action |
| Version | number field | — | — | `listProductTrailChange` ?version |
| Configuration area | select | — | Basic information · Validity · Pricing · Capacity · Entitlements · Eligibility · Media · Channels · Policies · Relationships · Lifecycle | `listProductTrailChange` ?configurationArea |
| Venue | picker: choose a venue | — | — | `listProductTrailChange` ?venue |
| Approval | text field | — | — | `listProductTrailChange` ?approval |
| Risk | radio group | — | Low · Medium · High · Critical | `listProductTrailChange` ?risk |
| Environment | radio group | — | Development · Sandbox · Uat · Staging · Production | `listProductTrailChange` ?environment |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **audit trail**: Filter by product, user, action; before and after. *(source: contracts/spine/catalogue.yaml#listProductTrailChange)*

**Data it reads**: `listProductTrailChange` (onLoad, Product Audit Trail & Change History)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductTrailChange`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product audit trail configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product audit trail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product audit trail configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product audit trail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  product: Day Pass
  user: Layla Hassan
  action: price change
  at: 2026-11-02 10:14
```

#### Permissions

- `listProductTrailChange` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-136` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-136`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 16: Works in Product Audit Trail & Change History → Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-136?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-137` Governance Risk, AI Monitoring & Control Center

**Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-137 |
| Who uses it | venue staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `findingId` (navigation) |
| Route | `/catalogue/governance-risk-ai-monitoring-control-center-adm-137` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI watching the catalogue for governance risks (price below cost, missing translations, expiring products, inconsistent rules), each finding decided by a person.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | radio group | — | Critical · High · Medium · Low | `listGovernanceRiskMonitoring` ?severity |
| Risk | select | — | Product without owner · Missing approval · Outdated pricing · Conflicting validity · Missing channel configuration · Orphaned dependency · Unused product · Duplicate product · Unusual configuration change · High override level · Scheduled publication conflict … | `listGovernanceRiskMonitoring` ?risk |
| Owner | text field | — | — | `listGovernanceRiskMonitoring` ?owner |
| Status | text field | — | — | `listGovernanceRiskMonitoring` ?status |

**Form: Decide catalogue AI finding** (modal, opened by *Decide catalogue AI finding*; *Decide catalogue AI finding* calls `decideCatalogueAiFinding`, *Cancel* sends nothing)

**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Acknowledge · Accept · Dismiss · Resolve | — | — | `decideCatalogueAiFinding` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideCatalogueAiFinding` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `decideCatalogueAiFinding` body |
| Due date `dueDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideCatalogueAiFinding` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`.

#### Outputs: what the screen shows and produces

**Shown**

**Every governance risk monitoring** (data table, from `listGovernanceRiskMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Critical / high / medium / low | text | not in the schema: `Critical / High / Medium / Low` |
| Risk | chip: Product without owner, Missing approval, Outdated pricing, Conflicting validity … | Risk detected (AI Monitoring, pack p.26) |
| Product | text | Product name |
| Venue | text | Venue name |
| Business impact | text | Business impact, in plain language |
| Recommended action | text | Recommended action; advisory |
| Owner | text | Owner (display name) |
| Due date | 1 Oct 2026 | Due date |
| Status | text | Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out) |

**The selected governance risk monitoring** (detail panel): The pack groups this record's detail under its own headings: “Potential duplicate detected”, “Governance warning”, “Backend Screen Primary Responsibility”, “Restore previous”, “Pre-change impact”.

| Shows | Format | Notes |
|---|---|---|
| Critical / high / medium / low | text | not in the schema: `Critical / High / Medium / Low` |
| Risk | chip: Product without owner, Missing approval, Outdated pricing, Conflicting validity … | Risk detected (AI Monitoring, pack p.26) |
| Product | text | Product name |
| Venue | text | Venue name |
| Business impact | text | Business impact, in plain language |
| Recommended action | text | Recommended action; advisory |
| Owner | text | Owner (display name) |
| Due date | 1 Oct 2026 | Due date |
| Status | text | Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out) |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide catalogue AI finding (primary button) | `decideCatalogueAiFinding` POST `/ai-findings/{findingId}/decision` | inline | CatalogueAiFinding | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`. | gated `AI_APPROVE`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Decide finding**: As on ADM-128. *(source: contracts/spine/catalogue.yaml#decideCatalogueAiFinding)*

**Data it reads**: `listGovernanceRiskMonitoring` (onLoad, Governance Risk, AI Monitoring & Control Center)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Product Governance Command Center*; carries `findingId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance risk monitoring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance risk monitoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance risk monitoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance risk monitoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyClosed`.; 422 `commentRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
finding:
  type: Arabic description missing
  products: 7
  severity: medium
```

#### Permissions

- `listGovernanceRiskMonitoring` → `PRODUCT_VIEW` (read) · staff
- `decideCatalogueAiFinding` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Catalogue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-137` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-137`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 18: Works in Governance Risk, AI Monitoring & Control Center → Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-137?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide catalogue AI finding.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
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

### In P08 · Catalogue

- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveReviewDecision": {"method":"PUT","path":"/review-decision","contract":"catalogue","summary":"Approval Review & Decision Workspace","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalReviewDecisionWorkspaceInput","responds":"ApprovalReviewDecisionWorkspaceView"},
"approveWorkflow": {"method":"PUT","path":"/workflow","contract":"catalogue","summary":"Approval Workflow Designer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalWorkflowDesignerInput","responds":"ApprovalWorkflowDesignerView"},
"decideCatalogueAiFinding": {"method":"POST","path":"/ai-findings/{findingId}/decision","contract":"catalogue","summary":"Acknowledge, accept, dismiss or resolve an AI finding","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CatalogueAiFinding"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChangeImpactAnalysis": {"method":"GET","path":"/change-impact-analysi","contract":"catalogue","summary":"Change Impact Analysis","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"changeRequestId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"area","in":"query","required":false},{"name":"minRisk","in":"query","required":false}],"requestBody":null,"responds":"ChangeImpactAnalysisView"},
"listChangePropagationDependency": {"method":"GET","path":"/change-propagation-dependency","contract":"catalogue","summary":"Change Propagation & Dependency Control","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"changeRequestId","in":"query","required":false},{"name":"dependencyType","in":"query","required":false},{"name":"conflictsOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGovernanceRiskMonitoring": {"method":"GET","path":"/governance-risk-monitoring","contract":"catalogue","summary":"Governance Risk, AI Monitoring & Control Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductGovernance": {"method":"GET","path":"/product-governance","contract":"catalogue","summary":"Product Governance Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"changeType","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"effectiveFrom","in":"query","required":false},{"name":"effectiveTo","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductRetirementSuspension": {"method":"GET","path":"/product-retirement-suspension","contract":"catalogue","summary":"Product Retirement, Suspension & Archive","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"action","in":"query","required":false},{"name":"lifecycleState","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductTrailChange": {"method":"GET","path":"/product-trail-change","contract":"catalogue","summary":"Product Audit Trail & Change History","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"userId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"version","in":"query","required":false},{"name":"configurationArea","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"approval","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"environment","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVersions": {"method":"GET","path":"/products/{productId}/versions","contract":"catalogue","summary":"What this product used to be","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductVersion"},
"listRollbackRecovery": {"method":"GET","path":"/rollback-recovery","contract":"catalogue","summary":"Rollback & Recovery Management","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"scope","in":"query","required":false},{"name":"emergency","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"requestPricingRollback": {"method":"POST","path":"/pricing-rollback-emergency","contract":"catalogue","summary":"Roll pricing back, or take an emergency pricing action","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueRollbackAction","responds":"CatalogueRollbackAction"},
"setProductLinks": {"method":"PUT","path":"/products/{productId}/links","contract":"catalogue","summary":"Replace what depends on a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductLink","responds":"ProductLink"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalReviewDecisionWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Review & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"decision":{"type":"string","enum":["approve","reject","requestChanges","reassign","delegate","escalate"],"description":"Approver action (pack p.18)"},"assignToPrincipalId":{"type":"string","description":"New approver for reassign/delegate/escalate","nullable":true},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"comment":{"type":"string","description":"Comment; required for reject and requestChanges","nullable":true}}},
"ApprovalReviewDecisionWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Review & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"approvalStatus":{"type":"string","description":"Approval status after this decision: pending, changesRequested, approved, rejected, escalated or withdrawn"},"requester":{"type":"string","description":"Requester (display name)"},"reasonForChange":{"type":"string","description":"Reason for change"},"businessJustification":{"type":"string","description":"Business justification"},"attachments":{"type":"array","items":{"type":"object","properties":{"fileId":{"type":"string"},"name":{"type":"string"}}},"description":"Attachments"},"effectiveDate":{"type":"string","description":"Effective date; empty = on approval","format":"date","nullable":true},"currentSales":{"type":"integer","description":"Tickets sold under the current version"},"futureReservations":{"type":"integer","description":"Future reservations of the product"},"channelsAffected":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels affected"},"pricingImpact":{"type":"string","description":"Pricing impact in plain language; the figures are in comparison"},"capacityImpact":{"type":"integer","description":"Change in capacity units (negative = reduction)"},"financeImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Estimated revenue difference over future reservations and forecast sales; advisory"},"accessImpact":{"type":"string","description":"Access impact in plain language"},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"comparison":{"type":"array","items":{"type":"object","properties":{"configurationArea":{"type":"string","enum":["basicInformation","validity","pricing","capacity","entitlements","eligibility","media","channels","policies","relationships","lifecycle"]},"field":{"type":"string"},"currentValue":{"type":"string","nullable":true},"proposedValue":{"type":"string","nullable":true},"changed":{"type":"boolean"}}},"description":"Change comparison, current vs proposed; changed rows are highlighted"},"aiSummary":{"type":"string","description":"AI summary of the proposed change; advisory, the AI does not approve","nullable":true}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"},"code":{"type":"string","maxLength":64,"nullable":true,"description":"**A stable code for the rule, unique within its matrix** (4 October 2026, CHG-FXC-005). The composite `approveMatrixMultiLevel` upserts a rule by it; `setApprovalMatrix` may leave it null."},"minimumApprovals":{"type":"integer","minimum":1,"nullable":true,"description":"N in N-of-M (CHG-FXC-005). Null means every approver the mode asks."},"requiredApproverRoleId":{"type":"string","format":"uuid","nullable":true,"description":"A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of `approverRoleIds` (CHG-FXC-005)."},"rejectionBehavior":{"type":"string","nullable":true,"enum":["rejectRequest","returnToPreviousLevel","returnToRequester"],"description":"What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005)."},"allowRequestChanges":{"type":"boolean","default":false},"allowDelegate":{"type":"boolean","default":true},"allowReassign":{"type":"boolean","default":false},"minPercentage":{"type":"number","nullable":true,"description":"A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside `minAmount` (CHG-FXC-005)."},"matchAttributes":{"type":"object","x-ticvai-persistence-column":"jsonb","nullable":true,"additionalProperties":{"type":"string"},"description":"**The request attributes a rule matches on** (CHG-FXC-005): keys `module`, `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the request's attributes must carry. Every key given must match; an absent key matches anything. Evaluated before `condition`."},"compositeMode":{"type":"string","nullable":true,"enum":["single","sequential","parallel","anyOne","allMustApprove","conditional","multiLevel"],"description":"The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels` and `minimumApprovals` are what the engine runs (CHG-FXC-005)."}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"ApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Existing workflow to change; empty to create","format":"uuid","nullable":true}}},
"ApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Workflow id","format":"uuid"}}},
"CatalogueAiFinding": {"type":"object","x-ticvai-persistence":"catalogue.ai_finding","description":"**Something the AI noticed about the catalogue or its channels, for a person to act on** (29 September, data model DM3). Merges governance risks (ADM-137) and channel optimisation recommendations (ADM-272). Advisory only: a finding never changes configuration; acting on it goes through the ordinary operations and their approvals. **Created by the AI monitoring job** (29 September, writers pass); a person acknowledges, accepts, dismisses or resolves it with `decideCatalogueAiFinding`, and the job resolves one whose condition has cleared (`states/catalogue-ai-finding.yaml`).","required":["id","scopePath","domain","findingType","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"domain":{"type":"string","enum":["productGovernance","channel"]},"findingType":{"type":"string","maxLength":60,"description":"Governance: the `risk` value; channel: the recommendation `category`."},"productId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"salesChannelIds":{"type":"array","items":{"type":"string","format":"uuid"}},"severity":{"type":"string","enum":["critical","high","medium","low",null],"nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"summary":{"type":"string","description":"The recommendation, or the risk in one line."},"explanation":{"type":"string","nullable":true},"businessImpact":{"type":"string","nullable":true},"recommendedAction":{"type":"string","nullable":true},"constraints":{"type":"array","items":{"type":"string"}},"signals":{"type":"array","items":{"type":"string"}},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"description":"Channel findings: `{expectedUnitsSold, revenueImpact, channelUtilization, risk, contractualConstraints}`."},"requiredApproval":{"type":"string","maxLength":100,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"dueDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["open","acknowledged","accepted","dismissed","resolved"],"default":"open"},"modelVersion":{"type":"string","maxLength":60,"nullable":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CatalogueRollbackAction": {"type":"object","x-ticvai-persistence":"catalogue.rollback_action","description":"**A rollback or emergency action on a product or on pricing** (29 September, data model DM3). Merges product rollback (ADM-133) and the pricing rollback and emergency centre (ADM-086). A rollback restores an earlier `catalogue.product_version` or `catalogue.price_list_version` as a new version; nothing is edited in place. Emergency actions may run before approval and then need `retrospectiveApprovalRequired`.","required":["id","scopePath","subject","actionType","reason","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"subject":{"type":"string","enum":["product","pricing"]},"actionType":{"type":"string","enum":["rollback","freezePriceList","freezeProductPricing","freezeVenuePricing","stopScheduledPublication","stopDistribution","restoreLastKnownGood"],"description":"Product rollbacks are `rollback`."},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"fromVersion":{"type":"integer","nullable":true},"toVersion":{"type":"integer","nullable":true},"productScope":{"type":"array","items":{"type":"string","enum":["entireProduct","pricingAssociation","channelAssociation","validityConfiguration","media","policy","entitlementConfiguration"]},"description":"Product rollbacks: which parts are restored."},"rollbackTarget":{"type":"string","enum":["previousVersion","selectedVersion","previousPrice","commercialBaseline",null],"nullable":true},"rollbackScope":{"type":"string","enum":["selectedProducts","selectedVenue","selectedMarket","selectedChannel","entirePublication",null],"nullable":true},"scopeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"dependencies":{"type":"array","items":{"type":"string"},"description":"Product rollbacks: the dependent objects reviewed before executing."},"reason":{"type":"string"},"executionMode":{"type":"string","enum":["immediate","scheduled"],"default":"immediate"},"isEmergency":{"type":"boolean","default":false},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"incidentReference":{"type":"string","maxLength":200,"nullable":true},"authorisedRole":{"type":"string","maxLength":100,"nullable":true},"retrospectiveApprovalRequired":{"type":"boolean","default":false},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"changeRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The change request whose publication is being rolled back."},"status":{"type":"string","enum":["requested","scheduled","executing","completed","failed","cancelled"],"default":"requested"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ChangeImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"area":{"type":"string","enum":["futureOrders","reservations","issuedTickets","capacity","pricing","tax","promotions","membership","entitlements","accessControl","salesChannels","b2bPartners","otas","pos","b2c","kiosk","media","finance","reporting"],"description":"Impact area (pack p.21-22)"},"changeRequestId":{"type":"string","description":"Change request analysed","format":"uuid"},"affectedCount":{"type":"integer","description":"How many items in this area are affected (orders, reservations, agreements, channels...)"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk classification"},"explanation":{"type":"string","description":"AI explanation in business language; advisory","nullable":true}}},
"ChangePropagationDependencyControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Change Propagation & Dependency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dependencyType":{"type":"string","enum":["parentProduct","childProduct","bundle","addOn","upgrade","membership","package","promotion","priceProfile","capacityPool","entitlement","salesChannel","mediaTemplate"],"description":"Dependency type (pack pp.22-23)"},"propagate":{"type":"boolean","description":"Whether the change will propagate to this linked object"},"localOverrideConflict":{"type":"boolean","description":"The linked object has a local override the change would overwrite"},"linkId":{"type":"string","description":"Link id","format":"uuid"},"sourceProductId":{"type":"string","description":"Master product","format":"uuid"},"linkedObjectId":{"type":"string","description":"Linked product or configuration id"},"linkedObjectName":{"type":"string","description":"Linked object name"},"overriddenFields":{"type":"array","items":{"type":"string"},"description":"Fields the linked object overrides locally"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"GovernanceRiskAiMonitoringControlCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"risk":{"type":"string","enum":["productWithoutOwner","missingApproval","outdatedPricing","conflictingValidity","missingChannelConfiguration","orphanedDependency","unusedProduct","duplicateProduct","unusualConfigurationChange","highOverrideLevel","scheduledPublicationConflict","expiredCommercialConfiguration","activeAfterEventEnd","brokenDependency"],"description":"Risk detected (AI Monitoring, pack p.26)"},"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"businessImpact":{"type":"string","description":"Business impact, in plain language"},"recommendedAction":{"type":"string","description":"Recommended action; advisory"},"owner":{"type":"string","description":"Owner (display name)","nullable":true},"dueDate":{"type":"string","description":"Due date","format":"date","nullable":true},"status":{"type":"string","description":"Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"},"riskId":{"type":"string","description":"Risk id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid","nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"],"description":"Severity (Risk Dashboard)"},"explanation":{"type":"string","description":"AI explanation, e.g. the two products share 96% of their configuration; advisory"},"detectedAt":{"type":"string","description":"Detected","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductAuditTrailChangeHistoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Audit Trail & Change History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dateTime":{"type":"string","description":"Date/time","format":"date-time"},"user":{"type":"string","description":"User (display name)"},"role":{"type":"string","description":"Role at the time"},"product":{"type":"string","description":"Product name"},"version":{"type":"integer","nullable":true,"description":"Product version"},"action":{"type":"string","enum":["created","updated","submitted","approved","rejected","changesRequested","scheduled","published","rolledBack","suspended","retired","archived","imported","exported","duplicated"],"description":"Action (decided 29 September, readiness close-out)"},"configurationArea":{"type":"string","enum":["basicInformation","validity","pricing","capacity","entitlements","eligibility","media","channels","policies","relationships","lifecycle"],"description":"Configuration area"},"previousValue":{"type":"string","description":"Previous value","nullable":true},"newValue":{"type":"string","description":"New value","nullable":true},"reason":{"type":"string","description":"Reason","nullable":true},"approvalReference":{"type":"string","description":"Approval reference (change request id)","nullable":true},"sourceChannel":{"type":"string","enum":["backOffice","api","bulkImport","environmentTransfer","scheduler","aiAssistant"],"description":"Where the change was made (decided 29 September, readiness close-out)"},"environment":{"type":"string","enum":["development","sandbox","uat","staging","production"],"description":"Environment"},"deviceMetadata":{"type":"object","nullable":true,"properties":{"ipAddress":{"type":"string"},"userAgent":{"type":"string"},"deviceId":{"type":"string","nullable":true}},"description":"IP/device metadata where applicable"},"auditId":{"type":"string","description":"Audit entry id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"userId":{"type":"string","description":"User principal id","format":"uuid"}}},
"ProductGovernanceCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Product Governance Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"productsAwaitingApproval":{"type":"integer","description":"Products awaiting approval"},"changesAwaitingApproval":{"type":"integer","description":"Changes awaiting approval"},"rejectedChanges":{"type":"integer","description":"Rejected changes (last 30 days) (decided 29 September, readiness close-out)"},"productsWithGovernanceWarnings":{"type":"integer","description":"Products with governance warnings"},"scheduledChanges":{"type":"integer","description":"Scheduled changes"},"productsWithUnpublishedChanges":{"type":"integer","description":"Products with unpublished changes"},"productsWithDependencyConflicts":{"type":"integer","description":"Products with dependency conflicts"},"productsApproachingRetirement":{"type":"integer","description":"Products approaching retirement: retirement date within 30 days (decided 29 September, readiness close-out)"},"recentlyPublishedVersions":{"type":"integer","description":"Recently published versions: published in the last 7 days (decided 29 September, readiness close-out)"},"failedPublications":{"type":"integer","description":"Failed publications"},"failedRollbacks":{"type":"integer","description":"Failed rollbacks"},"highRiskConfigurationChanges":{"type":"integer","description":"High-risk configuration changes (riskLevel high or critical) awaiting decision"}}},
"ProductGovernanceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"productOwner":{"type":"string","description":"Product owner (display name)"},"changeType":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"],"description":"Change type (decided 29 September, readiness close-out)"},"currentVersion":{"type":"integer","nullable":true,"description":"Current version number (ProductVersion.version); empty for a new product"},"proposedVersion":{"type":"integer","description":"Proposed version number"},"requestedBy":{"type":"string","description":"Requested by (display name)"},"requestedDate":{"type":"string","description":"Requested date-time","format":"date-time"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk level"},"approvalStatus":{"type":"string","description":"Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn"},"effectiveDate":{"type":"string","description":"Effective date of the change; empty = on approval","format":"date","nullable":true},"impactedChannels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Impacted channels"},"assignedApprover":{"type":"string","description":"Assigned approver (display name)","nullable":true},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"lifecycleState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Product's current lifecycle state"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27)"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductLink": {"type":"object","x-ticvai-persistence":"catalogue.product_link","description":"**What depends on a product, so a change can be propagated or held** (29 September, data model DM3). ADM-134. `propagatesChanges` says whether an approved change to the source flows to the linked object; `overriddenFields` are the local overrides a propagation must not overwrite (a conflict is reported, not resolved silently).","required":["id","scopePath","sourceProductId","dependencyType","linkedObjectId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"sourceProductId":{"type":"string","format":"uuid"},"dependencyType":{"type":"string","enum":["parentProduct","childProduct","bundle","addOn","upgrade","membership","package","promotion","priceProfile","capacityPool","entitlement","salesChannel","mediaTemplate"]},"linkedObjectId":{"type":"string","format":"uuid"},"linkedObjectName":{"type":"string","maxLength":200,"nullable":true},"propagatesChanges":{"type":"boolean","default":true},"overriddenFields":{"type":"array","items":{"type":"string"}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ProductRetirementSuspensionArchiveView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Retirement, Suspension & Archive displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"action":{"type":"string","enum":["suspendSales","temporarilyDisable","endSale","retire","archive"],"description":"End-of-life action (Available Actions, pack pp.23-24)"},"retirementDate":{"type":"string","description":"Retirement date","format":"date","nullable":true},"endOfSaleDate":{"type":"string","description":"End-of-sale date","format":"date","nullable":true},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels the action applies to; empty = all"},"reason":{"type":"string","description":"Reason"},"replacementProductId":{"type":"string","description":"Replacement product","format":"uuid","nullable":true},"existingReservationTreatment":{"type":"string","enum":["honour","moveToReplacement","cancel"],"description":"Existing reservation treatment; default honour (decided 29 September, readiness close-out)"},"existingTicketTreatment":{"type":"string","enum":["remainValid","exchangeForReplacement","invalidate"],"description":"Existing ticket treatment; default remainValid, and invalidate needs its own governed approval (decided 29 September, readiness close-out)"},"communicationRequirements":{"type":"string","description":"Communication requirements to holders and staff","nullable":true},"reportingTreatment":{"type":"string","enum":["keepInReports","reportUnderReplacement","historicalOnly"],"description":"Reporting treatment; default keepInReports (decided 29 September, readiness close-out)"},"activePromotions":{"type":"integer","description":"Active promotions"},"bundles":{"type":"integer","description":"Bundles"},"membershipBenefits":{"type":"integer","description":"Membership benefits"},"resellerAgreements":{"type":"integer","description":"Reseller agreements"},"futureReservations":{"type":"integer","description":"Future reservations"},"activePriceLists":{"type":"integer","description":"Active price lists"},"channelAssignments":{"type":"integer","description":"Channel assignments"},"productId":{"type":"string","description":"Product id","format":"uuid"},"productName":{"type":"string","description":"Product name"},"lifecycleState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Current lifecycle state"},"upgradePaths":{"type":"integer","description":"Upgrade paths"}}},
"ProductVersion": {"type":"object","x-ticvai-persistence":"catalogue.product_version","description":"1.1.47, 1.4.9 to 1.4.11. **Follows `white-label.ConfigVersion`** — the same pattern for the same reason, and the fourth place this mechanism was asked for.\n","required":["version","publishedAt","publishedByPrincipalId"],"properties":{"version":{"type":"integer"},"productId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"contentHash":{"type":"string","description":"**Lets a diff be cheap and a no-op change be recognised.** Republishing an unchanged product should not create a version.\n"},"restoredFromVersion":{"type":"integer","nullable":true,"description":"Set where this version was created by a restore. **A restore is a new version, not a rewind** — a price that was wrong for three days stays visible, because a finance query run next quarter has to reproduce what was charged.\n"}}},
"RollbackRecoveryManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Rollback & Recovery Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dependencies":{"type":"array","items":{"type":"string"},"description":"Dependencies identified for the rollback"},"reason":{"type":"string","description":"Rollback reason (mandatory)"},"executionMode":{"type":"string","enum":["immediate","scheduled"],"description":"Immediate (where authorised) or scheduled"},"status":{"type":"string","description":"Rollback status: requested, awaitingApproval, scheduled, executing, completed, failed or cancelled"},"scope":{"type":"array","items":{"type":"string","enum":["entireProduct","pricingAssociation","channelAssociation","validityConfiguration","media","policy","entitlementConfiguration"]},"description":"Rollback scope"},"rollbackId":{"type":"string","description":"Rollback id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"productName":{"type":"string","description":"Product name"},"fromVersion":{"type":"integer","description":"Current version rolled back from"},"toVersion":{"type":"integer","description":"Earlier version restored"},"emergency":{"type":"boolean","description":"Emergency rollback"},"scheduledAt":{"type":"string","description":"Scheduled time","format":"date-time","nullable":true},"requestedBy":{"type":"string","description":"Requested by (display name)"},"requestedAt":{"type":"string","description":"Requested","format":"date-time"},"completedAt":{"type":"string","description":"Completed","format":"date-time","nullable":true},"approvalReference":{"type":"string","description":"Approval reference","nullable":true}}}
}
```
