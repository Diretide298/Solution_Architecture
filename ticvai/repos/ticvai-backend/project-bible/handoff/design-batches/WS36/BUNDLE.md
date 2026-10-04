# WS36 — Pricing   Revenue Management board 3

**9 screens · 20 operations · 24 schemas · 6 permissions**

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
  `LEDGER_POST, LEDGER_VIEW, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, TAX_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-069` | Tax Profile & Jurisdiction Configuration | A | 64 | 16 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-070` | Tax Rule & Treatment Builder | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-071` | Fee & Surcharge Library | B | 30 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-072` | Fee Applicability & Charging Rule Builder | B | 5 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-073` | Fee Waiver, Tax Exemption & Exception Rules | B | 11 | 0 | 5 | 0 | 1 | 4 | — | notStarted (generated) |
| `ADM-074` | Price Calculation Sequence & Formula Engine | B | 25 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-075` | Currency Precision, Rounding & Monetary Rules | B | 11 | 2 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `ADM-076` | Price Breakdown, Calculation Simulation & Explainability | B | 13 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-077` | Calculation Validation, Reconciliation & Service Interface | A | 10 | 24 | 6 | 1 | 0 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-069` Tax Profile & Jurisdiction Configuration

**Set this venue's tax profile (one per venue: tax type, jurisdiction, rate, base, legal entity and registration, effective dates) and, for the legal entity it invoices under, the invoice templates and the e-invoicing connection.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 1 · needs the `ticketing` module |
| Block | Block A · task APP-SETUP-ADM-069 |
| Who uses it | venue staff holding `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TAX_CONFIGURE` (2 read, 2 configure); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): The venue's tax profile in one form, with the picked legal entity's invoice templates and e-invoicing beside it (defined 4 October 2026, CHG-FXS-001). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/tax-profile-jurisdiction-configuration-adm-069` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home. **Taxable base: one setting, here** (decided 2 October 2026, Chinmay; CHG-FIN-004). It was set in two places, the tax profile (`TaxProfile.taxBase`) and a venue policy flag on the tax calculation (`discountsAreTaxInclusive`), which could disagree; the flag is deprecated and ignored. The setting shows the Egypt worked example. **Tax documents** (CHG-FIN-011): the template sets the title the law prescribes, the auto-issue of the simplified tax invoice (on for a UAE registrant), and the AED 10,000 limit above which a VAT-registered buyer gets a full tax invoice. **Defined 4 October 2026: one tax profile per venue, read and saved as one record (Chinmay's default of 3 October: one tax-profile read, a list only if the design needs it); the legal entities come from listLegalEntities, which fills the invoice-template and e-invoicing calls and tells whether the entity is UAE VAT-registered** (CHG-FXS-001)

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Define reusable tax profiles per legal entity, country and jurisdiction: tax type, rate, where the profile applies, and the taxable base, including the region-configurable rule that tax is charged on the price before discount (Egypt). Also where the invoice templates, number series and e-invoicing connection are set. The one thing to get right: a rate or base change is a new, future-dated version; transactions already made keep the version they were calculated with.

**Known correction pending (do not draw the wrong version)**

- **Every field is drawn as a select, including name, registration number and dates.** Why: Text and date inputs; selects only for type, country, level and status. *(source: screens/P08-venue-back-office.yaml#ADM-069; Finance, Ledger & Tax · Reporting & Analytics)*
- **Five tax types are action buttons with no operation.** Why: They are values of one tax-type list (eight values, VAT and GST included). *(source: screens/P08-venue-back-office.yaml#ADM-069 / contracts/spine/catalogue.yaml#setTaxProfileJurisdiction; Finance, Ledger & Tax · Reporting & Analytics)*
- **The taxable base, rate, jurisdiction level and applicability are missing from the layout.** Why: The taxable base is the field that implements tax on the pre-discount price; without it the 1 September rule cannot be configured. *(source: DI-598 / contracts/spine/catalogue.yaml#setTaxProfileJurisdiction; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen declares no read of existing profiles.** Why: Its "as saved" state has nothing to load; the profile list is read by the command centre's list operation. *(source: screens/P08-venue-back-office.yaml#ADM-069 / contracts/spine/catalogue.yaml#listTaxFeeCalculation; Finance, Ledger & Tax · Reporting & Analytics)*
- **Saving a tax profile is gated by the product-configuration permission at venue scope.** Why: The permission set has a tax-configuration right, used by the finance tax operations; a tax profile is a legal setting. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction / contracts/shared/permissions.yaml#/components/schemas/Permission; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who configures tax profiles: platform staff in the console under a grant, or the client's finance team?** → Drawn default accepted: The client's finance team enters rates and registrations (the contract says so); platform staff only under a grant. *(decided by Chinmay, 2026-10-02; DEC-078 / CHG-NOTE-003)*
- **Is the VAT receipt issued automatically on every paid order?** → Drawn default accepted: On for UAE legal entities (the template default is off). *(decided by Chinmay, 2026-10-02; DEC-079 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tax profile name | text field | optional | — | — | — | Tax Profile Name | `TaxProfileJurisdictionConfigurationInput.taxProfileName` |
| Tax profile code | text field | optional | — | — | — | Tax Profile Code | `TaxProfileJurisdictionConfigurationInput.taxProfileCode` |
| Tax type | select | optional | — | VAT · Gst · Sales tax · Entertainment tax · Tourism tax · Municipality tax · Service tax · Custom regulatory tax | — | VAT, sales, entertainment, tourism, municipality, service or another regulatory tax. | `TaxProfileJurisdictionConfigurationInput.taxType` |
| Rate (%) | number field | optional | — | — | — | Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule | `TaxProfileJurisdictionConfigurationInput.ratePercent` |
| Country | text field | optional | — | pattern `^[A-Z]{2}$` | — | Country: ISO 3166-1 alpha-2 code | `TaxProfileJurisdictionConfigurationInput.country` |
| Jurisdiction level | segmented control | optional | — | Country · Region · Municipality | — | Jurisdiction Hierarchy (p.41): the level this profile applies at | `TaxProfileJurisdictionConfigurationInput.jurisdictionLevel` |
| Jurisdiction | text field | optional | — | — | — | Region/Jurisdiction | `TaxProfileJurisdictionConfigurationInput.jurisdiction` |
| Legal entity | text field | optional | — | — | — | Options from listLegalEntities. | `TaxProfileJurisdictionConfigurationInput.legalEntity` |
| Tax registration number | text field | optional | — | — | — | Prefilled from the legal entity's TRN. | `TaxProfileJurisdictionConfigurationInput.taxRegistrationNumber` |
| Taxable base | segmented control | optional | — | Discounted price · Pre discount price | — | Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. | `TaxProfileJurisdictionConfigurationInput.taxBase` |
| Effective from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective From; new structures are future-dated and never change historical transactions | `TaxProfileJurisdictionConfigurationInput.effectiveFrom` |
| Effective to | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective To; empty for open-ended | `TaxProfileJurisdictionConfigurationInput.effectiveTo` |
| Invoicing legal entity | picker: choose an id | optional | — | — | shows names, sends the id | A UAE VAT registrant is a legal entity with countryCode AE and a taxRegistrationNumber. | `LegalEntity.id` |
| Document title | key and value settings | optional | — | — | — | Per language. In the UAE fixed by law: Tax Invoice, Simplified Tax Invoice. | `FinTaxInvoiceTemplate.title` |
| Number prefix | text field | optional | — | max length 20 | — | e.g. `INV-`, `SINV-`, `CN-`. | `FinTaxInvoiceTemplate.numberPrefix` |
| Issue a tax invoice on every paid order | toggle | optional | off | 59(13)(1)); a template for such an entity saved with this false is refused 422 `tax-invoice-required`. | — | On and locked for a UAE VAT-registered legal entity. | `FinTaxInvoiceTemplate.autoIssueOnPayment` |
| E-invoicing mode | segmented control | optional | — | Disabled · Test · Live | — | — | `FinEInvoicingProvider.mode` |
| Provider name | text field | optional | — | max length 200 | — | The accredited service provider the client appoints. | `FinEInvoicingProvider.providerName` |
| Participant id | text field | optional | — | max length 100 | — | The legal entity's Peppol participant identifier. | `FinEInvoicingProvider.participantId` |
| Credential reference | text area | optional | — | max length 300 | — | A reference to the secret in the vault; the secret is never stored here. | `FinEInvoicingProvider.credentialRef` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoiceTemplates` ?legalEntityId |
| Tax profile | picker: choose a tax profile | — | — | `getTaxProfileJurisdiction` ?taxProfileId |

**Sent by *Save tax profile*** (`setTaxProfileJurisdiction`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tax profile name `taxProfileName` | text field | optional | — | — | — | Tax Profile Name | `setTaxProfileJurisdiction` body |
| Tax profile code `taxProfileCode` | text field | optional | — | — | — | Tax Profile Code | `setTaxProfileJurisdiction` body |
| Tax type `taxType` | select | optional | — | VAT · Gst · Sales tax · Entertainment tax · Tourism tax · Municipality tax · Service tax · Custom regulatory tax | — | Tax Type (pp.40-41) | `setTaxProfileJurisdiction` body |
| Country `country` | text field | optional | — | pattern `^[A-Z]{2}$` | — | Country: ISO 3166-1 alpha-2 code | `setTaxProfileJurisdiction` body |
| Jurisdiction `jurisdiction` | text field | optional | — | — | — | Region/Jurisdiction | `setTaxProfileJurisdiction` body |
| Legal entity `legalEntity` | text field | optional | — | — | — | Legal Entity | `setTaxProfileJurisdiction` body |
| Tax registration number `taxRegistrationNumber` | text field | optional | — | — | — | Tax Registration Number | `setTaxProfileJurisdiction` body |
| Currency `currency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | Currency: ISO 4217 code | `setTaxProfileJurisdiction` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective From; new structures are future-dated and never change historical transactions | `setTaxProfileJurisdiction` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective To; empty for open-ended | `setTaxProfileJurisdiction` body |
| Status `status` | text field | optional | — | — | — | Status: draft, active, inactive or expired | `setTaxProfileJurisdiction` body |
| Owner `owner` | text field | optional | — | — | — | Owner | `setTaxProfileJurisdiction` body |
| Rate percent `ratePercent` | number field | optional | — | — | — | Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule | `setTaxProfileJurisdiction` body |
| Tax profile `taxProfileId` | text field | optional | — | — | — | Tax profile ID; empty on create | `setTaxProfileJurisdiction` body |
| Jurisdiction level `jurisdictionLevel` | segmented control | optional | — | Country · Region · Municipality | — | Jurisdiction Hierarchy (p.41): the level this profile applies at | `setTaxProfileJurisdiction` body |
| Applicability `applicability` | repeatable rows | optional | — | — | — | Applicability (p.41): where the profile applies; a channel only where legally applicable | `setTaxProfileJurisdiction` body |
| Level `applicability[].level` | select | optional | — | Legal entity · Country · Market · Venue · Product category · Product · Service · Channel | — | — | `setTaxProfileJurisdiction` body |
| Ref `applicability[].refId` | text field | optional | — | — | — | — | `setTaxProfileJurisdiction` body |
| Tax base `taxBase` | segmented control | optional | — | Discounted price · Pre discount price | — | Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. | `setTaxProfileJurisdiction` body |

**Sent by *Save template*** (`setTaxInvoiceTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Legal entity `legalEntityId` | picker: choose a legal entity | required | — | — | shows names, sends the id | — | `setTaxInvoiceTemplate` body |
| Document kind `documentKind` | segmented control | required | — | Tax invoice · Simplified tax invoice · Credit memo | — | — | `setTaxInvoiceTemplate` body |
| Number prefix `numberPrefix` | text field | required | — | max length 20 | — | e.g. `INV-`, `SINV-`, `CN-`. | `setTaxInvoiceTemplate` body |
| Resets yearly `resetsYearly` | toggle | optional | on | — | — | A new series per fiscal year of the legal entity. | `setTaxInvoiceTemplate` body |
| Next number `nextNumber` | number field | optional | — | min 1 | — | May be raised, never lowered below the last number issued. | `setTaxInvoiceTemplate` body |
| Number padding `numberPadding` | stepper or slider | optional | 6 | min 1; max 12 | — | — | `setTaxInvoiceTemplate` body |
| Languages `languages` | list of values (chips) | required | — | at least 1 | — | Rendered on one page in this order, e.g. `en`, `ar`. | `setTaxInvoiceTemplate` body |
| Title `title` | key and value settings | optional | — | — | — | The document title per language. Prescribed wording is law (CF-133, answered by research 2 October 2026, CHG-FIN-011): in the UAE "Tax Invoice" for both `taxInvoice` and … | `setTaxInvoiceTemplate` body |
| Footer text `footerText` | key and value settings | optional | — | — | — | — | `setTaxInvoiceTemplate` body |
| Logo `logoAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setTaxInvoiceTemplate` body |
| Layout key `layoutKey` | text field | optional | — | max length 64 | — | — | `setTaxInvoiceTemplate` body |
| Auto issue on payment `autoIssueOnPayment` | toggle | optional | off | 59(13)(1)); a template for such an entity saved with this false is refused 422 `tax-invoice-required`. | — | For `simplifiedTaxInvoice`, issue one on every paid order (the VAT receipt). Always on for a UAE VAT-registered legal entity (research 2 October 2026, CHG-FIN-011): a registrant … | `setTaxInvoiceTemplate` body |
| Simplified allowed up to `simplifiedAllowedUpTo` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | For a VAT-registered recipient only: the consideration up to which a simplified invoice is still allowed (UAE AED 10,000, Executive Regulation Art. | `setTaxInvoiceTemplate` body |
| Show legal currency tax `showLegalCurrencyTax` | toggle | optional | on | — | — | Show the tax in the legal entity's currency when the invoice currency differs. | `setTaxInvoiceTemplate` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setTaxInvoiceTemplate` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setTaxInvoiceTemplate` body |

**Sent by *Save e-invoicing*** (`setEInvoicingProvider`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Legal entity `legalEntityId` | picker: choose a legal entity | required | — | — | shows names, sends the id | — | `setEInvoicingProvider` body |
| Provider name `providerName` | text field | required | — | max length 200 | — | The accredited service provider the client appoints. | `setEInvoicingProvider` body |
| Endpoint URL `endpointUrl` | URL field | optional | — | — | https:// | — | `setEInvoicingProvider` body |
| Test endpoint URL `testEndpointUrl` | URL field | optional | — | — | https:// | — | `setEInvoicingProvider` body |
| Credential ref `credentialRef` | text area | optional | — | max length 300 | — | A reference to the secret in the vault; the secret is never stored here. | `setEInvoicingProvider` body |
| Participant `participantId` | text field | optional | — | max length 100 | — | The legal entity's Peppol participant identifier. | `setEInvoicingProvider` body |
| Document format `documentFormat` | segmented control | optional | Pint ae | Pint ae | — | — | `setEInvoicingProvider` body |
| Mode `mode` | segmented control | required | — | Disabled · Test · Live | — | — | `setEInvoicingProvider` body |
| Transmit within hours `transmitWithinHours` | number field (hours) | optional | — | min 1 | — | — | `setEInvoicingProvider` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Tax type**: One select: VAT, GST, Sales tax, Entertainment tax, Tourism tax, Municipality tax, Service tax, Custom regulatory tax. Not five buttons. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Rate**: Percent (e.g. 5 for UAE VAT); empty when the tax is a fixed amount set on the tax rule. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Taxable base**: Discounted price (default) or Price before discount. Explain with a live example under the control: >- "AED 100 ticket, 20% off: guest pays AED 80; VAT is charged on AED 100". *(source: DI-598 / contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Jurisdiction level and applicability**: Country, region or municipality; applies to legal entity, country, market, venue, product category, product, service or channel (a channel only where legally applicable). Multiple applicability rows allowed. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Effective from / to**: Dates, not selects. From must be in the future for a change to an active profile; empty "to" means open-ended. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Tax registration number, legal entity, currency**: Text and pick lists; currency follows the legal entity. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Invoice template (per legal entity and document kind)**: Number prefix (INV-, SINV-, CN-), yearly reset, next number (may be raised, never lowered below the last issued), padding, languages in order (en, ar), title per language (prescribed wording is law), footer, logo, "issue a VAT receipt on every paid order", the amount up to which a simplified receipt is allowed, show tax in the legal currency. *(source: contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceTemplate)*
- **E-invoicing provider**: Provider name, endpoint and test endpoint, credential reference (never the secret), participant id, format, mode Disabled / Test / Live, transmit-within hours. *(source: contracts/spine/finance.yaml#/components/schemas/FinEInvoicingProvider)*

#### Outputs: what the screen shows and produces

**Shown**

**Tax profile in force** (detail panel, from `getTaxProfileJurisdiction`)

| Shows | Format | Notes |
|---|---|---|
| Tax profile name | text | Tax Profile Name |
| Tax type | chip: VAT, Gst, Sales tax, Entertainment tax, Tourism tax, Municipality tax… | Tax Type (pp.40-41) |
| Rate percent | 1,234.5 | Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule |
| Jurisdiction | text | Region/Jurisdiction |
| Effective from | 1 Oct 2026 | Effective From; new structures are future-dated and never change historical transactions |
| Consuming product count | 1,234 | Dependencies: products using the profile; read-only |

**Invoice templates** (data table, from `listTaxInvoiceTemplates`): Query legalEntityId the picked one.

| Shows | Format | Notes |
|---|---|---|
| Document kind | chip: Tax invoice, Simplified tax invoice, Credit memo | — |
| Number prefix | text | e.g. `INV-`, `SINV-`, `CN-`. |
| Next number | 1,234 | May be raised, never lowered below the last number issued. |
| Languages | list or chips (count when long) | Rendered on one page in this order, e.g. `en`, `ar`. |
| Auto issue on payment | yes / no (icon or chip) | For `simplifiedTaxInvoice`, issue one on every paid order (the VAT receipt). Always on for a UAE VAT-registered legal entity (research 2 … |
| Is active | yes / no (icon or chip) | — |

**E-invoicing** (detail panel, from `listEInvoicingProviders`)

| Shows | Format | Notes |
|---|---|---|
| Provider name | text | The accredited service provider the client appoints. |
| Mode | chip: Disabled, Test, Live | — |
| Participant | text | The legal entity's Peppol participant identifier. |
| Last accepted test at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save tax profile (primary button) | `setTaxProfileJurisdiction` PUT `/tax-profile-jurisdiction` | TaxProfileJurisdictionConfigurationInput | TaxProfileJurisdictionConfigurationView | — | — |
| Save template (secondary button) | `setTaxInvoiceTemplate` PUT `/tax-invoice-templates` | FinTaxInvoiceTemplate | FinTaxInvoiceTemplate | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `nextNumber` below the last number issued in the series, or a language the legal entity's region does not offer. | — |
| Save e-invoicing (secondary button) | `setEInvoicingProvider` PUT `/e-invoicing/providers` | FinEInvoicingProvider | FinEInvoicingProvider | 409 `live` requested before any `test` transmission from this legal entity was accepted. | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Dependencies**: "Used by 214 products at 3 venues", read-only, beside the profile; a change shows who it will affect from its effective date. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Worked preview**: Line-level preview of one sample basket: base, discount, taxable base, each tax in application order (tax on tax visible), rounding, payable. *(source: DI-596 / DI-598 / contracts/spine/finance.yaml#/components/schemas/TaxCalculation)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save profile**: Saves a new version from its effective date; the previous version stays for history. *(source: contracts/spine/catalogue.yaml#setTaxProfileJurisdiction)*
- **Switch e-invoicing to Live**: Only after a test document was accepted; until then Live is disabled with the reason. *(source: contracts/spine/finance.yaml#/components/schemas/FinEInvoicingProvider)*

**Data it reads**: `listTaxInvoiceTemplates` (onLoad, Show invoice templates and number series); `listEInvoicingProviders` (onLoad, Show the e-invoicing provider connection); `getTaxProfileJurisdiction` (onLoad, Load the tax profile and jurisdiction as saved); `listLegalEntities` (onLoad, The legal entities: the tax profile's entity, and the one …)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setTaxProfileJurisdiction`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The form with the venue's saved tax profile. |
| Error (`?state=error`) | Could not load. Names the read that failed; the form stays read-only until it loads. |
| Empty, first run (`?state=emptyFirstRun`) | No tax profile saved yet: the form is empty and Save creates it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listTaxInvoiceTemplates` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setTaxProfileJurisdiction` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `live` requested before any `test` transmission from this legal entity was accepted.; 422 `nextNumber` below the last number issued in the series, or a language the legal entity's region does not offer. |

#### Edge cases to draw

- **Two profiles apply to the same product and channel**: Flag the conflict before saving; the validation centre (ADM-077) lists it as overlapping. *(source: contracts/spine/catalogue.yaml#listCalculationValidationReconciliation)*
- **A three-decimal currency legal entity**: Preview and examples at three decimals (BHD 12.500 + VAT 10% = BHD 13.750). *(source: DI-306 / DI-598)*

#### Consistency with other screens

- Match `ADM-068`: The command centre lists these profiles and opens this screen to create or edit one.
- Match `BO-075`: The finance tax codes (rate, account, compounding) must carry the same names as these profiles.
- Match `POS-026`: Receipt and invoice layout comes from the template set here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- UAE VAT Standard · VAT · AE · federal · 5% · discounted price · Aquaventure Leisure LLC · TRN 100123456700003
  · from 1 Jan 2018
- 'Egypt VAT · VAT · EG · 14% · price before discount · Cairo Festival City venue · EGP 500.00 ticket, 20% off:
  pays EGP 400.00 + VAT EGP 70.00 = EGP 470.00'
- 'Dubai Tourism Dirham · Tourism tax · AE · municipality · fixed amount · venue: Atlantis Aquaventure'
template: 'SINV- · resets yearly · next 004813 · English + Arabic · VAT receipt on every paid order: on · simplified
  up to AED 10,000.00'
```

#### Permissions

- `setTaxProfileJurisdiction` → `PRODUCT_CONFIGURE` (configure) · staff
- `listTaxInvoiceTemplates` → `LEDGER_VIEW` (read) · staff
- `setTaxInvoiceTemplate` → `TAX_CONFIGURE` (configure) · staff
- `listEInvoicingProviders` → `LEDGER_VIEW` (read) · staff
- `setEInvoicingProvider` → `TAX_CONFIGURE` (configure) · staff
- `getTaxProfileJurisdiction` → `PRODUCT_VIEW` (read) · staff
- `listLegalEntities` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listTaxInvoiceTemplates` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setTaxProfileJurisdiction` …

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-069` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-069`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 2: Works in Tax Profile & Jurisdiction Configuration → Define reusable tax profiles according to legal entity, country, jurisdiction and commercial context.

#### Acceptance for the design

- [ ] Every input above is drawn (64), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-069?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save tax profile, Save template, Save e-invoicing.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TAX_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-070` Tax Rule & Treatment Builder

**Define how taxes are applied to products and transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-070 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/tax-rule-treatment-builder-adm-070` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Out of Scope, Fixed Tax. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How taxes apply: inclusive, exclusive, exempt, zero-rated or out of scope, by product, category, venue, country, transaction and customer type and channel; percentage, fixed, tiered, compound (tax on tax) or sequential; effective dates. Tax on the pre-discount price is a regional setting.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Product, category, venue, legal entity and customer type are strings. (CHG-MOV-008)
- No read operation: the screen declares only setTaxRuleTreatment and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Out of Scope, Fixed Tax. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **calculationMethod and taxes**: Compound and sequential methods show the order of taxes and a worked example ("AED 100 ticket, 20% off, taxed on AED 100"). *(source: contracts/spine/catalogue.yaml#setTaxRuleTreatment / DI-596 / DI-598)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Tax Inclusive (primary button) | navigation or local | — | — | — | — |
| Tax Exclusive (secondary button) | navigation or local | — | — | — | — |
| Tax Exempt (secondary button) | navigation or local | — | — | — | — |
| Out of Scope (secondary button) | navigation or local | — | — | — | — |
| Fixed Tax (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setTaxRuleTreatment`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tax rule treatment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tax rule treatment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tax rule treatment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tax rule treatment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: UAE VAT standard
  country: AE
  treatment: taxInclusive
  method: percentage
  rate: 5%
  from: '2026-01-01'
```

#### Permissions

- `setTaxRuleTreatment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-070` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-070`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 4: Works in Tax Rule & Treatment Builder → Define how taxes are applied to products and transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Tax Inclusive, Tax Exclusive, Tax Exempt, Out of Scope, Fixed Tax.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-071` Fee & Surcharge Library

**Create standardized reusable non-base-price charges.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-071 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure whether the fee is) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-surcharge-library-adm-071` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 18 actions on this screen; 8 are served since the writers pass (29 September): Booking Fee, Transaction Fee, Service Fee, Convenience Fee, Delivery Fee, Handling Fee, Modification …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The library of fees and surcharges (booking, convenience, delivery, change, cancellation, payment, channel, facility), each with how it computes, its tax treatment, refundability and visibility to the guest. When a fee applies is a separate rule (ADM-072).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fee Name | select field | — | — | — | — | — | — |
| Fee Code | select field | — | — | — | — | — | — |
| Fee Type | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Calculation Method | select field | — | — | — | — | — | — |
| Value | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Tax Treatment | select field | — | — | — | — | — | — |
| Refundability | select field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Customer Visible | select field | — | — | — | — | — | — |
| Included in Display Price | text field | — | — | — | — | — | — |
| Shown Separately | select field | — | — | — | — | — | — |
| Internal Only | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Fee type | select | — | Booking fee · Transaction fee · Service fee · Convenience fee · Delivery fee · Handling fee · Modification fee · Rescheduling fee · Cancellation fee · Refund fee · Payment fee · Channel fee … | `listFeeSurcharge` ?feeType |
| Status | radio group | — | Draft · Active · Inactive · Expired | `listFeeSurcharge` ?status |
| Search | text field | — | — | `listFeeSurcharge` ?search |

**Form: Save fee definition** (modal, opened by *Save fee definition*; *Save fee definition* calls `setFeeDefinition`, *Cancel* sends nothing)

**Collects what `setFeeDefinition` sends before it is called.** Required: `code`, `name`, `feeType`, `valueType`, `chargeBasis`, `status`. Optional: `description`, `amount`, `percentage`, `tiers`, `taxTreatment`, `refundability`, `visibility`, `effectiveFrom`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 40 | — | — | `setFeeDefinition` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFeeDefinition` body |
| Description `description` | text area | optional | — | — | — | — | `setFeeDefinition` body |
| Fee type `feeType` | select | required | — | Booking fee · Transaction fee · Service fee · Convenience fee · Delivery fee · Handling fee · Modification fee · Rescheduling fee · Cancellation fee · Refund fee · Payment fee · Channel fee … | — | — | `setFeeDefinition` body |
| Value type `valueType` | segmented control | required | — | Fixed amount · Percentage · Tiered | — | — | `setFeeDefinition` body |
| Charge basis `chargeBasis` | select | required | — | Per ticket · Per product · Per person · Per order · Per transaction · Per day | — | — | `setFeeDefinition` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setFeeDefinition` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `setFeeDefinition` body |
| Tiers `tiers` | key and value settings | optional | — | — | — | `[{fromOrderValue, amount, percentage}]` for `valueType: tiered`. | `setFeeDefinition` body |
| Tax treatment `taxTreatment` | text field | optional | — | max length 60 | — | How the fee is taxed; a `catalogue.tax_rule` may refine it. | `setFeeDefinition` body |
| Refundability `refundability` | segmented control | optional | Non refundable | Refundable · Non refundable | — | — | `setFeeDefinition` body |
| Visibility `visibility` | radio group | optional | Shown separately | Customer visible · Included in display price · Shown separately · Internal only | — | — | `setFeeDefinition` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setFeeDefinition` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setFeeDefinition` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setFeeDefinition` body |

Errors to draw in the form: 409 `changeRequestRequired`.; 422 `valueRequired`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **visibility**: Customer-visible, included in the displayed price, shown separately, or internal only, each with a preview of the guest's basket line. *(source: contracts/spine/catalogue.yaml#setFeeDefinition)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Booking Fee (primary button) | navigation or local | — | — | — | — |
| Transaction Fee (secondary button) | navigation or local | — | — | — | — |
| Service Fee (secondary button) | navigation or local | — | — | — | — |
| Convenience Fee (secondary button) | navigation or local | — | — | — | — |
| Delivery Fee (secondary button) | navigation or local | — | — | — | — |
| Handling Fee (secondary button) | navigation or local | — | — | — | — |
| Modification Fee (secondary button) | navigation or local | — | — | — | — |
| Rescheduling Fee (secondary button) | navigation or local | — | — | — | — |
| Save fee definition (secondary button) | `setFeeDefinition` PUT `/fees` | PricingFee | PricingFee | 409 `changeRequestRequired`.; 422 `valueRequired`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listFeeSurcharge` (onLoad, Fee & Surcharge Library)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listFeeSurcharge`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee surcharge configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee surcharge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee surcharge configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `changeRequestRequired`.; 422 `valueRequired`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fees:
- code: CC-CONV
  name: Call centre convenience fee
  type: convenienceFee
  value: AED 10.00 per order
  refundable: false
  visibility: shownSeparately
```

#### Permissions

- `listFeeSurcharge` → `PRODUCT_VIEW` (read) · staff
- `setFeeDefinition` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-071` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-071`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 6: Works in Fee & Surcharge Library → Create standardized reusable non-base-price charges.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-071?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Booking Fee, Transaction Fee, Service Fee, Convenience Fee, Delivery Fee, Handling Fee, Modification Fee, Rescheduling Fee, Save fee definition.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-072` Fee Applicability & Charging Rule Builder

**Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-072 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether fees can) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-applicability-charging-rule-builder-adm-072` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type …. Each needs … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read of the fee applicability and charging rules (setFeeApplicabilityCharging has no get).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When a fee applies: product, channel, venue, event, customer and transaction type, payment and delivery method, market, service action (new sale, change, cancel, refund, upgrade), order value and quantity ranges, delivery zones, and how it combines with other fees.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setFeeApplicabilityCharging and nothing that returns the current configuration. (CHG-WIR-027)
- Pack actions with no operation: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type …. (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Stack | select field | — | — | — | — | — | — |
| Replace | select field | — | — | — | — | — | — |
| Exclude Another Fee | select field | — | — | — | — | — | — |
| Apply Once | select field | — | — | — | — | — | — |
| Apply Per Item | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **deliveryDestinationZones**: Zones as chips (Dubai, Abu Dhabi, Ras Al Khaimah, international) with the fee per zone, calculated from the checkout address. *(source: contracts/spine/catalogue.yaml#setFeeApplicabilityCharging / DI-597)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product (primary button) | navigation or local | — | — | — | — |
| Product Category (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Customer Type (secondary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Transaction Type (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setFeeApplicabilityCharging`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee applicability charging configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee applicability charging untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee applicability charging configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  fee: Delivery fee
  action: newSale
  zones:
    Dubai: AED 15.00
    Abu Dhabi: AED 25.00
    International: AED 90.00
```

#### Permissions

- `setFeeApplicabilityCharging` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-072` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-072`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 8: Works in Fee Applicability & Charging Rule Builder → Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-072?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-073` Fee Waiver, Tax Exemption & Exception Rules

**Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-073 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-waiver-tax-exemption-exception-rules-adm-073` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver. Each needs an operation … Contract gap recorded 2 October 2026 (CHG-WIR-027): No write for fee waiver and tax exemption rules.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When a tax or fee is reduced, waived or exempted (per product, transaction or customer), and who may do it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver. (CHG-MOV-008)
- No write operation: a configuration screen (Fee Waiver, Tax Exemption & Exception Rules) declares only reads (listFeeWaiverTax). (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership Benefit | select field | — | — | — | — | — | — |
| Loyalty Tier | select field | — | — | — | — | — | — |
| Corporate Agreement | select field | — | — | — | — | — | — |
| B2B Contract | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Staff Role | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Service Recovery | select field | — | — | — | — | — | — |
| Operational Issue | select field | — | — | — | — | — | — |
| Legal Exemption | select field | — | — | — | — | — | — |
| Supervisor Override | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Exception type | select | — | Fee waiver · Fee reduction · Tax exemption · Zero rated tax · Complimentary transaction · Operational waiver · Contractual waiver | `listFeeWaiverTax` ?exceptionType |
| Eligibility basis | select | — | Membership benefit · Loyalty tier · Corporate agreement · B2B contract · Customer segment · Staff role · Promotion · Service recovery · Operational issue · Legal exemption · Supervisor override | `listFeeWaiverTax` ?eligibilityBasis |
| Status | radio group | — | Draft · Active · Inactive · Expired | `listFeeWaiverTax` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fee Waiver (primary button) | navigation or local | — | — | — | — |
| Fee Reduction (secondary button) | navigation or local | — | — | — | — |
| Tax Exemption (secondary button) | navigation or local | — | — | — | — |
| Zero-Rated Tax (secondary button) | navigation or local | — | — | — | — |
| Complimentary Transaction (secondary button) | navigation or local | — | — | — | — |
| Operational Waiver (secondary button) | navigation or local | — | — | — | — |
| Contractual Waiver (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **exemption rules**: Rule, what it waives, condition, approval needed. *(source: contracts/spine/catalogue.yaml#listFeeWaiverTax / DI-596)*

**Data it reads**: `listFeeWaiverTax` (onLoad, Fee Waiver, Tax Exemption & Exception Rules)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listFeeWaiverTax`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee waiver tax configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee waiver tax untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee waiver tax configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Diplomatic VAT exemption
  waives: VAT
  condition: valid exemption certificate
```

#### Permissions

- `listFeeWaiverTax` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-073` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-073`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 10: Works in Fee Waiver, Tax Exemption & Exception Rules → Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-073?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fee Waiver, Fee Reduction, Tax Exemption, Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-074` Price Calculation Sequence & Formula Engine

**Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-074 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each step should define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-calculation-sequence-formula-engine-adm-074` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The exact sequence from rate to payable amount: base rate, rules, discounts, fees, tax, rounding. Versioned, saved whole.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Input | select field | — | — | — | — | — | — |
| Formula | select field | — | — | — | — | — | — |
| Sequence | select field | — | — | — | — | — | — |
| Taxability | select field | — | — | — | — | — | — |
| Rounding | select field | — | — | — | — | — | — |
| Dependency | select field | — | — | — | — | — | — |
| Output | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Calculation profile | text field | — | — | `listPriceCalculationSequence` ?calculationProfileId |
| As of | date picker | — | — | `listPriceCalculationSequence` ?asOf |

**Form: Save price calculation policy** (modal, opened by *Save price calculation policy*; *Save price calculation policy* calls `setPriceCalculationPolicy`, *Cancel* sends nothing)

**Collects what `setPriceCalculationPolicy` sends before it is called.** Required: `code`, `name`, `status`. Optional: `isDefault`, `effectiveFrom`, `effectiveTo`, `steps`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 40 | — | — | `setPriceCalculationPolicy` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Version `version` | number field | required | — | min 1 | — | — | `setPriceCalculationPolicy` body |
| Is default `isDefault` | toggle | optional | off | — | — | — | `setPriceCalculationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPriceCalculationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPriceCalculationPolicy` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setPriceCalculationPolicy` body |
| Steps `steps` | repeatable rows | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Calculation profile `steps[].calculationProfileId` | picker: choose a calculation profile | required | — | — | shows names, sends the id | — | `setPriceCalculationPolicy` body |
| Sequence `steps[].sequence` | number field | required | — | min 1 | — | — | `setPriceCalculationPolicy` body |
| Step type `steps[].stepType` | select | required | — | Commercial base rate · Contextual rate selection · Dynamic pricing adjustment · Promotion discount · Package bundle adjustment · Fees surcharges · Tax calculation · Rounding · Final payable amount | — | — | `setPriceCalculationPolicy` body |
| Formula type `steps[].formulaType` | select | required | — | Fixed amount · Percentage · Percentage of base · Percentage of subtotal · Tiered · Conditional · Minimum · Maximum · Custom governed formula | — | — | `setPriceCalculationPolicy` body |
| Input `steps[].input` | text field | optional | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Formula `steps[].formula` | text field | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Depends on `steps[].dependsOn` | list of values (chips) | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Output `steps[].output` | text field | optional | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Taxability `steps[].taxability` | segmented control | optional | — | In tax base · Outside tax base | — | — | `setPriceCalculationPolicy` body |
| Rounding profile `steps[].roundingProfileId` | picker: choose a rounding profile | optional | — | — | shows names, sends the id | — | `setPriceCalculationPolicy` body |

Errors to draw in the form: 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **steps**: An ordered list of steps with drag to reorder and a running example basket showing the amount after each step. *(source: contracts/spine/catalogue.yaml#setPriceCalculationPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save price calculation policy (primary button) | `setPriceCalculationPolicy` PUT `/calculation-profiles` | CalculationProfile | CalculationProfile | 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceCalculationSequence` (onLoad, Price Calculation Sequence & Formula Engine)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listPriceCalculationSequence`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price calculation sequence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price calculation sequence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price calculation sequence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
steps:
- Base rate AED 295.00
- Resident -AED 45.00
- Promotion -10%
- Booking fee +AED 5.00
- VAT 5% (on pre-discount where regional)
- Round to 0.25
```

#### Permissions

- `listPriceCalculationSequence` → `PRODUCT_VIEW` (read) · staff
- `setPriceCalculationPolicy` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-074` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-074`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 12: Works in Price Calculation Sequence & Formula Engine → Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-074?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save price calculation policy.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-075` Currency Precision, Rounding & Monetary Rules

**Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-075 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/currency-precision-rounding-monetary-rules-adm-075` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Precision and rounding per currency the tenant sells in: decimal places (up to three, the third kept), display and calculation precision, method, the stage at which rounding happens, and the cash rounding increment. One profile per currency.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCurrencyPrecisionRounding return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Form: Save currency rounding rule** (modal, opened by *Save currency rounding rule*; *Save currency rounding rule* calls `setCurrencyRoundingRule`, *Cancel* sends nothing)

**Collects what `setCurrencyRoundingRule` sends before it is called.** Required: `currency`, `decimalPlaces`, `roundingMethod`, `roundingStage`, `status`. Optional: `code`, `name`, `minimumMonetaryUnit`, `displayPrecision`, `calculationPrecision`, `cashRoundingIncrement`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 40 | — | — | `setCurrencyRoundingRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setCurrencyRoundingRule` body |
| Currency `currency` | text field | required | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setCurrencyRoundingRule` body |
| Decimal places `decimalPlaces` | stepper or slider | required | — | min 0; max 3 | — | Up to three without rounding the third away (MoM 1 Sep 2026 §4.5). | `setCurrencyRoundingRule` body |
| Minimum monetary unit `minimumMonetaryUnit` | number field | optional | — | — | — | — | `setCurrencyRoundingRule` body |
| Display precision `displayPrecision` | stepper or slider | optional | — | min 0; max 4 | — | — | `setCurrencyRoundingRule` body |
| Calculation precision `calculationPrecision` | stepper or slider | optional | 4 | min 0; max 4 | — | — | `setCurrencyRoundingRule` body |
| Rounding method `roundingMethod` | select | required | — | Standard · Round up · Round down · Bankers · Nearest currency unit · Custom regulatory rule | — | — | `setCurrencyRoundingRule` body |
| Rounding stage `roundingStage` | radio group | required | — | Per item · Per tax · Per fee · Per line · At order total | — | — | `setCurrencyRoundingRule` body |
| Cash rounding increment `cashRoundingIncrement` | number field | optional | — | — | — | — | `setCurrencyRoundingRule` body |
| Status `status` | radio group | required | Active | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setCurrencyRoundingRule` body |

Errors to draw in the form: 422 `precisionBelowDecimals`.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **roundingStage**: Per item, per tax, per fee, per line, or at order total, each with a worked example of a three-line basket showing where the cents move. *(source: contracts/spine/catalogue.yaml#setCurrencyRoundingRule)*
- **cashRoundingIncrement**: For cash only (for example 0.25); card amounts are never rounded to it. *(source: contracts/spine/catalogue.yaml#/components/schemas/RoundingProfile)*

#### Outputs: what the screen shows and produces

**Shown**

**Every currency precision rounding** (data table, from `listCurrencyPrecisionRounding`)

| Shows | Format | Notes |
|---|---|---|
| 50 | text | not in the schema: `AED 199.50` |

**The selected currency precision rounding** (detail panel): The pack groups this record's detail under its own headings: “Calculated”, “Calculated Total”, “Cash Payable”, “The engine should ensure”, “Currency Conversion”.

| Shows | Format | Notes |
|---|---|---|
| 50 | text | not in the schema: `AED 199.50` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Round Down (primary button) | navigation or local | — | — | — | — |
| Save currency rounding rule (secondary button) | `setCurrencyRoundingRule` PUT `/rounding-profiles` | RoundingProfile | RoundingProfile | 422 `precisionBelowDecimals`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listCurrencyPrecisionRounding` (onLoad, Currency Precision, Rounding & Monetary Rules)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listCurrencyPrecisionRounding`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The currency precision rounding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the currency precision rounding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No currency precision rounding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the currency precision rounding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `precisionBelowDecimals`. |

#### Edge cases to draw

- **OMR or BHD**: Three decimals, displayed as "OMR 12.500"; a profile with fewer places than the region's scale is refused. *(source: ADR-0008 / DI-598)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- currency: AED
  decimalPlaces: 2
  method: standard
  stage: perLine
  cashIncrement: 0.25
- currency: OMR
  decimalPlaces: 3
  method: standard
  stage: atOrderTotal
```

#### Permissions

- `listCurrencyPrecisionRounding` → `PRODUCT_VIEW` (read) · staff
- `setCurrencyRoundingRule` → `PRICE_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-075` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-075`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 14: Works in Currency Precision, Rounding & Monetary Rules → Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-075?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Round Down, Save currency rounding rule.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-076` Price Breakdown, Calculation Simulation & Explainability

**Allow administrators to test the complete calculation before releasing configuration into production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block B · task VM-ADM-076 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-breakdown-calculation-simulation-explainability-adm-076` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): simulatePriceBreakdownCalculation is a PUT with no read of the calculation sequence it explains.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test the complete calculation before release and see why each line is what it is; compare channels side by side.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only simulatePriceBreakdownCalculation and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Timeslot | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Payment Method | select field | — | — | — | — | — | — |
| Delivery Method | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **explained breakdown**: Same breakdown component as BO-1049. *(source: contracts/spine/catalogue.yaml#simulatePriceBreakdownCalculation)*

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `simulatePriceBreakdownCalculation`
- → `BO-100` Venue Home: *Back to Venue Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price breakdown calculation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price breakdown calculation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price breakdown calculation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1049`: Same operation and breakdown.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  Website: AED 501.50
  Point of sale: AED 527.00
```

#### Permissions

- `simulatePriceBreakdownCalculation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-076` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-076`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 16: Works in Price Breakdown, Calculation Simulation & Explainability → Allow administrators to test the complete calculation before releasing configuration into production.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-076?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation.
- [ ] Every transition is wired: `ADM-068`, `BO-100`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-077` Calculation Validation, Reconciliation & Service Interface

**Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it. Boards 1–3 established the commercial and calculation engines: Board 1: What prices exist? Board 2: Which price applies? Board 3: How is the final payable amount calculated?**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 1 · needs the `ticketing` module |
| Block | Block A · task APP-SETUP-ADM-077 |
| Who uses it | venue staff holding `LEDGER_POST`, `LEDGER_VIEW`, `PRODUCT_VIEW` (1 operate, 2 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Validation findings and test results listed and filtered, with the e-invoicing connection and its transmission log beside them (defined 4 October 2026, CHG-FXS-001). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/calculation-validation-reconciliation-service-interface-adm-077` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. Its board's hub ADM-068 stays on the console (DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates); this screen keeps that edge and is also reached from BO-100 Venue Home. **Defined 4 October 2026 from CalculationValidationReconciliationServiceInterfaceView, FinEInvoicingProvider and FinEInvoiceTransmission, with the legal entity picked from listLegalEntities for the transmission log and a resend** (CHG-FXS-001)

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The last check before pricing and tax changes go live: configuration findings (missing profiles, invalid rates, overlapping rules, rounding problems) and the results of stored test scenarios, each compared against expected totals. It also records which e-invoices were sent, accepted or failed. The one thing to get right: a critical finding blocks progress, so critical items are first and say exactly what to fix.

**Known correction pending (do not draw the wrong version)**

- **The screen has a blank table and unlabelled buttons, and its gaps say the pack gives nothing to draw.** Why: The 29 September close-out defined the rows (findings and scenario results with expected against actual totals); the layout should be rebuilt from that shape. *(source: screens/P08-venue-back-office.yaml#ADM-077 / contracts/spine/catalogue.yaml#listCalculationValidationReconciliation; Finance, Ledger & Tax · Reporting & Analytics)*
- **Nothing runs the test suite or re-validates; the screen only lists results.** Why: The pack's regression run before major changes has no trigger operation on this screen. *(source: contracts/spine/catalogue.yaml#listCalculationValidationReconciliation; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Area | select | optional | — | Tax · Fees · Formula · Currency · Reconciliation · Test suite | — | Filter: tax, fees, formula, currency, reconciliation, test suite. | `CalculationValidationReconciliationServiceInterfaceView.area` |
| Severity | segmented control | optional | — | Critical · Warning · Information | — | Severity; critical blocks progress | `CalculationValidationReconciliationServiceInterfaceView.severity` |
| Legal entity | picker: choose an id | optional | — | — | shows names, sends the id | — | `LegalEntity.id` |
| Status | select | optional | — | Not required · Queued · Sent · Accepted · Rejected · Failed | — | 6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent. | `FinEInvoiceTransmission.status` |
| Issued from | date picker | — | — | — | — | Body issuedFrom; with Issued to, resends every document of the legal entity in the window. | — |
| Issued to | date picker | — | — | — | — | Body issuedTo. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Result kind | segmented control | — | Validation finding · Test scenario result | `listCalculationValidationReconciliation` ?resultKind |
| Area | select | — | Tax · Fees · Formula · Currency · Reconciliation · Test suite | `listCalculationValidationReconciliation` ?area |
| Severity | segmented control | — | Critical · Warning · Information | `listCalculationValidationReconciliation` ?severity |
| Passed | toggle | — | — | `listCalculationValidationReconciliation` ?passed |
| Legal entity | picker: choose a legal entity | — | — | `listEInvoiceTransmissions` ?legalEntityId |
| Status | select | — | Not required · Queued · Sent · Accepted · Rejected · Failed | `listEInvoiceTransmissions` ?status |
| Document | picker: choose a document | — | — | `listEInvoiceTransmissions` ?documentId |

**Sent by *Send to e-invoicing*** (`transmitEInvoices`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Legal entity `legalEntityId` | picker: choose a legal entity | required | — | — | shows names, sends the id | — | `transmitEInvoices` body |
| Documents `documentIds` | multi-picker: choose documents | optional | — | — | — | Tax invoice or credit memo ids. Omit to send everything issued in the range and not yet `accepted`. | `transmitEInvoices` body |
| Issued from `issuedFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `transmitEInvoices` body |
| Issued to `issuedTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `transmitEInvoices` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Filters**: Findings or scenario results; area (Tax, Fees, Formula, Currency, Reconciliation, Test suite); severity; passed or failed. *(source: contracts/spine/catalogue.yaml#listCalculationValidationReconciliation)*

#### Outputs: what the screen shows and produces

**Shown**

**Findings and test results** (data table, from `listCalculationValidationReconciliation`): Critical first. A test scenario row shows passed or failed with its reconciliation.

| Shows | Format | Notes |
|---|---|---|
| Result kind | chip: Validation finding, Test scenario result | A configuration finding or a test-suite scenario result |
| Area | chip: Tax, Fees, Formula, Currency, Reconciliation, Test suite | Validation Area (p.52) |
| Code | chip: Missing profile, Invalid rate, Expired rule, Overlapping rule, Duplicate fee … | What was checked |
| Severity | chip: Critical, Warning, Information | Severity; critical blocks progress |
| Message | text | What was found |
| Scenario name | text | Test scenario name |
| Passed | yes / no (icon or chip) | Scenario passed; empty for a finding |
| Calculation version | text | Calculation version the result was produced with (Historical Reproducibility) |

**The selected result** (detail panel, from `listCalculationValidationReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Message | text | What was found |
| Subject | text | The profile, rule, fee, formula or currency concerned |
| Scenario type | chip: Standard B2C sale, POS sale, Member sale, Group booking, B2B sale, Refund… | Test Suite scenario type (pp.52-53) |
| Reconciliation | grouped details | Reconciliation (p.52): expected against actual totals for a scenario |

**E-invoicing connection** (data table, from `listEInvoicingProviders`)

| Shows | Format | Notes |
|---|---|---|
| Legal entity | the name it points at, never the id | — |
| Provider name | text | The accredited service provider the client appoints. |
| Mode | chip: Disabled, Test, Live | — |
| Document format | chip: Pint ae | — |
| Last accepted test at | 1 Oct 2026, 14:30 | — |

**Transmissions** (data table, from `listEInvoiceTransmissions`)

| Shows | Format | Notes |
|---|---|---|
| Document number | text | — |
| Document kind | chip: Tax invoice, Credit memo | — |
| Mode | chip: Test, Live | — |
| Status | chip: Not required, Queued, Sent, Accepted, Rejected, Failed | 6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent. |
| Attempt | 1,234 | — |
| Error message | text | — |
| Sent at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send to e-invoicing (primary button) | `transmitEInvoices` POST `/e-invoicing/transmissions` | inline | inline | 409 The legal entity has no provider, or its provider is `disabled`. | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Findings**: Severity, area, what was checked in words (Missing tax profile, Invalid rate, Overlapping rule, Rounding difference…), the message, and a link to the profile, rule or currency concerned. Critical first. *(source: contracts/spine/catalogue.yaml#/components/schemas/CalculationValidationReconciliationServiceInterfaceView)*
- **Scenario results**: Scenario (standard web sale, POS sale, member sale, group booking, B2B sale, refund, reschedule, multi-product order, package sale, multi-currency sale), passed or failed, and expected against actual for line, tax, fee, discount and final totals, with the difference highlighted; the calculation version used. *(source: contracts/spine/catalogue.yaml#/components/schemas/CalculationValidationReconciliationServiceInterfaceView)*
- **E-invoice transmissions**: Document, status (Queued, Sent, Accepted, Rejected, Failed), attempts, provider message; failed and rejected first. *(source: contracts/spine/finance.yaml#/components/schemas/FinEInvoiceTransmissionStatus)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Resend e-invoices**: Queues the selected failed or rejected documents again. *(source: contracts/spine/finance.yaml#transmitEInvoices)*

**Data it reads**: `listCalculationValidationReconciliation` (onLoad, Calculation Validation, Reconciliation & Service Interface); `listEInvoicingProviders` (onLoad, Show the e-invoicing provider connection); `listEInvoiceTransmissions` (onLoad, E-invoicing transmission log and failures); `listLegalEntities` (onLoad, The legal entities whose documents are transmitted)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-068` Tax, Fee & Calculation Command Center: *Tax, Fee & Calculation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No findings: every check passed. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filters. Names them and offers to clear them. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listCalculationValidationReconciliation` requires to show this screen, and names that permission (the screen's other reads need `LEDGER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_POST` for `transmitEInvoices`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The legal entity has no provider, or its provider is `disabled`. |

#### Edge cases to draw

- **A rounding difference of one fil on a scenario**: Shown as a failure with the exact difference (AED 0.01); never hidden by display rounding. *(source: contracts/spine/catalogue.yaml#/components/schemas/CalculationValidationReconciliationServiceInterfaceView)*
- **A critical finding exists**: A banner "Changes cannot be published until 1 critical issue is fixed". *(source: contracts/spine/catalogue.yaml#listCalculationValidationReconciliation)*

#### Consistency with other screens

- Match `ADM-068`: "Validate configuration" on the command centre opens this screen.
- Match `ADM-069`: Findings link back to the profile to fix.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
findings:
- Critical · Tax · Overlapping rule · 'UAE VAT Standard' and 'Free zone 0%' both apply to Retail at Beach Shop
- Warning · Currency · Invalid precision · BHD price list has 2 decimals
scenarios:
- POS sale · passed · total AED 728.00 = AED 728.00 · version calc-2026.10.01-3
- Package sale · failed · tax expected AED 34.67, actual AED 34.68 · difference AED 0.01
```

#### Permissions

- `listCalculationValidationReconciliation` → `PRODUCT_VIEW` (read) · staff
- `listEInvoicingProviders` → `LEDGER_VIEW` (read) · staff
- `listEInvoiceTransmissions` → `LEDGER_VIEW` (read) · staff
- `transmitEInvoices` → `LEDGER_POST` (operate) · staff, service
- `listLegalEntities` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listCalculationValidationReconciliation` requires to show this screen, and names that permission (the screen's other reads need `LEDGER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_POST` for `transmitEInvoices`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.1 | The system should share all transactions and receipts generated in the system with the external e-invoicing solution. | Retail POS | CONTRACTED_PARTIAL | `transmitEInvoices` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-077` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-077`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 18: Works in Calculation Validation, Reconciliation & Service Interface → Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it. Boards 1–3 established the commercial and calculation engines …
- ADR-0062 *E-invoicing goes through a provider adapter, and a rejection stops for a person* (`docs/adr/0062-e-invoicing-through-a-provider-adapter.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send to e-invoicing.
- [ ] Every transition is wired: `BO-100`, `ADM-068`.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getTaxProfileJurisdiction": {"method":"GET","path":"/tax-profile-jurisdiction","contract":"catalogue","summary":"The tax profile and jurisdiction configuration as saved","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"taxProfileId","in":"query","required":false}],"requestBody":null,"responds":"TaxProfileJurisdictionConfigurationView"},
"listCalculationValidationReconciliation": {"method":"GET","path":"/calculation-validation-reconciliation","contract":"catalogue","summary":"Calculation Validation, Reconciliation & Service Interface","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resultKind","in":"query","required":false},{"name":"area","in":"query","required":false},{"name":"severity","in":"query","required":false},{"name":"passed","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCurrencyPrecisionRounding": {"method":"GET","path":"/currency-precision-rounding","contract":"catalogue","summary":"Currency Precision, Rounding & Monetary Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CurrencyPrecisionRoundingMonetaryRulesView"},
"listEInvoiceTransmissions": {"method":"GET","path":"/e-invoicing/transmissions","contract":"finance","summary":"What was sent to the e-invoicing provider, and what came back","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"documentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEInvoicingProviders": {"method":"GET","path":"/e-invoicing/providers","contract":"finance","summary":"The e-invoicing service provider connection per legal entity","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFeeSurcharge": {"method":"GET","path":"/fee-surcharge","contract":"catalogue","summary":"Fee & Surcharge Library","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"feeType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFeeWaiverTax": {"method":"GET","path":"/fee-waiver-tax","contract":"catalogue","summary":"Fee Waiver, Tax Exemption & Exception Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"exceptionType","in":"query","required":false},{"name":"eligibilityBasis","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLegalEntities": {"method":"GET","path":"/legal-entities","contract":"finance","summary":"List legal entities","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceCalculationSequence": {"method":"GET","path":"/price-calculation-sequence","contract":"catalogue","summary":"Price Calculation Sequence & Formula Engine","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"calculationProfileId","in":"query","required":false},{"name":"asOf","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoiceTemplates": {"method":"GET","path":"/tax-invoice-templates","contract":"finance","summary":"Invoice and credit memo templates and number series, per legal entity","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setCurrencyRoundingRule": {"method":"PUT","path":"/rounding-profiles","contract":"catalogue","summary":"Set precision and rounding for a currency","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoundingProfile","responds":"RoundingProfile"},
"setEInvoicingProvider": {"method":"PUT","path":"/e-invoicing/providers","contract":"finance","summary":"Connect a legal entity to its accredited e-invoicing service provider","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinEInvoicingProvider","responds":"FinEInvoicingProvider"},
"setFeeApplicabilityCharging": {"method":"PUT","path":"/fee-applicability-charging","contract":"catalogue","summary":"Fee Applicability & Charging Rule Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FeeApplicabilityChargingRuleBuilderInput","responds":"FeeApplicabilityChargingRuleBuilderView"},
"setFeeDefinition": {"method":"PUT","path":"/fees","contract":"catalogue","summary":"Create or update a fee or surcharge","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingFee","responds":"PricingFee"},
"setPriceCalculationPolicy": {"method":"PUT","path":"/calculation-profiles","contract":"catalogue","summary":"Save a price calculation sequence, whole","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CalculationProfile","responds":"CalculationProfile"},
"setTaxInvoiceTemplate": {"method":"PUT","path":"/tax-invoice-templates","contract":"finance","summary":"Set a legal entity's template and number series for one document kind","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinTaxInvoiceTemplate","responds":"FinTaxInvoiceTemplate"},
"setTaxProfileJurisdiction": {"method":"PUT","path":"/tax-profile-jurisdiction","contract":"catalogue","summary":"Tax Profile & Jurisdiction Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxProfileJurisdictionConfigurationInput","responds":"TaxProfileJurisdictionConfigurationView"},
"setTaxRuleTreatment": {"method":"PUT","path":"/tax-rule-treatment","contract":"catalogue","summary":"Tax Rule & Treatment Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxRuleTreatmentBuilderInput","responds":"TaxRuleTreatmentBuilderView"},
"simulatePriceBreakdownCalculation": {"method":"PUT","path":"/price-breakdown-calculation","contract":"catalogue","summary":"Price Breakdown, Calculation Simulation & Explainability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceBreakdownCalculationSimulationExplainabilityInput","responds":"PriceBreakdownCalculationSimulationExplainabilityView"},
"transmitEInvoices": {"method":"POST","path":"/e-invoicing/transmissions","contract":"finance","summary":"Send issued tax documents to the e-invoicing provider","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CalculationProfile": {"type":"object","x-ticvai-persistence":"catalogue.calculation_profile + catalogue.calculation_step","description":"**The ordered sequence that turns a rate into a payable amount** (29 September, data model DM3). ADM-074: base rate, contextual rate, dynamic adjustment, promotion, package adjustment, fees, tax, rounding, final amount. Versioned; a calculation records the version it used (`calculationVersion`), so history is reproducible.","required":["id","scopePath","code","name","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"version":{"type":"integer","minimum":1},"isDefault":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/CalculationStep"}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CalculationStep": {"type":"object","x-ticvai-persistence":"catalogue.calculation_step","description":"**One step of a calculation profile** (29 September, data model DM3). `dependsOn` names earlier steps; a cycle or a step depending on a later one is refused (`422 circularDependency` / `invalidSequence`).","required":["id","calculationProfileId","sequence","stepType","formulaType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"calculationProfileId":{"type":"string","format":"uuid"},"sequence":{"type":"integer","minimum":1},"stepType":{"type":"string","enum":["commercialBaseRate","contextualRateSelection","dynamicPricingAdjustment","promotionDiscount","packageBundleAdjustment","feesSurcharges","taxCalculation","rounding","finalPayableAmount"]},"formulaType":{"type":"string","enum":["fixedAmount","percentage","percentageOfBase","percentageOfSubtotal","tiered","conditional","minimum","maximum","customGovernedFormula"]},"input":{"type":"string","maxLength":200,"nullable":true},"formula":{"type":"string","nullable":true},"dependsOn":{"type":"array","items":{"type":"string"}},"output":{"type":"string","maxLength":200,"nullable":true},"taxability":{"type":"string","enum":["inTaxBase","outsideTaxBase",null],"nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true}}},
"CalculationValidationReconciliationServiceInterfaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Calculation Validation, Reconciliation & Service Interface displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"resultId":{"type":"string","description":"Result ID"},"resultKind":{"type":"string","enum":["validationFinding","testScenarioResult"],"description":"A configuration finding or a test-suite scenario result"},"area":{"type":"string","enum":["tax","fees","formula","currency","reconciliation","testSuite"],"description":"Validation Area (p.52)"},"code":{"type":"string","enum":["missingProfile","invalidRate","expiredRule","overlappingRule","duplicateFee","conflictingRule","missingTaxTreatment","circularDependency","invalidSequence","missingInput","invalidPrecision","unsupportedCurrency","roundingDifference","reconciliationMismatch","scenarioFailed"],"description":"What was checked"},"severity":{"type":"string","enum":["critical","warning","information"],"description":"Severity; critical blocks progress"},"message":{"type":"string","description":"What was found"},"subjectId":{"type":"string","nullable":true,"description":"The profile, rule, fee, formula or currency concerned"},"scenarioName":{"type":"string","nullable":true,"description":"Test scenario name"},"scenarioType":{"type":"string","enum":["standardB2cSale","posSale","memberSale","groupBooking","b2bSale","refund","reschedule","multiProductOrder","packageSale","multiCurrencySale"],"description":"Test Suite scenario type (pp.52-53)","nullable":true},"passed":{"type":"boolean","nullable":true,"description":"Scenario passed; empty for a finding"},"reconciliation":{"type":"object","nullable":true,"description":"Reconciliation (p.52): expected against actual totals for a scenario","properties":{"lineTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"taxTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"feeTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"discountTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"finalTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}},"calculationVersion":{"type":"string","description":"Calculation version the result was produced with (Historical Reproducibility)"}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"CurrencyPrecisionRoundingMonetaryRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Currency Precision, Rounding & Monetary Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"decimalPlaces":{"type":"integer","description":"Decimal Places of the currency, 0 to 3 (MoM 1 Sep §4.5)","minimum":0,"maximum":3},"minimumMonetaryUnit":{"type":"number","description":"Minimum Monetary Unit, e.g. 0.01, 0.001, 0.05"},"displayPrecision":{"type":"integer","description":"Display Precision: decimals shown","minimum":0,"maximum":3},"calculationPrecision":{"type":"integer","description":"Calculation Precision: decimals carried while calculating; at most 4, the scale Money is stored at (decided 29 September, readiness close-out)","minimum":0,"maximum":4},"roundingMethod":{"type":"string","enum":["standard","roundUp","roundDown","bankers","nearestCurrencyUnit","customRegulatoryRule"],"description":"Rounding Method (p.49)"},"ruleId":{"type":"string","description":"Currency rule ID"},"roundingStage":{"type":"string","enum":["perItem","perTax","perFee","perLine","atOrderTotal"],"description":"Rounding Stage (p.50): where rounding happens"},"cashRoundingIncrement":{"type":"number","nullable":true,"description":"Cash Rounding: increment cash totals round to (CHF 19.98 -> 20.00 at 0.05) while electronic payment keeps the exact total; empty for none"},"status":{"type":"string","description":"Status: active or inactive"}}},
"FeeApplicabilityChargingRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 5%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Fee Applicability & Charging Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue"},"event":{"type":"string","nullable":true,"description":"Condition: event"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type"},"membership":{"type":"string","nullable":true,"description":"Condition: membership product or tier"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type"},"paymentMethod":{"type":"string","nullable":true,"description":"Condition: payment method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Condition: delivery method"},"market":{"type":"string","nullable":true,"description":"Condition: market"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country"},"serviceAction":{"type":"string","enum":["newSale","modification","reschedule","cancellation","refund","upgrade"],"description":"Condition: service action (Action = Reschedule); empty for any","nullable":true},"rulePriority":{"type":"integer","description":"Rule Priority: the lower number is evaluated first"},"ruleId":{"type":"string","description":"Charging rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"feeId":{"type":"string","description":"The fee from the library (Screen 10.3.4, ADM-071) this rule charges"},"orderValueMin":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value at or above which the fee applies"},"orderValueMax":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"},"quantityMin":{"type":"integer","nullable":true,"description":"Condition: minimum quantity"},"quantityMax":{"type":"integer","nullable":true,"description":"Condition: maximum quantity"},"hoursBeforeEventMax":{"type":"integer","nullable":true,"description":"Condition: the event occurs within this many hours (reschedule within 48 hours)"},"deliveryDestinationZones":{"type":"array","items":{"type":"string"},"description":"Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"},"combination":{"type":"string","enum":["stack","replace","exclude"],"description":"Fee Combination (p.45): add to other fees, replace them, or exclude named fees"},"excludedFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees excluded or replaced when combination is exclude or replace"},"application":{"type":"string","enum":["applyOnce","applyPerItem"],"description":"Apply Once per order or Apply Per Item"},"onMatch":{"type":"string","enum":["stopProcessing","continueProcessing"],"description":"Stop or Continue Processing after this rule applies"},"mutualExclusionGroup":{"type":"string","nullable":true,"description":"Mutual Exclusion: rules sharing a group never apply together; empty for none"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FeeApplicabilityChargingRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee Applicability & Charging Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue"},"event":{"type":"string","nullable":true,"description":"Condition: event"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type"},"membership":{"type":"string","nullable":true,"description":"Condition: membership product or tier"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type"},"paymentMethod":{"type":"string","nullable":true,"description":"Condition: payment method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Condition: delivery method"},"market":{"type":"string","nullable":true,"description":"Condition: market"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country"},"serviceAction":{"type":"string","enum":["newSale","modification","reschedule","cancellation","refund","upgrade"],"description":"Condition: service action (Action = Reschedule); empty for any","nullable":true},"rulePriority":{"type":"integer","description":"Rule Priority: the lower number is evaluated first"},"ruleId":{"type":"string","description":"Charging rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"feeId":{"type":"string","description":"The fee from the library (Screen 10.3.4, ADM-071) this rule charges"},"orderValueMin":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value at or above which the fee applies"},"orderValueMax":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"},"quantityMin":{"type":"integer","nullable":true,"description":"Condition: minimum quantity"},"quantityMax":{"type":"integer","nullable":true,"description":"Condition: maximum quantity"},"hoursBeforeEventMax":{"type":"integer","nullable":true,"description":"Condition: the event occurs within this many hours (reschedule within 48 hours)"},"deliveryDestinationZones":{"type":"array","items":{"type":"string"},"description":"Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"},"combination":{"type":"string","enum":["stack","replace","exclude"],"description":"Fee Combination (p.45): add to other fees, replace them, or exclude named fees"},"excludedFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees excluded or replaced when combination is exclude or replace"},"application":{"type":"string","enum":["applyOnce","applyPerItem"],"description":"Apply Once per order or Apply Per Item"},"onMatch":{"type":"string","enum":["stopProcessing","continueProcessing"],"description":"Stop or Continue Processing after this rule applies"},"mutualExclusionGroup":{"type":"string","nullable":true,"description":"Mutual Exclusion: rules sharing a group never apply together; empty for none"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FeeSurchargeLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee & Surcharge Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"percentage":{"type":"number","nullable":true,"description":"Value in percent when the method is percentage (Online Service Fee 3%)"},"feeName":{"type":"string","description":"Fee Name"},"feeCode":{"type":"string","description":"Fee Code"},"feeType":{"type":"string","enum":["bookingFee","transactionFee","serviceFee","convenienceFee","deliveryFee","handlingFee","modificationFee","reschedulingFee","cancellationFee","refundFee","paymentFee","channelFee","facilityFee","surcharge","customFee"],"description":"Fee Type (p.43)"},"description":{"type":"string","description":"Description"},"valueType":{"type":"string","enum":["fixedAmount","percentage","tiered"],"description":"Calculation Method: how the value is expressed"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"taxTreatment":{"type":"string","nullable":true,"description":"Tax Treatment: the tax rule (ADM-070) applied to the fee; empty is flagged Missing Tax Treatment by validation"},"refundability":{"type":"string","enum":["refundable","nonRefundable"],"description":"Refundability when the order is refunded"},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"feeId":{"type":"string","description":"Fee ID"},"chargeBasis":{"type":"string","enum":["perTicket","perProduct","perPerson","perOrder","perTransaction","perDay"],"description":"What the value is charged per (Call Center Booking Fee AED 15 per order; Online Service Fee 3% per transaction)"},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Value when the method is fixedAmount"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"percentage":{"type":"number","nullable":true}}},"description":"Tiers when the method is tiered"},"visibility":{"type":"string","enum":["customerVisible","includedInDisplayPrice","shownSeparately","internalOnly"],"description":"Fee Visibility (p.44)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"FeeWaiverTaxExemptionExceptionRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee Waiver, Tax Exemption & Exception Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reasonRequired":{"type":"boolean","description":"Reason mandatory when the exception is applied"},"exemptionType":{"type":"string","nullable":true,"description":"Exemption Type for tax exemptions, e.g. diplomatic, charity (the client's list); empty for fee exceptions"},"ruleId":{"type":"string","description":"Exception rule ID"},"ruleName":{"type":"string","description":"Rule name"},"exceptionType":{"type":"string","enum":["feeWaiver","feeReduction","taxExemption","zeroRatedTax","complimentaryTransaction","operationalWaiver","contractualWaiver"],"description":"Exception Type (p.46)"},"targetFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees waived or reduced; empty for a tax exception"},"targetTaxProfileIds":{"type":"array","items":{"type":"string"},"description":"Tax profiles exempted or zero-rated; empty for a fee exception"},"reductionPercent":{"type":"number","nullable":true,"description":"Fee Reduction in percent; empty for a full waiver"},"reductionAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Fee Reduction as an amount; empty for a full waiver"},"eligibilityBasis":{"type":"string","enum":["membershipBenefit","loyaltyTier","corporateAgreement","b2bContract","customerSegment","staffRole","promotion","serviceRecovery","operationalIssue","legalExemption","supervisorOverride"],"description":"Eligibility Condition (p.46)"},"eligibilityRefId":{"type":"string","nullable":true,"description":"The membership tier, agreement, contract, segment, role or promotion that qualifies (Gold Member -> Booking Fee waived)"},"approvalRequired":{"type":"boolean","description":"Approval required before the exception takes effect"},"evidenceRequired":{"type":"boolean","description":"Tax Exemption Evidence must be captured (p.47)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FinEInvoiceTransmission": {"x-ticvai-persistence":"ledger.einvoice_transmission","type":"object","description":"6.1.1. One attempt to send one tax document to the provider, and its answer.","required":["id","documentKind","documentId","legalEntityId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentId":{"type":"string","format":"uuid"},"documentNumber":{"type":"string"},"legalEntityId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid","nullable":true},"mode":{"type":"string","enum":["test","live"]},"status":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"payloadHash":{"type":"string","nullable":true,"description":"SHA-256 of the document as sent, so a resend can be shown to be the same document."},"providerMessageId":{"type":"string","nullable":true},"attempt":{"type":"integer","minimum":1},"errorCodes":{"type":"array","items":{"type":"string"}},"errorMessage":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinEInvoicingProvider": {"x-ticvai-persistence":"ledger.einvoicing_provider","type":"object","description":"6.1.1. Also the `setEInvoicingProvider` body. One per legal entity.","required":["legalEntityId","providerName","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"legalEntityId":{"type":"string","format":"uuid"},"providerName":{"type":"string","maxLength":200,"description":"The accredited service provider the client appoints."},"endpointUrl":{"type":"string","format":"uri","nullable":true},"testEndpointUrl":{"type":"string","format":"uri","nullable":true},"credentialRef":{"type":"string","maxLength":300,"nullable":true,"description":"A reference to the secret in the vault; the secret is never stored here."},"participantId":{"type":"string","maxLength":100,"nullable":true,"description":"The legal entity's Peppol participant identifier."},"documentFormat":{"type":"string","enum":["pintAe"],"default":"pintAe"},"mode":{"type":"string","enum":["disabled","test","live"]},"transmitWithinHours":{"type":"integer","minimum":1,"nullable":true},"lastAcceptedTestAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"FinTaxInvoiceTemplate": {"x-ticvai-persistence":"ledger.tax_invoice_template","type":"object","description":"5.7.93, 5.7.94. Also the `setTaxInvoiceTemplate` body. One per legal entity and document kind.","required":["legalEntityId","documentKind","numberPrefix","languages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"legalEntityId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","simplifiedTaxInvoice","creditMemo"]},"numberPrefix":{"type":"string","maxLength":20,"description":"e.g. `INV-`, `SINV-`, `CN-`. The year is added by the series when `resetsYearly`."},"resetsYearly":{"type":"boolean","default":true,"description":"A new series per fiscal year of the legal entity."},"nextNumber":{"type":"integer","minimum":1,"description":"May be raised, never lowered below the last number issued."},"numberPadding":{"type":"integer","minimum":1,"maximum":12,"default":6},"languages":{"type":"array","minItems":1,"description":"Rendered on one page in this order, e.g. `en`, `ar`.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"title":{"type":"object","description":"The document title per language. **Prescribed wording is law** (CF-133, answered by research 2 October 2026, CHG-FIN-011): in the UAE \"Tax Invoice\" for both `taxInvoice` and `simplifiedTaxInvoice` (Executive Regulation Art. 59(1)(a), 59(2)(a)) and \"Tax Credit Note\" for `creditMemo` (Art. 60(1)(a)). Never \"Receipt\" or \"VAT receipt\" as the title; the Arabic title is the client's tax adviser's to confirm.","additionalProperties":{"type":"string"}},"footerText":{"type":"object","additionalProperties":{"type":"string"}},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"layoutKey":{"type":"string","maxLength":64,"nullable":true},"autoIssueOnPayment":{"type":"boolean","default":false,"description":"For `simplifiedTaxInvoice`, issue one on every paid order (the VAT receipt). **Always on for a UAE VAT-registered legal entity** (research 2 October 2026, CHG-FIN-011): a registrant making a taxable supply issues and delivers a tax invoice (Decree-Law Art. 65(1)), and a simplified one on the date of supply (Executive Regulation Art. 59(13)(1)); a template for such an entity saved with this false is refused 422 `tax-invoice-required`. The till prints it as the receipt (POS-026); the guest web and app show it on the order."},"simplifiedAllowedUpTo":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**For a VAT-registered recipient only**: the consideration up to which a simplified invoice is still allowed (UAE AED 10,000, Executive Regulation Art. 59(5)(b)). A recipient who is not registered may always get a simplified one (Art. 59(5)(a)). Above it, or where the reverse charge applies, the till and the back office offer the full invoice only (CHG-FIN-011)."},"showLegalCurrencyTax":{"type":"boolean","default":true,"description":"Show the tax in the legal entity's currency when the invoice currency differs."},"effectiveFrom":{"type":"string","format":"date"},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"LegalEntity": {"x-ticvai-persistence":"ledger.legal_entity","type":"object","description":"Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n","required":["id","code","name","countryCode","currency","currencyScale","fiscalYearStartMonth"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"taxRegistrationNumber":{"type":"string","nullable":true},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12},"regionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceBreakdownCalculationSimulationExplainabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Price Breakdown, Calculation Simulation & Explainability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"customerId":{"type":"string","nullable":true,"description":"Customer"},"productId":{"type":"string","description":"Product"},"quantity":{"type":"integer","description":"Quantity","minimum":1},"venueId":{"type":"string","nullable":true,"description":"Venue"},"eventId":{"type":"string","nullable":true,"description":"Event"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel"},"date":{"type":"string","format":"date","description":"Date of visit"},"timeslotId":{"type":"string","nullable":true,"description":"Timeslot"},"membershipId":{"type":"string","nullable":true,"description":"Membership"},"promotionCode":{"type":"string","nullable":true,"description":"Promotion"},"paymentMethod":{"type":"string","nullable":true,"description":"Payment Method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Delivery Method"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"compareChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"description":"Channel Comparison (p.51): run the same transaction through these channels too; empty for none"}}},
"PriceBreakdownCalculationSimulationExplainabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Breakdown, Calculation Simulation & Explainability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"finalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Payable"},"components":{"type":"array","items":{"type":"object","properties":{"sequence":{"type":"integer"},"componentType":{"type":"string","enum":["selectedRate","memberAdjustment","dynamicAdjustment","promotion","packageAdjustment","fee","surcharge","waiver","tax","rounding"]},"label":{"type":"string","description":"e.g. Booking Fee, VAT"},"source":{"type":"string","description":"Source: the price list, rule, fee or tax profile"},"rule":{"type":"string","description":"Rule: id of the rule applied, e.g. FE-021, TAX-UAE-01"},"formula":{"type":"string"},"input":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Input amount"},"output":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Output amount (negative for a reduction)"},"reason":{"type":"string"},"taxTreatment":{"type":"string","nullable":true}}},"description":"Explainability Panel and Rule Trace (p.51), in sequence"},"selectedRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Selected Rate x quantity"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discounts and adjustments total"},"feeTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees total"},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Subtotal before tax"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax total"},"calculationVersion":{"type":"string","description":"Calculation version used"},"channelComparison":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"finalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"type":"string","description":"Why it differs, e.g. Call Center Booking Fee"}}},"description":"Channel Comparison results"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"PriceCalculationSequenceFormulaEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Calculation Sequence & Formula Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"input":{"type":"string","description":"Input: the named value the step reads, e.g. subtotal"},"formula":{"type":"string","description":"Formula expression, governed"},"sequence":{"type":"integer","description":"Sequence: position in the pipeline"},"taxability":{"type":"string","enum":["inTaxBase","outsideTaxBase"],"description":"Taxability: whether this step's amount is part of the tax base; a discount outsideTaxBase gives tax on the pre-discount price where the region requires it (MoM 1 Sep §4.5)"},"rounding":{"type":"string","nullable":true,"description":"Rounding rule applied after the step (ADM-075); empty for none"},"dependsOn":{"type":"array","items":{"type":"string"},"description":"Dependency: steps whose output this step needs"},"output":{"type":"string","description":"Output: the named value the step produces"},"stepId":{"type":"string","description":"Step ID"},"calculationProfileId":{"type":"string","description":"Calculation profile the step belongs to"},"stepType":{"type":"string","enum":["commercialBaseRate","contextualRateSelection","dynamicPricingAdjustment","promotionDiscount","packageBundleAdjustment","feesSurcharges","taxCalculation","rounding","finalPayableAmount"],"description":"Pipeline stage (Recommended Calculation Pipeline, pp.47-48)"},"formulaType":{"type":"string","enum":["fixedAmount","percentage","percentageOfBase","percentageOfSubtotal","tiered","conditional","minimum","maximum","customGovernedFormula"],"description":"Formula Builder kind (p.48)"},"version":{"type":"string","description":"Formula version"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"PricingFee": {"type":"object","x-ticvai-persistence":"catalogue.fee","description":"**The fee and surcharge library** (29 September, data model DM3). ADM-071. What a fee is and how it computes; when it applies is `catalogue.fee_rule`. Distinct from `payments.fee_rule` (a provider's processing cost) and `orders.order_fee` (a fee as charged on one order).","required":["id","scopePath","code","name","feeType","valueType","chargeBasis","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"feeType":{"type":"string","enum":["bookingFee","transactionFee","serviceFee","convenienceFee","deliveryFee","handlingFee","modificationFee","reschedulingFee","cancellationFee","refundFee","paymentFee","channelFee","facilityFee","surcharge","customFee"]},"valueType":{"type":"string","enum":["fixedAmount","percentage","tiered"]},"chargeBasis":{"type":"string","enum":["perTicket","perProduct","perPerson","perOrder","perTransaction","perDay"]},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"percentage":{"type":"number","nullable":true,"minimum":0,"maximum":100},"tiers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{fromOrderValue, amount, percentage}]` for `valueType: tiered`."},"taxTreatment":{"type":"string","maxLength":60,"nullable":true,"description":"How the fee is taxed; a `catalogue.tax_rule` may refine it."},"refundability":{"type":"string","enum":["refundable","nonRefundable"],"default":"nonRefundable"},"visibility":{"type":"string","enum":["customerVisible","includedInDisplayPrice","shownSeparately","internalOnly"],"default":"shownSeparately"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RoundingProfile": {"type":"object","x-ticvai-persistence":"catalogue.rounding_profile","description":"**Precision and rounding for one currency** (29 September, data model DM3). ADM-075. One per currency the tenant sells in; the engine keeps line totals + tax + fees equal to the transaction total. Distinct from `payments.currency_rule` (settlement currency and payment limits). The currency here is the subject of the rule, not the denomination of an amount.","required":["id","scopePath","currency","decimalPlaces","roundingMethod","roundingStage","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"code":{"type":"string","maxLength":40,"nullable":true},"name":{"type":"string","maxLength":200,"nullable":true},"currency":{"type":"string","maxLength":3,"pattern":"^[A-Z]{3}$"},"decimalPlaces":{"type":"integer","minimum":0,"maximum":3,"description":"Up to three without rounding the third away (MoM 1 Sep 2026 §4.5)."},"minimumMonetaryUnit":{"type":"number","nullable":true},"displayPrecision":{"type":"integer","nullable":true,"minimum":0,"maximum":4},"calculationPrecision":{"type":"integer","minimum":0,"maximum":4,"default":4},"roundingMethod":{"type":"string","enum":["standard","roundUp","roundDown","bankers","nearestCurrencyUnit","customRegulatoryRule"]},"roundingStage":{"type":"string","enum":["perItem","perTax","perFee","perLine","atOrderTotal"]},"cashRoundingIncrement":{"type":"number","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TaxProfileJurisdictionConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Tax Profile & Jurisdiction Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"taxProfileName":{"type":"string","description":"Tax Profile Name"},"taxProfileCode":{"type":"string","description":"Tax Profile Code"},"taxType":{"type":"string","enum":["vat","gst","salesTax","entertainmentTax","tourismTax","municipalityTax","serviceTax","customRegulatoryTax"],"description":"Tax Type (pp.40-41)"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2 code","pattern":"^[A-Z]{2}$"},"jurisdiction":{"type":"string","description":"Region/Jurisdiction"},"legalEntity":{"type":"string","description":"Legal Entity"},"taxRegistrationNumber":{"type":"string","description":"Tax Registration Number"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From; new structures are future-dated and never change historical transactions"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"owner":{"type":"string","description":"Owner"},"ratePercent":{"type":"number","nullable":true,"description":"Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"},"taxProfileId":{"type":"string","description":"Tax profile ID; empty on create"},"jurisdictionLevel":{"type":"string","enum":["country","region","municipality"],"description":"Jurisdiction Hierarchy (p.41): the level this profile applies at"},"applicability":{"type":"array","items":{"type":"object","properties":{"level":{"type":"string","enum":["legalEntity","country","market","venue","productCategory","product","service","channel"]},"refId":{"type":"string"}}},"description":"Applicability (p.41): where the profile applies; a channel only where legally applicable"},"taxBase":{"type":"string","enum":["discountedPrice","preDiscountPrice"],"description":"Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"}}},
"TaxProfileJurisdictionConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Tax Profile & Jurisdiction Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"taxProfileName":{"type":"string","description":"Tax Profile Name"},"taxProfileCode":{"type":"string","description":"Tax Profile Code"},"taxType":{"type":"string","enum":["vat","gst","salesTax","entertainmentTax","tourismTax","municipalityTax","serviceTax","customRegulatoryTax"],"description":"Tax Type (pp.40-41)"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2 code","pattern":"^[A-Z]{2}$"},"jurisdiction":{"type":"string","description":"Region/Jurisdiction"},"legalEntity":{"type":"string","description":"Legal Entity"},"taxRegistrationNumber":{"type":"string","description":"Tax Registration Number"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From; new structures are future-dated and never change historical transactions"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"owner":{"type":"string","description":"Owner"},"ratePercent":{"type":"number","nullable":true,"description":"Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"},"taxProfileId":{"type":"string","description":"Tax profile ID; empty on create"},"jurisdictionLevel":{"type":"string","enum":["country","region","municipality"],"description":"Jurisdiction Hierarchy (p.41): the level this profile applies at"},"applicability":{"type":"array","items":{"type":"object","properties":{"level":{"type":"string","enum":["legalEntity","country","market","venue","productCategory","product","service","channel"]},"refId":{"type":"string"}}},"description":"Applicability (p.41): where the profile applies; a channel only where legally applicable"},"taxBase":{"type":"string","enum":["discountedPrice","preDiscountPrice"],"description":"Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"},"consumingProductCount":{"type":"integer","description":"Dependencies: products using the profile; read-only"},"consumingVenueCount":{"type":"integer","description":"Dependencies: venues using the profile; read-only"}}},
"TaxRuleTreatmentBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Tax Rule & Treatment Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category; empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue; empty for any"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country; empty for any"},"legalEntity":{"type":"string","nullable":true,"description":"Condition: legal entity; empty for any"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type (sale, refund, amendment, ...); empty for any"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type, only where legally relevant"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: sales channel, only where legally relevant; empty for any"},"taxRuleId":{"type":"string","description":"Tax rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"treatment":{"type":"string","enum":["taxInclusive","taxExclusive","taxExempt","zeroRated","outOfScope"],"description":"Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"},"calculationMethod":{"type":"string","enum":["percentage","fixedTax","tiered","compound","sequential","multipleConcurrent"],"description":"Calculation Method (p.42)"},"taxes":{"type":"array","items":{"type":"object","properties":{"taxProfileId":{"type":"string"},"sequence":{"type":"integer","description":"Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"},"onPreviousTaxes":{"type":"boolean","description":"Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"},"fixedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Amount when the method is fixedTax"}}},"description":"The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ratePercent":{"type":"number"}}},"description":"Tiers when the method is tiered; empty otherwise"},"exemptionRuleIds":{"type":"array","items":{"type":"string"},"description":"Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"TaxRuleTreatmentBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Tax Rule & Treatment Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category; empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue; empty for any"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country; empty for any"},"legalEntity":{"type":"string","nullable":true,"description":"Condition: legal entity; empty for any"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type (sale, refund, amendment, ...); empty for any"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type, only where legally relevant"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: sales channel, only where legally relevant; empty for any"},"taxRuleId":{"type":"string","description":"Tax rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"treatment":{"type":"string","enum":["taxInclusive","taxExclusive","taxExempt","zeroRated","outOfScope"],"description":"Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"},"calculationMethod":{"type":"string","enum":["percentage","fixedTax","tiered","compound","sequential","multipleConcurrent"],"description":"Calculation Method (p.42)"},"taxes":{"type":"array","items":{"type":"object","properties":{"taxProfileId":{"type":"string"},"sequence":{"type":"integer","description":"Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"},"onPreviousTaxes":{"type":"boolean","description":"Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"},"fixedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Amount when the method is fixedTax"}}},"description":"The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ratePercent":{"type":"number"}}},"description":"Tiers when the method is tiered; empty otherwise"},"exemptionRuleIds":{"type":"array","items":{"type":"string"},"description":"Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}}
}
```
