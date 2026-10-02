# WS58 — Sales Channel Management board 2

**10 screens · 18 operations · 20 schemas · 5 permissions**

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
  `AI_APPROVE, CAPACITY_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-268` | Channel Operations Command Center | B–D | 0 | 24 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `ADM-269` | Channel Connection & Integration Manager | B–D | 33 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-270` | Product, Price & Availability Synchronization | B–D | 6 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-271` | Real-Time Channel Availability & Inventory Monitor | B–D | 0 | 14 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `ADM-272` | Channel Allocation & Rebalancing Operations | B–D | 15 | 18 | 6 | 9 | 1 | 0 | — | notStarted (generated) |
| `ADM-273` | Channel Exceptions, Incidents & Recovery | B–D | 16 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-274` | Channel Performance & Commercial Analytics | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-275` | Channel Audit, Logs & Transaction Traceability | B–D | 2 | 4 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-276` | Channel Governance, SLA & Partner Control | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-277` | AI Channel Optimization & Intelligence Center | B–D | 4 | 6 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-271 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-268` Channel Operations Command Center

**Provide a real-time operational view of all active TICVAI sales channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each channel should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-operations-command-center-adm-268` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Live view of active channels: health, sales, sync status, incidents, and AI optimisation signals.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | radio group | — | Capacity · Channel · Schedule · Commercial · Operational | `listChannel2` ?category |
| Channel | text field | — | — | `listChannel2` ?channel |
| Status | select | — | Proposed · Accepted · Modified · Rejected · Scheduled · Assigned | `listChannel2` ?status |
| Type | select | — | B2C web · B2C mobile app · POS · Mobile POS · Flying POS · Kiosk · Call centre · B2B portal · Reseller · Ota · API · Partner portal … | `listChannel` ?type |
| Health status | select | — | Healthy · Warning · Degraded · Critical · Offline · Maintenance | `listChannel` ?healthStatus |
| Venue | text field | — | — | `listChannel` ?venue |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Channels** (metric tile)

**Connected Channels** (metric tile)

**Degraded Channels** (metric tile)

**Offline Channels** (metric tile)

**Transactions Today** (metric tile)

**Gross Sales** (metric tile)

**Products Available** (metric tile)

**Synchronization Errors** (metric tile)

**Capacity Alerts** (metric tile)

**Pricing Errors** (metric tile)

**Failed Transactions** (metric tile)

**Open Operational Incidents** (metric tile)

**Every channel operations** (data table, from `listChannel`)

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Type | chip: B2C web, B2C mobile app, POS, Mobile POS, Flying POS, Kiosk… | Type: the channel type |
| Venue scope | text | Venue/Scope |
| Connection status | text | Connection Status: connected, degraded, offline or maintenance |
| Last sync | 1 Oct 2026, 14:30 | Last Sync |
| Products | 1,234 | Products available on the channel |
| Transactions | 1,234 | Transactions today |
| Sales value | AED 1,234.50 | Sales Value today |
| Inventory status | text | Inventory Status: ok, low, soldOut or syncError (decided 29 September, readiness close-out) |
| Pricing status | text | Pricing Status: ok, mismatch or error (decided 29 September, readiness close-out) |
| Error count | 1,234 | Error Count today |
| Health score | 1,234.5 | Health Score, 0-100 |

