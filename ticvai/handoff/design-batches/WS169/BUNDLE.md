# WS169 — Seat Management Venue Mapping Reference v1.0 board 5

**10 screens · 10 operations · 13 schemas · 4 permissions**

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
  `CAPACITY_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-993` | Experience Command Center | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-994` | Choose My Seats | B–D | 0 | 0 | 6 | 12 | 1 | 6 | — | notStarted (—) |
| `BO-995` | Find Seats For Me | B–D | 0 | 20 | 6 | 18 | 2 | 6 | — | notStarted (—) |
| `BO-996` | Filters & Interactive Legend | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-997` | Real-Time Availability & Locking | B–D | 0 | 17 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-998` | Lock Timeout & Concurrency | B–D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-999` | Cart & Multi-Seat Management | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1000` | Mobile & Accessible Selection | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-1001` | View Preview, Compare & Heat Map | B–D | 0 | 20 | 6 | 20 | 0 | 0 | — | notStarted (—) |
| `BO-1002` | AI Conversational Seat Assistant | B–D | 0 | 20 | 6 | 20 | 0 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-993, BO-994, BO-995, BO-996, BO-997, BO-998, BO-999, BO-1000, BO-1001, BO-1002 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-993` Experience Command Center

**Monitor seat-selection performance, availability quality and conversion across channels. Show map loads, searches, selections, locks, expiries, carts, checkout conversion, abandonment and revenue. Compare web, mobile, POS, call center, box office, B2B and API channels by venue and performance. Surface slow maps, stale availability, lock conflicts, high timeout and selection drop-off with drill-down. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/experience-command-center-bo-993` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seating rules that shape selection (buffer seats, distancing, orphan-seat prevention, accessibility pairing) and selection performance.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **orphan prevention**: On by default with the minimum gap; the rule operators most want and least ask for. *(source: contracts/satellite/seating.yaml#setSeatingRules / TRACKER Actions row 64)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seating rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-994` Choose My Seats: *Choose My Seats*
- → `BO-995` Find Seats For Me: *Find Seats For Me*
- → `BO-996` Filters & Interactive Legend: *Filters & Interactive Legend*
- → `BO-997` Real-Time Availability & Locking: *Real-Time Availability & Locking*
- → `BO-998` Lock Timeout & Concurrency: *Lock Timeout & Concurrency*
- → `BO-999` Cart & Multi-Seat Management: *Cart & Multi-Seat Management*
- → `BO-1000` Mobile & Accessible Selection: *Mobile & Accessible Selection*
- → `BO-1001` View Preview, Compare & Heat Map: *View Preview, Compare & Heat Map*
- → `BO-1002` AI Conversational Seat Assistant: *AI Conversational Seat Assistant*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The experience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No experience yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  bufferSeats: 0
  orphanPrevention: true
  accessiblePairing: true
```

#### Permissions

- `getSeatingRules` → `PRODUCT_VIEW` (read) · staff
- `setSeatingRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.5.17 | Adjacent Seat Optimization | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.7.1 | Seat Kill Rules | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.7.2 | Buffer Seat Rules | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.7.3 | Companion Seat Rules | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.7.4 | Wheelchair Companion Rules | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.7.6 | Social Distancing Rules | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.8.1 | Wheelchair Seating | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |
| 21.8.2 | Companion Seating | Seat Management & Venue Mapping | CONTRACTED | `setSeatingRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-993` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-993`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 1: Opens Experience Command Center → Monitor seat-selection performance, availability quality and conversion across channels. Show map loads, searches, selections, locks, expiries, carts, checkout conversion, abandonment and revenue. …
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F278 branch at step 1 (expected): when Nothing has been set up on Experience Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F278 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-993?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seating rules, Cancel.
- [ ] Every transition is wired: `BO-100`, `BO-994`, `BO-995`, `BO-996`, `BO-997`, `BO-998`, `BO-999`, `BO-1000`, `BO-1001`, `BO-1002`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-994` Choose My Seats

**Allow a guest or authorized agent to select exact seats from an interactive map. Display section, row, seat, price, fees, type, view quality, accessibility, amenity and live availability. Support zoom, pan, section drill-down, keyboard navigation, clear selection and a live basket summary. Acquire locks only after server confirmation and clearly distinguish selected, unavailable, locked and accessible inventory. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/choose-my-seats-bo-994` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Choose exact seats on an interactive map, here for an authorised agent selling on a guest's behalf (call centre, box office); the guest version lives on the guest apps.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create seat hold (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **seat tooltip**: Section, row, seat, price with fees, type, view, accessibility. *(source: contracts/satellite/seating.yaml#getSeatAvailability)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Hold seats**: Named seats held for a short time with a visible countdown. *(source: contracts/satellite/seating.yaml#createSeatHold)*

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The choose seats list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the choose seats untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No choose seats yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the choose seats are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 One or more seats are no longer available, or the selection breaks a seating rule. (SeatConflictProblem); 422 More seats than one booking may take: above `VenueSettings.seating.maxSeatsPerGuestOrder` on a guest channel (decided 29 September, rev 3 REV3-7), or above 10 … (SeatLimitProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
selection:
  seats:
  - Lower 101 C-14
  - C-15
  total: AED 900.00
  holdExpires: '9:45'
```

#### Permissions

- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `createSeatHold` → `ORDER_CREATE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.4 | Seat Reservation Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.5 | Seat Sales Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.5.13 | Real-Time Seat Availability | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 1.3.12 | The system should constantly update the seating arrangement as not to cause any double reservation (i.e. as not for two guests to select the same seat). | Ticketing Catalogue | CONTRACTED | `createSeatHold` |
| 21.5.11 | Mobile Seat Selection | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |
| 21.5.12 | Cart Integration | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |
| 21.5.21 | Multi-Seat Cart Management | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-994` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-994`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 2: Works in Choose My Seats → Allow a guest or authorized agent to select exact seats from an interactive map. Display section, row, seat, price, fees, type, view quality, accessibility, amenity and live availability. Support …
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-994?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat hold, Cancel.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-995` Find Seats For Me

**Return best-available seat groups from stated customer preferences. Capture quantity, zone, level, price range, accessibility, aisle, view, amenity and proximity preferences. Rank valid contiguous or near-contiguous groups with total price, view summary, match score and trade-offs. Allow selection, alternative search and return to exact map without losing the current cart context. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Configuration Scope of Work / Version 1.0 22 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/find-seats-for-me-bo-995` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Best-available seats picked and held from stated preferences (quantity, zone, price, accessibility).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only assignSeats and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat status for a performance** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign seats (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Find and hold**: Contiguous seats where the party needs them; result held immediately. *(source: contracts/satellite/seating.yaml#assignSeats)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance)

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The find seats for list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the find seats for untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No find seats for yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the find seats for are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  party: 4
  zone: Lower
  maxPrice: AED 450.00
```

#### Permissions

- `assignSeats` → `ORDER_CREATE` (operate) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.5.3 | Auto Seat Assignment | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.4 | Seat Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.5 | Zone Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.6 | Price Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.7 | Group Size Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.8 | Amenities Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.9 | Seat Type Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.10 | View Filters | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.22 | AI Seat Selection Assistant | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 21.5.23 | Conversational Seat Search | Seat Management & Venue Mapping | CONTRACTED | `assignSeats` |
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Best-seat ranking (e.g. last-row-is-best vs. first-row-is-best, by venue sightlines) is configurable per seat map/event so the system recommends or auto-assigns the right best available seat. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-414)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-995` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-995`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 4: Works in Find Seats For Me → Return best-available seat groups from stated customer preferences. Capture quantity, zone, level, price range, accessibility, aisle, view, amenity and proximity preferences. Rank valid contiguous or …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-995?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Assign seats, Cancel.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-996` Filters & Interactive Legend

**Make large and complex seat maps understandable and searchable. Provide zone, price, group size, amenities, seat type, accessibility, view quality, level and availability filters. Update results, counts, map emphasis and legend in real time without hiding selected seats unexpectedly. Configure tenant/venue labels and colors while maintaining accessible contrast and non-color status cues. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/filters-interactive-legend-bo-996` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Filters and legend that make a large seat map understandable: zone, price, group size, amenities, type, accessibility, view, level.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **filter results**: Counts update as filters change. *(source: contracts/satellite/seating.yaml#getSeatAvailability)*

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The filters interactive legend list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the filters interactive legend untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No filters interactive legend yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the filters interactive legend are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
filter:
  price: AED 300-450
  accessible: true
  results: 14
```

#### Permissions

- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.4 | Seat Reservation Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.5 | Seat Sales Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.5.13 | Real-Time Seat Availability | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-996` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-996`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 6: Works in Filters & Interactive Legend → Make large and complex seat maps understandable and searchable. Provide zone, price, group size, amenities, seat type, accessibility, view quality, level and availability filters. Update results …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-996?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-997` Real-Time Availability & Locking

**Show and control atomic seat locks during selection. Display lock owner class, channel, transaction, acquisition time, expiry and current authoritative state to permitted roles. Broadcast lock, unlock, sale, hold, block and availability events to active selection sessions. Handle lock rejection, partial group success, lost connectivity and stale version with clear recovery options. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/real-time-availability-locking-bo-997` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-025): listRealTimeAvailability is promotions checkout validation, not seat locks; seat locks are seating's, and getSeatInventory returns every seat's state for a …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat locks during selection: owner class, channel, transaction, acquired and expiry, current state, for permitted roles.

**Fixed on main** (the package already carries these; draw what it says): listRealTimeAvailability is promotions checkout validation, not seat locks. (CHG-WIR-025); List operation(s) listRealTimeAvailability return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `getSeatInventory` ?performanceId |
| Section | picker: choose a section | — | — | `getSeatInventory` ?sectionId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat states** (detail panel, from `getSeatInventory`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| As of | 1 Oct 2026, 14:30 | — |
| Totals | grouped details | — |
| Capacity | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Reserved | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Out of service | 1,234 | — |
| Seats | list or chips (count when long) | — |
| Seat | the name it points at, never the id | — |
| Label | text | — |
| State | chip: Available, Held, Reserved, Sold, Blocked, Out of service… | — |
| Hold pool | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lock table**: Live list with countdown to expiry. *(source: contracts/satellite/promotions.yaml#listRealTimeAvailability)*

**Data it reads**: `getSeatInventory` (onLoad, Every seat's current state, with its locks)

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time availability locking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time availability locking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time availability locking yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time availability locking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
locks:
- seat: Balcony C-14
  owner: Guest basket
  channel: App
  expiresIn: 4 min
```

#### Permissions

- `getSeatInventory` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.28 | Visual Seat Categorization Automatically color-code seat categories. Generate interactive seat maps. Highlight restricted-view or obstructed seats. Visualize occupancy and sales patterns. | Ticketing Catalogue | CONTRACTED | `getSeatInventory` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-997` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-997`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 8: Works in Real-Time Availability & Locking → Show and control atomic seat locks during selection. Display lock owner class, channel, transaction, acquisition time, expiry and current authoritative state to permitted roles. Broadcast lock …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-997?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-998` Lock Timeout & Concurrency

**Configure fair timeout and collision behavior under concurrent demand. Set default lock duration, warning, grace period, extension policy, maximum extension and auto-release by channel or event. Configure optimistic concurrency, version checks, idempotency, conflict messages and retry boundaries. Simulate multiple customers selecting the same inventory and verify that no double lock or oversell can occur. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/lock-timeout-concurrency-bo-998` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-025): Lock timeouts are configured here, not performed: extending or relinquishing one hold (extendSeatHold, relinquishSeatHold) is a selection-time act; the missing …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat lock duration and concurrency: default hold, warning, grace, extensions up to the venue maximum.

