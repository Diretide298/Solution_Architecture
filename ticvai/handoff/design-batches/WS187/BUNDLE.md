# WS187 — Wallet Configuration Backend Structure v1.0 board 2

**10 screens · 8 operations · 9 schemas · 3 permissions**

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
  `WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1093` | Funding Command Center | C | 28 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-1094` | Funding Method Configuration | A | 38 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1095` | Top-Up Rule Configuration | C | 23 | 20 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-1096` | Channel & Funding Source Mapping | C | 20 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1097` | Auto-Reload Configuration | C | 18 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1098` | Recurring Funding Schedule | C | 17 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1099` | Funding Authorization & Approval Rules | C | 21 | 20 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-1100` | Funding Reversal & Correction Management | C | 12 | 15 | 6 | 28 | 1 | 0 | — | notStarted (—) |
| `BO-1101` | Funding Limits & Velocity Controls | C | 30 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1102` | Funding Transaction Audit & Reconciliation | C | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1093` Funding Command Center

**Provide administrators and finance/operations teams with a centralized view of all wallet funding activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1093 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/funding-command-center-bo-1093` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All funding activity in one place: top-ups by source and channel, and the funding rules in force.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Today | select field | — | — | — | — | — | — |
| Week | select field | — | — | — | — | — | — |
| Month | select field | — | — | — | — | — | — |
| Custom period | select field | — | — | — | — | — | — |
| Credit card | select field | — | — | — | — | — | — |
| Debit card | select field | — | — | — | — | — | — |
| Cash | select field | — | — | — | — | — | — |
| Online payment | select field | — | — | — | — | — | — |
| Gift card conversion | select field | — | — | — | — | — | — |
| Bank-linked funding | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Manual adjustment | select field | — | — | — | — | — | — |
| Auto-reload | select field | — | — | — | — | — | — |
| Recurring funding | select field | — | — | — | — | — | — |
| Successful top-ups | select field | — | — | — | — | — | — |
| Pending top-ups | select field | — | — | — | — | — | — |
| Failed top-ups | select field | — | — | — | — | — | — |
| Reversed top-ups | select field | — | — | — | — | — | — |
| Declined transactions | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Funding method | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Transaction status | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **funding activity**: By source and channel with totals. *(source: contracts/satellite/wallet.yaml#getWalletFundingRules / contracts/satellite/wallet.yaml#listWalletTransactions)*

**Data it reads**: `getWalletFundingRules` (onLoad, Funding rules in force)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1094` Funding Method Configuration: *Funding Method Configuration*
- → `BO-1095` Top-Up Rule Configuration: *Top-Up Rule Configuration*
- → `BO-1096` Channel & Funding Source Mapping: *Channel & Funding Source Mapping*
- → `BO-1097` Auto-Reload Configuration: *Auto-Reload Configuration*
- → `BO-1098` Recurring Funding Schedule: *Recurring Funding Schedule*
- → `BO-1099` Funding Authorization & Approval Rules: *Funding Authorization & Approval Rules*
- → `BO-1100` Funding Reversal & Correction Management: *Funding Reversal & Correction Management*; carries `subjectId`
- → `BO-1101` Funding Limits & Velocity Controls: *Funding Limits & Velocity Controls*
- → `BO-1102` Funding Transaction Audit & Reconciliation: *Funding Transaction Audit & Reconciliation*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The funding configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the funding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No funding configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
today:
  card: AED 31,200.00
  cash: AED 9,800.00
  kiosk: AED 7,200.00
```

#### Permissions

- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff
- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Top-up dashboard shows all top-ups (successful or failed) and funding-by-source breakdown (credit card, debit card, cash, etc.) with totals by day, month and year. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-515)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1093` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1093`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 1: Opens Funding Command Center → Provide administrators and finance/operations teams with a centralized view of all wallet funding activity.
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F294 branch at step 1 (expected): when Nothing has been set up on Funding Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F294 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1093?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1094`, `BO-1095`, `BO-1096`, `BO-1097`, `BO-1098`, `BO-1099`, `BO-1100`, `BO-1101`, `BO-1102`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1094` Funding Method Configuration

**Configure how wallets at this venue may be funded: which funding sources and channels are accepted, the minimum, maximum and preset top-ups, the amount above which a top-up needs approval, and automatic reload.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #28036 (APP-SETUP-BO-1094) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each method configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/funding-method-configuration-bo-1094` |

