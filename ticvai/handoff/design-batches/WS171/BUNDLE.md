# WS171 — Seat Management Venue Mapping Reference v1.0 board 7

**10 screens · 5 operations · 3 schemas · 1 permissions**

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
  `CAPACITY_CONFIGURE`. A control nobody can use must say so,
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
| `BO-1013` | Rules Command Center | B–D | 1 | 17 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1014` | Seat Kill Rules | B–D | 0 | 18 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1015` | Buffer Seat Rules | B–D | 0 | 18 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1016` | Companion Seat Rules | B–D | 0 | 18 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1017` | Wheelchair Companion Rules | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1018` | Accessible Seating Master | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1019` | Accessible Route Mapping | B–D | 0 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1020` | Accessible Filters & Eligibility | B–D | 0 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1021` | Flexible Spacing Rules | B–D | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1022` | Compliance Validation & Audit | B–D | 1 | 16 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1014, BO-1015, BO-1016, BO-1017, BO-1018, BO-1019, BO-1020, BO-1021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1013` Rules Command Center

**Monitor seating-rule coverage, violations and compliance across venues. Show total and active rules, affected seats, open violations, capacity impact and venue compliance score. Filter by rule category, tenant, venue, event, layout, effective date, owner and severity. Surface missing accessible mappings, conflicting buffers and production changes requiring revalidation. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/rules-command-center-bo-1013` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seating rule coverage and violations across venues: kill, buffer, companion and accessibility rules.

**Known correction pending (do not draw the wrong version)**

- **No write operation: a configuration screen (Rules Command Center) declares only reads (getSeatRules).** Why: Nothing it shows can be changed from it; either it is a view (and its edits happen on the record editor, which it should link to) or a write is missing. *(source: contracts/satellite/seating.yaml#getSeatRules; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Seat map | select field | — | — | — | — | Sends `?seatMapId=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getSeatRules` ?seatMapId |

#### Outputs: what the screen shows and produces

**Shown**

**Killed seats** (metric tile, from `getSeatRules`): Count of `killedSeatIds`.

| Shows | Format | Notes |
|---|---|---|
| Killed seats | list or chips (count when long) | — |

**Buffer rule** (metric tile, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Enabled | yes / no (icon or chip) | — |

**Companion rule** (metric tile, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Enabled | yes / no (icon or chip) | — |

**Open violations** (metric tile): The pack asks for open violations; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Open violations | text | not in the schema: `Open violations` |

**Venue compliance score** (metric tile): The pack asks for venue compliance score; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Venue compliance score | text | not in the schema: `Venue compliance score` |

**Killed seats and reasons** (data table, from `getSeatRules`): One row per killed seat with its reason from `killReasons`.

| Shows | Format | Notes |
|---|---|---|
| Killed seats | list or chips (count when long) | — |
| Kill reasons | grouped details | — |

**Rules in force** (detail panel, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Scope path | text | — |
| Seats either side | 1,234 | — |
| Rows either side | 1,234 | — |
| Avoid single gaps | yes / no (icon or chip) | The commercial case for buffers. A map leaving one empty seat between every party has lost those seats without anybody deciding to. |
| Pairs | list or chips (count when long) | — |
| Release companion hours before | 1,234 | — |
| Enabled | yes / no (icon or chip) | — |
| Density percent | 1,234 | — |
| Per performance override | yes / no (icon or chip) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rule summary**: Rules by kind, seats affected, open violations. *(source: contracts/satellite/seating.yaml#getSeatRules)*

**Data it reads**: `getSeatRules` (onLoad, Rules in force)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1014` Seat Kill Rules: *Seat Kill Rules*
- → `BO-1015` Buffer Seat Rules: *Buffer Seat Rules*
- → `BO-1016` Companion Seat Rules: *Companion Seat Rules*
- → `BO-1017` Wheelchair Companion Rules: *Wheelchair Companion Rules*
- → `BO-1018` Accessible Seating Master: *Accessible Seating Master*
- → `BO-1019` Accessible Route Mapping: *Accessible Route Mapping*
- → `BO-1020` Accessible Filters & Eligibility: *Accessible Filters & Eligibility*
- → `BO-1021` Flexible Spacing Rules: *Flexible Spacing Rules*
- → `BO-1022` Compliance Validation & Audit: *Compliance Validation & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
summary:
  killed: 18
  buffered: 0
  companionPairs: 16
  violations: 1