**Fixed on main** (the package already carries these; draw what it says): The configuration screen declares hold operations (extend, release) rather than a policy write. (CHG-WIR-025); No read operation: the screen declares only extendSeatHold, relinquishSeatHold and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **extension**: Bounded by the venue's maximum; shown as minutes. *(source: contracts/satellite/seating.yaml#extendSeatHold)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lock timeout concurrency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lock timeout concurrency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lock timeout concurrency yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the lock timeout concurrency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  hold: 10 min
  warning: 2 min
  maxExtensions: 1
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-998` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-998`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 10: Works in Lock Timeout & Concurrency → Configure fair timeout and collision behavior under concurrent demand. Set default lock duration, warning, grace period, extension policy, maximum extension and auto-release by channel or event. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-998?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-993`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-999` Cart & Multi-Seat Management

**Manage several seats as one controlled cart allocation. List each seat, assigned guest, ticket type, price, fee, promotion, lock expiry and eligibility status. Support add, remove, replace, reassign, save-for-later where permitted and clear-cart actions. Revalidate availability, price, eligibility and adjacency before checkout and release all abandoned locks reliably. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 23**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holdId` (navigation) |
| Route | `/access-venue/cart-multi-seat-management-bo-999` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Several held seats as one allocation: per seat guest, ticket type, price, lock expiry; remove or release.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (destructive button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **held seats**: One row per seat with expiry. *(source: contracts/satellite/seating.yaml#getSeatHold)*

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cart multi-seat list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cart multi-seat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cart multi-seat yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cart multi-seat are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The hold is no longer active (`holdNotActive`) - converted to an order, already released or expired. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
hold:
  seats: 4
  expiresIn: 6 min
```