**What the spec says about it.** **Bound 4 October 2026 to WalletFundingRules, one rules object per venue: funding sources are a fixed list in the contract, not records, so the screen edits which are allowed rather than creating methods. Per-method fees and provider choice are not in the contract and left the screen** (CHG-FXS-002)

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How wallets may be funded: minimum and maximum top-up, preset amounts, channels, funding sources (card, cash, bank transfer, voucher, corporate account, loyalty conversion), bonuses, auto-reload on a balance threshold, recurring funding on a date, an approval threshold and velocity limits. Manual admin funding for service recovery is permission-controlled.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the auto-reload use case valid for the client?** → Drawn default accepted: Draw it, marked optional per wallet type. *(decided by Chinmay, 2026-10-02; DEC-105 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet type | picker: choose a wallet type | optional | — | — | shows names, sends the id | Options from listWalletTypes. | `WalletFundingRules.walletTypeId` |
| Funding sources | multi-select chips | optional | — | Card · Cash · Bank transfer · Voucher · Corporate account · Loyalty conversion | — | Card, cash, bank transfer, voucher, corporate account, loyalty conversion. | `WalletFundingRules.allowedFundingSources` |
| Channels | list of values (chips) | optional | — | — | — | — | `WalletFundingRules.allowedChannels` |
| Minimum top-up | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `WalletFundingRules.minimumTopUp` |
| Maximum top-up | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `WalletFundingRules.maximumTopUp` |
| Preset amounts | repeatable rows | optional | — | — | — | — | `WalletFundingRules.presetAmounts` |
| Approval above | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `WalletFundingRules.approvalAboveAmount` |

**Sent by *Save funding rules*** (`setWalletFundingRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wallet type `walletTypeId` | picker: choose a wallet type | optional | — | — | shows names, sends the id | — | `setWalletFundingRules` body |
| Minimum top up `minimumTopUp` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Maximum top up `maximumTopUp` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Preset amounts `presetAmounts` | repeatable rows | optional | — | — | — | — | `setWalletFundingRules` body |
| Allowed channels `allowedChannels` | list of values (chips) | optional | — | — | — | — | `setWalletFundingRules` body |
| Allowed funding sources `allowedFundingSources` | multi-select chips | optional | — | Card · Cash · Bank transfer · Voucher · Corporate account · Loyalty conversion | — | — | `setWalletFundingRules` body |
| Bonus rules `bonusRules` | repeatable rows | optional | — | — | — | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from the cash. | `setWalletFundingRules` body |
| Minimum amount `bonusRules[].minimumAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Bonus amount `bonusRules[].bonusAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Bonus percent `bonusRules[].bonusPercent` | number field | optional | — | — | — | — | `setWalletFundingRules` body |
| Bonus credit type `bonusRules[].bonusCreditTypeId` | picker: choose a bonus credit type | optional | — | — | shows names, sends the id | — | `setWalletFundingRules` body |
| Valid from `bonusRules[].validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setWalletFundingRules` body |
| Valid to `bonusRules[].validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setWalletFundingRules` body |
| Auto reload `autoReload` | group | optional | — | — | — | Board 2.5, matrix 4.3.28. Fires when the balance drops. | `setWalletFundingRules` body |
| Enabled `autoReload.enabled` | toggle | optional | off | — | — | — | `setWalletFundingRules` body |
| Threshold amount `autoReload.thresholdAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Reload amount `autoReload.reloadAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Maximum per day `autoReload.maximumPerDay` | number field | optional | — | — | — | — | `setWalletFundingRules` body |
| Recurring funding `recurringFunding` | group | optional | — | — | — | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. | `setWalletFundingRules` body |
| Enabled `recurringFunding.enabled` | toggle | optional | off | — | — | — | `setWalletFundingRules` body |
| Cadence `recurringFunding.cadence` | segmented control | optional | — | Daily · Weekly · Monthly | — | — | `setWalletFundingRules` body |
| Amount `recurringFunding.amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Day of week `recurringFunding.dayOfWeek` | text field | optional | — | — | — | — | `setWalletFundingRules` body |
| Day of month `recurringFunding.dayOfMonth` | number field | optional | — | — | — | — | `setWalletFundingRules` body |
| Approval above amount `approvalAboveAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Velocity limits `velocityLimits` | group | optional | — | — | — | A fraud control, not a commercial one. Ten top-ups of ninety-nine in an hour is a card being tested, and a daily cap in total value does not catch it. | `setWalletFundingRules` body |
| Max transactions per hour `velocityLimits.maxTransactionsPerHour` | number field | optional | — | — | — | — | `setWalletFundingRules` body |
| Max transactions per day `velocityLimits.maxTransactionsPerDay` | number field | optional | — | — | — | — | `setWalletFundingRules` body |
| Max amount per day `velocityLimits.maxAmountPerDay` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Max amount per month `velocityLimits.maxAmountPerMonth` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletFundingRules` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletFundingRules` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **bonusRules**: "Top up AED 200, get AED 20": the bonus is a separate credit lot of a separate credit type with its own expiry; show the type and expiry with the rule. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules)*
- **autoReload vs recurringFunding**: Two separate sections, because one fires when the balance drops and the other on a date. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules / TRACKER Actions row 108)*
- **velocityLimits**: Labelled as a fraud control (top-ups per hour, value per day), not a commercial limit. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Automatic reload** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save funding rules (primary button) | `setWalletFundingRules` PUT `/wallet-funding-rules` | WalletFundingRules | WalletFundingRules | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up); `listWalletTypes` (onLoad, The wallet type the rules apply to (walletTypeId))

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The form with the saved rules. |
| Error (`?state=error`) | Could not load. Names the read that failed; the form stays read-only. |
| Empty, first run (`?state=emptyFirstRun`) | Never saved: the defaults getWalletFundingRules returns. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WALLET_VIEW`, which `getWalletFundingRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WALLET_CONFIGURE` for `setWalletFundingRules`. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  walletType: Dune Park Wallet
  minimumTopUp: AED 50.00
  maximumTopUp: AED 2,000.00
  presets:
  - AED 100.00
  - AED 200.00
  - AED 500.00
  bonus: Top up 500, get 50 Bonus credit (expires in 90 days)
  approvalAbove: AED 1,000.00
  velocity: 5 top-ups an hour, AED 3,000 a day
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WALLET_VIEW`, which `getWalletFundingRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WALLET_CONFIGURE` for `setWalletFundingRules`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding methods: cash, card, online, POS, kiosk self-service, plus manual admin funding used to issue a goodwill/service-recovery credit to a guest's wallet. Chinmay raised role-based permission for staff funding wallets. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-516)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1094` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1094`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 2: Works in Funding Method Configuration → Configure which funding methods TICVAI wallets can accept. The source requires multiple methods for funding wallet value, including bank-linked funding, credit/debit cards through digital channels …

#### Acceptance for the design

- [ ] Every input above is drawn (38), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1094?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save funding rules, Cancel.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1095` Top-Up Rule Configuration

**Control the business rules governing individual wallet top-up transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1095 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/top-up-rule-configuration-bo-1095` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules for each top-up: minimum and maximum, presets, approval above an amount.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum top-up amount | select field | — | — | — | — | — | — |
| Maximum top-up amount | select field | — | — | — | — | — | — |
| Allowed increments | select field | — | — | — | — | — | — |
| Maximum number of top-ups per day | text field | — | — | — | — | — | — |
| Maximum number per week/month | text field | — | — | — | — | — | — |
| Maximum daily funding value | text field | — | — | — | — | — | — |
| Maximum monthly funding value | text field | — | — | — | — | — | — |
| Wallet maximum-balance check | select field | — | — | — | — | — | — |
| Customer-specific limits | select field | — | — | — | — | — | — |
| Wallet-type-specific limits | select field | — | — | — | — | — | — |
| Currency-specific limits | select field | — | — | — | — | — | — |
| Channel-specific limits | select field | — | — | — | — | — | — |
| Venue-specific limits | select field | — | — | — | — | — | — |
| Funding-source restrictions | select field | — | — | — | — | — | — |
| Anonymous-wallet restrictions | select field | — | — | — | — | — | — |
| Membership-specific rules | select field | — | — | — | — | — | — |
| Corporate-wallet rules | select field | — | — | — | — | — | — |
| Promotional top-up rules | select field | — | — | — | — | — | — |
| Reject | select field | — | — | — | — | — | — |
| Warn | select field | — | — | — | — | — | — |
| Request approval | select field | — | — | — | — | — | — |
| Hold transaction | select field | — | — | — | — | — | — |
| Route for risk review | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The top-up rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the top-up rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No top-up rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1094`: Same record (setWalletFundingRules).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  minimum: AED 50.00
  maximum: AED 2,000.00
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1095` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1095`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 4: Works in Top-Up Rule Configuration → Control the business rules governing individual wallet top-up transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1095?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1096` Channel & Funding Source Mapping

**Determine where each funding method may be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1096 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure funding availability across; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/channel-funding-source-mapping-bo-1096` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which funding methods each channel takes.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| B2C Website | select field | — | — | — | — | — | — |
| Customer Mobile App | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Mobile POS | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| Guest Services | select field | — | — | — | — | — | — |
| Call Center | select field | — | — | — | — | — | — |
| Back Office | select field | — | — | — | — | — | — |
| Corporate Portal | select field | — | — | — | — | — | — |
| Partner/Reseller | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |
| Third-party systems | select field | — | — | — | — | — | — |
| Channel eligibility | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Credit type generated | select field | — | — | — | — | — | — |
| Funding limits | select field | — | — | — | — | — | — |
| Authentication requirements | select field | — | — | — | — | — | — |
| Applicable venue | select field | — | — | — | — | — | — |
| Applicable customer type | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel to method**: Matrix of channels by funding sources. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel funding source configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel funding source untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel funding source configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
  Kiosk:
  - card
  - cash
  App:
  - card
  Point of sale:
  - card
  - cash
  - voucher
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1096` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1096`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 6: Works in Channel & Funding Source Mapping → Determine where each funding method may be used.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1096?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1097` Auto-Reload Configuration

**Configure automatic wallet replenishment when balances fall below predefined thresholds. The attached scope specifically requires automatic top-up when a wallet balance falls below a configurable threshold.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1097 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/auto-reload-configuration-bo-1097` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Automatic top-up when a balance falls below a threshold.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trigger Balance | select field | — | — | — | — | — | — |
| Eligible wallet types | select field | — | — | — | — | — | — |
| Eligible credit types | select field | — | — | — | — | — | — |
| Reload amount | select field | — | — | — | — | — | — |
| Maximum reload amount | select field | — | — | — | — | — | — |
| Maximum auto-reloads per day | text field | — | — | — | — | — | — |
| Maximum auto-reloads per month | text field | — | — | — | — | — | — |
| Payment method | select field | — | — | — | — | — | — |
| Stored payment instrument | select field | — | — | — | — | — | — |
| Customer consent required | select field | — | — | — | — | — | — |
| Consent validity | select field | — | — | — | — | — | — |
| Failed payment behavior | select field | — | — | — | — | — | — |
| Retry rules | select field | — | — | — | — | — | — |
| Maximum retries | select field | — | — | — | — | — | — |
| Notification rules | select field | — | — | — | — | — | — |
| Suspension after repeated failure | text field | — | — | — | — | — | — |
| Funding limits | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **autoReload**: Threshold and amount; the guest sets their own within these bounds. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules / contracts/satellite/wallet.yaml#setWalletAutoReloadSetting)*

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The auto-reload configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the auto-reload untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No auto-reload configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
autoReload:
  below: AED 20.00
  topUp: AED 100.00
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Auto-reload (tops up a configured amount when balance falls below a threshold) and a separate recurring funding schedule (calendar-based, e.g. a fixed amount every Monday). Allam: auto-reload is a nice-to-have without a confirmed use case; Chinmay: keep it for high-value/frequent guests. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-518)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1097` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1097`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 8: Works in Auto-Reload Configuration → Configure automatic wallet replenishment when balances fall below predefined thresholds. The attached scope specifically requires automatic top-up when a wallet balance falls below a configurable …

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1097?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1098` Recurring Funding Schedule

**Configure scheduled wallet funding independent of the wallet's current balance. The source specifically requires scheduled or recurring top-ups based on date, frequency, amount, payment method and customer authorization.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1098 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/recurring-funding-schedule-bo-1098` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Scheduled funding independent of balance (an allowance), by date and frequency.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Schedule name | select field | — | — | — | — | — | — |
| Source wallet/payment method | select field | — | — | — | — | — | — |
| Destination wallet | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Start date | select field | — | — | — | — | — | — |
| End date | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Execution time | select field | — | — | — | — | — | — |
| Maximum occurrences | select field | — | — | — | — | — | — |
| Funding limits | select field | — | — | — | — | — | — |
| Customer authorization | select field | — | — | — | — | — | — |
| Retry policy | select field | — | — | — | — | — | — |
| Failure behavior | select field | — | — | — | — | — | — |
| Notification rules | select field | — | — | — | — | — | — |
| Pause/resume | select field | — | — | — | — | — | — |
| Cancellation | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **recurringFunding**: Frequency, day, amount, payment method. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Specific day of month (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recurring funding schedule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recurring funding schedule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recurring funding schedule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recurring:
  frequency: monthly
  day: 1
  amount: AED 200.00
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Auto-reload (tops up a configured amount when balance falls below a threshold) and a separate recurring funding schedule (calendar-based, e.g. a fixed amount every Monday). Allam: auto-reload is a nice-to-have without a confirmed use case; Chinmay: keep it for high-value/frequent guests. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-518)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1098` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1098`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 10: Works in Recurring Funding Schedule → Configure scheduled wallet funding independent of the wallet's current balance. The source specifically requires scheduled or recurring top-ups based on date, frequency, amount, payment method and …

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1098?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Specific day of month.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1099` Funding Authorization & Approval Rules

**Apply governance and approval controls to wallet funding operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1099 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure approval based on; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/funding-authorization-approval-rules-bo-1099` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Approval controls on funding: above an amount a supervisor approves.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Funding amount | select field | — | — | — | — | — | — |
| Funding method | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Customer type | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Administrative user | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Risk score | select field | — | — | — | — | — | — |
| Single approval | select field | — | — | — | — | — | — |
| Multi-level approval | select field | — | — | — | — | — | — |
| Maker-checker control | select field | — | — | — | — | — | — |
| Role-based approval | select field | — | — | — | — | — | — |
| Amount threshold | select field | — | — | — | — | — | — |
| Approval SLA | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Auto-rejection after expiry | select field | — | — | — | — | — | — |
| Mandatory reason | select field | — | — | — | — | — | — |
| Supporting documentation | select field | — | — | — | — | — | — |
| Approval notifications | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **approvalAboveAmount**: Money; manual admin funding always needs approval. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules / DI-516)*

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The funding authorization approval configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the funding authorization approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No funding authorization approval configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
approval:
  above: AED 1,000.00
  approver: Supervisor
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1099` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1099`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 12: Works in Funding Authorization & Approval Rules → Apply governance and approval controls to wallet funding operations.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1099?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1100` Funding Reversal & Correction Management

**Provide controlled correction of incorrectly funded wallet transactions without deleting financial history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1100 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subjectId` (navigation) · cold entry: Opened from BO-1093 with the wallet holder picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/orders-money/funding-reversal-correction-management-bo-1100` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Correct a wrongly funded top-up without deleting history: full or partial reversal, which is not a spend.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only reverseWalletFunding, adjustWallet and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Eligible transaction status | select field | — | — | — | — | — | — |
| Maximum reversal period | select field | — | — | — | — | — | — |
| Full/partial reversal permission | select field | — | — | — | — | — | — |
| Required reason code | select field | — | — | — | — | — | — |
| Required notes | select field | — | — | — | — | — | — |
| Approval threshold | select field | — | — | — | — | — | — |
| Maker-checker requirement | select field | — | — | — | — | — | — |
| Original funding reference | select field | — | — | — | — | — | — |
| Related payment reference | select field | — | — | — | — | — | — |
| Financial posting requirement | select field | — | — | — | — | — | — |
| Customer notification | select field | — | — | — | — | — | — |
| Credit expiry impact | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Read a guest wallet** (detail panel, from `getWallet`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | — |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Credits | list or chips (count when long) | 4.3.5 and 4.3.19. One balance and one bonus balance with one expiry could not express what the requirement asks for — cash, bonus and … |
| Kind | chip: Cash, Bonus, Redemption, Refund, Goodwill | `cash` is money the guest paid and the others are not. That distinction decides what is refundable, what expires, and what shows as a … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Source ref | text | — |
| Is refundable | yes / no (icon or chip) | True only for `cash`. A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice. |
| Bonus balance | AED 1,234.50 | Promotional value. Typically non-refundable and spent first. |
| Currency | text | — |
| Status | chip: Active, Suspended, Closed | — |
| Home cell name | text | Where the authoritative balance lives. Present when the guest is linked across cells. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last activity at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Full reversal (primary button) | navigation or local | — | — | — | — |
| Partial reversal (secondary button) | navigation or local | — | — | — | — |
| Duplicate top-up correction (secondary button) | navigation or local | — | — | — | — |
| Failed funding correction (secondary button) | navigation or local | — | — | — | — |
| Payment reversal (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Reverse**: Reason and amount; posts as a reversal, visible in the ledger as such. *(source: contracts/satellite/wallet.yaml#reverseWalletFunding)*

**Data it reads**: `getWallet` (onLoad, Read a guest wallet)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The funding reversal correction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the funding reversal correction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No funding reversal correction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already spent below the reversal amount |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reversal:
  topUp: TU-2026-55120
  amount: AED 200.00
  reason: Top-up taken on wrong wallet
```

