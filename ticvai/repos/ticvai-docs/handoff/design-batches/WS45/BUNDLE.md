# WS45 — Promotions   Bundles Management board 1

**10 screens · 21 operations · 26 schemas · 4 permissions**

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
  `APPROVAL_DECIDE, APPROVAL_VIEW, PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-138` | Promotion Command Center Dashboard | B–D | 0 | 18 | 6 | 1 | 1 | 2 | — | notStarted (generated) |
| `ADM-139` | Promotion & Campaign Directory | B | 21 | 47 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-140` | Promotion Overview | B–D | 0 | 62 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-141` | Promotion Lifecycle & Status Manager | B–D | 2 | 0 | 6 | 2 | 0 | 2 | — | notStarted (generated) |
| `ADM-142` | Campaign Calendar & Timeline | B | 6 | 14 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-143` | Promotion Channel & Publication Monitor | B | 0 | 2 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-144` | Promotion Alerts & Exception Center | B | 6 | 0 | 5 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-145` | Promotion Approval Inbox | B–D | 0 | 22 | 6 | 21 | 0 | 5 | — | notStarted (generated) |
| `ADM-146` | Promotion Health & Performance Monitor | B | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-147` | Promotion Audit, Activity & Version History | B | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-140, ADM-147 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-138` Promotion Command Center Dashboard

**Provide management with a real-time executive and operational overview of all promotional activities. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Global KPI cards) and a per-row directory (§Dashboard Visualizations) — counts over a population, then the population |
| Offline | online only |
| Opens with | `promotionId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that … |
| Route | `/venue-operations/promotions-coupons/promotion-command-center-dashboard-adm-138` |

**What the spec says about it.** **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The hub of the promotions board on the TICVAI Console (acting inside a tenant, PR-1): live, scheduled and paused promotions with what each has cost against its budget. The nine detail screens of the board are reached from here and return here.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Scheduled · Live · Paused · Expired · Ended | `listPromotions` ?status |
| Active at | date and time picker | — | — | `listPromotions` ?activeAt |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Promotions** (metric tile)

**Upcoming Promotions** (metric tile)

**Draft Promotions** (metric tile)

**Pending Approval** (metric tile)

**Suspended Promotions** (metric tile)

**Promotions Ending Soon** (metric tile)

**Total Promotion Revenue** (metric tile)

**Total Discount Granted** (metric tile)

**Incremental Revenue** (metric tile)

**Promotion Conversion Rate** (metric tile)

**Redemption Rate** (metric tile)

**Average Order Value Uplift** (metric tile)

**Promotion Cost** (metric tile)

**Estimated Margin Impact** (metric tile)

**Campaign Budget Utilization** (metric tile)

**Every promotion** (data table, from `listPromotions`)

| Shows | Format | Notes |
|---|---|---|
| Promotion revenue trend | text | not in the schema: `Promotion revenue trend` |
| Discount exposure trend | text | not in the schema: `Discount exposure trend` |
| Conversion uplift | text | not in the schema: `Conversion uplift` |
| Promotions by channel | text | not in the schema: `Promotions by channel` |
| Promotions by venue | text | not in the schema: `Promotions by venue` |
| Promotions by product | text | not in the schema: `Promotions by product` |
| Campaign budget consumption | text | not in the schema: `Campaign budget consumption` |
| Top performing promotions | text | not in the schema: `Top-performing promotions` |
| Underperforming promotions | text | not in the schema: `Underperforming promotions` |

**The selected promotion** (detail panel): The pack groups this record's detail under its own headings: “Break down current promotions by”.