#### Permissions

- `getSeatHold` → `ORDER_VIEW` (read) · staff
- `relinquishSeatHold` → `ORDER_CREATE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-999` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-999`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 12: Works in Cart & Multi-Seat Management → Manage several seats as one controlled cart allocation. List each seat, assigned guest, ticket type, price, fee, promotion, lock expiry and eligibility status. Support add, remove, replace, reassign …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-999?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1000` Mobile & Accessible Selection

**Deliver an equivalent and WCAG-aligned selection flow on supported devices. Provide responsive map/list modes, large targets, screen-reader labels, logical focus order, keyboard and switch access. Support high contrast, text scaling, reduced motion and clear wheelchair, companion, aisle and route information. Maintain selection and lock state through rotation, app backgrounding, network interruption and session recovery. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/mobile-accessible-selection-bo-1000` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Accessible seat selection: accessible seats, their routes and who may buy them; map and list modes for keyboard and screen readers.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **list mode**: Every seat reachable without the map, with route information. *(source: contracts/satellite/seating.yaml#getAccessibleSeating / DI-029)*

**Data it reads**: `getAccessibleSeating` (onLoad, Which seats and routes)

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mobile accessible selection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mobile accessible selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mobile accessible selection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mobile accessible selection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
seat:
  id: Lower 101 W-1
  route: Vom 3, step-free
  companion: W-2
```

