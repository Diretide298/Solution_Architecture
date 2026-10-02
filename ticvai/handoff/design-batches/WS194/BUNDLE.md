# WS194 — Wallet Configuration Backend Structure v1.0 board 9

**10 screens · 11 operations · 14 schemas · 5 permissions**

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
  `LEDGER_APPROVE, LEDGER_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1163` | Wallet Finance & Liability Command Center | B–D | 0 | 66 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1164` | Wallet Financial Classification & Accounting Mapping | B–D | 23 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1165` | Wallet Sub-Ledger & Balance Control | B–D | 2 | 25 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1166` | Multi-Source Reconciliation Configuration | B–D | 32 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1167` | Reconciliation Exception & Resolution Workbench | B–D | 0 | 24 | 6 | 1 | 2 | 0 | — | notStarted (—) |
| `BO-1168` | Gift Card Liability Management | B–D | 0 | 42 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1169` | Breakage & Revenue Recognition Policy | B–D | 0 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1170` | Wallet Financial Period & Closing Controls | B–D | 18 | 18 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1171` | Wallet Analytics & Management Reporting | B–D | 0 | 34 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1172` | Finance Validation, Reporting & Audit Center | B–D | 0 | 10 | 6 | 1 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1163, BO-1167, BO-1168, BO-1169, BO-1171 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1163` Wallet Finance & Liability Command Center

**Provide Finance and authorized management users with a consolidated financial view of all wallet obligations and movements. Executive KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-finance-liability-command-center-bo-1163` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All wallet obligations and movements for finance.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getWalletLiability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getWalletLiability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#getWalletLiability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet finance liability** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total wallet liability | text | not in the schema: `Total Wallet Liability` |
| Cash credit liability | text | not in the schema: `Cash Credit Liability` |
| Gift card liability | text | not in the schema: `Gift Card Liability` |
| Refund credit liability | text | not in the schema: `Refund Credit Liability` |
| Bonus/promotional value | text | not in the schema: `Bonus/Promotional Value` |
| Membership credit exposure | text | not in the schema: `Membership Credit Exposure` |
| Outstanding stored value | text | not in the schema: `Outstanding Stored Value` |
| Issued value | text | not in the schema: `Issued Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Breakage recognized | text | not in the schema: `Breakage Recognized` |
| Unreconciled value | text | not in the schema: `Unreconciled Value` |
| Suspended/frozen value | text | not in the schema: `Suspended/Frozen Value` |
| Liability breakdown | text | not in the schema: `Liability Breakdown` |
| Credit type | text | not in the schema: `Credit type` |
| Wallet type | text | not in the schema: `Wallet type` |
| Gift card | text | not in the schema: `Gift card` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Customer type | text | not in the schema: `Customer type` |
| Accounting period | text | not in the schema: `Accounting period` |
| Movement analysis | text | not in the schema: `Movement Analysis` |
| Opening liability | text | not in the schema: `Opening Liability` |
| Funding | text | not in the schema: `Funding` |
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Credits issued | text | not in the schema: `Credits Issued` |
| Refunds to wallet | text | not in the schema: `Refunds to Wallet` |
| − redemptions | text | not in the schema: `− Redemptions` |
| − expirations | text | not in the schema: `− Expirations` |
| … 3 more | | `schemas.json` |

**The selected wallet finance liability** (detail panel): The pack groups this record's detail under its own headings: “Highlight”.

| Shows | Format | Notes |
|---|---|---|
| Total wallet liability | text | not in the schema: `Total Wallet Liability` |
| Cash credit liability | text | not in the schema: `Cash Credit Liability` |
| Gift card liability | text | not in the schema: `Gift Card Liability` |
| Refund credit liability | text | not in the schema: `Refund Credit Liability` |
| Bonus/promotional value | text | not in the schema: `Bonus/Promotional Value` |
| Membership credit exposure | text | not in the schema: `Membership Credit Exposure` |
| Outstanding stored value | text | not in the schema: `Outstanding Stored Value` |
| Issued value | text | not in the schema: `Issued Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Breakage recognized | text | not in the schema: `Breakage Recognized` |
| Unreconciled value | text | not in the schema: `Unreconciled Value` |
| Suspended/frozen value | text | not in the schema: `Suspended/Frozen Value` |
| Liability breakdown | text | not in the schema: `Liability Breakdown` |
| Credit type | text | not in the schema: `Credit type` |
| Wallet type | text | not in the schema: `Wallet type` |
| Gift card | text | not in the schema: `Gift card` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Customer type | text | not in the schema: `Customer type` |
| Accounting period | text | not in the schema: `Accounting period` |
| Movement analysis | text | not in the schema: `Movement Analysis` |
| Opening liability | text | not in the schema: `Opening Liability` |
| Funding | text | not in the schema: `Funding` |
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Credits issued | text | not in the schema: `Credits Issued` |
| Refunds to wallet | text | not in the schema: `Refunds to Wallet` |
| − redemptions | text | not in the schema: `− Redemptions` |
| − expirations | text | not in the schema: `− Expirations` |
| … 3 more | | `schemas.json` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **finance KPIs**: Outstanding liability, funded, spent, breakage. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `getWalletLiability` (onLoad, Liability at a glance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1164` Wallet Financial Classification & Accounting Mapping: *Wallet Financial Classification & Accounting Mapping*
- → `BO-1165` Wallet Sub-Ledger & Balance Control: *Wallet Sub-Ledger & Balance Control*
- → `BO-1166` Multi-Source Reconciliation Configuration: *Multi-Source Reconciliation Configuration*
- → `BO-1167` Reconciliation Exception & Resolution Workbench: *Reconciliation Exception & Resolution Workbench*
- → `BO-1168` Gift Card Liability Management: *Gift Card Liability Management*
- → `BO-1169` Breakage & Revenue Recognition Policy: *Breakage & Revenue Recognition Policy*
- → `BO-1170` Wallet Financial Period & Closing Controls: *Wallet Financial Period & Closing Controls*
- → `BO-1171` Wallet Analytics & Management Reporting: *Wallet Analytics & Management Reporting*
- → `BO-1172` Finance Validation, Reporting & Audit Center: *Finance Validation, Reporting & Audit Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet finance liability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet finance liability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet finance liability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet finance liability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  outstanding: AED 2,184,300.00
  fundedMTD: AED 1,240,000.00
```

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1163` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1163`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 1: Opens Wallet Finance & Liability Command Center → Provide Finance and authorized management users with a consolidated financial view of all wallet obligations and movements. Executive KPIs
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F301 branch at step 1 (expected): when Nothing has been set up on Wallet Finance & Liability Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F301 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1163?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1164`, `BO-1165`, `BO-1166`, `BO-1167`, `BO-1168`, `BO-1169`, `BO-1170`, `BO-1171`, `BO-1172`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1164` Wallet Financial Classification & Accounting Mapping

**Define the financial classification of every wallet credit and transaction type. Credit Mapping**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure accounting treatment for; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-financial-classification-accounting-mapping-bo-1164` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet accounting mapping that setWalletAccountingMapping writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which ledger account each credit type and transaction type posts to; every wallet transaction maps to a GL entry.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletAccountingMapping and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cash Credit | select field | — | — | — | — | — | — |
| Refund Credit | select field | — | — | — | — | — | — |
| Gift Card | select field | — | — | — | — | — | — |
| Bonus Credit | select field | — | — | — | — | — | — |
| Promotional Credit | select field | — | — | — | — | — | — |
| Membership Credit | select field | — | — | — | — | — | — |
| Ride Credit | select field | — | — | — | — | — | — |
| F&B Credit | select field | — | — | — | — | — | — |
| Retail Credit | select field | — | — | — | — | — | — |
| Parking Credit | select field | — | — | — | — | — | — |
| Other credits | select field | — | — | — | — | — | — |
| Transaction Mapping | select field | — | — | — | — | — | — |
| Top-Up | select field | — | — | — | — | — | — |
| Redemption | select field | — | — | — | — | — | — |
| Refund | select field | — | — | — | — | — | — |
| Transfer | select field | — | — | — | — | — | — |
| Adjustment | select field | — | — | — | — | — | — |
| Reversal | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Gift Card Sale | select field | — | — | — | — | — | — |
| Gift Card Redemption | select field | — | — | — | — | — | — |
| Breakage | select field | — | — | — | — | — | — |
| Mapping Dimensions | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **mapping**: Credit types as rows, accounts picked from the chart of accounts. *(source: contracts/satellite/wallet.yaml#setWalletAccountingMapping / TRACKER Actions row 103)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet financial classification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet financial classification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet financial classification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping:
  Cash: 2310 Customer wallet liability
  Bonus: 2315 Promotional credit
  breakage: 4810 Breakage income
```

#### Permissions

- `setWalletAccountingMapping` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1164` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1164`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 2: Works in Wallet Financial Classification & Accounting Mapping → Define the financial classification of every wallet credit and transaction type. Credit Mapping

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1164?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1165` Wallet Sub-Ledger & Balance Control

**Maintain the authoritative financial transaction history behind every wallet balance. Sub-Ledger View**

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
| Route | `/orders-money/wallet-sub-ledger-balance-control-bo-1165` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The wallet sub-ledger behind every balance and its agreement with the general ledger.

**Known correction pending (do not draw the wrong version)**

- **No write operation: a configuration screen (Wallet Sub-Ledger & Balance Control) declares only reads (getWalletReconciliation).** Why: Nothing it shows can be changed from it; either it is a view (and its edits happen on the record editor, which it should link to) or a write is missing. *(source: contracts/satellite/wallet.yaml#getWalletReconciliation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Sub-ledger total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Sub ledger total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**General ledger total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| General ledger total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Acquirer total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Acquirer total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Balance exceptions** (data table, from `getWalletReconciliation`): The pack's balance integrity check: any mismatch is a financial exception.

| Shows | Format | Notes |
|---|---|---|
| Pair | chip: Sub ledger vs general ledger, Sub ledger vs acquirer, General ledger vs acquirer | — |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Transactions | list or chips (count when long) | — |
| Likely cause | text | — |

**Sub-ledger entries** (data table): No ledger-entry read is bound to this screen.

| Shows | Format | Notes |
|---|---|---|
| Ledger entry ID | text | not in the schema: `Ledger entry ID` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Customer / account | text | not in the schema: `Customer / account` |
| Transaction ID | text | not in the schema: `Transaction ID` |
| Transaction type | text | not in the schema: `Transaction type` |
| Credit bucket | text | not in the schema: `Credit bucket` |
| Credit lot | text | not in the schema: `Credit lot` |
| Debit | text | not in the schema: `Debit` |
| Credit | text | not in the schema: `Credit` |
| Currency | text | not in the schema: `Currency` |
| Balance before | text | not in the schema: `Balance before` |
| Balance after | text | not in the schema: `Balance after` |
| Source system | text | not in the schema: `Source system` |
| Venue | text | not in the schema: `Venue` |
| Channel | text | not in the schema: `Channel` |
| Timestamp | text | not in the schema: `Timestamp` |
| Financial status | text | not in the schema: `Financial status` |
| Related transaction | text | not in the schema: `Related transaction` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **sub-ledger**: Movements with the GL reference. *(source: contracts/satellite/wallet.yaml#getWalletReconciliation)*

**Data it reads**: `getWalletReconciliation` (onLoad, Sub-ledger against the ledger)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet sub-ledger balance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet sub-ledger balance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet sub-ledger balance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet sub-ledger balance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  movement: top-up AED 200.00
  gl: JE-2026-90112
```

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1165` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1165`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 4: Works in Wallet Sub-Ledger & Balance Control → Maintain the authoritative financial transaction history behind every wallet balance. Sub-Ledger View

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1165?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1166` Multi-Source Reconciliation Configuration

**Reconcile wallet financial events across Wallet, Payments, Sales Channels and Finance. The supplied requirements specifically call for reconciliation of payment status between sales channels, the bank/payment gateway and the ticketing system. Reconciliation Sources**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/multi-source-reconciliation-configuration-bo-1166` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which sources the wallet reconciles against, matched how and when.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transaction ID | select field | — | — | — | — | — | — |
| Wallet ID | select field | — | — | — | — | — | — |
| Payment reference | select field | — | — | — | — | — | — |
| Order number | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Terminal | select field | — | — | — | — | — | — |
| External reference | select field | — | — | — | — | — | — |
| Reconciliation Status | select field | — | — | — | — | — | — |
| Matched | select field | — | — | — | — | — | — |
| Partially Matched | select field | — | — | — | — | — | — |
| Unmatched | select field | — | — | — | — | — | — |
| Duplicate | select field | — | — | — | — | — | — |
| Amount Mismatch | select field | — | — | — | — | — | — |
| Currency Mismatch | select field | — | — | — | — | — | — |
| Missing Wallet Entry | select field | — | — | — | — | — | — |
| Missing Payment Entry | select field | — | — | — | — | — | — |
| Reconciliation Frequency | select field | — | — | — | — | — | — |
| Real-time | select field | — | — | — | — | — | — |
| Hourly | select field | — | — | — | — | — | — |
| End of day | select field | — | — | — | — | — | — |
| Scheduled | select field | — | — | — | — | — | — |
| Manual | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

**Sent by *Save reconciliation sources*** (`setWalletReconciliationSources`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sources `sources` | repeatable rows | required | — | at least 1 | — | — | `setWalletReconciliationSources` body |
| Kind `sources[].kind` | select | required | — | Wallet ledger · POS · Payment gateway · Payment server · Gift card · Finance | — | — | `setWalletReconciliationSources` body |
| Enabled `sources[].enabled` | toggle | required | on | — | — | — | `setWalletReconciliationSources` body |
| Match keys `sources[].matchKeys` | list of values (chips) | optional | — | — | — | Fields a movement is matched on, e.g. transactionId, authorisationCode, terminalId, amount, businessDate. | `setWalletReconciliationSources` body |
| Tolerance amount `sources[].toleranceAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | A pair differing by no more than this is agreed. Default zero. | `setWalletReconciliationSources` body |
| Schedule `sources[].schedule` | radio group | optional | End of business day | Real time · Hourly · Daily · End of business day | — | — | `setWalletReconciliationSources` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletReconciliationSources` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **sources**: Each source switched on with matching keys and schedule. *(source: contracts/satellite/wallet.yaml#setWalletReconciliationSources)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet Ledger (primary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| Payment Gateway (secondary button) | navigation or local | — | — | — | — |
| Payment Server (secondary button) | navigation or local | — | — | — | — |
| Gift Card (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Save reconciliation sources (primary button) | `setWalletReconciliationSources` PUT `/wallet-reconciliation-sources` | WalletReconciliationSources | WalletReconciliationSources | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 `walletLedger` disabled or missing, or a source kind listed twice. | — |

**Data it reads**: `getWalletReconciliation` (onLoad, Three sources compared)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-source reconciliation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-source reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-source reconciliation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `walletLedger` disabled or missing, or a source kind listed twice. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sources:
- name: Network International settlement
  match: provider reference
  schedule: daily 06:00
```

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `setWalletReconciliationSources` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1166` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1166`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 6: Works in Multi-Source Reconciliation Configuration → Reconcile wallet financial events across Wallet, Payments, Sales Channels and Finance. The supplied requirements specifically call for reconciliation of payment status between sales channels, the …

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1166?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Wallet Ledger, POS, Payment Gateway, Payment Server, Gift Card, Finance, Save reconciliation sources.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1167` Reconciliation Exception & Resolution Workbench

**Provide Finance and Operations with a governed workspace to investigate reconciliation failures. Exception Examples Payment successful / Wallet not funded Wallet funded / Payment failed Wallet debited / POS transaction missing Duplicate wallet debit Refund issued / Finance event missing Gift card redeemed / Liability unchanged**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/reconciliation-exception-resolution-workbench-bo-1167` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Investigate reconciliation failures (payment succeeded but wallet not funded, and the reverse) and fix them with an adjustment.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reconciliation exception resolution** (data table)

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Transaction | text | not in the schema: `Transaction` |
| Wallet | text | not in the schema: `Wallet` |
| Source | text | not in the schema: `Source` |
| Expected amount | text | not in the schema: `Expected amount` |
| Actual amount | text | not in the schema: `Actual amount` |
| Difference | text | not in the schema: `Difference` |
| Currency | text | not in the schema: `Currency` |
| Age | text | not in the schema: `Age` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**The selected reconciliation exception resolution** (detail panel): The pack groups this record's detail under its own headings: “Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Transaction | text | not in the schema: `Transaction` |
| Wallet | text | not in the schema: `Wallet` |
| Source | text | not in the schema: `Source` |
| Expected amount | text | not in the schema: `Expected amount` |
| Actual amount | text | not in the schema: `Actual amount` |
| Difference | text | not in the schema: `Difference` |
| Currency | text | not in the schema: `Currency` |
| Age | text | not in the schema: `Age` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Adjust to resolve**: Reason referencing the exception. *(source: contracts/satellite/wallet.yaml#adjustWallet)*

**Data it reads**: `getWalletReconciliation` (onLoad, Exceptions to resolve)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation exception resolution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation exception resolution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation exception resolution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconciliation exception resolution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  type: Payment OK, wallet not funded
  amount: AED 200.00
```

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `adjustWallet` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.113 | Refund management | Ticketing Catalogue | CONTRACTED | `adjustWallet` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1167` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1167`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 8: Works in Reconciliation Exception & Resolution Workbench → Provide Finance and Operations with a governed workspace to investigate reconciliation failures. Exception Examples Payment successful / Wallet not funded Wallet funded / Payment failed Wallet …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1167?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1168` Gift Card Liability Management

**Provide detailed financial control of outstanding gift-card obligations. Requirement 4.3.36 explicitly requires reporting of outstanding gift-card balances, redeemed value, unredeemed balances, expired balances and liability exposure by venue, tenant, currency and accounting period. Liability Dashboard**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/gift-card-liability-management-bo-1168` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Outstanding gift card obligations: balances, redeemed, unredeemed, expired.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getWalletLiability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getWalletLiability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#getWalletLiability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every gift card liability** (data table)

| Shows | Format | Notes |
|---|---|---|
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Original issued value | text | not in the schema: `Original Issued Value` |
| Outstanding value | text | not in the schema: `Outstanding Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Partially redeemed value | text | not in the schema: `Partially Redeemed Value` |
| Unredeemed value | text | not in the schema: `Unredeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Suspended value | text | not in the schema: `Suspended Value` |
| Breakage | text | not in the schema: `Breakage` |
| Liability exposure | text | not in the schema: `Liability Exposure` |
| Breakdown | text | not in the schema: `Breakdown` |
| Gift card program | text | not in the schema: `Gift card program` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Issuance date | text | not in the schema: `Issuance date` |
| Expiry date | text | not in the schema: `Expiry date` |
| Accounting period | text | not in the schema: `Accounting period` |
| Sales channel | text | not in the schema: `Sales channel` |
| Corporate program | text | not in the schema: `Corporate program` |
| Aging analysis | text | not in the schema: `Aging Analysis` |

**The selected gift card liability** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Original issued value | text | not in the schema: `Original Issued Value` |
| Outstanding value | text | not in the schema: `Outstanding Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Partially redeemed value | text | not in the schema: `Partially Redeemed Value` |
| Unredeemed value | text | not in the schema: `Unredeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Suspended value | text | not in the schema: `Suspended Value` |
| Breakage | text | not in the schema: `Breakage` |
| Liability exposure | text | not in the schema: `Liability Exposure` |
| Breakdown | text | not in the schema: `Breakdown` |
| Gift card program | text | not in the schema: `Gift card program` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Issuance date | text | not in the schema: `Issuance date` |
| Expiry date | text | not in the schema: `Expiry date` |
| Accounting period | text | not in the schema: `Accounting period` |
| Sales channel | text | not in the schema: `Sales channel` |
| Corporate program | text | not in the schema: `Corporate program` |
| Aging analysis | text | not in the schema: `Aging Analysis` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **gift card liability**: By issue period and status. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `getWalletLiability` (onLoad, Gift card liability)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card liability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card liability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card liability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card liability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
liability:
  outstanding: AED 612,000.00
  expired: AED 22,000.00
```

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1168` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1168`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 10: Works in Gift Card Liability Management → Provide detailed financial control of outstanding gift-card obligations. Requirement 4.3.36 explicitly requires reporting of outstanding gift-card balances, redeemed value, unredeemed balances …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1168?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1169` Breakage & Revenue Recognition Policy

**Configure the wallet-side business rules for expired/unredeemed gift-card value. Requirement 4.3.37 requires configurable expiration policies, gift-card breakage calculation and generation of revenue- recognition entries according to configured accounting policies. Breakage Configuration**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Gift Card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/breakage-revenue-recognition-policy-bo-1169` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet accounting mapping that setWalletAccountingMapping writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Breakage and revenue recognition rules for expired or unredeemed value.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletAccountingMapping and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **breakage account**: Account and recognition timing per credit type. *(source: contracts/satellite/wallet.yaml#setWalletAccountingMapping)*

#### Outputs: what the screen shows and produces

**Shown**

**Every breakage revenue recognition** (data table)

| Shows | Format | Notes |
|---|---|---|
| Original value → AED 500 | text | not in the schema: `Original value → AED 500` |
| Redeemed → AED 350 | text | not in the schema: `Redeemed → AED 350` |
| Expired remaining balance → AED 150 | text | not in the schema: `Expired remaining balance → AED 150` |

**The selected breakage revenue recognition** (detail panel): The pack groups this record's detail under its own headings: “Finance approval”, “Instead”.

| Shows | Format | Notes |
|---|---|---|
| Original value → AED 500 | text | not in the schema: `Original value → AED 500` |
| Redeemed → AED 350 | text | not in the schema: `Redeemed → AED 350` |
| Expired remaining balance → AED 150 | text | not in the schema: `Expired remaining balance → AED 150` |

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The breakage revenue recognition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the breakage revenue recognition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No breakage revenue recognition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the breakage revenue recognition are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  creditType: Gift card
  recognise: at expiry
  account: '4810'
```

#### Permissions

- `setWalletAccountingMapping` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1169` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1169`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 12: Works in Breakage & Revenue Recognition Policy → Configure the wallet-side business rules for expired/unredeemed gift-card value. Requirement 4.3.37 requires configurable expiration policies, gift-card breakage calculation and generation of …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1169?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1170` Wallet Financial Period & Closing Controls

**Support controlled month-end and financial-period processing for wallet balances. Period Status Open → Closing → Under Review → Closed → Reopened with Authorization Pre-Close Validation Unreconciled transactions Pending refunds Pending reversals Pending adjustments Negative balances Missing accounting mappings Failed integrations Unprocessed expirations Gift-card breakage candidates Pending approvals Closing Snapshot**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_VIEW`, `WALLET_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-financial-period-closing-controls-bo-1170` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Month-end for wallet money: a roll-forward of the wallet liability from opening to closing balance, the checks that must pass before the period closes, and the close itself. Wallet balances are a liability to customers until redeemed or recognised as breakage under policy; the finance manager must see every movement that explains the change and every blocker that stops the close.

**Known correction pending (do not draw the wrong version)**

- **The 18 fields are selectFields under a configEditor pattern, but most of them (Opening liability, Funding, Redemption, Breakage, Closing liability) are figures of a statement, not settings.** Why: A designer would draw dropdowns for amounts. *(source: screens/P08-venue-back-office.yaml#BO-1170; Finance, Ledger & Tax · Reporting & Analytics)*
- **The purpose lists statuses Open, Closing, Under Review, Closed, Reopened; the contract has open, closing and closed only.** Why: Under review is closing with an approval waiting; reopened is a history event. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodStatus / R144; Finance, Ledger & Tax · Reporting & Analytics)*
- **getWalletLiability returns outstanding, expiring and breakage at a date; it returns none of the movements (funding, credits issued, redemption, refunds, transfers, adjustments) the roll-forward needs.** Why: The roll-forward cannot be built from the declared reads. *(source: contracts/satellite/wallet.yaml#/components/schemas/WalletLiabilityRow; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Close by tenant", "Close by venue" and "Close by currency" imply separate closes; a fiscal period belongs to a legal entity and closes at region scope.** Why: There is no per-venue or per-currency close in the contract. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriod / contracts/spine/finance.yaml#closeFiscalPeriod; Finance, Ledger & Tax · Reporting & Analytics)*
- **The wallet pre-close validations (pending refunds, pending reversals, negative balances, missing accounting mappings, failed integrations, unprocessed expirations, breakage candidates) are not values of the close-check list.** Why: The close cannot block on them, so the screen would show checks nothing runs. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult / screens/P08-venue-back-office.yaml#BO-1170; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which wallet-specific checks join the period-close checks, and does a wallet movement summary operation get added?** → Add a wallet movement summary operation and wallet pre-close checks. *(decided by Chinmay, 2026-10-02; DEC-220 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Opening liability | select field | — | — | — | — | — | — |
| Funding | select field | — | — | — | — | — | — |
| Credits issued | select field | — | — | — | — | — | — |
| Redemption | select field | — | — | — | — | — | — |
| Refunds | select field | — | — | — | — | — | — |
| Transfers | select field | — | — | — | — | — | — |
| Adjustments | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Breakage | select field | — | — | — | — | — | — |
| Closing liability | select field | — | — | — | — | — | — |
| Controls | select field | — | — | — | — | — | — |
| Close by tenant | select field | — | — | — | — | — | — |
| Close by venue | select field | — | — | — | — | — | — |
| Close by currency | select field | — | — | — | — | — | — |
| Lock financial period | select field | — | — | — | — | — | — |
| Reopen with approval | select field | — | — | — | — | — | — |
| Carry exceptions forward | select field | — | — | — | — | — | — |
| Export close package | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Legal entity | picker: choose a legal entity | — | — | `listFiscalPeriods` ?legalEntityId |
| Status | segmented control | — | Open · Closing · Closed | `listFiscalPeriods` ?status |
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |
| From | date picker | — | — | `getWalletMovementSummary` ?from |
| To | date picker | — | — | `getWalletMovementSummary` ?to |
| Group by | segmented control | — | Credit type · Wallet type · Venue | `getWalletMovementSummary` ?groupBy |
| Period end | date picker | — | — | `getWalletPreCloseChecks` ?periodEnd |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **period and legal entity**: The fiscal period being closed, chosen from the legal entity's periods; close is per legal entity and region, so "close by tenant / venue / currency" are views of the roll-forward, not separate closes. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriod / contracts/spine/finance.yaml#closeFiscalPeriod)*
- **Reopen with approval**: Reopening needs a reason (kept in the period's history) and a finance approver who is not the requester; reopening restates figures already reported, so the default advice is a reversal in the open period instead. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriod / F13 step 6 / R144)*

#### Outputs: what the screen shows and produces

**Shown**

**Wallet movement summary** (data table, from `getWalletMovementSummary`)

| Shows | Format | Notes |
|---|---|---|
| Group key | text | — |
| Opening | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Top ups | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunds in | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Transfers in | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Adjustments in | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Transfers out | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Adjustments out | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunds out | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expired | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Breakage recognised | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Closing | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ties out | yes / no (icon or chip) | Opening plus every movement equals closing. |

**Wallet pre-close checks** (data table, from `getWalletPreCloseChecks`): **A wallet movement summary and wallet pre-close checks (decided 2 October 2026 by Chinmay, DEC-220; CHG-CSA-027, CHG-CSP-040)**; the period close waits in the approvals inbox (DEC-221) with a deep link here.

| Shows | Format | Notes |
|---|---|---|
| Code | chip: Roll forward ties, Sub ledger ties to ledger, No expired holds open, No pending … | — |
| Outcome | chip: Pass, Warn, Fail | — |
| Detail | text | — |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **liability roll-forward**: A vertical statement, read-only: Opening liability, plus Funding (top-ups), plus Credits issued, minus Redemption, minus Refunds, plus or minus Transfers, plus or minus Adjustments, minus Breakage recognised, equals Closing liability. Expired-this-period is a memo line, because breakage is recognised on policy, not on expiry. The check line "Opening + movements = Closing" shows a tick or the unexplained difference. *(source: contracts/satellite/wallet.yaml#getWalletLiability / contracts/satellite/wallet.yaml#/components/schemas/WalletLiabilityRow / TRACKER Actions row 164)*
- **liability breakdown**: Grouping switch by credit type, wallet type, venue and age band; one figure per currency. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*
- **period status**: Open, Closing, Closed. "Awaiting approval" is Closing with an approval request waiting, shown with the approver's name; "Reopened" is an event in the history, not a status. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodStatus / contracts/spine/finance.yaml#/components/schemas/FiscalPeriod)*
- **pre-close checks**: One row per check with pass or the blocking count and a link to fix it. The ledger's checks are trial balance balances, no unapproved journals, no open shifts, settlements reconciled, recognition run complete, prior period closed and variance exceptions reviewed. The wallet pre-close checks join them, read from a wallet movement summary (an operation to be added), so none is drawn greyed. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult / F13 step 1 / decided 2 October 2026 by Chinmay (CHG-NOTE-003))*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Export close package**: PDF and Excel of the roll-forward, the checks and the period history, stamped with who and when. *(source: screens/P08-venue-back-office.yaml#BO-1170 / ADR-0047)*
- **Carry exceptions forward**: Only an exception reviewed and accepted may be carried; it stays visible in the next period's checks with its age. *(source: screens/P08-venue-back-office.yaml#BO-1170 / contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult)*

**Data it reads**: `listFiscalPeriods` (onLoad, The period being closed); `getWalletLiability` (onLoad, Closing balance); `getWalletMovementSummary` (onLoad, Wallet movements for the period (DEC-220)); `getWalletPreCloseChecks` (onLoad, The wallet checks that must pass before the period closes …)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet financial period configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet financial period untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet financial period configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **the roll-forward does not tie (opening plus movements differs from closing)**: The difference is shown in red with the wallet-to-ledger and wallet-to-acquirer reconciliation one click away; close is not offered. *(source: contracts/satellite/wallet.yaml#getWalletReconciliation)*
- **a negative wallet balance exists**: Listed as a blocker with the wallet count; it cannot be netted against other balances. *(source: screens/P08-venue-back-office.yaml#BO-1170)*

#### Consistency with other screens

- Match `BO-090 Period Close and BO-1172`: One close, three doors. The close operations live on BO-090 (F13) and BO-1172; this screen must use the same status words and the same check names, and hand off rather than run a second close.
- Match `BO-076 Revenue Recognition`: Breakage recognised here equals the breakage posted to revenue there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entity: Aquaventure Leisure LLC · September 2026 · Closing (awaiting approval from Fatima Al Mansoori)
rollForward:
  openingLiability: AED 1,250,000.00
  funding: AED 486,300.00
  creditsIssued: AED 18,750.00
  redemption: − AED 512,940.00
  refunds: − AED 9,860.00
  transfers: AED 0.00
  adjustments: − AED 1,200.00
  breakageRecognised: − AED 6,200.00
  closingLiability: AED 1,224,850.00
  memoExpired: AED 14,500.00 expired this period, 6,200.00 recognised as breakage under policy, 8,300.00 still held
checks: 'Settlements reconciled: 2 open exceptions · No open shifts: passed · Recognition run complete: passed'
```

#### Permissions

- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff
- `getWalletLiability` → `WALLET_VIEW` (read) · staff
- `getWalletMovementSummary` → `WALLET_VIEW` (read) · staff
- `getWalletPreCloseChecks` → `WALLET_VIEW` (read) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1170` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1170`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 14: Works in Wallet Financial Period & Closing Controls → Support controlled month-end and financial-period processing for wallet balances. Period Status Open → Closing → Under Review → Closed → Reopened with Authorization Pre-Close Validation Unreconciled …

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1170?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1171` Wallet Analytics & Management Reporting

**Provide comprehensive analytics for wallet usage, financial performance and customer behavior. Requirement 4.3.17 requires intensive reporting across wallet credit types, including usage, balance and expiry, while 4.3.33 calls for dashboards covering balances, top-ups, redemptions, refunds, outstanding liability, expired value, usage by channel and transaction volume. Financial Analytics Wallet Liability Outstanding Stored Value Funding Redemption Refunds Transfers Expired Value Breakage Gift Card Liability Operational Analytics Active wallets Average wallet balance Average top-up Average spend Transaction volume Wallet usage frequency Dormant wallets Credit utilization Channel Analytics**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare; Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-analytics-management-reporting-bo-1171` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet analytics: usage, balances and behaviour by credit type.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getWalletLiability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getWalletLiability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#getWalletLiability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet analytics reporting** (data table)

| Shows | Format | Notes |
|---|---|---|
| POS | text | not in the schema: `POS` |
| Mobile app | text | not in the schema: `Mobile App` |
| B2 c | text | not in the schema: `B2C` |
| Kiosk | text | not in the schema: `Kiosk` |
| Wearables | text | not in the schema: `Wearables` |
| API | text | not in the schema: `API` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Attractions | text | not in the schema: `Attractions` |
| Customer analytics | text | not in the schema: `Customer Analytics` |
| Individual | text | not in the schema: `Individual` |
| Family | text | not in the schema: `Family` |
| Membership | text | not in the schema: `Membership` |
| Corporate | text | not in the schema: `Corporate` |
| Employee | text | not in the schema: `Employee` |
| Guest | text | not in the schema: `Guest` |
| AI insights | text | not in the schema: `AI Insights` |

**The selected wallet analytics reporting** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| POS | text | not in the schema: `POS` |
| Mobile app | text | not in the schema: `Mobile App` |
| B2 c | text | not in the schema: `B2C` |
| Kiosk | text | not in the schema: `Kiosk` |
| Wearables | text | not in the schema: `Wearables` |
| API | text | not in the schema: `API` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Attractions | text | not in the schema: `Attractions` |
| Customer analytics | text | not in the schema: `Customer Analytics` |
| Individual | text | not in the schema: `Individual` |
| Family | text | not in the schema: `Family` |
| Membership | text | not in the schema: `Membership` |
| Corporate | text | not in the schema: `Corporate` |
| Employee | text | not in the schema: `Employee` |
| Guest | text | not in the schema: `Guest` |
| AI insights | text | not in the schema: `AI Insights` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **analytics**: KPI cards and trends. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `getWalletLiability` (onLoad, Management reporting)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet analytics reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet analytics reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet analytics reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet analytics reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  activeWallets: 18420
  avgBalance: AED 118.60
```

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1171` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1171`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 16: Works in Wallet Analytics & Management Reporting → Provide comprehensive analytics for wallet usage, financial performance and customer behavior. Requirement 4.3.17 requires intensive reporting across wallet credit types, including usage, balance and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1171?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1172` Finance Validation, Reporting & Audit Center

**Provide a final finance-control screen for validating wallet financial integrity and reviewing all financial configuration changes. Finance Health Check Complete the TICVAI Wallet module with the enterprise integration and governance layer that allows Wallet to operate securely across the entire TICVAI ecosystem and with approved third-party platforms. This board covers Wallet APIs, integration profiles, event/webhook orchestration, synchronization, integration monitoring, access/security governance, configuration versioning, approval and publication, audit governance, and end-to-end platform health. It directly addresses requirements 4.3.20 and 4.3.34, while consolidating governance and administration capabilities required across the full wallet scope. The source specifically requires integration with internal and external systems through APIs, including balance inquiry, transaction history, wallet funding, wallet payment, refund processing and wallet-to-wallet transfers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW`, `WALLET_VIEW` (1 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | `periodId` (navigation) |
| Route | `/orders-money/finance-validation-reporting-audit-center-bo-1172` |

**What the spec says about it.** **Reconciliation is daily, per venue** (decided 2 October 2026, Chinmay; CHG-FIN-009; audit R110 (b)). The unit of work and of sign-off is one venue-day: POS cash, gateway settlements, bank and wallet against the ledger for that day. A longer range reviews days already reconciled; a provider's monthly file (DI-268) is matched day by day.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The finance controls centre (DI-277): one place that shows the transactions and balances with exceptions or variances needing review, proves that wallet balances, the wallet sub-ledger, the general ledger and the acquirer agree, and moves the period through submit and approve. Get right: the person who submits the close is never the one who approves it, and every check names what to fix.

**Known correction pending (do not draw the wrong version)**

- **"Run Finance Validation" is mapped to getUnifiedReconciliation; the contract's validation is the dry-run close, which returns the failed checks.** Why: A reconciliation read does not tell the user whether the period can close. *(source: screens/P08-venue-back-office.yaml#BO-1172 / contracts/spine/finance.yaml#closeFiscalPeriod / MATRIX 5.7.89; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Approve Close" is mapped to closeFiscalPeriod, but that operation raises an approval request to a different finance approver and returns with the period still closing; the approval is decided in approvals.** Why: A button labelled Approve that only requests approval misleads, and invites self-approval. *(source: contracts/spine/finance.yaml#closeFiscalPeriod / R144; Finance, Ledger & Tax · Reporting & Analytics)*
- **The table's column list includes "against", a fragment of the pack sentence, as a column.** Why: Parsing artefact. *(source: screens/P08-venue-back-office.yaml#BO-1172; Finance, Ledger & Tax · Reporting & Analytics)*
- **The purpose carries board 10's integration-governance text (APIs, webhooks, synchronisation) after "Finance Health Check".** Why: Page bleed from the pack; this screen is the finance health check only. *(source: screens/P08-venue-back-office.yaml#BO-1172; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which approval inbox does the finance approver use to decide a period close?** → Drawn default stands (answer: "The approvals inbox, with a deep link to the close checks"): The approvals inbox, with a deep link back to this screen showing the checks. *(decided by Chinmay, 2026-10-02; DEC-221 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |
| Legal entity | picker: choose a legal entity | — | — | `listFiscalPeriods` ?legalEntityId |
| Status | segmented control | — | Open · Closing · Closed | `listFiscalPeriods` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **period**: Arrives with the period from navigation; otherwise the oldest period that is open or closing. *(source: contracts/spine/finance.yaml#listFiscalPeriods)*

#### Outputs: what the screen shows and produces

**Shown**

**Every finance validation reporting** (data table)

| Shows | Format | Notes |
|---|---|---|
| Sum of customer wallet balances | text | not in the schema: `Sum of Customer Wallet Balances` |
| Against | text | not in the schema: `against` |
| Wallet sub ledger liability | text | not in the schema: `Wallet Sub-Ledger Liability` |
| Finance interface control total | text | not in the schema: `Finance Interface Control Total` |
| Configuration audit | text | not in the schema: `Configuration Audit` |

**The selected finance validation reporting** (detail panel): The pack groups this record's detail under its own headings: “Validate”, “Record changes to”, “For every change record”, “So we now have”, “Administration”.

| Shows | Format | Notes |
|---|---|---|
| Sum of customer wallet balances | text | not in the schema: `Sum of Customer Wallet Balances` |
| Against | text | not in the schema: `against` |
| Wallet sub ledger liability | text | not in the schema: `Wallet Sub-Ledger Liability` |
| Finance interface control total | text | not in the schema: `Finance Interface Control Total` |
| Configuration audit | text | not in the schema: `Configuration Audit` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run Finance Validation (primary button) | navigation or local | — | — | — | — |
| Review Exceptions (secondary button) | navigation or local | — | — | — | — |
| Submit Close (secondary button) | navigation or local | — | — | — | — |
| Approve Close (secondary button) | navigation or local | — | — | — | — |
| Generate Liability Report (secondary button) | navigation or local | — | — | — | — |
| Generate Reconciliation Report (secondary button) | navigation or local | — | — | — | — |
| Export Audit (secondary button) | navigation or local | — | — | — | — |
| Send to Finance (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **finance health check**: Three tie-outs, each with a tick or the difference: customer wallet balances vs wallet sub-ledger liability; wallet sub-ledger vs general ledger; general ledger vs acquirer. A difference names the pair, the amount, the transactions involved and the likely cause. *(source: contracts/satellite/wallet.yaml#/components/schemas/WalletReconciliation / DI-277)*
- **money sources vs ledger**: POS, gateway, bank, wallet and ledger totals with each named variance, same layout as BO-1081's strip. *(source: contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation)*
- **close checks**: The seven close checks with pass, or the blocking count and a link to the screen that fixes it. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult / MATRIX 5.7.89)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run checks**: Runs the close checks without locking anything and lists what fails. It changes nothing, so no confirmation. *(source: contracts/spine/finance.yaml#closeFiscalPeriod / MATRIX 5.7.89)*
- **Begin close**: Confirmation "Postings to September stop now. Sales continue and post to October." The period moves to Closing. *(source: contracts/spine/finance.yaml#beginPeriodClose / F13 step 4)*
- **Request approval to close**: Runs the checks; if they pass, an approval request goes to a finance approver who is not the caller and the period stays Closing with "Awaiting approval from …". If a check fails, the failed checks are listed and nothing is sent. *(source: contracts/spine/finance.yaml#closeFiscalPeriod / R144)*
- **Generate liability report**: The wallet liability by credit type, age band and venue as at period end, exportable. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `getWalletReconciliation` (onLoad, Validation and audit); `listFiscalPeriods` (onLoad, The fiscal periods to begin closing or close)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The finance validation reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the finance validation reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No finance validation reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the finance validation reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period is already `closed`, or one or more of the close checks failed. The checks are exactly the values of `PeriodCloseResult.checks[].check` … (PeriodCloseProblem); 409 The period is not `open`. |

#### Edge cases to draw

- **the user has wallet view but not ledger approval**: Tie-outs visible; Begin close and Request approval are absent, with "Needs ledger approval access" in their place. *(source: contracts/spine/finance.yaml#beginPeriodClose / contracts/satellite/wallet.yaml#getWalletReconciliation / DI-387)*
- **the approver is on leave at month end**: The request follows the approver's time-bounded delegation; the screen shows the delegate's name. *(source: F13 step 3)*
- **a trial balance that does not balance**: The close stops and is abandoned with a reason; the period reopens for posting. *(source: F13 step 5)*

#### Consistency with other screens

- Match `BO-090 Period Close`: Same three verbs (Begin close, Request approval, Reopen period) and the same check names; F13 runs there.
- Match `BO-1170`: The liability figure here equals that screen's closing liability.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
period: September 2026 · Aquaventure Leisure LLC · Closing
tieOuts:
- Customer wallet balances AED 1,224,850.00 vs wallet sub-ledger AED 1,224,850.00 · tied
- Wallet sub-ledger vs general ledger · tied
- Wallet sub-ledger vs acquirer · short AED 2,450.00 · 3 top-ups captured 30 Sep, credited 1 Oct (timing)
checks: Settlements reconciled · 2 exceptions open (Stripe, 29 Sep) · Fix in Daily Reconciliation
approval: Requested by Omar Haddad 1 Oct 10:12 · awaiting Fatima Al Mansoori
```

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff
- `beginPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `closeFiscalPeriod` → `LEDGER_APPROVE` (operate) · staff
- `getWalletLiability` → `WALLET_VIEW` (read) · staff
- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.89 | The system shall support fiscal year management, fiscal periods, month-end and year-end closing. Authorized users shall be able to open, close, lock, unlock, and re-open accounting periods with … | F&B & Guest Management | CONTRACTED | `closeFiscalPeriod` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1172` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1172`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 18: Works in Finance Validation, Reporting & Audit Center → Provide a final finance-control screen for validating wallet financial integrity and reviewing all financial configuration changes. Finance Health Check

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1172?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run Finance Validation, Review Exceptions, Submit Close, Approve Close, Generate Liability Report, Generate Reconciliation Report, Export Audit, Send to Finance.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_VIEW`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustWallet": {"method":"POST","path":"/wallets/{subjectId}/adjust","contract":"wallet","summary":"Manually adjust a wallet balance","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"beginPeriodClose": {"method":"POST","path":"/fiscal-periods/{periodId}/begin-close","contract":"finance","summary":"Begin closing a period","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FiscalPeriod"},
"closeFiscalPeriod": {"method":"POST","path":"/fiscal-periods/{periodId}/close","contract":"finance","summary":"Close a period and lock postings","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PeriodCloseResult"},
"getUnifiedReconciliation": {"method":"GET","path":"/reconciliation/unified","contract":"finance","summary":"Every money source against the ledger, in one view","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"UnifiedReconciliation"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"getWalletMovementSummary": {"method":"GET","path":"/wallet-movement-summary","contract":"wallet","summary":"How the stored-value balance moved over a period","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletMovementSummary"},
"getWalletPreCloseChecks": {"method":"GET","path":"/wallet-pre-close-checks","contract":"wallet","summary":"The wallet's checks before a period closes","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"periodEnd","in":"query","required":true}],"requestBody":null,"responds":"WalletPreCloseCheck"},
"getWalletReconciliation": {"method":"GET","path":"/wallet-reconciliation","contract":"wallet","summary":"The wallet sub-ledger against the general ledger and the acquirer","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"WalletReconciliation"},
"listFiscalPeriods": {"method":"GET","path":"/fiscal-periods","contract":"finance","summary":"List fiscal periods","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setWalletAccountingMapping": {"method":"PUT","path":"/wallet-accounting","contract":"wallet","summary":"Which ledger account each credit type sits in","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletAccountingMapping","responds":"WalletAccountingMapping"},
"setWalletReconciliationSources": {"method":"PUT","path":"/wallet-reconciliation-sources","contract":"wallet","summary":"Which sources the wallet reconciles against, matched how, and when","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletReconciliationSources","responds":"WalletReconciliationSources"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"FiscalPeriod": {"x-ticvai-persistence":"ledger.fiscal_period + ledger.fiscal_period_event","type":"object","description":"`startDate` and `endDate` are days in the region's time zone: a posting belongs to the period when its `postedAt`, in that zone, falls on or between them.\n","required":["id","legalEntityId","name","startDate","endDate","status"],"properties":{"id":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"name":{"type":"string"},"startDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"endDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"status":{"$ref":"#/components/schemas/PeriodStatus"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"closedAt":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approval request a close or reopen is waiting on (`approvals`), routed to a finance approver (decided 28 September, audit R144). Null when nothing is waiting."},"events":{"type":"array","description":"**Every step of the period's close, oldest first**: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. A reopened period restates figures somebody has already reported, so the reason is kept, not just the latest status.\n","items":{"$ref":"#/components/schemas/FiscalPeriodEvent"}}}},
"FiscalPeriodEvent": {"type":"object","description":"One step in a fiscal period's close. Written by the operation that took the step; never edited.","required":["action","principalId","occurredAt"],"properties":{"action":{"type":"string","enum":["beginClose","abandonClose","close","reopen"]},"reason":{"type":"string","nullable":true,"description":"Required by `abandonPeriodClose` and `reopenPeriod`; null for the other steps."},"principalId":{"type":"string","format":"uuid","description":"Who took the step."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The approver of a `reopen`. Null for the other steps."},"occurredAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PeriodCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","dryRun","passed","checks"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"passed":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["trialBalanceBalances","noUnapprovedJournals","noOpenShifts","settlementsReconciled","recognitionRunComplete","priorPeriodClosed","varianceExceptionsReviewed"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}},"walletChecks":{"type":"array","description":"**The wallet pre-close checks** (decided 2 October 2026, Chinmay, batch 6 #220, BO-1170; DEC-220; CHG-CSP-040). Beside `checks`, whose values clients built at r1 already switch on, so no value is added there. `passed` is false while any of these fails. Empty where the tenant has no wallet module.","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["walletRollForwardTies","walletLiabilityMatchesLedger","noPendingWalletAuthorisations","expiredBalancesReleased","walletDisputesReviewed"],"description":"`walletRollForwardTies`: opening liability plus top-ups, minus spend, refunds and expiry, equals closing liability. `walletLiabilityMatchesLedger`: that closing liability equals the wallet liability account. `noPendingWalletAuthorisations`: no authorisation is still held open in the period. `expiredBalancesReleased`: balances past expiry were released to breakage. `walletDisputesReviewed`: no wallet dispute raised in the period is unreviewed."},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}},"walletRollForward":{"type":"object","nullable":true,"description":"**The period's wallet movement summary, as the close checked it** (DEC-220; CHG-CSP-040): read from wallet `getWalletMovementSummary` so BO-1170 shows the roll-forward beside the ledger checks. Null where the tenant has no wallet module.","properties":{"openingLiability":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"toppedUp":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"spent":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expired":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closingLiability":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerLiability":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The wallet liability account's balance, to compare with `closingLiability`."}}}}},
"PeriodStatus": {"type":"string","enum":["open","closing","closed"]},
"UnifiedReconciliation": {"type":"object","description":"4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n","properties":{"from":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"to":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"sources":{"type":"array","items":{"type":"object","properties":{"source":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]},"providerName":{"type":"string","nullable":true},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionCount":{"type":"integer"}}}},"variances":{"type":"array","description":"**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n","items":{"type":"object","properties":{"between":{"type":"array","description":"The two sources that disagree, as named in `sources[].source`.","minItems":2,"maxItems":2,"items":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"likelyCause":{"type":"string","nullable":true}}}}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletAccountingMapping": {"type":"object","x-ticvai-persistence":"wallet.accounting_mapping","description":"Boards 9.2 and 9.3. **Different credit types are different liabilities.**","properties":{"mappings":{"type":"array","items":{"type":"object","properties":{"creditTypeId":{"type":"string","format":"uuid"},"liabilityAccountCode":{"type":"string"},"breakageRevenueAccountCode":{"type":"string","nullable":true},"costAccountCode":{"type":"string","nullable":true,"description":"**For credit the venue gave away.** Promotional credit is a marketing cost already incurred, not money owed back, and booking it as a liability overstates what the venue owes by whatever marketing did last quarter.\n"}}}},"breakagePolicy":{"type":"object","properties":{"recogniseAfterMonths":{"type":"integer","nullable":true,"description":"**Recognised on a policy, not on the expiry date.** Some jurisdictions require the liability to be held long after the printed expiry.\n"},"requiresApproval":{"type":"boolean","default":true}}},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}},
"WalletMovementSummary": {"type":"object","x-ticvai-persistence":"none — aggregated from wallet.transaction and wallet.credit_lot","description":"One row of the wallet roll-forward (`getWalletMovementSummary`, CHG-CSA-027). Every amount is in the base currency.","properties":{"groupKey":{"type":"string","nullable":true},"opening":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"topUps":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundsIn":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transfersIn":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustmentsIn":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"spend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transfersOut":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustmentsOut":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundsOut":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expired":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closing":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tiesOut":{"type":"boolean","description":"Opening plus every movement equals closing."}}},
"WalletPreCloseCheck": {"type":"object","x-ticvai-persistence":"none — computed at the call","description":"One wallet check before a period closes (`getWalletPreCloseChecks`, CHG-CSA-027).","properties":{"code":{"type":"string","enum":["rollForwardTies","subLedgerTiesToLedger","noExpiredHoldsOpen","noPendingExpiryRun","noOverdueDisputes","reconciliationSourcesMatched"]},"outcome":{"type":"string","enum":["pass","warn","fail"]},"detail":{"type":"string"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true}}},
"WalletReconciliation": {"type":"object","description":"Board 9.4. **Three sources, and the exception names which pair disagrees.**","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"subLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"generalLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptions":{"type":"array","items":{"type":"object","properties":{"pair":{"type":"string","enum":["subLedgerVsGeneralLedger","subLedgerVsAcquirer","generalLedgerVsAcquirer"]},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"likelyCause":{"type":"string","nullable":true}}}}}},
"WalletReconciliationSources": {"type":"object","x-ticvai-persistence":"wallet.reconciliation_source","description":"Board 9, p.105. **What `getWalletReconciliation` compares.** `walletLedger` is always on.","required":["sources"],"properties":{"sources":{"type":"array","minItems":1,"items":{"type":"object","required":["kind","enabled"],"properties":{"kind":{"type":"string","enum":["walletLedger","pos","paymentGateway","paymentServer","giftCard","finance"]},"enabled":{"type":"boolean","default":true},"matchKeys":{"type":"array","description":"Fields a movement is matched on, e.g. transactionId, authorisationCode, terminalId, amount, businessDate.","items":{"type":"string"}},"toleranceAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A pair differing by no more than this is agreed. Default zero."},"schedule":{"type":"string","enum":["realTime","hourly","daily","endOfBusinessDay"],"default":"endOfBusinessDay"}}}},"scopePath":{"type":"string"}}}
}
```
