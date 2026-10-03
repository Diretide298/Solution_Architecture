# WS53 — Promotions   Bundles Management board 9

**10 screens · 16 operations · 25 schemas · 4 permissions**

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
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-218` | Campaign Governance & Budget Command Center | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-219` | Campaign Budget & Financial Limit Setup | C | 29 | 5 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-220` | Redemption, Discount & Exposure Limit Manager | C | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-221` | Budget Consumption & Forecast Monitor | C | 0 | 13 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-222` | Threshold Actions & Automatic Suspension | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-223` | Campaign Approval Workflow Designer | C | 0 | 20 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-224` | Approval Inbox & Decision Workspace | C | 0 | 46 | 6 | 7 | 0 | 3 | — | notStarted (generated) |
| `ADM-225` | Campaign Financial & Commercial Simulator | C | 0 | 24 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-226` | Campaign Experiment & A/B Test Manager | C | 4 | 16 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-227` | Governance Audit, AI Risk & Launch Readiness | C | 2 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-221, ADM-225, ADM-227 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-218` Campaign Governance & Budget Command Center

**Provide executives, Marketing, Commercial, Revenue, and Finance with one centralized view of the financial and governance status of promotional campaigns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-218 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/campaign-governance-budget-command-center-adm-218` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The financial and governance status of campaigns: budgets, consumption, approvals.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCampaignGovernanceBudget return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCampaignGovernanceBudget carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCampaignGovernanceBudget; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Campaigns** (metric tile)

**Campaign Budget** (metric tile)

**Budget Consumed** (metric tile)

**Remaining Budget** (metric tile)

**Discount Exposure** (metric tile)

**Redemption Value** (metric tile)

**Revenue Generated** (metric tile)

**Incremental Revenue** (metric tile)

**Campaign ROI** (metric tile)

**Campaigns Near Budget Limit** (metric tile)

**Pending Approvals** (metric tile)

**Suspended Campaigns** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **governance overview**: Campaigns with budget used and approval state. *(source: contracts/satellite/promotions.yaml#listCampaignGovernanceBudget)*

**Data it reads**: `listCampaignGovernanceBudget` (onLoad, Campaign Governance & Budget Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-219` Campaign Budget & Financial Limit Setup: *Works in Campaign Budget & Financial Limit Setup*; calls `listCampaignGovernanceBudget`
- → `ADM-220` Redemption, Discount & Exposure Limit Manager: *Works in Redemption, Discount & Exposure Limit Manager*; calls `listCampaignGovernanceBudget`
- → `ADM-221` Budget Consumption & Forecast Monitor: *Works in Budget Consumption & Forecast Monitor*; calls `listCampaignGovernanceBudget`
- → `ADM-222` Threshold Actions & Automatic Suspension: *Works in Threshold Actions & Automatic Suspension*; calls `listCampaignGovernanceBudget`
- → `ADM-223` Campaign Approval Workflow Designer: *Works in Campaign Approval Workflow Designer*; calls `listCampaignGovernanceBudget`
- → `ADM-224` Approval Inbox & Decision Workspace: *Works in Approval Inbox & Decision Workspace*; calls `listCampaignGovernanceBudget`
- → `ADM-225` Campaign Financial & Commercial Simulator: *Works in Campaign Financial & Commercial Simulator*; calls `listCampaignGovernanceBudget`
- → `ADM-226` Campaign Experiment & A/B Test Manager: *Works in Campaign Experiment & A/B Test Manager*; calls `listCampaignGovernanceBudget`
- → `ADM-227` Governance Audit, AI Risk & Launch Readiness: *Works in Governance Audit, AI Risk & Launch Readiness*; calls `listCampaignGovernanceBudget`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign governance budget list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign governance budget untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign governance budget yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign governance budget are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  name: Winter Family 2026
  budgetUsed: 25%
  approval: approved
```

#### Permissions

- `listCampaignGovernanceBudget` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-218` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-218`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 1: Opens Campaign Governance & Budget Command Center → Provide executives, Marketing, Commercial, Revenue, and Finance with one centralized view of the financial and governance status of promotional campaigns.
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F162 branch at step 1 (expected): when Nothing has been set up on Campaign Governance & Budget Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F162 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-218?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-219`, `ADM-220`, `ADM-221`, `ADM-222`, `ADM-223`, `ADM-224`, `ADM-225`, `ADM-226`, `ADM-227`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-219` Campaign Budget & Financial Limit Setup

**Define the financial envelope within which a campaign is permitted to operate.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-219 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/commercial/campaign-budget-financial-limit-setup-adm-219` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Total campaign budget, Venue budget. Each needs an operation, or needs removing from the screen; this is the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The financial envelope a commercial campaign may spend: total, discount, reward, free-product, partner-funded and marketing-funded budgets, split by venue and department, with owner, cost centre and funding source. The campaign header is created first; budget lines hang under it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- totalCampaignBudget is an integer, costCenter is typed Money, and the other budgets are strings. (CHG-MOV-008)
- Pack actions with no operation: Total campaign budget, Venue budget. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Campaign | select field | — | — | — | — | — | — |
| Budget amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Budget owner | select field | — | — | — | — | — | — |
| Cost center | select field | — | — | — | — | — | — |
| Business entity | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Funding source | select field | — | — | — | — | — | — |
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |

**Form: Create commercial campaign** (modal, opened by *Create commercial campaign*; *Create commercial campaign* calls `createCommercialCampaign`, *Cancel* sends nothing)

