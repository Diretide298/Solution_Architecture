# WS153 — Payment Payment Orchestration board 7

**9 screens · 12 operations · 13 schemas · 6 permissions**

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
  `LEDGER_POST, LEDGER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, SETTLEMENT_RECONCILE, SETTLEMENT_VIEW`. A control nobody can use must say so,
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
| `ADM-620` | Reconciliation Source & Import Manager | C | 0 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-621` | Transaction Matching & Reconciliation Engine | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-622` | Reconciliation Exception & Investigation Center | C | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-623` | Settlement & Payout Manager | C | 0 | 32 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-624` | Fees, Commission, FX & Settlement Economics | C | 0 | 10 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `ADM-625` | Merchant Account & Settlement Calendar Manager | C | 2 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-626` | Settlement Posting, Finance Handoff & Close Manager | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-627` | Reconciliation Audit, Trace & Evidence Center | C | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-628` | Reconciliation Simulator, Forecast & AI Operations Advisor | C | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-620, ADM-621, ADM-622, ADM-623, ADM-626, ADM-628 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-620` Reconciliation Source & Import Manager

**Manage all sources used to compare TICVAI payment records with external financial processing records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-620 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`, `SETTLEMENT_RECONCILE` (1 configure, 1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/reconciliation-source-import-manager-t141-adm-620` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Scheduled report imports. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **Reconciliation Source & Import Manager\t141 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Settlement and statement feeds and their import.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Reconciliation Source & Import Manager\t141".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-620; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: Scheduled report imports.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-620; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setReconciliationSource, ingestSettlementFile and nothing that returns the current … (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Sources** (data table, from `listReconciliationSources`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Connection | the name it points at, never the id | — |
| Transport | chip: Sftp, API, Email, Manual upload | — |
| Format | chip: Csv, Fixed width, Json, Xml, Camt053 | — |
| Expected schedule | text | How often a file is expected. Daily by default, one per venue per trading day (decided 28 September, audit R110 (b)), because settlement is … |
| Expected by time | text | — |
| Alert if missing | yes / no (icon or chip) | — |
| Field mapping | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scheduled report imports (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Ingest file**: Step one of five (ingest, parse, match, classify, auto-resolve). *(source: contracts/spine/finance.yaml#ingestSettlementFile / contracts/satellite/payments.yaml#setReconciliationSource)*

**Data it reads**: `listReconciliationSources` (onLoad, The files and feeds reconciliation is run against)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation source import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation source import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation source import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconciliation source import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
feed:
  provider: Network International
  format: CSV daily
  last: 2026-11-14 06:00
```

#### Permissions

- `setReconciliationSource` → `PAYMENT_CONFIGURE` (configure) · staff
- `ingestSettlementFile` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listReconciliationSources` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-620` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-620`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 2: Works in Reconciliation Source & Import Manager\t141 → Manage all sources used to compare TICVAI payment records with external financial processing records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-620?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scheduled report imports, Cancel.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`, `SETTLEMENT_RECONCILE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-621` Transaction Matching & Reconciliation Engine

**Automatically match TICVAI payment transactions against provider/acquirer records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-621 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/transaction-matching-reconciliation-engine-t142-adm-621` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of reconciliation matching rules (setReconciliationMatchingRules has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How a platform transaction is matched to a settled one: net of fees, rounding, batching.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Transaction Matching & Reconciliation Engine\t142".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-621; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setReconciliationMatchingRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **matching rules**: Keys and tolerances. *(source: contracts/satellite/payments.yaml#setReconciliationMatchingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Exact Match — 100%** (metric tile)

**High Confidence — 97%** (metric tile)

**Potential Match — 82%** (metric tile)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transaction matching reconciliation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transaction matching reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No transaction matching reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the transaction matching reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  key: provider reference
  tolerance: AED 0.05
```

#### Permissions

- `setReconciliationMatchingRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-621` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-621`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 4: Works in Transaction Matching & Reconciliation Engine\t142 → Automatically match TICVAI payment transactions against provider/acquirer records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-621?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-622` Reconciliation Exception & Investigation Center

**Centralize all payment discrepancies requiring operational or financial investigation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-622 |
| Who uses it | venue staff holding `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `settlementId` (navigation) |
| Route | `/commercial/reconciliation-exception-investigation-center-t143-adm-622` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The queue of reconciliation exceptions that the automatic steps could not explain: each with what TICVAI recorded, what the provider reported, the difference and the likely cause, and a resolution that is recorded with who, when and why. Nothing is ever edited; resolving explains, it does not change the payment.

**Known correction pending (do not draw the wrong version)**

- **The exception list is read per settlement (the path needs a settlement), so a centralised queue across settlements and providers has no read; the screen also loads it on action, not on arrival.** Why: The screen's purpose is the cross-settlement queue. *(source: contracts/spine/finance.yaml#listSettlementExceptions / screens/P08-venue-back-office.yaml#ADM-622; Finance, Ledger & Tax · Reporting & Analytics)*
- **The pack's columns (order, merchant account, related refund or reversal, match result) are not on the exception record, which carries a payment reference only.** Why: Columns cannot bind. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementException; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **resolution**: One of Matched manually (requires choosing the payment), Write-off, Dispute raised, Provider error, Timing difference; a note is always required. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementResolution / contracts/spine/finance.yaml#resolveSettlementException)*
- **filters**: Exception kind, provider, venue, age, amount band; oldest and largest first by default. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementException)*

#### Outputs: what the screen shows and produces

**Shown**

**Every reconciliation exception investigation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Payment | text | not in the schema: `Payment` |
| Order | text | not in the schema: `Order` |
| Provider transaction | text | not in the schema: `Provider transaction` |
| Provider | text | not in the schema: `Provider` |
| Merchant account | text | not in the schema: `Merchant account` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Date | text | not in the schema: `Date` |
| Settlement | text | not in the schema: `Settlement` |
| Related refund/reversal | text | not in the schema: `Related refund/reversal` |
| Match result | text | not in the schema: `Match result` |

**The selected reconciliation exception investigation** (detail panel): The pack groups this record's detail under its own headings: “Exception Types”, “Detected”.

| Shows | Format | Notes |
|---|---|---|
| Payment | text | not in the schema: `Payment` |
| Order | text | not in the schema: `Order` |
| Provider transaction | text | not in the schema: `Provider transaction` |
| Provider | text | not in the schema: `Provider` |
| Merchant account | text | not in the schema: `Merchant account` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Date | text | not in the schema: `Date` |
| Settlement | text | not in the schema: `Settlement` |
| Related refund/reversal | text | not in the schema: `Related refund/reversal` |
| Match result | text | not in the schema: `Match result` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **exception row**: Kind in words (Not in provider file, Not in our records, Amount differs, Duplicate in provider file, Unexplained fee), provider reference, our payment, amount, expected amount, difference with Over or Short, age in days. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementException)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Resolve**: Records the resolution; the row leaves the open list and shows in the settlement's history with the resolver's name. *(source: contracts/spine/finance.yaml#resolveSettlementException)*

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation exception investigation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation exception investigation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation exception investigation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconciliation exception investigation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 409 The exception is already resolved. |

#### Edge cases to draw

- **two people resolve the same exception**: The second sees "Already resolved by Omar Haddad at 10:41" and nothing is overwritten. *(source: contracts/spine/finance.yaml#resolveSettlementException)*
- **an unresolved exception at month end**: It blocks the period close ("Settlements reconciled"). *(source: F13 step 1 / contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult)*

#### Consistency with other screens

- Match `BO-043 Daily Reconciliation and BO-025 Chargebacks & Disputes`: Same five resolution words and the same exception kind wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Amount differs · NI ref 4471-0930-88213 · payment POS-0441871 · AED 1,200.00 vs AED 1,250.00 · Short AED 50.00
  · likely partial refund · 1 day
- Not in provider file · Stripe · order WEB-0098340, Fatima Al Mansoori · AED 385.00 · 2 days
```

#### Permissions

- `listSettlementExceptions` → `SETTLEMENT_VIEW` (read) · staff, partner
- `resolveSettlementException` → `SETTLEMENT_RECONCILE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-622` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-622`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 6: Works in Reconciliation Exception & Investigation Center\t143 → Centralize all payment discrepancies requiring operational or financial investigation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-622?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-623` Settlement & Payout Manager

**Track expected and actual settlements from payment providers/acquirers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-623 |
| Who uses it | venue staff holding `SETTLEMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/settlement-payout-manager-t144-adm-623` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home. **Reconciliation is daily, per venue** (decided 2 October 2026, Chinmay; CHG-FIN-009; audit R110 (b)). The unit of work and of sign-off is one venue-day: POS cash, gateway settlements, bank and wallet against the ledger for that day. A longer range reviews days already reconciled; a provider's monthly file (DI-268) is matched day by day.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Settlement & Payout Manager\t144 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Expected against actual settlement per provider, merchant account and day: gross sales, minus refunds, chargebacks, fees, adjustments and any reserve held back, gives net expected; net received is what reached the bank. The gap between them, and how long it has been open, is what this screen is for.

**Known correction pending (do not draw the wrong version)**

- **Of the 16 pack columns, acquirer, merchant account, legal entity, refunds, chargebacks, adjustments, reserve, net expected, net received and settlement date have no field on the settlement record (it carries provider gross, fees, net and ledger gross).** Why: The payout bridge cannot be drawn from the contract. *(source: contracts/spine/finance.yaml#/components/schemas/Settlement; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Provider name | text field | — | — | `listSettlements` ?providerName |
| Status | select | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | `listSettlements` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every settlement payout \t144** (data table)

| Shows | Format | Notes |
|---|---|---|
| Settlement ID | text | not in the schema: `Settlement ID` |
| Provider | text | not in the schema: `Provider` |
| Acquirer | text | not in the schema: `Acquirer` |
| Merchant account | text | not in the schema: `Merchant Account` |
| Legal entity | text | not in the schema: `Legal Entity` |
| Settlement period | text | not in the schema: `Settlement Period` |
| Gross sales | text | not in the schema: `Gross Sales` |
| Refunds | text | not in the schema: `Refunds` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| Fees | text | not in the schema: `Fees` |
| Adjustments | text | not in the schema: `Adjustments` |
| Reserve/holdback | text | not in the schema: `Reserve/Holdback` |
| Net expected | text | not in the schema: `Net Expected` |
| Net received | text | not in the schema: `Net Received` |
| Currency | text | not in the schema: `Currency` |
| Settlement date | text | not in the schema: `Settlement Date` |

**The selected settlement payout \t144** (detail panel): The pack groups this record's detail under its own headings: “Refunds”, “Provider Fees”, “Chargebacks”, “Settlement States”.

| Shows | Format | Notes |
|---|---|---|
| Settlement ID | text | not in the schema: `Settlement ID` |
| Provider | text | not in the schema: `Provider` |
| Acquirer | text | not in the schema: `Acquirer` |
| Merchant account | text | not in the schema: `Merchant Account` |
| Legal entity | text | not in the schema: `Legal Entity` |
| Settlement period | text | not in the schema: `Settlement Period` |
| Gross sales | text | not in the schema: `Gross Sales` |
| Refunds | text | not in the schema: `Refunds` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| Fees | text | not in the schema: `Fees` |
| Adjustments | text | not in the schema: `Adjustments` |
| Reserve/holdback | text | not in the schema: `Reserve/Holdback` |
| Net expected | text | not in the schema: `Net Expected` |
| Net received | text | not in the schema: `Net Received` |
| Currency | text | not in the schema: `Currency` |
| Settlement date | text | not in the schema: `Settlement Date` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **settlement row**: Provider, merchant account, legal entity, settlement day, then the bridge Gross sales, Refunds, Chargebacks, Fees, Adjustments, Reserve, Net expected, Net received, and the variance as Over or Short. Currency on every amount. *(source: screens/P08-venue-back-office.yaml#ADM-623)*
- **ordering**: Unsettled and short first, then by age. *(source: designer default)*

**Data it reads**: `listSettlements` (onLoad, Settlement and payout)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The settlement payout \t144 list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the settlement payout \t144 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No settlement payout \t144 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the settlement payout \t144 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **settlement arrives in two payments**: Shown as Partially received with both receipts listed. *(source: screens/P09-platform-admin-console.yaml#ADM-619)*

#### Consistency with other screens

- Match `ADM-619`: Same tiles as the hub's settlement expected, received and variance.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Network International · MID 4471-AQV · UAE01 · 30 Sep · Gross 612,480.00 · Refunds 4,860.00 · Chargebacks 1,250.00
  · Fees 12,104.40 · Net expected AED 594,265.60 · Received 594,265.60 · Settled
- Stripe · acct_MGD · UAE02 · 29 Sep · Net expected AED 48,212.75 · Received 47,712.75 · Short AED 500.00 · 2 days
```

#### Permissions

- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-623` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-623`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 8: Works in Settlement & Payout Manager\t144 → Track expected and actual settlements from payment providers/acquirers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-623?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-624` Fees, Commission, FX & Settlement Economics

**Provide visibility into the financial deductions and differences between gross payment value and net settlement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-624 |
| Who uses it | venue staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fees-commission-fx-settlement-economics-t145-adm-624` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Fixed transaction fee, Percentage fee, Authorization fee, Capture fee, Refund fee, Chargeback fee … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Gross to net: fees, commission and FX deducted before settlement.

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Fees, Commission, FX & Settlement Economics\t145".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-624; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **Pack actions with no operation: Fixed transaction fee, Percentage fee, Authorization fee, Capture fee, Refund fee, Chargeback fee, Cross-border fee, Wallet/APM fee ….** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-624; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) getPaymentProviderEconomics return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#getPaymentProviderEconomics; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getPaymentProviderEconomics` ?from |
| To | date picker | — | — | `getPaymentProviderEconomics` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every fees commission settlement** (data table)

| Shows | Format | Notes |
|---|---|---|
| Contracted fee | text | not in the schema: `Contracted fee` |
| Calculated expected fee | text | not in the schema: `Calculated expected fee` |
| Provider charged fee | text | not in the schema: `Provider charged fee` |
| Variance | text | not in the schema: `Variance` |
| FX | text | not in the schema: `FX` |

**The selected fees commission settlement** (detail panel): The pack groups this record's detail under its own headings: “Provider Fee”, “Where currencies differ, show”, “Important Boundary”.

| Shows | Format | Notes |
|---|---|---|
| Contracted fee | text | not in the schema: `Contracted fee` |
| Calculated expected fee | text | not in the schema: `Calculated expected fee` |
| Provider charged fee | text | not in the schema: `Provider charged fee` |
| Variance | text | not in the schema: `Variance` |
| FX | text | not in the schema: `FX` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed transaction fee (primary button) | navigation or local | — | — | — | — |
| Percentage fee (secondary button) | navigation or local | — | — | — | — |
| Authorization fee (secondary button) | navigation or local | — | — | — | — |
| Capture fee (secondary button) | navigation or local | — | — | — | — |
| Refund fee (secondary button) | navigation or local | — | — | — | — |
| Chargeback fee (secondary button) | navigation or local | — | — | — | — |
| Cross-border fee (secondary button) | navigation or local | — | — | — | — |
| Wallet/APM fee (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **economics**: Gross, deductions by kind, net. *(source: contracts/satellite/payments.yaml#getPaymentProviderEconomics)*

**Data it reads**: `getPaymentProviderEconomics` (onLoad, Fees, commission and FX)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fees commission settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fees commission settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fees commission settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fees commission settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
settlement:
  gross: AED 1,240,000.00
  fees: AED 22,800.00
  net: AED 1,217,200.00
```

#### Permissions

- `getPaymentProviderEconomics` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-624` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-624`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 10: Works in Fees, Commission, FX & Settlement Economics\t145 → Provide visibility into the financial deductions and differences between gross payment value and net settlement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-624?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed transaction fee, Percentage fee, Authorization fee, Capture fee, Refund fee, Chargeback fee, Cross-border fee, Wallet/APM fee.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-625` Merchant Account & Settlement Calendar Manager

**Manage operational settlement expectations across providers, merchant accounts and legal entities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-625 |
| Who uses it | venue staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row Rendered on the calendar template (M17-03, 29 September). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/merchant-account-settlement-calendar-manager-t146-adm-625` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Merchant Account & Settlement Calendar Manager\t146 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Merchant accounts, which legal entity gets the money and when (settlement calendars).

**Known correction pending (do not draw the wrong version)**

- **The screen name ends in an escaped tab and the pack page number: "Merchant Account & Settlement Calendar Manager\t146".** Why: The pack page number leaked into the name; it would print on the screen title and the navigation. *(source: screens/P08-venue-back-office.yaml#ADM-625; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listMerchantAccounts return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#listMerchantAccounts; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| View: day, week or month | select field | — | — | — | — | **Every calendar has day, week and month views, and the day view is broken into hours from the venue's day start hour** (17 September minutes, M17-03). Built on the shared calendar view … | — |
| Category | multi select | — | — | — | — | **Filtered by category, so a team sees only what is theirs** (M17-03). | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **merchant account**: Entities, venues and calendar. *(source: contracts/satellite/payments.yaml#setMerchantAccount)*

#### Outputs: what the screen shows and produces

**Shown**

**Every merchant account settlement** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transaction period | text | not in the schema: `Transaction period` |
| Expected settlement date | text | not in the schema: `Expected settlement date` |
| Actual settlement date | text | not in the schema: `Actual settlement date` |
| Status | text | not in the schema: `Status` |

**Calendar** (calendar view, from `listMerchantAccounts`): Entries of the view in force, placed by date and hour.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Legal entity | the name it points at, never the id | — |
| Venues | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be … |
| Settlement calendar | chip: Daily, Weekly, Monthly, Custom | — |
| Settlement delay days | 1,234 | — |
| Bank account reference | text | — |

**The selected merchant account settlement** (detail panel): The pack groups this record's detail under its own headings: “Tenant”, “Legal Entity”, “Provider / Acquirer”, “Merchant Account”, “For each merchant account”, “Settlement”.

| Shows | Format | Notes |
|---|---|---|
| Transaction period | text | not in the schema: `Transaction period` |
| Expected settlement date | text | not in the schema: `Expected settlement date` |
| Actual settlement date | text | not in the schema: `Actual settlement date` |
| Status | text | not in the schema: `Status` |

**Data it reads**: `listMerchantAccounts` (onLoad, Merchant accounts and calendars)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The merchant account settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the merchant account settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No merchant account settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the merchant account settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
account:
  mid: MID-DP-001
  entity: Dune Park LLC
  calendar: T+2
```

#### Permissions

- `listMerchantAccounts` → `PAYMENT_VIEW` (read) · staff
- `setMerchantAccount` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-625` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-625`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 12: Works in Merchant Account & Settlement Calendar Manager\t146 → Manage operational settlement expectations across providers, merchant accounts and legal entities.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-625?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-626` Settlement Posting, Finance Handoff & Close Manager

**Control when reconciled payment information becomes ready for downstream financial posting and period close.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-626 |
| Who uses it | venue staff holding `LEDGER_POST` (1 operate); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `obligationId` (navigation) |
| Route | `/commercial/settlement-posting-finance-handoff-close-manager-t148-adm-626` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **Settlement Posting, Finance Handoff & Close Manager\t148 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The gate between reconciliation and the ledger: which reconciled settlements are ready to post, which are held by open exceptions, what was posted, and whether the period can close. Posting is append-only; a wrong posting is reversed, never edited.

**Known correction pending (do not draw the wrong version)**

- **The only operation is recordSettlement, which settles an inter-entity obligation (one entity paying another, at the obligation's rate), and the screen expects an obligation id.** Why: Nothing here posts reconciled provider settlements; the screen's operation serves a different process. *(source: contracts/spine/finance.yaml#recordSettlement / screens/P08-venue-back-office.yaml#ADM-626; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do settlement postings happen automatically after reconciliation, or through this release gate?** → Drawn default stands (answer: "Automatic when fully matched; the screen shows status and held days"): Automatic for fully matched days; this screen shows status and the held ones. *(decided by Chinmay, 2026-10-02; DEC-213 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **posting queue**: Ready to post, Held (with the reason), Posted (with the journal number); counts and values per day. *(source: screens/P08-venue-back-office.yaml#ADM-626 / contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Post**: Posts the selected ready settlements; each gets a journal number; confirmation names the total and the period. *(source: designer default)*

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The settlement posting finance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the settlement posting finance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No settlement posting finance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the settlement posting finance are still there. The pack's own statuses are Not Ready — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The obligation is already `settled`. An `outstanding` or `disputed` one settles. |

#### Edge cases to draw

- **posting into a period that is closing**: The posting goes to the next open period with a reference to the trading date. *(source: F13 step 4)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- 30 Sep 2026 · 14 settlements ready · AED 3,112,940.25 · 2 held (open exceptions)
```

#### Permissions

- `recordSettlement` → `LEDGER_POST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-626` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-626`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 14: Works in Settlement Posting, Finance Handoff & Close Manager\t148 → Control when reconciled payment information becomes ready for downstream financial posting and period close.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-626?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `LEDGER_POST`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-627` Reconciliation Audit, Trace & Evidence Center

**Provide a complete audit trail explaining how any payment became reconciled and financially closed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-627 |
| Who uses it | venue staff holding `LEDGER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/reconciliation-audit-trace-evidence-center-t149-adm-627` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home. **Reconciliation is daily, per venue** (decided 2 October 2026, Chinmay; CHG-FIN-009; audit R110 (b)). The unit of work and of sign-off is one venue-day: POS cash, gateway settlements, bank and wallet against the ledger for that day. A longer range reviews days already reconciled; a provider's monthly file (DI-268) is matched day by day.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The evidence trail of how one payment became reconciled and closed: ingested from which file, matched how, which exception, who resolved it with what reason and approval, and which journal posted it. Read-only and exportable for auditors.

**Known correction pending (do not draw the wrong version)**

- **The audit columns (user, action, previous state, new state, reason, timestamp, approval) are drawn as select fields under a configuration pattern.** Why: They are a read-only trail, not settings. *(source: screens/P08-venue-back-office.yaml#ADM-627; Finance, Ledger & Tax · Reporting & Analytics)*
- **getUnifiedReconciliation returns totals and variances for a date range; it returns no trail.** Why: The evidence comes from the exception's resolver, time and note and from the audit log. *(source: contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| User | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Previous state | select field | — | — | — | — | — | — |
| New state | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getUnifiedReconciliation` ?from |
| To | date picker | — | — | `getUnifiedReconciliation` ?to |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **trail**: A timeline, oldest first: file ingested, line matched or exception raised, resolution (user, action, previous state, new state, reason, time, approval), journal posted, period closed. Each step links to its record. *(source: screens/P08-venue-back-office.yaml#ADM-627 / contracts/spine/finance.yaml#/components/schemas/SettlementException)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Export evidence**: PDF of the trail with the source file reference; retained with payment records for 10 years. *(source: ADR-0047)*

**Data it reads**: `getUnifiedReconciliation` (onLoad, Audit and evidence)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation audit trace configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation audit trace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation audit trace configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- '30 Sep 22:10 file NI-20260930-AQV.csv ingested · 1 Oct 02:14 amount differs AED 50.00 · 1 Oct 10:41 Omar Haddad:
  Timing difference, note ''partial refund settles 2 Oct'' · 2 Oct 06:00 matched · JE-2026-10-000311'
```

#### Permissions

- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-627` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-627`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 16: Works in Reconciliation Audit, Trace & Evidence Center\t149 → Provide a complete audit trail explaining how any payment became reconciled and financially closed.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-627?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `LEDGER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-628` Reconciliation Simulator, Forecast & AI Operations Advisor

**Provide simulation, forecasting and AI-assisted analysis across reconciliation and settlement operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block C · task VM-ADM-628 |
| Who uses it | venue staff holding `LEDGER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/reconciliation-simulator-forecast-ai-operations-advisor--adm-628` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-619 stays on the console (DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Forward look at settlement cash: expected settlement and cash receipt by date, after provider fees, refund and chargeback deductions and conversion, plus a what-if simulator. Every projected figure is labelled Forecast; with too little history the screen says so instead of drawing a line.

**Known correction pending (do not draw the wrong version)**

- **The forecast is served by getUnifiedReconciliation, which returns past totals and variances only.** Why: No operation returns a settlement forecast. *(source: contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the reconciliation simulator and AI advisor in phase one, given AI finance reporting is phase two?** → Drawn default stands (answer: "Actuals now; forecast and advisor drawn but switched off"): Build the actuals view; forecast and advisor drawn but switched off. *(decided by Chinmay, 2026-10-02; DEC-214 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getUnifiedReconciliation` ?from |
| To | date picker | — | — | `getUnifiedReconciliation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reconciliation simulator forecast** (data table)

| Shows | Format | Notes |
|---|---|---|
| Expected settlement | text | not in the schema: `Expected settlement` |
| Expected cash receipt | text | not in the schema: `Expected cash receipt` |
| Provider fees | text | not in the schema: `Provider fees` |
| Refund deductions | text | not in the schema: `Refund deductions` |
| Chargeback deductions | text | not in the schema: `Chargeback deductions` |
| Currency conversion | text | not in the schema: `Currency conversion` |
| Merchant account payout | text | not in the schema: `Merchant account payout` |

**The selected reconciliation simulator forecast** (detail panel): The pack groups this record's detail under its own headings: “Chargebacks”, “Expected Settlement Date”, “Date”, “Sep 04AED 980K”, “Sep 06AED 760K”, “Refund”.

| Shows | Format | Notes |
|---|---|---|
| Expected settlement | text | not in the schema: `Expected settlement` |
| Expected cash receipt | text | not in the schema: `Expected cash receipt` |
| Provider fees | text | not in the schema: `Provider fees` |
| Refund deductions | text | not in the schema: `Refund deductions` |
| Chargeback deductions | text | not in the schema: `Chargeback deductions` |
| Currency conversion | text | not in the schema: `Currency conversion` |
| Merchant account payout | text | not in the schema: `Merchant account payout` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **forecast table**: Expected settlement, Expected cash receipt, Provider fees, Refund deductions, Chargeback deductions, Currency conversion, Merchant account payout, by expected settlement date; values labelled "Forecast" with the basis period. *(source: screens/P08-venue-back-office.yaml#ADM-628 / DI-973)*
- **not enough history**: "Not enough settlement history to forecast yet (needs 90 days; 23 days so far)" with the actuals shown instead. *(source: DI-280)*

**Data it reads**: `getUnifiedReconciliation` (onLoad, Forecast and trend)

**Where the user goes next**

- → `ADM-619` Reconciliation & Settlement Command Center: *Back to Reconciliation & Settlement Command Center\t139*
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation simulator forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation simulator forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation simulator forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconciliation simulator forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **AI advice**: Explains why a figure moved and suggests an action; never posts, resolves or approves anything. *(source: DI-719 / DI-735)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Forecast · Fri 4 Sep · expected settlement AED 980,000 · basis last 8 Fridays
- Forecast · Sun 6 Sep · AED 760,000
```

#### Permissions

- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-628` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-628`
- Workshop pack: Payment_Payment_Orchestration.pdf board 7
- Flow F262 *Payment Payment Orchestration board 7: Reconciliation & Settlement Command …*, step 18: Works in Reconciliation Simulator, Forecast & AI Operations Advisor\t150 → Provide simulation, forecasting and AI-assisted analysis across reconciliation and settlement operations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-628?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-619`, `BO-100`.
- [ ] Every gated control is gated: `LEDGER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"getPaymentProviderEconomics": {"method":"GET","path":"/payment-providers/economics","contract":"payments","summary":"What each provider actually costs","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ProviderEconomics"},
"getUnifiedReconciliation": {"method":"GET","path":"/reconciliation/unified","contract":"finance","summary":"Every money source against the ledger, in one view","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"UnifiedReconciliation"},
"ingestSettlementFile": {"method":"POST","path":"/settlements","contract":"finance","summary":"Ingest a provider settlement file","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listMerchantAccounts": {"method":"GET","path":"/merchant-accounts","contract":"payments","summary":"Merchant accounts, settlement calendars and payout routing","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MerchantAccount"},
"listReconciliationSources": {"method":"GET","path":"/reconciliation-sources","contract":"payments","summary":"The files and feeds reconciliation is run against","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ReconciliationSource"},
"listSettlementExceptions": {"method":"GET","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Unmatched or mismatched settlement lines","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordSettlement": {"method":"POST","path":"/inter-entity-obligations/{obligationId}/settle","contract":"finance","summary":"One entity paid another","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InterEntityObligation"},
"resolveSettlementException": {"method":"POST","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Resolve a settlement exception","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SettlementException"},
"setMerchantAccount": {"method":"PUT","path":"/merchant-accounts","contract":"payments","summary":"Bind a merchant account to entities, venues and a calendar","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"MerchantAccount","responds":"MerchantAccount"},
"setReconciliationMatchingRules": {"method":"PUT","path":"/reconciliation-rules","contract":"payments","summary":"How a platform transaction is matched to a settled one","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ReconciliationMatchingRules","responds":"ReconciliationMatchingRules"},
"setReconciliationSource": {"method":"PUT","path":"/reconciliation-sources","contract":"payments","summary":"Define a settlement or statement feed","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ReconciliationSource","responds":"ReconciliationSource"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"InterEntityObligation": {"type":"object","x-ticvai-persistence":"ledger.inter_entity_obligation","required":["id","fromLegalEntityId","toLegalEntityId","arisingAmount","arisingAt","status"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when the obligation arises, so a UUID, as the `obligationId` path parameter types it."},"fromLegalEntityId":{"type":"string","format":"uuid","description":"The selling entity. Holds the liability, and therefore the FX exposure."},"toLegalEntityId":{"type":"string","format":"uuid","description":"The consuming entity, which provided the service at redemption."},"entitlementId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"arisingAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"In the **consuming** entity's base currency, at the rate in force on the redemption date. Neither entity ever holds a balance in a currency that is not its own.\n"},"rateApplied":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}]},"arisingAt":{"type":"string","format":"date-time","description":"Redemption. Not sale — the obligation exists when the service is given."},"status":{"type":"string","enum":["outstanding","settled","disputed"]},"settledAt":{"type":"string","format":"date-time","nullable":true},"settlementRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true},"fxMovement":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Rate movement between arising and settling. Posts to FX gain and loss on the selling entity, which carried the balance.\n"},"agreedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"description":"**The figure a dispute was resolved at** (4 October 2026, CHG-FXC-003): written by `resolveObligationDispute`, which returns the obligation to `outstanding`. `arisingAmount` keeps the original, so the difference stays auditable; settlement settles `agreedAmount` where it is set and `arisingAmount` otherwise. Null until a dispute is resolved."},"disputeNote":{"type":"string","nullable":true,"readOnly":true,"description":"The `note` of the last `disputeObligation` or `resolveObligationDispute`."}}},
"MerchantAccount": {"type":"object","x-ticvai-persistence":"payments.merchant_account","description":"Board 7.7. **Which legal entity gets the money, and when.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"legalEntityId":{"type":"string","format":"uuid"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be anything else. Kept on the wire, removed from the table.\n"},"settlementCalendar":{"type":"string","enum":["daily","weekly","monthly","custom"]},"settlementDelayDays":{"type":"integer","default":1},"bankAccountReference":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProviderEconomics": {"type":"object","description":"Board 2.9. **Cost per transaction is a routing input.**","properties":{"connectionId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"transactions":{"type":"integer"},"grossVolume":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"schemeFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"interchange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerMargin":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fxSpread":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargebackCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"effectiveRatePercent":{"type":"number"}}},
"ReconciliationMatchingRules": {"type":"object","x-ticvai-persistence":"payments.matching_rules","description":"Board 7.3. **Exact matching was never enough.**","properties":{"primaryKey":{"type":"string","enum":["providerReference","platformReference","authorisationCode","retrievalReference"]},"fallbackKeys":{"type":"array","items":{"type":"string"}},"amountToleranceMinor":{"type":"integer","default":0},"dateWindowDays":{"type":"integer","default":2,"description":"**Acquirers batch across midnight.** A same-day-only match manufactures exceptions every night.\n"},"netOfFees":{"type":"boolean","default":true},"autoResolveBelowMinor":{"type":"integer","default":0,"description":"**Rounding differences of a fil are not worth a person.** Above this they are."},"scopePath":{"type":"string"}}},
"ReconciliationSource": {"type":"object","x-ticvai-persistence":"payments.reconciliation_source","description":"Board 7.2. **A file that did not arrive looks like a day with no settlements.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"connectionId":{"type":"string","format":"uuid","nullable":true},"transport":{"type":"string","enum":["sftp","api","email","manualUpload"]},"format":{"type":"string","enum":["csv","fixedWidth","json","xml","camt053"]},"expectedSchedule":{"type":"string","nullable":true,"default":"daily","description":"How often a file is expected. **Daily by default, one per venue per trading day** (decided 28 September, audit R110 (b)), because settlement is reconciled daily per venue (`finance.ingestSettlementFile`)."},"expectedByTime":{"type":"string","nullable":true},"alertIfMissing":{"type":"boolean","default":true},"fieldMapping":{"type":"object","additionalProperties":{"type":"string"}},"scopePath":{"type":"string"}}},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementException": {"x-ticvai-persistence":"ledger.settlement_exception","type":"object","required":["id","settlementId","kind","providerReference","amount"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."},"settlementId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["unmatchedInProvider","unmatchedInLedger","amountMismatch","duplicateInProvider","feeUnexplained"]},"providerReference":{"type":"string","nullable":true},"paymentId":{"type":"string","format":"uuid","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"resolution":{"allOf":[{"$ref":"#/components/schemas/SettlementResolution"}],"nullable":true,"description":"Null while the exception is open."},"note":{"type":"string","nullable":true,"description":"The `note` given to `resolveSettlementException`, stored with the resolution."},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"SettlementResolution": {"type":"string","description":"How a settlement exception was explained. One vocabulary for the request and the stored exception.","enum":["matchedManually","writeOff","disputeRaised","providerError","timingDifference"]},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]},
"UnifiedReconciliation": {"type":"object","description":"4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n","properties":{"from":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"to":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"sources":{"type":"array","items":{"type":"object","properties":{"source":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]},"providerName":{"type":"string","nullable":true},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionCount":{"type":"integer"}}}},"variances":{"type":"array","description":"**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n","items":{"type":"object","properties":{"between":{"type":"array","description":"The two sources that disagree, as named in `sources[].source`.","minItems":2,"maxItems":2,"items":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"likelyCause":{"type":"string","nullable":true}}}}}}
}
```