#### Permissions

- `reverseWalletFunding` → `WALLET_OPERATE` (operate) · staff
- `adjustWallet` → `WALLET_OPERATE` (operate) · staff
- `getWallet` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

28 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.113 | Refund management | Ticketing Catalogue | CONTRACTED | `adjustWallet` |
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 16 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1100` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1100`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 14: Works in Funding Reversal & Correction Management → Provide controlled correction of incorrectly funded wallet transactions without deleting financial history.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1100?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Full reversal, Partial reversal, Duplicate top-up correction, Failed funding correction, Payment reversal.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1101` Funding Limits & Velocity Controls

**Protect wallets against excessive or suspicious funding activity. The source specifically requires configurable maximum balance, daily top-up limit, single-transaction limit and user- specific limits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1101 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/funding-limits-velocity-controls-bo-1101` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Protection against excessive funding: maximum balance, daily top-up limit, single transaction limit, velocity.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletFundingRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Balance Limits | select field | — | — | — | — | — | — |
| Maximum wallet balance | select field | — | — | — | — | — | — |
| Maximum credit-type balance | select field | — | — | — | — | — | — |
| Transaction Limits | select field | — | — | — | — | — | — |
| Minimum funding | select field | — | — | — | — | — | — |
| Maximum single top-up | select field | — | — | — | — | — | — |
| Velocity Limits | select field | — | — | — | — | — | — |
| Maximum top-ups per hour | text field | — | — | — | — | — | — |
| Maximum top-ups per day | text field | — | — | — | — | — | — |
| Maximum daily amount | select field | — | — | — | — | — | — |
| Maximum weekly amount | select field | — | — | — | — | — | — |
| Maximum monthly amount | select field | — | — | — | — | — | — |
| Source Limits | select field | — | — | — | — | — | — |
| Maximum per payment instrument | text field | — | — | — | — | — | — |
| Maximum cash funding | select field | — | — | — | — | — | — |
| Maximum gift-card conversion | select field | — | — | — | — | — | — |
| Maximum promotional funding | select field | — | — | — | — | — | — |
| Customer Limits | select field | — | — | — | — | — | — |
| Individual | select field | — | — | — | — | — | — |
| Child | select field | — | — | — | — | — | — |
| Family | select field | — | — | — | — | — | — |
| Corporate | select field | — | — | — | — | — | — |
| Employee | select field | — | — | — | — | — | — |
| Guest | select field | — | — | — | — | — | — |
| Allow | select field | — | — | — | — | — | — |
| Warn | select field | — | — | — | — | — | — |
| Decline | select field | — | — | — | — | — | — |
| Hold | select field | — | — | — | — | — | — |
| Require MFA | select field | — | — | — | — | — | — |
| Require approval | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **velocityLimits**: Labelled as fraud controls. *(source: contracts/satellite/wallet.yaml#setWalletFundingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**How a wallet may be topped up** (detail panel, from `getWalletFundingRules`)

| Shows | Format | Notes |
|---|---|---|
| Wallet type | the name it points at, never the id | — |
| Minimum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum top up | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Preset amounts | list or chips (count when long) | — |
| Allowed channels | list or chips (count when long) | — |
| Allowed funding sources | list or chips (count when long) | — |
| Bonus rules | list or chips (count when long) | Board 2.3. *Top up 200, get 20.* The bonus is a separate lot of a separate credit type, which is how it can expire on different terms from … |
| Minimum amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Bonus percent | 1,234.5 | — |
| Bonus credit type | the name it points at, never the id | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Auto reload | grouped details | Board 2.5, matrix 4.3.28. Fires when the balance drops. |
| Enabled | yes / no (icon or chip) | — |
| Threshold amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reload amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Maximum per day | 1,234 | — |
| Recurring funding | grouped details | Board 2.6, matrix 4.3.29 — *"distinct from auto-reload"*. Fires on a date, which is what an allowance needs. |
| Enabled | yes / no (icon or chip) | — |

**Data it reads**: `getWalletFundingRules` (onLoad, How a wallet may be topped up)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The funding limits velocity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the funding limits velocity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No funding limits velocity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
limits:
  maxBalance: AED 5,000.00
  daily: AED 3,000.00
  perHour: 5
```

#### Permissions

- `setWalletFundingRules` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletFundingRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding limits and velocity controls (daily, monthly, min and max transaction thresholds), and a funding audit trail listing all top-up transactions for any period or account. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-521)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1101` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1101`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 16: Works in Funding Limits & Velocity Controls → Protect wallets against excessive or suspicious funding activity. The source specifically requires configurable maximum balance, daily top-up limit, single-transaction limit and user- specific limits.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1101?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1102` Funding Transaction Audit & Reconciliation

**Provide a complete administrative record of every value entering a wallet. The source requires a complete audit trail for wallet top-ups, payments, refunds, transfers, adjustments, expirations, reversals and administrative actions. Configure the intelligence behind the TICVAI wallet balance: what types of value can be stored, where each credit can be spent, when it expires, which balance is consumed first, how FEFO operates, and how credits behave across Ticketing, F&B, Retail, Attractions, Parking, Membership and other TICVAI services. This board directly addresses requirements including multiple credit types, configurable expiry, usage criteria, FEFO consumption, stored-value balances, membership-related credits, and wallet reporting.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1102 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/funding-transaction-audit-reconciliation-bo-1102` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The record of every value entering wallets, and the reconciliation of the wallet sub-ledger against the general ledger and the acquirer.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payment succeeded but wallet not funded (primary button) | navigation or local | — | — | — | — |
| Wallet funded but payment unresolved (secondary button) | navigation or local | — | — | — | — |
| Duplicate funding (secondary button) | navigation or local | — | — | — | — |
| Missing external reference (secondary button) | navigation or local | — | — | — | — |
| Unreconciled transaction (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **three-way reconciliation**: Wallet, ledger and acquirer totals side by side with differences. *(source: contracts/satellite/wallet.yaml#getWalletReconciliation)*

**Data it reads**: `getWalletReconciliation` (onLoad, Against the acquirer and the ledger)

**Where the user goes next**

- → `BO-1093` Funding Command Center: *Back to Funding Command Center*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The funding transaction audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the funding transaction audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No funding transaction audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the funding transaction audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recon:
  wallet: AED 48,200.00
  ledger: AED 48,200.00
  acquirer: AED 48,050.00
  difference: AED 150.00
```

#### Permissions

- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest
- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding limits and velocity controls (daily, monthly, min and max transaction thresholds), and a funding audit trail listing all top-up transactions for any period or account. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-521)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1102` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1102`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 2
- Flow F294 *Wallet Configuration Backend Structure v1.0 board 2: Funding Command Center*, step 18: Works in Funding Transaction Audit & Reconciliation → Provide a complete administrative record of every value entering a wallet. The source requires a complete audit trail for wallet top-ups, payments, refunds, transfers, adjustments, expirations …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1102?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payment succeeded but wallet not funded, Wallet funded but payment unresolved, Duplicate funding, Missing external reference, Unreconciled transaction.
- [ ] Every transition is wired: `BO-1093`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustWallet": {"method":"POST","path":"/wallets/{subjectId}/adjust","contract":"wallet","summary":"Manually adjust a wallet balance","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWalletFundingRules": {"method":"GET","path":"/wallet-funding-rules","contract":"wallet","summary":"How a wallet may be topped up","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WalletFundingRules"},
"getWalletReconciliation": {"method":"GET","path":"/wallet-reconciliation","contract":"wallet","summary":"The wallet sub-ledger against the general ledger and the acquirer","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"WalletReconciliation"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletTypes": {"method":"GET","path":"/wallet-types","contract":"wallet","summary":"The kinds of wallet that may exist — who owns one","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WalletType"},
"reverseWalletFunding": {"method":"POST","path":"/wallet-funding/reversals","contract":"wallet","summary":"Undo a top-up, in full or in part","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletAdjustment"},
"setWalletFundingRules": {"method":"PUT","path":"/wallet-funding-rules","contract":"wallet","summary":"Amounts, channels, bonuses, limits and velocity","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletFundingRules","responds":"WalletFundingRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletAdjustment": {"type":"object","x-ticvai-persistence":"wallet.adjustment","description":"Board 7.7. **A correction, distinguishable from a spend.**","properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["reversal","chargeback","goodwill","correction","writeOff"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"affectedLotIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string"},"performedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"WalletFundingRules": {"type":"object","x-ticvai-persistence":"wallet.funding_rules","description":"Board 2, which is the 27 August minute one screen for one.","properties":{"walletTypeId":{"type":"string","format":"uuid","nullable":true},"minimumTopUp":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumTopUp":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"presetAmounts":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"allowedChannels":{"type":"array","items":{"type":"string"}},"allowedFundingSources":{"type":"array","items":{"type":"string","enum":["card","cash","bankTransfer","voucher","corporateAccount","loyaltyConversion"]}},"bonusRules":{"type":"array","description":"Board 2.3. *Top up 200, get 20.* **The bonus is a separate lot of a separate credit type**, which is how it can expire on different terms from the cash.\n","items":{"type":"object","properties":{"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"bonusAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"bonusPercent":{"type":"number","nullable":true},"bonusCreditTypeId":{"type":"string","format":"uuid"},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true}}}},"autoReload":{"type":"object","description":"Board 2.5, matrix 4.3.28. **Fires when the balance drops.**","properties":{"enabled":{"type":"boolean","default":false},"thresholdAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reloadAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumPerDay":{"type":"integer","nullable":true}}},"recurringFunding":{"type":"object","description":"Board 2.6, matrix 4.3.29 — ***\"distinct from auto-reload\"***. **Fires on a date**, which is what an allowance needs.\n","properties":{"enabled":{"type":"boolean","default":false},"cadence":{"type":"string","enum":["daily","weekly","monthly"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"dayOfWeek":{"type":"string","nullable":true},"dayOfMonth":{"type":"integer","nullable":true}}},"approvalAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"velocityLimits":{"type":"object","description":"**A fraud control, not a commercial one.** Ten top-ups of ninety-nine in an hour is a card being tested, and a daily cap in total value does not catch it.\n","properties":{"maxTransactionsPerHour":{"type":"integer","nullable":true},"maxTransactionsPerDay":{"type":"integer","nullable":true},"maxAmountPerDay":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmountPerMonth":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"scopePath":{"type":"string"}}},
"WalletReconciliation": {"type":"object","description":"Board 9.4. **Three sources, and the exception names which pair disagrees.**","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"subLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"generalLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptions":{"type":"array","items":{"type":"object","properties":{"pair":{"type":"string","enum":["subLedgerVsGeneralLedger","subLedgerVsAcquirer","generalLedgerVsAcquirer"]},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"likelyCause":{"type":"string","nullable":true}}}}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]},
"WalletType": {"type":"object","x-ticvai-persistence":"wallet.wallet_type","description":"Board 1.2. **Who owns a wallet** — the first of the two vocabularies.","required":["code","name"],"properties":{"autoReloadAllowed":{"type":"boolean","default":true,"description":"**Auto-reload is optional per wallet type** (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). Where false, a holder of this type cannot set an auto top-up (`setWalletAutoReloadSetting` refuses it) whatever the venue's `WalletFundingRules.autoReload` says."},"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"ownerKind":{"type":"string","enum":["guest","registeredCustomer","family","parent","child","corporate","school","employee"]},"storedValueCapability":{"type":"boolean","default":true,"description":"Board 1.2. Whether this wallet holds a balance at all. A pure entitlement wallet — passes and vouchers, no money — does not.\n"},"topUpCapability":{"type":"boolean","default":false},"transferCapability":{"type":"boolean","default":false},"refundCapability":{"type":"boolean","default":false},"giftCardSupport":{"type":"boolean","default":false},"voucherSupport":{"type":"boolean","default":false},"membershipCreditSupport":{"type":"boolean","default":false},"wearableSupport":{"type":"boolean","default":false},"usageChannels":{"type":"array","description":"**Where this wallet may be used, declared on the type itself.** Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and this is what lets one `topUpWallet` serve every caller: the operation is shared and the type says which channel may reach it. `WalletChannelRules` still governs the per-credential detail — PIN thresholds, offline floor limits — and this governs whether the channel is open at all.\n","items":{"type":"string","enum":["online","pos","mobileApp","api","kiosk","reader"]}},"presetName":{"type":"string","description":"**The client's own name for this composition** — \"Resort Wallet\", \"Cashless Venue Wallet\", \"Closed-Loop Wallet\". Board 1.2 lists thirteen such names as examples, not as kinds: they are combinations of `ownerKind`, `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client's vocabulary without hard-coding it into an enum.\n"},"holderMayDifferFromOwner":{"type":"boolean","default":false,"description":"**A child wallet's owner is the parent.** Without this the model has to pretend a seven-year-old holds an account.\n"},"requiresIdentification":{"type":"boolean","default":false},"maximumBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowNegativeBalance":{"type":"boolean","default":false},"sharedStructureAllowed":{"type":"boolean","default":false},"lifecycleStates":{"type":"array","items":{"type":"string"}},"numberingPattern":{"type":"string","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}}
}
```
