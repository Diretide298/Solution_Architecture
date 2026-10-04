# WS35 — Pricing   Revenue Management board 2

**10 screens · 11 operations · 14 schemas · 1 permissions**

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
  `PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-058` | Pricing Rule Command Center | B | 11 | 26 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-059` | Customer Segment & Profile Pricing Rules | B | 17 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-060` | Membership & Loyalty Pricing Rules | B | 4 | 0 | 5 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-061` | Residency, Nationality & Market Pricing Rules | B | 13 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-062` | Channel-Based Pricing Rules | B | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `ADM-063` | Location, Venue & Event Pricing Rules | B | 6 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-064` | Quantity, Group & Volume Pricing Rules | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-065` | Effective Date, Season & Day-Based Pricing Rules | B | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-066` | Timeslot, Performance & Time-of-Day Pricing Rules | B | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-067` | Pricing Rule Priority, Conflict Resolution & Testing | B | 11 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-062, ADM-064, ADM-066, ADM-067 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-058` Pricing Rule Command Center

**Provide administrators with a centralized workspace for all pricing eligibility and contextual pricing rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29824 (VM-ADM-058) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each rule should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/commercial/pricing-rule-command-center-adm-058` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Customer Segment, Membership, Channel, Quantity, Timeslot, Event, Create Rule, Duplicate …. Each needs an …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All pricing rules (segment, membership, residency, channel, venue and event, quantity, date and season, time slot) with status and conflicts, and a Test Rule on a sample booking.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Customer Segment, Membership, Channel, Quantity, Timeslot, Event, Create Rule, Duplicate …. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Rule type | select | — | Customer segment · Membership · Loyalty · Residency · Nationality · Channel · Location · Quantity · Group · Seasonal · Day of week · Timeslot … | `listPricingRule` ?ruleType |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listPricingRule` ?status |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPricingRule` ?channel |
| Venue location | text field | — | — | `listPricingRule` ?venueLocation |
| Search | text field | — | — | `listPricingRule` ?search |
| Rule type | select | — | Customer segment · Membership · Loyalty · Residency · Nationality · Channel · Location · Quantity · Group · Seasonal · Day of week · Timeslot … | `listPricingRulePriority` ?ruleType |
| Has conflict | toggle | — | — | `listPricingRulePriority` ?hasConflict |
| Customer | text field | — | — | `listPricingRulePriority` ?customerId |
| Membership | text field | — | — | `listPricingRulePriority` ?membershipId |
| Residency | text field | — | pattern `^[A-Z]{2}$` | `listPricingRulePriority` ?residency |
| Product | text field | — | — | `listPricingRulePriority` ?productId |
| Quantity | number field | — | min 1 | `listPricingRulePriority` ?quantity |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPricingRulePriority` ?channel |
| Date | date picker | — | — | `listPricingRulePriority` ?date |
| Time | time picker | — | — | `listPricingRulePriority` ?time |

**Sent by *Test Rule*** (`testPricingRule`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `testPricingRule` body |
| Variant `variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Absent means the product's own venue. | `testPricingRule` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `testPricingRule` body |
| Date `date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | Visit or event date. | `testPricingRule` body |
| Time `time` | time picker | optional | — | — | HH:mm, 24-hour | Visit time or timeslot start, venue local. | `testPricingRule` body |
| Customer segment `customerSegment` | text field | optional | — | — | — | — | `testPricingRule` body |
| Customer `customerId` | picker: choose a customer | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Residency `residency` | text field | optional | — | — | — | — | `testPricingRule` body |
| Quantity `quantity` | number field | optional | 1 | min 1; max 500 | — | — | `testPricingRule` body |

#### Outputs: what the screen shows and produces

**Shown**

**Active Pricing Rules** (metric tile)

**Draft Rules** (metric tile)

**Customer Segment Rules** (metric tile)

**Membership Rules** (metric tile)

**Residency Rules** (metric tile)

**Channel Rules** (metric tile)

**Location Rules** (metric tile)

**Quantity Rules** (metric tile)

**Seasonal Rules** (metric tile)

**Timeslot Rules** (metric tile)

**Rule Conflicts** (metric tile)

**Rules Expiring Soon** (metric tile)

**Every pricing rule** (data table, from `listPricingRule`)

| Shows | Format | Notes |
|---|---|---|
| Rule | text | Rule ID |
| Rule name | text | Rule Name |
| Rule type | chip: Customer segment, Membership, Loyalty, Residency, Nationality, Channel… | Rule Type (the pack's Rule Types list, pp.24-25) |
| Price list | text | Price List: the name of the price list whose rate this rule selects |
| Product scope | text | Product Scope: the products or product categories the rule covers |
| Customer scope | text | Customer Scope: the customer segment, membership or partner the rule covers |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Channel the rule is limited to; empty for all channels |
| Venue location | text | Venue/Location |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Priority | 1,234 | Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins |
| Status | text | Status: draft, active, disabled or expired |
| Owner | text | Owner |

**The selected pricing rule** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Rule | text | Rule ID |
| Rule name | text | Rule Name |
| Rule type | chip: Customer segment, Membership, Loyalty, Residency, Nationality, Channel… | Rule Type (the pack's Rule Types list, pp.24-25) |
| Price list | text | Price List: the name of the price list whose rate this rule selects |
| Product scope | text | Product Scope: the products or product categories the rule covers |
| Customer scope | text | Customer Scope: the customer segment, membership or partner the rule covers |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Channel the rule is limited to; empty for all channels |
| Venue location | text | Venue/Location |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Priority | 1,234 | Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins |
| Status | text | Status: draft, active, disabled or expired |
| Owner | text | Owner |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer Segment (primary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Quantity (secondary button) | navigation or local | — | — | — | — |
| Timeslot (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Create Rule (secondary button) | navigation or local | — | — | — | — |
| Duplicate (secondary button) | navigation or local | — | — | — | — |
| Test Rule (secondary button) | `testPricingRule` POST `/pricing-rule/{ruleId}/test` | PricingRuleTestInput | PricingRuleTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 The sample booking cannot be priced - the product has no price on that date or channel (`noBasePrice`), or the … | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Test rule**: Booking (product, channel, date, time, segment, residency, quantity) in; whether the rule matches, what it does to the price, and why not if it does not. *(source: contracts/spine/catalogue.yaml#testPricingRule / DI-593)*

**Data it reads**: `listPricingRule` (onLoad, Pricing Rule Command Center); `listPricingRulePriority` (onLoad, Pricing Rule Priority, Conflict Resolution & Testing)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-059` Customer Segment & Profile Pricing Rules: *Works in Customer Segment & Profile Pricing Rules*; calls `listPricingRule`
- → `ADM-060` Membership & Loyalty Pricing Rules: *Works in Membership & Loyalty Pricing Rules*; calls `listPricingRule`
- → `ADM-061` Residency, Nationality & Market Pricing Rules: *Works in Residency, Nationality & Market Pricing Rules*; calls `listPricingRule`
- → `ADM-062` Channel-Based Pricing Rules: *Works in Channel-Based Pricing Rules*; calls `listPricingRule`
- → `ADM-063` Location, Venue & Event Pricing Rules: *Works in Location, Venue & Event Pricing Rules*; calls `listPricingRule`
- → `ADM-064` Quantity, Group & Volume Pricing Rules: *Works in Quantity, Group & Volume Pricing Rules*; calls `listPricingRule`
- → `ADM-065` Effective Date, Season & Day-Based Pricing Rules: *Works in Effective Date, Season & Day-Based Pricing Rules*; calls `listPricingRule`
- → `ADM-066` Timeslot, Performance & Time-of-Day Pricing Rules: *Works in Timeslot, Performance & Time-of-Day Pricing Rules*; calls `listPricingRule`
- → `ADM-067` Pricing Rule Priority, Conflict Resolution & Testing: *Works in Pricing Rule Priority, Conflict Resolution & Testing*; carries `ruleId`; calls `listPricingRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing rule list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The sample booking cannot be priced - the product has no price on that date or channel (`noBasePrice`), or the product is not sold at the venue … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- rule: UAE residents 15% weekdays
  type: residency
  status: Active
  conflicts: 1
```