| Shows | Format | Notes |
|---|---|---|
| Promotion revenue trend | text | not in the schema: `Promotion revenue trend` |
| Discount exposure trend | text | not in the schema: `Discount exposure trend` |
| Conversion uplift | text | not in the schema: `Conversion uplift` |
| Promotions by channel | text | not in the schema: `Promotions by channel` |
| Promotions by venue | text | not in the schema: `Promotions by venue` |
| Promotions by product | text | not in the schema: `Promotions by product` |
| Campaign budget consumption | text | not in the schema: `Campaign budget consumption` |
| Top performing promotions | text | not in the schema: `Top-performing promotions` |
| Underperforming promotions | text | not in the schema: `Underperforming promotions` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPI row**: Live promotions, redemptions today, discount given this period with delta, budgets near exhaustion; each card filters the list below. *(source: contracts/satellite/promotions.yaml#getPromotionUsage / DI-041)*
- **promotion list**: Status badge (Draft, Scheduled, Live, Paused, Expired, Ended), dates, redemptions, discount given as a bar against the budget cap; exhausted budgets first. *(source: contracts/satellite/promotions.yaml#listPromotions / contracts/satellite/promotions.yaml#getPromotionUsage)*

**Data it reads**: `listPromotions` (onLoad, List promotions)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-145` Promotion Approval Inbox: *Promotion Approval Inbox*
- → `ADM-142` Campaign Calendar & Timeline: *Works in Campaign Calendar & Timeline*; calls `listPromotions`
- → `ADM-143` Promotion Channel & Publication Monitor: *Works in Promotion Channel & Publication Monitor*; calls `listPromotions`
- → `ADM-144` Promotion Alerts & Exception Center: *Works in Promotion Alerts & Exception Center*; calls `listPromotions`
- → `ADM-146` Promotion Health & Performance Monitor: *Works in Promotion Health & Performance Monitor*; calls `listPromotions`
- → `ADM-147` Promotion Audit, Activity & Version History: *Works in Promotion Audit, Activity & Version History*; calls `listPromotions`
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `campaignId`, `code`, `promotionId`
- → `ADM-139` Promotion & Campaign Directory: *Works in Promotion & Campaign Directory*; carries `campaignId`
- → `ADM-140` Promotion Overview: *Works in Promotion Overview*; carries `promotionId`; calls `listPromotions`
- → `ADM-141` Promotion Lifecycle & Status Manager: *Works in Promotion Lifecycle & Status Manager*; carries `promotionId`; calls `listPromotions`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-010`: The venue's promotions desk shows the same records; same badges and budget bar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  live: 7
  redemptionsToday: 1284
  discountThisMonth: AED 212,400.00
  nearBudget: 2
```

#### Permissions

- `listPromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `getPromotionUsage` → `PRICE_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.12 | The system should be able to manage all promotions in Backoffice application, where the positioning of the promotions fits in with the mechanics of the booking platform. In this way the Shop Cart is … | Admission and Access | CONTRACTED | `listPromotions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-138` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-138`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 1: Opens Promotion Command Center Dashboard → Provide management with a real-time executive and operational overview of all promotional activities.
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F154 branch at step 1 (expected): when Nothing has been set up on Promotion Command Center Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F154 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-138?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-145`, `ADM-142`, `ADM-143`, `ADM-144`, `ADM-146`, `ADM-147`, `BO-010`, `ADM-139`, `ADM-140`, `ADM-141`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-139` Promotion & Campaign Directory

**Provide the master searchable list of every promotion and commercial campaign created within TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29974 (VM-ADM-139) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Table Columns) and no metric row |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/commercial/promotion-campaign-directory-adm-139` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The searchable master list of promotions and commercial campaigns, with performance per row, and where a campaign header is created before its promotions and budget.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listPromotionCampaign, listCampaignPromotionPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search promotion campaign | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by promotion type, campaign, product, product category, venue, attraction and 13 more — which are present is a decision the pack already made. | — |
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Promotion type | text field | — | — | `listPromotionCampaign` ?promotionType |
| Campaign | text field | — | — | `listPromotionCampaign` ?campaign |
| Product | text field | — | — | `listPromotionCampaign` ?product |
| Product category | text field | — | — | `listPromotionCampaign` ?productCategory |
| Venue | text field | — | — | `listPromotionCampaign` ?venue |
| Attraction | text field | — | — | `listPromotionCampaign` ?attraction |
| Event | text field | — | — | `listPromotionCampaign` ?event |
| Fnb | text field | — | — | `listPromotionCampaign` ?fnb |
| Retail | text field | — | — | `listPromotionCampaign` ?retail |
| Membership | text field | — | — | `listPromotionCampaign` ?membership |
| Channel | text field | — | — | `listPromotionCampaign` ?channel |
| Partner | text field | — | — | `listPromotionCampaign` ?partner |
| Customer segment | text field | — | — | `listPromotionCampaign` ?customerSegment |
| Date | text field | — | — | `listPromotionCampaign` ?date |
| Status | text field | — | — | `listPromotionCampaign` ?status |
| Owner | text field | — | — | `listPromotionCampaign` ?owner |
| … 3 more | | | | `operations.json` |

**Form: Create commercial campaign** (modal, opened by *Create commercial campaign*; *Create commercial campaign* calls `createCommercialCampaign`, *Cancel* sends nothing)

**Collects what `createCommercialCampaign` sends before it is called.** Required: `venueId`, `name`. Optional: `code`, `description`, `ownerPrincipalId`, `legalEntityId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createCommercialCampaign` body |
| Code `code` | text field | optional | — | max length 64 | — | Unique at the venue when given. | `createCommercialCampaign` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createCommercialCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createCommercialCampaign` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | The campaign (and budget) owner. | `createCommercialCampaign` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | The business entity that funds and books the campaign. | `createCommercialCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCommercialCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCommercialCampaign` body |

Errors to draw in the form: 400 `validTo` at or before `validFrom`.; 409 `code` is already used by another campaign at the venue.

**Form: Save commercial campaign** (modal, opened by *Save commercial campaign*; *Save commercial campaign* calls `updateCommercialCampaign`, *Cancel* sends nothing)

**Collects what `updateCommercialCampaign` sends before it is called.** Nothing in the body is required. Optional: `code`, `name`, `description`, `ownerPrincipalId`, `legalEntityId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 64 | — | — | `updateCommercialCampaign` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateCommercialCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateCommercialCampaign` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `updateCommercialCampaign` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | — | `updateCommercialCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCommercialCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCommercialCampaign` body |

Errors to draw in the form: 400 `validTo` at or before `validFrom`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The new code is already used at the venue, or the new dates would leave a scheduled or live promotion, coupon campaign or active bundle of the campaign outside …

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Every promotion campaign** (data table, from `listPromotionCampaign`)

| Shows | Format | Notes |
|---|---|---|
| Promotion | text | Promotion ID |
| Promotion name | text | Promotion Name |
| Promotion type | text | Promotion Type |
| Campaign | text | Campaign |
| Status | text | Status |
| Business entity | text | Business Entity |
| Venue | text | Venue |
| Product | text | Product |
| Target segment | text | Target Segment |
| Channel | text | Channel |
| Start date | 1 Oct 2026, 14:30 | Start Date |
| End date | 1 Oct 2026, 14:30 | End Date |
| Discount type | text | Discount Type |
| Discount value | AED 1,234.50 | Discount Value |
| Budget | AED 1,234.50 | Budget |
| Redemption count | 1,234 | Redemption Count |
| Revenue generated | AED 1,234.50 | Revenue Generated |
| Owner | text | Owner |
| Approval status | text | Approval Status |
| Version | text | Version |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**The selected promotion campaign** (detail panel): The pack groups this record's detail under its own headings: “Supported Statuses”.

| Shows | Format | Notes |
|---|---|---|
| Promotion | text | Promotion ID |
| Promotion name | text | Promotion Name |
| Promotion type | text | Promotion Type |
| Campaign | text | Campaign |
| Status | text | Status |
| Business entity | text | Business Entity |
| Venue | text | Venue |
| Product | text | Product |
| Target segment | text | Target Segment |
| Channel | text | Channel |
| Start date | 1 Oct 2026, 14:30 | Start Date |
| End date | 1 Oct 2026, 14:30 | End Date |
| Discount type | text | Discount Type |
| Discount value | AED 1,234.50 | Discount Value |
| Budget | AED 1,234.50 | Budget |
| Redemption count | 1,234 | Redemption Count |
| Revenue generated | AED 1,234.50 | Revenue Generated |
| Owner | text | Owner |
| Approval status | text | Approval Status |
| Version | text | Version |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Activate, Pause, Extend, Duplicate, Archive, Export, Assign owner, Submit for approval. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create commercial campaign (primary button) | `createCommercialCampaign` POST `/commercial-campaigns` | CreateCommercialCampaignRequest | CommercialCampaign | 400 `validTo` at or before `validFrom`.; 409 `code` is already used by another campaign at the venue. | gated `PRICE_CONFIGURE`; opens modal first |
| Save commercial campaign (secondary button) | `updateCommercialCampaign` PATCH `/commercial-campaigns/{campaignId}` | inline | CommercialCampaign | 400 `validTo` at or before `validFrom`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The new code is already used at the venue, or the new dates would … | gated `PRICE_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **directory**: Promotion, type, campaign, status, venue, channel, dates, discount, budget, redemptions, revenue, owner, approval status; grouped by campaign with a collapsible header row. *(source: contracts/satellite/promotions.yaml#listPromotionCampaign / contracts/satellite/promotions.yaml#listCommercialCampaigns)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **New campaign**: Creates the header only (name, owner, business entity, dates); budget lines follow on ADM-219. *(source: contracts/satellite/promotions.yaml#createCommercialCampaign)*

**Data it reads**: `listPromotionCampaign` (onLoad, Promotion & Campaign Directory); `listCampaignPromotionPerformance` (onLoad, Campaign & Promotion Performance Explorer); `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion campaign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion campaign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion campaign yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion campaign are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `validTo` at or before `validFrom`.; 409 The new code is already used at the venue, or the new dates would leave a scheduled or live promotion, coupon campaign or active bundle of the campaign outside …; 409 `code` is already used by another campaign at the venue. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- campaign: Winter Family 2026
  promotion: Family Fun Bundle 15% off
  status: Live
  redemptions: 640
  revenue: AED 412,000.00
```

#### Permissions

- `listPromotionCampaign` → `PRICE_VIEW` (read) · staff
- `listCampaignPromotionPerformance` → `PRICE_VIEW` (read) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff
- `createCommercialCampaign` → `PRICE_CONFIGURE` (configure) · staff
- `updateCommercialCampaign` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-139` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-139`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 2: Works in Promotion & Campaign Directory → Provide the master searchable list of every promotion and commercial campaign created within TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-139?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create commercial campaign, Save commercial campaign.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-140` Promotion Overview

**Provide the complete business summary of one selected promotion without opening its detailed configuration. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `promotionId` (navigation) |
| Route | `/venue-operations/promotions-coupons/promotion-overview-adm-140` |

**What the spec says about it.** **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-025): The overview of one selected promotion listed every promotion (listPromotions); it reads the selected promotion (getPromotion) and its usage (getPromotionUsage). …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** One promotion's business summary without its configuration: what it gives, to whom, where, when, and how it is doing.

