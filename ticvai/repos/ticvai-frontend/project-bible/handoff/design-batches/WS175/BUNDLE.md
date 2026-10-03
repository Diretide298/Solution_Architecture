# WS175 — Seat Management Venue Mapping Reference v1.0 board 11

**10 screens · 9 operations · 23 schemas · 5 permissions**

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
  `CAPACITY_CONFIGURE, PRODUCT_VIEW, REPORT_EXPORT, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1051` | Seat Analytics Command Center | B–D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-1052` | Occupancy Reporting | B–D | 3 | 17 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1053` | Zone Performance Reporting | B–D | 3 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1054` | Revenue by Section | B–D | 3 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1055` | Revenue by Seat Category | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1056` | Seat Utilization Analytics | B–D | 2 | 19 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1057` | Hold Inventory Reporting | B–D | 0 | 12 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `BO-1058` | Sales Pace & Pick Curves | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-1059` | Heat Maps & Drill-Down | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-1060` | Report Builder, Export & Audit | B–D | 0 | 0 | 6 | 87 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1051, BO-1055, BO-1057, BO-1058, BO-1059, BO-1060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1051` Seat Analytics Command Center

**Provide a consolidated view of seat commercial and operational performance. Show occupancy, revenue, utilization, average ticket price, held inventory, release yield and forecast variance. Present trend, benchmark, target and prior-period comparison by tenant, venue and event. Surface low occupancy, excessive holds, inventory conflict, price variance and data-quality alerts. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/access-venue/seat-analytics-command-center-bo-1051` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A seat analytics read (occupancy, revenue, yield by section and performance); listSeats carries no sales.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat commercial and operational performance: occupancy, revenue, utilisation, average price, holds.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The only read lists seats of a map; it carries no sales or revenue. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPIs**: KPI cards (DI-041) and a section table. *(source: contracts/satellite/seating.yaml#listSeats / DI-041)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1052` Occupancy Reporting: *Occupancy Reporting*
- → `BO-1053` Zone Performance Reporting: *Zone Performance Reporting*
- → `BO-1054` Revenue by Section: *Revenue by Section*
- → `BO-1055` Revenue by Seat Category: *Revenue by Seat Category*
- → `BO-1056` Seat Utilization Analytics: *Seat Utilization Analytics*
- → `BO-1057` Hold Inventory Reporting: *Hold Inventory Reporting*
- → `BO-1058` Sales Pace & Pick Curves: *Sales Pace & Pick Curves*
- → `BO-1059` Heat Maps & Drill-Down: *Heat Maps & Drill-Down*
- → `BO-1060` Report Builder, Export & Audit: *Report Builder, Export & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  occupancy: 86%
  avgPrice: AED 312.00
```

#### Permissions

- `listSeats` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.4.7 | Seat Audit Trail | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |
| 21.4.8 | Seat History | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |
| 21.13.5 | Seat Audit Logs | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1051` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1051`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 1: Opens Seat Analytics Command Center → Provide a consolidated view of seat commercial and operational performance. Show occupancy, revenue, utilization, average ticket price, held inventory, release yield and forecast variance. Present …
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F284 branch at step 1 (expected): when Nothing has been set up on Seat Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F284 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1052`, `BO-1053`, `BO-1054`, `BO-1055`, `BO-1056`, `BO-1057`, `BO-1058`, `BO-1059`, `BO-1060`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1052` Occupancy Reporting

**Report sold and attended occupancy against configured capacity. Calculate sold, issued, scanned, no-show, blocked, available and effective capacity with clear metric definitions. Analyze by event, performance, venue, section, category, channel and time. Compare events and periods and drill to approved seat-level evidence. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/occupancy-reporting-bo-1052` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Sold and attended occupancy against capacity for an event or performance, with every capacity figure defined: capacity, blocked, sellable, sold, issued (including complimentary), scanned, no-show, available. Utilisation divides by sellable capacity and says how holds and blocked seats are treated.

**Known correction pending (do not draw the wrong version)**

- **The layout notes say the occupancy and no-show KPIs are "not seeded"; occupancy, capacity utilisation and no-show rate are already named metric sources, so they are KPI definitions to create, not contract gaps. No seat-level drill or section breakdown exists.** Why: Prevents a contract change request for something the KPI builder covers. *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource / screens/P08-venue-back-office.yaml#BO-1052; Finance, Ledger & Tax · Reporting & Analytics)*
- **Occupancy reporting inside the seating module duplicates the reporting area's capacity dashboard.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-015; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope | select field | — | — | — | — | Sends `?scopePath=` (venue, event). | — |
| Period | select field | — | — | — | — | Sends `?period=`. | — |
| Compare to | select field | — | — | — | — | Sends `?compareTo=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Sold occupancy** (metric tile, from `getKpiValues`): Needs a sold-occupancy KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Scanned occupancy** (metric tile, from `getKpiValues`): Needs a scanned-occupancy KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**No-shows** (metric tile, from `getKpiValues`): Needs a no-show KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Occupancy measures** (data table, from `getKpiValues`): Sold, issued, scanned, no-show, blocked, available and effective capacity, one KPI per row.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Status | chip: Green, Amber, Red, No target | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **measures**: Sold occupancy = sold over sellable; Scanned occupancy = scanned over sellable; No-show rate = issued not scanned over issued. Each figure's definition in an info popover; percentages 2 decimals. *(source: MATRIX 8.2.36 / MATRIX 1.1.40 / MATRIX 8.9.2 / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **status band**: Capacity utilisation amber from 80%, red from 95% unless the venue set its own target bands; 90–95% sits in amber. *(source: MATRIX 8.2.36 / MATRIX 1.1.40 / DI-704)*

**Data it reads**: `getKpiValues` (onLoad, Occupancy KPIs)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The occupancy reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the occupancy reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No occupancy reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the occupancy reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **event still on sale**: Scanned occupancy and no-shows show "After doors open" rather than 0%. *(source: designer default)*

#### Consistency with other screens

- Match `P16 ANL-015 Capacity & Utilization Monitor, ANL-014 Attendance & Footfall`: Same occupancy definition and colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Etihad Arena, Abu Dhabi · Arabian Nights Gala · 24 Sep 2026
figures: Capacity 18,000 · Blocked 420 · Sellable 17,580 · Sold 15,906 (90.48%, amber) · Issued 16,216 incl. 310
  complimentary · Scanned 14,872 (84.60%) · No-shows 1,344 (8.29%)
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1052` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1052`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 2: Works in Occupancy Reporting → Report sold and attended occupancy against configured capacity. Calculate sold, issued, scanned, no-show, blocked, available and effective capacity with clear metric definitions. Analyze by event …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1053` Zone Performance Reporting

**Compare capacity, demand and yield across venue zones. Show zone capacity, sold, occupancy, average price, revenue, utilization, holds and release conversion. Rank zones and compare target, forecast, prior period and venue benchmark. Drill from zone to section, row and seat while preserving the selected metric and filters. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 46**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/zone-performance-reporting-bo-1053` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Zones ranked by capacity, sold, occupancy, average price and revenue, compared with target, prior period and the venue benchmark, drilling from zone to section, row and seat while keeping the chosen measure and filters.

**Known correction pending (do not draw the wrong version)**

- **KPI values carry a scope path and no zone dimension; zones are reachable only if they are scope paths.** Why: The ranking cannot be read as declared. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiValue; Finance, Ledger & Tax · Reporting & Analytics)*
- **Zone reporting duplicates the reporting area.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-020; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope | select field | — | — | — | — | Sends `?scopePath=`; a zone is reachable only if zones are scope paths. | — |
| Period | select field | — | — | — | — | Sends `?period=`. | — |
| Compare to | select field | — | — | — | — | Sends `?compareTo=`; target, benchmark or prior period. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Zone occupancy** (metric tile, from `getKpiValues`): Needs a zone-occupancy KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Zone revenue** (metric tile, from `getKpiValues`): Needs a zone-revenue KPI code; `takings` is venue-wide.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Zone ranking** (data table, from `getKpiValues`): Ranked by value; one KPI at a time.

| Shows | Format | Notes |
|---|---|---|
| Scope path | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Direction | chip: Up, Down, Flat | — |
| Status | chip: Green, Amber, Red, No target | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **zone ranking**: One measure at a time, ranked high to low; zone totals must add up to the event total shown above. *(source: screens/P08-venue-back-office.yaml#BO-1053)*

**Data it reads**: `getKpiValues` (onLoad, By zone)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The zone performance reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the zone performance reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No zone performance reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the zone performance reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `P16 ANL-015, ANL-020 Multi-Site & Performance Comparison`: Same ranking component and comparison words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Platinum 1,188 of 1,200 (99.00%) · Gold 4,512 of 4,800 (94.00%) · Silver 6,336 of 7,200 (88.00%) · Upper 3,870
  of 4,380 (88.36%) · total 15,906 of 17,580
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1053` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1053`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 4: Works in Zone Performance Reporting → Compare capacity, demand and yield across venue zones. Show zone capacity, sold, occupancy, average price, revenue, utilization, holds and release conversion. Rank zones and compare target, forecast …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1054` Revenue by Section

**Analyze financial contribution from each seating section. Report gross/net revenue, tax, fees, discounts, refunds, average ticket price and percentage of performance total. Compare section revenue, yield, occupancy, price band and prior-year/forecast variance. Link summarized values to governed finance/order detail and reconciliation status. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/revenue-by-section-bo-1054` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Each seating section's financial contribution: gross sales, discounts, refunds, net revenue, VAT, fees, average ticket price and share of the performance total, linked to order detail and reconciliation status. Gross and net are never the same column.

**Known correction pending (do not draw the wrong version)**

- **Section revenue duplicates the reporting area's sales and revenue views.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-002; Finance, Ledger & Tax · Reporting & Analytics)*

**Fixed on main** (the package already carries these; draw what it says): The "Net revenue" tile is bound to the seeded takings KPI. (CHG-FIN-007).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance scope | select field | — | — | — | — | Sends `?scopePath=`. | — |
| Period | select field | — | — | — | — | Sends `?period=`. | — |
| Compare to | select field | — | — | — | — | Sends `?compareTo=`; samePeriodLastYear gives the pack's prior-year variance. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Net revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=netRevenue` (CHG-FIN-007). Never the `takings` KPI (CHG-FIN-002, CHG-FIN-010).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Average ticket price** (metric tile, from `getKpiValues`): Needs an average-ticket-price KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Net revenue by section** (data table, from `getKpiValues`): KpiValue has no section dimension; the section columns are pack labels. (CHG-FIN-002: never a bare "Revenue")

| Shows | Format | Notes |
|---|---|---|
| Scope path | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Status | chip: Green, Amber, Red, No target | — |
| Section | text | not in the schema: `Section` |
| Gross sales | text | not in the schema: `Gross sales` |
| Tax | text | not in the schema: `Tax` |
| Fees | text | not in the schema: `Fees` |
| Discounts | text | not in the schema: `Discounts` |
| Refunds | text | not in the schema: `Refunds` |
| % of performance total | text | not in the schema: `% of performance total` |
| Reconciliation status | text | not in the schema: `Reconciliation status` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **section table**: Section, sold, Gross sales, Discounts, Refunds, Net revenue, VAT, Fees, Average ticket price (excludes complimentary tickets), % of performance total (adds to 100.00%). Totals row equals the performance's figures. *(source: MATRIX 6.1.66 / MATRIX 8.7.21 / MATRIX 8.1.3 / screens/P08-venue-back-office.yaml#BO-1054)*

**Data it reads**: `getKpiValues` (onLoad, Revenue by section)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue section list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue section untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue section yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue section are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
performance: Etihad Arena · Arabian Nights Gala · 24 Sep 2026 · gross sales excl. VAT
sections:
- Platinum · 1,188 · AED 1,722,600.00 · ATP 1,450.00 · 19.87%
- Gold · 4,512 · AED 3,384,000.00 · ATP 750.00 · 39.03%
- Silver · 6,336 · AED 2,692,800.00 · ATP 425.00 · 31.06%
- Upper · 3,870 · AED 870,750.00 · ATP 225.00 · 10.04%
- Total · 15,906 · AED 8,670,150.00 · 100.00%
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1054` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1054`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 6: Works in Revenue by Section → Analyze financial contribution from each seating section. Report gross/net revenue, tax, fees, discounts, refunds, average ticket price and percentage of performance total. Compare section revenue …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1055` Revenue by Seat Category

**Measure performance of Premium, Standard, Value, Accessible and configured categories. Show revenue mix, seats sold, average price, discount, refund, yield and sell-through by category. Compare venue, event, performance, channel, customer segment and days to event. Preserve accessible-category privacy and prevent misleading comparison caused by protected inventory rules. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/revenue-by-seat-category-bo-1055` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Revenue by seat category: mix, seats sold, average price, discount, refunds, sell-through.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSeatCategories return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#listSeatCategories; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **category table**: Categories as rows with revenue mix. *(source: contracts/satellite/seating.yaml#listSeatCategories)*

**Data it reads**: `listSeatCategories` (onLoad, List seat categories)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue seat category list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue seat category untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue seat category yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue seat category are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  category: Gold
  revenue: AED 412,000.00
  sellThrough: 91%
```

#### Permissions

- `listSeatCategories` → `PRODUCT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1055` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1055`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 8: Works in Revenue by Seat Category → Measure performance of Premium, Standard, Value, Accessible and configured categories. Show revenue mix, seats sold, average price, discount, refund, yield and sell-through by category. Compare …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1055?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1056` Seat Utilization Analytics

**Measure how effectively physical and sellable seating capacity is used. Calculate booked, sold, scanned, occupied estimate, idle and unavailable hours or performances as applicable. Analyze utilization by venue, map, section, seat type, day, time and event category. Identify permanently underused areas, recurring blocks, maintenance patterns and lost-sale opportunities. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/seat-utilization-analytics-bo-1056` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** How well seats are used across performances: booked, sold, scanned, idle and unavailable seat-performances by section, seat type, day and time, pointing at permanently underused areas and recurring blocks.

**Known correction pending (do not draw the wrong version)**

- **Utilisation by section, seat type or time cannot be read; KPI values have no such dimension.** Why: The heatmap cannot bind. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiValue; Finance, Ledger & Tax · Reporting & Analytics)*
- **Seat utilisation duplicates the reporting area's capacity dashboard.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-015; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope | select field | — | — | — | — | Sends `?scopePath=`. | — |
| Period | select field | — | — | — | — | Sends `?period=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Seat utilization** (metric tile, from `getKpiValues`): Needs a seat-utilization KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Idle seat-performances** (metric tile, from `getKpiValues`): Needs an idle KPI code; not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |

**Utilization measures** (data table, from `getKpiValues`): Booked, sold, scanned, occupied estimate, idle and unavailable.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Scope path | text | — |
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Status | chip: Green, Amber, Red, No target | — |
| Stale | yes / no (icon or chip) | True when the pipeline behind it has not refreshed. A number nobody flagged as stale is a number somebody will act on. |

**Underused areas** (chart): Permanently underused areas, recurring blocks and maintenance patterns; KpiValue has no section, seat-type or time-of-day dimension.

| Shows | Format | Notes |
|---|---|---|
| Section | text | not in the schema: `Section` |
| Seat type | text | not in the schema: `Seat type` |
| Day | text | not in the schema: `Day` |
| Time | text | not in the schema: `Time` |
| Utilization | text | not in the schema: `Utilization` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **underused areas**: A heatmap of section by day of week, coloured by utilisation; a block repeated on 3 or more performances is called out. *(source: MATRIX 6.1.69 / screens/P08-venue-back-office.yaml#BO-1056)*

**Data it reads**: `getKpiValues` (onLoad, Seat utilisation)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat utilization analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat utilization analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat utilization analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat utilization analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Upper tier, Section 412 · 18 performances · utilisation 61.20% · idle seat-performances 2,140 · blocked for camera
  position on 12 of 18
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1056` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1056`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 10: Works in Seat Utilization Analytics → Measure how effectively physical and sellable seating capacity is used. Calculate booked, sold, scanned, occupied estimate, idle and unavailable hours or performances as applicable. Analyze …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1056?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1057` Hold Inventory Reporting