#### Permissions

- `listPricingRule` → `PRODUCT_VIEW` (read) · staff
- `listPricingRulePriority` → `PRODUCT_VIEW` (read) · staff
- `testPricingRule` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-058` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-058`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 1: Opens Pricing Rule Command Center → Provide administrators with a centralized workspace for all pricing eligibility and contextual pricing rules.
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F144 branch at step 1 (expected): when Nothing has been set up on Pricing Rule Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F144 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer Segment, Membership, Channel, Quantity, Timeslot, Event, Create Rule, Duplicate, Test Rule.
- [ ] Every transition is wired: `BO-100`, `ADM-059`, `ADM-060`, `ADM-061`, `ADM-062`, `ADM-063`, `ADM-064`, `ADM-065`, `ADM-066`, `ADM-067`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-059` Customer Segment & Profile Pricing Rules

**Define price eligibility based on customer characteristics and commercial segments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29820 (VM-ADM-059) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-segment-profile-pricing-rules-adm-059` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the customer segment and profile pricing rules that listCustomerSegmentProfile lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Price eligibility by customer characteristics: regular, school, corporate, group and other segments.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Customer Segment & Profile Pricing Rules) declares only reads (listCustomerSegmentProfile). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer Type | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Account Type | select field | — | — | — | — | — | — |
| CRM Segment | select field | — | — | — | — | — | — |
| VIP Status | select field | — | — | — | — | — | — |
| Corporate Customer | select field | — | — | — | — | — | — |
| Employee/Staff | select field | — | — | — | — | — | — |
| Partner Customer | select field | — | — | — | — | — | — |
| Guest/Registered User | select field | — | — | — | — | — | — |
| Rule Name | select field | — | — | — | — | — | — |
| Segment | select field | — | — | — | — | — | — |
| Applicable Products | select field | — | — | — | — | — | — |
| Price List | select field | — | — | — | — | — | — |
| Rate | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Dimension | select | — | Customer type · Customer segment · Account type · Crm segment · Vip status · Corporate customer · Employee staff · Partner customer · Guest registered user | `listCustomerSegmentProfile` ?dimension |
| Segment source | radio group | — | Crm · Membership · B2B partner · Corporate account · Customer profile | `listCustomerSegmentProfile` ?segmentSource |
| Customer | text field | — | — | `listCustomerSegmentProfile` ?customerId |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listCustomerSegmentProfile` ?status |
| Search | text field | — | — | `listCustomerSegmentProfile` ?search |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **segment rules**: Rules as rows (segment, products, adjustment, dates, status) with Edit opening the rule. *(source: contracts/spine/catalogue.yaml#listCustomerSegmentProfile / DI-593)*

**Data it reads**: `listCustomerSegmentProfile` (onLoad, Customer Segment & Profile Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listCustomerSegmentProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer segment profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer segment profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer segment profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  segment: School
  products: Day Pass
  adjustment: -30%
  status: Active
```

#### Permissions