**The selected channel operations** (detail panel): The pack groups this record's detail under its own headings: “Use”, “Show important events such as”.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Type | chip: B2C web, B2C mobile app, POS, Mobile POS, Flying POS, Kiosk… | Type: the channel type |
| Venue scope | text | Venue/Scope |
| Connection status | text | Connection Status: connected, degraded, offline or maintenance |
| Last sync | 1 Oct 2026, 14:30 | Last Sync |
| Products | 1,234 | Products available on the channel |
| Transactions | 1,234 | Transactions today |
| Sales value | AED 1,234.50 | Sales Value today |
| Inventory status | text | Inventory Status: ok, low, soldOut or syncError (decided 29 September, readiness close-out) |
| Pricing status | text | Pricing Status: ok, mismatch or error (decided 29 September, readiness close-out) |
| Error count | 1,234 | Error Count today |
| Health score | 1,234.5 | Health Score, 0-100 |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Open Channel, Force Sync, Pause Channel, Resume Channel, Open Incident, View Logs, View Transactions, View Performance. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel health**: One card per channel with status light, sales today, last sync, open incidents. *(source: contracts/spine/catalogue.yaml#listChannel)*

**Data it reads**: `listChannel2` (onLoad, AI Channel Optimization & Intelligence Center); `listChannel` (onLoad, Channel Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-269` Channel Connection & Integration Manager: *Works in Channel Connection & Integration Manager*; calls `listChannel`
- → `ADM-270` Product, Price & Availability Synchronization: *Works in Product, Price & Availability Synchronization*; calls `listChannel`
- → `ADM-271` Real-Time Channel Availability & Inventory Monitor: *Works in Real-Time Channel Availability & Inventory Monitor*; calls `listChannel`
- → `ADM-272` Channel Allocation & Rebalancing Operations: *Works in Channel Allocation & Rebalancing Operations*; calls `listChannel`
- → `ADM-273` Channel Exceptions, Incidents & Recovery: *Works in Channel Exceptions, Incidents & Recovery*; calls `listChannel`
- → `ADM-274` Channel Performance & Commercial Analytics: *Works in Channel Performance & Commercial Analytics*; calls `listChannel`
- → `ADM-275` Channel Audit, Logs & Transaction Traceability: *Works in Channel Audit, Logs & Transaction Traceability*; calls `listChannel`
- → `ADM-276` Channel Governance, SLA & Partner Control: *Works in Channel Governance, SLA & Partner Control*; calls `listChannel`
- → `ADM-277` AI Channel Optimization & Intelligence Center: *Works in AI Channel Optimization & Intelligence Center*; calls `listChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  channel: Klook
  status: degraded
  salesToday: 84
  lastSync: 22 min ago
  incidents: 1
```

#### Permissions

- `listChannel2` → `PRODUCT_VIEW` (read) · staff
- `listChannel` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.32 | System shall support dynamic adjustment of ticket inventory and capacity based on demand forecasts, operational capacity and business rules. | Ticketing Catalogue | CONTRACTED_PARTIAL | `listChannel2` |
| 2.7.54 | AI shall recommend optimal allocation of inventory and quotas across B2B partners based on sales performance, demand forecasts, unused allocation, partner ranking, seasonality, event capacity, and … | Ticketing Sales | CONTRACTED_PARTIAL | `listChannel2` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-268` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-268`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 1: Opens Channel Operations Command Center → Provide a real-time operational view of all active TICVAI sales channels.
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F167 branch at step 1 (expected): when Nothing has been set up on Channel Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F167 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-268?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-269`, `ADM-270`, `ADM-271`, `ADM-272`, `ADM-273`, `ADM-274`, `ADM-275`, `ADM-276`, `ADM-277`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-269` Channel Connection & Integration Manager

**Configure and manage the technical connection between TICVAI and external or internal sales channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `connectionId` (navigation) |
| Route | `/commercial/channel-connection-integration-manager-adm-269` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The technical connection to each channel per environment (sandbox, UAT, production), with a test now and the latest test results; credentials never shown.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Connector Name | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| Endpoint | select field | — | — | — | — | — | — |
| API Version | select field | — | — | — | — | — | — |
| Authentication Type | select field | — | — | — | — | — | — |
| Credentials reference | select field | — | — | — | — | — | — |
| Certificate | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Retry Policy | select field | — | — | — | — | — | — |
| Rate Limit | select field | — | — | — | — | — | — |
| IP Restrictions | select field | — | — | — | — | — | — |
| Connection Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelConnectionIntegration` ?channel |
| Partner | text field | — | — | `listChannelConnectionIntegration` ?partner |
| Connection type | select | — | Ticvai native · Rest API · Webhook · Ota adapter · Reseller API · Partner API · Middleware · File sftp · Custom connector | `listChannelConnectionIntegration` ?connectionType |
| Environment | segmented control | — | Sandbox · Uat · Production | `listChannelConnectionIntegration` ?environment |

**Form: Save channel connection configuration** (modal, opened by *Save channel connection configuration*; *Save channel connection configuration* calls `setChannelConnectionConfiguration`, *Cancel* sends nothing)

**Collects what `setChannelConnectionConfiguration` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `connectorName`, `environment`, `connectionType`. Optional: `partner`, `direction`, `endpoint`, `apiVersion`, `authenticationType`, `credentialsReference`, `certificateReference`, `certificateExpiresAt`, `timeoutMs`, `rateLimitPerMinute`, `ipRestrictions`, `retryPolicy` and 3 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sales channel `salesChannelId` | picker: choose a sales channel | required | — | — | shows names, sends the id | — | `setChannelConnectionConfiguration` body |
| Connector name `connectorName` | text field | required | — | max length 200 | — | — | `setChannelConnectionConfiguration` body |
| Partner `partner` | text field | optional | — | max length 200 | — | — | `setChannelConnectionConfiguration` body |
| Environment `environment` | segmented control | required | — | Sandbox · Uat · Production | — | — | `setChannelConnectionConfiguration` body |
| Connection type `connectionType` | select | required | — | Ticvai native · Rest API · Webhook · Ota adapter · Reseller API · Partner API · Middleware · File sftp · Custom connector | — | — | `setChannelConnectionConfiguration` body |
| Direction `direction` | segmented control | optional | Outbound | Outbound · Inbound · Bidirectional | — | — | `setChannelConnectionConfiguration` body |
| Endpoint `endpoint` | text area | optional | — | max length 500 | — | — | `setChannelConnectionConfiguration` body |
| API version `apiVersion` | text field | optional | — | max length 40 | — | — | `setChannelConnectionConfiguration` body |
| Authentication type `authenticationType` | select | optional | — | None · Oauth · API key · Client credentials · Certificate · Signed request | — | — | `setChannelConnectionConfiguration` body |
| Credentials reference `credentialsReference` | text field | optional | — | max length 200 | — | A vault reference, never the secret. | `setChannelConnectionConfiguration` body |
| Certificate reference `certificateReference` | text field | optional | — | max length 200 | — | — | `setChannelConnectionConfiguration` body |
| Certificate expires at `certificateExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelConnectionConfiguration` body |
| Timeout ms `timeoutMs` | number field | optional | — | min 1 | — | — | `setChannelConnectionConfiguration` body |
| Rate limit per minute `rateLimitPerMinute` | number field | optional | — | min 1 | — | — | `setChannelConnectionConfiguration` body |
| Ip restrictions `ipRestrictions` | list of values (chips) | optional | — | — | — | — | `setChannelConnectionConfiguration` body |
| Retry policy `retryPolicy` | key and value settings | optional | — | — | — | `{maxAttempts, backoffSeconds}`. | `setChannelConnectionConfiguration` body |
| Adapter `adapterId` | text field | optional | — | max length 100 | — | — | `setChannelConnectionConfiguration` body |
| Connection status `connectionStatus` | radio group | optional | Not tested | Not tested · Connected · Degraded · Offline · Disabled | — | — | `setChannelConnectionConfiguration` body |

Errors to draw in the form: 422 `secretNotReference`.

**Form: Test channel connection** (modal, opened by *Test channel connection*; *Test channel connection* calls `testChannelConnection`, *Cancel* sends nothing)

**Collects what `testChannelConnection` sends before it is called.** Nothing in the body is required. Optional: `tests`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tests `tests` | multi-select chips | optional | — | Connectivity · Authentication · Product sync · Availability · Pricing · Order creation · Cancellation · Webhook | — | The tests to run; all that apply to the connection type when omitted. | `testChannelConnection` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `connectionDisabled`.; 422 `orderTestInProduction`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| TICVAI Native (primary button) | navigation or local | — | — | — | — |
| REST API (secondary button) | navigation or local | — | — | — | — |
| Webhook (secondary button) | navigation or local | — | — | — | — |
| Reseller API (secondary button) | navigation or local | — | — | — | — |
| Partner API (secondary button) | navigation or local | — | — | — | — |
| File/SFTP where required (secondary button) | navigation or local | — | — | — | — |
| Save channel connection configuration (secondary button) | `setChannelConnectionConfiguration` PUT `/channel-connections` | ChannelConnection | ChannelConnection | 422 `secretNotReference`. | gated `PRODUCT_CONFIGURE`; opens modal first |
| Test channel connection (secondary button) | `testChannelConnection` POST `/channel-connections/{connectionId}/test` | inline | ChannelConnection | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `connectionDisabled`.; 422 `orderTestInProduction`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Test connection**: Runs the tests and records each result; overall status updates. *(source: contracts/spine/catalogue.yaml#testChannelConnection)*

**Data it reads**: `listChannelConnectionIntegration` (onLoad, Channel Connection & Integration Manager)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelConnectionIntegration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel connection integration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel connection integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel connection integration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `connectionDisabled`.; 422 `orderTestInProduction`.; 422 `secretNotReference`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
connection:
  channel: Klook
  environment: production
  status: connected
  lastTest: passed 09:00
```

#### Permissions

- `listChannelConnectionIntegration` → `PRODUCT_VIEW` (read) · staff
- `setChannelConnectionConfiguration` → `PRODUCT_CONFIGURE` (configure) · staff
- `testChannelConnection` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-269` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-269`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 2: Works in Channel Connection & Integration Manager → Configure and manage the technical connection between TICVAI and external or internal sales channels.

#### Acceptance for the design

- [ ] Every input above is drawn (33), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-269?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: TICVAI Native, REST API, Webhook, Reseller API, Partner API, File/SFTP where required, Save channel connection configuration, Test channel connection.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-270` Product, Price & Availability Synchronization

**Control how TICVAI distributes commercial information to connected channels and receives supported updates.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/product-price-availability-synchronization-adm-270` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen; 1 are served since the writers pass (29 September): Channel → TICVAI by `setChannelSyncSetting`.** Still unserved: Sync Now, Retry Failed, Compare …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How product, description, schedule, availability, capacity and price synchronise with each connected channel: direction, frequency, paused or not.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listProductPriceAvailability` ?channel |
| Domain | select | — | Product · Product description · Schedule · Availability · Capacity · Price · Tax · Fees · Media · Restrictions · Sales status | `listProductPriceAvailability` ?domain |
| Frequency | radio group | — | Real time · Near real time · Scheduled · Manual · Event triggered | `listProductPriceAvailability` ?frequency |
| Has failures | toggle | — | — | `listProductPriceAvailability` ?hasFailures |

**Form: Save channel sync setting** (modal, opened by *Save channel sync setting*; *Save channel sync setting* calls `setChannelSyncSetting`, *Cancel* sends nothing)

**Collects what `setChannelSyncSetting` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `domain`. Optional: `channelConnectionId`, `direction`, `frequency`, `isPaused`, `lastSuccessfulSyncAt`, `nextSyncAt`, `recordsProcessed`, `successful`, `failed`, `pending`, `warnings`, `durationMs` and 1 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sales channel `salesChannelId` | picker: choose a sales channel | required | — | — | shows names, sends the id | — | `setChannelSyncSetting` body |
| Channel connection `channelConnectionId` | picker: choose a channel connection | optional | — | — | shows names, sends the id | — | `setChannelSyncSetting` body |
| Domain `domain` | select | required | — | Product · Product description · Schedule · Availability · Capacity · Price · Tax · Fees · Media · Restrictions · Sales status | — | — | `setChannelSyncSetting` body |
| Direction `direction` | segmented control | optional | Ticvai to channel | Ticvai to channel · Channel to ticvai · Bidirectional | — | — | `setChannelSyncSetting` body |
| Frequency `frequency` | radio group | optional | Near real time | Real time · Near real time · Scheduled · Manual · Event triggered | — | — | `setChannelSyncSetting` body |
| Is paused `isPaused` | toggle | optional | off | — | — | — | `setChannelSyncSetting` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **sync per domain**: Domains as rows, direction and frequency per channel; the push interval is the oversell window (label it). *(source: contracts/spine/catalogue.yaml#setChannelSyncSetting / contracts/satellite/subscription.yaml#setChannelListing)*

#### Outputs: what the screen shows and produces

**Shown**

**Every product price availability** (data table, from `listProductPriceAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Last successful sync | 1 Oct 2026, 14:30 | Last Successful Sync |
| Next sync | 1 Oct 2026, 14:30 | Next Sync; empty for manual |
| Records processed | 1,234 | Records Processed in the last run |
| Successful | 1,234 | Successful |
| Failed | 1,234 | Failed |
| Pending | 1,234 | Pending |
| Warning | 1,234 | Warning: records synced with a warning |
| Duration | 1,234 | Duration of the last run in seconds |

**The selected product price availability** (detail panel): The pack groups this record's detail under its own headings: “Manage”, “Bidirectional”, “Mismatch”.

| Shows | Format | Notes |
|---|---|---|
| Last successful sync | 1 Oct 2026, 14:30 | Last Successful Sync |
| Next sync | 1 Oct 2026, 14:30 | Next Sync; empty for manual |
| Records processed | 1,234 | Records Processed in the last run |
| Successful | 1,234 | Successful |
| Failed | 1,234 | Failed |
| Pending | 1,234 | Pending |
| Warning | 1,234 | Warning: records synced with a warning |
| Duration | 1,234 | Duration of the last run in seconds |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Channel → TICVAI (primary button) | navigation or local | — | — | — | — |
| Sync Now (secondary button) | navigation or local | — | — | — | — |
| Retry Failed (secondary button) | navigation or local | — | — | — | — |
| Compare (secondary button) | navigation or local | — | — | — | — |
| Reprocess (secondary button) | navigation or local | — | — | — | — |
| Pause Sync (secondary button) | navigation or local | — | — | — | — |
| Resume (secondary button) | navigation or local | — | — | — | — |
| Export Error (secondary button) | navigation or local | — | — | — | — |
| Save channel sync setting (secondary button) | `setChannelSyncSetting` PUT `/channel-syncs` | ChannelSync | ChannelSync | — | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listProductPriceAvailability` (onLoad, Product, Price & Availability Synchronization)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listProductPriceAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product price availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product price availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product price availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product price availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sync:
  channel: Klook
  availability: push every 5 min
  price: push on change
  product: manual
```

#### Permissions

- `listProductPriceAvailability` → `PRODUCT_VIEW` (read) · staff
- `setChannelSyncSetting` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-270` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-270`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 4: Works in Product, Price & Availability Synchronization → Control how TICVAI distributes commercial information to connected channels and receives supported updates.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-270?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Channel → TICVAI, Sync Now, Retry Failed, Compare, Reprocess, Pause Sync, Resume, Export Error, Save channel sync setting.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-271` Real-Time Channel Availability & Inventory Monitor

**Provide operations with a live view of what each channel can currently sell.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/real-time-channel-availability-inventory-monitor-adm-271` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What each channel can sell right now: remaining allocation and availability per product and date.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listRealTimeAvailability return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | text field | — | — | `listRealTimeChannel` ?product |
| Channel | text field | — | — | `listRealTimeChannel` ?channel |
| Event | text field | — | — | `listRealTimeChannel` ?event |
| Availability status | select | — | Available · Low availability · Sold out · Closed · Suspended · Not assigned · Sync error | `listRealTimeChannel` ?availabilityStatus |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every real-time channel availability** (data table, from `listRealTimeChannel`)

| Shows | Format | Notes |
|---|---|---|
| Allocated | 1,234 | Allocated; empty when the channel sells from the shared pool |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining sellable units |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Sales velocity | 1,234.5 | Sales Velocity: units sold per hour over the last 24 hours (decided 29 September, readiness close-out) |
| Forecasted sell out | 1 Oct 2026, 14:30 | Forecasted Sell-Out; empty when no sell-out is forecast |

**The selected real-time channel availability** (detail panel): The pack groups this record's detail under its own headings: “B2C POS Kiosk”, “Adult 420 180”, “Child 610 160 75”, “For every product/channel combination”, “Seat Map”.

| Shows | Format | Notes |
|---|---|---|
| Allocated | 1,234 | Allocated; empty when the channel sells from the shared pool |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining sellable units |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Sales velocity | 1,234.5 | Sales Velocity: units sold per hour over the last 24 hours (decided 29 September, readiness close-out) |
| Forecasted sell out | 1 Oct 2026, 14:30 | Forecasted Sell-Out; empty when no sell-out is forecast |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **live availability**: Channels as columns, products and dates as rows. *(source: contracts/spine/catalogue.yaml#listRealTimeChannel)*

**Data it reads**: `listRealTimeChannel` (onLoad, Real-Time Channel Availability & Inventory Monitor); `listRealTimeAvailability` (onLoad, Real-Time Availability & Checkout Validation)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listRealTimeChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time channel availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time channel availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time channel availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time channel availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  product: Day Pass Sat 22 Nov
  Website: 412
  Klook: 38
  Point of sale: 600
```

#### Permissions

- `listRealTimeChannel` → `PRODUCT_VIEW` (read) · staff
- `listRealTimeAvailability` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-271` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-271`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 6: Works in Real-Time Channel Availability & Inventory Monitor → Provide operations with a live view of what each channel can currently sell.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-271?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-272` Channel Allocation & Rebalancing Operations

**Allow authorized users to operationally adjust inventory allocations as demand changes. Board 1 defines the allocation rules. Board 2 manages those allocations during live operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `channelCapacityId` (navigation) |
| Route | `/commercial/channel-allocation-rebalancing-operations-adm-272` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Adjust channel allocations during live trading as demand changes, within the rules of ADM-262.

**Fixed on main** (the package already carries these; draw what it says): Rebalancing has no write here; setChannelAllocations (BO-013) is the writer. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Event | text field | — | — | `listChannelAllocationRebalancing` ?event |
| Product | text field | — | — | `listChannelAllocationRebalancing` ?product |
| Channel | text field | — | — | `listChannelAllocationRebalancing` ?channel |

**Form: Rebalance allocation** (modal, opened by *Rebalance allocation*; *Rebalance allocation* calls `setChannelAllocations`, *Cancel* sends nothing)

**Collects what `setChannelAllocations` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Allocations `allocations` | repeatable rows | required | — | at least 1 | — | — | `setChannelAllocations` body |
| Channel `allocations[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `setChannelAllocations` body |
| Allocated units `allocations[].allocatedUnits` | number field | required | — | min 0 | — | — | `setChannelAllocations` body |
| Release at `allocations[].releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it. | `setChannelAllocations` body |
| Sales channel `allocations[].salesChannelId` | picker: choose a sales channel | optional | — | — | shows names, sends the id | The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3). | `setChannelAllocations` body |
| Allocation type `allocations[].allocationType` | radio group | optional | Dedicated | Shared pool · Dedicated · Percentage · Dynamic | — | How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row. | `setChannelAllocations` body |
| Minimum units `allocations[].minimumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Maximum units `allocations[].maximumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Replenishment rule `allocations[].replenishmentRule` | key and value settings | optional | — | — | — | `{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`. | `setChannelAllocations` body |
| Waitlist behavior `allocations[].waitlistBehavior` | segmented control | optional | None | None · Join waitlist · Notify on release | — | — | `setChannelAllocations` body |
| Release threshold units `allocations[].releaseThresholdUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Release hours before event `allocations[].releaseHoursBeforeEvent` | number field | optional | — | min 0 | — | Alternative to `releaseAt`, relative to the performance start. | `setChannelAllocations` body |
| Contractual units `allocations[].contractualUnits` | number field | optional | — | min 0 | — | Units a partner agreement guarantees; rebalancing never goes below it. | `setChannelAllocations` body |
| Minimum guaranteed units `allocations[].minimumGuaranteedUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Is frozen `allocations[].isFrozen` | toggle | optional | off | — | — | Excluded from rebalancing. | `setChannelAllocations` body |

Errors to draw in the form: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101)

#### Outputs: what the screen shows and produces

**Shown**

**Every channel allocation rebalancing** (data table, from `listChannelAllocationRebalancing`)

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Initial allocation | 1,234 | Initial Allocation |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Sales velocity | 1,234.5 | Sales Velocity: units per hour over the last 24 hours (decided 29 September, readiness close-out) |
| Forecast | 1,234 | Forecast: units the channel is expected to sell by the event |
| Recommended allocation | 1,234 | Recommended Allocation (advisory) |

**The selected channel allocation rebalancing** (detail panel): The pack groups this record's detail under its own headings: “OTA”, “B2C”, “Reallocation must respect”, “Approval”.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Initial allocation | 1,234 | Initial Allocation |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Sales velocity | 1,234.5 | Sales Velocity: units per hour over the last 24 hours (decided 29 September, readiness close-out) |
| Forecast | 1,234 | Forecast: units the channel is expected to sell by the event |
| Recommended allocation | 1,234 | Recommended Allocation (advisory) |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Increase allocation, Reduce allocation, Return inventory, Transfer allocation, Release hold, Move to shared pool, Freeze allocation. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Rebalance allocation (secondary button) | `setChannelAllocations` PUT `/channel-capacities/{channelCapacityId}/channel-allocations` | inline | ChannelAllocationSet | 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rebalancing view**: Per channel sold, allocated, remaining and pace; suggested moves. *(source: contracts/spine/catalogue.yaml#listChannelAllocationRebalancing)*

**Data it reads**: `listChannelAllocationRebalancing` (onLoad, Channel Allocation & Rebalancing Operations)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelAllocationRebalancing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel allocation rebalancing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel allocation rebalancing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel allocation rebalancing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel allocation rebalancing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
move:
  from: B2B partners
  to: Website
  units: 50
  reason: B2B pace 30% below target
```

#### Permissions

- `listChannelAllocationRebalancing` → `PRODUCT_VIEW` (read) · staff
- `setChannelAllocations` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.10 | The system should allow the capacity for all type of ticket to be configurable. Capacity of a ticket can be configurable at multiple levels: 1) Sales Capacity: Allow only a fixed number of tickets to … | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 1.1.127 | Maximum sellable quantity controls | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 2.1.1 | The system should have the ability to create as many sales channels as necessary by the system admin. Sales Channels creation should involve capture of all required data such as account assignment … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.2 | The system should support the configuration of products, prices, quotas, sales limits and sales schedule for each sales channels. Some sales channels can be configured to be accessible to only … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.3 | The system should store and manage all rules for product compatibility, eligibility and pricing that will be applicable to for each sales channel. These rules will be part of the system and not … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.5 | For BtoB online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.11 | - Only BtoB PLUs | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.15 | - Quotas can be applied for one Customer or a category of Customers | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 7.3.3 | Channel-based & slot-based inventory controls to stop OTAs or B2B partners overselling peak capacity | F&B POS | CONTRACTED | `setChannelAllocations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory centralised or split per channel by percentage/quantity (e.g. 50% online / 50% onsite). Qossai: automatic migration rules, e.g. when B2C sells out pull a configured 20% from B2B, in the same configuration area. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-581)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-272` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-272`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 8: Works in Channel Allocation & Rebalancing Operations → Allow authorized users to operationally adjust inventory allocations as demand changes. Board 1 defines the allocation rules. Board 2 manages those allocations during live operations.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-272?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Rebalance allocation.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-273` Channel Exceptions, Incidents & Recovery

**Provide one operational workspace for resolving channel problems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `incidentId` (navigation) |
| Route | `/commercial/channel-exceptions-incidents-recovery-adm-273` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Connection Failure, Product Sync Failure, Pricing Mismatch, Inventory Mismatch, Order Failure, Payment …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Channel problems in one workspace: own, investigate, retry the failed call, resolve, close, with SLA.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Connection Failure, Product Sync Failure, Pricing Mismatch, Inventory Mismatch, Order Failure, Payment Error, Duplicate Transaction, Partner Error. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Incident ID | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Severity | select field | — | — | — | — | — | — |
| Error Type | select field | — | — | — | — | — | — |
| Affected Product/Event | select field | — | — | — | — | — | — |
| Transactions Affected | select field | — | — | — | — | — | — |
| Business Impact | select field | — | — | — | — | — | — |
| First Detected | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| SLA | select field | — | — | — | — | — | — |
| Current Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelExceptionIncident` ?channel |
| Partner | text field | — | — | `listChannelExceptionIncident` ?partner |
| Severity | radio group | — | Critical · High · Medium · Low | `listChannelExceptionIncident` ?severity |
| Error type | select | — | Connection failure · Authentication failure · Product sync failure · Pricing mismatch · Inventory mismatch · Order failure · Payment error · Timeout · Cancellation failure · Duplicate transaction · Fulfillment failure · Rate limit … | `listChannelExceptionIncident` ?errorType |
| Current status | select | — | Open · Assigned · Investigating · Recovering · Resolved · Closed | `listChannelExceptionIncident` ?currentStatus |

**Form: Save channel incident** (modal, opened by *Save channel incident*; *Save channel incident* calls `updateChannelIncident`, *Cancel* sends nothing)

**Collects what `updateChannelIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `ownerPrincipalId`, `slaDueAt`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | optional | — | Investigating · Resolved · Closed | — | — | `updateChannelIncident` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `updateChannelIncident` body |
| Sla due at `slaDueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateChannelIncident` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 1000 | — | — | `updateChannelIncident` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `resolutionNoteRequired`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Connection Failure (primary button) | navigation or local | — | — | — | — |
| Product Sync Failure (secondary button) | navigation or local | — | — | — | — |
| Pricing Mismatch (secondary button) | navigation or local | — | — | — | — |
| Inventory Mismatch (secondary button) | navigation or local | — | — | — | — |
| Order Failure (secondary button) | navigation or local | — | — | — | — |
| Payment Error (secondary button) | navigation or local | — | — | — | — |
| Duplicate Transaction (secondary button) | navigation or local | — | — | — | — |
| Partner Error (secondary button) | navigation or local | — | — | — | — |
| Save channel incident (secondary button) | `updateChannelIncident` PATCH `/channel-incidents/{incidentId}` | inline | ChannelIncident | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `resolutionNoteRequired`. | gated `PRODUCT_CONFIGURE`; opens modal first |
| Retry channel incident (secondary button) | `retryChannelIncident` POST `/channel-incidents/{incidentId}/retry` | — | ChannelIncident | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `notRetryable`. | gated `PRODUCT_CONFIGURE` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Retry**: Queues the failed call again with the same id; retry count increments. *(source: contracts/spine/catalogue.yaml#retryChannelIncident)*
- **Own / Resolve / Close**: Moves the incident along its states with owner and SLA due time. *(source: contracts/spine/catalogue.yaml#updateChannelIncident)*

**Data it reads**: `listChannelExceptionIncident` (onLoad, Channel Exceptions, Incidents & Recovery)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelExceptionIncident`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel exceptions incidents configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel exceptions incidents untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel exceptions incidents configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `illegalTransition`.; 409 `notRetryable`.; 422 `resolutionNoteRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident:
  channel: Klook
  severity: high
  error: Availability push rejected 401
  retries: 2
  sla: 45 min left
```

#### Permissions

- `listChannelExceptionIncident` → `PRODUCT_VIEW` (read) · staff
- `updateChannelIncident` → `PRODUCT_CONFIGURE` (configure) · staff
- `retryChannelIncident` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-273` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-273`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 10: Works in Channel Exceptions, Incidents & Recovery → Provide one operational workspace for resolving channel problems.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-273?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Connection Failure, Product Sync Failure, Pricing Mismatch, Inventory Mismatch, Order Failure, Payment Error, Duplicate Transaction, Partner Error, Save channel incident, Retry channel incident.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-274` Channel Performance & Commercial Analytics

**Compare the commercial effectiveness of TICVAI sales channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-performance-commercial-analytics-adm-274` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Channel effectiveness compared: sales, revenue, cost of sale, conversion, cancellations per channel.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search channel performance commercial | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, channel, partner, country and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listChannelPerformanceCommercial` ?venue |
| Event | text field | — | — | `listChannelPerformanceCommercial` ?event |
| Product | text field | — | — | `listChannelPerformanceCommercial` ?product |
| Channel | text field | — | — | `listChannelPerformanceCommercial` ?channel |
| Partner | text field | — | — | `listChannelPerformanceCommercial` ?partner |
| Country | text field | — | — | `listChannelPerformanceCommercial` ?country |
| Customer segment | text field | — | — | `listChannelPerformanceCommercial` ?customerSegment |
| Date from | date picker | — | — | `listChannelPerformanceCommercial` ?dateFrom |
| Date to | date picker | — | — | `listChannelPerformanceCommercial` ?dateTo |
| Time from | text field | — | — | `listChannelPerformanceCommercial` ?timeFrom |
| Time to | text field | — | — | `listChannelPerformanceCommercial` ?timeTo |
| Currency | text field | — | — | `listChannelPerformanceCommercial` ?currency |

#### Outputs: what the screen shows and produces

**Shown**

**Gross Sales** (metric tile)

**Net Sales** (metric tile)

**Transactions** (metric tile)

**Tickets Sold** (metric tile)

**Average Order Value** (metric tile)

**Conversion Rate** (metric tile)

**Cancellation Rate** (metric tile)

**Refund Rate** (metric tile)

**Capacity Utilization** (metric tile)

**Revenue per Available Unit** (metric tile)

**Fees** (metric tile)

**Commission** (metric tile)

**Cost of Sale where available** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **comparison**: Channels as rows with net revenue after commission first. *(source: contracts/spine/catalogue.yaml#listChannelPerformanceCommercial)*

**Data it reads**: `listChannelPerformanceCommercial` (onLoad, Channel Performance & Commercial Analytics)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelPerformanceCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel performance commercial list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel performance commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel performance commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel performance commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  channel: Klook
  revenue: AED 84,000.00
  commission: AED 12,600.00
```

#### Permissions

- `listChannelPerformanceCommercial` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-274` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-274`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 12: Works in Channel Performance & Commercial Analytics → Compare the commercial effectiveness of TICVAI sales channels.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-274?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-275` Channel Audit, Logs & Transaction Traceability

**Provide complete traceability across channel configuration, synchronization and transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-audit-logs-transaction-traceability-adm-275` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Traceability across channel configuration, synchronisation and transactions.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search channel audit logs | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by channel, order id, transaction id, ticket, partner reference, product and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelLogTransaction` ?channel |
| Order | text field | — | — | `listChannelLogTransaction` ?orderId |
| Transaction | text field | — | — | `listChannelLogTransaction` ?transactionId |
| Ticket | text field | — | — | `listChannelLogTransaction` ?ticket |
| Partner reference | text field | — | — | `listChannelLogTransaction` ?partnerReference |
| Product | text field | — | — | `listChannelLogTransaction` ?product |
| Customer | text field | — | — | `listChannelLogTransaction` ?customer |
| Correlation | text field | — | — | `listChannelLogTransaction` ?correlationId |
| API request | text field | — | — | `listChannelLogTransaction` ?apiRequest |
| User | text field | — | — | `listChannelLogTransaction` ?user |
| Category | select | — | Configuration change · Activation · Suspension · Allocation change · Price assignment · Sync · Order · Cancellation · Error · Manual intervention · Integration change | `listChannelLogTransaction` ?category |
| From | date and time picker | — | — | `listChannelLogTransaction` ?from |
| To | date and time picker | — | — | `listChannelLogTransaction` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Every channel audit logs** (data table, from `listChannelLogTransaction`)

| Shows | Format | Notes |
|---|---|---|
| Category | chip: Configuration change, Activation, Suspension, Allocation change, Price assignment … | Audit Category (pack p.31) |
| Sync | text | not in the schema: `Sync` |

**The selected channel audit logs** (detail panel): The pack groups this record's detail under its own headings: “Transaction Trace”, “Partner Request”, “Export”.

| Shows | Format | Notes |
|---|---|---|
| Category | chip: Configuration change, Activation, Suspension, Allocation change, Price assignment … | Audit Category (pack p.31) |
| Sync | text | not in the schema: `Sync` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **log**: Filter by channel, kind, time; each sync and transaction with its correlation id. *(source: contracts/spine/catalogue.yaml#listChannelLogTransaction)*

**Data it reads**: `listChannelLogTransaction` (onLoad, Channel Audit, Logs & Transaction Traceability)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelLogTransaction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel audit logs list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel audit logs untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel audit logs yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel audit logs are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
log:
  at: '14:02:11'
  channel: Klook
  event: availability push
  result: ok
```

#### Permissions

- `listChannelLogTransaction` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-275` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-275`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 14: Works in Channel Audit, Logs & Transaction Traceability → Provide complete traceability across channel configuration, synchronization and transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-275?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-276` Channel Governance, SLA & Partner Control

**Govern live channels and ensure that internal/external channels operate within approved commercial and service conditions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure/monitor) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-governance-sla-partner-control-adm-276` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for channel governance, SLA and partner controls.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Live channels within approved commercial and service conditions: SLAs, partner obligations, breaches.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No write operation: a configuration screen (Channel Governance, SLA & Partner Control) declares only reads (listChannelGovernanceSla). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel Owner | select field | — | — | — | — | — | — |
| Partner Owner | select field | — | — | — | — | — | — |
| Commercial Agreement Reference | select field | — | — | — | — | — | — |
| SLA | select field | — | — | — | — | — | — |
| Transaction Limits | select field | — | — | — | — | — | — |
| Rate Limits | select field | — | — | — | — | — | — |
| Contract Dates | select field | — | — | — | — | — | — |
| Renewal Date | select field | — | — | — | — | — | — |
| Support Contacts | select field | — | — | — | — | — | — |
| Escalation Contacts | select field | — | — | — | — | — | — |
| Review Frequency | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelGovernanceSla` ?channel |
| Partner | text field | — | — | `listChannelGovernanceSla` ?partner |
| Compliance flag | select | — | Expired agreement · Expired certificate · Expiring API credentials · Missing owner · Unapproved production integration · Sla breach · Excessive transaction failures | `listChannelGovernanceSla` ?complianceFlag |
| Governance status | radio group | — | Normal · Under review · Restricted · Suspended | `listChannelGovernanceSla` ?governanceStatus |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **governance**: Each channel's SLA and current compliance. *(source: contracts/spine/catalogue.yaml#listChannelGovernanceSla)*

**Data it reads**: `listChannelGovernanceSla` (onLoad, Channel Governance, SLA & Partner Control)

**Where the user goes next**

- → `ADM-268` Channel Operations Command Center: *Returns to the board's landing screen*; calls `listChannelGovernanceSla`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel governance sla configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel governance sla untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel governance sla configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sla:
  channel: Klook
  availabilitySla: 99.5%
  actual: 98.9%
  breach: true
```

#### Permissions

- `listChannelGovernanceSla` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-276` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-276`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 16: Works in Channel Governance, SLA & Partner Control → Govern live channels and ensure that internal/external channels operate within approved commercial and service conditions.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-276?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-268`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-277` AI Channel Optimization & Intelligence Center

**Create the AI intelligence layer that looks across all sales channels together rather than optimizing each channel in isolation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze; Monitor) and no metric row |
| Offline | online only |
| Opens with | `findingId` (navigation) |
| Route | `/commercial/ai-channel-optimization-intelligence-center-adm-277` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Revenue impact, Risk. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI across all channels together: opportunities and risks, each decided by a person.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Revenue impact, Risk. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | radio group | — | Capacity · Channel · Schedule · Commercial · Operational | `listChannel2` ?category |
| Channel | text field | — | — | `listChannel2` ?channel |
| Status | select | — | Proposed · Accepted · Modified · Rejected · Scheduled · Assigned | `listChannel2` ?status |
| Type | select | — | B2C web · B2C mobile app · POS · Mobile POS · Flying POS · Kiosk · Call centre · B2B portal · Reseller · Ota · API · Partner portal … | `listChannel` ?type |
| Health status | select | — | Healthy · Warning · Degraded · Critical · Offline · Maintenance | `listChannel` ?healthStatus |
| Venue | text field | — | — | `listChannel` ?venue |

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

**Every channel optimization intelligence** (data table, from `listChannel2`)

| Shows | Format | Notes |
|---|---|---|
| Signals | list or chips (count when long) | AI Analysis signals behind the recommendation (pack p.33-34) |
| Channel allocation & rebalancing operational capacity | text | not in the schema: `Channel Allocation & Rebalancing Operational capacity` |
| 5 | text | not in the schema: `4.2.5` |

**The selected channel optimization intelligence** (detail panel): The pack groups this record's detail under its own headings: “Backend Screen Primary Responsibility”, “Product, Price & Availability”, “Synchronization”, “Channel Performance & Commercial”, “Channel Audit, Logs & Transaction”, “Channel Governance, SLA & Partner”.

| Shows | Format | Notes |
|---|---|---|
| Signals | list or chips (count when long) | AI Analysis signals behind the recommendation (pack p.33-34) |
| Channel allocation & rebalancing operational capacity | text | not in the schema: `Channel Allocation & Rebalancing Operational capacity` |
| 5 | text | not in the schema: `4.2.5` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Revenue impact (primary button) | navigation or local | — | — | — | — |
| Channel utilization (secondary button) | navigation or local | — | — | — | — |
| Risk (secondary button) | navigation or local | — | — | — | — |
| Decide catalogue AI finding (secondary button) | `decideCatalogueAiFinding` POST `/ai-findings/{findingId}/decision` | inline | CatalogueAiFinding | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`. | gated `AI_APPROVE`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Decide finding**: As on ADM-128. *(source: contracts/spine/catalogue.yaml#decideCatalogueAiFinding)*

**Data it reads**: `listChannel2` (onLoad, AI Channel Optimization & Intelligence Center); `listChannel` (onLoad, Channel Operations Command Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel optimization intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel optimization intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel optimization intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel optimization intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyClosed`.; 422 `commentRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
finding:
  recommendation: Shift 40 Saturday units from B2B to Website
  impact: +AED 4,800.00
```

#### Permissions

- `listChannel2` → `PRODUCT_VIEW` (read) · staff
- `listChannel` → `PRODUCT_VIEW` (read) · staff
- `decideCatalogueAiFinding` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.32 | System shall support dynamic adjustment of ticket inventory and capacity based on demand forecasts, operational capacity and business rules. | Ticketing Catalogue | CONTRACTED_PARTIAL | `listChannel2` |
| 2.7.54 | AI shall recommend optimal allocation of inventory and quotas across B2B partners based on sales performance, demand forecasts, unused allocation, partner ranking, seasonality, event capacity, and … | Ticketing Sales | CONTRACTED_PARTIAL | `listChannel2` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-277` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-277`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 2
- Flow F167 *Sales Channel Management board 2: Channel Operations Command Center*, step 18: Works in AI Channel Optimization & Intelligence Center → Create the AI intelligence layer that looks across all sales channels together rather than optimizing each channel in isolation.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-277?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Revenue impact, Channel utilization, Risk, Decide catalogue AI finding.
- [ ] No transition is declared; back returns where the user came from.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decideCatalogueAiFinding": {"method":"POST","path":"/ai-findings/{findingId}/decision","contract":"catalogue","summary":"Acknowledge, accept, dismiss or resolve an AI finding","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CatalogueAiFinding"},
"listChannel": {"method":"GET","path":"/channel","contract":"catalogue","summary":"Channel Operations Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"healthStatus","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannel2": {"method":"GET","path":"/channel-2","contract":"catalogue","summary":"AI Channel Optimization & Intelligence Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelAllocationRebalancing": {"method":"GET","path":"/channel-allocation-rebalancing","contract":"catalogue","summary":"Channel Allocation & Rebalancing Operations","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelConnectionIntegration": {"method":"GET","path":"/channel-connection-integration","contract":"catalogue","summary":"Channel Connection & Integration Manager","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"connectionType","in":"query","required":false},{"name":"environment","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelExceptionIncident": {"method":"GET","path":"/channel-exception-incident","contract":"catalogue","summary":"Channel Exceptions, Incidents & Recovery","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"severity","in":"query","required":false},{"name":"errorType","in":"query","required":false},{"name":"currentStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelGovernanceSla": {"method":"GET","path":"/channel-governance-sla","contract":"catalogue","summary":"Channel Governance, SLA & Partner Control","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"complianceFlag","in":"query","required":false},{"name":"governanceStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelLogTransaction": {"method":"GET","path":"/channel-log-transaction","contract":"catalogue","summary":"Channel Audit, Logs & Transaction Traceability","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"transactionId","in":"query","required":false},{"name":"ticket","in":"query","required":false},{"name":"partnerReference","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"correlationId","in":"query","required":false},{"name":"apiRequest","in":"query","required":false},{"name":"user","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelPerformanceCommercial": {"method":"GET","path":"/channel-performance-commercial","contract":"catalogue","summary":"Channel Performance & Commercial Analytics","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"timeFrom","in":"query","required":false},{"name":"timeTo","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductPriceAvailability": {"method":"GET","path":"/product-price-availability","contract":"catalogue","summary":"Product, Price & Availability Synchronization","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"domain","in":"query","required":false},{"name":"frequency","in":"query","required":false},{"name":"hasFailures","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRealTimeAvailability": {"method":"GET","path":"/real-time-availability","contract":"promotions","summary":"Real-Time Availability & Checkout Validation","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RealTimeAvailabilityCheckoutValidationView"},
"listRealTimeChannel": {"method":"GET","path":"/real-time-channel","contract":"catalogue","summary":"Real-Time Channel Availability & Inventory Monitor","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"availabilityStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"retryChannelIncident": {"method":"POST","path":"/channel-incidents/{incidentId}/retry","contract":"catalogue","summary":"Retry the failed channel call behind an incident","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setChannelAllocations": {"method":"PUT","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Allocate a channel capacity across sales channels","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"setChannelConnectionConfiguration": {"method":"PUT","path":"/channel-connections","contract":"catalogue","summary":"Create or update a channel connection","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelConnection","responds":"ChannelConnection"},
"setChannelSyncSetting": {"method":"PUT","path":"/channel-syncs","contract":"catalogue","summary":"Set how one kind of data synchronises with a channel","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelSync","responds":"ChannelSync"},
"testChannelConnection": {"method":"POST","path":"/channel-connections/{connectionId}/test","contract":"catalogue","summary":"Test a channel connection now","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelConnection"},
"updateChannelIncident": {"method":"PATCH","path":"/channel-incidents/{incidentId}","contract":"catalogue","summary":"Own, investigate, resolve or close a channel incident","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelIncident"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiChannelOptimizationIntelligenceCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Channel Optimization & Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"recommendation":{"type":"string","description":"Recommendation"},"reason":{"type":"string","description":"Reason"},"expectedImpact":{"type":"string","description":"Expected Impact"},"confidence":{"type":"number","description":"Confidence, 0-1","minimum":0,"maximum":1},"constraints":{"type":"array","items":{"type":"string"},"description":"Constraints (contractual, capacity, approval)"},"requiredApproval":{"type":"string","description":"Required Approval: the role that must approve","nullable":true},"recommendationId":{"type":"string","description":"Recommendation ID"},"category":{"type":"string","enum":["capacity","channel","schedule","commercial","operational"],"description":"Recommendation Category (pack p.34)"},"channelIds":{"type":"array","items":{"type":"string"},"description":"Channels the recommendation concerns"},"signals":{"type":"array","items":{"type":"string","enum":["salesVelocity","conversion","capacity","allocation","revenue","netRevenue","pricing","channelFees","commission","customerDemand","timeToEvent","historicalPerformance","failures","availability"]},"description":"AI Analysis signals behind the recommendation (pack p.33-34)"},"simulation":{"type":"object","nullable":true,"description":"Scenario Simulation estimate (pack p.34)","properties":{"expectedUnitsSold":{"type":"integer"},"revenueImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channelUtilization":{"type":"number"},"risk":{"type":"string","enum":["low","medium","high"]},"contractualConstraints":{"type":"array","items":{"type":"string"}}}},"status":{"type":"string","description":"Status: proposed, accepted, modified, rejected, scheduled or assigned (decided 29 September, readiness close-out)"}}},
"CatalogueAiFinding": {"type":"object","x-ticvai-persistence":"catalogue.ai_finding","description":"**Something the AI noticed about the catalogue or its channels, for a person to act on** (29 September, data model DM3). Merges governance risks (ADM-137) and channel optimisation recommendations (ADM-272). Advisory only: a finding never changes configuration; acting on it goes through the ordinary operations and their approvals. **Created by the AI monitoring job** (29 September, writers pass); a person acknowledges, accepts, dismisses or resolves it with `decideCatalogueAiFinding`, and the job resolves one whose condition has cleared (`states/catalogue-ai-finding.yaml`).","required":["id","scopePath","domain","findingType","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"domain":{"type":"string","enum":["productGovernance","channel"]},"findingType":{"type":"string","maxLength":60,"description":"Governance: the `risk` value; channel: the recommendation `category`."},"productId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"salesChannelIds":{"type":"array","items":{"type":"string","format":"uuid"}},"severity":{"type":"string","enum":["critical","high","medium","low",null],"nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"summary":{"type":"string","description":"The recommendation, or the risk in one line."},"explanation":{"type":"string","nullable":true},"businessImpact":{"type":"string","nullable":true},"recommendedAction":{"type":"string","nullable":true},"constraints":{"type":"array","items":{"type":"string"}},"signals":{"type":"array","items":{"type":"string"}},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"description":"Channel findings: `{expectedUnitsSold, revenueImpact, channelUtilization, risk, contractualConstraints}`."},"requiredApproval":{"type":"string","maxLength":100,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"dueDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["open","acknowledged","accepted","dismissed","resolved"],"default":"open"},"modelVersion":{"type":"string","maxLength":60,"nullable":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelAllocation": {"x-ticvai-persistence":"catalogue.channel_allocation","type":"object","required":["channel","allocatedUnits"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/Channel"},"allocatedUnits":{"type":"integer","minimum":0},"soldUnits":{"type":"integer","readOnly":true},"leasedUnits":{"type":"integer","readOnly":true,"description":"Held by terminals on this channel but not yet sold."},"remainingUnits":{"type":"integer","readOnly":true},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"},"salesChannelId":{"type":"string","format":"uuid","nullable":true,"description":"The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"default":"dedicated","description":"How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."},"minimumUnits":{"type":"integer","nullable":true,"minimum":0},"maximumUnits":{"type":"integer","nullable":true,"minimum":0},"replenishmentRule":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"default":"none"},"releaseThresholdUnits":{"type":"integer","nullable":true,"minimum":0},"releaseHoursBeforeEvent":{"type":"integer","nullable":true,"minimum":0,"description":"Alternative to `releaseAt`, relative to the performance start."},"contractualUnits":{"type":"integer","nullable":true,"minimum":0,"description":"Units a partner agreement guarantees; rebalancing never goes below it."},"minimumGuaranteedUnits":{"type":"integer","nullable":true,"minimum":0},"isFrozen":{"type":"boolean","default":false,"description":"Excluded from rebalancing."}}},
"ChannelAllocationRebalancingOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Allocation & Rebalancing Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"initialAllocation":{"type":"integer","description":"Initial Allocation"},"sold":{"type":"integer","description":"Sold"},"held":{"type":"integer","description":"Held"},"remaining":{"type":"integer","description":"Remaining"},"utilization":{"type":"number","description":"Utilization %: sold plus held over allocated, 0-100","minimum":0,"maximum":100},"salesVelocity":{"type":"number","description":"Sales Velocity: units per hour over the last 24 hours (decided 29 September, readiness close-out)"},"forecast":{"type":"integer","description":"Forecast: units the channel is expected to sell by the event"},"recommendedAllocation":{"type":"integer","description":"Recommended Allocation (advisory)","nullable":true},"contractualAllocation":{"type":"integer","description":"Contractual allocation from the partner agreement","nullable":true},"minimumGuaranteedInventory":{"type":"integer","description":"Minimum guaranteed inventory","nullable":true},"event":{"type":"string","description":"Event or performance ID"},"product":{"type":"string","description":"Product ID","nullable":true},"frozen":{"type":"boolean","description":"Allocation frozen"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI allocation recommendations (pack p.27, e.g. transfer 500 units from OTA to B2C). Advisory only: nothing is changed until a user acts."}}},
"ChannelAllocationSet": {"x-ticvai-persistence":"none — projection","type":"object","required":["channelCapacityId","capacity","allocations","generalPoolUnits"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"capacity":{"type":"integer"},"allocations":{"type":"array","items":{"$ref":"#/components/schemas/ChannelAllocation"}},"generalPoolUnits":{"type":"integer","description":"Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"},"totalSold":{"type":"integer"},"totalRemaining":{"type":"integer"}}},
"ChannelAuditLogsTransactionTraceabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Audit, Logs & Transaction Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"userSystem":{"type":"string","description":"User/System: user ID or the system component that acted"},"action":{"type":"string","description":"Action"},"previousValue":{"type":"string","description":"Previous Value (as text)","nullable":true},"newValue":{"type":"string","description":"New Value (as text)","nullable":true},"reference":{"type":"string","description":"Reference: order, transaction, ticket or partner reference","nullable":true},"result":{"type":"string","enum":["success","failure","partial"],"description":"Result"},"environment":{"type":"string","enum":["sandbox","uat","production"],"description":"Environment"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"category":{"type":"string","enum":["configurationChange","activation","suspension","allocationChange","priceAssignment","sync","order","cancellation","error","manualIntervention","integrationChange"],"description":"Audit Category (pack p.31)"},"trace":{"type":"array","items":{"type":"object","properties":{"step":{"type":"string","enum":["partnerRequest","requestReceived","productValidation","priceValidation","capacityHold","orderCreation","paymentHandling","ticketIssuance","responseSent"]},"at":{"type":"string","format":"date-time"},"result":{"type":"string","enum":["success","failure","skipped"]}}},"description":"Transaction Trace for an external order (pack p.31); empty for other records"}}},
"ChannelConnection": {"type":"object","x-ticvai-persistence":"catalogue.channel_connection","description":"**How TICVAI technically reaches a channel** (29 September, data model DM3). ADM-266. One row per connector and environment. **Credentials are never stored here**: `credentialsReference` names the secret in the vault. `control.integration_listing` is the marketplace entry an adapter comes from; this row is the tenant's connection using it.","required":["id","scopePath","salesChannelId","connectorName","environment","connectionType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"salesChannelId":{"type":"string","format":"uuid"},"connectorName":{"type":"string","maxLength":200},"partner":{"type":"string","maxLength":200,"nullable":true},"environment":{"type":"string","enum":["sandbox","uat","production"]},"connectionType":{"type":"string","enum":["ticvaiNative","restApi","webhook","otaAdapter","resellerApi","partnerApi","middleware","fileSftp","customConnector"]},"direction":{"type":"string","enum":["outbound","inbound","bidirectional"],"default":"outbound"},"endpoint":{"type":"string","maxLength":500,"nullable":true},"apiVersion":{"type":"string","maxLength":40,"nullable":true},"authenticationType":{"type":"string","enum":["none","oauth","apiKey","clientCredentials","certificate","signedRequest"]},"credentialsReference":{"type":"string","maxLength":200,"nullable":true,"description":"A vault reference, never the secret."},"certificateReference":{"type":"string","maxLength":200,"nullable":true},"certificateExpiresAt":{"type":"string","format":"date-time","nullable":true},"timeoutMs":{"type":"integer","nullable":true,"minimum":1},"rateLimitPerMinute":{"type":"integer","nullable":true,"minimum":1},"ipRestrictions":{"type":"array","items":{"type":"string"}},"retryPolicy":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{maxAttempts, backoffSeconds}`."},"adapterId":{"type":"string","maxLength":100,"nullable":true},"connectionStatus":{"type":"string","enum":["notTested","connected","degraded","offline","disabled"],"default":"notTested"},"lastTests":{"type":"object","additionalProperties":true,"readOnly":true,"description":"`[{test, result, testedAt}]`, the latest result per test."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ChannelConnectionIntegrationManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Connection & Integration Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"connectorName":{"type":"string","description":"Connector Name"},"channel":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"partner":{"type":"string","description":"Partner ID (the B2B/OTA partner record)","nullable":true},"environment":{"type":"string","enum":["sandbox","uat","production"],"description":"Environment (pack p.23)"},"endpoint":{"type":"string","description":"Endpoint URL","format":"uri","nullable":true},"apiVersion":{"type":"string","description":"API Version","nullable":true},"authenticationType":{"type":"string","enum":["none","oauth","apiKey","clientCredentials","certificate","signedRequest"],"description":"Authentication Type (pack p.23 Security)"},"credentialsReference":{"type":"string","description":"Credentials reference: the secret-store key; the secret itself is never returned"},"certificate":{"type":"string","description":"Certificate reference (secret-store key)","nullable":true},"timeout":{"type":"integer","description":"Timeout in seconds","minimum":1,"default":30},"rateLimit":{"type":"integer","description":"Rate Limit: requests per minute","minimum":1,"nullable":true},"ipRestrictions":{"type":"array","items":{"type":"string"},"description":"IP Restrictions: allowed CIDR ranges"},"connectionStatus":{"type":"string","description":"Connection Status: notTested, connected, degraded, failed or disabled (decided 29 September, readiness close-out)"},"connectionType":{"type":"string","enum":["ticvaiNative","restApi","webhook","otaAdapter","resellerApi","partnerApi","middleware","fileSftp","customConnector"],"description":"Connection Type (pack p.22)"},"direction":{"type":"string","enum":["outbound","inbound","bidirectional"],"description":"Who calls whom: TICVAI calls the partner's API, the partner calls TICVAI, or both (MoM 31 Aug §4.3)"},"adapterId":{"type":"string","description":"Reusable adapter for an external platform; the platform is named as data on the adapter. Enabling it for a new tenant needs no rebuild (MoM 31 Aug §4.3)","nullable":true},"retryPolicy":{"type":"object","description":"Retry Policy (pack p.23)","properties":{"maxAttempts":{"type":"integer","minimum":0},"backoffSeconds":{"type":"integer","minimum":0}}},"certificateExpiresAt":{"type":"string","format":"date-time","description":"Certificate expiry, for governance alerts","nullable":true},"lastTests":{"type":"array","items":{"type":"object","properties":{"test":{"type":"string","enum":["authentication","connectivity","product","price","availability","order","cancellation"]},"result":{"type":"string","enum":["passed","failed","notSupported"]},"testedAt":{"type":"string","format":"date-time"}}},"description":"Connection Testing results, latest per test (pack p.23)"}}},
"ChannelExceptionsIncidentsRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Exceptions, Incidents & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"incidentId":{"type":"string","description":"Incident ID"},"channel":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"partner":{"type":"string","description":"Partner ID","nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"],"description":"Severity (pack p.28)"},"errorType":{"type":"string","enum":["connectionFailure","authenticationFailure","productSyncFailure","pricingMismatch","inventoryMismatch","orderFailure","paymentError","timeout","cancellationFailure","duplicateTransaction","fulfillmentFailure","rateLimit","partnerError"],"description":"Error Type (pack p.27-28 Exception Categories)"},"affectedProductEvent":{"type":"string","description":"Affected Product/Event: product or event ID","nullable":true},"transactionsAffected":{"type":"integer","description":"Transactions Affected"},"businessImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Business Impact: estimated sales value at risk"},"firstDetected":{"type":"string","format":"date-time","description":"First Detected"},"owner":{"type":"string","description":"Owner (user ID)","nullable":true},"slaDueAt":{"type":"string","format":"date-time","description":"SLA: resolution due time","nullable":true},"currentStatus":{"type":"string","description":"Current Status: open, assigned, investigating, recovering, resolved or closed (decided 29 September, readiness close-out)"},"errorCode":{"type":"string","description":"Error Code","nullable":true},"apiRequestReference":{"type":"string","description":"API Request Reference","nullable":true},"response":{"type":"string","description":"Response body, sensitive data masked","nullable":true},"correlationId":{"type":"string","description":"Correlation ID","nullable":true},"timestamp":{"type":"string","format":"date-time","description":"Timestamp of the last failing call","nullable":true},"retryCount":{"type":"integer","description":"Retry Count"},"aiSummary":{"type":"string","description":"AI summary of the incident in business language (pack p.29); advisory","nullable":true}}},
"ChannelGovernanceSlaPartnerControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Governance, SLA & Partner Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelOwner":{"type":"string","description":"Channel Owner (user ID)","nullable":true},"partnerOwner":{"type":"string","description":"Partner Owner (user ID)","nullable":true},"commercialAgreementReference":{"type":"string","description":"Commercial Agreement Reference: the B2B/OTA agreement ID","nullable":true},"sla":{"type":"object","description":"SLA targets","properties":{"availabilityPercent":{"type":"number"},"responseTimeMs":{"type":"integer"},"resolutionHours":{"type":"number"}}},"transactionLimits":{"type":"integer","description":"Transaction Limits: maximum transactions per day","nullable":true},"rateLimits":{"type":"integer","description":"Rate Limits: requests per minute","nullable":true},"contractDates":{"type":"object","description":"Contract Dates","properties":{"start":{"type":"string","format":"date"},"end":{"type":"string","format":"date","nullable":true}}},"renewalDate":{"type":"string","format":"date","description":"Renewal Date","nullable":true},"supportContacts":{"type":"array","items":{"type":"string"},"description":"Support Contacts"},"escalationContacts":{"type":"array","items":{"type":"string"},"description":"Escalation Contacts"},"availability":{"type":"number","description":"Availability % measured"},"apiResponseTime":{"type":"integer","description":"API Response Time, milliseconds (p95) (decided 29 September, readiness close-out)"},"transactionSuccess":{"type":"number","description":"Transaction Success %"},"errorRate":{"type":"number","description":"Error Rate %"},"incidentResolutionTime":{"type":"number","description":"Incident Resolution Time, average hours"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"reviewFrequency":{"type":"string","enum":["monthly","quarterly","semiAnnual","annual"],"description":"Review Frequency"},"syncSuccess":{"type":"number","description":"Sync Success %"},"complianceFlags":{"type":"array","items":{"type":"string","enum":["expiredAgreement","expiredCertificate","expiringApiCredentials","missingOwner","unapprovedProductionIntegration","slaBreach","excessiveTransactionFailures"]},"description":"Compliance Controls raised (pack p.32-33)"},"governanceStatus":{"type":"string","description":"Governance status: normal, underReview, restricted or suspended (decided 29 September, readiness close-out)"}}},
"ChannelIncident": {"type":"object","x-ticvai-persistence":"catalogue.channel_incident","description":"**A channel failure someone has to resolve** (29 September, data model DM3). ADM-269. Opened by the sync and order paths when a call to or from a channel fails; retried, owned and closed here. The per-call trace is in `catalogue.audit_entry` (`domain: channel`). **Opened by the channel sync and order jobs, never through the API** (29 September, writers pass); owned and closed with `updateChannelIncident`, retried with `retryChannelIncident` (`states/channel-incident.yaml`).","required":["id","scopePath","salesChannelId","severity","errorType","status","firstDetectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"salesChannelId":{"type":"string","format":"uuid"},"channelConnectionId":{"type":"string","format":"uuid","nullable":true},"partner":{"type":"string","maxLength":200,"nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"]},"errorType":{"type":"string","enum":["connectionFailure","authenticationFailure","productSyncFailure","pricingMismatch","inventoryMismatch","orderFailure","paymentError","timeout","cancellationFailure","duplicateTransaction","fulfillmentFailure","rateLimit","partnerError"]},"productId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"transactionsAffected":{"type":"integer","default":0},"businessImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"firstDetectedAt":{"type":"string","format":"date-time","readOnly":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["open","investigating","retrying","resolved","closed"],"default":"open"},"errorCode":{"type":"string","maxLength":100,"nullable":true},"apiRequestReference":{"type":"string","maxLength":200,"nullable":true},"responseExcerpt":{"type":"string","nullable":true,"description":"The partner response, truncated and scrubbed of personal data."},"correlationId":{"type":"string","maxLength":100,"nullable":true},"retryCount":{"type":"integer","default":0},"aiSummary":{"type":"string","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ChannelOperationsCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Channel Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeChannels":{"type":"integer","description":"Active Channels"},"connectedChannels":{"type":"integer","description":"Connected Channels"},"degradedChannels":{"type":"integer","description":"Degraded Channels"},"offlineChannels":{"type":"integer","description":"Offline Channels"},"transactionsToday":{"type":"integer","description":"Transactions Today"},"grossSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Sales today"},"productsAvailable":{"type":"integer","description":"Products Available"},"synchronizationErrors":{"type":"integer","description":"Synchronization Errors"},"capacityAlerts":{"type":"integer","description":"Capacity Alerts"},"pricingErrors":{"type":"integer","description":"Pricing Errors"},"failedTransactions":{"type":"integer","description":"Failed Transactions"},"openOperationalIncidents":{"type":"integer","description":"Open Operational Incidents"},"liveActivity":{"type":"array","items":{"type":"object","properties":{"occurredAt":{"type":"string","format":"date-time"},"channelId":{"type":"string"},"message":{"type":"string"}}},"description":"Live Activity: latest important channel events, newest first (the 50 most recent (decided 29 September, readiness close-out))"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Operational problems prioritised by business impact (pack p.22). Advisory only: nothing is changed until a user acts."}}},
"ChannelOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"type":{"type":"string","enum":["b2cWeb","b2cMobileApp","pos","mobilePos","flyingPos","kiosk","callCentre","b2bPortal","reseller","ota","api","partnerPortal","marketplace","thirdPartyChannel","customChannel"],"description":"Type: the channel type"},"venueScope":{"type":"string","description":"Venue/Scope"},"connectionStatus":{"type":"string","description":"Connection Status: connected, degraded, offline or maintenance"},"lastSync":{"type":"string","format":"date-time","description":"Last Sync","nullable":true},"products":{"type":"integer","description":"Products available on the channel"},"transactions":{"type":"integer","description":"Transactions today"},"salesValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Value today"},"inventoryStatus":{"type":"string","description":"Inventory Status: ok, low, soldOut or syncError (decided 29 September, readiness close-out)"},"pricingStatus":{"type":"string","description":"Pricing Status: ok, mismatch or error (decided 29 September, readiness close-out)"},"errorCount":{"type":"integer","description":"Error Count today"},"healthScore":{"type":"number","description":"Health Score, 0-100","minimum":0,"maximum":100},"healthStatus":{"type":"string","description":"Health Status: healthy, warning, degraded, critical, offline or maintenance (pack p.21)"}}},
"ChannelPerformanceCommercialAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Performance & Commercial Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Sales"},"netSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Sales"},"transactions":{"type":"integer","description":"Transactions"},"ticketsSold":{"type":"integer","description":"Tickets Sold"},"averageOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Average Order Value"},"conversionRate":{"type":"number","description":"Conversion Rate %","nullable":true},"cancellationRate":{"type":"number","description":"Cancellation Rate %"},"capacityUtilization":{"type":"number","description":"Capacity Utilization %"},"revenuePerAvailableUnit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Available Unit"},"fees":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"costOfSale":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost of Sale where available"},"allocation":{"type":"integer","description":"Partner Comparison: Allocation","nullable":true},"sold":{"type":"integer","description":"Partner Comparison: Sold","nullable":true},"utilization":{"type":"number","description":"Partner Comparison: Utilization %","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Comparison: Revenue"},"cancellations":{"type":"integer","description":"Partner Comparison: Cancellations","nullable":true},"settlement":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Comparison: Settlement, amount settled in the period"},"growth":{"type":"number","description":"Partner Comparison: Growth % against the previous equal period","nullable":true},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"partner":{"type":"string","description":"Partner ID for a B2B/OTA row","nullable":true},"refundRate":{"type":"number","description":"Refund Rate %"},"funnel":{"type":"object","nullable":true,"description":"Channel Funnel for digital channels (pack p.30)","properties":{"available":{"type":"integer"},"viewed":{"type":"integer"},"selected":{"type":"integer"},"checkout":{"type":"integer"},"paid":{"type":"integer"}}},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Insights (pack p.30). Advisory only: nothing is changed until a user acts."}}},
"ChannelSync": {"type":"object","x-ticvai-persistence":"catalogue.channel_sync","description":"**The synchronisation state of one channel for one kind of data** (29 September, data model DM3). ADM-267. One row per channel and domain (product, price, availability ...); counts are the latest run's, overwritten by the sync job. **Two writers** (29 September, writers pass): the sync job writes the counts and timestamps (the `readOnly` fields); a person sets `direction`, `frequency` and `isPaused` with `setChannelSyncSetting`.","required":["id","scopePath","salesChannelId","domain"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"salesChannelId":{"type":"string","format":"uuid"},"channelConnectionId":{"type":"string","format":"uuid","nullable":true},"domain":{"type":"string","enum":["product","productDescription","schedule","availability","capacity","price","tax","fees","media","restrictions","salesStatus"]},"direction":{"type":"string","enum":["ticvaiToChannel","channelToTicvai","bidirectional"],"default":"ticvaiToChannel"},"frequency":{"type":"string","enum":["realTime","nearRealTime","scheduled","manual","eventTriggered"],"default":"nearRealTime"},"isPaused":{"type":"boolean","default":false},"lastSuccessfulSyncAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"nextSyncAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"recordsProcessed":{"type":"integer","readOnly":true},"successful":{"type":"integer","readOnly":true},"failed":{"type":"integer","readOnly":true},"pending":{"type":"integer","readOnly":true},"warnings":{"type":"integer","readOnly":true},"durationMs":{"type":"integer","nullable":true,"readOnly":true},"mismatchCount":{"type":"integer","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductPriceAvailabilitySynchronizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product, Price & Availability Synchronization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"lastSuccessfulSync":{"type":"string","format":"date-time","description":"Last Successful Sync","nullable":true},"nextSync":{"type":"string","format":"date-time","description":"Next Sync; empty for manual","nullable":true},"recordsProcessed":{"type":"integer","description":"Records Processed in the last run"},"successful":{"type":"integer","description":"Successful"},"failed":{"type":"integer","description":"Failed"},"pending":{"type":"integer","description":"Pending"},"warning":{"type":"integer","description":"Warning: records synced with a warning"},"duration":{"type":"integer","description":"Duration of the last run in seconds"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"connectorId":{"type":"string","description":"Connector ID (ADM-269)","nullable":true},"domain":{"type":"string","enum":["product","productDescription","schedule","availability","capacity","price","tax","fees","media","restrictions","salesStatus"],"description":"Synchronization Domain (pack p.23-24)"},"direction":{"type":"string","enum":["ticvaiToChannel","channelToTicvai","bidirectional"],"description":"Synchronization Direction (pack p.24)"},"frequency":{"type":"string","enum":["realTime","nearRealTime","scheduled","manual","eventTriggered"],"description":"Sync Frequency (pack p.24)"},"paused":{"type":"boolean","description":"Sync paused"},"mismatchCount":{"type":"integer","description":"Difference Detection: records whose channel value differs from TICVAI's"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Grouped repetitive failures and probable root causes (pack p.25). Advisory only: nothing is changed until a user acts."}}},
"RealTimeAvailabilityCheckoutValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"failedChecks":{"type":"array","items":{"type":"string","enum":["productInactive","inventoryUnavailable","capacityUnavailable","timeslotUnavailable","resourceUnavailable","priceInvalid","promotionInvalid","partnerComponentInvalid","componentMappingInvalid"]},"description":"Checkout validations that failed; empty means the bundle is sellable."},"bundleId":{"type":"string","description":"Bundle ID"},"sellable":{"type":"boolean","description":"Whether the bundle can be sold now"}}},
"RealTimeChannelAvailabilityInventoryMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Real-Time Channel Availability & Inventory Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"allocated":{"type":"integer","description":"Allocated; empty when the channel sells from the shared pool","nullable":true},"sold":{"type":"integer","description":"Sold"},"held":{"type":"integer","description":"Held"},"remaining":{"type":"integer","description":"Remaining sellable units"},"utilization":{"type":"number","description":"Utilization %: sold plus held over allocated, 0-100","minimum":0,"maximum":100},"salesVelocity":{"type":"number","description":"Sales Velocity: units sold per hour over the last 24 hours (decided 29 September, readiness close-out)"},"forecastedSellOut":{"type":"string","format":"date-time","description":"Forecasted Sell-Out; empty when no sell-out is forecast","nullable":true},"product":{"type":"string","description":"Product ID"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"event":{"type":"string","description":"Event or performance ID","nullable":true},"sharedPool":{"type":"boolean","description":"The channel sells from the shared pool (shown as Shared in the matrix)"},"availabilityStatus":{"type":"string","description":"Status for this product/channel: available, lowAvailability, soldOut, closed, suspended, notAssigned or syncError (pack p.25)"}}}
}
```