**Report the size, age and outcome of seat holds. Show held quantity/value, capacity percentage, active age, upcoming release, conversion and expired unused. Compare VIP, Sponsor, Artist, Media, Corporate, Internal and custom types by owner/stakeholder. Measure released-to-sold outcomes and potential revenue suppressed by late or unused holds. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/hold-inventory-reporting-bo-1057` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-025): listInventoryHolds lists terminal and basket leases, not stakeholder seat holds; VIP, sponsor and media holds are seating's pools (listSeatHoldPools) …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat holds by size, age and outcome (VIP, sponsor, artist, media, corporate, internal): held quantity and value, upcoming releases, converted and expired unused.

**Fixed on main** (the package already carries these; draw what it says): listInventoryHolds lists terminal and basket leases, not stakeholder seat holds. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Hold pools** (data table, from `listSeatHoldPools`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Hold type | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Seats | list or chips (count when long) | — |
| Seat count | 1,234 | — |
| Used count | 1,234 | — |
| Released count | 1,234 | — |
| Holder name | text | — |
| Reason | text | — |
| Release at | 1 Oct 2026, 14:30 | — |
| Status | chip: Active, Partially released, Released, Expired | — |
| Created by | the name it points at, never the id | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **holds report**: Grouped by hold type and owner with age and value. *(source: contracts/spine/catalogue.yaml#listInventoryHolds)*

**Data it reads**: `listSeatHoldPools` (onLoad, Held seats by pool and stakeholder, with what is left and …)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold inventory reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold inventory reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold inventory reporting yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold inventory reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holds:
- type: Sponsor
  owner: Emirates Bank
  seats: 40
  value: AED 18,000.00
  age: 12 days
```

