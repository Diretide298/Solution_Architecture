# P08-venue-operations-02 — P08 · Venue Operations (2 of 2)

**5 screens · 20 operations · 28 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AUDIT_VIEW, DEVICE_MANAGE, DEVICE_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |

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
| `BO-129` | Software, Configuration & Version Management | B | 16 | 12 | 6 | 5 | 4 | 0 | — | notStarted (generated) |
| `BO-130` | Offline Policy & Rules Configuration | A | 14 | 19 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-131` | Connectivity & Auto-Switch Settings | B | 13 | 0 | 5 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-132` | Offline Transaction Monitor & Sync Queue | C | 43 | 13 | 6 | 2 | 2 | 6 | — | notStarted (generated) |
| `BO-133` | Offline Alerts, Limits & Audit | A | 25 | 26 | 6 | 8 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-129` Software, Configuration & Version Management

**Manage configuration profiles and device firmware versions across the fleet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `core` module |
| Block | Block B · task VM-BO-129 |
| Who uses it | venue staff holding `DEVICE_MANAGE`, `DEVICE_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (2 configure, 2 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkstations` reads the population and `getWorkstationHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `profileId` (deepLink), `workstationId` (deepLink), `rolloutId` (navigation), `firmwareId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. Resolves from the session — a till is signed into. |
| Route | `/venue-operations/software-configuration-version-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** **`getWorkstationHealth` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-021): configureWorkstation and setConnectivityThresholds shared the firmware and profile screen; connectivity thresholds have their own screen (BO-131) and workstation … Removed 2 October 2026 (CHG-WIR-021): configureWorkstation and setConnectivityThresholds shared the firmware and profile screen; connectivity thresholds have their own screen (BO-131) and workstation …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Software and firmware for the venue's devices: profile versions, firmware versions per device model, staged rollout and rollback. A rollout names how many devices it touches and can be rolled back.

**Fixed on main** (the package already carries these; draw what it says): configureWorkstation and setConnectivityThresholds share the screen with firmware rollout. (CHG-WIR-021); formSetConfigurationProfile asks the person for status, id. (CHG-SBO-004); formDeployConfigurationProfile asks the person for status, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every workstation' drop id, venueId, regionId, departmentId, scopePath, accessPointId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listWorkstations`. | `listWorkstations` ?venueId |
| Sale board kind | radio group | optional | — | Ticketing · Fnb · Retail · Mixed | — | Sends `?saleBoardKind=` to `listWorkstations`. | `listWorkstations` ?saleBoardKind |
| Search software, configuration | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Device kind | text field | — | — | `listDeviceFirmware` ?deviceKind |
| Version | text field | — | — | `listDeviceFirmware` ?version |

**Form: Save configuration profile** (modal, opened by *Save configuration profile*; *Save configuration profile* calls `setConfigurationProfile`, *Cancel* sends nothing)

**Collects what `setConfigurationProfile` sends before it is called.** Required: `name`, `venueKindScope`. Optional: `scopePath`, `settings`. **Not asked:** `id` is a client UUIDv7 generated silently; `status` is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `deployedCount`, `publishedAt` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setConfigurationProfile` body |
| Name `name` | text field | required | — | — | — | — | `setConfigurationProfile` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setConfigurationProfile` body |
| Venue kind scope `venueKindScope` | list of values (chips) | required | — | — | — | Which workstation types it applies to. A ticketing counter and a kitchen display do not share a profile, and a profile that claims to is a profile somebody deploys to the wrong … | `setConfigurationProfile` body |
| Settings `settings` | key and value settings | optional | — | — | — | — | `setConfigurationProfile` body |
| Status `status` | select | required | — | Draft · Published · Deploying · Deployed · Superseded · Rolled back | — | On input only `draft` or `published`; sending `published` publishes this version. | `setConfigurationProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Deploy configuration profile** (modal, opened by *Deploy configuration profile*; *Deploy configuration profile* calls `deployConfigurationProfile`, *Cancel* sends nothing)

**Collects what `deployConfigurationProfile` sends before it is called.** Nothing in the body is required. Optional: `targetWorkstationIds`, `targetFilter`, `strategy`. **Not asked:** is a client UUIDv7 generated silently; is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `completedAt`, `failedCount`, `failureReasons`, `id`, `profileId`, `startedAt`, `status`, `succeededCount` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | number field | required | — | — | — | The published version to deploy. | `deployConfigurationProfile` body |
| Target workstations `targetWorkstationIds` | multi-picker: choose target workstations | optional | — | — | — | — | `deployConfigurationProfile` body |
| Target filter `targetFilter` | group | optional | — | — | — | By department, type or venue, where the target is a set rather than a list. | `deployConfigurationProfile` body |
| Venues `targetFilter.venueIds` | multi-picker: choose venues | optional | — | — | — | — | `deployConfigurationProfile` body |
| Departments `targetFilter.departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `deployConfigurationProfile` body |
| Workstation types `targetFilter.workstationTypes` | list of values (chips) | optional | — | — | — | The same workstation-type values `ConfigurationProfile.venueKindScope` holds. | `deployConfigurationProfile` body |
| Strategy `strategy` | segmented control | optional | On next idle | Immediate · Staged · On next idle | — | — | `deployConfigurationProfile` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setConfigurationProfile: tenant-wide only, no region or venue override is offered; configureWorkstation, setConnectivityThresholds: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setConfigurationProfile; contracts/spine/tenancy.yaml#configureWorkstation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**Workstation health** (detail panel, from `getWorkstationHealth`): Shows `score`, `status`, `contributors` from `getWorkstationHealth`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Score | 1,234 | — |
| Status | chip: Healthy, Warning, Degraded, Offline | — |
| Contributors | list or chips (count when long) | — |
| Factor | chip: Heartbeat age, Device offline, Device battery, Firmware outdated, Sync backlog … | — |
| Detail | text | — |
| Weight | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Save configuration profile (primary button) | `setConfigurationProfile` PUT `/configuration-profiles` | ConfigurationProfile | ConfigurationProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Deploy configuration profile (secondary button) | `deployConfigurationProfile` POST `/configuration-profiles/{profileId}/deploy` | ProfileDeployment | ProfileDeployment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Deploy configuration profile**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/spine/tenancy.yaml#deployConfigurationProfile)*