#### Permissions

- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.4 | Seat Reservation Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.5 | Seat Sales Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.5.13 | Real-Time Seat Availability | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1000` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1000`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 14: Works in Mobile & Accessible Selection → Deliver an equivalent and WCAG-aligned selection flow on supported devices. Provide responsive map/list modes, large targets, screen-reader labels, logical focus order, keyboard and switch access. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1000?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1001` View Preview, Compare & Heat Map

**Help customers understand qualitative and demand differences before choosing. Show approved seat-view previews or representative section views with source, freshness and obstruction disclosure. Compare seats by price, distance, view, level, amenities, accessibility and overall match. Display configurable demand, price or availability heat maps without revealing sensitive sales strategy. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/view-preview-compare-heat-map-bo-1001` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** View previews and comparisons before choosing, with demand heat.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only recommendSeats and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat status for a performance** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **recommendations**: Best available, best value, closest to stage, accessible with companions. *(source: contracts/satellite/seating.yaml#recommendSeats)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance)

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The view preview compare list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the view preview compare untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No view preview compare yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the view preview compare are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
options:
- strategy: bestValue
  seats: Upper 204 A-1..4
  total: AED 1,040.00
```

#### Permissions

- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.10 | The system should provide the option to enable or disable seat reservation for any type of event ticket. Guests shall be able to reserve a seat from a GUI when they purchase a ticket. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 1.3.11 | The system should offer assigned seating with multiple options for seat selection such as “pick a seat” or “best seat available.” Assigned seating should be made available both online and at the POS. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 21.5.1 | Choose My Seats | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.2 | Find Seats For Me | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.16 | Best Available Seat Selection | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.7.5 | Accessibility Rules | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.8.4 | Accessible Seat Filters | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.1 | Best Seat Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.2 | Best Value Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.3 | Closest-to-Stage Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.5 | Accessibility Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.7 | Alternative Seat Suggestions | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1001` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1001`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 16: Works in View Preview, Compare & Heat Map → Help customers understand qualitative and demand differences before choosing. Show approved seat-view previews or representative section views with source, freshness and obstruction disclosure. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1002` AI Conversational Seat Assistant

**Allow natural-language seat discovery through governed AI. Understand requests such as family size, budget, view, aisle, stage proximity, accessibility and preferred level. Return only currently valid seat groups with match score, rationale, trade-offs, total price and add-to-cart action. Record model/version and feedback, disclose uncertainty and prevent AI from bypassing locks, pricing, eligibility or accessible-seat rules. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 24 Board 6 - Holds, Blocks & Inventory Controls Figure 6. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 25**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `performanceId` (navigation) |
| Route | `/access-venue/ai-conversational-seat-assistant-bo-1002` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Natural-language seat search ("four together near the aisle under AED 400") returning only valid seats.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only recommendSeats and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Seat status for a performance** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **answer**: Options with why each matches. *(source: contracts/satellite/seating.yaml#recommendSeats)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance)

**Where the user goes next**

- → `BO-993` Experience Command Center: *Back to Experience Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conversational seat assistant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conversational seat assistant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conversational seat assistant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conversational seat assistant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
query: 4 seats together, aisle, under AED 400 each
```

#### Permissions

- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.10 | The system should provide the option to enable or disable seat reservation for any type of event ticket. Guests shall be able to reserve a seat from a GUI when they purchase a ticket. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 1.3.11 | The system should offer assigned seating with multiple options for seat selection such as “pick a seat” or “best seat available.” Assigned seating should be made available both online and at the POS. | Ticketing Catalogue | CONTRACTED | `recommendSeats` |
| 21.5.1 | Choose My Seats | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.2 | Find Seats For Me | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.5.16 | Best Available Seat Selection | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.7.5 | Accessibility Rules | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.8.4 | Accessible Seat Filters | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.1 | Best Seat Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.2 | Best Value Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.3 | Closest-to-Stage Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.5 | Accessibility Recommendations | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| 21.10.7 | Alternative Seat Suggestions | Seat Management & Venue Mapping | CONTRACTED | `recommendSeats` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1002` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1002`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 5
- Flow F278 *Seat Management Venue Mapping Reference v1.0 board 5: Experience Command Center*, step 18: Works in AI Conversational Seat Assistant → Allow natural-language seat discovery through governed AI. Understand requests such as family size, budget, view, aisle, stage proximity, accessibility and preferred level. Return only currently …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-993`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"assignSeats": {"method":"POST","path":"/performances/{performanceId}/assign-seats","contract":"seating","summary":"Pick and hold the best available seats","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createSeatHold": {"method":"POST","path":"/seat-holds","contract":"seating","summary":"Hold specific seats","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSeatHoldRequest","responds":"SeatHold"},
"getAccessibleSeating": {"method":"GET","path":"/accessible-seating","contract":"seating","summary":"Accessible seats, their routes and who may buy them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"seatMapId","in":"query","required":true}],"requestBody":null,"responds":"AccessibleSeating"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getSeatHold": {"method":"GET","path":"/seat-holds/{holdId}","contract":"seating","summary":"Read a hold","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatHold"},
"getSeatInventory": {"method":"GET","path":"/seat-inventory","contract":"seating","summary":"Every seat's state for a performance, in one read","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":true},{"name":"sectionId","in":"query","required":null}],"requestBody":null,"responds":"SeatInventory"},
"getSeatingRules": {"method":"GET","path":"/seat-maps/{seatMapId}/rules","contract":"seating","summary":"Read seating rules","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatingRules"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"relinquishSeatHold": {"method":"DELETE","path":"/seat-holds/{holdId}","contract":"seating","summary":"Release a hold","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setSeatingRules": {"method":"PUT","path":"/seat-maps/{seatMapId}/rules","contract":"seating","summary":"Set seating rules","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SeatingRules","responds":"SeatingRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibleSeating": {"type":"object","x-ticvai-persistence":"seating.accessible","description":"Boards 7.6 to 7.8. **An accessible seat with no accessible route is not an accessible seat.**\n","properties":{"seatMapId":{"type":"string","format":"uuid"},"spaces":{"type":"array","items":{"type":"object","properties":{"seatId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["wheelchairSpace","transferSeat","ambulant","easyAccess","assistanceDog","hearingLoop","visuallyImpaired"]},"routeDescription":{"type":"string","nullable":true},"stepFree":{"type":"boolean","default":true},"nearestAccessibleWc":{"type":"string","nullable":true}}}},"eligibility":{"type":"string","enum":["open","selfDeclared","verifiedOnce","verifiedEachTime"],"default":"selfDeclared","description":"**Contested in both directions.** Open sale leaves none for the guests who need them; hard gating turns people away at the door.\n"},"minimumProvisionPercent":{"type":"number","nullable":true},"scopePath":{"type":"string"}}},
"CreateSeatHoldRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","performanceId","seatIds"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","minItems":1,"maxItems":50,"description":"50 is the ceiling of the venue setting, not the limit a caller gets. On a guest channel the limit is `VenueSettings.seating.maxSeatsPerGuestOrder` (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); on a staff channel it stays 10 per sale (audit R080 (c)), as POS-002 shows. Either is refused with `422` `seat-limit-exceeded`.\n","items":{"type":"string"}},"ttlSeconds":{"type":"integer","minimum":60,"maximum":1800,"default":480,"description":"**8 minutes by default, extendable to 30 in all** (decided 28 September, audit R169). Left out, the hold lasts 480 seconds. No hold, first grant or extended, outlives 1800 seconds from its creation.\n"},"subjectId":{"type":"string","format":"uuid"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatHold": {"x-ticvai-persistence":"seating.seat_hold","type":"object","required":["id","performanceId","seatIds","status","createdAt","expiresAt"],"properties":{"id":{"type":"string"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string"}},"bufferedSeatIds":{"type":"array","items":{"type":"string"},"description":"Neighbours implicitly held by a seating rule."},"status":{"type":"string","enum":["held","converted","released","expired"]},"totalPrice":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"heldByPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"extensionCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SeatInventory": {"type":"object","description":"Board 4. **One read, because a real-time map assembling four endpoints renders one state late.**\n","properties":{"performanceId":{"type":"string","format":"uuid"},"asOf":{"type":"string","format":"date-time"},"totals":{"type":"object","properties":{"capacity":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"reserved":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"outOfService":{"type":"integer"}}},"seats":{"type":"array","items":{"type":"object","properties":{"seatId":{"type":"string","format":"uuid"},"label":{"type":"string"},"state":{"type":"string","enum":["available","held","reserved","sold","blocked","outOfService","killed"]},"holdPoolId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"SeatingRules": {"x-ticvai-persistence":"seating.seating_rules","type":"object","required":["seatMapId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"seatMapId":{"type":"string","format":"uuid"},"bufferSeats":{"type":"integer","minimum":0,"default":0,"description":"Seats kept empty either side of a sold party."},"bufferRows":{"type":"integer","minimum":0,"default":0},"preventOrphanSeats":{"type":"boolean","default":false,"description":"Refuse a selection that would leave a single unsellable seat between parties. Operators want this and rarely ask for it by name.\n"},"maxPartySize":{"type":"integer","nullable":true},"requireContiguous":{"type":"boolean","default":false,"description":"A party must sit together or the selection is refused."},"accessibleCompanionCount":{"type":"integer","default":1,"description":"Companion seats sold alongside each accessible space."},"allowSplitAcrossRows":{"type":"boolean","default":true}}}
}
```