#### Permissions

- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1057` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1057`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 12: Works in Hold Inventory Reporting → Report the size, age and outcome of seat holds. Show held quantity/value, capacity percentage, active age, upcoming release, conversion and expired unused. Compare VIP, Sponsor, Artist, Media …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1058` Sales Pace & Pick Curves

**Analyze when seats sell and which inventory customers select first. Plot cumulative sales by days/hours to event against target, forecast and comparable events. Configuration Scope of Work / Version 1.0 47 Show seat-pick sequence by section, row, price, view and channel and identify preferred inventory patterns. Support cohort comparison and expose sufficient sample and confidence information for decisions. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/sales-pace-pick-curves-bo-1058` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When seats sell and which seats sell first: cumulative sales against target and comparable events, and the pick order by section and price.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **pick curve**: Cumulative curve by days to event with the target line. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve)*

**Data it reads**: `listDemandBookingCurve` (onLoad, Sales pace and pick curve)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales pace pick list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales pace pick untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales pace pick yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sales pace pick are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
curve:
  event: Desert Symphony
  daysOut: 30
  sold: 54%
  target: 50%
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1058` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1058`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 14: Works in Sales Pace & Pick Curves → Analyze when seats sell and which inventory customers select first. Plot cumulative sales by days/hours to event against target, forecast and comparable events. Configuration Scope of Work / Version …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1059` Heat Maps & Drill-Down

**Visualize spatial performance directly on the approved seat map. Display occupancy, revenue, average price, demand, availability, holds, scan and utilization heat maps. Switch level, section, row and seat granularity and synchronize filters with tables and charts. Open the supporting transactions where authorized and show metric definition, source and refresh time. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation) |
| Route | `/access-venue/heat-maps-drill-down-bo-1059` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Performance drawn on the seat map: occupancy, revenue, price, demand, holds and scans as heat maps.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `getSeatInventory` ?performanceId |
| Section | picker: choose a section | — | — | `getSeatInventory` ?sectionId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **heat map**: Metric picker, colour scale with legend, drill from level to seat. *(source: contracts/satellite/seating.yaml#getSeatInventory / contracts/satellite/reporting.yaml#runReport)*

**Data it reads**: `getSeatInventory` (onLoad, The map behind the heat)

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The heat maps drill-down list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the heat maps drill-down untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No heat maps drill-down yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the heat maps drill-down are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
heat:
  metric: occupancy
  performance: Desert Symphony 22 Nov
```