- `listCustomerSegmentProfile` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-059` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-059`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 2: Works in Customer Segment & Profile Pricing Rules → Define price eligibility based on customer characteristics and commercial segments.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-059?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-060` Membership & Loyalty Pricing Rules

**Control member-specific and loyalty-tier pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29821 (VM-ADM-060) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether benefits apply to) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/membership-loyalty-pricing-rules-adm-060` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Customer Status. Each needs an operation, or needs removing from the screen; this is the Phase 3 … Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the membership and loyalty pricing rules that listMembershipLoyaltyPricing lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Member and loyalty-tier pricing: who gets which rate by membership and tier.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Customer Status. (CHG-MOV-008)
- No write operation: a configuration screen (Membership & Loyalty Pricing Rules) declares only reads (listMembershipLoyaltyPricing). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Member Only | select field | — | — | — | — | — | — |
| Member + 1 Guest | text field | — | — | — | — | — | — |
| Member + Family | select field | — | — | — | — | — | — |
| Selected Quantity | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Dimension | select | — | Membership product · Membership status · Membership tier · Annual pass type · Membership level · Loyalty tier · Loyalty program · Points band · Customer status | `listMembershipLoyaltyPricing` ?dimension |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listMembershipLoyaltyPricing` ?status |
| Search | text field | — | — | `listMembershipLoyaltyPricing` ?search |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Membership Product (primary button) | navigation or local | — | — | — | — |
| Membership Status (secondary button) | navigation or local | — | — | — | — |
| Membership Tier (secondary button) | navigation or local | — | — | — | — |
| Membership Level (secondary button) | navigation or local | — | — | — | — |
| Loyalty Tier (secondary button) | navigation or local | — | — | — | — |
| Customer Status (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **member rates**: Tiers as columns, products as rows, rates or adjustments in cells. *(source: contracts/spine/catalogue.yaml#listMembershipLoyaltyPricing)*

**Data it reads**: `listMembershipLoyaltyPricing` (onLoad, Membership & Loyalty Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listMembershipLoyaltyPricing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership loyalty pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership loyalty pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership loyalty pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rates:
  Gold: -20%
  Platinum: -30%
```

#### Permissions

- `listMembershipLoyaltyPricing` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-060` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-060`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 4: Works in Membership & Loyalty Pricing Rules → Control member-specific and loyalty-tier pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-060?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Membership Product, Membership Status, Membership Tier, Membership Level, Loyalty Tier, Customer Status.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-061` Residency, Nationality & Market Pricing Rules

**Support geographically differentiated commercial pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29825 (VM-ADM-061) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure whether eligibility requires) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/residency-nationality-market-pricing-rules-adm-061` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the residency, nationality and market pricing rules that listResidencyNationalityMarket lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Geographic pricing: resident and non-resident, nationality and market rates, with the ID proof a resident rate requires.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Residency, Nationality & Market Pricing Rules) declares only reads (listResidencyNationalityMarket). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Residency | select field | — | — | — | — | — | — |
| Nationality | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Region | select field | — | — | — | — | — | — |
| Customer Address | select field | — | — | — | — | — | — |
| Verified ID | select field | — | — | — | — | — | — |
| Government ID Integration where applicable | text field | — | — | — | — | — | — |
| Customer Declaration | select field | — | — | — | — | — | — |
| Account Profile | select field | — | — | — | — | — | — |
| ID Upload | select field | — | — | — | — | — | — |
| Government/Identity Verification | select field | — | — | — | — | — | — |
| Staff Verification | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Eligibility basis | select | — | Residency · Nationality · Country · Market · Region · Customer address · Verified ID · Government ID | `listResidencyNationalityMarket` ?eligibilityBasis |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listResidencyNationalityMarket` ?status |
| Search | text field | — | — | `listResidencyNationalityMarket` ?search |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **residency rules**: Each rule with the proof required (Emirates ID) shown, because the gate checks it. *(source: contracts/spine/catalogue.yaml#listResidencyNationalityMarket / DI-463 / DI-443)*

**Data it reads**: `listResidencyNationalityMarket` (onLoad, Residency, Nationality & Market Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listResidencyNationalityMarket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The residency nationality market configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the residency nationality market untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No residency nationality market configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: UAE resident
  proof: Emirates ID
  adjustment: AED 45.00 off Day Pass
```

#### Permissions