```

#### Permissions

- `getSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1013` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1013`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 1: Opens Rules Command Center → Monitor seating-rule coverage, violations and compliance across venues. Show total and active rules, affected seats, open violations, capacity impact and venue compliance score. Filter by rule …
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F280 branch at step 1 (expected): when Nothing has been set up on Rules Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F280 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1014`, `BO-1015`, `BO-1016`, `BO-1017`, `BO-1018`, `BO-1019`, `BO-1020`, `BO-1021`, `BO-1022`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1014` Seat Kill Rules

**Remove seats from sale based on permanent or conditional unusability. Configure sightline, stage, production, obstruction, equipment, safety, maintenance and venue-defined kill reasons. Apply by seat list, section, row, polygon, obstruction distance, event type or layout condition. Preview affected capacity, sold/reserved inventory and alternative seating before activation. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/seat-kill-rules-bo-1014` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seats taken out of sale permanently or conditionally (sightline, stage, production, obstruction, safety).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getSeatRules` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kill rule**: Reason and seats; conditional kills tied to a stage configuration. *(source: contracts/satellite/seating.yaml#setSeatRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Kill, buffer, companion and accessibility rules** (detail panel, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Killed seats | list or chips (count when long) | — |
| Kill reasons | grouped details | — |
| Buffer rule | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Seats either side | 1,234 | — |
| Rows either side | 1,234 | — |
| Avoid single gaps | yes / no (icon or chip) | The commercial case for buffers. A map leaving one empty seat between every party has lost those seats without anybody deciding to. |
| Companion rule | grouped details | The one with legal weight. Selling the companion seat separately strands a carer. |
| Enabled | yes / no (icon or chip) | — |
| Pairs | list or chips (count when long) | — |
| Wheelchair space | the name it points at, never the id | — |
| Companion seats | list or chips (count when long) | — |
| Release companion hours before | 1,234 | — |
| Flexible spacing | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Density percent | 1,234 | — |
| Per performance override | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRules` (onLoad, Kill, buffer, companion and accessibility rules)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat kill rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat kill rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat kill rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat kill rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kill:
  seats: Lower 104 K-7..9
  reason: obstruction
```

#### Permissions

- `setSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1014` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1014`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 2: Works in Seat Kill Rules → Remove seats from sale based on permanent or conditional unusability. Configure sightline, stage, production, obstruction, equipment, safety, maintenance and venue-defined kill reasons. Apply by seat …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat rules, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1015` Buffer Seat Rules

**Create controlled unsold spacing around seats, zones or production objects. Define left/right, radial, row, perimeter, alternating or custom buffer patterns and minimum distance. Apply dynamically around selected seats, wheelchair spaces, camera positions, stages or restricted zones. Configure release behavior, priority, interaction with holds and treatment when a buffer conflicts with a sale. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 30**

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
| Route | `/access-venue/buffer-seat-rules-bo-1015` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Unsold spacing around seats, zones or production objects (left and right, row, perimeter, alternating).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getSeatRules` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **buffer pattern**: Pattern and distance, previewed on the map. *(source: contracts/satellite/seating.yaml#setSeatRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Kill, buffer, companion and accessibility rules** (detail panel, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Killed seats | list or chips (count when long) | — |
| Kill reasons | grouped details | — |
| Buffer rule | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Seats either side | 1,234 | — |
| Rows either side | 1,234 | — |
| Avoid single gaps | yes / no (icon or chip) | The commercial case for buffers. A map leaving one empty seat between every party has lost those seats without anybody deciding to. |
| Companion rule | grouped details | The one with legal weight. Selling the companion seat separately strands a carer. |
| Enabled | yes / no (icon or chip) | — |
| Pairs | list or chips (count when long) | — |
| Wheelchair space | the name it points at, never the id | — |
| Companion seats | list or chips (count when long) | — |
| Release companion hours before | 1,234 | — |
| Flexible spacing | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Density percent | 1,234 | — |
| Per performance override | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRules` (onLoad, Kill, buffer, companion and accessibility rules)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The buffer seat rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the buffer seat rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No buffer seat rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the buffer seat rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
buffer:
  around: camera platform
  pattern: perimeter
  seats: 1
```

#### Permissions

- `setSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1015` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1015`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 4: Works in Buffer Seat Rules → Create controlled unsold spacing around seats, zones or production objects. Define left/right, radial, row, perimeter, alternating or custom buffer patterns and minimum distance. Apply dynamically …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat rules, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1016` Companion Seat Rules

**Keep appropriate companion inventory linked to designated seats. Configure eligible seat types, adjacency, ratio, maximum companions and same-row or nearby rules. Control whether companions must be selected together and when unneeded companion seats may be released. Support family, premium, group and venue-defined companion policies without overriding wheelchair-specific rules. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/companion-seat-rules-bo-1016` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Companion inventory linked to designated seats: eligible seat types, adjacency, ratio, maximum companions.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getSeatRules` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **companion rule**: Ratio and adjacency (same row, next seat). *(source: contracts/satellite/seating.yaml#setSeatRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Kill, buffer, companion and accessibility rules** (detail panel, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Killed seats | list or chips (count when long) | — |
| Kill reasons | grouped details | — |
| Buffer rule | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Seats either side | 1,234 | — |
| Rows either side | 1,234 | — |
| Avoid single gaps | yes / no (icon or chip) | The commercial case for buffers. A map leaving one empty seat between every party has lost those seats without anybody deciding to. |
| Companion rule | grouped details | The one with legal weight. Selling the companion seat separately strands a carer. |
| Enabled | yes / no (icon or chip) | — |
| Pairs | list or chips (count when long) | — |
| Wheelchair space | the name it points at, never the id | — |
| Companion seats | list or chips (count when long) | — |
| Release companion hours before | 1,234 | — |
| Flexible spacing | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Density percent | 1,234 | — |
| Per performance override | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRules` (onLoad, Kill, buffer, companion and accessibility rules)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The companion seat rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the companion seat rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No companion seat rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the companion seat rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  ratio: '1:1'
  adjacency: same row, next seat
```

#### Permissions

- `setSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1016` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1016`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 6: Works in Companion Seat Rules → Keep appropriate companion inventory linked to designated seats. Configure eligible seat types, adjacency, ratio, maximum companions and same-row or nearby rules. Control whether companions must be …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat rules, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1017` Wheelchair Companion Rules

**Manage wheelchair-space and companion-seat pairing. Define one-to-one or configurable ratios, adjacency, transfer-seat eligibility and alternative companion locations. Require wheelchair space selection before companion inventory where policy permits and explain the rule clearly. Control release to general sale only through approved timing, evidence and accessible-demand safeguards. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/wheelchair-companion-rules-bo-1017` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wheelchair spaces paired with companion seats, transfer seats and alternatives.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **pairing**: Pairs drawn on the map; a wheelchair space without a companion is a validation error. *(source: contracts/satellite/seating.yaml#setSeatRules / contracts/satellite/seating.yaml#validateSeatMap)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getAccessibleSeating` (onLoad, The spaces being paired)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wheelchair companion rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wheelchair companion rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wheelchair companion rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wheelchair companion rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pair:
  space: Lower 101 W-1
  companion: W-2
```

#### Permissions

- `setSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1017` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1017`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 8: Works in Wheelchair Companion Rules → Manage wheelchair-space and companion-seat pairing. Define one-to-one or configurable ratios, adjacency, transfer-seat eligibility and alternative companion locations. Require wheelchair space …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat rules, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1018` Accessible Seating Master

**Maintain a standard catalog of accessible seat and space attributes. Configure wheelchair, companion, ambulatory, transfer, hearing, vision, service-animal and other supported types. Store dimensions, capacity treatment, route requirements, amenities, assisted access and display labels. Map each type to venue inventory, ticket products, customer-facing filters and compliance reporting. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/accessible-seating-master-bo-1018` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The catalogue of accessible seat and space types (wheelchair, companion, ambulatory, transfer, hearing, vision, service animal) and which seats carry them.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **accessible seats**: Type, dimensions, route, eligibility. *(source: contracts/satellite/seating.yaml#setAccessibleSeating)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accessible seating (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getAccessibleSeating` (onLoad, The accessible inventory)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accessible seating master list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accessible seating master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accessible seating master yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accessible seating master are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
seat:
  id: Lower 101 W-1
  type: wheelchair
  width: 90 cm
```

#### Permissions

- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff
- `setAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1018` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1018`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 10: Works in Accessible Seating Master → Maintain a standard catalog of accessible seat and space attributes. Configure wheelchair, companion, ambulatory, transfer, hearing, vision, service-animal and other supported types. Store …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accessible seating, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1019` Accessible Route Mapping

**Identify accessible journeys from entry to seats and facilities. Create routes through accessible entrances, lifts, ramps, concourses, restrooms and designated seating. Store distance, slope, level changes, width, surface, assistance requirement and temporary closure status. Validate route continuity and show impact when a layout, facility or access point becomes unavailable. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 31**

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
| Route | `/access-venue/accessible-route-mapping-bo-1019` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Accessible routes from entry to seats and facilities; an accessible seat without an accessible route is not accessible.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setAccessibleSeating and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **route**: Entrance, lifts, ramps, concourses to the seat, with distance and level changes. *(source: contracts/satellite/seating.yaml#setAccessibleSeating)*

#### Outputs: what the screen shows and produces

**Shown**

**Accessible seats, their routes and who may buy them** (detail panel, from `getAccessibleSeating`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Spaces | list or chips (count when long) | — |
| Seat | the name it points at, never the id | — |
| Kind | chip: Wheelchair space, Transfer seat, Ambulant, Easy access, Assistance dog, Hearing … | — |
| Route description | text | — |
| Step free | yes / no (icon or chip) | — |
| Nearest accessible wc | text | — |
| Eligibility | chip: Open, Self declared, Verified once, Verified each time | Contested in both directions. Open sale leaves none for the guests who need them; hard gating turns people away at the door. |
| Minimum provision percent | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accessible seating (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getAccessibleSeating` (onLoad, Accessible seats, their routes and who may buy them)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accessible route mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accessible route mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accessible route mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accessible route mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
route:
  from: Gate 2
  via:
  - Lift L1
  - Concourse 1
  to: Lower 101 W-1
  distance: 140 m
```

#### Permissions

- `setAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff
- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1019` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1019`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 12: Works in Accessible Route Mapping → Identify accessible journeys from entry to seats and facilities. Create routes through accessible entrances, lifts, ramps, concourses, restrooms and designated seating. Store distance, slope, level …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accessible seating, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1020` Accessible Filters & Eligibility

**Configure inclusive discovery without exposing sensitive guest information. Define filters and labels for wheelchair, companion, aisle, step-free, transfer, hearing, vision and service-animal needs. Configure eligibility attestation, documentation policy where lawful, assisted-sale path and privacy restrictions. Preview the B2C, mobile, POS and call-center experience and ensure equivalent inventory visibility. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/accessible-filters-eligibility-bo-1020` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How accessible seats are found and who may buy them, without exposing sensitive guest information.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setAccessibleSeating and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getAccessibleSeating` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **eligibility**: Filters and labels; proof required (for example Sanad card) shown, the guest's condition never stored on the seat. *(source: contracts/satellite/seating.yaml#setAccessibleSeating)*

#### Outputs: what the screen shows and produces

**Shown**

**Accessible seats, their routes and who may buy them** (detail panel, from `getAccessibleSeating`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Spaces | list or chips (count when long) | — |
| Seat | the name it points at, never the id | — |
| Kind | chip: Wheelchair space, Transfer seat, Ambulant, Easy access, Assistance dog, Hearing … | — |
| Route description | text | — |
| Step free | yes / no (icon or chip) | — |
| Nearest accessible wc | text | — |
| Eligibility | chip: Open, Self declared, Verified once, Verified each time | Contested in both directions. Open sale leaves none for the guests who need them; hard gating turns people away at the door. |
| Minimum provision percent | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accessible seating (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getAccessibleSeating` (onLoad, Accessible seats, their routes and who may buy them)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accessible filters eligibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accessible filters eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accessible filters eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accessible filters eligibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
eligibility:
  seatType: wheelchair
  proof: Sanad card
```

#### Permissions

- `setAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff
- `getAccessibleSeating` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1020` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1020`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 14: Works in Accessible Filters & Eligibility → Configure inclusive discovery without exposing sensitive guest information. Define filters and labels for wheelchair, companion, aisle, step-free, transfer, hearing, vision and service-animal needs. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accessible seating, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1021` Flexible Spacing Rules

**Support temporary public-health or operational spacing requirements. Configure distance, seat count, checkerboard, blocked-row, household-group and custom patterns. Apply by event, venue, zone, seat type or time window and preview capacity and revenue impact. Coordinate with group seating, accessible inventory, holds and sold seats and prevent retroactive unsafe changes. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/flexible-spacing-rules-bo-1021` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Temporary spacing (distance, checkerboard, blocked rows, household groups) applied by event, venue or zone.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `getSeatRules` ?seatMapId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **spacing pattern**: Pattern with the capacity it leaves. *(source: contracts/satellite/seating.yaml#setSeatRules / TRACKER Actions row 64)*

#### Outputs: what the screen shows and produces

**Shown**

**Kill, buffer, companion and accessibility rules** (detail panel, from `getSeatRules`)

| Shows | Format | Notes |
|---|---|---|
| Seat map | the name it points at, never the id | — |
| Killed seats | list or chips (count when long) | — |
| Kill reasons | grouped details | — |
| Buffer rule | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Seats either side | 1,234 | — |
| Rows either side | 1,234 | — |
| Avoid single gaps | yes / no (icon or chip) | The commercial case for buffers. A map leaving one empty seat between every party has lost those seats without anybody deciding to. |
| Companion rule | grouped details | The one with legal weight. Selling the companion seat separately strands a carer. |
| Enabled | yes / no (icon or chip) | — |
| Pairs | list or chips (count when long) | — |
| Wheelchair space | the name it points at, never the id | — |
| Companion seats | list or chips (count when long) | — |
| Release companion hours before | 1,234 | — |
| Flexible spacing | grouped details | — |
| Enabled | yes / no (icon or chip) | — |
| Density percent | 1,234 | — |
| Per performance override | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSeatRules` (onLoad, Kill, buffer, companion and accessibility rules)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The flexible spacing rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the flexible spacing rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No flexible spacing rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the flexible spacing rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
spacing:
  pattern: checkerboard
  capacityLeft: 52%
```

#### Permissions

- `setSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff
- `getSeatRules` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1021` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1021`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 16: Works in Flexible Spacing Rules → Support temporary public-health or operational spacing requirements. Configure distance, seat count, checkerboard, blocked-row, household-group and custom patterns. Apply by event, venue, zone, seat …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat rules, Cancel.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1022` Compliance Validation & Audit

**Demonstrate that seating rules and accessibility configuration are complete and enforced. Run validations for accessible quantities, companion ratios, route continuity, conflicts, labels and customer-channel parity. Provide issue severity, affected inventory, rule reference, owner, deadline, remediation and evidence. Retain configuration, approval, enforcement, release and override history with controlled compliance export. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 32 Board 8 - Group Reservations & Bulk Allocation Figure 8. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 33**

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
| Route | `/access-venue/compliance-validation-audit-bo-1022` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether the map still meets its obligations: accessible quantities against the legal ratio, companion ratios, route continuity, conflicts.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) validateSeatCompliance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of validateSeatCompliance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#validateSeatCompliance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Seat map | select field | — | — | — | — | Sends `?seatMapId=` (required). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Seat map | picker: choose a seat map | — | — | `validateSeatCompliance` ?seatMapId |

#### Outputs: what the screen shows and produces

**Shown**

**Breaches** (metric tile, from `validateSeatCompliance`): Count where `severity` is breach.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Breach, Warning, Advisory | — |

**Warnings** (metric tile, from `validateSeatCompliance`): Count where `severity` is warning.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Breach, Warning, Advisory | — |

**Findings** (data table, from `validateSeatCompliance`): Accessible quantities, companion ratios, route continuity, conflicts, labels and channel parity.

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Severity | chip: Breach, Warning, Advisory | — |
| Message | text | — |
| Required | 1,234.5 | — |
| Actual | 1,234.5 | — |
| Owner | text | not in the schema: `Owner` |

**The selected finding** (detail panel, from `validateSeatCompliance`): Rule reference, remediation and evidence are pack labels.

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Severity | chip: Breach, Warning, Advisory | — |
| Message | text | — |
| Required | 1,234.5 | — |
| Actual | 1,234.5 | — |
| Rule reference | text | not in the schema: `Rule reference` |
| Remediation | text | not in the schema: `Remediation` |
| Evidence | text | not in the schema: `Evidence` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run validation (secondary button) | `validateSeatCompliance` GET `/seat-compliance` | — | SeatComplianceFinding[] | — | — |
| Export compliance evidence (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **compliance checks**: Each check passed or failed with the required and actual numbers. *(source: contracts/satellite/seating.yaml#validateSeatCompliance)*

**Data it reads**: `validateSeatCompliance` (onLoad, Whether the map still complies)

**Where the user goes next**

- → `BO-1013` Rules Command Center: *Back to Rules Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The compliance validation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the compliance validation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No compliance validation audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the compliance validation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
check:
  rule: Wheelchair spaces 0.5% of capacity
  required: 16
  actual: 16
  result: passed
```

#### Permissions

- `validateSeatCompliance` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1022` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1022`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 7
- Flow F280 *Seat Management Venue Mapping Reference v1.0 board 7: Rules Command Center*, step 18: Works in Compliance Validation & Audit → Demonstrate that seating rules and accessibility configuration are complete and enforced. Run validations for accessible quantities, companion ratios, route continuity, conflicts, labels and …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run validation, Export compliance evidence.
- [ ] Every transition is wired: `BO-1013`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
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
"getAccessibleSeating": {"method":"GET","path":"/accessible-seating","contract":"seating","summary":"Accessible seats, their routes and who may buy them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"seatMapId","in":"query","required":true}],"requestBody":null,"responds":"AccessibleSeating"},
"getSeatRules": {"method":"GET","path":"/seat-rules","contract":"seating","summary":"Kill, buffer, companion and accessibility rules","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"seatMapId","in":"query","required":null}],"requestBody":null,"responds":"SeatRules"},
"setAccessibleSeating": {"method":"PUT","path":"/accessible-seating","contract":"seating","summary":"Define accessible seats, routes and eligibility","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessibleSeating","responds":"AccessibleSeating"},
"setSeatRules": {"method":"PUT","path":"/seat-rules","contract":"seating","summary":"Which seats are killed, buffered, paired or reserved for access","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRules","responds":"SeatRules"},
"validateSeatCompliance": {"method":"GET","path":"/seat-compliance","contract":"seating","summary":"Whether the map still meets its obligations","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"seatMapId","in":"query","required":true}],"requestBody":null,"responds":"SeatComplianceFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibleSeating": {"type":"object","x-ticvai-persistence":"seating.accessible","description":"Boards 7.6 to 7.8. **An accessible seat with no accessible route is not an accessible seat.**\n","properties":{"seatMapId":{"type":"string","format":"uuid"},"spaces":{"type":"array","items":{"type":"object","properties":{"seatId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["wheelchairSpace","transferSeat","ambulant","easyAccess","assistanceDog","hearingLoop","visuallyImpaired"]},"routeDescription":{"type":"string","nullable":true},"stepFree":{"type":"boolean","default":true},"nearestAccessibleWc":{"type":"string","nullable":true}}}},"eligibility":{"type":"string","enum":["open","selfDeclared","verifiedOnce","verifiedEachTime"],"default":"selfDeclared","description":"**Contested in both directions.** Open sale leaves none for the guests who need them; hard gating turns people away at the door.\n"},"minimumProvisionPercent":{"type":"number","nullable":true},"scopePath":{"type":"string"}}},
"SeatComplianceFinding": {"type":"object","description":"Board 7.10. **A map drifts below its obligation one kill rule at a time.**","properties":{"code":{"type":"string"},"severity":{"type":"string","enum":["breach","warning","advisory"]},"message":{"type":"string"},"required":{"type":"number","nullable":true},"actual":{"type":"number","nullable":true},"affectedSeatIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"SeatRules": {"type":"object","x-ticvai-persistence":"seating.seat_rules","description":"Board 7. **Four rules that move the same seats and are decided by different people.**\n","properties":{"seatMapId":{"type":"string","format":"uuid"},"killedSeatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"killReasons":{"type":"object","additionalProperties":{"type":"string"}},"bufferRule":{"type":"object","properties":{"enabled":{"type":"boolean","default":false},"seatsEitherSide":{"type":"integer","default":1},"rowsEitherSide":{"type":"integer","default":0},"avoidSingleGaps":{"type":"boolean","default":true,"description":"**The commercial case for buffers.** A map leaving one empty seat between every party has lost those seats without anybody deciding to.\n"}}},"companionRule":{"type":"object","description":"**The one with legal weight.** Selling the companion seat separately strands a carer.\n","properties":{"enabled":{"type":"boolean","default":true},"pairs":{"type":"array","items":{"type":"object","properties":{"wheelchairSpaceId":{"type":"string","format":"uuid"},"companionSeatIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"releaseCompanionHoursBefore":{"type":"integer","nullable":true}}},"flexibleSpacing":{"type":"object","properties":{"enabled":{"type":"boolean","default":false},"densityPercent":{"type":"integer","nullable":true},"perPerformanceOverride":{"type":"boolean","default":true}}},"scopePath":{"type":"string"}}}
}
```