**Collects what `createCommercialCampaign` sends before it is called.** Required: `venueId`, `name`. Optional: `code`, `description`, `ownerPrincipalId`, `legalEntityId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createCommercialCampaign` body |
| Code `code` | text field | optional | — | max length 64 | — | Unique at the venue when given. | `createCommercialCampaign` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createCommercialCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createCommercialCampaign` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | The campaign (and budget) owner. | `createCommercialCampaign` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | The business entity that funds and books the campaign. | `createCommercialCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCommercialCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCommercialCampaign` body |

Errors to draw in the form: 400 `validTo` at or before `validFrom`.; 409 `code` is already used by another campaign at the venue.

**Form: Save commercial campaign** (modal, opened by *Save commercial campaign*; *Save commercial campaign* calls `updateCommercialCampaign`, *Cancel* sends nothing)

**Collects what `updateCommercialCampaign` sends before it is called.** Nothing in the body is required. Optional: `code`, `name`, `description`, `ownerPrincipalId`, `legalEntityId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 64 | — | — | `updateCommercialCampaign` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateCommercialCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateCommercialCampaign` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `updateCommercialCampaign` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | — | `updateCommercialCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCommercialCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCommercialCampaign` body |

Errors to draw in the form: 400 `validTo` at or before `validFrom`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The new code is already used at the venue, or the new dates would leave a scheduled or live promotion, coupon campaign or active bundle of the campaign outside …

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **budget lines**: A table (dimension, budget, consumed, committed, remaining) with a total that must not exceed the campaign total. *(source: contracts/satellite/promotions.yaml#setCampaignBudgetFinancial / contracts/satellite/promotions.yaml#listCommercialCampaigns)*
- **campaign dates**: Narrowing dates is refused while it would strand a scheduled or live promotion, coupon campaign or bundle; the refusal names them. *(source: contracts/satellite/promotions.yaml#updateCommercialCampaign)*

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Total campaign budget (primary button) | navigation or local | — | — | — | — |
| Venue budget (secondary button) | navigation or local | — | — | — | — |
| Create commercial campaign (secondary button) | `createCommercialCampaign` POST `/commercial-campaigns` | CreateCommercialCampaignRequest | CommercialCampaign | 400 `validTo` at or before `validFrom`.; 409 `code` is already used by another campaign at the venue. | gated `PRICE_CONFIGURE`; opens modal first |
| Save commercial campaign (secondary button) | `updateCommercialCampaign` PATCH `/commercial-campaigns/{campaignId}` | inline | CommercialCampaign | 400 `validTo` at or before `validFrom`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The new code is already used at the venue, or the new dates would … | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `setCampaignBudgetFinancial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign budget financial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign budget financial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign budget financial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `validTo` at or before `validFrom`.; 409 The new code is already used at the venue, or the new dates would leave a scheduled or live promotion, coupon campaign or active bundle of the campaign outside …; 409 `code` is already used by another campaign at the venue. |

#### Consistency with other screens

- Match `BO-010`: A promotion's budget cap and the campaign budget are different limits; show both where the promotion belongs to a campaign.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  code: WINTER-FAM-26
  name: Winter Family 2026
  nameAr: شتاء العائلة 2026
  owner: Head of marketing
  dates: 2026-11-15 to 2027-01-15
budgets:
- line: Discount
  budget: AED 250,000.00
  consumed: AED 61,400.00
- line: Partner-funded
  budget: AED 40,000.00