**Data it reads**: `listWorkstations` (onLoad, List workstations); `listDeviceFirmware` (onLoad, Firmware versions per device fleet)

**Where the user goes next**

- → `BO-130` Offline Policy & Rules Configuration: *Offline Policy & Rules Configuration*
- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-037` Offline Package Status: *Each device's cached package is checked*; carries `version`
- → `BO-124` Layout & Journey Builder: *Its sale board layout is built*; carries `profileId`; calls `setConfigurationProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The software version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the software version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No software version yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, saleBoardKind and the software version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires to show this screen, and names that permission (the screen's other reads need `DEVICE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_MANAGE` for `startDeviceFirmwareRollout` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A release with this `deviceKind` and `version` already exists; 409 The firmware named by `firmwareId` is not `released`; 409 The move is not allowed from the release's current status (back to `draft`, out of `withdrawn`, or `deprecated` before `released`) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds DEVICE_VIEW, SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save configuration profile, Deploy configuration profile, Save connectivity thresholds; WORKSTATION_CONFIGURE for Configure workstation; DEVICE_MANAGE for startDeviceFirmwareRollout, rollbackDeviceFirmware, createDeviceFirmware. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setConfigurationProfile)*
- **deployConfigurationProfile answers 409**: Show it as something the person can act on, not a failure: **The named version is not deployable** — it is still a `draft`, or this profile has no such version. Names the version and its status. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*
- **configureWorkstation answers 409**: Show it as something the person can act on, not a failure: **A shift is open on this workstation.** The change is not applied; it can be made once the shift has closed. Names the open shift. *(source: contracts/spine/tenancy.yaml#configureWorkstation)*
- **startDeviceFirmwareRollout answers 409**: Show it as something the person can act on, not a failure: The firmware named by `firmwareId` is not `released` *(source: contracts/spine/tenancy.yaml#startDeviceFirmwareRollout)*
- **rollbackDeviceFirmware answers 409**: Show it as something the person can act on, not a failure: The rollout kept no previous image (`previousVersionRetained` false), so there is nothing to roll back to *(source: contracts/spine/tenancy.yaml#rollbackDeviceFirmware)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
firmware:
- model: Sunmi T2s
  version: 4.2.1
  status: rolling out
  devices: 12 of 30
- model: Zebra TC52
  version: 11-49-18
  status: current
```

#### Permissions

- `setConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `deployConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `getWorkstationHealth` → `DEVICE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `listDeviceFirmware` → `DEVICE_VIEW` (read) · staff
- `startDeviceFirmwareRollout` → `DEVICE_MANAGE` (configure) · staff
- `rollbackDeviceFirmware` → `DEVICE_MANAGE` (configure) · staff
- `createDeviceFirmware` → `DEVICE_MANAGE` (configure) · staff
- `getDeviceFirmware` → `DEVICE_VIEW` (read) · staff
- `setDeviceFirmwareStatus` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires to show this screen, and names that permission (the screen's other reads need `DEVICE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_MANAGE` for `startDeviceFirmwareRollout` …

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.6.32 | Software Version Tracking - System shall maintain software version records. | Device Management | CONTRACTED | `listDeviceFirmware` |
| 16.6.31 | Remote Firmware Updates - System shall support remote firmware deployment. | Device Management | CONTRACTED | `startDeviceFirmwareRollout` |
| 16.6.34 | Update Rollback - System shall support rollback of updates. | Device Management | CONTRACTED | `rollbackDeviceFirmware` |
| 16.6.30 | Firmware Management - System shall support firmware management. | Device Management | CONTRACTED | `createDeviceFirmware` |
| 16.6.33 | Software Update Management - System shall support software update management. | Device Management | CONTRACTED | `createDeviceFirmware` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Firmware: package library per device; compatibility rules limit deployment to compatible models; update wizard with phased/scheduled rollout; live monitor flags failures (e.g. device offline at deployment); rollback and update history. *(client request · MoM 15 Sep 2026, 4.7 Firmware & Software Management · DI-903)*
- Remote configuration deploys a device type's settings (e.g. receipt printers) to many workstations in one action; configuration versions can be compared and rolled back. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-898)*
- Versioned configuration profiles with deployments: board 1F shows 1,248 workstations across four configuration versions. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 1F · DI-404)*
- Software configuration tracks software version and pending/completed updates per workstation. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-305)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-129` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5d`
- Flow F79 *A workstation is registered, configured and rolled out*, step 2: A configuration profile is set for it. → Software version, settings and when it counts as offline.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-129?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Save configuration profile, Deploy configuration profile, What publishing changes.
- [ ] Every transition is wired: `BO-130`, `BO-108`, `BO-037`, `BO-124`.
- [ ] Every gated control is gated: `DEVICE_MANAGE`, `DEVICE_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-130` Offline Policy & Rules Configuration

**Offline Policy & Rules Configuration — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `core` module |
| Block | Block A · task VM-BO-130 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (1 operate, 2 read, 1 configure); in the flows as cashier, technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSyncRejections` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `rejectionId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/venue-operations/offline-policy-rules-configuration` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Moved to wave 1 on 24 August.** F33 walks a till going offline and coming back, which is a wave-1 journey — ADR-0013 makes the POS local-first from the first release. **A venue that can trade offline and cannot resolve a sync rejection has an unbounded journal and no way to clear it**, and `check-flows` refused the flow rather than let that ship. **Resolved remotely by design.** is venue-scoped and this is a web screen — **a supervisor at the main venue clears a mall kiosk's rejections without going there.** An IT technician restores the connection; **deciding whether a sale stands is a commercial act and they have the access without the authority.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Devices replay their own journals (syncOrders is POS-013's) and a supervisor resolves a rejection rather than typing a sync batch or a new order … Removed 2 October 2026 (CHG-WIR-025): Devices replay their own journals (syncOrders is POS-013's) and a supervisor resolves a rejection rather than typing a sync batch or a new order …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What a till, kiosk or device may do with no network, and for how long: allowed actions by data class, ceilings on value and on count, and what happens at the ceiling. It also lists the offline transactions the server refused, which a supervisor resolves remotely. Offline switching is automatic; the policy sets the limits.

**Fixed on main** (the package already carries these; draw what it says): syncOrders and createOrder are offered as forms on this policy screen. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listSyncRejections`. | `listSyncRejections` ?workstationId |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
| Search offline policy | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope path | text field | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | `getOfflinePolicy` ?scopePath |

**Form: Save offline policy** (modal, opened by *Save offline policy*; *Save offline policy* calls `setOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node this policy is for, and the key `setOfflinePolicy` upserts on. The body names its target here, because the path does not. | `setOfflinePolicy` body |
| Max offline hours `maxOfflineHours` | stepper or slider (hours) | optional | 24 | min 1; max 72 | — | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody … | `setOfflinePolicy` body |
| Allowed offline `allowedOffline` | multi-select chips | optional | — | Sale · Refund · Exchange · Entitlement issue · Entitlement validate · Loyalty accrual · Loyalty redemption · Wallet spend · Price override · Discount · Void line · No sale; Selling from a cached catalogue is safe; issuing a refund is not, because the original … | — | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified. | `setOfflinePolicy` body |
| Offline value ceiling `offlineValueCeiling` | money field | optional | — | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | `setOfflinePolicy` body |
| Offline transaction ceiling `offlineTransactionCeiling` | number field | optional | — | min 1; max 5000 | — | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. | `setOfflinePolicy` body |
| On ceiling breach `onCeilingBreach` | segmented control | optional | Block new sales | Warn · Block new sales · Block all | — | — | `setOfflinePolicy` body |
| Requires manager to extend `requiresManagerToExtend` | toggle | optional | on | — | — | — | `setOfflinePolicy` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Resolve rejection** (modal, opened by *Resolve rejection*; *Resolve rejection* calls `resolveSyncRejection`, *Cancel* sends nothing)

**Collects what `resolveSyncRejection` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | segmented control | required | — | Posted · Voided · Refunded | — | `posted` — the sale was entered with `createOrder` (F33 step 8); `voided` — with `voidOrder`; `refunded` — with `createRefund`. | `resolveSyncRejection` body |
| Resolved record `resolvedRecordId` | picker: choose a resolved record | required | — | — | shows names, sends the id | The id of the order, void or refund that resolution produced. | `resolveSyncRejection` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveSyncRejection` body |

Errors to draw in the form: 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allowedOffline**: A checklist grouped Safe offline (sale, entitlement validate, no sale) and Risky offline (refund, exchange, price override, discount, wallet spend, loyalty redemption) with the risky group unticked by default and a one-line reason for each. *(source: contracts/spine/tenancy.yaml#setOfflinePolicy / DI-142)*
- **ceilings**: Maximum hours offline (1 to 72, default 24), value ceiling in the venue's currency, transaction ceiling (1 to 5,000); the action at breach (warn, block new sales, block all) and whether a manager may extend. *(source: contracts/spine/tenancy.yaml#/components/schemas/OfflinePolicy / DI-405)*
- **scope**: The policy is set at a node (venue, department, workstation group) and inherited below it (PR-4). *(source: contracts/spine/tenancy.yaml#setOfflinePolicy / ADR-0018)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the offline policy saved at this scope** (card list, from `getOfflinePolicy`)

| Shows | Format | Notes |
|---|---|---|
| Max offline hours | 1,234 | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a … |
| Allowed offline | list or chips (count when long) | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale … |
| Offline value ceiling | AED 1,234.50 | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September … |
| Offline transaction ceiling | 1,234 | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only … |
| On ceiling breach | chip: Warn, Block new sales, Block all | — |
| Requires manager to extend | yes / no (icon or chip) | — |

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save offline policy (primary button) | `setOfflinePolicy` PUT `/offline-policy` | OfflinePolicy | OfflinePolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Resolve rejection (secondary button) | `resolveSyncRejection` POST `/sync/rejections/{rejectionId}/resolve` | ResolveSyncRejectionRequest | SyncRejection | 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **sync rejections**: Each refused offline entry with device, time recorded, product and amount, and the reason; these never retry, so the list is a to-do, not a log. *(source: contracts/spine/orders.yaml#listSyncRejections / F33 step 7)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Resolve rejection**: Posts the sale against the retired product at the price the guest paid (the catalogue moved, the transaction did not) and removes it from the unresolved view. *(source: F33 step 8)*

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused); `getOfflinePolicy` (onLoad, Load the offline policy saved at this scope)

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-129` Software, Configuration & Version Management: *The connectivity thresholds are set*; carries `workstationId`; calls `setOfflinePolicy`
- → `BO-131` Connectivity & Auto-Switch Settings: *The connectivity thresholds are set*; calls `setOfflinePolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline policy rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline policy rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline policy rules yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the offline policy rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `resolveSyncRejection`; `TENANT_CONFIGURE` for `setOfflinePolicy`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  scope: Dune Park / Retail
  maxOfflineHours: 12
  valueCeiling: AED 20,000.00
  transactionCeiling: 400
  onBreach: blockNewSales
  managerMayExtend: true
rejection:
  device: Kiosk K-03
  recordedAt: 2026-11-14 11:20
  item: Summer Splash Pass (retired 13 Nov)
  amount: AED 120.00
```

#### Permissions

- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `resolveSyncRejection` → `ORDER_MODIFY` (operate) · staff
- `getOfflinePolicy` → `TENANT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `resolveSyncRejection`; `TENANT_CONFIGURE` for `setOfflinePolicy`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- POS offline policy configuration (board 5B) and connectivity auto-switch with a threshold (board 5D): how quickly a device flips to offline is a venue setting. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 5B / 5D · DI-405)*
- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-130` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5e`
- Flow F33 *A till goes offline and comes back*, step 7: Four transactions are rejected — a product retired while the till was offline. → **Rejected, not discarded.** A sale that happened is a sale, and the guest has the goods — the rejection is a reconciliation task, not a reversal.
- Flow F33 *A till goes offline and comes back*, step 8: The supervisor resolves each one. → Posted against the retired product at the price the guest paid. **The catalogue moved and the transaction did not** — repricing it now would change what was charged.
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 1: The venue sets its offline policy. → What a till may do with no network, and for how long.
- Flow F33 branch at step 8 (medium): when A rejected transaction sold stock the venue no longer had., **The oversell stands and the stock goes negative.** A movement is written either way, because **a stock level that refuses to go negative is a stock level that hides what happened** — and the count …
- Flow F89 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-130?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save offline policy, Resolve rejection.
- [ ] Every transition is wired: `BO-108`, `BO-129`, `BO-131`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-131` Connectivity & Auto-Switch Settings

**Set when a device is treated as offline and when it switches back online.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `core` module |
| Block | Block B · task VM-BO-131 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setConnectivityThresholds`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/venue-operations/connectivity-auto-switch-settings` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** When a till decides it is offline and when it switches back: probe interval, timeout, failures before offline, successes and stable seconds before online, and whether it switches automatically. Values are bounded so a venue cannot set a till to flap.

**Fixed on main** (the package already carries these; draw what it says): id and scopePath are form fields. (CHG-SBO-015); 8 text fields are raw schema property names, not inputs: id, scopePath, failuresBeforeOffline, probeIntervalSeconds, probeTimeoutMs … (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Failures before offline | stepper or slider | optional | 3 | min 1; max 10 | — | Consecutive, not cumulative. One dropped request on a busy till is normal; three in a row is a network. | `ConnectivityPolicy.failuresBeforeOffline` |
| Probe every (seconds) | number field (seconds) | optional | 15 | min 5; max 300 | — | — | `ConnectivityPolicy.probeIntervalSeconds` |
| Probe timeout (ms) | number field | optional | 2000 | min 500; max 30000; Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129). | — | Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129). | `ConnectivityPolicy.probeTimeoutMs` |
| Successes before online | stepper or slider | optional | 5 | min 1; max 20; Never below `failuresBeforeOffline`, or the body is refused `400` (audit R129). | — | Higher than the offline threshold, deliberately. Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing. | `ConnectivityPolicy.successesBeforeOnline` |
| Stable for (seconds) | number field (seconds) | optional | 30 | min 10; max 600 | — | How long the connection must hold before the workstation trusts it. This is what stops the flapping, and it is the field a venue with poor wifi will actually tune. | `ConnectivityPolicy.minimumStableSeconds` |
| Switch automatically | toggle | optional | on | — | — | — | `ConnectivityPolicy.autoSwitch` |

**Sent by *Save connectivity thresholds*** (`setConnectivityThresholds`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node these thresholds are for, and the key `setConnectivityThresholds` upserts on. | `setConnectivityThresholds` body |
| Failures before offline `failuresBeforeOffline` | stepper or slider | optional | 3 | min 1; max 10 | — | Consecutive, not cumulative. One dropped request on a busy till is normal; three in a row is a network. | `setConnectivityThresholds` body |
| Probe interval seconds `probeIntervalSeconds` | number field (seconds) | optional | 15 | min 5; max 300 | — | — | `setConnectivityThresholds` body |
| Probe timeout ms `probeTimeoutMs` | number field | optional | 2000 | min 500; max 30000; Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129). | — | Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129). | `setConnectivityThresholds` body |
| Successes before online `successesBeforeOnline` | stepper or slider | optional | 5 | min 1; max 20; Never below `failuresBeforeOffline`, or the body is refused `400` (audit R129). | — | Higher than the offline threshold, deliberately. Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing. | `setConnectivityThresholds` body |
| Minimum stable seconds `minimumStableSeconds` | number field (seconds) | optional | 30 | min 10; max 600 | — | How long the connection must hold before the workstation trusts it. This is what stops the flapping, and it is the field a venue with poor wifi will actually tune. | `setConnectivityThresholds` body |
| Auto switch `autoSwitch` | toggle | optional | on | — | — | — | `setConnectivityThresholds` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Thresholds**: Number fields with units (seconds, milliseconds) and the proposed minimum and maximum shown beside each; values outside are refused. *(source: R270; R129)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setConnectivityThresholds: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setConnectivityThresholds)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save connectivity thresholds (primary button) | `setConnectivityThresholds` PUT `/connectivity-policy` | ConnectivityPolicy | ConnectivityPolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-037` Offline Package Status: *Each device's cached package is checked*; calls `setConnectivityThresholds`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved connectivity auto-switch settings. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the connectivity auto-switch settings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No connectivity auto-switch settings configured. The form opens empty and `setConnectivityThresholds` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `setConnectivityThresholds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
thresholds:
  probeIntervalSeconds: 10
  probeTimeoutMs: 1500
  failuresBeforeOffline: 3
  successesBeforeOnline: 3
  minimumStableSeconds: 30
  autoSwitch: true
```

#### Permissions

- `setConnectivityThresholds` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `setConnectivityThresholds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- POS offline policy configuration (board 5B) and connectivity auto-switch with a threshold (board 5D): how quickly a device flips to offline is a venue setting. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 5B / 5D · DI-405)*
- Qossai: for seated/zoned venues, POS terminals on the same network share real-time seat state; a disconnected network needs its own offline zone. Whether zoning is automatic or client-enabled is a per-venue setting. *(client request · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-143)*
- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-131` · status **notStarted** · provenance generated
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 2: The connectivity thresholds are set. → When a device counts as offline rather than slow.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-131?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save connectivity thresholds.
- [ ] Every transition is wired: `BO-108`, `BO-037`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-132` Offline Transaction Monitor & Sync Queue

**Offline Transaction Monitor & Sync Queue — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `ticketing` module |
| Block | Block C · task VM-BO-132 |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSyncRejections` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/venue-operations/offline-transaction-monitor-sync-queue` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Offline transactions waiting to sync and those the server refused, per device; refused entries never retry.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listSyncRejections`. | `listSyncRejections` ?workstationId |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
| Search offline transaction monitor | search field | — | — | — | — | — | — |

**Form: Sync orders** (modal, opened by *Sync orders*; *Sync orders* calls `syncOrders`, *Cancel* sends nothing)

**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Orders `orders` | repeatable rows | required | — | at least 1; at most 200 | — | — | `syncOrders` body |
| ID `orders[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `syncOrders` body |
| Venue `orders[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Channel `orders[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `syncOrders` body |
| Shift `orders[].shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Subject `orders[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `syncOrders` body |
| Guest link `orders[].guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `syncOrders` body |
| Catalogue bundle version `orders[].catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `syncOrders` body |
| Lines `orders[].lines` | repeatable rows | required | — | at least 1 | — | — | `syncOrders` body |
| ID `orders[].lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `syncOrders` body |
| Variant `orders[].lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Recommendation `orders[].lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `syncOrders` body |
| Performance `orders[].lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Booked window `orders[].lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `syncOrders` body |
| Inventory hold `orders[].lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `syncOrders` body |
| Seats `orders[].lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `syncOrders` body |
| Resource hold `orders[].lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `syncOrders` body |
| Attributes `orders[].lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `syncOrders` body |
| Quantity `orders[].lines[].quantity` | number field | required | — | min 1 | — | — | `syncOrders` body |
| Eligibility declaration `orders[].lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `syncOrders` body |
| Quoted unit price `orders[].lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `syncOrders` body |
| Holder name `orders[].lines[].holderName` | text field | optional | — | — | — | — | `syncOrders` body |
| Data mask values `orders[].lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `syncOrders` body |
| Recorded at `orders[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |
| Sequence `orders[].sequence` | number field | required | — | min 1 | — | Monotonic per device. Processed in this order. | `syncOrders` body |
| Payments `orders[].payments` | repeatable rows | required | — | — | — | — | `syncOrders` body |
| ID `orders[].payments[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `syncOrders` body |
| Order `orders[].payments[].orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Tender `orders[].payments[].tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `syncOrders` body |
| Amount `orders[].payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `syncOrders` body |
| Tender currency `orders[].payments[].tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `syncOrders` body |
| Tender amount `orders[].payments[].tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `syncOrders` body |
| Wallet authorisation `orders[].payments[].walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `syncOrders` body |
| Wallet hold `orders[].payments[].walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `syncOrders` body |
| Return URL `orders[].payments[].returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `syncOrders` body |
| Terminal `orders[].payments[].terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `syncOrders` body |
| Device `orders[].payments[].deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Recorded at `orders[].payments[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync orders (primary button) | `syncOrders` POST `/sync/orders` | inline | OrderSyncResult | — | emits `order.paid`, `sync.rejectionRaised`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **sync queue**: Per device, pending count and oldest; refused entries with the reason and Resolve. *(source: contracts/spine/orders.yaml#listSyncRejections / F33 step 7)*

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused)

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline transaction sync list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline transaction sync untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline transaction sync yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the offline transaction sync are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `syncOrders`. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-130`: Same rejection list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
device:
  name: Kiosk K-03
  pending: 18
  rejected: 4
  oldest: '11:20'
```

#### Permissions

- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `syncOrders` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `syncOrders`.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.3.1 | The system should support offline mode for POS and Kiosk: - Ability to switch automatically to offline mode in case of server outage / network loss - Definition of which functionality will be lost in … | Ticketing Sales | CONTRACTED | `syncOrders` |
| 2.14.2 | For all sales at POS, it is possible to have an offline mode. | Ticketing Sales | CONTRACTED | `syncOrders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-132` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (43), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-132?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync orders.
- [ ] Every transition is wired: `BO-108`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-133` Offline Alerts, Limits & Audit

**Offline Alerts, Limits & Audit — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `ticketing` module |
| Block | Block A · task APP-SETUP-BO-133 |
| Who uses it | venue staff holding `AUDIT_VIEW`, `ORDER_MODIFY`, `ORDER_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW` (3 read, 2 operate, 1 configure); in the flows as cashier |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `decideApprovalRequest` decides items that `listSyncRejections` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `venueId` (session), `reportId` (deepLink), `requestId` (deepLink), `rejectionId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. An approval request opened from the queue. |
| Route | `/venue-operations/offline-alerts-limits-audit` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-5F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Moved to wave 1 on 24 August.** F33 walks a till going offline and coming back, which is a wave-1 journey — ADR-0013 makes the POS local-first from the first release. **A venue that can trade offline and cannot resolve a sync rejection has an unbounded journal and no way to clear it**, and `check-flows` refused the flow rather than let that ship.

**Known gaps.** A refused offline entry is resolved with resolveSyncRejection, not with an approval decision (design-note correction finance-insights BO-133, CHG-SBO-012).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The venue's control over offline trading: what the server refused when tills synced back, which offline limits were crossed, and who did what. From the finance angle the screen is about money that exists in the till but not yet in the books. The one thing to get right: every refused sale, payment, refund or void stays visible until a supervisor resolves it, because an unresolved one is cash with no ledger entry.

**Fixed on main** (the package already carries these; draw what it says): The queue is the refused entries, but the decision button is "Decide approval request". (CHG-SBO-012); The workstation filter is a typed id. (CHG-SBO-012).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Till | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Workstation.id` |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
| Search offline alerts, limits | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listSyncRejections` ?workstationId |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Action | text field | — | — | `listAuditRecords` ?action |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| From | date and time picker | — | — | `listAuditRecords` ?from |
| To | date and time picker | — | — | `listAuditRecords` ?to |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Save alert rule** (modal, opened by *Save alert rule*; *Save alert rule* calls `setAlertRule`, *Cancel* sends nothing)

**Collects what `setAlertRule` sends before it is called.** Required: `id`, `name`, `metric`, `comparator`, `threshold`, `severity`, `isActive`, `scopePath`. Optional: `thresholdUpper`, `windowMinutes`, `deliverTo`, `recipientRoleIds`, `cooldownMinutes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setAlertRule` body |
| Name `name` | text field | required | — | — | — | — | `setAlertRule` body |
| Metric `metric` | select | required | — | Occupancy · Capacity utilisation · Admission rate · No show rate · Conversion · Sales by operator · Sales by workstation · Wait time · Throughput · Abandonment rate · Inventory valuation · Stock turnover … | — | From the closed set, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for. | `setAlertRule` body |
| Comparator `comparator` | radio group | required | — | Above · Below · Outside range · Changes by · Equals | — | — | `setAlertRule` body |
| Threshold `threshold` | number field | required | — | — | — | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its … | `setAlertRule` body |
| Threshold upper `thresholdUpper` | number field | optional | — | Required when `comparator` is `outsideRange` (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is … | — | Required when `comparator` is `outsideRange` (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not … | `setAlertRule` body |
| Window minutes `windowMinutes` | number field (minutes) | optional | 15 | — | — | The window is what stops an alert firing on noise. A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes … | `setAlertRule` body |
| Severity `severity` | segmented control | required | — | Info · Warning · Critical | — | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. | `setAlertRule` body |
| Deliver to `deliverTo` | multi-select chips | optional | — | Dashboard panel · Email · Whatsapp · SMS · Push | — | CF-134. The dashboard panel is the default and the only one that always applies. | `setAlertRule` body |
| Recipient roles `recipientRoleIds` | multi-picker: choose recipient roles | optional | — | — | — | — | `setAlertRule` body |
| Cooldown minutes `cooldownMinutes` | number field (minutes) | optional | 30 | — | — | How long before the same rule may fire again. Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close. | `setAlertRule` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setAlertRule` body |
| Scope path `scopePath` | text field | required | — | `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused. | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setAlertRule` body |

Errors to draw in the form: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158)

**Form: Resolve refused entry** (modal, opened by *Resolve refused entry*; *Resolve refused entry* calls `resolveSyncRejection`, *Cancel* sends nothing)

**Collects what `resolveSyncRejection` sends before it is called.** Required: `resolution`, `resolvedRecordId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | segmented control | required | — | Posted · Voided · Refunded | — | `posted` — the sale was entered with `createOrder` (F33 step 8); `voided` — with `voidOrder`; `refunded` — with `createRefund`. | `resolveSyncRejection` body |
| Resolved record `resolvedRecordId` | picker: choose a resolved record | required | — | — | shows names, sends the id | The id of the order, void or refund that resolution produced. | `resolveSyncRejection` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveSyncRejection` body |

Errors to draw in the form: 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem)

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Resolution of a refused entry**: Post it, void it, or refund it, with a note; the entry is shown exactly as the till recorded it, never retyped. *(source: contracts/spine/orders.yaml#/components/schemas/SyncRejection / contracts/spine/orders.yaml#resolveSyncRejection)*
- **Alert rule (offline exposure)**: A ceiling on value and a ceiling on count of offline sales per till, severity, who is told, and a cool-down. Both ceilings matter: nine hundred small sales and one large one are different risks. *(source: F33 step 4 / contracts/satellite/reporting.yaml#setAlertRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Rule name | text | `AlertRule.name` as it stood when the alert was raised. The line a person reads — a list of rule ids is not an alert panel, and a screen … |
| Metric | chip: Occupancy, Capacity utilisation, Admission rate, No show rate, Conversion, Sales by … | The rule's metric, carried so the alert says what went out of range. |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |

**Every audit** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save alert rule (secondary button) | `setAlertRule` PUT `/alert-rules` | AlertRule | AlertRule | 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158) | opens modal first |
| Resolve refused entry (primary button) | `resolveSyncRejection` POST `/sync/rejections/{rejectionId}/resolve` | ResolveSyncRejectionRequest | SyncRejection | 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Refused entries**: Kind (sale, payment, refund, void, scan), till, recorded time, refused time, amount, and the reason in words. Unresolved first; resolved ones show the outcome and who resolved them. *(source: contracts/spine/orders.yaml#/components/schemas/SyncRejection)*
- **Voids and discounts report**: By operator, reason and approver for the chosen day. *(source: R282)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Resolve**: The entry is posted, voided or refunded and leaves the waiting list. *(source: contracts/spine/orders.yaml#resolveSyncRejection)*
- **Save alert rule**: The ceiling applies from now; the next breach raises an alert to the named roles. *(source: contracts/satellite/reporting.yaml#setAlertRule)*

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused); `listAlerts` (onLoad, What is currently raised); `listAuditRecords` (onLoad, Who did what, where, and when); `listWorkstations` (onLoad, List workstations (the pick list))

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*
- → `POS-002` Sell — Ticket Catalogue: *The connection returns*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline alerts limits list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline alerts limits untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the offline alerts limits are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) |

#### Edge cases to draw

- **A refused card payment for goods already handed over**: Flag as money at risk with the amount; resolution choices explain the ledger effect. *(source: contracts/spine/orders.yaml#/components/schemas/SyncRejection)*
- **Month end is closing with refused entries open**: Show "Open shifts or unresolved entries block the close" with a link to BO-090. *(source: F13 step 1)*

#### Consistency with other screens

- Match `POS-020`: Same alert wording and severity as the till's queue.
- Match `BO-090`: Open items here are what the period close checks name.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rejections:
- Sale · Till 4 Beach Shop · recorded 13:12 offline · refused 13:47 · AED 340.00 · price no longer valid
- Refund · Till 2 · AED 125.00 · original sale not found
rule: Offline exposure · Till · above AED 15,000.00 or 120 sales · Critical · notify Venue manager, Finance
```

#### Permissions

- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `setAlertRule` → `REPORT_MANAGE` (configure) · staff
- `resolveSyncRejection` → `ORDER_MODIFY` (operate) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for …

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 6.1.56 | The system should be able to report on Daily revenue alerts in a Mobile application format (Dashboard in a Mobile App). | Retail POS | CONTRACTED | data `AlertRule` |
| 8.7.22 | System shall support KPI alerts. | Unified Operations Dashboard | CONTRACTED | data `AlertRule` |
| 8.9.10 | System shall provide dashboards, reports, drill-down analytics, alerts, and historical operational performance analysis. | Unified Operations Dashboard | CONTRACTED | data `AlertRule` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-133` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5f`
- Flow F33 *A till goes offline and comes back*, step 4: The venue's offline exposure crosses a ceiling. → **A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-133?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report, Save alert rule, Resolve refused entry.
- [ ] Every transition is wired: `BO-108`, `POS-002`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `ORDER_MODIFY`, `ORDER_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P08 · Venue Operations

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createDeviceFirmware": {"method":"POST","path":"/device-firmware","contract":"tenancy","summary":"Register a firmware or software release before it is deployed","permission":"DEVICE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceFirmware","responds":"DeviceFirmware"},
"deployConfigurationProfile": {"method":"POST","path":"/configuration-profiles/{profileId}/deploy","contract":"tenancy","summary":"Push a version to a fleet, in stages","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProfileDeployment","responds":null},
"getDeviceFirmware": {"method":"GET","path":"/device-firmware/{firmwareId}","contract":"tenancy","summary":"Read one firmware release, and how much of the fleet is on it","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"DeviceFirmware"},
"getOfflinePolicy": {"method":"GET","path":"/offline-policy","contract":"tenancy","summary":"The offline policy saved at one scope node","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":true}],"requestBody":null,"responds":"OfflinePolicy"},
"getWorkstationHealth": {"method":"GET","path":"/workstations/{workstationId}/health","contract":"tenancy","summary":"A score a manager can sort by, and what is dragging it down","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceFirmware": {"method":"GET","path":"/device-firmware","contract":"tenancy","summary":"Firmware and software versions, and what is running where","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"deviceKind","in":"query","required":null},{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"DeviceFirmware"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"resolveSyncRejection": {"method":"POST","path":"/sync/rejections/{rejectionId}/resolve","contract":"orders","summary":"Record what was done about a refused entry","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResolveSyncRejectionRequest","responds":"SyncRejection"},
"rollbackDeviceFirmware": {"method":"POST","path":"/device-firmware/rollouts/{rolloutId}/rollback","contract":"tenancy","summary":"Put the fleet back on the previous version","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceFirmwareRollout"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"setAlertRule": {"method":"PUT","path":"/alert-rules","contract":"reporting","summary":"Watch a metric and tell somebody","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AlertRule","responds":"AlertRule"},
"setConfigurationProfile": {"method":"PUT","path":"/configuration-profiles","contract":"tenancy","summary":"What a class of workstation is configured to be","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationProfile","responds":"ConfigurationProfile"},
"setConnectivityThresholds": {"method":"PUT","path":"/connectivity-policy","contract":"tenancy","summary":"When a workstation decides it is offline, and when it is back","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConnectivityPolicy","responds":"ConnectivityPolicy"},
"setDeviceFirmwareStatus": {"method":"POST","path":"/device-firmware/{firmwareId}/status","contract":"tenancy","summary":"Release, deprecate or withdraw a firmware release","permission":"DEVICE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceFirmware"},
"setOfflinePolicy": {"method":"PUT","path":"/offline-policy","contract":"tenancy","summary":"What a workstation may do with no network, and for how long","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflinePolicy","responds":"OfflinePolicy"},
"startDeviceFirmwareRollout": {"method":"POST","path":"/device-firmware/rollouts","contract":"tenancy","summary":"Push an update to a fleet, in waves","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceFirmwareRollout","responds":"DeviceFirmwareRollout"},
"syncOrders": {"method":"POST","path":"/sync/orders","contract":"orders","summary":"Replay orders recorded offline","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSyncResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertRule": {"type":"object","x-ticvai-persistence":"reporting.alert_rule","description":"BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n","required":["id","name","metric","comparator","threshold","severity","isActive","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"},"comparator":{"type":"string","enum":["above","below","outsideRange","changesBy","equals"]},"threshold":{"$ref":"#/components/schemas/MetricValue"},"thresholdUpper":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true,"description":"**Required when `comparator` is `outsideRange`** (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is refused by `setAlertRule` with 400. Ignored for every other comparator.\n"},"windowMinutes":{"type":"integer","default":15,"description":"**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"deliverTo":{"type":"array","description":"CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n","items":{"type":"string","enum":["dashboardPanel","email","whatsapp","sms","push"]},"x-ticvai-push-note":"**`push` added 29 September** (6.1.56, 18.1.5, build pass): delivered to every staff-app handset registered for a recipient (tenancy `RegisteredDevice`, kind `mobileHandset`, with a push token). It is how a daily revenue alert reaches a manager's phone, which a panel on a web dashboard does not.\n"},"recipientRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"cooldownMinutes":{"type":"integer","default":30,"description":"**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**\n\n**Required, and it is the write target.** `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused."}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"ConfigurationProfile": {"type":"object","x-ticvai-persistence":"platform.configuration_profile","description":"Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n","required":["id","name","venueKindScope","version","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"scopePath":{"type":"string"},"venueKindScope":{"type":"array","description":"Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n","items":{"type":"string"}},"version":{"type":"integer","readOnly":true,"description":"**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was. Assigned by the server: 1 on create, and one more each time a change lands on a published version (see `setConfigurationProfile`).\n"},"settings":{"type":"object","additionalProperties":true},"status":{"type":"string","enum":["draft","published","deploying","deployed","superseded","rolledBack"],"description":"On input only `draft` or `published`; sending `published` publishes this version. The other four are set by deployment and refused on input.\n"},"deployedCount":{"type":"integer","readOnly":true},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ConnectivityPolicy": {"type":"object","x-ticvai-persistence":"platform.connectivity_policy","description":"Board 5 of the client's POS set, and the second of the two genuine gaps. **Nothing in the package held a threshold**, so a device that flips offline on one dropped packet and one that waits five minutes were the same product.\n**Going offline and coming back need different thresholds.** Symmetric ones produce a workstation that flaps — offline, online, offline — across a marginal connection, and each flap is a sync.\n**One per scope node, keyed on `scopePath`.** `id` is server-owned and absent where `getConnectivityPolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them, or a broken cross-field rule, is refused `400` with `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node these thresholds are for, and the key `setConnectivityThresholds` upserts on.** The body names its target here, because the path does not.\n"},"failuresBeforeOffline":{"type":"integer","default":3,"minimum":1,"maximum":10,"description":"**Consecutive, not cumulative.** One dropped request on a busy till is normal; three in a row is a network.\n"},"probeIntervalSeconds":{"type":"integer","default":15,"minimum":5,"maximum":300},"probeTimeoutMs":{"type":"integer","default":2000,"minimum":500,"maximum":30000,"description":"Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129)."},"successesBeforeOnline":{"type":"integer","default":5,"minimum":1,"maximum":20,"description":"**Higher than the offline threshold, deliberately.** Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing. **Never below `failuresBeforeOffline`**, or the body is refused `400` (audit R129).\n"},"minimumStableSeconds":{"type":"integer","default":30,"minimum":10,"maximum":600,"description":"How long the connection must hold before the workstation trusts it. **This is what stops the flapping**, and it is the field a venue with poor wifi will actually tune.\n"},"autoSwitch":{"type":"boolean","default":true}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency. For a guest-channel card or wallet payment on an order with a `chargeCurrency`, the server sets it from the order (CHG-FIN-001)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"DeviceFirmware": {"type":"object","x-ticvai-persistence":"tenancy.device_firmware","description":"16.6.30 and 16.6.32. **A release, and how much of the fleet is on it.** Written by `createDeviceFirmware` and moved through its life by `setDeviceFirmwareStatus` (29 September, build pass); `startDeviceFirmwareRollout` deploys only a `released` one.\n","required":["deviceKind","version"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"deviceKind":{"type":"string"},"version":{"type":"string"},"vendor":{"type":"string","nullable":true,"description":"Who built the image, as the device's driver names its maker."},"checksumAlgorithm":{"type":"string","enum":["sha256","sha512"],"default":"sha256"},"releaseNotes":{"type":"string","nullable":true},"artefactAssetId":{"type":"string","format":"uuid","nullable":true},"checksum":{"type":"string","nullable":true},"minimumPreviousVersion":{"type":"string","nullable":true,"description":"**Some updates cannot be applied from any starting point.** Naming the floor is how a two-step upgrade stays possible instead of bricking the devices that skipped one.\n"},"releasedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set when `setDeviceFirmwareStatus` first makes the release `released`."},"installedCount":{"type":"integer","readOnly":true},"status":{"type":"string","readOnly":true,"default":"draft","enum":["draft","released","deprecated","withdrawn"]},"statusReason":{"type":"string","nullable":true,"readOnly":true,"description":"The `reason` given when the release was deprecated or withdrawn."},"scopePath":{"type":"string","readOnly":true,"description":"The tenant the release belongs to. Releases are tenant-wide; rollouts narrow them."}}},
"DeviceFirmwareRollout": {"type":"object","x-ticvai-persistence":"tenancy.device_rollout","description":"16.6.31, 16.6.33 and 16.6.34. **Staged, windowed and reversible.**","required":["firmwareId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"firmwareId":{"type":"string","format":"uuid"},"targetScopePath":{"type":"string","nullable":true},"targetDeviceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"waves":{"type":"array","description":"**A canary first.** Gate hardware failing across a venue at once is an evacuation problem rather than an IT one.\n","items":{"type":"object","properties":{"name":{"type":"string"},"percent":{"type":"integer"},"startAt":{"type":"string","format":"date-time","nullable":true},"haltOnFailurePercent":{"type":"integer","default":5}}}},"maintenanceWindow":{"type":"object","nullable":true,"description":"**When a device may be updated.** `from` and `to` are wall-clock values read in the region's time zone, not UTC.\n","properties":{"from":{"type":"string"},"to":{"type":"string"}}},"previousVersionRetained":{"type":"boolean","default":true,"description":"**Rollback is only possible if the old image is still there**, so this is a property of the rollout rather than of the rollback.\n"},"status":{"type":"string","readOnly":true,"enum":["scheduled","running","paused","completed","halted","rolledBack"]},"succeededCount":{"type":"integer","readOnly":true},"failedCount":{"type":"integer","readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"OfflineOrder": {"x-ticvai-persistence":"none — client-side journal, not server storage","allOf":[{"$ref":"#/components/schemas/CreateOrderRequest"},{"type":"object","required":["sequence","payments"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. Processed in this order."},"payments":{"type":"array","items":{"$ref":"#/components/schemas/CreatePaymentRequest"}}}}]},
"OfflinePolicy": {"type":"object","x-ticvai-persistence":"platform.offline_policy","description":"Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"},"maxOfflineHours":{"type":"integer","default":24,"minimum":1,"maximum":72,"description":"**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"},"allowedOffline":{"type":"array","description":"**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n","items":{"type":"string","enum":["sale","refund","exchange","entitlementIssue","entitlementValidate","loyaltyAccrual","loyaltyRedemption","walletSpend","priceOverride","discount","voidLine","noSale"]}},"offlineValueCeiling":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"},"offlineTransactionCeiling":{"type":"integer","nullable":true,"minimum":1,"maximum":5000,"description":"**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"},"onCeilingBreach":{"type":"string","enum":["warn","blockNewSales","blockAll"],"default":"blockNewSales"},"requiresManagerToExtend":{"type":"boolean","default":true}}},
"OrderSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer"},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The `OfflineOrder.id` this result is about."},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","rejected","blockedByRejection"],"description":"`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."},"orderNumber":{"type":"string","nullable":true},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Posted to the variance account. Not surfaced to the cashier."},"varianceExceedsThreshold":{"type":"boolean","description":"True when review is required per the venue's variance threshold."},"rejectionId":{"type":"string","nullable":true,"description":"For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProfileDeployment": {"type":"object","x-ticvai-persistence":"platform.profile_deployment","description":"**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n","required":["id","profileId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path of `deployConfigurationProfile`."},"version":{"type":"integer","description":"The published version to deploy."},"targetWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"targetFilter":{"type":"object","nullable":true,"description":"By department, type or venue, where the target is a set rather than a list.\n","properties":{"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"workstationTypes":{"type":"array","description":"The same workstation-type values `ConfigurationProfile.venueKindScope` holds.","items":{"type":"string"}}}},"strategy":{"type":"string","enum":["immediate","staged","onNextIdle"],"default":"onNextIdle"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"],"readOnly":true},"succeededCount":{"type":"integer","readOnly":true},"failedCount":{"type":"integer","readOnly":true},"failureReasons":{"type":"object","readOnly":true,"additionalProperties":{"type":"integer"},"description":"**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ResolveSyncRejectionRequest": {"type":"object","x-ticvai-persistence":"none — request only; lands on sync.rejection","required":["resolution","resolvedRecordId"],"properties":{"resolution":{"type":"string","enum":["posted","voided","refunded"],"description":"`posted` — the sale was entered with `createOrder` (F33 step 8); `voided` — with `voidOrder`; `refunded` — with `createRefund`.\n"},"resolvedRecordId":{"type":"string","format":"uuid","description":"The id of the order, void or refund that resolution produced."},"note":{"type":"string","maxLength":500,"nullable":true}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
