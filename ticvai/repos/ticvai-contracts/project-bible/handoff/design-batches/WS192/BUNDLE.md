# WS192 — Wallet Configuration Backend Structure v1.0 board 7

**10 screens · 19 operations · 23 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `APPROVAL_CONFIGURE, ORDER_REFUND, ORDER_VIEW, REGION_CONFIGURE, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1143` | Wallet Operations Command Center | B–D | 2 | 46 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-1144` | Peer-to-Peer Transfer Configuration | B–D | 21 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1145` | Transfer Eligibility, Limits & Approval Rules | B–D | 19 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-1146` | Refund-to-Wallet Policy Configuration | B–D | 21 | 11 | 6 | 0 | 3 | 6 | — | notStarted (—) |
| `BO-1147` | Refund Routing & Credit Restoration Engine | B–D | 6 | 40 | 6 | 6 | 0 | 6 | — | notStarted (—) |
| `BO-1148` | Reversal & Transaction Correction Management | B–D | 11 | 14 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-1149` | Administrative Balance Adjustment Studio | B–D | 9 | 35 | 6 | 77 | 1 | 0 | — | notStarted (—) |
| `BO-1150` | Wallet Block, Freeze & Restriction Management | B–D | 6 | 15 | 6 | 28 | 0 | 6 | — | notStarted (—) |
| `BO-1151` | Wallet Disputes & Operational Exception Queue | B–D | 24 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1152` | Operations Simulator, Approval & Audit Trail | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-1152 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1143` Wallet Operations Command Center

**Provide operations, finance and customer-service administrators with a centralized view of wallet operational activity and exceptions. Dashboard KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/wallet-operations-command-center-bo-1143` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet operational activity and exceptions: disputes, failures, unusual activity.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletDisputes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletDisputes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search wallet operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, wallet type, customer, operation, credit type and 6 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet operations** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transfers today | text | not in the schema: `Transfers Today` |
| Transfer value | text | not in the schema: `Transfer Value` |
| Refunds today | text | not in the schema: `Refunds Today` |
| Refund value | text | not in the schema: `Refund Value` |
| Reversals | text | not in the schema: `Reversals` |
| Manual adjustments | text | not in the schema: `Manual Adjustments` |
| Blocked wallets | text | not in the schema: `Blocked Wallets` |
| Frozen balances | text | not in the schema: `Frozen Balances` |
| Pending operations | text | not in the schema: `Pending Operations` |
| Failed operations | text | not in the schema: `Failed Operations` |
| Disputed transactions | text | not in the schema: `Disputed Transactions` |
| Operations awaiting approval | text | not in the schema: `Operations Awaiting Approval` |
| Activity breakdown | text | not in the schema: `Activity Breakdown` |
| P2 p transfer | text | not in the schema: `P2P Transfer` |
| Refund | text | not in the schema: `Refund` |
| Reversal | text | not in the schema: `Reversal` |
| Credit adjustment | text | not in the schema: `Credit Adjustment` |
| Debit adjustment | text | not in the schema: `Debit Adjustment` |
| Wallet block | text | not in the schema: `Wallet Block` |
| Wallet unblock | text | not in the schema: `Wallet Unblock` |
| Balance freeze | text | not in the schema: `Balance Freeze` |
| Correction | text | not in the schema: `Correction` |
| Administrative operation | text | not in the schema: `Administrative Operation` |

**The selected wallet operations** (detail panel): The pack groups this record's detail under its own headings: “Highlight”.

| Shows | Format | Notes |
|---|---|---|
| Transfers today | text | not in the schema: `Transfers Today` |
| Transfer value | text | not in the schema: `Transfer Value` |
| Refunds today | text | not in the schema: `Refunds Today` |
| Refund value | text | not in the schema: `Refund Value` |
| Reversals | text | not in the schema: `Reversals` |
| Manual adjustments | text | not in the schema: `Manual Adjustments` |
| Blocked wallets | text | not in the schema: `Blocked Wallets` |
| Frozen balances | text | not in the schema: `Frozen Balances` |
| Pending operations | text | not in the schema: `Pending Operations` |
| Failed operations | text | not in the schema: `Failed Operations` |
| Disputed transactions | text | not in the schema: `Disputed Transactions` |
| Operations awaiting approval | text | not in the schema: `Operations Awaiting Approval` |
| Activity breakdown | text | not in the schema: `Activity Breakdown` |
| P2 p transfer | text | not in the schema: `P2P Transfer` |
| Refund | text | not in the schema: `Refund` |
| Reversal | text | not in the schema: `Reversal` |
| Credit adjustment | text | not in the schema: `Credit Adjustment` |
| Debit adjustment | text | not in the schema: `Debit Adjustment` |
| Wallet block | text | not in the schema: `Wallet Block` |
| Wallet unblock | text | not in the schema: `Wallet Unblock` |
| Balance freeze | text | not in the schema: `Balance Freeze` |
| Correction | text | not in the schema: `Correction` |
| Administrative operation | text | not in the schema: `Administrative Operation` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **exceptions**: Open disputes and exceptions by age. *(source: contracts/satellite/wallet.yaml#listWalletDisputes)*

**Data it reads**: `listWalletDisputes` (onLoad, Open exceptions)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1144` Peer-to-Peer Transfer Configuration: *Peer-to-Peer Transfer Configuration*
- → `BO-1145` Transfer Eligibility, Limits & Approval Rules: *Transfer Eligibility, Limits & Approval Rules*
- → `BO-1146` Refund-to-Wallet Policy Configuration: *Refund-to-Wallet Policy Configuration*; carries `venueId`
- → `BO-1147` Refund Routing & Credit Restoration Engine: *Refund Routing & Credit Restoration Engine*; carries `orderId`
- → `BO-1148` Reversal & Transaction Correction Management: *Reversal & Transaction Correction Management*; carries `subjectId`
- → `BO-1149` Administrative Balance Adjustment Studio: *Administrative Balance Adjustment Studio*; carries `subjectId`
- → `BO-1150` Wallet Block, Freeze & Restriction Management: *Wallet Block, Freeze & Restriction Management*; carries `walletId`, `subjectId`
- → `BO-1151` Wallet Disputes & Operational Exception Queue: *Wallet Disputes & Operational Exception Queue*; carries `disputeId`
- → `BO-1152` Operations Simulator, Approval & Audit Trail: *Operations Simulator, Approval & Audit Trail*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
open:
  disputes: 6
  failedCharges: 2
