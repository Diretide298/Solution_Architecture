# WS46 — Promotions   Bundles Management board 2

**10 screens · 11 operations · 13 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-148` | Promotion Rule Builder | B–D | 0 | 0 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-149` | Percentage & Fixed Discount Configurator | B | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-150` | Cart & Transaction Threshold Rules | B | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-151` | Volume, Bulk & Tier Discount Configurator | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-152` | Time-Based & Seasonal Discount Rules | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-153` | Customer, Membership & Segment Discount Rules | B | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-154` | Payment Method, Bank & Partner Discount Rules | B | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-155` | Special Price & Guest Offer Configurator | B | 12 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-156` | Discount Limits, Guardrails & Commercial Controls | B | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-157` | Rule Test, Simulation & AI Recommendation Workspace | B–D | 15 | 0 | 6 | 18 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-148, ADM-150, ADM-151, ADM-152, ADM-153 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-148` Promotion Rule Builder

**Provide the main no-code workspace for creating the commercial logic behind a promotion. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/promotions-coupons/promotion-rule-builder-adm-148` |

**What the spec says about it.** **Its own writer is retired in r2** (decided 2 October 2026, Chinmay: "13 dupes would be gone in r2"; CHG-CLN-001). `setPromotionRule` duplicated BO-010 Promotions & Coupons's createPromotion and updatePromotion, so it is removed from the contract (BC-011) and BO-010 saves this record. This id stays the anchor of its section of BO-010: nothing on it writes separately. **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Nested condition groups. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The no-code workspace for a promotion's logic: conditions (nested groups), outcomes (percentage, fixed off, fixed price, free product or ticket, added value, voucher, reward entitlement) and rule ordering, plus which promotions may stack.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Nested condition groups. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): setPromotionRule types promotion, owner, venue, freeProduct, freeTicket, nested groups and priority as strings, and duplicates … (CHG-CLN-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **outcome**: One outcome kind at a time with its own inputs; "multiple outcomes" adds a second outcome block rather than more fields. *(source: contracts/satellite/promotions.yaml#/components/schemas/PromotionRuleBuilderInput)*
- **stacking rule**: Scope (transaction, product, category, ticket, bundle component, customer, channel) and model (fully stackable, non-stackable, conditional, category, at most N); "can A stack with B" as a matrix of promotion types. *(source: contracts/satellite/promotions.yaml#setPromotionStackingRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Nested condition groups (primary button) | navigation or local | — | — | — | — |
| Rule ordering (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-149` Percentage & Fixed Discount Configurator: *Works in Percentage & Fixed Discount Configurator*
- → `ADM-150` Cart & Transaction Threshold Rules: *Works in Cart & Transaction Threshold Rules*
- → `ADM-151` Volume, Bulk & Tier Discount Configurator: *Works in Volume, Bulk & Tier Discount Configurator*
- → `ADM-152` Time-Based & Seasonal Discount Rules: *Works in Time-Based & Seasonal Discount Rules*
- → `ADM-153` Customer, Membership & Segment Discount Rules: *Works in Customer, Membership & Segment Discount Rules*
- → `ADM-154` Payment Method, Bank & Partner Discount Rules: *Works in Payment Method, Bank & Partner Discount Rules*
- → `ADM-155` Special Price & Guest Offer Configurator: *Works in Special Price & Guest Offer Configurator*
- → `ADM-156` Discount Limits, Guardrails & Commercial Controls: *Works in Discount Limits, Guardrails & Commercial Controls*
- → `ADM-157` Rule Test, Simulation & AI Recommendation Workspace: *Works in Rule Test, Simulation & AI Recommendation Workspace*
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-010`: Same states, stacking vocabulary and conflict panel as the venue's promotions desk.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Spend AED 500 get a free fast track
  condition: basket >= AED 500 AND channel in (Website, App)
  outcome: free Fast Track Express x1
  priority: 3
```

#### Permissions

- `setPromotionStackingRule` → `PRICE_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-148` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-148`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 1: Opens Promotion Rule Builder, a section of BO-010, which saves the record with createPromotion and updatePromotion … → Provide the main no-code workspace for creating the commercial logic behind a promotion.
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F155 branch at step 1 (expected): when Nothing has been set up on Promotion Rule Builder yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F155 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-148?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Nested condition groups, Rule ordering.
- [ ] Every transition is wired: `BO-100`, `ADM-149`, `ADM-150`, `ADM-151`, `ADM-152`, `ADM-153`, `ADM-154`, `ADM-155`, `ADM-156`, `ADM-157`, `BO-010`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-149` Percentage & Fixed Discount Configurator

**Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29956 (VM-ADM-149) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/percentage-fixed-discount-configurator-adm-149` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Percentage & Fixed Discount Configurator declares no operation that writes anything** — its only declared call is `listPercentageFixedDiscount`, a read. The name promises authoring and the contract … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listPercentageFixedDiscount lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A view of the promotions that are percentage or fixed-amount discounts, with their limits (maximum percentage, maximum discount, minimum qualifying amount, rounding). Configuration happens on the promotion itself.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listPercentageFixedDiscount return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPercentageFixedDiscount carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Percentage & Fixed Discount Configurator) declares only reads (listPercentageFixedDiscount). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Discount percentage | select field | — | — | — | — | — | — |
| Maximum percentage | select field | — | — | — | — | — | — |
| Maximum monetary discount | select field | — | — | — | — | — | — |
| Minimum qualifying amount | select field | — | — | — | — | — | — |
| Rounding method | select field | — | — | — | — | — | — |
| Discount amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Minimum basket value | select field | — | — | — | — | — | — |
| Maximum uses | select field | — | — | — | — | — | — |
| Whether applied per item or transaction | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **discount table**: One row per promotion of these kinds with the limits; Edit opens the promotion's rule (ADM-148 or BO-010). *(source: contracts/satellite/promotions.yaml#listPercentageFixedDiscount / contracts/satellite/promotions.yaml#/components/schemas/Discount)*

**Data it reads**: `listPercentageFixedDiscount` (onLoad, Percentage & Fixed Discount Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listPercentageFixedDiscount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The percentage fixed discount configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the percentage fixed discount untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No percentage fixed discount configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- promotion: RESIDENT-15
  kind: percentage
  value: 15%
  maxDiscount: AED 150.00
  minimum: AED 200.00
```

#### Permissions

- `listPercentageFixedDiscount` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-149` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-149`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 2: Works in Percentage & Fixed Discount Configurator → Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-149?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-150` Cart & Transaction Threshold Rules

**Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply Y discount to the entire transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29962 (VM-ADM-150) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cart-transaction-threshold-rules-adm-150` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listCartTransactionThreshold lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promotions triggered by basket value, ticket count or composition ("more than 10 tickets, 10% off the whole transaction"), and how the threshold is counted (tax, fees, vouchers, discounts before or after, voids and refunds).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCartTransactionThreshold return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCartTransactionThreshold carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Cart & Transaction Threshold Rules) declares only reads (listCartTransactionThreshold). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **counting rules**: The threshold counting switches shown as a worked basket ("AED 1,000 incl. VAT: counts AED 952.38 net"). *(source: contracts/satellite/promotions.yaml#listCartTransactionThreshold)*

**Data it reads**: `listCartTransactionThreshold` (onLoad, Cart & Transaction Threshold Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listCartTransactionThreshold`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cart transaction threshold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cart transaction threshold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cart transaction threshold yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cart transaction threshold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  promotion: Groups of 10+
  threshold: 10 tickets
  discount: 10% on transaction
  taxCounts: false
```

#### Permissions

- `listCartTransactionThreshold` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-150` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-150`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 4: Works in Cart & Transaction Threshold Rules → Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-150?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-151` Volume, Bulk & Tier Discount Configurator

**Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29963 (VM-ADM-151) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/volume-bulk-tier-discount-configurator-adm-151` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Volume, Bulk & Tier Discount Configurator declares no operation that writes anything** — its only declared call is `listVolumeBulkTier`, a read. The name promises authoring and the contract offers … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Quantity and bulk rules: tiers of minimum and maximum quantity with a discount or a fixed unit price, per product, customer and channel.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listVolumeBulkTier return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listVolumeBulkTier carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Volume, Bulk & Tier Discount Configurator) declares only reads (listVolumeBulkTier). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **tier table**: Tiers as rows with non-overlapping ranges; a gap or overlap is flagged. *(source: contracts/satellite/promotions.yaml#listVolumeBulkTier / contracts/satellite/promotions.yaml#/components/schemas/Discount)*

**Data it reads**: `listVolumeBulkTier` (onLoad, Volume, Bulk & Tier Discount Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listVolumeBulkTier`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The volume bulk tier list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the volume bulk tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No volume bulk tier yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the volume bulk tier are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiers:
- '10-19 tickets: 5%'
- '20-49: 10%'
- '50+: AED 180.00 each'
```

#### Permissions

- `listVolumeBulkTier` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-151` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-151`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 6: Works in Volume, Bulk & Tier Discount Configurator → Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-151?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-152` Time-Based & Seasonal Discount Rules

**Configure promotional pricing based on when the customer purchases or visits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29964 (VM-ADM-152) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/time-based-seasonal-discount-rules-adm-152` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listTimeBasedSeasonal lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion; see the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Discounts by when the guest buys or visits: purchase date, visit date, days or hours before the visit, day of week, time, slot, season, event period.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listTimeBasedSeasonal return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listTimeBasedSeasonal carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Time-Based & Seasonal Discount Rules) declares only reads (listTimeBasedSeasonal). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **time rules**: Each rule as a sentence and on a mini calendar. *(source: contracts/satellite/promotions.yaml#listTimeBasedSeasonal)*

**Data it reads**: `listTimeBasedSeasonal` (onLoad, Time-Based & Seasonal Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listTimeBasedSeasonal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The time-based seasonal discount list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the time-based seasonal discount untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No time-based seasonal discount yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the time-based seasonal discount are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- 'Book 14+ days ahead: 10% off'
- 'Weekday visits Sun-Thu: AED 30.00 off'
```

#### Permissions

- `listTimeBasedSeasonal` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-152` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-152`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 8: Works in Time-Based & Seasonal Discount Rules → Configure promotional pricing based on when the customer purchases or visits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-152?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-153` Customer, Membership & Segment Discount Rules

**Configure discounts based on who the customer is.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29957 (VM-ADM-153) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-membership-segment-discount-rules-adm-153` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listCustomerMembershipSegment lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Discounts by who the guest is: segment, guest category, age, membership status and tier, loyalty tier, annual pass holder, corporate or partner affiliation, residency, B2B.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCustomerMembershipSegment return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCustomerMembershipSegment carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Customer, Membership & Segment Discount Rules) declares only reads (listCustomerMembershipSegment). (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **audience rules**: The audience as chips with the discount it receives. *(source: contracts/satellite/promotions.yaml#listCustomerMembershipSegment)*

**Data it reads**: `listCustomerMembershipSegment` (onLoad, Customer, Membership & Segment Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listCustomerMembershipSegment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer membership segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer membership segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer membership segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer membership segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- audience: Annual pass holders, Gold
  discount: 20% F&B
- audience: UAE residents
  discount: 15% weekdays
```

#### Permissions

- `listCustomerMembershipSegment` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-153` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-153`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 10: Works in Customer, Membership & Segment Discount Rules → Configure discounts based on who the customer is.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-153?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-154` Payment Method, Bank & Partner Discount Rules

**Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29958 (VM-ADM-154) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-method-bank-partner-discount-rules-adm-154` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Membership programs. Each needs an operation, or needs removing from the screen; this is the Phase 3 … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listPaymentMethodBank lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion; see the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Discounts by how the guest pays or which partner they belong to: gateway, bank, card BIN range, spend, cap, uses, budget.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Membership programs. (CHG-MOV-008)
- List operation(s) listPaymentMethodBank return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPaymentMethodBank carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Payment Method, Bank & Partner Discount Rules) declares only reads (listPaymentMethodBank). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner bank | select field | — | — | — | — | — | — |
| BIN/IIN eligibility reference | select field | — | — | — | — | — | — |
| Promotion period | select field | — | — | — | — | — | — |
| Eligible products | select field | — | — | — | — | — | — |
| Minimum spend | select field | — | — | — | — | — | — |
| Discount % | select field | — | — | — | — | — | — |
| Maximum discount | select field | — | — | — | — | — | — |
| Number of uses | select field | — | — | — | — | — | — |
| Customer limit | select field | — | — | — | — | — | — |
| Campaign budget | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Membership programs (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **bank offers**: Bank and card range, period, discount and cap, uses per customer, budget used. *(source: contracts/satellite/promotions.yaml#listPaymentMethodBank)*

**Data it reads**: `listPaymentMethodBank` (onLoad, Payment Method, Bank & Partner Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listPaymentMethodBank`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method bank configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method bank untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method bank configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The card is only known at payment**: The discount is shown as "applies when you pay with" in the basket and applied at payment, not earlier. *(source: designer default)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  bank: Emirates Bank
  cards: Visa Infinite (BIN 4xxxx)
  discount: 20%
  cap: AED 100.00
  period: Nov-Dec 2026
```

#### Permissions

- `listPaymentMethodBank` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-154` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-154`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 12: Works in Payment Method, Bank & Partner Discount Rules → Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-154?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Membership programs.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-155` Special Price & Guest Offer Configurator

**Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29965 (VM-ADM-155) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/special-price-guest-offer-configurator-adm-155` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Special Price & Guest Offer Configurator declares no operation that writes anything** — its only declared call is `listSpecialPriceGuest`, a read. The name promises authoring and the contract … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for the rules listSpecialPriceGuest lists (or the rule is a typed Discount/PromotionConditions on createPromotion/updatePromotion; see the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Special prices for a guest group (resident, tourist, employee, student, school, family, group, partner) without duplicating product SKUs.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listSpecialPriceGuest return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listSpecialPriceGuest carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Special Price & Guest Offer Configurator) declares only reads (listSpecialPriceGuest). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Offer name | select field | — | — | — | — | — | — |
| Eligible product | select field | — | — | — | — | — | — |
| Eligible guest | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Discount | select field | — | — | — | — | — | — |
| Valid dates | select field | — | — | — | — | — | — |
| Valid visit dates | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |
| Restrictions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **special prices**: Offer, product, eligible guest, price per group as columns, dates, channel, capacity. *(source: contracts/satellite/promotions.yaml#listSpecialPriceGuest)*

**Data it reads**: `listSpecialPriceGuest` (onLoad, Special Price & Guest Offer Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listSpecialPriceGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The special price guest configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the special price guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No special price guest configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  product: Day Pass
  resident: AED 250.00
  tourist: AED 295.00
  student: AED 199.00
```

#### Permissions

- `listSpecialPriceGuest` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-155` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-155`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 14: Works in Special Price & Guest Offer Configurator → Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-155?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-156` Discount Limits, Guardrails & Commercial Controls

**Protect the business from incorrectly configured discounts and excessive commercial exposure.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29959 (VM-ADM-156) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/discount-limits-guardrails-commercial-controls-adm-156` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listDiscountLimitGuardrail lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The commercial limits no promotion may break: maximum discount, minimum selling price and margin, maximum per transaction, per customer and per campaign exposure, usage limits, when approval is needed.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listDiscountLimitGuardrail return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDiscountLimitGuardrail carry no identifier. (CHG-MOV-008)
- No write operation: a configuration screen (Discount Limits, Guardrails & Commercial Controls) declares only reads (listDiscountLimitGuardrail). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum discount % | select field | — | — | — | — | — | — |
| Maximum discount value | select field | — | — | — | — | — | — |
| Minimum selling price | select field | — | — | — | — | — | — |
| Minimum margin | select field | — | — | — | — | — | — |
| Maximum transaction discount | select field | — | — | — | — | — | — |
| Maximum customer discount | select field | — | — | — | — | — | — |
| Maximum campaign exposure | select field | — | — | — | — | — | — |
| Maximum redemption count | select field | — | — | — | — | — | — |
| Per-customer usage | select field | — | — | — | — | — | — |
| Per-account usage | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **guardrails**: Each limit with its value and the promotions currently closest to it. *(source: contracts/satellite/promotions.yaml#listDiscountLimitGuardrail)*

**Data it reads**: `listDiscountLimitGuardrail` (onLoad, Discount Limits, Guardrails & Commercial Controls)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listDiscountLimitGuardrail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount limits guardrails configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount limits guardrails untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount limits guardrails configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-095`: Pricing guardrails and discount guardrails are different limits; label each clearly.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guardrails:
  maximumDiscount: 50%
  minimumSellingPrice: AED 1.00
  maximumCustomerDiscount: AED 500.00 a month
```

#### Permissions

- `listDiscountLimitGuardrail` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-156` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-156`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 16: Works in Discount Limits, Guardrails & Commercial Controls → Protect the business from incorrectly configured discounts and excessive commercial exposure.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-156?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-157` Rule Test, Simulation & AI Recommendation Workspace

**Test a promotion before it goes live: run a sample basket through the promotion engine (evaluatePromotions) and replay it against past sales (simulatePromotion), to see which offer applies, what it costs and what it would have done. (A section of BO-010 Promotions & Coupons since 2 October 2026.) (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `promotionId` (navigation) |
| Route | `/venue-operations/promotions-coupons/rule-test-simulation-ai-recommendation-workspace-adm-157` |

**What the spec says about it.** **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager. Each needs an … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test a promotion before activation: a hypothetical guest, segment, products, quantity, channel, date, venue, membership, loyalty, payment type and promo code, and see which rules match, which do not and why.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager. (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): setRuleTestRecommendation takes the test inputs as strings and is a PUT for a test. (CHG-WIR-025); No read operation: the screen declares only setRuleTestRecommendation and nothing that returns the current configuration. (CHG-WIR-025); The purpose text is shared word for word with ADM-187 and does not describe this screen (Rule Test, Simulation & AI Recommendation … (CHG-MOV-005).

#### Inputs: what the user enters or picks

**Form: Test a basket** (modal, opened by *Test a basket*; *Test a basket* calls `evaluatePromotions`, *Cancel* sends nothing)

**Collects what `evaluatePromotions` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary. | `evaluatePromotions` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Membership tier `membershipTierId` | picker: choose a membership tier | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Coupon codes `couponCodes` | list of values (chips) | optional | — | — | — | — | `evaluatePromotions` body |
| Evaluate at `evaluateAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For back-office testing of a rule before publishing. | `evaluatePromotions` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one … | `evaluatePromotions` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `evaluatePromotions` body |
| Line `lines[].lineId` | text field | required | — | — | — | — | `evaluatePromotions` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `evaluatePromotions` body |
| Unit price `lines[].unitPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluatePromotions` body |

Errors to draw in the form: 400 Validation failed

**Form: Simulate on history** (modal, opened by *Simulate on history*; *Simulate on history* calls `simulatePromotion`, *Cancel* sends nothing)

**Collects what `simulatePromotion` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period from `periodFrom` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |
| Period to `periodTo` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create rules, Edit rules, Change discount, Change thresholds, Change segments, Change dates, Override limits, Run simulation, Submit, Approve, Activate. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Campaign Manager (primary button) | navigation or local | — | — | — | — |
| Commercial Manager (secondary button) | navigation or local | — | — | — | — |
| Revenue Manager (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| B2B Manager (secondary button) | navigation or local | — | — | — | — |
| Venue Manager (secondary button) | navigation or local | — | — | — | — |
| Test a basket (secondary button) | `evaluatePromotions` POST `/promotions/evaluate` | EvaluatePromotionsRequest | PromotionEvaluation | 400 Validation failed | opens modal first |
| Simulate on history (secondary button) | `simulatePromotion` POST `/promotions/{promotionId}/simulate` | inline | inline | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **test result**: Applied and rejected rules with the reason for each (the working, not just a total). *(source: contracts/satellite/promotions.yaml#evaluatePromotions)*

**Where the user goes next**

- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule test simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule test simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule test simulation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule test simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  basket: 2 x Day Pass Adult
  channel: App
  code: RESIDENT-15
  result: '15% applied; SUMMER-BOGO rejected: quantity below 3'
```

#### Permissions

- `evaluatePromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `simulatePromotion` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.11 | - Discounts | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.12 | - Dynamic promotions | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.13 | - Coupons | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.8.5 | The system should allow call center agents to apply promotions, discounts, up-sales and offers configured in the system. Application of discount coupons via a code supplied (on the phone) by the … | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 3.5.9 | System shall automatically present bundle offers based on configurable conditions such as number of tickets purchased, guest type, loyalty tier, membership status, sales channel, season, location, or … | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.16 | The system should allow creation of promotion on a bundle: “buy x, get x free”, or “buy a ticket and a catalogue and get 10% off or get AED 10 discount” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.17 | The system should allow creation of added value: “Buy for more than 200 AED and get a free pencil” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.32 | Discounts can be under conditions (dynamic discounts): - early birds, - subject to volume (buy one get one, 4 for 3 …), - subject to the type of tickets or - subject to the customer segment. | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.34 | Cart-level promotions & bundle logic (e.g., “Buy 4 Pay 3”, multi-park family packs) applied automatically at checkout, without new SKUs | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 4.1.7 | The system should be able to accept promotions linked with admission tickets and/or vouchers. | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.9 | The system should be able to apply BOGO based promotion offers based on purchased product types and/or product count | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.10 | The system should be able to allow: - Buy X product and get X product for free. - Buy X product and get Y product for free. - Buy N number of products and Get X product for free. - Buy N number of … | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-157` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-157`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 18: Works in Rule Test, Simulation & AI Recommendation Workspace → Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-157?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager, Test a basket, Simulate on history.
- [ ] Every transition is wired: `BO-010`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"evaluatePromotions": {"method":"POST","path":"/promotions/evaluate","contract":"promotions","summary":"Evaluate promotions against a cart","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EvaluatePromotionsRequest","responds":"PromotionEvaluation"},
"listCartTransactionThreshold": {"method":"GET","path":"/cart-transaction-threshold","contract":"promotions","summary":"Cart & Transaction Threshold Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CartTransactionThresholdRulesView"},
"listCustomerMembershipSegment": {"method":"GET","path":"/customer-membership-segment","contract":"promotions","summary":"Customer, Membership & Segment Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomerMembershipSegmentDiscountRulesView"},
"listDiscountLimitGuardrail": {"method":"GET","path":"/discount-limit-guardrail","contract":"promotions","summary":"Discount Limits, Guardrails & Commercial Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DiscountLimitsGuardrailsCommercialControlsView"},
"listPaymentMethodBank": {"method":"GET","path":"/payment-method-bank","contract":"promotions","summary":"Payment Method, Bank & Partner Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PaymentMethodBankPartnerDiscountRulesView"},
"listPercentageFixedDiscount": {"method":"GET","path":"/percentage-fixed-discount","contract":"promotions","summary":"Percentage & Fixed Discount Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PercentageFixedDiscountConfiguratorView"},
"listSpecialPriceGuest": {"method":"GET","path":"/special-price-guest","contract":"promotions","summary":"Special Price & Guest Offer Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SpecialPriceGuestOfferConfiguratorView"},
"listTimeBasedSeasonal": {"method":"GET","path":"/time-based-seasonal","contract":"promotions","summary":"Time-Based & Seasonal Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TimeBasedSeasonalDiscountRulesView"},
"listVolumeBulkTier": {"method":"GET","path":"/volume-bulk-tier","contract":"promotions","summary":"Volume, Bulk & Tier Discount Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VolumeBulkTierDiscountConfiguratorView"},
"setPromotionStackingRule": {"method":"PUT","path":"/promotion-stacking-rule","contract":"promotions","summary":"Promotion Stacking Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromotionStackingRuleBuilderInput","responds":"PromotionStackingRuleBuilderView"},
"simulatePromotion": {"method":"POST","path":"/promotions/{promotionId}/simulate","contract":"promotions","summary":"What this promotion would have cost on real history","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CartTransactionThresholdRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Cart & Transaction Threshold Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"taxCountsTowardThreshold":{"type":"integer","description":"Tax counts toward threshold"},"feesCount":{"type":"integer","description":"Fees count"},"vouchersCount":{"type":"integer","description":"Vouchers count"},"discountsAreEvaluatedBeforeAfterThreshold":{"type":"integer","description":"Discounts are evaluated before/after threshold"},"voidedItemsAreExcluded":{"type":"string","description":"Voided items are excluded"},"refundedItemsAffectQualification":{"type":"string","description":"Refunded items affect qualification"}}},
"CustomerMembershipSegmentDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Customer, Membership & Segment Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customerSegment":{"type":"string","description":"Customer segment"},"crmSegment":{"type":"string","description":"CRM segment"},"guestCategory":{"type":"string","description":"Guest category"},"ageCategory":{"type":"string","description":"Age category"},"membershipStatus":{"type":"string","description":"Membership status"},"membershipTier":{"type":"string","description":"Membership tier"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"annualPassHolder":{"type":"string","description":"Annual pass holder"},"corporateAffiliation":{"type":"string","description":"Corporate affiliation"},"partnerAffiliation":{"type":"string","description":"Partner affiliation"},"account":{"type":"string","description":"Account"},"countryResidency":{"type":"string","description":"Country/residency"},"b2bCustomer":{"type":"string","description":"B2B customer"}}},
"DiscountLimitsGuardrailsCommercialControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Discount Limits, Guardrails & Commercial Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumDiscount":{"type":"number","description":"Maximum discount %"},"maximumDiscountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount value"},"minimumSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum selling price"},"minimumMargin":{"type":"number","description":"Minimum margin"},"maximumTransactionDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum transaction discount"},"maximumCustomerDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum customer discount"},"maximumCampaignExposure":{"type":"string","description":"Maximum campaign exposure"},"maximumRedemptionCount":{"type":"integer","description":"Maximum redemption count"},"perCustomerUsage":{"type":"string","description":"Per-customer usage"},"perAccountUsage":{"type":"string","description":"Per-account usage"},"requireApproval":{"type":"boolean","description":"Require approval"}}},
"EvaluatePromotionsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","channel","lines"],"properties":{"venueId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"},"subjectId":{"type":"string","format":"uuid"},"membershipTierId":{"type":"string","format":"uuid"},"couponCodes":{"type":"array","items":{"type":"string"}},"evaluateAt":{"type":"string","format":"date-time","description":"For back-office testing of a rule before publishing."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["lineId","variantId","quantity","unitPrice"],"properties":{"lineId":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"PaymentMethodBankPartnerDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Payment Method, Bank & Partner Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"selectedPaymentGateway":{"type":"string","description":"Selected payment gateway"},"partnerBank":{"type":"string","description":"Partner bank"},"binIinEligibilityReference":{"type":"string","description":"BIN/IIN eligibility reference"},"promotionPeriod":{"type":"string","format":"date-time","description":"Promotion period"},"eligibleProducts":{"type":"string","description":"Eligible products"},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum spend"},"discount":{"type":"number","description":"Discount %"},"maximumDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount"},"numberOfUses":{"type":"integer","description":"Number of uses"},"customerLimit":{"type":"integer","description":"Customer limit"},"campaignBudget":{"type":"string","description":"Campaign budget"},"banks":{"type":"string","description":"Banks"},"paymentConditions":{"type":"array","items":{"type":"string","enum":["creditCard","debitCard","visa","mastercard","mada","applePay","wallet","giftCard","bankSpecificCard"]},"description":"Payment methods that qualify."},"partnerType":{"type":"string","enum":["hotels","airlines","tourismPartners","corporatePartners","governmentPartners","membershipPrograms"],"description":"Partner behind the offer."}}},
"PercentageFixedDiscountConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Percentage & Fixed Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discountPercentage":{"type":"number","description":"Discount percentage"},"maximumPercentage":{"type":"number","description":"Maximum percentage"},"maximumMonetaryDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum monetary discount"},"minimumQualifyingAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum qualifying amount"},"roundingMethod":{"type":"string","description":"Rounding method"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount amount"},"currency":{"type":"string","description":"Currency"},"minimumBasketValue":{"type":"string","description":"Minimum basket value"},"maximumUses":{"type":"string","description":"Maximum uses"},"priceBasis":{"type":"string","enum":["currentSellingPrice","dynamicPrice","membershipPrice","b2bPrice","packagePrice"],"description":"The price the discount applies against."}}},
"PromotionEvaluation": {"x-ticvai-persistence":"none — computed","type":"object","required":["totalDiscount","lines","applied","rejected"],"properties":{"totalDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["lineId","originalPrice","discountedPrice","discount"],"properties":{"lineId":{"type":"string"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"applied":{"type":"array","items":{"type":"object","required":["promotionId","promotionCode","discount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"couponCode":{"type":"string","nullable":true}}}},"rejected":{"type":"array","description":"Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n","items":{"type":"object","required":["promotionCode","reason"],"properties":{"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"reason":{"type":"string","enum":["conditionsNotMet","supersededByBetterOffer","exclusivePromotionApplied","redemptionLimitReached","budgetExhausted","outsideValidPeriod","wrongChannel","membershipRequired","couponRequired"]},"detail":{"type":"string"}}}}}},
"PromotionStackingRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the configurable part of a `promotions.stacking_rule` row (StackingRule composes it) (DM5, 29 September: data model for the agreed operations)","description":"**What Promotion Stacking Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"PromotionStackingRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Stacking Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"SpecialPriceGuestOfferConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Special Price & Guest Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"offerName":{"type":"string","description":"Offer name"},"eligibleProduct":{"type":"string","description":"Eligible product"},"eligibleGuest":{"type":"string","description":"Eligible guest"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"validDates":{"type":"string","description":"Valid dates"},"validVisitDates":{"type":"string","description":"Valid visit dates"},"quantity":{"type":"integer","description":"Quantity"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"capacity":{"type":"integer","description":"Capacity"},"restrictions":{"type":"string","description":"Restrictions"},"residentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resident price"},"touristPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tourist price"},"employeePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Employee price"},"studentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Student price"},"schoolPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"School price"},"familyPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Family price"},"groupPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Group price"},"partnerPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner price"}}},
"TimeBasedSeasonalDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Time-Based & Seasonal Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"purchaseDate":{"type":"string","format":"date-time","description":"Purchase date"},"visitDate":{"type":"string","format":"date-time","description":"Visit date"},"daysBeforeVisit":{"type":"string","description":"Days-before-visit"},"hoursBeforeVisit":{"type":"string","description":"Hours-before-visit"},"dayOfWeek":{"type":"string","description":"Day of week"},"time":{"type":"string","format":"date-time","description":"Time"},"timeslot":{"type":"string","description":"Timeslot"},"season":{"type":"string","description":"Season"},"eventPeriod":{"type":"string","format":"date-time","description":"Event period"},"seasonType":{"type":"string","enum":["summer","ramadan","eid","schoolHolidays","nationalDay","peakOffPeak","customSeasons"],"description":"Season the rule applies in."}}},
"VolumeBulkTierDiscountConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Volume, Bulk & Tier Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"maximumQuantity":{"type":"integer","description":"Maximum quantity"},"discount":{"type":"number","description":"Discount %"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount value"},"fixedUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed unit price"},"eligibleProduct":{"type":"string","description":"Eligible product"},"eligibleCustomer":{"type":"string","description":"Eligible customer"},"eligibleChannel":{"type":"string","description":"Eligible channel"}}}
}
```