```

#### Permissions

- `setCampaignBudgetFinancial` → `PRICE_CONFIGURE` (configure) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff
- `createCommercialCampaign` → `PRICE_CONFIGURE` (configure) · staff
- `updateCommercialCampaign` → `PRICE_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-219` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-219`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 2: Works in Campaign Budget & Financial Limit Setup → Define the financial envelope within which a campaign is permitted to operate.

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-219?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Total campaign budget, Venue budget, Create commercial campaign, Save commercial campaign.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-220` Redemption, Discount & Exposure Limit Manager

**Define non-budget commercial limits controlling campaign exposure.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-220 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/redemption-discount-exposure-limit-manager-adm-220` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Redemption, Discount & Exposure Limit Manager declares no operation that writes anything** — its only declared call is `listRedemptionDiscountExposure`, a read. The name promises authoring and the … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for what listRedemptionDiscountExposure lists.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Non-budget limits on campaign exposure: redemptions, discount, exposure.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRedemptionDiscountExposure return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listRedemptionDiscountExposure carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRedemptionDiscountExposure; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Redemption, Discount & Exposure Limit Manager) declares only reads (listRedemptionDiscountExposure). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 50% | select field | — | — | — | — | — | — |
| 75% | select field | — | — | — | — | — | — |
| 90% | select field | — | — | — | — | — | — |
| 95% | select field | — | — | — | — | — | — |
| 100% | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **limits**: Limit, used, remaining. *(source: contracts/satellite/promotions.yaml#listRedemptionDiscountExposure)*

**Data it reads**: `listRedemptionDiscountExposure` (onLoad, Redemption, Discount & Exposure Limit Manager)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `listRedemptionDiscountExposure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption discount exposure configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption discount exposure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption discount exposure configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
limit:
  redemptions: 5000
  used: 1284
```

#### Permissions

- `listRedemptionDiscountExposure` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-220` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-220`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 4: Works in Redemption, Discount & Exposure Limit Manager → Define non-budget commercial limits controlling campaign exposure.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-220?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-221` Budget Consumption & Forecast Monitor

**Provide real-time tracking of campaign financial consumption and predict when limits will be reached.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-221 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/budget-consumption-forecast-monitor-adm-221` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Budget consumption in real time and when limits will be reached.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listBudgetConsumptionForecast return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listBudgetConsumptionForecast carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listBudgetConsumptionForecast; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every budget consumption forecast** (data table, from `listBudgetConsumptionForecast`)

| Shows | Format | Notes |
|---|---|---|
| Original budget | text | Original budget |
| Consumed | text | Consumed |
| Committed | text | Committed |
| Reserved | text | Reserved |
| Remaining | text | Remaining |
| Daily burn rate | 12.5% | Daily burn rate |

**The selected budget consumption forecast** (detail panel): The pack groups this record's detail under its own headings: “Consumed”, “Reserved”, “Committed”, “Remaining campaign”.

| Shows | Format | Notes |
|---|---|---|
| Original budget | text | Original budget |
| Consumed | text | Consumed |
| Committed | text | Committed |
| Reserved | text | Reserved |
| Remaining | text | Remaining |
| Forecast final spend | AED 1,234.50 | Forecast final spend |
| Daily burn rate | 12.5% | Daily burn rate |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **burn-down**: Consumption line with forecast exhaustion date. *(source: contracts/satellite/promotions.yaml#listBudgetConsumptionForecast)*

**Data it reads**: `listBudgetConsumptionForecast` (onLoad, Budget Consumption & Forecast Monitor)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `listBudgetConsumptionForecast`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The budget consumption forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the budget consumption forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No budget consumption forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the budget consumption forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  campaign: Winter Family 2026
  exhaustion: '2027-01-08'
```

#### Permissions

- `listBudgetConsumptionForecast` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-221` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-221`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 6: Works in Budget Consumption & Forecast Monitor → Provide real-time tracking of campaign financial consumption and predict when limits will be reached.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-221?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-222` Threshold Actions & Automatic Suspension

**Define what TICVAI should do as financial or redemption thresholds are approached or exceeded. This is explicitly required by the matrix.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-222 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/threshold-actions-automatic-suspension-adm-222` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 10 actions on this screen and the screen declares 1 operation.** Unserved: Notify, Warn, Require approval, Reduce allocation, Stop specific channel, Stop partner, Stop promotion … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What happens as thresholds are approached or exceeded: alert, require approval, suspend automatically.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Notify, Warn, Require approval, Reduce allocation, Stop specific channel, Stop partner, Stop promotion, Stop campaign ….** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-222; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listThresholdActionAutomatic return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listThresholdActionAutomatic; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Notify (primary button) | navigation or local | — | — | — | — |
| Warn (secondary button) | navigation or local | — | — | — | — |
| Require approval (secondary button) | navigation or local | — | — | — | — |
| Reduce allocation (secondary button) | navigation or local | — | — | — | — |
| Stop specific channel (destructive button) | navigation or local | — | — | — | — |
| Stop partner (destructive button) | navigation or local | — | — | — | — |
| Stop promotion (destructive button) | navigation or local | — | — | — | — |
| Stop campaign (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **threshold actions**: Threshold to action ladder. *(source: contracts/satellite/promotions.yaml#listThresholdActionAutomatic)*

**Data it reads**: `listThresholdActionAutomatic` (onLoad, Threshold Actions & Automatic Suspension)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `listThresholdActionAutomatic`

**What opens over it**

- confirmDialog *Stop specific channel*: **Stop specific channel on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Stop partner*: **Stop partner on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Stop promotion*: **Stop promotion on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Stop campaign*: **Stop campaign on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The threshold actions automatic list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the threshold actions automatic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No threshold actions automatic yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the threshold actions automatic are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ladder:
- '80% budget: alert owner'
- '100%: suspend'
```

#### Permissions

- `listThresholdActionAutomatic` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-222` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-222`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 8: Works in Threshold Actions & Automatic Suspension → Define what TICVAI should do as financial or redemption thresholds are approached or exceeded. This is explicitly required by the matrix.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-222?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Notify, Warn, Require approval, Reduce allocation, Stop specific channel, Stop partner, Stop promotion, Stop campaign.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-223` Campaign Approval Workflow Designer

**Configure multi-level approval workflows for promotions and campaigns. The matrix explicitly requires configurable multi-level approval for promotion creation, modification, activation, and deactivation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-223 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `PRICE_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/campaign-approval-workflow-designer-adm-223` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Sequential approval, Parallel approval, Conditional approval, Mandatory approval, Optional review. Each … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Multi-level approval for promotion creation, change, activation and deactivation.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Sequential approval, Parallel approval, Conditional approval, Mandatory approval, Optional review.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-223; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveCampaignWorkflow and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

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
| Sequential approval (primary button) | navigation or local | — | — | — | — |
| Parallel approval (secondary button) | navigation or local | — | — | — | — |
| Conditional approval (secondary button) | navigation or local | — | — | — | — |
| Mandatory approval (secondary button) | navigation or local | — | — | — | — |
| Optional review (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalMatrices` (onLoad, The campaign approval routes already configured)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `approveCampaignWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign approval workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-770`: Same operation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: 'Discount over 30%: Marketing director then CFO'
```

#### Permissions

- `approveCampaignWorkflow` → `PRICE_CONFIGURE` (configure) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-223` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-223`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 10: Works in Campaign Approval Workflow Designer → Configure multi-level approval workflows for promotions and campaigns. The matrix explicitly requires configurable multi-level approval for promotion creation, modification, activation, and …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-223?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sequential approval, Parallel approval, Conditional approval, Mandatory approval, Optional review.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-224` Approval Inbox & Decision Workspace

**Provide approvers with enough commercial information to make an informed decision without navigating through every configuration screen.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-224 |
| Who uses it | venue staff holding `APPROVAL_VIEW`, `PRICE_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/approval-inbox-decision-workspace-adm-224` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The approver's inbox with the commercial context needed to decide.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveDecision and nothing that returns the current configuration. (CHG-WIR-025).

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

#### Outputs: what the screen shows and produces

**Shown**

**Every approval decision** (data table, from `approveDecision`)

| Shows | Format | Notes |
|---|---|---|
| Campaign | text | Campaign |
| Promotion | text | Promotion |
| Requested by | text | Requested by |
| Request date | 1 Oct 2026, 14:30 | Request date |
| Requested action | text | Requested action |
| Discount | AED 1,234.50 | Discount |
| Budget | text | Budget |
| Estimated redemptions | 1,234 | Estimated redemptions |
| Estimated revenue | AED 1,234.50 | Estimated revenue |
| Margin impact | 1,234.5 | Margin impact |
| Customer reach | text | Customer reach |
| Risk level | text | Risk level |
| AI forecast | text | AI forecast |

**Approval inbox** (data table, from `listApprovalRequests`)

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

**The selected approval decision** (detail panel): The pack groups this record's detail under its own headings: “Current”, “Discount”, “Budget”, “Duration”, “Approver Actions”, “Comments”.

| Shows | Format | Notes |
|---|---|---|
| Campaign | text | Campaign |
| Promotion | text | Promotion |
| Requested by | text | Requested by |
| Request date | 1 Oct 2026, 14:30 | Request date |
| Requested action | text | Requested action |
| Discount | AED 1,234.50 | Discount |
| Budget | text | Budget |
| Estimated redemptions | 1,234 | Estimated redemptions |
| Estimated revenue | AED 1,234.50 | Estimated revenue |
| Margin impact | 1,234.5 | Margin impact |
| Customer reach | text | Customer reach |
| Risk level | text | Risk level |
| AI forecast | text | AI forecast |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalRequests` (onLoad, Requests awaiting a decision, or already decided)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `approveDecision`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-374`: Same operation and decision set.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  promotion: SUMMER-BOGO
  exposure: AED 50,000.00
  decision: pending
```

#### Permissions

- `approveDecision` → `PRICE_CONFIGURE` (configure) · staff
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

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-224` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-224`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 12: Works in Approval Inbox & Decision Workspace → Provide approvers with enough commercial information to make an informed decision without navigating through every configuration screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-224?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`, `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-225` Campaign Financial & Commercial Simulator

**Simulate the likely financial result of a campaign before activation. This is a major matrix requirement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-225 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/campaign-financial-commercial-simulator-adm-225` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The likely financial result of a campaign before activation.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCampaignFinancialCommercial return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCampaignFinancialCommercial carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCampaignFinancialCommercial; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every campaign financial commercial** (data table, from `listCampaignFinancialCommercial`)

| Shows | Format | Notes |
|---|---|---|
| Eligible audience | text | Eligible audience |
| Expected transactions | 1,234 | Expected transactions |
| Expected redemptions | 1,234 | Expected redemptions |
| Gross revenue | AED 1,234.50 | Gross revenue |
| Discount cost | AED 1,234.50 | Discount cost |
| Net revenue | AED 1,234.50 | Net revenue |
| Incremental revenue | AED 1,234.50 | Incremental revenue |
| Average order value | 1,234.5 | Average order value |
| Gross margin | 1,234.5 | Gross margin |
| Margin impact | 1,234.5 | Margin impact |
| Expected budget consumption | text | Expected budget consumption |
| Roi | text | ROI |

**The selected campaign financial commercial** (detail panel): The pack groups this record's detail under its own headings: “Simulation Inputs”, “Scenario ROI”, “Historical Replay”.

| Shows | Format | Notes |
|---|---|---|
| Eligible audience | text | Eligible audience |
| Expected transactions | 1,234 | Expected transactions |
| Expected redemptions | 1,234 | Expected redemptions |
| Gross revenue | AED 1,234.50 | Gross revenue |
| Discount cost | AED 1,234.50 | Discount cost |
| Net revenue | AED 1,234.50 | Net revenue |
| Incremental revenue | AED 1,234.50 | Incremental revenue |
| Average order value | 1,234.5 | Average order value |
| Gross margin | 1,234.5 | Gross margin |
| Margin impact | 1,234.5 | Margin impact |
| Expected budget consumption | text | Expected budget consumption |
| Roi | text | ROI |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **simulation**: Revenue, discount, margin, incremental. *(source: contracts/satellite/promotions.yaml#listCampaignFinancialCommercial / contracts/satellite/promotions.yaml#simulatePromotion)*

**Data it reads**: `listCampaignFinancialCommercial` (onLoad, Campaign Financial & Commercial Simulator)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `listCampaignFinancialCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign financial commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign financial commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign financial commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign financial commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  discount: AED 48,000.00
  incremental: AED 120,000.00
```

#### Permissions

- `listCampaignFinancialCommercial` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-225` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-225`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 14: Works in Campaign Financial & Commercial Simulator → Simulate the likely financial result of a campaign before activation. This is a major matrix requirement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-225?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-226` Campaign Experiment & A/B Test Manager

**Allow TICVAI to test campaign variants and determine which commercial strategy performs better. The matrix explicitly requires A/B testing of promotion variants, including discount levels, validity periods, bundles, and target segments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-226 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Measure) and no metric row |
| Offline | online only |
| Opens with | `promotionId` (navigation) |
| Route | `/commercial/campaign-experiment-a-b-test-manager-adm-226` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Campaign Experiment & A/B Test Manager declares no operation that writes anything** — its only declared call is `listCampaignExperimentTest`, a read. The name promises authoring and the contract …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Campaign variants tested against each other (discount level, validity, channel).

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCampaignExperimentTest return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listCampaignExperimentTest carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listCampaignExperimentTest; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No write operation: a configuration screen (Campaign Experiment & A/B Test Manager) declares only reads (listCampaignExperimentTest). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Form: Set variants** (modal, opened by *Set variants*; *Set variants* calls `setPromotionVariants`, *Cancel* sends nothing)

**Collects what `setPromotionVariants` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variants `variants` | repeatable rows | required | — | at least 2; at most 4 | — | — | `setPromotionVariants` body |
| Label `variants[].label` | text field | required | — | — | — | — | `setPromotionVariants` body |
| Traffic percent `variants[].trafficPercent` | stepper or slider | required | — | min 0; max 100 | — | Share of traffic. All variants of a promotion sum to 100, with no minimum per variant (decided 28 September, audit R101). | `setPromotionVariants` body |
| Discount percent `variants[].discountPercent` | number field | optional | — | — | — | — | `setPromotionVariants` body |

Errors to draw in the form: 400 The variants' `trafficPercent` values do not sum to 100 (audit R101)

#### Outputs: what the screen shows and produces

**Shown**

**Every campaign experiment test** (data table, from `listCampaignExperimentTest`)

| Shows | Format | Notes |
|---|---|---|
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Aov | text | AOV |
| Redemption | text | Redemption |
| Discount cost | AED 1,234.50 | Discount cost |
| Margin | 1,234.5 | Margin |
| Incremental revenue | AED 1,234.50 | Incremental revenue |
| Roi | text | ROI |

**The selected campaign experiment test** (detail panel): The pack groups this record's detail under its own headings: “Variant A”, “Variant B”, “Variant C”, “Audience Allocation”, “Test”.

| Shows | Format | Notes |
|---|---|---|
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Aov | text | AOV |
| Redemption | text | Redemption |
| Discount cost | AED 1,234.50 | Discount cost |
| Margin | 1,234.5 | Margin |
| Incremental revenue | AED 1,234.50 | Incremental revenue |
| Roi | text | ROI |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| AI recommendation (primary button) | navigation or local | — | — | — | — |
| Set variants (secondary button) | `setPromotionVariants` PUT `/promotions/{promotionId}/variants` | inline | inline | 400 The variants' `trafficPercent` values do not sum to 100 (audit R101) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **experiments**: Variants, traffic, results with significance. *(source: contracts/satellite/promotions.yaml#listCampaignExperimentTest / contracts/satellite/promotions.yaml#setPromotionVariants)*

**Data it reads**: `listCampaignExperimentTest` (onLoad, Campaign Experiment & A/B Test Manager)

**Where the user goes next**

- → `ADM-218` Campaign Governance & Budget Command Center: *Returns to the board's landing screen*; calls `listCampaignExperimentTest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign experiment test list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign experiment test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign experiment test yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign experiment test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The variants' `trafficPercent` values do not sum to 100 (audit R101) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  variants:
  - 10%
  - 15%
  winner: 10% (higher margin, same conversion)
```

#### Permissions

- `listCampaignExperimentTest` → `PRICE_VIEW` (read) · staff
- `setPromotionVariants` → `PRICE_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-226` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-226`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 16: Works in Campaign Experiment & A/B Test Manager → Allow TICVAI to test campaign variants and determine which commercial strategy performs better. The matrix explicitly requires A/B testing of promotion variants, including discount levels, validity …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-226?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: AI recommendation, Set variants.
- [ ] Every transition is wired: `ADM-218`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-227` Governance Audit, AI Risk & Launch Readiness

**Provide the final governance checkpoint before a campaign is allowed to go live.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-ADM-227 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure commercial behavior) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/governance-audit-ai-risk-launch-readiness-adm-227` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The final governance checkpoint before a campaign goes live: audit, AI risk, readiness.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGovernanceRiskLaunch return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGovernanceRiskLaunch carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listGovernanceRiskLaunch; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |
| Board 9 — Governance | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **readiness checklist**: Checks passed or failed with risk notes. *(source: contracts/satellite/promotions.yaml#listGovernanceRiskLaunch)*

**Data it reads**: `listGovernanceRiskLaunch` (onLoad, Governance Audit, AI Risk & Launch Readiness)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance audit risk configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance audit risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance audit risk configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
readiness:
  passed: 9
  failed:
  - Arabic copy missing
```

#### Permissions

- `listGovernanceRiskLaunch` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-227` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS114 Promotions   Bundles Management Board 9.dc.html#adm-227`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 9
- Flow F162 *Promotions Bundles Management board 9: Campaign Governance & Budget Command …*, step 18: Works in Governance Audit, AI Risk & Launch Readiness → Provide the final governance checkpoint before a campaign is allowed to go live.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-227?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveCampaignWorkflow": {"method":"PUT","path":"/campaign-workflow","contract":"promotions","summary":"Campaign Approval Workflow Designer","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CampaignApprovalWorkflowDesignerInput","responds":"CampaignApprovalWorkflowDesignerView"},
"approveDecision": {"method":"PUT","path":"/decision","contract":"promotions","summary":"Approval Inbox & Decision Workspace","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalInboxDecisionWorkspaceInput","responds":"ApprovalInboxDecisionWorkspaceView"},
"createCommercialCampaign": {"method":"POST","path":"/commercial-campaigns","contract":"promotions","summary":"Create a commercial campaign","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCommercialCampaignRequest","responds":"CommercialCampaign"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBudgetConsumptionForecast": {"method":"GET","path":"/budget-consumption-forecast","contract":"promotions","summary":"Budget Consumption & Forecast Monitor","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BudgetConsumptionForecastMonitorView"},
"listCampaignExperimentTest": {"method":"GET","path":"/campaign-experiment-test","contract":"promotions","summary":"Campaign Experiment & A/B Test Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CampaignExperimentABTestManagerView"},
"listCampaignFinancialCommercial": {"method":"GET","path":"/campaign-financial-commercial","contract":"promotions","summary":"Campaign Financial & Commercial Simulator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CampaignFinancialCommercialSimulatorView"},
"listCampaignGovernanceBudget": {"method":"GET","path":"/campaign-governance-budget","contract":"promotions","summary":"Campaign Governance & Budget Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CampaignGovernanceBudgetCommandCenterView"},
"listCommercialCampaigns": {"method":"GET","path":"/commercial-campaigns","contract":"promotions","summary":"List commercial campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":"ownerPrincipalId","in":"query","required":null},{"name":"q","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGovernanceRiskLaunch": {"method":"GET","path":"/governance-risk-launch","contract":"promotions","summary":"Governance Audit, AI Risk & Launch Readiness","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GovernanceAuditAiRiskLaunchReadinessView"},
"listRedemptionDiscountExposure": {"method":"GET","path":"/redemption-discount-exposure","contract":"promotions","summary":"Redemption, Discount & Exposure Limit Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RedemptionDiscountExposureLimitManagerView"},
"listThresholdActionAutomatic": {"method":"GET","path":"/threshold-action-automatic","contract":"promotions","summary":"Threshold Actions & Automatic Suspension","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ThresholdActionsAutomaticSuspensionView"},
"setCampaignBudgetFinancial": {"method":"PUT","path":"/campaign-budget-financial","contract":"promotions","summary":"Campaign Budget & Financial Limit Setup","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CampaignBudgetFinancialLimitSetupInput","responds":"CampaignBudgetFinancialLimitSetupView"},
"setPromotionVariants": {"method":"PUT","path":"/promotions/{promotionId}/variants","contract":"promotions","summary":"A/B test two versions against each other","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCommercialCampaign": {"method":"PATCH","path":"/commercial-campaigns/{campaignId}","contract":"promotions","summary":"Amend a commercial campaign","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CommercialCampaign"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalInboxDecisionWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Inbox & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"decision":{"type":"string","enum":["approve","reject","returnForChange","requestInformation","delegate"],"description":"Approver decision"},"comment":{"type":"string","description":"Approver comment"},"delegateTo":{"type":"string","description":"Approver delegated to, for delegate"}}},
"ApprovalInboxDecisionWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Approval Inbox & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"campaign":{"type":"string","description":"Campaign"},"promotion":{"type":"string","description":"Promotion"},"requestedBy":{"type":"string","description":"Requested by"},"requestDate":{"type":"string","format":"date-time","description":"Request date"},"requestedAction":{"type":"string","description":"Requested action"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"budget":{"type":"string","description":"Budget"},"estimatedRedemptions":{"type":"integer","description":"Estimated redemptions"},"estimatedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated revenue"},"marginImpact":{"type":"number","description":"Margin impact"},"customerReach":{"type":"string","description":"Customer reach"},"riskLevel":{"type":"string","description":"Risk level"},"aiForecast":{"type":"string","description":"AI forecast"},"decision":{"type":"string","enum":["approve","reject","returnForChange","requestInformation","delegate"],"description":"Approver decision"},"comment":{"type":"string","description":"Approver comment"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"BudgetConsumptionForecastMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Budget Consumption & Forecast Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"originalBudget":{"type":"string","description":"Original budget"},"consumed":{"type":"string","description":"Consumed"},"committed":{"type":"string","description":"Committed"},"reserved":{"type":"string","description":"Reserved"},"remaining":{"type":"string","description":"Remaining"},"forecastFinalSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast final spend"},"dailyBurnRate":{"type":"number","description":"Daily burn rate"}}},
"CampaignApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.coupon_campaign at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Campaign Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"discount":{"type":"number","description":"Discount %"},"campaignBudget":{"type":"string","description":"Campaign budget"},"margin":{"type":"number","description":"Margin"},"promotionType":{"type":"string","description":"Promotion type"},"venue":{"type":"string","description":"Venue"},"partner":{"type":"string","description":"Partner"},"channel":{"type":"string","description":"Channel"},"freeProductValue":{"type":"string","description":"Free-product value"},"campaignDuration":{"type":"string","format":"date-time","description":"Campaign duration"},"financialExposure":{"type":"string","description":"Financial exposure"},"sequentialApproval":{"type":"string","description":"Sequential approval"},"parallelApproval":{"type":"string","description":"Parallel approval"},"conditionalApproval":{"type":"string","description":"Conditional approval"},"mandatoryApproval":{"type":"string","description":"Mandatory approval"},"optionalReview":{"type":"string","description":"Optional review"},"delegation":{"type":"string","description":"Delegation"},"escalation":{"type":"string","description":"Escalation"}}},
"CampaignApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discount":{"type":"number","description":"Discount %"},"campaignBudget":{"type":"string","description":"Campaign budget"},"margin":{"type":"number","description":"Margin"},"promotionType":{"type":"string","description":"Promotion type"},"venue":{"type":"string","description":"Venue"},"partner":{"type":"string","description":"Partner"},"channel":{"type":"string","description":"Channel"},"freeProductValue":{"type":"string","description":"Free-product value"},"campaignDuration":{"type":"string","format":"date-time","description":"Campaign duration"},"financialExposure":{"type":"string","description":"Financial exposure"},"sequentialApproval":{"type":"string","description":"Sequential approval"},"parallelApproval":{"type":"string","description":"Parallel approval"},"conditionalApproval":{"type":"string","description":"Conditional approval"},"mandatoryApproval":{"type":"string","description":"Mandatory approval"},"optionalReview":{"type":"string","description":"Optional review"},"delegation":{"type":"string","description":"Delegation"},"escalation":{"type":"string","description":"Escalation"}}},
"CampaignBudget": {"x-ticvai-persistence":"promotions.campaign_budget","type":"object","description":"One budget line of a commercial campaign (setCampaignBudgetFinancial): what kind of spend it caps, who funds it, what it covers, and what happens as it is consumed. **Consumed, committed and reserved are not stored**: consumed is the discount given on orders (`orders.discount`, `promotions.promotion.discount_given`), committed and reserved are priced carts not yet paid, all worked out on read so they cannot drift from the orders they summarise. (DM5, 29 September: data model for the agreed operations)","required":["budgetType","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"budgetType":{"type":"string","enum":["total","discount","reward","freeProduct"],"description":"The spend this line caps (total campaign, discount, reward or free-product budget)."},"fundingSource":{"type":"string","nullable":true,"enum":["venue","department","marketing","partner"],"description":"Who pays for it; `partner` is a co-funded (e.g. bank or partner-funded) line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scope":{"type":"string","enum":["entireCampaign","promotion","product","channel","partner","customerSegment"],"default":"entireCampaign","description":"What the line covers."},"scopeRef":{"type":"string","nullable":true,"description":"The promotion, product, partner or segment id, or the SalesChannel value, that `scope` names. Null for `entireCampaign`."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The budget owner."},"costCentre":{"type":"string","maxLength":64,"nullable":true},"department":{"type":"string","maxLength":100,"nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"thresholdPolicy":{"$ref":"#/components/schemas/BudgetThresholdPolicy"}}},
"CampaignBudgetFinancialLimitSetupInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; saved as the `promotions.campaign` header (campaign, budget owner, business entity, venue, effective dates) and its `promotions.campaign_budget` lines (one per budget amount given, with funding source, cost centre and scope) (DM5, 29 September: data model for the agreed operations)","description":"**What Campaign Budget & Financial Limit Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"totalCampaignBudget":{"type":"integer","description":"Total campaign budget"},"discountBudget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount budget"},"rewardBudget":{"type":"string","description":"Reward budget"},"freeProductBudget":{"type":"string","description":"Free-product budget"},"partnerFundedBudget":{"type":"string","description":"Partner-funded budget"},"marketingFundedBudget":{"type":"string","description":"Marketing-funded budget"},"venueBudget":{"type":"string","description":"Venue budget"},"departmentBudget":{"type":"string","description":"Department budget"},"campaign":{"type":"string","description":"Campaign"},"budgetAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Budget amount"},"currency":{"type":"string","description":"Currency"},"effectiveDates":{"type":"string","description":"Effective dates"},"budgetOwner":{"type":"string","description":"Budget owner"},"costCenter":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost center"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"department":{"type":"string","description":"Department"},"fundingSource":{"type":"string","description":"Funding source"},"entireCampaign":{"type":"string","description":"Entire campaign"},"promotion":{"type":"string","description":"Promotion"},"product":{"type":"string","description":"Product"},"channel":{"type":"string","description":"Channel"},"partner":{"type":"string","description":"Partner"},"customerSegment":{"type":"string","description":"Customer segment"}}},
"CampaignBudgetFinancialLimitSetupView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Budget & Financial Limit Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"totalCampaignBudget":{"type":"integer","description":"Total campaign budget"},"discountBudget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount budget"},"rewardBudget":{"type":"string","description":"Reward budget"},"freeProductBudget":{"type":"string","description":"Free-product budget"},"partnerFundedBudget":{"type":"string","description":"Partner-funded budget"},"marketingFundedBudget":{"type":"string","description":"Marketing-funded budget"},"venueBudget":{"type":"string","description":"Venue budget"},"departmentBudget":{"type":"string","description":"Department budget"},"campaign":{"type":"string","description":"Campaign"},"budgetAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Budget amount"},"currency":{"type":"string","description":"Currency"},"effectiveDates":{"type":"string","description":"Effective dates"},"budgetOwner":{"type":"string","description":"Budget owner"},"costCenter":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost center"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"department":{"type":"string","description":"Department"},"fundingSource":{"type":"string","description":"Funding source"},"entireCampaign":{"type":"string","description":"Entire campaign"},"promotion":{"type":"string","description":"Promotion"},"product":{"type":"string","description":"Product"},"channel":{"type":"string","description":"Channel"},"partner":{"type":"string","description":"Partner"},"customerSegment":{"type":"string","description":"Customer segment"}}},
"CampaignExperimentABTestManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Experiment & A/B Test Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discount":{"type":"number","description":"Discount %"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount value"},"promotionType":{"type":"string","description":"Promotion type"},"bundle":{"type":"string","description":"Bundle"},"reward":{"type":"string","description":"Reward"},"audience":{"type":"string","description":"Audience"},"channel":{"type":"string","description":"Channel"},"validity":{"type":"string","description":"Validity"},"messageOffer":{"type":"string","description":"Message/offer"},"timing":{"type":"string","description":"Timing"},"conversion":{"type":"number","description":"Conversion"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"aov":{"type":"string","description":"AOV"},"redemption":{"type":"string","description":"Redemption"},"discountCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount cost"},"margin":{"type":"number","description":"Margin"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"roi":{"type":"string","description":"ROI"},"manualWinner":{"type":"string","description":"Manual winner"},"ruleBasedWinner":{"type":"string","description":"Rule-based winner"},"aiRecommendation":{"type":"string","description":"AI recommendation"},"variantAllocation":{"type":"array","items":{"type":"string"},"description":"Audience allocation per variant, e.g. A 40%, B 40%, control 20%"}}},
"CampaignFinancialCommercialSimulatorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Financial & Commercial Simulator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"audience":{"type":"string","description":"Audience"},"products":{"type":"string","description":"Products"},"promotion":{"type":"string","description":"Promotion"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"duration":{"type":"string","format":"date-time","description":"Duration"},"channels":{"type":"string","description":"Channels"},"historicalConversion":{"type":"number","description":"Historical conversion"},"expectedTraffic":{"type":"string","description":"Expected traffic"},"redemptionLimit":{"type":"integer","description":"Redemption limit"},"budget":{"type":"string","description":"Budget"},"eligibleAudience":{"type":"string","description":"Eligible audience"},"expectedTransactions":{"type":"integer","description":"Expected transactions"},"expectedRedemptions":{"type":"integer","description":"Expected redemptions"},"grossRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross revenue"},"discountCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount cost"},"netRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net revenue"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"averageOrderValue":{"type":"number","description":"Average order value"},"grossMargin":{"type":"number","description":"Gross margin"},"marginImpact":{"type":"number","description":"Margin impact"},"expectedBudgetConsumption":{"type":"string","description":"Expected budget consumption"},"roi":{"type":"string","description":"ROI"}}},
"CampaignGovernanceBudgetCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Governance & Budget Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeCampaigns":{"type":"integer","description":"Active Campaigns"},"campaignBudget":{"type":"string","description":"Campaign Budget"},"budgetConsumed":{"type":"string","description":"Budget Consumed"},"remainingBudget":{"type":"string","description":"Remaining Budget"},"discountExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Exposure"},"redemptionValue":{"type":"string","description":"Redemption Value"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Generated"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental Revenue"},"campaignRoi":{"type":"string","description":"Campaign ROI"},"campaignsNearBudgetLimit":{"type":"integer","description":"Campaigns Near Budget Limit"},"pendingApprovals":{"type":"integer","description":"Pending Approvals"},"suspendedCampaigns":{"type":"integer","description":"Suspended Campaigns"},"budgetHealth":{"type":"string","enum":["healthy","monitor","warning","critical","budgetExhausted","suspended"],"description":"Campaign budget health."},"utilization":{"type":"number","description":"Budget utilisation, percent"}}},
"CommercialCampaign": {"x-ticvai-persistence":"promotions.campaign + promotions.campaign_budget","type":"object","description":"A commercial campaign: the grouping of promotions, coupon campaigns and bundles that share an owner, a business entity, dates and a budget. **Not `marketing.campaign`**, which is the CRM send campaign in another service. The header is saved with its budget lines by setCampaignBudgetFinancial (the budget screen is where the pack captures campaign, owner, business entity and effective dates), and on its own by createCommercialCampaign and updateCommercialCampaign; listCommercialCampaigns lists it (decided 29 September, writers pass); promotions, coupon campaigns and bundles point at it by `campaignId`. No status of its own: a campaign is live while its promotions are, and a threshold action that stops it pauses them. (DM5, 29 September: data model for the agreed operations)","required":["id","venueId","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"budgets":{"type":"array","description":"The rows of `promotions.campaign_budget`, one per budget line.","items":{"$ref":"#/components/schemas/CampaignBudget"}}}},
"CreateCommercialCampaignRequest": {"x-ticvai-persistence":"none — request only; saved as a `promotions.campaign` row (CommercialCampaign)","type":"object","description":"What createCommercialCampaign takes: the campaign header only. Budget lines are set by setCampaignBudgetFinancial. (decided 29 September, writers pass)","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true,"description":"Unique at the venue when given."},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}},
"GovernanceAuditAiRiskLaunchReadinessView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Governance Audit, AI Risk & Launch Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promotionConfiguration":{"type":"string","description":"Promotion Configuration ✓"},"eligibility":{"type":"string","description":"Eligibility ✓"},"stackingRules":{"type":"string","description":"Stacking Rules ✓"},"budget":{"type":"string","description":"Budget ✓"},"redemptionLimits":{"type":"string","description":"Redemption Limits ✓"},"marginGuardrail":{"type":"number","description":"Margin Guardrail ✓"},"simulationCompleted":{"type":"string","description":"Simulation Completed ✓"},"requiredApproval":{"type":"string","description":"Required Approval ✓"},"channelPublication":{"type":"string","description":"Channel Publication ✓"},"auditRequirements":{"type":"string","description":"Audit Requirements ✓"},"budgetCreation":{"type":"string","description":"Budget creation"},"budgetChange":{"type":"string","description":"Budget change"},"limitChanges":{"type":"integer","description":"Limit changes"},"approvalSubmissions":{"type":"string","description":"Approval submissions"},"approvalDecisions":{"type":"string","description":"Approval decisions"},"overrides":{"type":"string","description":"Overrides"},"automaticSuspension":{"type":"string","description":"Automatic suspension"},"reactivation":{"type":"string","description":"Reactivation"},"simulationResults":{"type":"string","description":"Simulation results"},"experimentChanges":{"type":"string","description":"Experiment changes"},"campaignLaunch":{"type":"string","description":"Campaign launch"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PromotionVariant": {"x-ticvai-persistence":"promotions.promotion_variant","type":"object","description":"One arm of a promotion A/B test (BL-114), written by `setPromotionVariants`. **Stored as rows** because the split has to be read back at evaluation time. The body used to be a free object with no table behind it, so the variants a caller set could not be persisted.\n","required":["label","trafficPercent"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"promotionId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path."},"label":{"type":"string"},"trafficPercent":{"type":"integer","minimum":0,"maximum":100,"description":"Share of traffic. All variants of a promotion sum to 100, with no minimum per variant (decided 28 September, audit R101)."},"discountPercent":{"type":"number"}}},
"RedemptionDiscountExposureLimitManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Redemption, Discount & Exposure Limit Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"typesType":{"type":"string","enum":["maximumRedemptions","maximumDiscountValue","maximumDiscount","maximumRewardQuantity","maximumFreeTickets","maximumFreeProducts","maximumTransactions","maximumCustomers","maximumRedemptionsPerCustomer","maximumDailyExposure"],"description":"Vocabulary listed under Limit Types."},"maximumRedemptions":{"type":"integer","description":"Maximum redemptions (the pack shows 50,000)"},"maximumCustomerRedemption":{"type":"string","description":"Maximum customer redemption (the pack shows 2)"},"dailyRedemptionLimit":{"type":"integer","description":"Daily redemption limit (the pack shows 5,000)"}}},
"ThresholdActionsAutomaticSuspensionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Threshold Actions & Automatic Suspension displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"campaignId":{"type":"string","description":"Campaign ID"},"thresholdPercent":{"type":"number","description":"Budget threshold, percent"},"action":{"type":"string","enum":["warn","requireApproval","reduceAllocation","stopSpecificChannel","stopPartner","stopPromotion","stopCampaign","allowGraceAmount","continueWithExecutiveAuthorization"],"description":"Configured action when the threshold is reached"}}}
}
```