```

#### Permissions

- `listWalletDisputes` → `WALLET_VIEW` (read) · staff
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

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1143` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1143`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 1: Opens Wallet Operations Command Center → Provide operations, finance and customer-service administrators with a centralized view of wallet operational activity and exceptions. Dashboard KPIs
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F299 branch at step 1 (expected): when Nothing has been set up on Wallet Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F299 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1143?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1144`, `BO-1145`, `BO-1146`, `BO-1147`, `BO-1148`, `BO-1149`, `BO-1150`, `BO-1151`, `BO-1152`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1144` Peer-to-Peer Transfer Configuration

**Configure direct value transfers between independent TICVAI wallet accounts. Requirement 4.3.16 specifically requires guests to transfer money from their wallet to another guest's wallet. Transfer Methods**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/peer-to-peer-transfer-configuration-bo-1144` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet transfer rules that setWalletTransferRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Peer-to-peer transfers between guests' wallets: whether allowed (a venue toggle), limits, approvals.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletTransferRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| P2P enabled | select field | — | — | — | — | — | — |
| Eligible wallet types | select field | — | — | — | — | — | — |
| Eligible customer types | select field | — | — | — | — | — | — |
| Eligible credit types | select field | — | — | — | — | — | — |
| Supported currencies | select field | — | — | — | — | — | — |
| Minimum transfer | select field | — | — | — | — | — | — |
| Maximum transfer | select field | — | — | — | — | — | — |
| Daily transfer amount | select field | — | — | — | — | — | — |
| Monthly transfer amount | select field | — | — | — | — | — | — |
| Maximum transfer count | select field | — | — | — | — | — | — |
| Transfer fee | select field | — | — | — | — | — | — |
| Recipient verification | select field | — | — | — | — | — | — |
| Sender authentication | select field | — | — | — | — | — | — |
| Recipient confirmation | select field | — | — | — | — | — | — |
| Transfer expiry | select field | — | — | — | — | — | — |
| Cross-tenant transfer | select field | — | — | — | — | — | — |
| Cross-venue transfer | select field | — | — | — | — | — | — |
| Cross-currency transfer | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |
| Wallet A | select field | — | — | — | — | — | — |
| Cash Credit: AED 500 | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **transfer rules**: Off by default; limits and approval when on. *(source: contracts/satellite/wallet.yaml#setWalletTransferRules / DI-535 / TRACKER Actions row 115)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet ID (primary button) | navigation or local | — | — | — | — |
| Customer ID (secondary button) | navigation or local | — | — | — | — |
| Membership ID (secondary button) | navigation or local | — | — | — | — |
| Contact selection (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The peer-to-peer transfer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the peer-to-peer transfer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No peer-to-peer transfer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  enabled: false
```

#### Permissions

- `setWalletTransferRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1144` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1144`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 2: Works in Peer-to-Peer Transfer Configuration → Configure direct value transfers between independent TICVAI wallet accounts. Requirement 4.3.16 specifically requires guests to transfer money from their wallet to another guest's wallet. Transfer …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1144?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Wallet ID, Customer ID, Membership ID, Contact selection, API.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1145` Transfer Eligibility, Limits & Approval Rules

**Apply governance controls to wallet-to-wallet transfers. Eligibility**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/transfer-eligibility-limits-approval-rules-bo-1145` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet transfer rules that setWalletTransferRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Eligibility, limits and approvals of wallet-to-wallet transfers.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletTransferRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet type | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Customer verification status | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Customer age | select field | — | — | — | — | — | — |
| Family role | select field | — | — | — | — | — | — |
| Corporate role | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Country/region where applicable | select field | — | — | — | — | — | — |
| Credit Transferability | select field | — | — | — | — | — | — |
| Per transaction | select field | — | — | — | — | — | — |
| Per hour | select field | — | — | — | — | — | — |
| Daily | select field | — | — | — | — | — | — |
| Weekly | select field | — | — | — | — | — | — |
| Monthly | select field | — | — | — | — | — | — |
| Recipient limits | select field | — | — | — | — | — | — |
| Sender limits | select field | — | — | — | — | — | — |
| Approval / Authentication | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **limits**: Per transfer, per day, verified accounts only. *(source: contracts/satellite/wallet.yaml#setWalletTransferRules)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transfer eligibility limits configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transfer eligibility limits untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No transfer eligibility limits configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
limits:
  perTransfer: AED 200.00
  perDay: AED 500.00
  verifiedOnly: true
```

#### Permissions

- `setWalletTransferRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1145` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1145`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 4: Works in Transfer Eligibility, Limits & Approval Rules → Apply governance controls to wallet-to-wallet transfers. Eligibility

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1145?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1146` Refund-to-Wallet Policy Configuration

**Configure when refunds from TICVAI transactions may be returned directly to a digital wallet. Requirement 4.3.15 specifically requires instant refund to the digital wallet with customer notification. Refund Sources Ticket cancellation Event cancellation F&B refund Retail return Rental refund Parking refund Membership adjustment Attraction cancellation Failed service Customer-service compensation Refund Destinations**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `REGION_CONFIGURE`, `WALLET_CONFIGURE` (1 read, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Refund policy can define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `venueId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/orders-money/refund-to-wallet-policy-configuration-bo-1146` |

**What the spec says about it.** **Two sections, gated separately (PR-6; design-note correction, 2 October 2026):** the venue refund policy (`setRefundPolicy`, region configuration) and the refund-to-wallet policy (`setWalletRefundPolicy`, wallet configuration). A user holding one sees the other read-only.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A per-source refund destination in the wallet refund policy (ticket, event, F&B, retail, rental, parking, membership, compensation), or a narrowed …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a refund goes: to the original payment method, to the guest's TICVAI wallet, or the guest's choice; whether money returns to the credit lots it came from with their original expiry; any bonus for taking wallet credit. It sits with the venue's refund policy thresholds. A refund to a wallet and a refund to a card are different promises, and which one a guest gets must not depend on who is at the counter.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The purpose lists refund sources (ticket, event, F&B, retail, rental, parking, membership, compensation) that the policy cannot distinguish; the wallet refund policy has one default destination for all. (CHG-WIR-027)

**Fixed on main** (the package already carries these; draw what it says): setRefundPolicy needs REGION_CONFIGURE while setWalletRefundPolicy needs WALLET_CONFIGURE on the same screen. (CHG-SBO-010); No read operation: the screen declares only setRefundPolicy, setWalletRefundPolicy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Original wallet | select field | — | — | — | — | — | — |
| Refund Credit bucket | select field | — | — | — | — | — | — |
| Cash Credit | select field | — | — | — | — | — | — |
| Original gift-card balance | select field | — | — | — | — | — | — |
| Original credit bucket | select field | — | — | — | — | — | — |
| External payment method | select field | — | — | — | — | — | — |
| Rules | select field | — | — | — | — | — | — |
| Instant wallet refund | select field | — | — | — | — | — | — |
| Full refund | select field | — | — | — | — | — | — |
| Partial refund | select field | — | — | — | — | — | — |
| Refund amount limit | select field | — | — | — | — | — | — |
| Refund fee | select field | — | — | — | — | — | — |
| Refund validity | select field | — | — | — | — | — | — |
| Refund-credit expiry | select field | — | — | — | — | — | — |
| Transferability | select field | — | — | — | — | — | — |
| Withdrawal eligibility | select field | — | — | — | — | — | — |
| Original tender dependency | select field | — | — | — | — | — | — |
| Original customer requirement | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |
| Wallet → AED 200 returned | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **defaultDestination**: Original payment method, TICVAI wallet, or guest's choice, each with a sentence of what the guest is told. *(source: contracts/satellite/wallet.yaml#setWalletRefundPolicy / DI-468 / DI-673)*
- **restoreToOriginalLots and restoreOriginalExpiry**: Both on by default; turning off "original expiry" shows the warning that a fresh expiry is a gift. *(source: contracts/satellite/wallet.yaml#/components/schemas/WalletRefundPolicy)*
- **walletRefundBonusPercent**: Optional incentive shown as "+5% if refunded to wallet". *(source: contracts/satellite/wallet.yaml#/components/schemas/WalletRefundPolicy)*
- **refund policy thresholds**: Self-authorise limit, second user above, approval above, time bands, refund window days (0 means day of purchase only; empty means no window), partial allowed. *(source: contracts/spine/orders.yaml#setRefundPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Read a venue's refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | The venue in the path. Not taken from a `setRefundPolicy` body. |
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Hours before | 1,234 | — |
| Percentage | 12.5% | — |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**Data it reads**: `getRefundPolicy` (onLoad, Read a venue's refund policy)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refund-to-wallet policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refund-to-wallet policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refund-to-wallet policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` (`refund-thresholds-not-ascending` … |

#### Consistency with other screens

- Match `BO-023`: The refund dialog offers exactly the destinations configured here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  defaultDestination: guestChoice
  restoreToOriginalLots: true
  restoreOriginalExpiry: true
  walletRefundBonusPercent: 5
  refundWindowDays: 30
  selfAuthoriseLimit: AED 500.00
  approvalAbove: AED 2,000.00
```

#### Permissions

- `setRefundPolicy` → `REGION_CONFIGURE` (configure) · staff
- `setWalletRefundPolicy` → `WALLET_CONFIGURE` (configure) · staff
- `getRefundPolicy` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- End-of-visit unload/refund: a guest can unload the remaining balance at a counter after a balance check. Configurable venue-level toggle, not always on. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-535)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1146` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1146`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 6: Works in Refund-to-Wallet Policy Configuration → Configure when refunds from TICVAI transactions may be returned directly to a digital wallet. Requirement 4.3.15 specifically requires instant refund to the digital wallet with customer notification. …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (404, 412, 422).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1146?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `REGION_CONFIGURE`, `WALLET_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1147` Refund Routing & Credit Restoration Engine

**Determine exactly where returned value goes when the original transaction consumed multiple wallet credits. This is important because a simple “+AED 200 to Cash Credit” can corrupt wallet economics. Example**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND`, `ORDER_VIEW`, `WALLET_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `orderId` (navigation) |
| Route | `/orders-money/refund-routing-credit-restoration-engine-bo-1147` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where refunded value goes when a purchase used several credits: back to the lots it came from with their original expiry, not "+AED 200 to cash".

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletRefundPolicy, createRefund and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Restore with original expiry | text field | — | — | — | — | — | — |
| Restore with new validity | text field | — | — | — | — | — | — |
| Convert to refund credit | text field | — | — | — | — | — | — |
| Do not restore | select field | — | — | — | — | — | — |
| Require administrator approval | select field | — | — | — | — | — | — |
| FEFO Interaction | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Read an order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Charge currency | text | The currency the guest selected and is charged in (CHG-FIN-001, 2 October 2026). |
| Charge FX rate | text | Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`) … |
| Charge FX rate | the name it points at, never the id | The `finance.FxRate` row the rate was taken from, for audit. |
| Charge total | AED 1,234.50 | `grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to … |
| Charge rate locked until | 1 Oct 2026, 14:30 | The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms … |
| Dropped promotions | list or chips (count when long) | Promotions left off this order at checkout because their budget cap would have been exceeded (decided 28 September, audit R101 (8)). |
| Promotion | the name it points at, never the id | — |
| Name | text | — |
| Reason | chip: Budget cap reached | — |

**List refunds against an order** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Tender currency | text | A refund goes back in the currency the guest paid (decided 2 October 2026, Chinmay; CHG-FIN-001). |
| Tender amount | AED 1,234.50 | The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001). |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |
| Secondary principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Ledger entry | the name it points at, never the id | Written before the gateway is called. |
| Gateway reference | text | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `getOrder` (onLoad, Read an order); `listOrderRefunds` (onLoad, List refunds against an order)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refund routing credit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refund routing credit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refund routing credit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem) |

#### Consistency with other screens

- Match `BO-1146`: Same wallet refund policy record.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
refund:
  purchase: AED 200.00 = Bonus 50 + Gift card 150
  restored:
  - Bonus AED 50.00 (expires 31 Dec)
  - Gift card AED 150.00
```

#### Permissions

- `setWalletRefundPolicy` → `WALLET_CONFIGURE` (configure) · staff
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.12.3 | The system provide the ability for cashiers to issue refund up to a certain value with another user (cashier or supervisor) putting in their name as an audit control. | Ticketing Sales | CONTRACTED | `createRefund` |
| 2.12.13 | The system should change ticket status to Refunded after the Refund transaction is posted. Refund transaction should be linked with the ticket identifier to allow for reconciliation. There should be … | Ticketing Sales | CONTRACTED | `createRefund` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1147` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1147`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 8: Works in Refund Routing & Credit Restoration Engine → Determine exactly where returned value goes when the original transaction consumed multiple wallet credits. This is important because a simple “+AED 200 to Cash Credit” can corrupt wallet economics. …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1147?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `ORDER_REFUND`, `ORDER_VIEW`, `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1148` Reversal & Transaction Correction Management

**Correct operational wallet transactions while maintaining an immutable ledger. Supported Operations Payment reversal Transfer reversal Refund reversal Duplicate debit correction Duplicate credit correction Failed transaction correction Offline synchronization correction Incorrect wallet correction Incorrect amount correction Important Rule Never delete or overwrite the original wallet ledger transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/reversal-transaction-correction-management-bo-1148` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): Reversals of payments, transfers and refunds on a wallet (reverseWalletFunding reverses a top-up only).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Correct wallet transactions while the ledger stays immutable: reversals of payments, transfers, refunds, duplicates.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The only operation reverses a top-up; payment, transfer and refund reversals have no operation. (CHG-WIR-027)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only reverseWalletFunding and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Eligible transaction type | select field | — | — | — | — | — | — |
| Reversal period | select field | — | — | — | — | — | — |
| Full reversal | select field | — | — | — | — | — | — |
| Partial reversal | select field | — | — | — | — | — | — |
| Reason code | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Supporting documentation | select field | — | — | — | — | — | — |
| Customer notification | select field | — | — | — | — | — | — |
| Finance notification | select field | — | — | — | — | — | — |
| Reconciliation behavior | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Wallet transaction history** (data table, from `listWalletTransactions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Wallet | the name it points at, never the id | The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance … |
| Wallet hold | the name it points at, never the id | The hold a spend settled, where it came through `holdWalletFunds`. |
| Kind | chip: Top up, Spend, Refund, Adjustment, Bonus, Expiry… | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Balance after | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Order | text | — |
| Venue | the name it points at, never the id | — |
| Reason | text | — |
| Principal | the name it points at, never the id | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Reverse**: A new reversing entry, never an edit. *(source: contracts/satellite/wallet.yaml#reverseWalletFunding)*

**Data it reads**: `listWalletTransactions` (onLoad, Wallet transaction history)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reversal transaction correction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reversal transaction correction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reversal transaction correction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already spent below the reversal amount |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reversal:
  transaction: WT-2026-889120
  type: duplicate debit
  amount: AED 8.00
```

#### Permissions

- `reverseWalletFunding` → `WALLET_OPERATE` (operate) · staff
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

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1148` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1148`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 10: Works in Reversal & Transaction Correction Management → Correct operational wallet transactions while maintaining an immutable ledger. Supported Operations Payment reversal Transfer reversal Refund reversal Duplicate debit correction Duplicate credit …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1148?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1149` Administrative Balance Adjustment Studio

**Allow authorized personnel to perform governed wallet balance adjustments. Adjustment Types Credit Customer compensation Service recovery Promotional correction Migration adjustment Balance correction Manual award Debit Incorrect credit recovery Duplicate credit recovery Administrative correction Fraud recovery where authorized**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/administrative-balance-adjustment-studio-bo-1149` |

**Known gaps.** **Administrative Balance Adjustment Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Governed balance adjustments (compensation, service recovery, corrections) with approval above thresholds.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only adjustWallet, setApprovalMatrix and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adjustment reason | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Wallet | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Financial classification | select field | — | — | — | — | — | — |
| Customer-visible description | select field | — | — | — | — | — | — |
| Supporting reference | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

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

**What requires approval here** (data table, from `listApprovalMatrices`)

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
| Multi-level approval (primary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Adjust**: Type and reason required; approval per the matrix. *(source: contracts/satellite/wallet.yaml#adjustWallet / contracts/spine/approvals.yaml#setApprovalMatrix)*

**Data it reads**: `getWallet` (onLoad, Read a guest wallet); `listApprovalMatrices` (onLoad, What requires approval here)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The administrative balance adjustment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the administrative balance adjustment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No administrative balance adjustment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
adjustment:
  type: Service recovery
  amount: +AED 50.00
  approval: Supervisor
```

#### Permissions

- `adjustWallet` → `WALLET_OPERATE` (operate) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff
- `getWallet` → `WALLET_VIEW` (read) · staff, guest
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

77 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.113 | Refund management | Ticketing Catalogue | CONTRACTED | `adjustWallet` |
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 65 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Funding methods: cash, card, online, POS, kiosk self-service, plus manual admin funding used to issue a goodwill/service-recovery credit to a guest's wallet. Chinmay raised role-based permission for staff funding wallets. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-516)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1149` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1149`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 12: Works in Administrative Balance Adjustment Studio → Allow authorized personnel to perform governed wallet balance adjustments. Adjustment Types Credit Customer compensation Service recovery Promotional correction Migration adjustment Balance …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1149?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Multi-level approval.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1150` Wallet Block, Freeze & Restriction Management

**Protect wallet accounts and individual balances without necessarily closing the wallet. Requirement 4.3.21 explicitly states that it must be possible to block a wallet account.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletId` (navigation), `subjectId` (navigation) · cold entry: Opened from BO-1143 with the wallet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/orders-money/wallet-block-freeze-restriction-management-bo-1150` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Block, freeze or restrict a wallet; three different things a single suspended flag conflated.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setWalletRestriction, suspendWallet and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediate | select field | — | — | — | — | — | — |
| Until date | select field | — | — | — | — | — | — |
| Until investigation completed | select field | — | — | — | — | — | — |
| Permanent | select field | — | — | — | — | — | — |
| Manual release | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |

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
| Block wallet (primary button) | navigation or local | — | — | — | — |
| Unblock wallet (secondary button) | navigation or local | — | — | — | — |
| Suspend wallet (destructive button) | navigation or local | — | — | — | — |
| Freeze entire balance (secondary button) | navigation or local | — | — | — | — |
| Freeze specific credit (secondary button) | navigation or local | — | — | — | — |
| Disable spending (destructive button) | navigation or local | — | — | — | — |
| Disable transfers (destructive button) | navigation or local | — | — | — | — |
| Disable top-up (destructive button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Restrict**: Kind (block, freeze, restrict), reason; the balance is preserved. *(source: contracts/satellite/wallet.yaml#setWalletRestriction)*

**Data it reads**: `getWallet` (onLoad, Read a guest wallet)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*; carries `subjectId`

**What opens over it**

- confirmDialog *Suspend wallet*: **Suspend wallet on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable spending*: **Disable spending on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable transfers*: **Disable transfers on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable top-up*: **Disable top-up on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet block freeze configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet block freeze untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet block freeze configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The wallet is closed, and a closed wallet cannot be suspended. (WalletStateProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
restriction:
  wallet: DW-0011-9012
  kind: freeze
  reason: Suspected card testing
```

#### Permissions

- `setWalletRestriction` → `WALLET_OPERATE` (operate) · staff
- `suspendWallet` → `WALLET_OPERATE` (operate) · staff
- `getWallet` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

28 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.21 | It shall be possible to block wallet account. | Bundles and Promotions | CONTRACTED | `suspendWallet` |
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

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1150` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1150`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 14: Works in Wallet Block, Freeze & Restriction Management → Protect wallet accounts and individual balances without necessarily closing the wallet. Requirement 4.3.21 explicitly states that it must be possible to block a wallet account.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1150?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Block wallet, Unblock wallet, Suspend wallet, Freeze entire balance, Freeze specific credit, Disable spending, Disable transfers, Disable top-up.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1151` Wallet Disputes & Operational Exception Queue

**Provide a controlled workflow for wallet transaction problems requiring investigation. Exception Types Customer disputes transaction Duplicate wallet debit Wallet charged but service failed Transfer recipient not received Refund missing Offline transaction conflict Balance mismatch Gift card issue Credential misuse Suspicious transfer Reconciliation mismatch Case Information**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `disputeId` (navigation) |
| Route | `/orders-money/wallet-disputes-operational-exception-queue-bo-1151` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet disputes and operational exceptions worked to resolution.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletDisputes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletDisputes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): The queue cannot resolve a dispute; resolveWalletDispute exists but is declared only on BO-1179. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Case ID | select field | — | — | — | — | — | — |
| Wallet | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Transaction | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Issue category | select field | — | — | — | — | — | — |
| Customer description | select field | — | — | — | — | — | — |
| Evidence | select field | — | — | — | — | — | — |
| Risk score | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Resolution SLA | select field | — | — | — | — | — | — |
| Assignment | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Notifications | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |

**Form: Resolve dispute** (modal, opened by *Resolve dispute*; *Resolve dispute* calls `resolveWalletDispute`, *Cancel* sends nothing)

**Collects what `resolveWalletDispute` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | segmented control | required | — | Reprocess · Escalate · Resolve | — | — | `resolveWalletDispute` body |
| Outcome `outcome` | segmented control | optional | — | Upheld · Rejected | — | Required with `resolve`. | `resolveWalletDispute` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | Required with `resolve`. | `resolveWalletDispute` body |
| Escalate to role `escalateToRoleId` | picker: choose an escalate to role | optional | — | — | shows names, sends the id | Required with `escalate`. | `resolveWalletDispute` body |
| Adjustment `adjustmentId` | picker: choose an adjustment | optional | — | — | shows names, sends the id | The `adjustWallet` adjustment that settled an upheld dispute, if any. | `resolveWalletDispute` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or `resolutionNote`, or `escalate` without `escalateToRoleId`.

**Sent by *Withdraw dispute*** (`withdrawWalletDispute`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 500 | — | — | `withdrawWalletDispute` body |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** No action, Refund, Reverse, Adjust balance, Block wallet, Replace credential, Escalate, Refer to finance/security, SLA. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Withdraw dispute (primary button) | `withdrawWalletDispute` POST `/wallet-disputes/{disputeId}/withdraw` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`). | — |
| Resolve dispute (secondary button) | `resolveWalletDispute` POST `/wallet-disputes/{disputeId}/resolve` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **queue**: Type, amount, age, state; withdraw available while open. *(source: contracts/satellite/wallet.yaml#listWalletDisputes / contracts/satellite/wallet.yaml#withdrawWalletDispute)*

**Data it reads**: `listWalletDisputes` (onLoad, The dispute queue)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet disputes operational configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet disputes operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet disputes operational configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or `resolutionNote`, or `escalate` without `escalateToRoleId`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
dispute:
  type: Charged but game failed
  amount: AED 6.00
  age: 1 day
```

#### Permissions

- `listWalletDisputes` → `WALLET_VIEW` (read) · staff
- `raiseWalletDispute` → `WALLET_OPERATE` (operate) · staff
- `withdrawWalletDispute` → `WALLET_OPERATE` (operate) · staff, guest
- `resolveWalletDispute` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1151` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1151`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 16: Works in Wallet Disputes & Operational Exception Queue → Provide a controlled workflow for wallet transaction problems requiring investigation. Exception Types Customer disputes transaction Duplicate wallet debit Wallet charged but service failed Transfer …

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1151?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Withdraw dispute, Resolve dispute.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1152` Operations Simulator, Approval & Audit Trail

**Provide administrators with a final controlled workspace for testing sensitive wallet operations and reviewing the immutable operational history. Simulation Example — Refund Configure TICVAI’s centralized wallet security and fraud-control layer, combining rule-based controls, transaction risk scoring, velocity monitoring, device and credential intelligence, AI anomaly detection, automated protective actions, fraud investigation, and security governance. This board directly covers requirements 4.3.30, 4.3.31 and 4.3.32, which require configurable wallet limits, suspicious- transaction controls, manual review, spending/transfer restrictions and AI identification of unusual top-ups, spending, account sharing, rapid transfers, duplicate transactions and unauthorized-access patterns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/operations-simulator-approval-audit-trail-bo-1152` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test sensitive wallet operations and review their history.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletDisputes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletDisputes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **history**: Disputes and operations timeline. *(source: contracts/satellite/wallet.yaml#listWalletDisputes)*

**Data it reads**: `listWalletDisputes` (onLoad, Operations audit trail)

**Where the user goes next**

- → `BO-1143` Wallet Operations Command Center: *Back to Wallet Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operations simulator approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operations simulator approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operations simulator approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operations simulator approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
history:
- at: 14 Nov 10:12
  event: dispute resolved, refund AED 6.00
```

#### Permissions

- `listWalletDisputes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1152` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1152`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 7
- Flow F299 *Wallet Configuration Backend Structure v1.0 board 7: Wallet Operations Command …*, step 18: Works in Operations Simulator, Approval & Audit Trail → Provide administrators with a final controlled workspace for testing sensitive wallet operations and reviewing the immutable operational history. Simulation Example — Refund

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1152?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1143`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustWallet": {"method":"POST","path":"/wallets/{subjectId}/adjust","contract":"wallet","summary":"Manually adjust a wallet balance","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getRefundPolicy": {"method":"GET","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Read a venue's refund policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundPolicy"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletDisputes": {"method":"GET","path":"/wallet-disputes","contract":"wallet","summary":"Contested transactions and operational exceptions","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"WalletDispute"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"raiseWalletDispute": {"method":"POST","path":"/wallet-disputes","contract":"wallet","summary":"A guest contests a wallet transaction","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletDispute","responds":"WalletDispute"},
"resolveWalletDispute": {"method":"POST","path":"/wallet-disputes/{disputeId}/resolve","contract":"wallet","summary":"Work a wallet dispute or integration exception","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletDispute"},
"reverseWalletFunding": {"method":"POST","path":"/wallet-funding/reversals","contract":"wallet","summary":"Undo a top-up, in full or in part","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletAdjustment"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setRefundPolicy": {"method":"PUT","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Set a venue's refund policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RefundPolicy","responds":"RefundPolicy"},
"setWalletRefundPolicy": {"method":"PUT","path":"/wallet-refund-policy","contract":"wallet","summary":"What a refund puts back, and where","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletRefundPolicy","responds":"WalletRefundPolicy"},
"setWalletRestriction": {"method":"POST","path":"/wallet-restrictions","contract":"wallet","summary":"Block, freeze or restrict a wallet","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletRestriction","responds":"WalletRestriction"},
"setWalletTransferRules": {"method":"PUT","path":"/wallet-transfer-rules","contract":"wallet","summary":"Whether guests may move money to each other, and on what terms","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletTransferRules","responds":"WalletTransferRules"},
"suspendWallet": {"method":"POST","path":"/wallets/{walletId}/suspend","contract":"wallet","summary":"Freeze a wallet","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"withdrawWalletDispute": {"method":"POST","path":"/wallet-disputes/{disputeId}/withdraw","contract":"wallet","summary":"Withdraw a wallet dispute that is still open or under review","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletDispute"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefundPolicy": {"x-ticvai-persistence":"orders.refund_policy + orders.refund_policy_time_band","type":"object","description":"Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n","required":["venueId","selfAuthoriseLimit","requiresApprovalAbove"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue in the path. Not taken from a `setRefundPolicy` body."},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"},"requiresSecondUserAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"},"requiresApprovalAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, an ORDER_REFUND_APPROVE holder must approve."},"timeBands":{"type":"array","description":"Refundable percentage by time before the performance. Evaluated most-specific first.\n","items":{"type":"object","required":["hoursBefore","percentage"],"properties":{"hoursBefore":{"type":"integer","minimum":0},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"allowPartial":{"type":"boolean","default":true},"refundWindowDays":{"type":"integer","nullable":true,"minimum":0,"description":"Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."},"varianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletAdjustment": {"type":"object","x-ticvai-persistence":"wallet.adjustment","description":"Board 7.7. **A correction, distinguishable from a spend.**","properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["reversal","chargeback","goodwill","correction","writeOff"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"affectedLotIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string"},"performedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"WalletDispute": {"type":"object","x-ticvai-persistence":"wallet.dispute","description":"Board 7.9. **Internal, and the venue decides it** — unlike a card chargeback.","required":["walletId","description"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"description":{"type":"string"},"raisedBy":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["open","investigating","escalated","upheld","rejected","withdrawn"],"description":"`escalated` added with `resolveWalletDispute` (VM close-out, 29 September). `upheld`, `rejected` and `withdrawn` are closed."},"resolution":{"type":"string","nullable":true},"escalatedToRoleId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"reprocessedTransactionIds":{"type":"array","readOnly":true,"description":"Transactions created by a `reprocess` action.","items":{"type":"string","format":"uuid"}},"resolvedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"adjustmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletRefundPolicy": {"type":"object","x-ticvai-persistence":"wallet.refund_policy","description":"Boards 7.4 and 7.5. **Restoration is to the lot, not to the balance.**","properties":{"defaultDestination":{"type":"string","enum":["originalTender","wallet","guestChoice"]},"walletRefundCreditTypeId":{"type":"string","format":"uuid"},"restoreToOriginalLots":{"type":"boolean","default":true},"restoreOriginalExpiry":{"type":"boolean","default":true,"description":"**Refunding into a new lot with a fresh expiry is a gift.** Sometimes intended, never by accident.\n"},"walletRefundBonusPercent":{"type":"number","nullable":true,"description":"An incentive to take the refund as credit rather than to a card."},"destinationsBySource":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**A destination per refund source** (contract gap CHG-WIR-027, BO-1146; CHG-CSA-045). A refund of a ticket, an event, F&B, retail, a rental, parking, a membership or a compensation goes to the destination listed for its source; a source not listed takes `defaultDestination`.","items":{"type":"object","properties":{"source":{"type":"string","enum":["ticket","event","fnb","retail","rental","parking","membership","compensation"]},"destination":{"type":"string","enum":["originalTender","wallet","guestChoice"]}}}},"scopePath":{"type":"string"}}},
"WalletRestriction": {"type":"object","x-ticvai-persistence":"wallet.restriction","description":"Board 7.8. **Freeze, block and restrict are three different things.**","required":["walletId","kind","reason"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["freeze","block","restrict","none"],"description":"**`freeze` stops spending and allows funding** — what you do while investigating. **`block` stops both** — a confirmed fraud. **`restrict` limits channels or categories** — what a parent asked for.\n"},"blockedChannels":{"type":"array","items":{"type":"string"}},"blockedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string"},"appliedBy":{"type":"string","format":"uuid"},"appliedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]},
"WalletTransferRules": {"type":"object","x-ticvai-persistence":"wallet.transfer_rules","description":"Boards 7.2 and 7.3. **A money-transmission question before it is a feature.**","properties":{"peerToPeerAllowed":{"type":"boolean","default":false},"transferableCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maximumPerTransfer":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumPerDay":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"approvalAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"bothPartiesIdentified":{"type":"boolean","default":true},"withinSharedWalletOnly":{"type":"boolean","default":false},"scopePath":{"type":"string"}}}
}
```