- `listResidencyNationalityMarket` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-061` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-061`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 6: Works in Residency, Nationality & Market Pricing Rules → Support geographically differentiated commercial pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-061?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-062` Channel-Based Pricing Rules

**Determine which commercial rate applies based on sales channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29944 (VM-ADM-062) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-based-pricing-rules-adm-062` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the channel-based pricing rules that listChannelBasedPricing lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which rate applies by sales channel (online cheaper than at the counter, kiosk in between).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Channel-Based Pricing Rules) declares only reads (listChannelBasedPricing). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listChannelBasedPricing` ?channel |
| Product | text field | — | — | `listChannelBasedPricing` ?product |
| Is override | toggle | — | — | `listChannelBasedPricing` ?isOverride |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listChannelBasedPricing` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel matrix**: Channels as columns using the vocabulary labels, rates in cells. *(source: contracts/spine/catalogue.yaml#listChannelBasedPricing / DI-580 / DI-582)*

**Data it reads**: `listChannelBasedPricing` (onLoad, Channel-Based Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listChannelBasedPricing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel-based pricing rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel-based pricing rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel-based pricing rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel-based pricing rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  product: Day Pass Adult
  Website: AED 295.00
  Point of sale: AED 310.00
  Kiosk: AED 299.00
```

#### Permissions

- `listChannelBasedPricing` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*
- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*
- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-062` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-062`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 8: Works in Channel-Based Pricing Rules → Determine which commercial rate applies based on sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-063` Location, Venue & Event Pricing Rules

**Allow rates to vary according to where and for which event/experience the product is sold.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29822 (VM-ADM-063) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/location-venue-event-pricing-rules-adm-063` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Attraction, Zone, Experience, Pop-up Venue, Temporary Event Location. Each needs an operation, or needs … Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the location, venue and event pricing rules that listLocationVenueEvent lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rates that vary by location, venue and event.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Attraction, Zone, Experience, Pop-up Venue, Temporary Event Location. (CHG-MOV-008)
- No write operation: a configuration screen (Location, Venue & Event Pricing Rules) declares only reads (listLocationVenueEvent). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Rate | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Context level | select | — | Country · City · Venue · Attraction · Location · Event · Performance · Zone · Experience | `listLocationVenueEvent` ?contextLevel |
| Context ref | text field | — | — | `listLocationVenueEvent` ?contextRefId |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listLocationVenueEvent` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Zone (secondary button) | navigation or local | — | — | — | — |
| Experience (secondary button) | navigation or local | — | — | — | — |
| Pop-up Venue (secondary button) | navigation or local | — | — | — | — |
| Temporary Event Location (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **location rules**: Rules grouped by venue then event. *(source: contracts/spine/catalogue.yaml#listLocationVenueEvent)*

**Data it reads**: `listLocationVenueEvent` (onLoad, Location, Venue & Event Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listLocationVenueEvent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The location venue event configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the location venue event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No location venue event configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  venue: Coastal Aqua
  event: Night Swim Fridays
  rate: AED 99.00
```

#### Permissions

- `listLocationVenueEvent` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-063` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-063`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 10: Works in Location, Venue & Event Pricing Rules → Allow rates to vary according to where and for which event/experience the product is sold.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-063?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Attraction, Event, Zone, Experience, Pop-up Venue, Temporary Event Location.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-064` Quantity, Group & Volume Pricing Rules

**Support commercial rates based on purchased quantity or group size.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29826 (VM-ADM-064) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/quantity-group-volume-pricing-rules-adm-064` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Minimum Quantity. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rates by quantity or group size: volume bands applied automatically (up to 1,000 tickets, 1,000 to 5,000, above 5,000).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Minimum Quantity. (CHG-MOV-008)
- No write operation: a configuration screen (Quantity, Group & Volume Pricing Rules) declares only reads (listQuantityGroupVolume). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Quantity model | select | — | Minimum quantity · Quantity bands · Group size · Volume threshold · Buy x rate · Per person group rate | `listQuantityGroupVolume` ?quantityModel |
| Group type | select | — | School · Corporate · Tour · Family · B2B · Custom | `listQuantityGroupVolume` ?groupType |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listQuantityGroupVolume` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Minimum Quantity (primary button) | navigation or local | — | — | — | — |
| Quantity Bands (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **bands**: Non-overlapping bands with the rate per band. *(source: contracts/spine/catalogue.yaml#listQuantityGroupVolume / DI-594)*

**Data it reads**: `listQuantityGroupVolume` (onLoad, Quantity, Group & Volume Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listQuantityGroupVolume`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quantity group volume list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quantity group volume untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quantity group volume yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quantity group volume are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bands:
- '1-999: base'
- '1,000-4,999: -8%'
- '5,000+: -12%'
```

#### Permissions

- `listQuantityGroupVolume` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-064` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-064`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 12: Works in Quantity, Group & Volume Pricing Rules → Support commercial rates based on purchased quantity or group size.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Minimum Quantity, Quantity Bands.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-065` Effective Date, Season & Day-Based Pricing Rules

**Control commercial price selection over time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29823 (VM-ADM-065) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/effective-date-season-day-based-pricing-rules-adm-065` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the effective date, season and day-based pricing rules that listEffectiveDateSeason lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Price selection over time: effective dates, seasons (low season to 30 September, high season from 1 October), days of the week.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Effective Date, Season & Day-Based Pricing Rules) declares only reads (listEffectiveDateSeason). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Sales Start | select field | — | — | — | — | — | — |
| Sales End | select field | — | — | — | — | — | — |
| Visit Date Range | select field | — | — | — | — | — | — |
| Season | select field | — | — | — | — | — | — |
| Holiday Period | select field | — | — | — | — | — | — |
| Event Period | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date rule type | select | — | Effective period · Season · Day of week · Holiday period · Event period · Public holiday · School holiday · Special date · Blackout date · Peak date | `listEffectiveDateSeason` ?dateRuleType |
| Visit from | date picker | — | — | `listEffectiveDateSeason` ?visitFrom |
| Visit to | date picker | — | — | `listEffectiveDateSeason` ?visitTo |
| Product | text field | — | — | `listEffectiveDateSeason` ?product |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listEffectiveDateSeason` ?status |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **season calendar**: Seasons on a year bar; day-of-week rules beneath. *(source: contracts/spine/catalogue.yaml#listEffectiveDateSeason / DI-594)*

**Data it reads**: `listEffectiveDateSeason` (onLoad, Effective Date, Season & Day-Based Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listEffectiveDateSeason`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The effective date season configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the effective date season untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No effective date season configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
seasons:
- name: Low
  to: '2026-09-30'
- name: High
  from: '2026-10-01'
```

#### Permissions

- `listEffectiveDateSeason` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-065` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-065`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 14: Works in Effective Date, Season & Day-Based Pricing Rules → Control commercial price selection over time.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-065?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-066` Timeslot, Performance & Time-of-Day Pricing Rules

**Allow commercial pricing to differ across times within the same day or event.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29827 (VM-ADM-066) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/timeslot-performance-time-of-day-pricing-rules-adm-066` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for the timeslot, performance and time-of-day pricing rules that listTimeslotPerformanceTime lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Prices that differ across times of the same day or event: time slots, performances, time of day.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Timeslot, Performance & Time-of-Day Pricing Rules) declares only reads (listTimeslotPerformanceTime). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Event | text field | — | — | `listTimeslotPerformanceTime` ?event |
| Time of day band | radio group | — | Peak · Standard · Off peak · Late entry · Early entry | `listTimeslotPerformanceTime` ?timeOfDayBand |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listTimeslotPerformanceTime` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every timeslot performance time-of-day** (data table, from `listTimeslotPerformanceTime`)

| Shows | Format | Notes |
|---|---|---|
| Validation issues | list or chips (count when long) | Validation (p.34) |

**The selected timeslot performance time-of-day** (detail panel): The pack groups this record's detail under its own headings: “Supported Contexts”, “Museum Admission”, “Concert”.

| Shows | Format | Notes |
|---|---|---|
| Validation issues | list or chips (count when long) | Validation (p.34) |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **time bands**: A day timeline with rates per band. *(source: contracts/spine/catalogue.yaml#listTimeslotPerformanceTime / DI-594)*

**Data it reads**: `listTimeslotPerformanceTime` (onLoad, Timeslot, Performance & Time-of-Day Pricing Rules)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Returns to the board's landing screen*; carries `ruleId`; calls `listTimeslotPerformanceTime`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The timeslot performance time-of-day list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the timeslot performance time-of-day untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No timeslot performance time-of-day yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the timeslot performance time-of-day are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bands:
- '10:00-14:00: base'
- '18:00-22:00: +AED 30.00'
```

#### Permissions

- `listTimeslotPerformanceTime` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-066` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-066`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 16: Works in Timeslot, Performance & Time-of-Day Pricing Rules → Allow commercial pricing to differ across times within the same day or event.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-058`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-067` Pricing Rule Priority, Conflict Resolution & Testing

**Define how TICVAI decides the final applicable rate when multiple pricing rules match. This is the critical control screen for Board 2. Board 1 established what commercial prices exist. Board 2 determines which commercial rate applies to a transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29828 (VM-ADM-067) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify; Show) and no metric row |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/commercial/pricing-rule-priority-conflict-resolution-testing-adm-067` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write that orders static pricing rule priority (setRulePriorityConflict covers dynamic rules only).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How the final rate is decided when several pricing rules match, with a test on a sample booking. The configured hierarchy decides; there is no lowest-price default.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The screen lists priorities but declares no operation to reorder them; setRulePriorityConflict exists for dynamic rules only. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Rule type | select | — | Customer segment · Membership · Loyalty · Residency · Nationality · Channel · Location · Quantity · Group · Seasonal · Day of week · Timeslot … | `listPricingRulePriority` ?ruleType |
| Has conflict | toggle | — | — | `listPricingRulePriority` ?hasConflict |
| Customer | text field | — | — | `listPricingRulePriority` ?customerId |
| Membership | text field | — | — | `listPricingRulePriority` ?membershipId |
| Residency | text field | — | pattern `^[A-Z]{2}$` | `listPricingRulePriority` ?residency |
| Product | text field | — | — | `listPricingRulePriority` ?productId |
| Quantity | number field | — | min 1 | `listPricingRulePriority` ?quantity |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPricingRulePriority` ?channel |
| Date | date picker | — | — | `listPricingRulePriority` ?date |
| Time | time picker | — | — | `listPricingRulePriority` ?time |
| Rule type | select | — | Customer segment · Membership · Loyalty · Residency · Nationality · Channel · Location · Quantity · Group · Seasonal · Day of week · Timeslot … | `listPricingRule` ?ruleType |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listPricingRule` ?status |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPricingRule` ?channel |
| Venue location | text field | — | — | `listPricingRule` ?venueLocation |
| Search | text field | — | — | `listPricingRule` ?search |

**Sent by *Test Rule*** (`testPricingRule`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `testPricingRule` body |
| Variant `variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Absent means the product's own venue. | `testPricingRule` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `testPricingRule` body |
| Date `date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | Visit or event date. | `testPricingRule` body |
| Time `time` | time picker | optional | — | — | HH:mm, 24-hour | Visit time or timeslot start, venue local. | `testPricingRule` body |
| Customer segment `customerSegment` | text field | optional | — | — | — | — | `testPricingRule` body |
| Customer `customerId` | picker: choose a customer | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | — | `testPricingRule` body |
| Residency `residency` | text field | optional | — | — | — | — | `testPricingRule` body |
| Quantity `quantity` | number field | optional | 1 | min 1; max 500 | — | — | `testPricingRule` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing rule priority** (data table, from `listPricingRulePriority`)

| Shows | Format | Notes |
|---|---|---|
| Validation issues | list or chips (count when long) | Conflict Detection (p.35) |

**The selected pricing rule priority** (detail panel): The pack groups this record's detail under its own headings: “Standard Rate”, “Inputs”, “Input”, “Candidate Rates”, “Resolved Rate”, “Reason”.

| Shows | Format | Notes |
|---|---|---|
| Validation issues | list or chips (count when long) | Conflict Detection (p.35) |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Test Rule (primary button) | `testPricingRule` POST `/pricing-rule/{ruleId}/test` | PricingRuleTestInput | PricingRuleTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 The sample booking cannot be priced - the product has no price on that date or channel (`noBasePrice`), or the … | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **priority list and test**: Same priority list and test console as BO-441, for static pricing rules. *(source: contracts/spine/catalogue.yaml#listPricingRulePriority / contracts/spine/catalogue.yaml#testPricingRule / DI-595)*

**Data it reads**: `listPricingRulePriority` (onLoad, Pricing Rule Priority, Conflict Resolution & Testing); `listPricingRule` (onLoad, The pricing rules to pick one to test)

**Where the user goes next**

- → `ADM-058` Pricing Rule Command Center: *Pricing Rule Command Center*; carries `ruleId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing rule priority list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing rule priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing rule priority yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing rule priority are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The sample booking cannot be priced - the product has no price on that date or channel (`noBasePrice`), or the product is not sold at the venue … |

#### Consistency with other screens

- Match `BO-441`: Same component for rule order and test.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  booking: School group, 40 pupils, Day Pass, Tue 18 Nov
  matched:
  - School -30%
  - Weekday -10%
  applied: School -30% (priority 1, stop processing)
```

#### Permissions

- `listPricingRulePriority` → `PRODUCT_VIEW` (read) · staff
- `listPricingRule` → `PRODUCT_VIEW` (read) · staff
- `testPricingRule` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- When several rules apply to one sale (e.g. summer rate plus school-group discount) the configurable pricing hierarchy decides; there is no automatic lowest-price-wins default. *(agreed · MoM 1 Sep 2026, 4.4 Seasonal & Date-Based Pricing; Rule Priority · DI-595)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-067` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-067`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 2
- Flow F144 *Pricing Revenue Management board 2: Pricing Rule Command Center*, step 18: Works in Pricing Rule Priority, Conflict Resolution & Testing → Define how TICVAI decides the final applicable rate when multiple pricing rules match. This is the critical control screen for Board 2. Board 1 established what commercial prices exist. Board 2 …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Test Rule.
- [ ] Every transition is wired: `ADM-058`.
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

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listChannelBasedPricing": {"method":"GET","path":"/channel-based-pricing","contract":"catalogue","summary":"Channel-Based Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"isOverride","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerSegmentProfile": {"method":"GET","path":"/customer-segment-profile","contract":"catalogue","summary":"Customer Segment & Profile Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dimension","in":"query","required":false},{"name":"segmentSource","in":"query","required":false},{"name":"customerId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEffectiveDateSeason": {"method":"GET","path":"/effective-date-season","contract":"catalogue","summary":"Effective Date, Season & Day-Based Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dateRuleType","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLocationVenueEvent": {"method":"GET","path":"/location-venue-event","contract":"catalogue","summary":"Location, Venue & Event Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"contextLevel","in":"query","required":false},{"name":"contextRefId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipLoyaltyPricing": {"method":"GET","path":"/membership-loyalty-pricing","contract":"catalogue","summary":"Membership & Loyalty Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dimension","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingRule": {"method":"GET","path":"/pricing-rule","contract":"catalogue","summary":"Pricing Rule Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ruleType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"venueLocation","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPricingRulePriority": {"method":"GET","path":"/pricing-rule-priority","contract":"catalogue","summary":"Pricing Rule Priority, Conflict Resolution & Testing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ruleType","in":"query","required":false},{"name":"hasConflict","in":"query","required":false},{"name":"customerId","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":"residency","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"quantity","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"time","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQuantityGroupVolume": {"method":"GET","path":"/quantity-group-volume","contract":"catalogue","summary":"Quantity, Group & Volume Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"quantityModel","in":"query","required":false},{"name":"groupType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResidencyNationalityMarket": {"method":"GET","path":"/residency-nationality-market","contract":"catalogue","summary":"Residency, Nationality & Market Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"eligibilityBasis","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTimeslotPerformanceTime": {"method":"GET","path":"/timeslot-performance-time","contract":"catalogue","summary":"Timeslot, Performance & Time-of-Day Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"event","in":"query","required":false},{"name":"timeOfDayBand","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"testPricingRule": {"method":"POST","path":"/pricing-rule/{ruleId}/test","contract":"catalogue","summary":"Test one pricing rule against a sample booking, on demand","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":"PricingRuleTestInput","responds":"PricingRuleTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ChannelBasedPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel-Based Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel (Supported Channels, p.29)"},"product":{"type":"string","description":"Product"},"priceList":{"type":"string","description":"Price List"},"rate":{"type":"string","description":"Rate: code of the rate, e.g. Trade Adult"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"isOverride":{"type":"boolean","description":"Channel Override (pp.29-30): a controlled, time-boxed override of the channel's normal rate"},"overrideReason":{"type":"string","nullable":true,"description":"Reason, required for an override"},"fallbackRate":{"type":"string","nullable":true,"description":"Fallback Rate once the override ends"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"}}},
"CustomerSegmentProfilePricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Customer Segment & Profile Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleName":{"type":"string","description":"Rule Name"},"segment":{"type":"string","description":"Segment: the value the dimension must equal, e.g. VIP"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Applicable Products: product ids or product category codes"},"priceList":{"type":"string","description":"Price List: the list whose rate the rule selects"},"rate":{"type":"string","description":"Rate: code of the rate used when the rule matches, e.g. VIP Adult"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"ruleId":{"type":"string","description":"Rule ID"},"dimension":{"type":"string","enum":["customerType","customerSegment","accountType","crmSegment","vipStatus","corporateCustomer","employeeStaff","partnerCustomer","guestRegisteredUser"],"description":"Supported Dimension (p.25) the rule tests"},"segmentSource":{"type":"string","enum":["crm","membership","b2bPartner","corporateAccount","customerProfile"],"description":"Customer Segment Source (p.26) the segment is read from"},"fallbackRate":{"type":"string","description":"Fallback (p.26): rate used when the customer no longer qualifies; the standard rate by default (decided 29 September, readiness close-out)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"EffectiveDateSeasonDayBasedPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Effective Date, Season & Day-Based Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"salesStart":{"type":"string","format":"date-time","nullable":true,"description":"Sales Start: purchases from this moment get the rule"},"salesEnd":{"type":"string","format":"date-time","nullable":true,"description":"Sales End"},"season":{"type":"string","nullable":true,"description":"Season name, e.g. Low, Regular, Peak (Seasonal Pricing, p.33)"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"dateRuleType":{"type":"string","enum":["effectivePeriod","season","dayOfWeek","holidayPeriod","eventPeriod","publicHoliday","schoolHoliday","specialDate","blackoutDate","peakDate"],"description":"Kind of date rule (Effective Dating and Calendar Rules, pp.32-33)"},"visitFrom":{"type":"string","format":"date","description":"Visit Date Range start","nullable":true},"visitTo":{"type":"string","format":"date","description":"Visit Date Range end","nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Day-of-Week Pricing (p.33); empty for every day"},"specificDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Special, blackout, peak or holiday dates the rule covers"},"product":{"type":"string","description":"Product"},"priceList":{"type":"string","description":"Price List"},"rate":{"type":"string","description":"Rate code"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"validationIssues":{"type":"array","description":"Overlap Detection (p.33), e.g. Peak Season and Public Holiday overlap with different rates","items":{"type":"object","properties":{"code":{"type":"string","enum":["overlappingRules"]},"message":{"type":"string"}}}}}},
"LocationVenueEventPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Location, Venue & Event Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"rate":{"type":"string","description":"Rate: code of the rate used in this context"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"contextLevel":{"type":"string","enum":["country","city","venue","attraction","location","event","performance","zone","experience"],"description":"Pricing Context (p.30) the rule is keyed on"},"contextRefId":{"type":"string","description":"The country, city, venue, attraction, location, event, performance, zone or experience"},"temporaryLocationType":{"type":"string","enum":["popUpVenue","exhibition","seasonalSite","temporaryEventLocation"],"description":"Temporary Location Pricing (p.30); empty for a permanent location","nullable":true},"priceList":{"type":"string","description":"Price List"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, disabled or expired"}}},
"MembershipLoyaltyPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Membership & Loyalty Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"conditions":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["membershipProduct","membershipStatus","membershipTier","annualPassType","membershipLevel","loyaltyTier","loyaltyProgram","pointsBand","customerStatus"]},"value":{"type":"string","description":"e.g. active, Gold, Platinum"}}},"description":"Conditions, all of which must hold (Membership = Active AND Tier = Gold)"},"priceList":{"type":"string","description":"Price List"},"rate":{"type":"string","description":"Rate: code of the rate used when the rule matches, e.g. Gold Member Rate"},"benefitScope":{"type":"string","enum":["memberOnly","memberPlusOneGuest","memberPlusFamily","selectedQuantity"],"description":"Member + Guest Rules (p.27): who in the booking receives the member rate"},"benefitQuantity":{"type":"integer","nullable":true,"description":"Number of tickets at the member rate when benefitScope is selectedQuantity"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"validationIssues":{"type":"array","description":"Validation (p.27)","items":{"type":"object","properties":{"code":{"type":"string","enum":["inactiveMembership","expiredMembership","missingTierRate","conflictingLoyaltyMemberRates"]},"message":{"type":"string"}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PricingRuleCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Pricing Rule Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activePricingRules":{"type":"integer","description":"Active Pricing Rules"},"draftRules":{"type":"integer","description":"Draft Rules"},"customerSegmentRules":{"type":"integer","description":"Customer Segment Rules"},"membershipRules":{"type":"integer","description":"Membership Rules"},"residencyRules":{"type":"integer","description":"Residency Rules"},"channelRules":{"type":"integer","description":"Channel Rules"},"locationRules":{"type":"integer","description":"Location Rules"},"quantityRules":{"type":"integer","description":"Quantity Rules"},"seasonalRules":{"type":"integer","description":"Seasonal Rules"},"timeslotRules":{"type":"integer","description":"Timeslot Rules"},"ruleConflicts":{"type":"integer","description":"Rule Conflicts"},"rulesExpiringSoon":{"type":"integer","description":"Rules Expiring Soon: active rules whose effective-to date falls within the next 30 days (decided 29 September, readiness close-out)"}}},
"PricingRuleCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Rule Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"ruleType":{"type":"string","enum":["customerSegment","membership","loyalty","residency","nationality","channel","location","quantity","group","seasonal","dayOfWeek","timeslot","event","corporateB2b","custom"],"description":"Rule Type (the pack's Rule Types list, pp.24-25)"},"priceList":{"type":"string","description":"Price List: the name of the price list whose rate this rule selects"},"productScope":{"type":"string","description":"Product Scope: the products or product categories the rule covers"},"customerScope":{"type":"string","description":"Customer Scope: the customer segment, membership or partner the rule covers"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel the rule is limited to; empty for all channels"},"venueLocation":{"type":"string","description":"Venue/Location"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","nullable":true,"description":"Effective To; empty for open-ended"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"owner":{"type":"string","description":"Owner"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Capability (p.25): e.g. three rules may return different prices for the same Adult ticket on Saturday through B2C; advisory"}}},
"PricingRulePriorityConflictResolutionTestingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Rule Priority, Conflict Resolution & Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"specificity":{"type":"integer","description":"Specificity: number of conditions the rule tests; breaks ties within a priority"},"fallbackBehavior":{"type":"string","enum":["useStandardRate","useNextMatchingRule","blockSale"],"description":"Fallback Behavior when the rule matches but its rate is unavailable"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"ruleType":{"type":"string","enum":["customerSegment","membership","loyalty","residency","nationality","channel","location","quantity","group","seasonal","dayOfWeek","timeslot","event","corporateB2b","custom"],"description":"Rule Type"},"hierarchyLevel":{"type":"string","enum":["contractPartner","customerMember","eventPerformance","venueLocation","channel","quantityGroup","seasonDate","standardRate"],"description":"Rule Resolution level (p.35): Contract/Partner -> Customer/Member -> Event/Performance -> Venue/Location -> Channel -> Quantity/Group -> Season/Date -> Standard Rate; the order is configurable"},"onMatch":{"type":"string","enum":["stopProcessing","continueProcessing"],"description":"Stop or Continue Processing once this rule matches"},"overrideAllowed":{"type":"boolean","description":"Override Allowed"},"validationIssues":{"type":"array","description":"Conflict Detection (p.35)","items":{"type":"object","properties":{"code":{"type":"string","enum":["samePriorityMatches","contradictoryRates","circularFallback","unreachableRule","missingFallback","overlappingTimeDateConditions"]},"message":{"type":"string"}}}},"simulationOutcome":{"type":"string","enum":["selected","matched","rejected","notMatched"],"description":"Pricing Rule Simulator result for this rule; empty when no simulator parameters were sent","nullable":true},"candidateRate":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Candidate rate the rule would give in the simulated context (Gold Member - AED 190)"},"outcomeReason":{"type":"string","nullable":true,"description":"Why it was selected or rejected, e.g. member pricing priority exceeds resident, day and standard pricing"}}},
"PricingRuleTestInput": {"type":"object","x-ticvai-persistence":"none — request only; a dry run stores nothing","description":"The sample booking `testPricingRule` prices (decided 29 September, readiness close-out). The inputs are the ones `listPricingRulePriority` filters its test rows by.","required":["productId","channel","date"],"properties":{"productId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Absent means the product's own venue."},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"date":{"type":"string","format":"date","description":"Visit or event date."},"time":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Visit time or timeslot start, venue local."},"customerSegment":{"type":"string","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"membershipId":{"type":"string","format":"uuid","nullable":true},"residency":{"type":"string","nullable":true},"quantity":{"type":"integer","minimum":1,"maximum":500,"default":1}}},
"PricingRuleTestResult": {"type":"object","x-ticvai-persistence":"none — response only; a dry run stores nothing","description":"What `testPricingRule` returns. `matched` answers the question the button asks; the rest is the calculation the checkout would run.","required":["ruleId","matched","basePrice","finalPrice"],"properties":{"ruleId":{"type":"string"},"matched":{"type":"boolean","description":"Whether the tested rule's conditions match the sample booking."},"notMatchedReasons":{"type":"array","description":"The conditions that failed when `matched` is false, e.g. `channel not in rule`.","items":{"type":"string"}},"appliedByPriority":{"type":"boolean","description":"Matched and actually applied after priority and conflict resolution; a matching rule can still lose to a higher-priority one."},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"finalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"rulesApplied":{"type":"array","items":{"type":"object","properties":{"ruleId":{"type":"string"},"ruleName":{"type":"string"},"priority":{"type":"integer"},"adjustment":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"applied":{"type":"boolean"}}}},"calculationPath":{"type":"array","description":"Each step from base price to final price, in order, in words.","items":{"type":"string"}},"testedAt":{"type":"string","format":"date-time"}}},
"QuantityGroupVolumePricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Quantity, Group & Volume Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupMinimum":{"type":"integer","nullable":true,"description":"Group Minimum: smallest party the group rate applies to"},"maximumGroupSize":{"type":"integer","nullable":true,"description":"Maximum Group Size"},"groupType":{"type":"string","enum":["school","corporate","tour","family","b2b","custom"],"description":"Group Type (p.31)","nullable":true},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"quantityModel":{"type":"string","enum":["minimumQuantity","quantityBands","groupSize","volumeThreshold","buyXRate","perPersonGroupRate"],"description":"Quantity Model (p.31)"},"product":{"type":"string","description":"Product or product family the rule covers"},"priceList":{"type":"string","description":"Price List"},"bands":{"type":"array","items":{"type":"object","properties":{"minQuantity":{"type":"integer"},"maxQuantity":{"type":"integer","nullable":true},"rate":{"type":"string","description":"Rate code for the band"}}},"description":"Tiered Rate Matrix (p.32): 1-9, 10-24, 25-49, 50+ each with its rate; the last band has no maximum"},"quantityBasis":{"type":"string","enum":["perProduct","perProductFamily","perOrder","perGroupBooking","cumulativePartnerVolume"],"description":"Mixed Products (p.32): what quantity is counted; cumulativePartnerVolume counts a partner's sales over its agreement period (MoM 1 Sep §4.3)"},"complimentary":{"type":"object","nullable":true,"description":"Complimentary Logic (p.32): freeQuantity complimentary per paidQuantity paid; empty for none","properties":{"freeQuantity":{"type":"integer"},"paidQuantity":{"type":"integer"},"label":{"type":"string","description":"e.g. coordinator"}}},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, disabled or expired"}}},
"ResidencyNationalityMarketPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Residency, Nationality & Market Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"marketLabel":{"type":"string","description":"Market pricing label, e.g. UAE Resident, GCC Resident, International Visitor"},"eligibilityBasis":{"type":"string","enum":["residency","nationality","country","market","region","customerAddress","verifiedId","governmentId"],"description":"Eligibility Input (pp.27-28) the rule tests"},"eligibleValues":{"type":"array","items":{"type":"string"},"description":"Values that qualify, e.g. ISO country codes AE, SA, or market codes"},"verificationRequired":{"type":"array","items":{"type":"string","enum":["customerDeclaration","accountProfile","idUpload","governmentIdentityVerification","staffVerification"]},"description":"Verification Requirements (p.28) that must be satisfied; empty means none"},"priceList":{"type":"string","description":"Price List"},"rate":{"type":"string","description":"Rate used when eligible, e.g. UAE Resident Adult"},"fallbackRate":{"type":"string","description":"Fallback (p.28): rate used when eligibility cannot be verified; the Non-Resident rate by default (decided 29 September, readiness close-out)"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, disabled or expired"}}},
"TimeslotPerformanceTimeOfDayPricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Timeslot, Performance & Time-of-Day Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"timeslot":{"type":"string","nullable":true,"description":"Timeslot the rule is limited to; empty for any"},"performance":{"type":"string","nullable":true,"description":"Performance the rule is limited to (Matinee, Evening, Final Performance); empty for any"},"timeOfDayBand":{"type":"string","enum":["peak","standard","offPeak","lateEntry","earlyEntry"],"description":"Time-of-Day Band (Peak/Off-Peak, p.34)","nullable":true},"product":{"type":"string","description":"Product"},"event":{"type":"string","nullable":true,"description":"Event"},"priceList":{"type":"string","description":"Price List"},"rate":{"type":"string","description":"Rate code"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"timeBasis":{"type":"string","enum":["timeslotStart","performanceStart","arrivalWindow"],"description":"Which time the range is tested against (Supported Contexts, p.33)"},"timeFrom":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Time Range start, local HH:mm (09:00)"},"timeTo":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Time Range end, local HH:mm, exclusive (12:00)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"validationIssues":{"type":"array","description":"Validation (p.34)","items":{"type":"object","properties":{"code":{"type":"string","enum":["overlappingTimeRanges","missingTimeslotRate","conflictingPerformanceRule"]},"message":{"type":"string"}}}}}}
}
```