#### Permissions

- `getSeatInventory` → `CAPACITY_CONFIGURE` (configure) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.28 | Visual Seat Categorization Automatically color-code seat categories. Generate interactive seat maps. Highlight restricted-view or obstructed seats. Visualize occupancy and sales patterns. | Ticketing Catalogue | CONTRACTED | `getSeatInventory` |
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1059` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1059`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 16: Works in Heat Maps & Drill-Down → Visualize spatial performance directly on the approved seat map. Display occupancy, revenue, average price, demand, availability, holds, scan and utilization heat maps. Switch level, section, row and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1059?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1060` Report Builder, Export & Audit

**Allow authorized users to assemble and distribute controlled seat reports. Select approved dimensions, measures, filters, grouping, sorting, chart/map and date context. Save personal/team views and schedule email or in-app delivery with recipient and permission validation. Export CSV, XLSX or PDF subject to policy and log report definition, recipients, downloads and sensitive access. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 48 Board 12 - Multi-Tenant & Venue Configuration Figure 12. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 49**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_EXPORT`, `REPORT_MANAGE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `executionId` (navigation) |
| Route | `/access-venue/report-builder-export-audit-bo-1060` |

**Known gaps.** **Report Builder, Export & Audit declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Building and distributing seat reports: approved dimensions and measures, filters, grouping, chart or map, saved views, scheduled delivery and exports, with every definition, recipient and download logged. Definitions use versioned metrics, so "occupancy" means the same everywhere.

**Known correction pending (do not draw the wrong version)**

- **BO-1060 duplicates the reporting area's builder, export centre and audit trail.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-032; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen arrives with an execution id but its only write creates a definition.** Why: Entry parameter does not match the act. *(source: screens/P08-venue-back-office.yaml#BO-1060; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **dimensions and measures**: Only from the approved seating dataset; seat-level and guest-level fields are offered only to users allowed to see them. *(source: MATRIX 6.1.13 / screens/P08-venue-back-office.yaml#BO-1060)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create report (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **audit**: Who built, changed, ran, scheduled and downloaded each report, with the scope applied. *(source: MATRIX 6.1.15 / contracts/satellite/reporting.yaml#listReportExecutions)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Export**: CSV, Excel or PDF; large ones run in the background and notify when ready; links expire. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportExport)*

**Where the user goes next**

- → `BO-1051` Seat Analytics Command Center: *Back to Seat Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report export audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report export audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report export audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report export audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Consistency with other screens

- Match `P16 ANL-032 Report Creation Wizard, ANL-045 Export & Download Center, ANL-049 Report Audit Trail`: Same builder; seat reports are definitions over the seating source.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Seat sales by section and price band · Etihad Arena · Arabian Nights Gala 24 Sep · saved by Rahul Menon · shared
  with Box Office team
```