**Fixed on main** (the package already carries these; draw what it says): The screen lists all promotions (listPromotions) but shows one. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Promotion** (detail panel, from `getPromotion`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique per tenant (6 October 2026, CHG-R4-015; the rule of audit R108 for configuration codes). |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Kind | chip: Percentage, Fixed amount, Fixed price, Buy x get y, Free item, Tiered percentage | — |
| Percentage | 12.5% | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fixed price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Buy quantity | 1,234 | — |
| Get quantity | 1,234 | — |
| Get discount percentage | 1,234.5 | 100 makes the free items actually free; lower values give a partial discount. |
| Tiers | list or chips (count when long) | For `tieredPercentage` — more units, larger discount. |
| Min quantity | 1,234 | — |
| Percentage | 12.5% | — |
| Max discount amount | AED 1,234.50 | Cap on a percentage discount. Prevents an unbounded discount on a large basket. |
| Reward variants | list or chips (count when long) | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` … |
| Max applications per basket | 1,234 | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (createPromotion; setFixedPriceOffer was … |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Variants | list or chips (count when long) | — |

**Usage** (detail panel, from `getPromotionUsage`)

| Shows | Format | Notes |
|---|---|---|
| Promotion | the name it points at, never the id | — |
| Redemption count | 1,234 | — |
| Discount given | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget remaining | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is budget exhausted | yes / no (icon or chip) | — |
| By channel | list or chips (count when long) | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Redemption count | 1,234 | — |
| Discount given | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected promotion overview** (detail panel): The pack groups this record's detail under its own headings: “Direct links to”.

| Shows | Format | Notes |
|---|---|---|
| Promotion name | text | not in the schema: `Promotion name` |
| Promotion ID | text | not in the schema: `Promotion ID` |
| Version | text | not in the schema: `Version` |
| Status | text | not in the schema: `Status` |
| Owner | text | not in the schema: `Owner` |
| Created by | text | not in the schema: `Created by` |
| Effective dates | text | not in the schema: `Effective dates` |
| Campaign | text | not in the schema: `Campaign` |
| Business entity | text | not in the schema: `Business entity` |
| Promotion mechanism | text | not in the schema: `Promotion mechanism` |
| Discount/reward | text | not in the schema: `Discount/reward` |
| Eligible products | text | not in the schema: `Eligible products` |
| Eligible customers | text | not in the schema: `Eligible customers` |
| Eligible channels | text | not in the schema: `Eligible channels` |
| Eligible locations | text | not in the schema: `Eligible locations` |
| Applicable time/date conditions | text | not in the schema: `Applicable time/date conditions` |
| Usage limits | text | not in the schema: `Usage limits` |
| Budget | text | not in the schema: `Budget` |
| Redemption ceiling | text | not in the schema: `Redemption ceiling` |
| Promotion hierarchy | text | not in the schema: `Promotion hierarchy` |
| Stacking behavior | text | not in the schema: `Stacking behavior` |
| Approval state | text | not in the schema: `Approval state` |
| Transactions | text | not in the schema: `Transactions` |
| Redemptions | text | not in the schema: `Redemptions` |
| Gross revenue | text | not in the schema: `Gross revenue` |
| Discount granted | text | not in the schema: `Discount granted` |
| Net revenue | text | not in the schema: `Net revenue` |
| Incremental revenue | text | not in the schema: `Incremental revenue` |
| Conversion | text | not in the schema: `Conversion` |
| AOV impact | text | not in the schema: `AOV impact` |
| … 2 more | | `schemas.json` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **summary card**: The rule in one sentence ("Buy 2 Day Passes, get the 3rd free, website and app, until 31 Jan"), status, budget used, redemptions, and an "Edit configuration" link. *(source: contracts/satellite/promotions.yaml#getPromotion)*

**Data it reads**: `getPromotion` (onLoad, The selected promotion); `getPromotionUsage` (onLoad, Its redemption count and the discount given)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `campaignId`, `code`, `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion overview list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion overview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion overview yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion overview are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
promotion:
  code: SUMMER-BOGO
  sentence: Buy 2 Day Passes, get the 3rd free
  status: Live
  used: 37% of AED 50,000.00
```

#### Permissions

- `getPromotion` → `PRICE_VIEW` (read) · staff, guest, partner
- `getPromotionUsage` → `PRICE_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-140` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-140`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 4: Works in Promotion Overview → Provide the complete business summary of one selected promotion without opening its detailed configuration.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-140?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-138`, `BO-010`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-141` Promotion Lifecycle & Status Manager

**Control the operational lifecycle of promotions. (a section of BO-010 Promotions & Coupons since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `promotionId` (navigation) |
| Route | `/venue-operations/promotions-coupons/promotion-lifecycle-status-manager-adm-141` |

**What the spec says about it.** **Merged into BO-010 Promotions & Coupons as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-010: it renders inside BO-010's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **Promotion Lifecycle & Status Manager declares no operation that writes anything** — its only declared call is `listPromotionLifecycleStatus`, a read. The name promises authoring and the contract … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Lifecycle of promotions: where each stands, failed activation checks, suspension reasons, and the moves allowed (publish, pause, end, unschedule).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listPromotionLifecycleStatus return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

**Fixed on main** (the package already carries these; draw what it says): The screen has no lifecycle write; the moves exist (publishPromotion, pausePromotion, endPromotion, unschedulePromotion) but are not … (CHG-WIR-025); No write operation: a configuration screen (Promotion Lifecycle & Status Manager) declares only reads (listPromotionLifecycleStatus). (CHG-MOV-002).

#### Inputs: what the user enters or picks

**Form: Pause** (modal, opened by *Pause*; *Pause* calls `pausePromotion`, *Cancel* sends nothing)

**Collects what `pausePromotion` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `pausePromotion` body |

Errors to draw in the form: 409 Not in a state that permits this

**Form: End** (modal, opened by *End*; *End* calls `endPromotion`, *Cancel* sends nothing)

**Collects what `endPromotion` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `endPromotion` body |

Errors to draw in the form: 409 Not in a state that permits this

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Save Draft, Validate, Submit for Simulation, Submit for Approval, Approve, Reject, Schedule, Activate, Pause, Resume, Suspend, Extend, Terminate, Archive. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (secondary button) | `publishPromotion` POST `/promotions/{promotionId}/publish` | — | Promotion | 409 Conflict analysis failed. (StackingProblem) | — |
| Pause (secondary button) | `pausePromotion` POST `/promotions/{promotionId}/pause` | inline | no body | 409 Not in a state that permits this | opens modal first |
| End (secondary button) | `endPromotion` POST `/promotions/{promotionId}/end` | inline | no body | 409 Not in a state that permits this | opens modal first |
| Unschedule (secondary button) | `unschedulePromotion` POST `/promotions/{promotionId}/unschedule` | — | no body | 409 Not in a state that permits this | — |
|  (publish gate) | `publishPromotion` POST `/promotions/{promotionId}/publish` | — | Promotion | 409 Conflict analysis failed. (StackingProblem) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lifecycle board**: Columns by stage (Draft, Scheduled, Live, Paused, Ended) with failed checks shown on the card. *(source: contracts/satellite/promotions.yaml#listPromotionLifecycleStatus)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Lifecycle moves**: The same actions and rules as BO-010 (publish runs the conflict analysis; pause keeps carts priced). *(source: contracts/satellite/promotions.yaml#publishPromotion / contracts/satellite/promotions.yaml#pausePromotion)*

**Data it reads**: `listPromotionLifecycleStatus` (onLoad, Promotion Lifecycle & Status Manager)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`
- → `BO-010` Promotions & Coupons: *Open Promotions & Coupons*; carries `campaignId`, `code`, `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion lifecycle status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion lifecycle status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion lifecycle status yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion lifecycle status are still there. The pack's own statuses are Paused/Suspended → Expired → Archived — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Conflict analysis failed. (StackingProblem); 409 Not in a state that permits this |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- promotion: RESIDENT-15
  stage: Draft
  failedChecks:
  - no channel selected
```

#### Permissions

- `listPromotionLifecycleStatus` → `PRICE_VIEW` (read) · staff
- `publishPromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `pausePromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `endPromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `unschedulePromotion` → `PRICE_CONFIGURE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.9 | The system should be able to manage flash sales which are required to operate within the existing planned Promo code functionality. | Admission and Access | CONTRACTED | `publishPromotion` |
| 3.6.10 | The system should be able to accommodate promotions to remain active during the event i.e. flash sales, campaigns etc. The requirements would be different for every path of marketing chosen by the … | Admission and Access | CONTRACTED | `publishPromotion` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-141` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-141`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 6: Works in Promotion Lifecycle & Status Manager → Control the operational lifecycle of promotions.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-141?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, Pause, End, Unschedule, .
- [ ] Every transition is wired: `ADM-138`, `BO-010`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-142` Campaign Calendar & Timeline

**Provide a calendar-based operational view of promotions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29960 (VM-ADM-142) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify) and no metric row Rendered on the calendar template (M17-03, 29 September). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/campaign-calendar-timeline-adm-142` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promotions on a calendar (day, week, month, agenda) by venue and channel, overlaps visible.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCampaignCalendarTimeline return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |
| View: day, week or month | select field | — | — | — | — | **Every calendar has day, week and month views, and the day view is broken into hours from the venue's day start hour** (17 September minutes, M17-03). Built on the shared calendar view … | — |
| Category | multi select | — | — | — | — | **Filtered by category, so a team sees only what is theirs** (M17-03). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listCampaignCalendarTimeline` ?venue |
| Product | text field | — | — | `listCampaignCalendarTimeline` ?product |
| Attraction | text field | — | — | `listCampaignCalendarTimeline` ?attraction |
| Channel | text field | — | — | `listCampaignCalendarTimeline` ?channel |
| Campaign | text field | — | — | `listCampaignCalendarTimeline` ?campaign |
| Promotion family | text field | — | — | `listCampaignCalendarTimeline` ?promotionFamily |
| View | radio group | — | Day · Week · Month · Quarter · Campaign timeline | `listCampaignCalendarTimeline` ?view |

#### Outputs: what the screen shows and produces

**Shown**

**Every campaign calendar timeline** (data table, from `listCampaignCalendarTimeline`)

| Shows | Format | Notes |
|---|---|---|
| Calendar state | chip: Active, Upcoming, Ending soon, Expired, Pending approval, Conflicting… | How the calendar marks this promotion. |

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Calendar** (calendar view, from `listCampaignCalendarTimeline`): Entries of the view in force, placed by date and hour.

| Shows | Format | Notes |
|---|---|---|
| Calendar state | chip: Active, Upcoming, Ending soon, Expired, Pending approval, Conflicting… | How the calendar marks this promotion. |
| Promotion | text | Promotion ID |
| Promotion name | text | Promotion Name |
| Start date | 1 Oct 2026, 14:30 | Start Date |
| End date | 1 Oct 2026, 14:30 | End Date |
| Venue | text | Venue |
| Channel | text | Channel |

**The selected campaign calendar timeline** (detail panel): The pack groups this record's detail under its own headings: “Views”, “Show promotions by”, “Users may”, “Conflict Detection”.

| Shows | Format | Notes |
|---|---|---|
| Calendar state | chip: Active, Upcoming, Ending soon, Expired, Pending approval, Conflicting… | How the calendar marks this promotion. |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **calendar**: Bars coloured by state; overlapping promotions on the same product stacked so stacking risks are visible. *(source: contracts/satellite/promotions.yaml#listCampaignCalendarTimeline / DI-919)*

**Data it reads**: `listCampaignCalendarTimeline` (onLoad, Campaign Calendar & Timeline); `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign calendar timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign calendar timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign calendar timeline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign calendar timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-765`: Same calendar component as the venue's campaign calendar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bars:
- promotion: Winter Family 2026
  from: 15 Nov
  to: 15 Jan
  venue: Dune Park
```

#### Permissions

- `listCampaignCalendarTimeline` → `PRICE_VIEW` (read) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-142` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-142`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 8: Works in Campaign Calendar & Timeline → Provide a calendar-based operational view of promotions.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-142?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-143` Promotion Channel & Publication Monitor

**Ensure promotional configurations are correctly synchronized across every TICVAI sales channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29975 (VM-ADM-143) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Show) and a per-row directory (§For each channel display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-channel-publication-monitor-adm-143` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Publish, Republish, Disable channel, Compare configurations, View synchronization log. Each needs an …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether each promotion is correctly published on every channel: version published, last synchronised, rules and products published, code availability, errors.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Publish, Republish, Disable channel, Compare configurations, View synchronization log. (CHG-MOV-008)
- List operation(s) listPromotionChannel return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPromotionChannel carry no identifier. (CHG-MOV-008)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Promotion version** (metric tile)

**Last synchronized** (metric tile)

**Rules published** (metric tile)

**Products published** (metric tile)

**Code availability** (metric tile)

**Channel restrictions** (metric tile)

**Error messages** (metric tile)

**Every promotion channel publication** (data table, from `listPromotionChannel`)

| Shows | Format | Notes |
|---|---|---|
| Publication status | chip: Not assigned, Pending publication, Published, Synchronizing, Publication failed … | The promotion's publication status on this channel. |

**The selected promotion channel publication** (detail panel): The pack groups this record's detail under its own headings: “Supported Channels”.

| Shows | Format | Notes |
|---|---|---|
| Publication status | chip: Not assigned, Pending publication, Published, Synchronizing, Publication failed … | The promotion's publication status on this channel. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| Republish (secondary button) | navigation or local | — | — | — | — |
| Disable channel (destructive button) | navigation or local | — | — | — | — |
| Compare configurations (secondary button) | navigation or local | — | — | — | — |
| View synchronization log (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel matrix**: Promotions as rows, channels as columns, each cell In sync, Out of sync (after an edit), Suspended or Error with the message. *(source: contracts/satellite/promotions.yaml#listPromotionChannel / contracts/satellite/promotions.yaml#updatePromotion)*

**Data it reads**: `listPromotionChannel` (onLoad, Promotion Channel & Publication Monitor)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*

**What opens over it**

- confirmDialog *Disable channel*: **Disable channel on a promotion channel publication is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion channel publication list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion channel publication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion channel publication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion channel publication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  promotion: SUMMER-BOGO
  Website: In sync v3
  App: In sync v3
  Point of sale: Out of sync (till release pending)
```

#### Permissions

- `listPromotionChannel` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-143` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-143`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 10: Works in Promotion Channel & Publication Monitor → Ensure promotional configurations are correctly synchronized across every TICVAI sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-143?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, Republish, Disable channel, Compare configurations, View synchronization log.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-144` Promotion Alerts & Exception Center

**Centralize operational, commercial, and financial alerts affecting promotions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29976 (VM-ADM-144) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-alerts-exception-center-adm-144` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Assign alert, Acknowledge, Resolve, Suspend campaign, Open related configuration, Add internal comment. Each …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Alerts affecting promotions (budget near exhaustion, abnormal redemption, publication failures, margin breaches) by severity.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions with no operation: Assign alert, Acknowledge, Resolve, Suspend campaign, Open related configuration, Add internal comment. (CHG-MOV-008)
- List operation(s) listPromotionAlertException return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Missing product | select field | — | — | — | — | — | — |
| Missing eligibility | select field | — | — | — | — | — | — |
| Invalid dates | select field | — | — | — | — | — | — |
| Invalid discount | select field | — | — | — | — | — | — |
| Invalid code | select field | — | — | — | — | — | — |
| Missing approval | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign alert (primary button) | navigation or local | — | — | — | — |
| Acknowledge (secondary button) | navigation or local | — | — | — | — |
| Resolve (secondary button) | navigation or local | — | — | — | — |
| Suspend campaign (destructive button) | navigation or local | — | — | — | — |
| Open related configuration (secondary button) | navigation or local | — | — | — | — |
| Add internal comment (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **alert list**: Severity, type, promotion, raised at (relative time as DI-042), with "open promotion". *(source: contracts/satellite/promotions.yaml#listPromotionAlertException / DI-042)*

**Data it reads**: `listPromotionAlertException` (onLoad, Promotion Alerts & Exception Center)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`

**What opens over it**

- confirmDialog *Suspend campaign*: **Suspend campaign on a promotion alerts exception is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion alerts exception configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion alerts exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion alerts exception configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alerts:
- severity: high
  type: Budget 90% used
  promotion: SUMMER-BOGO
  raised: 12 min ago
```

#### Permissions

- `listPromotionAlertException` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-144` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-144`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 12: Works in Promotion Alerts & Exception Center → Centralize operational, commercial, and financial alerts affecting promotions.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-144?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Assign alert, Acknowledge, Resolve, Suspend campaign, Open related configuration, Add internal comment.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-145` Promotion Approval Inbox

**Provide one centralized approval workspace for promotional changes. (a section of BO-084 Approval Inbox since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW`, `PRICE_VIEW` (1 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): the pack lists Approve and Reject among this screen's own actions — every row is waiting for a decision, so the empty state is success rather than a prompt to create something |
| Offline | online only |
| Opens with | `requestId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that … |
| Route | `/approvals/approval-inbox/promotion-approval-inbox-adm-145` |

**What the spec says about it.** **Merged into BO-084 Approval Inbox as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-084: it renders inside BO-084's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 3 operations.** Unserved: Approve, Reject, Return for Change, Delegate. Each needs an operation, or needs removing from the screen …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Approvals for promotional changes (new promotion, discount depth, activation): the request with its discount exposure, revenue and margin impact, decided in place with approve, reject, return or request information.

**Fixed on main** (the package already carries these; draw what it says): "Delegate" is a decision button. (CHG-MOV-005); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listPromotions (PRICE_VIEW), listApprovalRequests … (CHG-MOV-001); requiresModule is 'marketing' on a TICVAI Console screen. (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Scheduled · Live · Paused · Expired · Ended | `listPromotions` ?status |
| Active at | date and time picker | — | — | `listPromotions` ?activeAt |
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| Promotion | text | not in the schema: `Promotion` |
| Request type | text | not in the schema: `Request type` |
| Requested by | text | not in the schema: `Requested by` |
| Requested date | text | not in the schema: `Requested date` |
| Discount exposure | text | not in the schema: `Discount exposure` |
| Revenue impact estimate | text | not in the schema: `Revenue impact estimate` |
| Margin impact | text | not in the schema: `Margin impact` |
| Campaign budget | text | not in the schema: `Campaign budget` |
| Risk level | text | not in the schema: `Risk level` |
| Requested activation date | text | not in the schema: `Requested activation date` |
| Current approval level | text | not in the schema: `Current approval level` |

**The selected promotion approval** (detail panel): The pack groups this record's detail under its own headings: “Approval can be required for”.

| Shows | Format | Notes |
|---|---|---|
| Promotion | text | not in the schema: `Promotion` |
| Request type | text | not in the schema: `Request type` |
| Requested by | text | not in the schema: `Requested by` |
| Requested date | text | not in the schema: `Requested date` |
| Discount exposure | text | not in the schema: `Discount exposure` |
| Revenue impact estimate | text | not in the schema: `Revenue impact estimate` |
| Margin impact | text | not in the schema: `Margin impact` |
| Campaign budget | text | not in the schema: `Campaign budget` |
| Risk level | text | not in the schema: `Risk level` |
| Requested activation date | text | not in the schema: `Requested activation date` |
| Current approval level | text | not in the schema: `Current approval level` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Return for Change (secondary button) | navigation or local | — | — | — | — |
| Request Information (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Impact columns**: Discount exposure and revenue impact as money with currency; margin impact as percentage points; requested activation date in the venue's dates. *(source: contracts/spine/approvals.yaml#listApprovalRequests; ADR-0008)*
- **Money columns (Discount exposure)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Data it reads**: `listPromotions` (onLoad, List promotions); `listApprovalRequests` (onLoad, Promotions awaiting a decision)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`
- → `BO-084` Approval Inbox: *Open Approval Inbox*; carries `approvalRequestId`, `requestId`

**What opens over it**

- confirmDialog *Reject*: **Reject on a promotion approval is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every request has been decided — this state offers no create action, because creating work is not what an empty inbox needs. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW, PRICE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for decideApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-084`: Same decision dialog as every approval.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Waiting for a decision:
- Promotion: 46
  Request type: Refund above threshold
  Requested by: Rahul Menon
  Requested date: 57
  Discount exposure: AED 12,400.00
  Revenue impact estimate: AED 12,400.00
  Margin impact: 233
  Campaign budget: 11
- Promotion: 312
  Request type: Price change
  Requested by: Fatima Al Mansoori
  Requested date: 11
  Discount exposure: AED 482,300.00
  Revenue impact estimate: AED 482,300.00
  Margin impact: 57
  Campaign budget: 128
- Promotion: 74
  Request type: Discount override
  Requested by: Omar Haddad
  Requested date: 128
  Discount exposure: AED 96,750.00
  Revenue impact estimate: AED 96,750.00
  Margin impact: 11
  Campaign budget: 46
```

#### Permissions

- `listPromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

21 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.12 | The system should be able to manage all promotions in Backoffice application, where the positioning of the promotions fits in with the mechanics of the booking platform. In this way the Shop Cart is … | Admission and Access | CONTRACTED | `listPromotions` |
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 9 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-145` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-145`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 14: Works in Promotion Approval Inbox → Provide one centralized approval workspace for promotional changes.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-145?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Reject, Return for Change, Request Information.
- [ ] Every transition is wired: `ADM-138`, `BO-084`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-146` Promotion Health & Performance Monitor

**Provide near-real-time operational performance monitoring while campaigns are running.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29961 (VM-ADM-146) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-health-performance-monitor-adm-146` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How running promotions perform: views, applications, redemptions, conversion, sales, discount, incremental revenue, margin, budget, compared with baseline, previous campaign, AI forecast and control group.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listPromotionHealthPerformance, listPromotionPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listPromotionHealthPerformance, listPromotionPerformance … (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date range | text field | — | — | `listPromotionPerformance` ?dateRange |
| Business entity | text field | — | — | `listPromotionPerformance` ?businessEntity |
| Venue | text field | — | — | `listPromotionPerformance` ?venue |
| Attraction | text field | — | — | `listPromotionPerformance` ?attraction |
| Campaign | text field | — | — | `listPromotionPerformance` ?campaign |
| Promotion | text field | — | — | `listPromotionPerformance` ?promotion |
| Bundle | text field | — | — | `listPromotionPerformance` ?bundle |
| Channel | text field | — | — | `listPromotionPerformance` ?channel |
| Customer segment | text field | — | — | `listPromotionPerformance` ?customerSegment |
| Product | text field | — | — | `listPromotionPerformance` ?product |
| Partner | text field | — | — | `listPromotionPerformance` ?partner |
| Market | text field | — | — | `listPromotionPerformance` ?market |
| Currency | text field | — | — | `listPromotionPerformance` ?currency |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Impressions** (metric tile)

**Promotion views** (metric tile)

**Eligible transactions** (metric tile)

**Promotion applications** (metric tile)

**Redemptions** (metric tile)

**Redemption rate** (metric tile)

**Conversion rate** (metric tile)

**Gross sales** (metric tile)

**Net sales** (metric tile)

**Discount granted** (metric tile)

**Incremental revenue** (metric tile)

**AOV uplift** (metric tile)

**Margin** (metric tile)

**Cost per redemption** (metric tile)

**Budget consumed** (metric tile)

**Budget remaining** (metric tile)

**Promotion vs baseline** (metric tile)

**Promotion vs previous campaign** (metric tile)

**Promotion vs AI forecast** (metric tile)

**Promotion vs control group** (metric tile)

**Channel vs channel** (metric tile)

**Venue vs venue** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **comparisons**: Each KPI with its comparison selector (baseline, previous, forecast, control group); incremental revenue is the headline, not gross sales. *(source: contracts/satellite/promotions.yaml#listPromotionHealthPerformance / contracts/satellite/promotions.yaml#simulatePromotion)*

**Data it reads**: `listPromotionHealthPerformance` (onLoad, Promotion Health & Performance Monitor); `listPromotionPerformance` (onLoad, Promotion Performance Command Center)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion health performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion health performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion health performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion health performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  redemptionRate: 6.2%
  incrementalRevenue: AED 84,300.00
  discountGranted: AED 31,900.00
  vsControl: +11%
```

#### Permissions

- `listPromotionHealthPerformance` → `PRICE_VIEW` (read) · staff
- `listPromotionPerformance` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-146` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-146`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 16: Works in Promotion Health & Performance Monitor → Provide near-real-time operational performance monitoring while campaigns are running.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-146?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-147` Promotion Audit, Activity & Version History

**Provide complete governance and traceability for every promotion. Board 2 is the core commercial rule engine for promotions. It shall allow authorized TICVAI business users to configure discount and promotion mechanics without development, including percentage and fixed discounts, transaction thresholds, volume discounts, bulk pricing, early-bird and last-minute offers, special guest pricing, payment-method discounts, partner discounts, and dynamic conditional discounts. The matrix explicitly requires percentage/value discounts, quantity thresholds, bulk discounts, early-bird/volume/customer-segment conditions, payment-type offers, group pricing, and special individual pricing. The board should contain 10 backend screens.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29977 (VM-ADM-147) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-audit-activity-version-history-adm-147` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every change to a promotion: who, role, when, previous and new value, reason, approval reference, version.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listPromotionActivityVersion return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-MOV-008)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From version | text field | — | — | `listPromotionActivityVersion` ?fromVersion |
| To version | text field | — | — | `listPromotionActivityVersion` ?toVersion |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View, Create, Edit, Submit, Approve, Activate, Pause, Suspend, Change budget, Archive, Export. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Version 2.3 ↔ Version 2.4 (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **audit trail**: Newest first, grouped by version, with before and after side by side. *(source: contracts/satellite/promotions.yaml#listPromotionActivityVersion)*

**Data it reads**: `listPromotionActivityVersion` (onLoad, Promotion Audit, Activity & Version History)

**Where the user goes next**

- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*; carries `promotionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion audit activity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion audit activity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion audit activity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion audit activity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  user: Noura Saeed
  role: Promotions manager
  at: 2026-11-10 11:42
  change: budgetCap AED 40,000.00 to AED 50,000.00
  reason: Extended to Abu Dhabi
```

#### Permissions

- `listPromotionActivityVersion` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-147` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS106 Promotions   Bundles Management Board 1.dc.html#adm-147`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 1
- Flow F154 *Promotions Bundles Management board 1: Promotion Command Center Dashboard*, step 18: Works in Promotion Audit, Activity & Version History → Provide complete governance and traceability for every promotion. Board 2 is the core commercial rule engine for promotions. It shall allow authorized TICVAI business users to configure discount and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-147?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Version 2.3 ↔ Version 2.4.
- [ ] Every transition is wired: `ADM-138`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
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
"createCommercialCampaign": {"method":"POST","path":"/commercial-campaigns","contract":"promotions","summary":"Create a commercial campaign","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCommercialCampaignRequest","responds":"CommercialCampaign"},
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"endPromotion": {"method":"POST","path":"/promotions/{promotionId}/end","contract":"promotions","summary":"End a promotion early","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getPromotion": {"method":"GET","path":"/promotions/{promotionId}","contract":"promotions","summary":"Read a promotion","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Promotion"},
"getPromotionUsage": {"method":"GET","path":"/promotions/{promotionId}/usage","contract":"promotions","summary":"Redemption count and discount given","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionUsage"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCampaignCalendarTimeline": {"method":"GET","path":"/campaign-calendar-timeline","contract":"promotions","summary":"Campaign Calendar & Timeline","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"promotionFamily","in":"query","required":false},{"name":"view","in":"query","required":false}],"requestBody":null,"responds":"CampaignCalendarTimelineView"},
"listCampaignPromotionPerformance": {"method":"GET","path":"/campaign-promotion-performance","contract":"promotions","summary":"Campaign & Promotion Performance Explorer","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CampaignPromotionPerformanceExplorerView"},
"listCommercialCampaigns": {"method":"GET","path":"/commercial-campaigns","contract":"promotions","summary":"List commercial campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":"ownerPrincipalId","in":"query","required":null},{"name":"q","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromotionActivityVersion": {"method":"GET","path":"/promotion-activity-version","contract":"promotions","summary":"Promotion Audit, Activity & Version History","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromVersion","in":"query","required":false},{"name":"toVersion","in":"query","required":false}],"requestBody":null,"responds":"PromotionAuditActivityVersionHistoryView"},
"listPromotionAlertException": {"method":"GET","path":"/promotion-alert-exception","contract":"promotions","summary":"Promotion Alerts & Exception Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionAlertsExceptionCenterView"},
"listPromotionCampaign": {"method":"GET","path":"/promotion-campaign","contract":"promotions","summary":"Promotion & Campaign Directory","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"promotionType","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"productCategory","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"fnb","in":"query","required":false},{"name":"retail","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"approvalState","in":"query","required":false},{"name":"promotionValue","in":"query","required":false},{"name":"budgetStatus","in":"query","required":false}],"requestBody":null,"responds":"PromotionCampaignDirectoryView"},
"listPromotionChannel": {"method":"GET","path":"/promotion-channel","contract":"promotions","summary":"Promotion Channel & Publication Monitor","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionChannelPublicationMonitorView"},
"listPromotionHealthPerformance": {"method":"GET","path":"/promotion-health-performance","contract":"promotions","summary":"Promotion Health & Performance Monitor","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PromotionHealthPerformanceMonitorView"},
"listPromotionLifecycleStatus": {"method":"GET","path":"/promotion-lifecycle-statu","contract":"promotions","summary":"Promotion Lifecycle & Status Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionLifecycleStatusManagerView"},
"listPromotionPerformance": {"method":"GET","path":"/promotion-performance","contract":"promotions","summary":"Promotion Performance Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"dateRange","in":"query","required":false},{"name":"businessEntity","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"promotion","in":"query","required":false},{"name":"bundle","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"currency","in":"query","required":false}],"requestBody":null,"responds":"PromotionPerformanceCommandCenterView"},
"listPromotions": {"method":"GET","path":"/promotions","contract":"promotions","summary":"List promotions","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"pausePromotion": {"method":"POST","path":"/promotions/{promotionId}/pause","contract":"promotions","summary":"Pause a live promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishPromotion": {"method":"POST","path":"/promotions/{promotionId}/publish","contract":"promotions","summary":"Publish a promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Promotion"},
"unschedulePromotion": {"method":"POST","path":"/promotions/{promotionId}/unschedule","contract":"promotions","summary":"Pull a scheduled promotion before it starts","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCommercialCampaign": {"method":"PATCH","path":"/commercial-campaigns/{campaignId}","contract":"promotions","summary":"Amend a commercial campaign","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CommercialCampaign"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CampaignBudget": {"x-ticvai-persistence":"promotions.campaign_budget","type":"object","description":"One budget line of a commercial campaign (setCampaignBudgetFinancial): what kind of spend it caps, who funds it, what it covers, and what happens as it is consumed. **Consumed, committed and reserved are not stored**: consumed is the discount given on orders (`orders.discount`, `promotions.promotion.discount_given`), committed and reserved are priced carts not yet paid, all worked out on read so they cannot drift from the orders they summarise. (DM5, 29 September: data model for the agreed operations)","required":["budgetType","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"budgetType":{"type":"string","enum":["total","discount","reward","freeProduct"],"description":"The spend this line caps (total campaign, discount, reward or free-product budget)."},"fundingSource":{"type":"string","nullable":true,"enum":["venue","department","marketing","partner"],"description":"Who pays for it; `partner` is a co-funded (e.g. bank or partner-funded) line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scope":{"type":"string","enum":["entireCampaign","promotion","product","channel","partner","customerSegment"],"default":"entireCampaign","description":"What the line covers."},"scopeRef":{"type":"string","nullable":true,"description":"The promotion, product, partner or segment id, or the SalesChannel value, that `scope` names. Null for `entireCampaign`."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The budget owner."},"costCentre":{"type":"string","maxLength":64,"nullable":true},"department":{"type":"string","maxLength":100,"nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"thresholdPolicy":{"$ref":"#/components/schemas/BudgetThresholdPolicy"}}},
"CampaignCalendarTimelineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Calendar & Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"calendarState":{"type":"string","enum":["active","upcoming","endingSoon","expired","pendingApproval","conflicting","suspended"],"description":"How the calendar marks this promotion."},"promotionId":{"type":"string","description":"Promotion ID"},"promotionName":{"type":"string","description":"Promotion Name"},"startDate":{"type":"string","format":"date-time","description":"Start Date"},"endDate":{"type":"string","format":"date-time","description":"End Date"},"venue":{"type":"string","description":"Venue"},"channel":{"type":"string","description":"Channel"}}},
"CampaignPromotionPerformanceExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign & Promotion Performance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"transactions":{"type":"string","description":"Transactions"},"units":{"type":"string","description":"Units"},"redemptions":{"type":"string","description":"Redemptions"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"margin":{"type":"number","description":"Margin"},"conversion":{"type":"number","description":"Conversion"},"aov":{"type":"string","description":"AOV"},"roi":{"type":"string","description":"ROI"},"customerAcquisition":{"type":"string","description":"Customer acquisition"},"repeatPurchase":{"type":"string","description":"Repeat purchase"},"marginRisk":{"type":"number","description":"Margin Risk"},"classification":{"type":"string","enum":["excellent","healthy","monitor","underperforming","critical"],"description":"AI/system classification."},"campaignId":{"type":"string","description":"Campaign ID"},"campaignName":{"type":"string","description":"Campaign"}}},
"CommercialCampaign": {"x-ticvai-persistence":"promotions.campaign + promotions.campaign_budget","type":"object","description":"A commercial campaign: the grouping of promotions, coupon campaigns and bundles that share an owner, a business entity, dates and a budget. **Not `marketing.campaign`**, which is the CRM send campaign in another service. The header is saved with its budget lines by setCampaignBudgetFinancial (the budget screen is where the pack captures campaign, owner, business entity and effective dates), and on its own by createCommercialCampaign and updateCommercialCampaign; listCommercialCampaigns lists it (decided 29 September, writers pass); promotions, coupon campaigns and bundles point at it by `campaignId`. No status of its own: a campaign is live while its promotions are, and a threshold action that stops it pauses them. (DM5, 29 September: data model for the agreed operations)","required":["id","venueId","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"budgets":{"type":"array","description":"The rows of `promotions.campaign_budget`, one per budget line.","items":{"$ref":"#/components/schemas/CampaignBudget"}}}},
"CreateCommercialCampaignRequest": {"x-ticvai-persistence":"none — request only; saved as a `promotions.campaign` row (CommercialCampaign)","type":"object","description":"What createCommercialCampaign takes: the campaign header only. Budget lines are set by setCampaignBudgetFinancial. (decided 29 September, writers pass)","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true,"description":"Unique at the venue when given."},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}},
"CreatePromotionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","x-ticvai-unique":"tenant","description":"**Unique per tenant** (6 October 2026, CHG-R4-015; the rule of audit R108 for configuration codes). A code already used by any promotion in the tenant, at any venue and in any state, is refused by `createPromotion` with `409 duplicate-code`. Compared case-insensitively.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"allOf":[{"$ref":"#/components/schemas/StackingMode"}],"default":"bestOnly"},"stackingGroup":{"type":"string","maxLength":64},"precedence":{"type":"integer","default":0,"description":"Higher evaluates first where several could apply."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptions":{"type":"integer","nullable":true},"maxRedemptionsPerGuest":{"type":"integer","nullable":true},"budgetCap":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"},"recommendable":{"type":"boolean","default":false,"description":"**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."},"recommendableSegmentIds":{"type":"array","nullable":true,"description":"The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.","items":{"type":"string","format":"uuid"}}}},
"Discount": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","required":["kind"],"properties":{"kind":{"$ref":"#/components/schemas/DiscountKind"},"percentage":{"type":"number","minimum":0,"maximum":100},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fixedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"buyQuantity":{"type":"integer","minimum":1},"getQuantity":{"type":"integer","minimum":1},"getDiscountPercentage":{"type":"number","minimum":0,"maximum":100,"description":"100 makes the free items actually free; lower values give a partial discount."},"tiers":{"type":"array","description":"For `tieredPercentage` — more units, larger discount.","items":{"type":"object","required":["minQuantity","percentage"],"properties":{"minQuantity":{"type":"integer","minimum":1},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"maxDiscountAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Cap on a percentage discount. Prevents an unbounded discount on a large basket."},"rewardVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (createPromotion; the builders setGiftFreeProduct and setBuyGetBogo were retired in r2, CHG-CLN-001). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"},"maxApplicationsPerBasket":{"type":"integer","minimum":1,"nullable":true,"description":"How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (createPromotion; setFixedPriceOffer was retired in r2, CHG-CLN-001). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"}}},
"GuestPromotion": {"x-ticvai-persistence":"none — guest projection of promotions.promotion","type":"object","description":"**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n","additionalProperties":false,"required":["id","code","name","discount","validFrom"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"$ref":"#/components/schemas/StackingMode"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptionsPerGuest":{"type":"integer","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Promotion": {"x-ticvai-persistence":"promotions.promotion","allOf":[{"$ref":"#/components/schemas/CreatePromotionRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/PromotionStatus"},"isPaused":{"type":"boolean"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"}}}]},
"PromotionAlertsExceptionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Alerts & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"alertType":{"type":"string","enum":["missingProduct","missingEligibility","invalidDates","invalidDiscount","invalidCode","missingApproval","budgetNearLimit","budgetExceeded","marginBelowThreshold","excessiveDiscountExposure","promotionFailedToPublish","productUnavailable","bundleComponentUnavailable","channelSynchronizationFailure","lowConversion","lowRedemption","unexpectedHighRedemption","campaignUnderperforming","abnormalCouponUsage","excessiveRepeatRedemption","suspiciousCustomerBehavior","promoCodeLeakage"],"description":"What the alert is about."},"severity":{"type":"string","enum":["information","warning","critical"],"description":"Alert severity."},"alertId":{"type":"string","description":"Alert ID"},"promotionId":{"type":"string","description":"Promotion ID"},"alertCategory":{"type":"string","enum":["configuration","financial","operational","commercial","fraudRisk"],"description":"The pack's alert group."},"raisedAt":{"type":"string","format":"date-time","description":"When the alert was raised"}}},
"PromotionAuditActivityVersionHistoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Audit, Activity & Version History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"user":{"type":"string","description":"User"},"role":{"type":"string","description":"Role"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"previousValue":{"type":"string","description":"Previous value"},"newValue":{"type":"integer","description":"New value"},"reason":{"type":"string","description":"Reason"},"approvalReference":{"type":"string","description":"Approval reference"},"promotionVersion":{"type":"string","description":"Promotion version"},"eventType":{"type":"string","enum":["promotionCreated","promotionEdited","ruleChanged","discountChanged","productAdded","productRemoved","eligibilityChanged","channelChanged","datesChanged","budgetChanged","approvalSubmitted","approvalGranted","approvalRejected","promotionActivated","promotionPaused","promotionSuspended","promotionExpired","promotionArchived"],"description":"What happened to the promotion."},"promotionId":{"type":"string","description":"Promotion ID"}}},
"PromotionCampaignDirectoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion & Campaign Directory displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promotionId":{"type":"string","description":"Promotion ID"},"promotionName":{"type":"string","description":"Promotion Name"},"promotionType":{"type":"string","description":"Promotion Type"},"campaign":{"type":"string","description":"Campaign"},"status":{"type":"string","description":"Status"},"businessEntity":{"type":"string","description":"Business Entity"},"venue":{"type":"string","description":"Venue"},"product":{"type":"string","description":"Product"},"targetSegment":{"type":"string","description":"Target Segment"},"channel":{"type":"string","description":"Channel"},"startDate":{"type":"string","format":"date-time","description":"Start Date"},"endDate":{"type":"string","format":"date-time","description":"End Date"},"discountType":{"type":"string","description":"Discount Type"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Value"},"budget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Budget"},"redemptionCount":{"type":"integer","description":"Redemption Count"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Generated"},"owner":{"type":"string","description":"Owner"},"approvalStatus":{"type":"string","description":"Approval Status"},"version":{"type":"string","description":"Version"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"statusesType":{"type":"string","enum":["draft","configurationIncomplete","simulationRequired","pendingApproval","approved","scheduled","active","paused","suspended","budgetExhausted","expired","cancelled","archived"],"description":"Vocabulary listed under Supported Statuses."}}},
"PromotionChannelPublicationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Channel & Publication Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelsType":{"type":"string","enum":["b2cWebsite","b2bPortal","pos","mobilePos","kiosk","mobileApp","callCenter","guestPortal","api","ota","reseller","partnerPortal","fBPos","retailPos"],"description":"Vocabulary listed under Supported Channels."},"promotionVersion":{"type":"string","description":"Promotion version"},"lastSynchronized":{"type":"string","format":"date-time","description":"Last synchronized"},"rulesPublished":{"type":"string","description":"Rules published"},"productsPublished":{"type":"string","description":"Products published"},"codeAvailability":{"type":"string","description":"Code availability"},"channelRestrictions":{"type":"integer","description":"Channel restrictions"},"errorMessages":{"type":"integer","description":"Error messages"},"publicationStatus":{"type":"string","enum":["notAssigned","pendingPublication","published","synchronizing","publicationFailed","outOfSync","suspended"],"description":"The promotion's publication status on this channel."}}},
"PromotionConditions": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","description":"All conditions must hold. An empty object matches everything.","properties":{"variantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productKinds":{"type":"array","items":{"type":"string"}},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minQuantity":{"type":"integer","minimum":1},"minBasketValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channels":{"type":"array","description":"Empty or absent matches every channel.","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"purchaseGate":{"type":"boolean","default":false,"description":"BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"},"paymentMethod":{"type":"array","nullable":true,"description":"BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n","items":{"type":"string"}},"issuerBins":{"type":"array","nullable":true,"description":"Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n","items":{"type":"string"}},"componentRedemption":{"type":"string","nullable":true,"enum":["allTogether","independently","sequenced"],"description":"BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresCoupon":{"type":"boolean","default":false},"firstPurchaseOnly":{"type":"boolean","default":false},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"advanceDaysMin":{"type":"integer","description":"Early-bird — booked at least this many days ahead."},"advanceDaysMax":{"type":"integer","description":"Last-minute — booked no more than this many days ahead."},"eligibilityRuleIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own) that must also hold. **Deprecated in r2** (CHG-CLN-001): setEligibilityRule, which saved library rules, was retired (BC-017), so no operation creates one; send the conditions inline. Rules already saved still apply. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"}}},
"PromotionHealthPerformanceMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Health & Performance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"impressions":{"type":"integer","description":"Impressions"},"promotionViews":{"type":"integer","description":"Promotion views"},"eligibleTransactions":{"type":"integer","description":"Eligible transactions"},"promotionApplications":{"type":"integer","description":"Promotion applications"},"redemptions":{"type":"integer","description":"Redemptions"},"redemptionRate":{"type":"number","description":"Redemption rate"},"conversionRate":{"type":"number","description":"Conversion rate"},"grossSales":{"type":"integer","description":"Gross sales"},"netSales":{"type":"integer","description":"Net sales"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount granted"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental revenue"},"aovUplift":{"type":"number","description":"AOV uplift"},"margin":{"type":"number","description":"Margin"},"costPerRedemption":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost per redemption"},"budgetConsumed":{"type":"string","description":"Budget consumed"},"budgetRemaining":{"type":"string","description":"Budget remaining"},"promotionVsBaseline":{"type":"string","description":"Promotion vs baseline"},"promotionVsPreviousCampaign":{"type":"string","description":"Promotion vs previous campaign"},"promotionVsAiForecast":{"type":"string","description":"Promotion vs AI forecast"},"promotionVsControlGroup":{"type":"string","description":"Promotion vs control group"},"channelVsChannel":{"type":"string","description":"Channel vs channel"},"venueVsVenue":{"type":"string","description":"Venue vs venue"}}},
"PromotionLifecycleStatusManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Lifecycle & Status Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"failedActivationChecks":{"type":"array","items":{"type":"string","enum":["requiredConfigurationCompleted","validProductsExist","datesValid","rulesDoNotConflict","budgetExistsWhereRequired","channelsAssigned","customerEligibilityExists","approvalCompleted"]},"description":"Activation checks this promotion currently fails; empty when it may activate. The service runs every check before activation and refuses activation while any fails."},"suspensionReason":{"type":"string","enum":["abnormalFinancialExposure","fraudDetected","incorrectDiscount","partnerRequest","inventoryUnavailable","budgetExhausted"],"description":"Why an authorised user suspended the promotion immediately (pack: 'suspend a promotion if')."},"promotionId":{"type":"string","description":"Promotion ID"},"promotionName":{"type":"string","description":"Promotion Name"},"status":{"$ref":"#/components/schemas/PromotionStatus","description":"The promotion's status (states/promotion.yaml)."},"lifecycleStage":{"type":"string","enum":["draft","validation","simulation","approval","scheduled","active","paused","suspended","expired","archived"],"description":"The pack's lifecycle stage for display. validation, simulation and approval are stages of a draft promotion (approval runs in the approvals engine); active is the live status; archived is an ended or expired promotion hidden from the working lists."}}},
"PromotionPerformanceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Performance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossSales":{"type":"integer","description":"Gross Sales"},"promotionInfluencedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion-Influenced Revenue"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Incremental Revenue"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Granted"},"netRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Revenue"},"grossMargin":{"type":"number","description":"Gross Margin"},"promotionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion Cost"},"roi":{"type":"string","description":"ROI"},"transactions":{"type":"integer","description":"Transactions"},"redemptions":{"type":"integer","description":"Redemptions"},"conversionRate":{"type":"number","description":"Conversion Rate"},"averageOrderValue":{"type":"number","description":"Average Order Value"},"revenuePerRedemption":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Redemption"},"activeCampaigns":{"type":"integer","description":"Active Campaigns"}}},
"PromotionStatus": {"type":"string","enum":["draft","scheduled","live","paused","expired","ended"]},
"PromotionUsage": {"x-ticvai-persistence":"none — aggregated from ledger and orders","type":"object","required":["promotionId","redemptionCount","discountGiven"],"properties":{"promotionId":{"type":"string","format":"uuid"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetRemaining":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBudgetExhausted":{"type":"boolean"},"byChannel":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"StackingMode": {"type":"string","description":"How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n","enum":["exclusive","stackable","bestOnly","stackWithGroup"]}
}
```