#### Permissions

- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `exportReportResult` → `REPORT_EXPORT` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

87 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| 3.7.11 | System shall provide reporting on upsell impressions, conversion rates, revenue generated, average order value uplift, and campaign effectiveness across channels. | Admission and Access | CONTRACTED | `createReport` |
| 5.6.28 | Provide reporting on wait times, abandonment rates, no-shows, throughput, utilization, and satisfaction. | F&B & Guest Management | CONTRACTED | `createReport` |
| 6.1.5 | The system should be able to Generate reports with admission types/information. | Retail POS | CONTRACTED | `createReport` |
| 6.1.8 | The system should have the ability to retrieve information "on the fly" for items, (e.g., keyword, item #, description, category etc.) in user-friendly format such as pull-down menus and/or auto fill … | Retail POS | CONTRACTED | `createReport` |
| 6.1.9 | The system should be able to report historical sales look up by item, ticket number etc.. | Retail POS | CONTRACTED | `createReport` |
| … 75 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1060` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1060`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 11
- Flow F284 *Seat Management Venue Mapping Reference v1.0 board 11: Seat Analytics Command …*, step 18: Works in Report Builder, Export & Audit → Allow authorized users to assemble and distribute controlled seat reports. Select approved dimensions, measures, filters, grouping, sorting, chart/map and date context. Save personal/team views and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create report, Cancel.
- [ ] Every transition is wired: `BO-1051`.
- [ ] Every gated control is gated: `REPORT_EXPORT`, `REPORT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"exportReportResult": {"method":"POST","path":"/report-executions/{executionId}/export","contract":"reporting","summary":"Export a completed result","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getSeatInventory": {"method":"GET","path":"/seat-inventory","contract":"seating","summary":"Every seat's state for a performance, in one read","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":true},{"name":"sectionId","in":"query","required":null}],"requestBody":null,"responds":"SeatInventory"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeatCategories": {"method":"GET","path":"/seat-categories","contract":"seating","summary":"List seat categories","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"SeatCategory"},
"listSeatHoldPools": {"method":"GET","path":"/seat-hold-pools","contract":"seating","summary":"Held seats, by pool, with what is left and when it releases","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null}],"requestBody":null,"responds":"SeatHoldPool"},
"listSeats": {"method":"GET","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"List seats in a map","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"rowLabel","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"attribute","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true},"role":{"type":"string","nullable":true,"enum":["dimension","measure"],"description":"**What the column is to a chart** (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue, count of admissions). Null on a column only a table shows."},"encoding":{"type":"string","nullable":true,"enum":["category","x","y","series","value","size","colour","location","stage","source","target","row","column","hierarchyLevel","label","tooltip"],"description":"**Which field well the column fills** (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. The per-mark rule is on that field."},"axis":{"type":"string","nullable":true,"enum":["primary","secondary"],"description":"For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007)."},"seriesType":{"type":"string","nullable":true,"enum":["bar","line","area"],"description":"For a measure on a `combo`, how that series is drawn (CHG-FIN-007)."},"hierarchyLevel":{"type":"integer","nullable":true,"minimum":1,"description":"For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. Levels must follow a real hierarchy (DI-709), for example year, month, day, or region, venue, outlet (CHG-FIN-007)."},"unitLabel":{"type":"string","nullable":true,"maxLength":40,"description":"The unit an axis states, for example \"AED\" or \"Admissions\". Required on a secondary axis (CHG-FIN-007)."}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"Seat": {"x-ticvai-persistence":"seating.seat","type":"object","required":["id","sectionCode","rowLabel","seatNumber","attribute"],"properties":{"id":{"type":"string","format":"uuid","description":"**Stable for the life of the seat.** Section, row and number are display labels that change on a refit; this does not. A ticket sold today must still resolve after a renumbering.\n"},"sectionCode":{"type":"string"},"rowLabel":{"type":"string"},"seatNumber":{"type":"string"},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"companionSeatIds":{"type":"array","items":{"type":"string"},"description":"Present on accessible seats. Sold together, released together."},"isActive":{"type":"boolean"}}},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatCategory": {"x-ticvai-persistence":"seating.seat_category","type":"object","required":["id","code","name","venueId","rank"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"displayColour":{"type":"string","nullable":true},"rank":{"type":"integer","description":"Ordering for best-seat assignment. Lower is better."},"seatCount":{"type":"integer"},"priceBands":{"type":"array","description":"What a seat in this category costs, by band (decided 28 September, audit R275 (d), from the BO-1045 pack). Written by `createSeatCategory` and `updateSeatCategory`. A band may be narrowed to a sales channel or a customer segment and to a window; where several match a sale, the narrowest wins.\n","items":{"$ref":"#/components/schemas/SeatPriceBand"}}}},
"SeatHoldPool": {"type":"object","x-ticvai-persistence":"seating.hold_pool","description":"Board 6.3. **Utilisation decides next season's allocation.**","required":["holdTypeId","performanceId"],"properties":{"id":{"type":"string","format":"uuid"},"holdTypeId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"seatCount":{"type":"integer","readOnly":true},"usedCount":{"type":"integer","readOnly":true},"releasedCount":{"type":"integer","readOnly":true},"holderName":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"releaseAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","partiallyReleased","released","expired"]},"createdBy":{"type":"string","format":"uuid"},"scopePath":{"type":"string"}}},
"SeatInventory": {"type":"object","description":"Board 4. **One read, because a real-time map assembling four endpoints renders one state late.**\n","properties":{"performanceId":{"type":"string","format":"uuid"},"asOf":{"type":"string","format":"date-time"},"totals":{"type":"object","properties":{"capacity":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"reserved":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"outOfService":{"type":"integer"}}},"seats":{"type":"array","items":{"type":"object","properties":{"seatId":{"type":"string","format":"uuid"},"label":{"type":"string"},"state":{"type":"string","enum":["available","held","reserved","sold","blocked","outOfService","killed"]},"holdPoolId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"SeatPriceBand": {"x-ticvai-persistence":"seating.seat_price_band","type":"object","description":"One price band on a seat category (decided 28 September, audit R275 (d)). The currency is `amount.currency`, resolved from the region like every `Money` (ADR-0018), so the band carries no currency of its own.\n","required":["code","displayLabel","amount","effectiveFrom"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"seatCategoryId":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64,"description":"Unique within the category."},"displayLabel":{"type":"string","maxLength":200},"displayColour":{"type":"string","nullable":true,"pattern":"^#[0-9A-Fa-f]{6}$"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"nullable":true,"description":"Null means every channel.","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}]},"customerSegmentId":{"type":"string","format":"uuid","nullable":true,"description":"A `marketing-crm` customer segment; null means everyone."},"effectiveFrom":{"type":"string","format":"date-time"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"description":"Null means open-ended."}}}
}
```
