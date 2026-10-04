# WS29 — Membership   Annual Pass Management board 1

**10 screens · 23 operations · 33 schemas · 6 permissions**

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
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-284` | Membership & Annual Pass Command Center | B | 11 | 228 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-285` | Membership Product & Tier Builder | B | 48 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | B | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-287` | Validity, Activation & Expiry Configuration | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | B | 14 | 0 | 5 | 25 | 0 | 0 | — | notStarted (generated) |
| `BO-289` | Membership Usage, Visit & Consumption Rules | B | 19 | 20 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `BO-290` | Family, Household & Dependent Membership Configuration | B | 21 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-291` | Membership Commercial, Pricing & Channel Association | B | 35 | 0 | 5 | 4 | 0 | 0 | — | notStarted (generated) |
| `BO-292` | Renewal, Auto-Renewal & Membership Continuity Configuration | B | 11 | 0 | 5 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-293` | Membership Product Validation, Approval, Publication & Versioning | B | 14 | 69 | 5 | 0 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**BO-287, BO-289 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-284` Membership & Annual Pass Command Center

**Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29857 (VM-BO-284) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Identify) and no metric row |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/sell/membership-annual-pass-command-center-bo-284` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The guest membership and annual-pass board's hub for the tenant's membership team: products by type and tier, members, expiring and renewal-enabled products, configuration issues. "Membership" here is the guest's pass, not the tenant's TICVAI subscription.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMembershipAnnualPass (PLATFORM_TENANT_VIEW), approveMembershipProductValidation (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Membership types (Monthly, Fixed-Term, Corporate...) are drawn as buttons. (CHG-SBO-015); Reaches approveMembershipProductValidation (step-up mfa) and declares no way to raise the challenge. (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership type | multi select | — | — | — | — | Monthly, fixed-term, corporate, family, individual, student, VIP or custom: a filter (and the type chosen when creating), not buttons. | — |
| Authentication code | text field | — | — | — | — | Asked in the confirmation of the approval: `approveMembershipProductValidation` is step-up mfa and refuses without a fresh token. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership type | select | — | Annual pass · Season pass · Monthly membership · Fixed term membership · Corporate membership · Family membership · Individual membership · Student membership · Vip membership · Custom membership | `listMembershipAnnualPass` ?membershipType |
| Status | select | — | Draft · In review · Approved · Scheduled · Active · Suspended · Expired · Retired | `listMembershipAnnualPass` ?status |
| Tier | text field | — | — | `listMembershipAnnualPass` ?tier |
| Venue | text field | — | — | `listMembershipAnnualPass` ?venue |
| Has configuration issues | toggle | — | — | `listMembershipAnnualPass` ?hasConfigurationIssues |
| Search | text field | — | — | `listMembershipAnnualPass` ?search |

**Sent by *Suspend membership product*** (`approveMembershipProductValidation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Migration policy `migrationPolicy` | segmented control | optional | — | Remain on current version · Move at next renewal · Move on effective date | — | Migration policy for existing member contracts (pack p.18). | `approveMembershipProductValidation` body |
| Membership code `membershipCode` | text field | optional | — | — | — | Membership code | `approveMembershipProductValidation` body |
| Version `version` | number field | optional | — | — | — | Configuration version the decision applies to | `approveMembershipProductValidation` body |
| Action `action` | select | optional | — | Validate · Submit for review · Approve commercial · Approve operational · Reject · Schedule · Publish · Suspend · Reinstate | — | Decision taken on BO-293; `suspend` (from `active`, reason required) and `reinstate` (from `suspended`) are the BO-284 quick actions (decided 29 September, writers pass; DM4) | `approveMembershipProductValidation` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective date for schedule/publish | `approveMembershipProductValidation` body |
| Reason `reason` | text area | optional | — | — | — | Reason, recorded in the audit | `approveMembershipProductValidation` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Shown**

**Active Membership Products** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Annual Pass Products** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Draft Products** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Active Members** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Family Memberships** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Memberships expiring soon** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Renewal-Enabled Products** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Suspended Products** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Products with configuration issues** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Average membership duration** (metric tile, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |
| Code | chip: Missing entitlements, Missing pricing association, Missing validity, Invalid … | — |
| Message | text | — |
| AI insights | list or chips (count when long) | AI Assistance: advisory observations only; never applied automatically (pack AI sections) |
| Next cursor | text | — |

**Every membership annual pass** (data table, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |

**The selected membership annual pass** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product ID |
| Membership name | text | Membership Name |
| Type | chip: Annual pass, Season pass, Monthly membership, Fixed term membership, Corporate … | Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type |
| Tier | text | Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names) |
| Venue attraction | text | Venue/Attraction the membership admits to |
| Validity method | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method (pack p.8 Validity Methods) |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method (pack pp.8-9) |
| Renewal mode | chip: Manual, Customer self service, Agent assisted, Auto renewal, Invitation only, Non … | Renewal: the product's primary renewal mode (pack p.15 Renewal Modes) |
| Membership structure | chip: Individual, Couple, Family, Household, Parent child, Corporate group… | Family/Individual: the membership structure (pack p.12 Membership Structures) |
| Current members | 1,234 | Current Members |
| Effective from | 1 Oct 2026 | Effective From: the date the current version becomes sellable |
| Status | text | Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses) |
| Owner | text | Owner |
| Validation issues | list or chips (count when long) | Configuration Health (pack p.5): the checks this product currently fails |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Suspend membership product (destructive button) | `approveMembershipProductValidation` PUT `/membership-product-validation` | MembershipProductValidationApprovalPublicationVersioInput | MembershipProductValidationApprovalPublicationVersioView | 409 The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass …; 422 A suspend sent without a reason … | step-up: mfa (Platform-level product state, across tenants.); gated `PLATFORM_CELL_MANAGE` |
| Reinstate membership product (secondary button) | `approveMembershipProductValidation` PUT `/membership-product-validation` | MembershipProductValidationApprovalPublicationVersioInput | MembershipProductValidationApprovalPublicationVersioView | 409 The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass …; 422 A suspend sent without a reason … | step-up: mfa (Platform-level product state, across tenants.); gated `PLATFORM_CELL_MANAGE` |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Suspend / Reinstate membership product**: Suspending stops new sales; existing members keep their entitlement until expiry; the confirmation states the number of current members. *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*
- **Suspend membership product**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends approveMembershipProductValidation with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Platform-level product state, across tenants. *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Data it reads**: `listMembershipAnnualPass` (onLoad, Membership & Annual Pass Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-285` Membership Product & Tier Builder: *Works in Membership Product & Tier Builder*; calls `listMembershipAnnualPass`
- → `BO-286` Membership Eligibility & Qualification Rule Builder: *Works in Membership Eligibility & Qualification Rule Builder*; calls `listMembershipAnnualPass`
- → `BO-287` Validity, Activation & Expiry Configuration: *Works in Validity, Activation & Expiry Configuration*; calls `listMembershipAnnualPass`
- → `BO-288` Membership Entitlement & Admission Benefit Builder: *Works in Membership Entitlement & Admission Benefit Builder*; calls `listMembershipAnnualPass`
- → `BO-289` Membership Usage, Visit & Consumption Rules: *Works in Membership Usage, Visit & Consumption Rules*; calls `listMembershipAnnualPass`
- → `BO-290` Family, Household & Dependent Membership Configuration: *Works in Family, Household & Dependent Membership Configuration*; calls `listMembershipAnnualPass`
- → `BO-291` Membership Commercial, Pricing & Channel Association: *Works in Membership Commercial, Pricing & Channel Association*; calls `listMembershipAnnualPass`
- → `BO-292` Renewal, Auto-Renewal & Membership Continuity Configuration: *Works in Renewal, Auto-Renewal & Membership Continuity Configuration*; calls `listMembershipAnnualPass`
- → `BO-293` Membership Product Validation, Approval, Publication & Versioning: *Works in Membership Product Validation, Approval, Publication & Versioning*; carries `challengeId`, `membershipCode`, `version`; calls `listMembershipAnnualPass`

**What opens over it**

- confirmDialog *Suspend membership product*: **Names what suspending stops and what it leaves alone**: the membership product and version, every channel it stops selling on, and that members already holding it keep their entitlements until their own expiry. **Collects what `approveMembershipProductValidation` sends before it is called.** …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership annual pass list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership annual pass untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership annual pass yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership annual pass are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass …; 422 A suspend sent without a reason (`reason-required`) (decided 29 September, writers pass; DM4); 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Suspend membership product. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*
- **approveMembershipProductValidation answers 409**: Show it as something the person can act on, not a failure: The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass; DM4) *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*
- **approveMembershipProductValidation answers 422**: Show it as something the person can act on, not a failure: A suspend sent without a reason (`reason-required`) (decided 29 September, writers pass; DM4) *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
products:
- name: AquaCove Annual Pass Gold
  type: annualPass
  tier: Gold
  members: 4210
  renewal: auto
- name: AquaCove Family Pass
  type: familyMembership
  tier: Silver
  members: 1385
  renewal: manual
```

#### Permissions

- `listMembershipAnnualPass` → `PLATFORM_TENANT_VIEW` (read) · staff
- `approveMembershipProductValidation` → `PLATFORM_CELL_MANAGE` (configure) · staff · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-284` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-284`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 1: Opens Membership & Annual Pass Command Center → Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F138 branch at step 1 (expected): when Nothing has been set up on Membership & Annual Pass Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F138 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409, 410, 422).
- [ ] Every output is drawn (228 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-284?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Suspend membership product, Reinstate membership product, Email me a code instead.
- [ ] Every transition is wired: `BO-100`, `BO-285`, `BO-286`, `BO-287`, `BO-288`, `BO-289`, `BO-290`, `BO-291`, `BO-292`, `BO-293`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-285` Membership Product & Tier Builder

**Configure the fundamental definition and hierarchy of a membership/pass.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29249 (VM-BO-285) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE`, `PRODUCT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Define; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-product-tier-builder-bo-285` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Define a membership product and its place in the tier hierarchy: name, code, type, venue or attraction, market, currency context, effective dates, tier level, upgrade and downgrade paths. A change to an active product creates a new version.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setMembershipProductTier (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Fields drawn as drop-downs that cannot be choices: text field: Membership Name, Membership Code, Description, Brand, Venue, Attraction … (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership Name | text field | optional | — | — | — | Membership Name | `MembershipProductTierBuilderInput.membershipName` |
| Membership Code | text field | optional | — | — | — | Membership Code | `MembershipProductTierBuilderInput.membershipCode` |
| Description | text area | optional | — | — | — | Description | `MembershipProductTierBuilderInput.description` |
| Membership Type | select | optional | — | Annual pass · Season pass · Monthly membership · Fixed term membership · Corporate membership · Family membership · Individual membership · Student membership · Vip membership · Custom membership | — | Membership Type (pack pp.4-5) | `MembershipProductTierBuilderInput.membershipType` |
| Brand | text field | optional | — | — | — | Brand | `MembershipProductTierBuilderInput.brand` |
| Venue | text field | optional | — | — | — | Venue | `MembershipProductTierBuilderInput.venue` |
| Attraction | text field | optional | — | — | — | Attraction | `MembershipProductTierBuilderInput.attraction` |
| Market | text field | optional | — | — | — | Market | `MembershipProductTierBuilderInput.market` |
| Currency Context | select field | — | — | — | — | — | — |
| Effective From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective From | `MembershipProductTierBuilderInput.effectiveFrom` |
| Effective To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective To; empty for open-ended | `MembershipProductTierBuilderInput.effectiveTo` |
| Tier Level | number field | optional | — | — | — | Tier Level: rank within the membership family; higher is more premium | `MembershipProductTierBuilderInput.tierLevel` |
| Display Order | number field | optional | — | — | — | Display Order in listings and upgrade choices | `MembershipProductTierBuilderInput.displayOrder` |
| Upgrade Path | select field | — | — | — | — | — | — |
| Downgrade Path | select field | — | — | — | — | — | — |
| Parent Membership | select field | — | — | — | — | — | — |
| Replacement Membership | select field | — | — | — | — | — | — |
| Individual / Family / Corporate | text field | — | — | — | — | — | — |
| Named / Transferable | select field | — | — | — | — | — | — |
| Physical / Digital | select field | — | — | — | — | — | — |
| Renewable / Non-Renewable | select field | — | — | — | — | — | — |
| Auto-Renew Eligible | select field | — | — | — | — | — | — |
| Admission-Based / Benefit-Based / Hybrid | text field | — | — | — | — | — | — |

**Form: Save membership product** (modal, opened by *Save membership product*; *Save membership product* calls `setMembershipProductTier`, *Cancel* sends nothing)

**Collects what `setMembershipProductTier` sends before it is called.** Nothing in the body is required. Optional: `membershipName`, `membershipCode`, `description`, `membershipType`, `brand`, `venue`, `attraction`, `market`, `currencyContext`, `effectiveFrom`, `effectiveTo`, `tierLevel`, `displayOrder`, `parentMembership`, `replacementMembership`, `holderModel`, `transferable`, `credentialForm`, `renewable`, `autoRenewEligible`, `benefitModel`, `tier`, `upgradePath`, `downgradePath`, `catalogueProductId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Membership name `membershipName` | text field | optional | — | — | — | Membership Name | `setMembershipProductTier` body |
| Membership code `membershipCode` | text field | optional | — | — | — | Membership Code | `setMembershipProductTier` body |
| Description `description` | text area | optional | — | — | — | Description | `setMembershipProductTier` body |
| Membership type `membershipType` | select | optional | — | Annual pass · Season pass · Monthly membership · Fixed term membership · Corporate membership · Family membership · Individual membership · Student membership · Vip membership · Custom membership | — | Membership Type (pack pp.4-5) | `setMembershipProductTier` body |
| Brand `brand` | text field | optional | — | — | — | Brand | `setMembershipProductTier` body |
| Venue `venue` | text field | optional | — | — | — | Venue | `setMembershipProductTier` body |
| Attraction `attraction` | text field | optional | — | — | — | Attraction | `setMembershipProductTier` body |
| Market `market` | text field | optional | — | — | — | Market | `setMembershipProductTier` body |
| Currency context `currencyContext` | text field | optional | — | — | — | Currency Context: ISO 4217 currency code the product is sold in | `setMembershipProductTier` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective From | `setMembershipProductTier` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective To; empty for open-ended | `setMembershipProductTier` body |
| Tier level `tierLevel` | number field | optional | — | — | — | Tier Level: rank within the membership family; higher is more premium | `setMembershipProductTier` body |
| Display order `displayOrder` | number field | optional | — | — | — | Display Order in listings and upgrade choices | `setMembershipProductTier` body |
| Parent membership `parentMembership` | text field | optional | — | — | — | Parent Membership: code of the membership family this tier belongs to | `setMembershipProductTier` body |
| Replacement membership `replacementMembership` | text field | optional | — | — | — | Replacement Membership: code of the product that replaces this one when it is retired | `setMembershipProductTier` body |
| Holder model `holderModel` | segmented control | optional | — | Individual · Family · Corporate | — | Individual / Family / Corporate (pack p.6 Product Characteristics) | `setMembershipProductTier` body |
| Transferable `transferable` | toggle | optional | — | — | — | Named / Transferable: true when the membership may be transferred; false (the default) keeps it named to one member (decided 29 September, readiness close-out) | `setMembershipProductTier` body |
| Credential form `credentialForm` | segmented control | optional | — | Physical · Digital · Both | — | Physical / Digital credential form | `setMembershipProductTier` body |
| Renewable `renewable` | toggle | optional | — | — | — | Renewable / Non-Renewable: true when the membership can be renewed | `setMembershipProductTier` body |
| Auto renew eligible `autoRenewEligible` | toggle | optional | — | — | — | Auto-Renew Eligible: the product may be auto-renewed; a member is only auto-renewed after their own explicit opt-in. | `setMembershipProductTier` body |
| Benefit model `benefitModel` | segmented control | optional | — | Admission based · Benefit based · Hybrid | — | Admission-Based / Benefit-Based / Hybrid | `setMembershipProductTier` body |
| Tier `tier` | text field | optional | — | — | — | Tier: Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names (pack p.6 Tier Configuration) | `setMembershipProductTier` body |
| Upgrade path `upgradePath` | list of values (chips) | optional | — | — | — | Upgrade Path: membership codes this tier may upgrade to (pack p.6 Tier Relationships; the transaction runs in Area 11) | `setMembershipProductTier` body |
| Downgrade path `downgradePath` | list of values (chips) | optional | — | — | — | Downgrade Path: membership codes this tier may downgrade to | `setMembershipProductTier` body |
| Catalogue product `catalogueProductId` | text field | optional | — | — | — | Catalogue Association: the sellable product in the Ticketing Catalogue this membership configures (a membership ProductKind) | `setMembershipProductTier` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Membership code**: Unique per tenant; a clash is the duplicate-code refusal. *(source: R108)*
- **Effective dates**: Effective To must follow Effective From; dates in the region's format. *(source: designer default)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setMembershipProductTier: tenant-wide only, no region or venue override is offered; setMembershipProgramme: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setMembershipProductTier; contracts/spine/catalogue.yaml#setMembershipProgramme)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save membership product (primary button) | `setMembershipProductTier` PUT `/membership-product-tier` | MembershipProductTierBuilderInput | MembershipProductTierBuilderView | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Versioning**: Saving an active product says "creates version N; current members stay on version N-1 until renewal". *(source: contracts/satellite/subscription.yaml#/components/schemas/MembershipProductTierBuilderInput)*

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipProductTier`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership product tier configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership product tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership product tier configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Membership Name: 11
  Membership Code: 128
  Description: 233
  Membership Type: seasonPass
  Brand: 46
  Venue: AquaCove Muscat
  Attraction: 128
  Market: 233
  Currency Context: 128
  Effective From: 01/11/2026
  Effective To: 15/10/2026 00:00
  Tier Level: 233
  Display Order: 46
  Upgrade Path: 46
```

#### Permissions

- `setMembershipProductTier` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `setMembershipProgramme` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-285` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-285`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 2: Works in Membership Product & Tier Builder → Configure the fundamental definition and hierarchy of a membership/pass.

#### Acceptance for the design

- [ ] Every input above is drawn (48), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-285?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save membership product.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-286` Membership Eligibility & Qualification Rule Builder

**Determine who is allowed to purchase, activate, hold or renew a particular membership.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29240 (VM-BO-286) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether qualification requires) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-eligibility-qualification-rule-builder-bo-286` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who may buy, activate, hold or renew a membership: exclusivity, prerequisites, verification level.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setMembershipEligibilityQualification (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Multiple Memberships Allowed | select field | — | — | — | — | — | — |
| One Membership per Customer | text field | — | — | — | — | — | — |
| Mutually Exclusive Memberships | select field | — | — | — | — | — | — |
| Prerequisite Membership | select field | — | — | — | — | — | — |
| Existing Tier Requirement | select field | — | — | — | — | — | — |
| No Verification | select field | — | — | — | — | — | — |
| Customer Declaration | select field | — | — | — | — | — | — |
| Document Verification | select field | — | — | — | — | — | — |
| Identity Verification | select field | — | — | — | — | — | — |
| Staff Verification | select field | — | — | — | — | — | — |
| External Verification | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipEligibilityQualification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership eligibility qualification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership eligibility qualification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership eligibility qualification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Multiple Memberships Allowed: 19
  One Membership per Customer: Desert Gate Tours LLC
  Mutually Exclusive Memberships: 128
  Prerequisite Membership: 312
  Existing Tier Requirement: 233
  No Verification: 19
  Customer Declaration: Marina Leisure Group
  Document Verification: 19
  Identity Verification: 233
  Staff Verification: 74
  External Verification: 11
```

#### Permissions

- `setMembershipEligibilityQualification` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-286` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-286`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 4: Works in Membership Eligibility & Qualification Rule Builder → Determine who is allowed to purchase, activate, hold or renew a particular membership.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-286?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-287` Validity, Activation & Expiry Configuration

**Define exactly when a membership becomes valid, how long it remains valid and how it expires.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29241 (VM-BO-287) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/validity-activation-expiry-configuration-bo-287` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** When a membership becomes valid, how long it lasts and how it expires (from purchase, first visit, fixed date).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setValidityActivationExpiry (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setValidityActivationExpiry`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validity activation expiry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validity activation expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validity activation expiry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validity activation expiry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
validity:
  activation: first visit
  duration: 12 months
  activationDeadline: 90 days from purchase
  graceDays: 7
```

#### Permissions

- `setValidityActivationExpiry` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-287` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-287`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 6: Works in Validity, Activation & Expiry Configuration → Define exactly when a membership becomes valid, how long it remains valid and how it expires.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-287?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-288` Membership Entitlement & Admission Benefit Builder

**Define exactly what the member receives. This is the heart of the membership product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29880 (VM-BO-288) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/sell/membership-entitlement-admission-benefit-builder-bo-288` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Exactly what a member receives per tier: admission entitlements and benefits (discounts, guest passes, parking, fast track), each with its limit and period. The heart of the membership product.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- setMembershipEntitlementAdmission requires PLATFORM_CELL_MANAGE (a platform permission) at tenant scope, on a venue screen. (CHG-SBO-005)
- List operation(s) listEntitlementTemplates return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Event Type | select field | — | — | — | — | — | — |
| Admission Type | select field | — | — | — | — | — | — |
| Number of Visits | select field | — | — | — | — | — | — |
| Period | select field | — | — | — | — | — | — |
| Days | select field | — | — | — | — | — | — |
| Times | select field | — | — | — | — | — | — |
| Timeslots | select field | — | — | — | — | — | — |
| Per Day | select field | — | — | — | — | — | — |
| Per Week | select field | — | — | — | — | — | — |
| Per Month | select field | — | — | — | — | — | — |
| Per Membership Year | select field | — | — | — | — | — | — |
| Lifetime of Membership | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **benefits**: A list per tier, each benefit with type, value and unit (10% off F&B, 4 guest passes a year), linked to an entitlement template where it grants entry; the plan's benefit set is replaced whole. *(source: contracts/spine/catalogue.yaml#setMembershipBenefit / contracts/spine/catalogue.yaml#setPlanBenefits)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Attraction Access (primary button) | navigation or local | — | — | — | — |
| Event Access (secondary button) | navigation or local | — | — | — | — |
| Zone Access (secondary button) | navigation or local | — | — | — | — |
| Priority Entry (secondary button) | navigation or local | — | — | — | — |
| Guest Tickets (secondary button) | navigation or local | — | — | — | — |
| F&B Benefit (secondary button) | navigation or local | — | — | — | — |
| Retail Benefit (secondary button) | navigation or local | — | — | — | — |
| Rental Benefit (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **tier comparison**: Tiers as columns, benefits as rows, so Gold and Platinum can be compared. *(source: designer default)*

**Data it reads**: `listEntitlementTemplates` (onLoad, The membership plan templates whose benefits are set)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipEntitlementAdmission`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership entitlement admission configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership entitlement admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership entitlement admission configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-012`: Same entitlement templates and wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tier:
  membership: Annual Pass
  tier: Gold
  benefits:
  - Unlimited entry
  - 10% off Harbour Kitchen
  - 4 guest passes a year
  - Free parking
```

#### Permissions

- `setMembershipEntitlementAdmission` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `setMembershipBenefit` → `PRODUCT_CONFIGURE` (configure) · staff
- `setPlanBenefits` → `PRODUCT_CONFIGURE` (configure) · staff
- `listEntitlementTemplates` → `PRODUCT_VIEW` (read) · staff
- `createEntitlementTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.32 | Membership & Annual Pass Sales | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 2.14.11 | Support validity periods, renewals and expiry rules. | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 5.3.15 | Maintain membership type, tier, status, activation date, expiration date, benefits, renewal history, suspension history, and usage history. | F&B & Guest Management | CONTRACTED | `listEntitlementTemplates` |
| 6.1.37 | The system should be able to provide aging report for ticketing & reward age. | Retail POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.21 | For each PLU, it is possible to manage a validity date range | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.23 | For each PLU, it is possible to manage Events having a scheduled usage, based on slot date and time | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.24 | For each PLU, it is possible to have Capacity management rules (valid until there is no available place) | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.29 | For each PLU, it is possible to Allow re-entry or not | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 1.1.5 | The system should be able to sell multiple day tickets for attractions. The number of days should be configurable. This type of ticket should require a start date to be specified before first entry. | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.9 | The system should allow the validity period for a ticket to be configurable. For open-dated tickets, the validity period is intended to define the mandatory date by which the ticket must be used. For … | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.11 | The system should allow the number of entitled access per ticket to be configurable (N entries to Y access areas). Some tickets will allow only access once per attraction while some tickets will … | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.16 | System shall allow administrators to create reusable ticket templates containing pricing, validity, capacity, access rights, add-ons, restrictions and approval workflows. | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-288` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-288`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 8: Works in Membership Entitlement & Admission Benefit Builder → Define exactly what the member receives. This is the heart of the membership product.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-288?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Attraction Access, Event Access, Zone Access, Priority Entry, Guest Tickets, F&B Benefit, Retail Benefit, Rental Benefit.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-289` Membership Usage, Visit & Consumption Rules

**Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29788 (VM-BO-289) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Maintain counters such as) and no metric row |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/sell/membership-usage-visit-consumption-rules-bo-289` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How membership entitlements are consumed: visits per period, blackout dates, guest tickets, benefits.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMembershipUsageVisit (PLATFORM_TENANT_VIEW), setMembershipUsagePolicy (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership code | text field | — | — | `listMembershipUsageVisit` ?membershipCode |
| Tier | text field | — | — | `listMembershipUsageVisit` ?tier |

**Form: Save membership usage policy** (modal, opened by *Save membership usage policy*; *Save membership usage policy* calls `setMembershipUsagePolicy`, *Cancel* sends nothing)

**Collects what `setMembershipUsagePolicy` sends before it is called.** Required: `membershipCode`, `reEntryPolicy`, `reservationRequirement`. Optional: `tier`, `maximumVisitsPerDay`, `maximumAdmissionsPerPeriod`, `admissionPeriod`, `reEntryCooldownMinutes`, `walkInAllowed`, `maximumAdvanceBookingDays`, `maximumActiveFutureReservations`, `concurrentReservations`, `noShowTreatment`, `noShowThreshold`, `noShowWindowDays` and 4 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Membership code `membershipCode` | text field | required | — | — | — | The membership product (subscription.membership_product) whose rules these are. | `setMembershipUsagePolicy` body |
| Tier `tier` | text field | optional | — | — | — | Tier, where the product code covers several tiers. | `setMembershipUsagePolicy` body |
| Maximum visits per day `maximumVisitsPerDay` | number field | optional | — | min 1 | — | Maximum Visits per Day; empty for unlimited | `setMembershipUsagePolicy` body |
| Maximum admissions per period `maximumAdmissionsPerPeriod` | number field | optional | — | min 1 | — | Maximum Admissions per admissionPeriod; empty for unlimited | `setMembershipUsagePolicy` body |
| Admission period `admissionPeriod` | radio group | optional | — | Per day · Per week · Per month · Per membership year | — | Period for maximumAdmissionsPerPeriod; required when that is set | `setMembershipUsagePolicy` body |
| Re entry policy `reEntryPolicy` | radio group | required | — | Unlimited same day · No re entry · After minutes · Venue specific | — | Re-entry (pack p.12) | `setMembershipUsagePolicy` body |
| Re entry cooldown minutes `reEntryCooldownMinutes` | number field (minutes) | optional | — | min 1 | — | Re-entry Cooldown in minutes; required for reEntryPolicy afterMinutes | `setMembershipUsagePolicy` body |
| Reservation requirement `reservationRequirement` | segmented control | required | — | Required · Optional | — | Advance Reservation (pack pp.11-12) | `setMembershipUsagePolicy` body |
| Walk in allowed `walkInAllowed` | toggle | optional | on | — | — | Walk-In Allowed without a reservation | `setMembershipUsagePolicy` body |
| Maximum advance booking days `maximumAdvanceBookingDays` | number field (days) | optional | — | min 0 | — | Maximum Advance Booking Days | `setMembershipUsagePolicy` body |
| Maximum active future reservations `maximumActiveFutureReservations` | number field | optional | — | min 1 | — | Maximum Active Future Reservations | `setMembershipUsagePolicy` body |
| Concurrent reservations `concurrentReservations` | number field | optional | 1 | min 1 | — | Concurrent Reservations: maximum active reservations per timeslot. | `setMembershipUsagePolicy` body |
| No show treatment `noShowTreatment` | segmented control | optional | None | None · Restrict reservations | — | No-Show Treatment (pack p.12) | `setMembershipUsagePolicy` body |
| No show threshold `noShowThreshold` | number field | optional | — | min 1 | — | No-shows that trigger the restriction; required for restrictReservations | `setMembershipUsagePolicy` body |
| No show window days `noShowWindowDays` | number field (days) | optional | — | min 1 | — | Window in which no-shows are counted; required for restrictReservations | `setMembershipUsagePolicy` body |
| No show restriction days `noShowRestrictionDays` | number field (days) | optional | 14 | min 1 | — | Days reservation privilege stays restricted. | `setMembershipUsagePolicy` body |
| Cancellation limit `cancellationLimit` | number field | optional | — | min 0 | — | Reservation cancellations allowed per 30 days; empty for unlimited | `setMembershipUsagePolicy` body |
| Guest usage `guestUsage` | segmented control | optional | With member only | With member only · Independent | — | Guest Usage: whether guest tickets need the member present | `setMembershipUsagePolicy` body |
| Benefit consumption `benefitConsumption` | segmented control | optional | On redemption | On redemption · On validated visit | — | Benefit Consumption: when a benefit counter decrements | `setMembershipUsagePolicy` body |

Errors to draw in the form: 404 No membership product with this code; 409 The product version is retired or expired and cannot take new rules; 422 A conditional field is missing (cooldown for afterMinutes, the no-show triple for restrictReservations, the period for an admissions limit)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setMembershipUsagePolicy: tenant-wide only, no region or venue override is offered; setPlanBenefits: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/catalogue.yaml#setPlanBenefits; contracts/satellite/subscription.yaml#setMembershipUsagePolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every membership usage visit** (data table, from `listMembershipUsageVisit`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Maximum visits per day | 1,234 | Maximum Visits per Day; empty for unlimited |
| Maximum admissions per period | 1,234 | Maximum Admissions per admissionPeriod; empty for unlimited |
| Re entry cooldown minutes | 1,234 | Re-entry Cooldown in minutes, for reEntryPolicy afterMinutes |
| Concurrent reservations | 1,234 | Concurrent Reservations: maximum active reservations per timeslot (pack example: one). |
| No show treatment | chip: None, Restrict reservations | No-Show Treatment (pack p.12) |
| Cancellation limit | 1,234 | Cancellation Limit: reservation cancellations allowed per 30 days; empty for unlimited (decided 29 September, readiness close-out) |
| Guest usage | chip: With member only, Independent | Guest Usage: whether guest tickets need the member present. |
| Benefit consumption | chip: On redemption, On validated visit | Benefit Consumption: when a benefit counter decrements. |
| Walk in allowed | yes / no (icon or chip) | Walk-In Allowed without a reservation |
| Maximum advance booking days | 1,234 | Maximum Advance Booking Days |
| Maximum active future reservations | 1,234 | Maximum Active Future Reservations |
| Membership code | text | Membership code |
| Tier | text | Tier |
| Admission period | chip: Per day, Per week, Per month, Per membership year | Period for maximumAdmissionsPerPeriod |
| Re entry policy | chip: Unlimited same day, No re entry, After minutes, Venue specific | Re-entry (pack p.12) |
| Reservation requirement | chip: Required, Optional | Advance Reservation (pack pp.11-12) |
| No show threshold | 1,234 | No-shows that trigger the restriction (pack example: 3) |
| No show window days | 1,234 | Window in which no-shows are counted (pack example: 30 days) |
| No show restriction days | 1,234 | Days reservation privilege stays restricted. |

**The selected membership usage visit** (detail panel): The pack groups this record's detail under its own headings: “Unlimited annual visits”, “Access Integration”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save membership usage policy (primary button) | `setMembershipUsagePolicy` PUT `/membership-usage-policy` | MembershipUsagePolicyInput | MembershipUsageVisitConsumptionRulesView | 404 No membership product with this code; 409 The product version is retired or expired and cannot take new rules; 422 A conditional field is missing (cooldown for afterMinutes, the no-show triple for … | gated `PLATFORM_CELL_MANAGE`; opens modal first |

**Data it reads**: `listMembershipUsageVisit` (onLoad, Membership Usage, Visit & Consumption Rules); `listEntitlementTemplates` (onLoad, The membership plan templates whose usage rules are set)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `listMembershipUsageVisit`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership usage visit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership usage visit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership usage visit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership usage visit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The product version is retired or expired and cannot take new rules; 422 A conditional field is missing (cooldown for afterMinutes, the no-show triple for restrictReservations, the period for an admissions limit) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW, PRODUCT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PRODUCT_CONFIGURE for setPlanBenefits; PLATFORM_CELL_MANAGE for Save membership usage policy. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/catalogue.yaml#setPlanBenefits)*
- **setMembershipUsagePolicy answers 404**: Show it as something the person can act on, not a failure: No membership product with this code *(source: contracts/satellite/subscription.yaml#setMembershipUsagePolicy)*
- **setMembershipUsagePolicy answers 409**: Show it as something the person can act on, not a failure: The product version is retired or expired and cannot take new rules *(source: contracts/satellite/subscription.yaml#setMembershipUsagePolicy)*
- **setMembershipUsagePolicy answers 422**: Show it as something the person can act on, not a failure: A conditional field is missing (cooldown for afterMinutes, the no-show triple for restrictReservations, the period for an admissions limit) *(source: contracts/satellite/subscription.yaml#setMembershipUsagePolicy)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMembershipUsageVisit (MembershipUsageVisitConsumptionRulesView):
- maximumVisitsPerDay: 12
  maximumAdmissionsPerPeriod: 12
  reEntryCooldownMinutes: 12
  concurrentReservations: 12
  noShowTreatment: none
  cancellationLimit: AED 1,250.00
  guestUsage: withMemberOnly
  benefitConsumption: onRedemption
- maximumVisitsPerDay: 3
  maximumAdmissionsPerPeriod: 3
  reEntryCooldownMinutes: 3
  concurrentReservations: 3
  noShowTreatment: restrictReservations
  cancellationLimit: AED 48,000.00
  guestUsage: independent
  benefitConsumption: onValidatedVisit
```

#### Permissions

- `listMembershipUsageVisit` → `PLATFORM_TENANT_VIEW` (read) · staff
- `setPlanBenefits` → `PRODUCT_CONFIGURE` (configure) · staff
- `listEntitlementTemplates` → `PRODUCT_VIEW` (read) · staff
- `setMembershipUsagePolicy` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.32 | Membership & Annual Pass Sales | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 2.14.11 | Support validity periods, renewals and expiry rules. | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 5.3.15 | Maintain membership type, tier, status, activation date, expiration date, benefits, renewal history, suspension history, and usage history. | F&B & Guest Management | CONTRACTED | `listEntitlementTemplates` |
| 6.1.37 | The system should be able to provide aging report for ticketing & reward age. | Retail POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.21 | For each PLU, it is possible to manage a validity date range | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.23 | For each PLU, it is possible to manage Events having a scheduled usage, based on slot date and time | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.24 | For each PLU, it is possible to have Capacity management rules (valid until there is no available place) | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.29 | For each PLU, it is possible to Allow re-entry or not | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 2.14.7 | Annual-pass reservation quota engine linked to biometric identity, with self-service reschedule/cancel | Ticketing Sales | CONTRACTED | `setMembershipUsagePolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-289` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-289`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 10: Works in Membership Usage, Visit & Consumption Rules → Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-289?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save membership usage policy.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-290` Family, Household & Dependent Membership Configuration

**Support memberships covering more than one person while preserving individual identities and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29242 (VM-BO-290) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Possible configured action) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/family-household-dependent-membership-configuration-bo-290` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Memberships covering several people with individual identities: primary member, adults, dependents, age bands, relationship and verification rules, changes allowed per period.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setFamilyHouseholdDependent (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary Member | select field | — | — | — | — | — | — |
| Secondary Adult | select field | — | — | — | — | — | — |
| Dependent | select field | — | — | — | — | — | — |
| Child | select field | — | — | — | — | — | — |
| Guardian | select field | — | — | — | — | — | — |
| Authorized Manager | select field | — | — | — | — | — | — |
| Minimum Age | select field | — | — | — | — | — | — |
| Maximum Age | select field | — | — | — | — | — | — |
| Relationship Requirement | select field | — | — | — | — | — | — |
| Verification Requirement | select field | — | — | — | — | — | — |
| Same Household Requirement where applicable | text field | — | — | — | — | — | — |
| Allowed | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Fee | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Eligibility Revalidation | select field | — | — | — | — | — | — |
| Grace Period | select field | — | — | — | — | — | — |
| Upgrade Required | select field | — | — | — | — | — | — |
| Renewal Correction | select field | — | — | — | — | — | — |
| Manual Review | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Dependents**: Age limits checked against date of birth; a missing date of birth is treated as a minor (minor age is the value client counsel sets). *(source: R126)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setFamilyHouseholdDependent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family household dependent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family household dependent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family household dependent configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Primary Member: 57
  Secondary Adult: 128
  Dependent: 74
  Child: 128
  Guardian: 19
  Authorized Manager: 1.8 s
  Minimum Age: 1.8 s
  Maximum Age: 3 h 20 min
  Relationship Requirement: 128
  Verification Requirement: 46
  Same Household Requirement where applicable: 233
  Allowed: 312
  Effective Date: 01/10/2026 09:14
  Frequency: 57
```

#### Permissions

- `setFamilyHouseholdDependent` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-290` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-290`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 12: Works in Family, Household & Dependent Membership Configuration → Support memberships covering more than one person while preserving individual identities and entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-290?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-291` Membership Commercial, Pricing & Channel Association

**Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29883 (VM-BO-291) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW`, `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE` (3 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure sale through; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `priceListId` (navigation) |
| Route | `/sell/membership-commercial-pricing-channel-association-bo-291` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Connects a membership product to the central commercial engines without duplicating pricing: pricing, tax and fee profiles, upgrade price policy, payment terms (full, instalments, corporate credit, auto-renew), billing frequency independent of the validity term, sales period and channels. References only, never money.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The profiles (pricing, tax, fee, upgrade policy) are free strings and the writer needs PLATFORM_CELL_MANAGE. (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| B2C | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Call Center | select field | — | — | — | — | — | — |
| Box Office | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| B2B | select field | — | — | — | — | — | — |
| Corporate | select field | — | — | — | — | — | — |
| Reseller | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |
| Always Available | select field | — | — | — | — | — | — |
| Fixed Sales Window | select field | — | — | — | — | — | — |
| Seasonal Sale | select field | — | — | — | — | — | — |
| Invitation Only | select field | — | — | — | — | — | — |
| Capacity Limited | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership code | text field | — | — | `listMembershipCommercialPricing` ?membershipCode |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listMembershipCommercialPricing` ?channel |
| Sales period | radio group | — | Always available · Fixed sales window · Seasonal sale · Invitation only · Capacity limited | `listMembershipCommercialPricing` ?salesPeriod |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listPriceLists` ?channel |

**Form: Save membership commercial config** (modal, opened by *Save membership commercial config*; *Save membership commercial config* calls `setMembershipCommercialConfig`, *Cancel* sends nothing)

**Collects what `setMembershipCommercialConfig` sends before it is called.** Required: `membershipCode`, `basePricingProfile`, `taxProfile`, `salesPeriod`. Optional: `feeProfile`, `upgradePricePolicy`, `promotionalPricingEligibility`, `paymentTerms`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Membership code `membershipCode` | text field | required | — | — | — | The membership product (subscription.membership_product) being associated. | `setMembershipCommercialConfig` body |
| Base pricing profile `basePricingProfile` | text field | required | — | — | — | Base Pricing Profile id | `setMembershipCommercialConfig` body |
| Tax profile `taxProfile` | text field | required | — | — | — | Tax Profile id | `setMembershipCommercialConfig` body |
| Fee profile `feeProfile` | text field | optional | — | — | — | Fee Profile id | `setMembershipCommercialConfig` body |
| Upgrade price policy `upgradePricePolicy` | text field | optional | — | — | — | Upgrade Price Policy id (pack p.14); pro-rata credit on upgrade per MoM 1 Sep §4.9 | `setMembershipCommercialConfig` body |
| Promotional pricing eligibility `promotionalPricingEligibility` | toggle | optional | off | — | — | Promotional Pricing Eligibility: promotions may apply to this membership | `setMembershipCommercialConfig` body |
| Payment terms `paymentTerms` | multi-select chips | optional | — | Full payment · Installments · Corporate credit · Auto renew payment | — | Payment Eligibility (pp.14-15); installments only where the payments module supports them | `setMembershipCommercialConfig` body |
| Sales period `salesPeriod` | radio group | required | — | Always available · Fixed sales window · Seasonal sale · Invitation only · Capacity limited | — | Sales Period (pack p.15); the window itself is the catalogue product's sales window | `setMembershipCommercialConfig` body |
| Billing frequency `billingFrequency` | select | optional | Up front | Up front · Monthly · Quarterly · Semi annual · Annual · Custom; A recurring frequency needs `autoRenewPayment` or `installments` in `paymentTerms` and a card on file under a recurring mandate; each cycle is an instalment of the plan payments … | — | 2.14.19 (29 September, build). How often the member is charged, independent of the validity term: an annual membership may be billed monthly or quarterly. | `setMembershipCommercialConfig` body |
| Billing interval months `billingIntervalMonths` | stepper or slider | optional | — | min 1; max 24 | — | For `custom`, every how many months. Null otherwise. | `setMembershipCommercialConfig` body |
| Billing anchor `billingAnchor` | segmented control | optional | Purchase date | Purchase date · Calendar month start; A cycle longer than the term is refused (422). | — | `purchaseDate` bills on the purchase day each cycle; `calendarMonthStart` on the 1st of the month, the first cycle prorated. | `setMembershipCommercialConfig` body |

Errors to draw in the form: 404 No membership product with this code; 409 The product version is retired or expired and cannot be changed; 422 An unknown or inactive profile, autoRenewPayment on a product that is not auto-renew eligible, or installments where payments does not support them, or a …

**Sent by *What publishing changes*** (`publishChannelAvailability`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | repeatable rows | optional | — | — | — | Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates | `publishChannelAvailability` body |
| Channel `channels[].channel` | select | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `publishChannelAvailability` body |
| Enabled `channels[].enabled` | toggle | optional | — | — | — | — | `publishChannelAvailability` body |
| Sites `channels[].siteIds` | list of values (chips) | optional | — | — | — | Specific sites/webstores; empty = all | `publishChannelAvailability` body |
| POS groups `channels[].posGroupIds` | list of values (chips) | optional | — | — | — | Specific POS groups; empty = all | `publishChannelAvailability` body |
| Venues `channels[].venueIds` | list of values (chips) | optional | — | — | — | Availability by venue; empty = all the product's venues | `publishChannelAvailability` body |
| Effective from `channels[].effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Effective to `channels[].effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Product id | `publishChannelAvailability` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **billingFrequency**: Up front, monthly, quarterly, semi-annual, annual or custom (every N months), with the billing anchor; shown with an example schedule for a year. *(source: contracts/satellite/subscription.yaml#setMembershipCommercialConfig)*
- **paymentTerms**: Instalments offered only where the instalment policy allows it (ADM-603). *(source: contracts/satellite/subscription.yaml#setMembershipCommercialConfig / contracts/satellite/payments.yaml#setInstalmentPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | `publishChannelAvailability` PUT `/channel-availability` | ChannelPublicationAvailabilityInput | ChannelPublicationAvailabilityView | — | — |
| Save membership commercial config (primary button) | `setMembershipCommercialConfig` PUT `/membership-commercial-config` | MembershipCommercialConfigInput | MembershipCommercialPricingChannelAssociationView | 404 No membership product with this code; 409 The product version is retired or expired and cannot be changed; 422 An unknown or inactive profile, autoRenewPayment on a product that is not auto-renew eligible, or … | gated `PLATFORM_CELL_MANAGE`; opens modal first |

**Data it reads**: `listMembershipCommercialPricing` (onLoad, Membership Commercial, Pricing & Channel Association); `listPriceLists` (onLoad, The price lists a membership is priced on)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `listMembershipCommercialPricing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership commercial pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership commercial pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Currency or scale mismatch against the region; 409 The product version is retired or expired and cannot be changed; 422 An unknown or inactive profile, autoRenewPayment on a product that is not auto-renew eligible, or installments where payments does not support them, or a … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  membership: Annual Pass Gold
  price: AED 1,450.00
  renewal: AED 1,305.00
  billing: monthly, from purchase date
  salesPeriod: alwaysAvailable
  channels:
  - Website
  - App
  - Point of sale
```

#### Permissions

- `listMembershipCommercialPricing` → `PLATFORM_TENANT_VIEW` (read) · staff
- `setPrices` → `PRICE_CONFIGURE` (configure) · staff
- `publishChannelAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `listPriceLists` → `PRICE_VIEW` (read) · staff, partner
- `setMembershipCommercialConfig` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.10.4 | The system should allow sales of free tickets. These tickets can be configured as a standard ticket with a price of zero or as a full price ticket with a 100% discount. | Ticketing Sales | CONTRACTED | `setPrices` |
| 7.4.17 | For each PLU, it is possible to manage its Unit price and the related currency | F&B POS | CONTRACTED | `setPrices` |
| 7.4.19 | For each PLU, it is possible to manage its VAT rate | F&B POS | CONTRACTED | `setPrices` |
| 2.14.19 | System shall support recurring membership billing cycles including monthly, quarterly, annual, and configurable subscription periods. | Ticketing Sales | CONTRACTED | `setMembershipCommercialConfig` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-291` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-291`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 14: Works in Membership Commercial, Pricing & Channel Association → Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-291?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Save membership commercial config.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_TENANT_VIEW`, `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-292` Renewal, Auto-Renewal & Membership Continuity Configuration

**Define how a membership moves from one validity period into the next.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29265 (VM-BO-292) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; At renewal, configure whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/renewal-auto-renewal-membership-continuity-configuration-bo-292` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How a membership moves into the next period: renewal window, auto-renew with consent and a payment method, retries, tier change at renewal.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setRenewalAutoMembership (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 60 days before expiry | text field | — | — | — | — | — | — |
| Eligible Products | select field | — | — | — | — | — | — |
| Consent Requirement | select field | — | — | — | — | — | — |
| Payment Method Requirement | select field | — | — | — | — | — | — |
| Pre-Renewal Notification | select field | — | — | — | — | — | — |
| Retry Policy | select field | — | — | — | — | — | — |
| Failure Handling | select field | — | — | — | — | — | — |
| Same Tier Only | select field | — | — | — | — | — | — |
| Upgrade Allowed | select field | — | — | — | — | — | — |
| Downgrade Allowed | select field | — | — | — | — | — | — |
| Suggested Tier | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Renewal (primary button) | navigation or local | — | — | — | — |
| Customer Self-Service Renewal (secondary button) | navigation or local | — | — | — | — |
| Agent-Assisted Renewal (secondary button) | navigation or local | — | — | — | — |
| Invitation-Only Renewal (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setRenewalAutoMembership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal auto-renewal membership configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal auto-renewal membership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal auto-renewal membership configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  60 days before expiry: 233
  Eligible Products: 312
  Consent Requirement: 233
  Payment Method Requirement: 233
  Pre-Renewal Notification: 19
  Retry Policy: 46
  Failure Handling: 5
  Same Tier Only: 233
  Upgrade Allowed: 11
  Downgrade Allowed: 312
  Suggested Tier: 128
```

#### Permissions

- `setRenewalAutoMembership` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.20 | System shall support automatic membership renewal using stored payment methods, configurable renewal notices, renewal reminders, and renewal grace periods. | Ticketing Sales | CONTRACTED | `setRenewalAutoMembership` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-292` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-292`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 16: Works in Renewal, Auto-Renewal & Membership Continuity Configuration → Define how a membership moves from one validity period into the next.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-292?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Renewal, Customer Self-Service Renewal, Agent-Assisted Renewal, Invitation-Only Renewal.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-293` Membership Product Validation, Approval, Publication & Versioning

**Provide the final governance layer before a membership/pass configuration becomes commercially available.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · ticket #29864 (VM-BO-293) |
| Who uses it | venue staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Synchronize relevant configuration with; AI Configuration Review) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `membershipCode` (BO-284), `version` (BO-284), `challengeId` (navigation) |
| Route | `/sell/membership-product-validation-approval-publication-versi-bo-293` |

**What the spec says about it.** **Bound 4 October 2026: the screen reads the version it works on (getMembershipProductValidation, agreed in the ledger) by the membershipCode and version BO-284 carries; the eight publication targets are read, and the action, effective date, migration policy and reason are the inputs the PUT takes** (CHG-FXS-002)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The final check before a membership product is sold: validation across channels (web, POS, app, B2B, access), approval under a second factor, publication and versioning.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: approveMembershipProductValidation (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Reaches approveMembershipProductValidation (step-up mfa) and declares no way to raise the challenge. (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Action | select | optional | — | Validate · Submit for review · Approve commercial · Approve operational · Reject · Schedule · Publish · Suspend · Reinstate | — | Only the actions the approval stage allows next are offered. | `MembershipProductValidationApprovalPublicationVersioInput.action` |
| Effective from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | For schedule and publish. | `MembershipProductValidationApprovalPublicationVersioInput.effectiveFrom` |
| Existing members | segmented control | optional | — | Remain on current version · Move at next renewal · Move on effective date | — | Stay on the current version, move at next renewal, or move on the effective date. | `MembershipProductValidationApprovalPublicationVersioInput.migrationPolicy` |
| Reason | text area | optional | — | — | — | Required for reject and suspend. | `MembershipProductValidationApprovalPublicationVersioInput.reason` |
| Authentication code | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership code | text field | — | — | `getMembershipProductValidation` ?membershipCode |
| Version | text field | — | — | `getMembershipProductValidation` ?version |

**Sent by *Submit*** (`approveMembershipProductValidation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Migration policy `migrationPolicy` | segmented control | optional | — | Remain on current version · Move at next renewal · Move on effective date | — | Migration policy for existing member contracts (pack p.18). | `approveMembershipProductValidation` body |
| Membership code `membershipCode` | text field | optional | — | — | — | Membership code | `approveMembershipProductValidation` body |
| Version `version` | number field | optional | — | — | — | Configuration version the decision applies to | `approveMembershipProductValidation` body |
| Action `action` | select | optional | — | Validate · Submit for review · Approve commercial · Approve operational · Reject · Schedule · Publish · Suspend · Reinstate | — | Decision taken on BO-293; `suspend` (from `active`, reason required) and `reinstate` (from `suspended`) are the BO-284 quick actions (decided 29 September, writers pass; DM4) | `approveMembershipProductValidation` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Effective date for schedule/publish | `approveMembershipProductValidation` body |
| Reason `reason` | text area | optional | — | — | — | Reason, recorded in the audit | `approveMembershipProductValidation` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Shown**

**Version** (detail panel, from `getMembershipProductValidation`)

| Shows | Format | Notes |
|---|---|---|
| Membership code | text | Membership code |
| Version | 1,234 | Configuration version under approval |
| Approval stage | text | Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17) |
| Effective from | 1 Oct 2026 | Effective Dating: date this version takes effect |
| Migration policy | chip: Remain on current version, Move at next renewal, Move on effective date | Migration policy for existing member contracts (pack p.18). |

**Validation checks** (data table, from `getMembershipProductValidation`)

| Shows | Format | Notes |
|---|---|---|
| Migration policy | chip: Remain on current version, Move at next renewal, Move on effective date | Migration policy for existing member contracts (pack p.18). |
| Active members affected | 1,234 | Active Members Affected |
| Future renewals | 1,234 | Future Renewals affected by the change |
| Entitlements affected | list or chips (count when long) | Entitlements Affected |
| Channels | list or chips (count when long) | Channels affected |
| Pricing dependencies | list or chips (count when long) | Pricing Dependencies: pricing profiles and rules referenced |
| Access dependencies | list or chips (count when long) | Access Dependencies: access-control rules and credentials referenced |
| Membership code | text | Membership code |
| Approval stage | text | Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17) |
| Effective from | 1 Oct 2026 | Effective Dating: date this version takes effect |
| Validation checks | list or chips (count when long) | Configuration Validation (pack p.17) |
| Check | chip: Product definition complete, Catalogue association, Eligibility rules, Validity … | — |
| Passed | yes / no (icon or chip) | — |
| Message | text | — |
| Validation issues | list or chips (count when long) | Dependency Health (pack p.17 examples); missingCancellationPolicy is a warning (decided 29 September, readiness close-out) |
| Code | chip: Inactive pricing profile, Missing dependent eligibility, Auto renew without consent … | — |
| Message | text | — |
| Publication targets | list or chips (count when long) | Publication (pack p.18): services the configuration is synchronised to |
| Target | chip: B2C, POS, Mobile app, Call center, B2B, Access control… | — |
| Synchronised at | 1 Oct 2026, 14:30 | — |

**Issues** (data table, from `getMembershipProductValidation`)

| Shows | Format | Notes |
|---|---|---|
| Migration policy | chip: Remain on current version, Move at next renewal, Move on effective date | Migration policy for existing member contracts (pack p.18). |
| Active members affected | 1,234 | Active Members Affected |
| Future renewals | 1,234 | Future Renewals affected by the change |
| Entitlements affected | list or chips (count when long) | Entitlements Affected |
| Channels | list or chips (count when long) | Channels affected |
| Pricing dependencies | list or chips (count when long) | Pricing Dependencies: pricing profiles and rules referenced |
| Access dependencies | list or chips (count when long) | Access Dependencies: access-control rules and credentials referenced |
| Membership code | text | Membership code |
| Approval stage | text | Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17) |
| Effective from | 1 Oct 2026 | Effective Dating: date this version takes effect |
| Validation checks | list or chips (count when long) | Configuration Validation (pack p.17) |
| Check | chip: Product definition complete, Catalogue association, Eligibility rules, Validity … | — |
| Passed | yes / no (icon or chip) | — |
| Message | text | — |
| Validation issues | list or chips (count when long) | Dependency Health (pack p.17 examples); missingCancellationPolicy is a warning (decided 29 September, readiness close-out) |
| Code | chip: Inactive pricing profile, Missing dependent eligibility, Auto renew without consent … | — |
| Message | text | — |
| Publication targets | list or chips (count when long) | Publication (pack p.18): services the configuration is synchronised to |
| Target | chip: B2C, POS, Mobile app, Call center, B2B, Access control… | — |
| Synchronised at | 1 Oct 2026, 14:30 | — |

**Publication targets** (data table, from `getMembershipProductValidation`): B2C, POS, mobile app, call centre, B2B, access control, ticketing and other dependent services, each with its state (the pack's eight, read, not chosen).

| Shows | Format | Notes |
|---|---|---|
| Migration policy | chip: Remain on current version, Move at next renewal, Move on effective date | Migration policy for existing member contracts (pack p.18). |
| Active members affected | 1,234 | Active Members Affected |
| Future renewals | 1,234 | Future Renewals affected by the change |
| Entitlements affected | list or chips (count when long) | Entitlements Affected |
| Channels | list or chips (count when long) | Channels affected |
| Pricing dependencies | list or chips (count when long) | Pricing Dependencies: pricing profiles and rules referenced |
| Access dependencies | list or chips (count when long) | Access Dependencies: access-control rules and credentials referenced |
| Membership code | text | Membership code |
| Approval stage | text | Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17) |
| Effective from | 1 Oct 2026 | Effective Dating: date this version takes effect |
| Validation checks | list or chips (count when long) | Configuration Validation (pack p.17) |
| Check | chip: Product definition complete, Catalogue association, Eligibility rules, Validity … | — |
| Passed | yes / no (icon or chip) | — |
| Message | text | — |
| Validation issues | list or chips (count when long) | Dependency Health (pack p.17 examples); missingCancellationPolicy is a warning (decided 29 September, readiness close-out) |
| Code | chip: Inactive pricing profile, Missing dependent eligibility, Auto renew without consent … | — |
| Message | text | — |
| Publication targets | list or chips (count when long) | Publication (pack p.18): services the configuration is synchronised to |
| Target | chip: B2C, POS, Mobile app, Call center, B2B, Access control… | — |
| Synchronised at | 1 Oct 2026, 14:30 | — |

**Impact** (detail panel, from `getMembershipProductValidation`)

| Shows | Format | Notes |
|---|---|---|
| Active members affected | 1,234 | Active Members Affected |
| Future renewals | 1,234 | Future Renewals affected by the change |
| Entitlements affected | list or chips (count when long) | Entitlements Affected |
| Channels | list or chips (count when long) | Channels affected |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit (primary button) | `approveMembershipProductValidation` PUT `/membership-product-validation` | MembershipProductValidationApprovalPublicationVersioInput | MembershipProductValidationApprovalPublicationVersioView | 409 The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass …; 422 A suspend sent without a reason … | step-up: mfa (Platform-level product state, across tenants.) |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **approveMembershipProductValidation**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends approveMembershipProductValidation with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Platform-level product state, across tenants. *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Data it reads**: `getMembershipProductValidation` (onLoad, The product version's validation checks, issues, impact …)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Membership & Annual Pass Command Center*; carries `challengeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version's checks and impact load first. |
| Error (`?state=error`) | Could not load. Names the read that failed; no action is offered until it loads. |
| Empty, first run (`?state=emptyFirstRun`) | Not used: the screen opens on one product version. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_MANAGE`, which `approveMembershipProductValidation` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass …; 422 A suspend sent without a reason (`reason-required`) (decided 29 September, writers pass; DM4); 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Edge cases to draw

- **approveMembershipProductValidation answers 409**: Show it as something the person can act on, not a failure: The action is not allowed from the version's current status (`invalid-product-transition`, states/membership-product.yaml) (decided 29 September, writers pass; DM4) *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*
- **approveMembershipProductValidation answers 422**: Show it as something the person can act on, not a failure: A suspend sent without a reason (`reason-required`) (decided 29 September, writers pass; DM4) *(source: contracts/satellite/subscription.yaml#approveMembershipProductValidation)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  B2C: 74
  POS: 19
  Mobile App: 19
  Call Center: 57
  B2B: 11
  Access Control: 74
  Ticketing: 11
  Other dependent services: 11
```

#### Permissions

- `approveMembershipProductValidation` → `PLATFORM_CELL_MANAGE` (configure) · staff · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `getMembershipProductValidation` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_MANAGE`, which `approveMembershipProductValidation` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-293` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-293`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 18: Works in Membership Product Validation, Approval, Publication & Versioning → Provide the final governance layer before a membership/pass configuration becomes commercially available.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (404, 409, 410, 422).
- [ ] Every output is drawn (69 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-293?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit, Email me a code instead.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveMembershipProductValidation": {"method":"PUT","path":"/membership-product-validation","contract":"subscription","summary":"Membership Product Validation, Approval, Publication & Versioning","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipProductValidationApprovalPublicationVersioInput","responds":"MembershipProductValidationApprovalPublicationVersioView"},
"createEntitlementTemplate": {"method":"POST","path":"/entitlement-templates","contract":"catalogue","summary":"Create an entitlement template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EntitlementTemplate","responds":"EntitlementTemplate"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getMembershipProductValidation": {"method":"GET","path":"/membership-product-validation","contract":"subscription","summary":"A membership product's validation, as the approver sees it","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipCode","in":"query","required":true},{"name":"version","in":"query","required":false}],"requestBody":null,"responds":"MembershipProductValidationApprovalPublicationVersioView"},
"listEntitlementTemplates": {"method":"GET","path":"/entitlement-templates","contract":"catalogue","summary":"List entitlement templates","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"EntitlementTemplate"},
"listMembershipAnnualPass": {"method":"GET","path":"/membership-annual-pass","contract":"subscription","summary":"Membership & Annual Pass Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"tier","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"hasConfigurationIssues","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipCommercialPricing": {"method":"GET","path":"/membership-commercial-pricing","contract":"subscription","summary":"Membership Commercial, Pricing & Channel Association","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipCode","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"salesPeriod","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipUsageVisit": {"method":"GET","path":"/membership-usage-visit","contract":"subscription","summary":"Membership Usage, Visit & Consumption Rules","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipCode","in":"query","required":false},{"name":"tier","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceLists": {"method":"GET","path":"/price-lists","contract":"catalogue","summary":"List price lists","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishChannelAvailability": {"method":"PUT","path":"/channel-availability","contract":"catalogue","summary":"Channel Publication & Availability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPublicationAvailabilityInput","responds":"ChannelPublicationAvailabilityView"},
"setFamilyHouseholdDependent": {"method":"PUT","path":"/family-household-dependent","contract":"subscription","summary":"Family, Household & Dependent Membership Configuration","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FamilyHouseholdDependentMembershipConfigurationInput","responds":"FamilyHouseholdDependentMembershipConfigurationView"},
"setMembershipBenefit": {"method":"PUT","path":"/membership-benefits","contract":"catalogue","summary":"Define a benefit","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueMembershipBenefit","responds":"CatalogueMembershipBenefit"},
"setMembershipCommercialConfig": {"method":"PUT","path":"/membership-commercial-config","contract":"subscription","summary":"Save a membership product's commercial references, payment eligibility and sales period","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipCommercialConfigInput","responds":"MembershipCommercialPricingChannelAssociationView"},
"setMembershipEligibilityQualification": {"method":"PUT","path":"/membership-eligibility-qualification","contract":"subscription","summary":"Membership Eligibility & Qualification Rule Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipEligibilityQualificationRuleBuilderInput","responds":"MembershipEligibilityQualificationRuleBuilderView"},
"setMembershipEntitlementAdmission": {"method":"PUT","path":"/membership-entitlement-admission","contract":"subscription","summary":"Membership Entitlement & Admission Benefit Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipEntitlementAdmissionBenefitBuilderInput","responds":"MembershipEntitlementAdmissionBenefitBuilderView"},
"setMembershipProductTier": {"method":"PUT","path":"/membership-product-tier","contract":"subscription","summary":"Membership Product & Tier Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipProductTierBuilderInput","responds":"MembershipProductTierBuilderView"},
"setMembershipProgramme": {"method":"PUT","path":"/membership-programmes","contract":"catalogue","summary":"Define a membership programme","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueMembershipProgramme","responds":"CatalogueMembershipProgramme"},
"setMembershipUsagePolicy": {"method":"PUT","path":"/membership-usage-policy","contract":"subscription","summary":"Save a membership product's usage, visit and consumption rules","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipUsagePolicyInput","responds":"MembershipUsageVisitConsumptionRulesView"},
"setPlanBenefits": {"method":"PUT","path":"/entitlement-templates/{templateId}/benefits","contract":"catalogue","summary":"Replace the benefits a plan grants","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"templateId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"CataloguePlanBenefit","responds":"CataloguePlanBenefit"},
"setPrices": {"method":"PUT","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"Set prices in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setRenewalAutoMembership": {"method":"PUT","path":"/renewal-auto-membership","contract":"subscription","summary":"Renewal, Auto-Renewal & Membership Continuity Configuration","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RenewalAutoRenewalMembershipContinuityConfigurationInput","responds":"RenewalAutoRenewalMembershipContinuityConfigurationView"},
"setValidityActivationExpiry": {"method":"PUT","path":"/validity-activation-expiry","contract":"subscription","summary":"Validity, Activation & Expiry Configuration","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidityActivationExpiryConfigurationInput","responds":"ValidityActivationExpiryConfigurationView"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"CatalogueMembershipBenefit": {"type":"object","x-ticvai-persistence":"catalogue.membership_benefit","description":"**Taken from the backend workbook, 20 September.** Defines a benefit that can be included in one or more membership plans.","required":["code","name","type","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":150},"type":{"type":"string","maxLength":30},"description":{"type":"string","maxLength":500,"nullable":true},"value":{"type":"number","nullable":true},"unit":{"type":"string","maxLength":30,"nullable":true},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"CatalogueMembershipProgramme": {"type":"object","x-ticvai-persistence":"catalogue.membership_programme","description":"**Taken from the backend workbook, 20 September.** Defines the overall membership programme available to customers.","required":["programId","programCode","programName","isActive","createdAt"],"properties":{"programId":{"type":"string","format":"uuid"},"programCode":{"type":"string","maxLength":100},"programName":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"CataloguePlanBenefit": {"type":"object","x-ticvai-persistence":"catalogue.plan_benefit","description":"**Taken from the backend workbook, 20 September.** Maps membership benefits to plans and defines usage limits for each benefit.","required":["entitlementTemplateId","membershipBenefitId","priority","isActive","createdAt"],"properties":{"entitlementTemplateId":{"type":"string","format":"uuid"},"membershipBenefitId":{"type":"string","format":"uuid"},"usageLimit":{"type":"number","nullable":true},"usagePeriod":{"type":"string","maxLength":30,"nullable":true},"priority":{"type":"integer"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelPublicationAvailabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ChannelPublicationAvailabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"publicationPreview":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"venueId":{"type":"string"},"exposed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"description":"Preview of where the product will actually be on sale"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["channelNotConfigured","noPriceForChannel","noCapacityAllocation","productNotApproved","venueNotAssigned"]},"message":{"type":"string"}}},"description":"Missing channel dependencies (decided 29 September, readiness close-out)"},"productId":{"type":"string","description":"Product id","format":"uuid"},"issuedEntitlementsUnaffected":{"type":"integer","description":"Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"}}},
"EntitlementTemplate": {"x-ticvai-persistence":"catalogue.entitlement_template","type":"object","required":["id","code","name","validityKind"],"properties":{"description":{"type":"string","description":"**Validity, re-entry and transfer rules in prose.** \"Can I leave and come back\" is answered from here, and a name cannot answer it.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on create; `createEntitlementTemplate` does not take it."},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"validityKind":{"type":"string","enum":["singleUse","dated","dateRange","rolling","unlimited","countLimited"]},"validFromOffsetDays":{"type":"integer","nullable":true},"validForDays":{"type":"integer","nullable":true},"daysOfWeek":{"type":"array","nullable":true,"description":"1.1.7 and 1.1.82. **A camp ticket admits on Tuesdays and Thursdays for six weeks**, and `validityKind` had six values with no day pattern among them.\nThe shape is settled elsewhere in the package — `fnb.MenuAvailability` and `promotions.PromotionConditions` both carry it. **Null means every day**, which is what every existing entitlement means today.\n","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]}},"expiryAnchor":{"type":"string","nullable":true,"enum":["offsetDays","endOfMonth","endOfQuarter","endOfYear","fixedDate","seasonEnd"],"description":"1.1.90 to 1.1.92. **A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days.** `offsetDays` is the existing behaviour and stays the default.\n`seasonEnd` anchors to the venue's own season rather than the calendar — a water park closing in October is not a quarter boundary.\n"},"expiryDate":{"type":"string","format":"date","nullable":true,"description":"Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase."},"expiryNoticeDays":{"type":"integer","minimum":1,"maximum":180,"nullable":true,"description":"**How many days before `validTo` access raises `entitlement.expiringSoon`** for an entitlement of this template still `issued` or `partiallyConsumed` (29 September, build pass, group G2; 5.5.30). What a pre-expiry message or campaign is triggered by. Null, the default, means no notice: a day ticket needs none, an annual pass might want 30. An entitlement bought inside its own notice period raises nothing."},"carriesStoredValue":{"type":"boolean","default":false,"description":"BL-033. **A ticket that is also a wallet** — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till.\n**The value is a `retail.Wallet` bound to the entitlement, not a balance on the ticket.** One balance mechanism (CF-126), so it holds authorisations, expires by credit type and appears in the same reports — a second balance on the entitlement would have been the seventh implementation.\n"},"includedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"validTimeWindows":{"type":"array","nullable":true,"description":"BL-036, 1.1.81 and 1.1.83. **A time-window entitlement needed a performance to express** — valid 09:00 to 13:00 on any day was a thing you built by creating performances.\n**A window is a property of the entitlement and a performance is an occurrence**, and conflating them means a morning pass generates 365 performances a year.\n","items":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"},"daysOfWeek":{"type":"array","items":{"type":"string"}}}}},"blackoutDates":{"type":"array","nullable":true,"description":"**Calendar exceptions on the entitlement.** An annual pass excluding public holidays is the normal case and had nowhere to live.\n","items":{"type":"string","format":"date"}},"fastTrackTier":{"type":"string","nullable":true,"enum":["none","priority","express","unlimited"],"description":"19.2.20, BL-015. **Fast track existed nowhere in the package** — not an enum value, not a description, not a screen.\n**An attribute of the entitlement rather than a queue class or a product kind**, because the same ride serves standby and fast-track guests from one capacity: `queue` already has `isFastPass` on an entry and needed something to read it from.\n"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited. The Fast Pass consumption counter lives here."},"transportRestriction":{"type":"object","nullable":true,"description":"**The journey a transport pass is good for** (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest bought the pass for, and copied to the entitlement. `access` refuses a boarding scan whose departure does not serve both stations in a direction the restriction allows, and consumes one of `entriesAllowed` per boarding. Null on every other template.\n","required":["fromStationId","toStationId"],"properties":{"fromStationId":{"type":"string","format":"uuid","description":"A `transport.Station`."},"toStationId":{"type":"string","format":"uuid"},"bothDirections":{"type":"boolean","default":true,"description":"Valid from either station to the other, as the prototype sells it."},"routeIds":{"type":"array","description":"The routes it may be used on. Empty means any active route serving both stations.","items":{"type":"string","format":"uuid"}}}},"reentryAllowed":{"type":"boolean","default":false},"purchaseEligibility":{"type":"object","nullable":true,"description":"1.1.38, 1.1.121, 1.1.125, 1.1.126. **`admissionRulesId` governs where an entitlement admits, not who may buy it**, and `promotions.evaluatePromotions` gates a discount rather than a sale. Neither refuses a purchase.\n**Evaluated at add-to-cart, not at checkout.** A guest told at payment that they cannot buy a resident rate has already entered a card.\n","properties":{"minAgeYears":{"type":"integer","nullable":true},"maxAgeYears":{"type":"integer","nullable":true},"minHeightCm":{"type":"integer","nullable":true,"description":"**Height gates a ride and can gate a sale.** A ticket sold to somebody who cannot ride it is a refund at the gate.\n"},"residencyRequired":{"type":"boolean","default":false},"nationalities":{"type":"array","nullable":true,"items":{"type":"string"}},"minLoyaltyTier":{"type":"string","nullable":true},"requiresVerification":{"type":"boolean","default":false,"description":"**Whether the claim is checked or taken on trust.** A resident rate sold unverified and refused at the gate is worse than one that could not be bought.\n"}}},"personType":{"type":"string","nullable":true,"enum":["adult","child","infant","senior","student","resident","staff"],"description":"2.11.7. **Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder.** So changing a child ticket to an adult one was an exchange to a different product, and an upgrade that should be a price difference became a cancel-and-rebuy.\nRecorded here as well as on the variant, because **the guest ages and the product does not.**\n"},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"isTransferable":{"type":"boolean","default":true},"canShareMedia":{"type":"boolean","default":true,"description":"Whether this entitlement may be appended to media a guest already holds (CF-58). False for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards.\n"},"canClaimShopAndDrop":{"type":"boolean","default":false,"description":"Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds is not a claim token.\n"},"isNameBound":{"type":"boolean","default":false,"description":"True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns.\n"},"autoRenewDefault":{"type":"boolean","default":false,"description":"**Taken from their `membership_plan`, 20 September — the \"take those\" half of the TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per holder and nothing said what it should start as.\n"},"renewalTermDays":{"type":"integer","nullable":true,"description":"What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.\n"},"renewalGraceDays":{"type":"integer","default":0,"description":"How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the expiry date had no defined consequence.\n"},"renewalVariantId":{"type":"string","format":"uuid","nullable":true,"description":"**What a renewal sells, which is usually not what joining sold.** A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty discount unrepresentable. Null means renewal sells the same thing.\n"},"crossesCells":{"type":"boolean","default":false,"description":"True propagates a redemption right to other cells on issue (ADR-0010).\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.** Set by the server, never taken from a body."}}},
"FamilyHouseholdDependentMembershipConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_household_policy (MembershipHouseholdPolicy) (decided 29 September, data model DM4)","description":"**What Family, Household & Dependent Membership Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"minimumAge":{"type":"integer","description":"Dependent Rules: minimum age of a dependent","nullable":true},"maximumAge":{"type":"integer","description":"Dependent Rules: maximum age of a dependent (pack example: a child dependent turning 16 is flagged)","nullable":true},"relationshipRequirement":{"type":"string","enum":["none","declared","verified"],"description":"Relationship Requirement between dependent and primary member. Default declared (decided 29 September, readiness close-out)"},"verificationRequirement":{"type":"string","enum":["none","customerDeclaration","documentVerification","identityVerification","staffVerification","externalVerification"],"description":"Verification Requirement for dependents"},"sameHouseholdRequired":{"type":"boolean","description":"Same Household Requirement where applicable. Default false (decided 29 September, readiness close-out)"},"memberChangesAllowed":{"type":"boolean","description":"Add/Remove Member Rules: members may be added or removed during the term"},"memberChangeEffective":{"type":"string","enum":["immediately","nextRenewal"],"description":"Add/Remove effective date. Default immediately (decided 29 September, readiness close-out)"},"memberChangesPerTerm":{"type":"integer","description":"Frequency: add/remove changes allowed per membership term; empty for unlimited","nullable":true},"memberChangeFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Fee charged per add/remove change, as the venue configures it; empty for no fee"},"memberChangeApprovalRequired":{"type":"boolean","description":"Approval: add/remove changes need staff approval. Default false (decided 29 September, readiness close-out)"},"eligibilityRevalidation":{"type":"boolean","description":"Eligibility Revalidation of the added member against the dependent rules. Default true (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code"},"membershipStructure":{"type":"string","enum":["individual","couple","family","household","parentChild","corporateGroup","custom"],"description":"Membership Structure (pack p.12)"},"roleLimits":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["primaryMember","secondaryAdult","dependent","child","guardian","authorizedManager"]},"minCount":{"type":"integer"},"maxCount":{"type":"integer","nullable":true}}},"description":"Roles and Family Limits (pack p.13; example Family Gold: 2 adults, maximum 3 children)"},"entitlementModel":{"type":"string","enum":["individual","shared","mixed"],"description":"Entitlement Model (pack p.13): each member's own benefits, shared benefits (e.g. 6 guest tickets for the family) or both"},"ageTransitionAction":{"type":"string","enum":["gracePeriod","upgradeRequired","renewalCorrection","manualReview"],"description":"Age Transition (pp.13-14): action when a dependent no longer qualifies. Default manualReview (decided 29 September, readiness close-out)"},"ageTransitionGraceDays":{"type":"integer","description":"Days a dependent keeps access after ageing out, for gracePeriod","nullable":true}}},
"FamilyHouseholdDependentMembershipConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Family, Household & Dependent Membership Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumAge":{"type":"integer","description":"Dependent Rules: minimum age of a dependent","nullable":true},"maximumAge":{"type":"integer","description":"Dependent Rules: maximum age of a dependent (pack example: a child dependent turning 16 is flagged)","nullable":true},"relationshipRequirement":{"type":"string","enum":["none","declared","verified"],"description":"Relationship Requirement between dependent and primary member. Default declared (decided 29 September, readiness close-out)"},"verificationRequirement":{"type":"string","enum":["none","customerDeclaration","documentVerification","identityVerification","staffVerification","externalVerification"],"description":"Verification Requirement for dependents"},"sameHouseholdRequired":{"type":"boolean","description":"Same Household Requirement where applicable. Default false (decided 29 September, readiness close-out)"},"memberChangesAllowed":{"type":"boolean","description":"Add/Remove Member Rules: members may be added or removed during the term"},"memberChangeEffective":{"type":"string","enum":["immediately","nextRenewal"],"description":"Add/Remove effective date. Default immediately (decided 29 September, readiness close-out)"},"memberChangesPerTerm":{"type":"integer","description":"Frequency: add/remove changes allowed per membership term; empty for unlimited","nullable":true},"memberChangeFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Fee charged per add/remove change, as the venue configures it; empty for no fee"},"memberChangeApprovalRequired":{"type":"boolean","description":"Approval: add/remove changes need staff approval. Default false (decided 29 September, readiness close-out)"},"eligibilityRevalidation":{"type":"boolean","description":"Eligibility Revalidation of the added member against the dependent rules. Default true (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code"},"membershipStructure":{"type":"string","enum":["individual","couple","family","household","parentChild","corporateGroup","custom"],"description":"Membership Structure (pack p.12)"},"roleLimits":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["primaryMember","secondaryAdult","dependent","child","guardian","authorizedManager"]},"minCount":{"type":"integer"},"maxCount":{"type":"integer","nullable":true}}},"description":"Roles and Family Limits (pack p.13; example Family Gold: 2 adults, maximum 3 children)"},"entitlementModel":{"type":"string","enum":["individual","shared","mixed"],"description":"Entitlement Model (pack p.13): each member's own benefits, shared benefits (e.g. 6 guest tickets for the family) or both"},"ageTransitionAction":{"type":"string","enum":["gracePeriod","upgradeRequired","renewalCorrection","manualReview"],"description":"Age Transition (pp.13-14): action when a dependent no longer qualifies. Default manualReview (decided 29 September, readiness close-out)"},"ageTransitionGraceDays":{"type":"integer","description":"Days a dependent keeps access after ageing out, for gracePeriod","nullable":true}}},
"MembershipAnnualPassCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Membership & Annual Pass Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeMembershipProducts":{"type":"integer","description":"Active Membership Products"},"annualPassProducts":{"type":"integer","description":"Annual Pass Products"},"draftProducts":{"type":"integer","description":"Draft Products"},"activeMembers":{"type":"integer","description":"Active Members"},"familyMemberships":{"type":"integer","description":"Family Memberships"},"membershipsExpiringSoon":{"type":"integer","description":"Memberships Expiring Soon: active memberships whose expiry falls within the next 30 days (decided 29 September, readiness close-out)"},"renewalEnabledProducts":{"type":"integer","description":"Renewal-Enabled Products"},"suspendedProducts":{"type":"integer","description":"Suspended Products"},"productsWithConfigurationIssues":{"type":"integer","description":"Products with Configuration Issues: products with at least one validationIssues entry"},"averageMembershipDuration":{"type":"number","description":"Average Membership Duration, in days, across active members (decided 29 September, readiness close-out)"}}},
"MembershipAnnualPassCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership & Annual Pass Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"productId":{"type":"string","description":"Product ID"},"membershipName":{"type":"string","description":"Membership Name"},"type":{"type":"string","enum":["annualPass","seasonPass","monthlyMembership","fixedTermMembership","corporateMembership","familyMembership","individualMembership","studentMembership","vipMembership","customMembership"],"description":"Type: the membership type (pack pp.4-5 Membership Types); customMembership for a venue-defined type"},"tier":{"type":"string","description":"Tier name (Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names)"},"venueAttraction":{"type":"string","description":"Venue/Attraction the membership admits to"},"validityMethod":{"type":"string","enum":["fixedCalendar","durationFromPurchase","durationFromActivation","seasonBased","customPeriod"],"description":"Validity method (pack p.8 Validity Methods)"},"activationMethod":{"type":"string","enum":["immediateOnPurchase","fixedStartDate","firstVisit","manualActivation","customerActivation","membershipCardCollection","identityVerification","configuredTrigger"],"description":"Activation Method (pack pp.8-9)"},"renewalMode":{"type":"string","enum":["manual","customerSelfService","agentAssisted","autoRenewal","invitationOnly","nonRenewable"],"description":"Renewal: the product's primary renewal mode (pack p.15 Renewal Modes)"},"membershipStructure":{"type":"string","enum":["individual","couple","family","household","parentChild","corporateGroup","custom"],"description":"Family/Individual: the membership structure (pack p.12 Membership Structures)"},"currentMembers":{"type":"integer","description":"Current Members"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From: the date the current version becomes sellable"},"status":{"type":"string","description":"Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses)"},"owner":{"type":"string","description":"Owner"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["missingEntitlements","missingPricingAssociation","missingValidity","invalidEligibility","conflictingRules","missingRenewalPolicy"]},"message":{"type":"string"}}},"description":"Configuration Health (pack p.5): the checks this product currently fails"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Assistance: advisory observations only; never applied automatically (pack AI sections)"}}},
"MembershipCommercialConfigInput": {"type":"object","x-ticvai-persistence":"none — request only; stored as the commercial columns of subscription.membership_product (MembershipProduct: basePricingProfile, taxProfile, feeProfile, upgradePricePolicy, promotionalPricingEligibility, paymentTerms, salesPeriod) (decided 29 September, writers pass; DM4)","description":"What setMembershipCommercialConfig submits. Prices, channels, the sales window and capacity are catalogue data and are set there (setPrices, publishChannelAvailability, createChannelCapacity/updateChannelCapacity), so none is repeated here (decided 29 September, writers pass; DM4)","required":["membershipCode","basePricingProfile","taxProfile","salesPeriod"],"properties":{"membershipCode":{"type":"string","description":"The membership product (subscription.membership_product) being associated."},"basePricingProfile":{"type":"string","description":"Base Pricing Profile id"},"taxProfile":{"type":"string","description":"Tax Profile id"},"feeProfile":{"type":"string","nullable":true,"description":"Fee Profile id"},"upgradePricePolicy":{"type":"string","nullable":true,"description":"Upgrade Price Policy id (pack p.14); pro-rata credit on upgrade per MoM 1 Sep §4.9"},"promotionalPricingEligibility":{"type":"boolean","default":false,"description":"Promotional Pricing Eligibility: promotions may apply to this membership"},"paymentTerms":{"type":"array","items":{"type":"string","enum":["fullPayment","installments","corporateCredit","autoRenewPayment"]},"description":"Payment Eligibility (pp.14-15); installments only where the payments module supports them"},"salesPeriod":{"type":"string","enum":["alwaysAvailable","fixedSalesWindow","seasonalSale","invitationOnly","capacityLimited"],"description":"Sales Period (pack p.15); the window itself is the catalogue product's sales window"},"billingFrequency":{"type":"string","enum":["upFront","monthly","quarterly","semiAnnual","annual","custom"],"default":"upFront","description":"2.14.19 (29 September, build). **How often the member is charged, independent of the validity term**: an annual membership may be billed monthly or quarterly. `upFront` charges the whole term at sale. A recurring frequency needs `autoRenewPayment` or `installments` in `paymentTerms` and a card on file under a recurring mandate; each cycle is an instalment of the plan payments `createInstalmentPlan` schedules at sale, charged to the stored card on its due date."},"billingIntervalMonths":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"For `custom`, every how many months. Null otherwise."},"billingAnchor":{"type":"string","enum":["purchaseDate","calendarMonthStart"],"default":"purchaseDate","description":"`purchaseDate` bills on the purchase day each cycle; `calendarMonthStart` on the 1st of the month, the first cycle prorated. A cycle longer than the term is refused (422)."}}},
"MembershipCommercialPricingChannelAssociationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Commercial, Pricing & Channel Association displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basePricingProfile":{"type":"string","description":"Base Pricing Profile id"},"membershipTierPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Membership Tier Price, as calculated by the linked pricing profile (read-only)"},"renewalPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Renewal Price, as calculated by the linked renewal pricing (read-only)"},"promotionalPricingEligibility":{"type":"boolean","description":"Promotional Pricing Eligibility: promotions may apply to this membership"},"taxProfile":{"type":"string","description":"Tax Profile id"},"feeProfile":{"type":"string","description":"Fee Profile id","nullable":true},"salesCapacity":{"type":"integer","description":"Capacity limit for a capacityLimited sales period","nullable":true},"membershipCode":{"type":"string","description":"Membership code"},"upgradePricePolicy":{"type":"string","description":"Upgrade Price Policy id (pack p.14); pro-rata credit on upgrade per MoM 1 Sep §4.9","nullable":true},"availableChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"description":"Channel Availability (pack p.14): B2C -> guestWeb, Mobile App -> guestApp, POS and Box Office -> pos, Call Center -> callCentre, Kiosk -> kiosk, B2B and Corporate -> b2b, Reseller -> partner, API -> api"},"paymentTerms":{"type":"array","items":{"type":"string","enum":["fullPayment","installments","corporateCredit","autoRenewPayment"]},"description":"Payment Eligibility (pp.14-15); installments only where the payments module supports them"},"salesPeriod":{"type":"string","enum":["alwaysAvailable","fixedSalesWindow","seasonalSale","invitationOnly","capacityLimited"],"description":"Sales Period (pack p.15)"},"billingFrequency":{"type":"string","enum":["upFront","monthly","quarterly","semiAnnual","annual","custom"],"default":"upFront","description":"2.14.19 (29 September, build). **How often the member is charged, independent of the validity term**: an annual membership may be billed monthly or quarterly. `upFront` charges the whole term at sale. A recurring frequency needs `autoRenewPayment` or `installments` in `paymentTerms` and a card on file under a recurring mandate; each cycle is an instalment of the plan payments `createInstalmentPlan` schedules at sale, charged to the stored card on its due date."},"billingIntervalMonths":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"For `custom`, every how many months. Null otherwise."},"billingAnchor":{"type":"string","enum":["purchaseDate","calendarMonthStart"],"default":"purchaseDate","description":"`purchaseDate` bills on the purchase day each cycle; `calendarMonthStart` on the 1st of the month, the first cycle prorated. A cycle longer than the term is refused (422)."},"salesWindowFrom":{"type":"string","format":"date","description":"Sales window start, for fixedSalesWindow or seasonalSale","nullable":true},"salesWindowTo":{"type":"string","format":"date","description":"Sales window end","nullable":true}}},
"MembershipEligibilityQualificationRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_eligibility_rule (MembershipEligibilityRule) for the rules and subscription.membership_product for the product-level switches (decided 29 September, data model DM4)","description":"**What Membership Eligibility & Qualification Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"multipleMembershipsAllowed":{"type":"boolean","description":"Multiple Memberships Allowed: false means one membership of this product per customer. Default false (decided 29 September, readiness close-out)"},"mutuallyExclusiveMemberships":{"type":"array","items":{"type":"string"},"description":"Mutually Exclusive Memberships: membership codes a customer may not hold alongside this one"},"prerequisiteMembership":{"type":"string","description":"Prerequisite Membership: code of a membership the customer must already hold","nullable":true},"existingTierRequirement":{"type":"string","description":"Existing Tier Requirement: minimum tier the customer must already hold","nullable":true},"separatePurchaseAndActivationRules":{"type":"boolean","description":"Purchase vs Activation: true when the rules apply at activation to the assigned member rather than to the buyer (pack p.8: a parent may buy a Junior Pass that must be assigned to an eligible child). Default true (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code the rules belong to"},"rules":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["age","personType","residency","country","customerSegment","corporateAffiliation","studentStatus","existingMembership","previousPurchase","membershipHistory","channel","venue","promotionalQualification"],"description":"Eligibility Dimension (pack p.7)"},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","between","atLeast","atMost"]},"values":{"type":"array","items":{"type":"string"},"description":"Values compared, e.g. the age bounds of a junior pass"},"appliesAt":{"type":"array","items":{"type":"string","enum":["purchase","activation","holding","renewal"]},"description":"When the rule is evaluated (pack p.7 purpose: purchase, activate, hold or renew)"}}},"description":"Eligibility rules; all must pass"},"verificationMethod":{"type":"string","enum":["none","customerDeclaration","documentVerification","identityVerification","staffVerification","externalVerification"],"description":"Verification (pack pp.7-8): how qualification is proven. Default none (decided 29 September, readiness close-out)"}}},
"MembershipEligibilityQualificationRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Eligibility & Qualification Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"multipleMembershipsAllowed":{"type":"boolean","description":"Multiple Memberships Allowed: false means one membership of this product per customer. Default false (decided 29 September, readiness close-out)"},"mutuallyExclusiveMemberships":{"type":"array","items":{"type":"string"},"description":"Mutually Exclusive Memberships: membership codes a customer may not hold alongside this one"},"prerequisiteMembership":{"type":"string","description":"Prerequisite Membership: code of a membership the customer must already hold","nullable":true},"existingTierRequirement":{"type":"string","description":"Existing Tier Requirement: minimum tier the customer must already hold","nullable":true},"separatePurchaseAndActivationRules":{"type":"boolean","description":"Purchase vs Activation: true when the rules apply at activation to the assigned member rather than to the buyer (pack p.8: a parent may buy a Junior Pass that must be assigned to an eligible child). Default true (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code the rules belong to"},"rules":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["age","personType","residency","country","customerSegment","corporateAffiliation","studentStatus","existingMembership","previousPurchase","membershipHistory","channel","venue","promotionalQualification"],"description":"Eligibility Dimension (pack p.7)"},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","between","atLeast","atMost"]},"values":{"type":"array","items":{"type":"string"},"description":"Values compared, e.g. the age bounds of a junior pass"},"appliesAt":{"type":"array","items":{"type":"string","enum":["purchase","activation","holding","renewal"]},"description":"When the rule is evaluated (pack p.7 purpose: purchase, activate, hold or renew)"}}},"description":"Eligibility rules; all must pass"},"verificationMethod":{"type":"string","enum":["none","customerDeclaration","documentVerification","identityVerification","staffVerification","externalVerification"],"description":"Verification (pack pp.7-8): how qualification is proven. Default none (decided 29 September, readiness close-out)"}}},
"MembershipEntitlementAdmissionBenefitBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_entitlement (MembershipEntitlement), one row per entitlement (decided 29 September, data model DM4)","description":"**What Membership Entitlement & Admission Benefit Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"membershipCode":{"type":"string","description":"Membership code"},"tier":{"type":"string","description":"Tier the package belongs to"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"],"description":"Entitlement Type (pack pp.9-10)"},"venue":{"type":"string","nullable":true},"attraction":{"type":"string","nullable":true},"eventType":{"type":"string","nullable":true},"admissionType":{"type":"string","nullable":true},"quantity":{"type":"integer","nullable":true,"description":"Number of visits or uses per limitPeriod; empty for unlimited"},"limitPeriod":{"type":"string","enum":["perDay","perWeek","perMonth","perMembershipYear","lifetimeOfMembership"],"description":"Benefit Limits (pack p.10)"},"days":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Days the entitlement is valid; empty for every day"},"timeFrom":{"type":"string","nullable":true,"description":"Times: local start time HH:mm"},"timeTo":{"type":"string","nullable":true,"description":"Times: local end time HH:mm"},"timeslots":{"type":"array","items":{"type":"string"},"description":"Timeslot ids the entitlement is restricted to"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Blackouts (pack pp.10-11; MoM 25 Aug blockout dates)"},"requiresSameDayVisit":{"type":"boolean","description":"Benefit Dependencies (pack p.11): valid only with a valid visit the same day, e.g. parking"},"pricingRuleId":{"type":"string","nullable":true,"description":"For a discount benefit (F&B, retail, rental): the central pricing rule that calculates it (pack p.15: Area 13 identifies the benefit, the commercial engine calculates)"},"ownership":{"type":"string","enum":["memberSpecific","familyShared","dependentSpecific","accountShared"],"description":"Entitlement Ownership (pack p.11)"}}},"description":"The admission and benefit package for the tier (pack p.10 example: Gold Annual Pass)"}}},
"MembershipEntitlementAdmissionBenefitBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Entitlement & Admission Benefit Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"membershipCode":{"type":"string","description":"Membership code"},"tier":{"type":"string","description":"Tier the package belongs to"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"],"description":"Entitlement Type (pack pp.9-10)"},"venue":{"type":"string","nullable":true},"attraction":{"type":"string","nullable":true},"eventType":{"type":"string","nullable":true},"admissionType":{"type":"string","nullable":true},"quantity":{"type":"integer","nullable":true,"description":"Number of visits or uses per limitPeriod; empty for unlimited"},"limitPeriod":{"type":"string","enum":["perDay","perWeek","perMonth","perMembershipYear","lifetimeOfMembership"],"description":"Benefit Limits (pack p.10)"},"days":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Days the entitlement is valid; empty for every day"},"timeFrom":{"type":"string","nullable":true,"description":"Times: local start time HH:mm"},"timeTo":{"type":"string","nullable":true,"description":"Times: local end time HH:mm"},"timeslots":{"type":"array","items":{"type":"string"},"description":"Timeslot ids the entitlement is restricted to"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Blackouts (pack pp.10-11; MoM 25 Aug blockout dates)"},"requiresSameDayVisit":{"type":"boolean","description":"Benefit Dependencies (pack p.11): valid only with a valid visit the same day, e.g. parking"},"pricingRuleId":{"type":"string","nullable":true,"description":"For a discount benefit (F&B, retail, rental): the central pricing rule that calculates it (pack p.15: Area 13 identifies the benefit, the commercial engine calculates)"},"ownership":{"type":"string","enum":["memberSpecific","familyShared","dependentSpecific","accountShared"],"description":"Entitlement Ownership (pack p.11)"}}},"description":"The admission and benefit package for the tier (pack p.10 example: Gold Annual Pass)"}}},
"MembershipProductTierBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_product (MembershipProduct), a new version when the product is active (decided 29 September, data model DM4)","description":"**What Membership Product & Tier Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"membershipName":{"type":"string","description":"Membership Name"},"membershipCode":{"type":"string","description":"Membership Code"},"description":{"type":"string","description":"Description"},"membershipType":{"type":"string","enum":["annualPass","seasonPass","monthlyMembership","fixedTermMembership","corporateMembership","familyMembership","individualMembership","studentMembership","vipMembership","customMembership"],"description":"Membership Type (pack pp.4-5)"},"brand":{"type":"string","description":"Brand"},"venue":{"type":"string","description":"Venue"},"attraction":{"type":"string","description":"Attraction"},"market":{"type":"string","description":"Market"},"currencyContext":{"type":"string","description":"Currency Context: ISO 4217 currency code the product is sold in"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"tierLevel":{"type":"integer","description":"Tier Level: rank within the membership family; higher is more premium"},"displayOrder":{"type":"integer","description":"Display Order in listings and upgrade choices"},"parentMembership":{"type":"string","description":"Parent Membership: code of the membership family this tier belongs to","nullable":true},"replacementMembership":{"type":"string","description":"Replacement Membership: code of the product that replaces this one when it is retired","nullable":true},"holderModel":{"type":"string","enum":["individual","family","corporate"],"description":"Individual / Family / Corporate (pack p.6 Product Characteristics)"},"transferable":{"type":"boolean","description":"Named / Transferable: true when the membership may be transferred; false (the default) keeps it named to one member (decided 29 September, readiness close-out)"},"credentialForm":{"type":"string","enum":["physical","digital","both"],"description":"Physical / Digital credential form"},"renewable":{"type":"boolean","description":"Renewable / Non-Renewable: true when the membership can be renewed"},"autoRenewEligible":{"type":"boolean","description":"Auto-Renew Eligible: the product may be auto-renewed; a member is only auto-renewed after their own explicit opt-in. Default false (decided 29 September, readiness close-out)"},"benefitModel":{"type":"string","enum":["admissionBased","benefitBased","hybrid"],"description":"Admission-Based / Benefit-Based / Hybrid"},"tier":{"type":"string","description":"Tier: Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names (pack p.6 Tier Configuration)"},"upgradePath":{"type":"array","items":{"type":"string"},"description":"Upgrade Path: membership codes this tier may upgrade to (pack p.6 Tier Relationships; the transaction runs in Area 11)"},"downgradePath":{"type":"array","items":{"type":"string"},"description":"Downgrade Path: membership codes this tier may downgrade to"},"catalogueProductId":{"type":"string","description":"Catalogue Association: the sellable product in the Ticketing Catalogue this membership configures (a membership ProductKind)"}}},
"MembershipProductTierBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Product & Tier Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"membershipName":{"type":"string","description":"Membership Name"},"membershipCode":{"type":"string","description":"Membership Code"},"description":{"type":"string","description":"Description"},"membershipType":{"type":"string","enum":["annualPass","seasonPass","monthlyMembership","fixedTermMembership","corporateMembership","familyMembership","individualMembership","studentMembership","vipMembership","customMembership"],"description":"Membership Type (pack pp.4-5)"},"brand":{"type":"string","description":"Brand"},"venue":{"type":"string","description":"Venue"},"attraction":{"type":"string","description":"Attraction"},"market":{"type":"string","description":"Market"},"currencyContext":{"type":"string","description":"Currency Context: ISO 4217 currency code the product is sold in"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"tierLevel":{"type":"integer","description":"Tier Level: rank within the membership family; higher is more premium"},"displayOrder":{"type":"integer","description":"Display Order in listings and upgrade choices"},"parentMembership":{"type":"string","description":"Parent Membership: code of the membership family this tier belongs to","nullable":true},"replacementMembership":{"type":"string","description":"Replacement Membership: code of the product that replaces this one when it is retired","nullable":true},"holderModel":{"type":"string","enum":["individual","family","corporate"],"description":"Individual / Family / Corporate (pack p.6 Product Characteristics)"},"transferable":{"type":"boolean","description":"Named / Transferable: true when the membership may be transferred; false (the default) keeps it named to one member (decided 29 September, readiness close-out)"},"credentialForm":{"type":"string","enum":["physical","digital","both"],"description":"Physical / Digital credential form"},"renewable":{"type":"boolean","description":"Renewable / Non-Renewable: true when the membership can be renewed"},"autoRenewEligible":{"type":"boolean","description":"Auto-Renew Eligible: the product may be auto-renewed; a member is only auto-renewed after their own explicit opt-in. Default false (decided 29 September, readiness close-out)"},"benefitModel":{"type":"string","enum":["admissionBased","benefitBased","hybrid"],"description":"Admission-Based / Benefit-Based / Hybrid"},"tier":{"type":"string","description":"Tier: Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names (pack p.6 Tier Configuration)"},"upgradePath":{"type":"array","items":{"type":"string"},"description":"Upgrade Path: membership codes this tier may upgrade to (pack p.6 Tier Relationships; the transaction runs in Area 11)"},"downgradePath":{"type":"array","items":{"type":"string"},"description":"Downgrade Path: membership codes this tier may downgrade to"},"catalogueProductId":{"type":"string","description":"Catalogue Association: the sellable product in the Ticketing Catalogue this membership configures (a membership ProductKind)"},"version":{"type":"integer","description":"Version number of this configuration; each saved change to an active product creates a new version"},"status":{"type":"string","description":"Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses)"}}},
"MembershipProductValidationApprovalPublicationVersioInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_product (status, approvalStage) with an audit row in subscription.membership_product_history (decided 29 September, data model DM4)","description":"**What Membership Product Validation, Approval, Publication & Versioning submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"migrationPolicy":{"type":"string","enum":["remainOnCurrentVersion","moveAtNextRenewal","moveOnEffectiveDate"],"description":"Migration policy for existing member contracts (pack p.18). Default moveAtNextRenewal (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code"},"version":{"type":"integer","description":"Configuration version the decision applies to"},"action":{"type":"string","enum":["validate","submitForReview","approveCommercial","approveOperational","reject","schedule","publish","suspend","reinstate"],"description":"Decision taken on BO-293; `suspend` (from `active`, reason required) and `reinstate` (from `suspended`) are the BO-284 quick actions (decided 29 September, writers pass; DM4)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective date for schedule/publish","nullable":true},"reason":{"type":"string","description":"Reason, recorded in the audit","nullable":true}}},
"MembershipProductValidationApprovalPublicationVersioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Product Validation, Approval, Publication & Versioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"migrationPolicy":{"type":"string","enum":["remainOnCurrentVersion","moveAtNextRenewal","moveOnEffectiveDate"],"description":"Migration policy for existing member contracts (pack p.18). Default moveAtNextRenewal (decided 29 September, readiness close-out)"},"activeMembersAffected":{"type":"integer","description":"Active Members Affected"},"futureRenewals":{"type":"integer","description":"Future Renewals affected by the change"},"entitlementsAffected":{"type":"array","items":{"type":"string"},"description":"Entitlements Affected"},"channels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"description":"Channels affected"},"pricingDependencies":{"type":"array","items":{"type":"string"},"description":"Pricing Dependencies: pricing profiles and rules referenced"},"accessDependencies":{"type":"array","items":{"type":"string"},"description":"Access Dependencies: access-control rules and credentials referenced"},"membershipCode":{"type":"string","description":"Membership code"},"version":{"type":"integer","description":"Configuration version under approval"},"approvalStage":{"type":"string","description":"Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective Dating: date this version takes effect"},"validationChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["productDefinitionComplete","catalogueAssociation","eligibilityRules","validity","activation","entitlements","usageRules","pricingAssociation","taxFeeAssociation","channelAvailability","renewalPolicy","requiredCredentialConfiguration"]},"passed":{"type":"boolean"},"message":{"type":"string","nullable":true}}},"description":"Configuration Validation (pack p.17)"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["inactivePricingProfile","missingDependentEligibility","autoRenewWithoutConsentConfiguration","missingCancellationPolicy","other"]},"message":{"type":"string"}}},"description":"Dependency Health (pack p.17 examples); missingCancellationPolicy is a warning (decided 29 September, readiness close-out)"},"publicationTargets":{"type":"array","items":{"type":"object","properties":{"target":{"type":"string","enum":["b2c","pos","mobileApp","callCenter","b2b","accessControl","ticketing","otherDependentServices"]},"synchronisedAt":{"type":"string","format":"date-time","nullable":true}}},"description":"Publication (pack p.18): services the configuration is synchronised to"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Assistance: advisory observations only; never applied automatically (pack AI sections)"}}},
"MembershipUsagePolicyInput": {"type":"object","x-ticvai-persistence":"none — request only; stored as subscription.membership_usage_policy (MembershipUsagePolicy), one row per product version (decided 29 September, writers pass; DM4)","description":"What setMembershipUsagePolicy submits for one membership product version; the fields of MembershipUsagePolicy a venue sets. Counters and figures are not sent (decided 29 September, writers pass; DM4)","required":["membershipCode","reEntryPolicy","reservationRequirement"],"properties":{"membershipCode":{"type":"string","description":"The membership product (subscription.membership_product) whose rules these are."},"tier":{"type":"string","nullable":true,"description":"Tier, where the product code covers several tiers."},"maximumVisitsPerDay":{"type":"integer","minimum":1,"nullable":true,"description":"Maximum Visits per Day; empty for unlimited"},"maximumAdmissionsPerPeriod":{"type":"integer","minimum":1,"nullable":true,"description":"Maximum Admissions per admissionPeriod; empty for unlimited"},"admissionPeriod":{"type":"string","enum":["perDay","perWeek","perMonth","perMembershipYear"],"nullable":true,"description":"Period for maximumAdmissionsPerPeriod; required when that is set"},"reEntryPolicy":{"type":"string","enum":["unlimitedSameDay","noReEntry","afterMinutes","venueSpecific"],"description":"Re-entry (pack p.12)"},"reEntryCooldownMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Re-entry Cooldown in minutes; required for reEntryPolicy afterMinutes"},"reservationRequirement":{"type":"string","enum":["required","optional"],"description":"Advance Reservation (pack pp.11-12)"},"walkInAllowed":{"type":"boolean","default":true,"description":"Walk-In Allowed without a reservation"},"maximumAdvanceBookingDays":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum Advance Booking Days"},"maximumActiveFutureReservations":{"type":"integer","minimum":1,"nullable":true,"description":"Maximum Active Future Reservations"},"concurrentReservations":{"type":"integer","minimum":1,"default":1,"description":"Concurrent Reservations: maximum active reservations per timeslot. Default 1 (decided 29 September, readiness close-out)"},"noShowTreatment":{"type":"string","enum":["none","restrictReservations"],"default":"none","description":"No-Show Treatment (pack p.12)"},"noShowThreshold":{"type":"integer","minimum":1,"nullable":true,"description":"No-shows that trigger the restriction; required for restrictReservations"},"noShowWindowDays":{"type":"integer","minimum":1,"nullable":true,"description":"Window in which no-shows are counted; required for restrictReservations"},"noShowRestrictionDays":{"type":"integer","minimum":1,"nullable":true,"default":14,"description":"Days reservation privilege stays restricted. Default 14 (decided 29 September, readiness close-out)"},"cancellationLimit":{"type":"integer","minimum":0,"nullable":true,"description":"Reservation cancellations allowed per 30 days; empty for unlimited"},"guestUsage":{"type":"string","enum":["withMemberOnly","independent"],"default":"withMemberOnly","description":"Guest Usage: whether guest tickets need the member present"},"benefitConsumption":{"type":"string","enum":["onRedemption","onValidatedVisit"],"default":"onRedemption","description":"Benefit Consumption: when a benefit counter decrements"}}},
"MembershipUsageVisitConsumptionRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Usage, Visit & Consumption Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumVisitsPerDay":{"type":"integer","description":"Maximum Visits per Day; empty for unlimited","nullable":true},"maximumAdmissionsPerPeriod":{"type":"integer","description":"Maximum Admissions per admissionPeriod; empty for unlimited","nullable":true},"reEntryCooldownMinutes":{"type":"integer","description":"Re-entry Cooldown in minutes, for reEntryPolicy afterMinutes","nullable":true},"concurrentReservations":{"type":"integer","description":"Concurrent Reservations: maximum active reservations per timeslot (pack example: one). Default 1 (decided 29 September, readiness close-out)"},"noShowTreatment":{"type":"string","enum":["none","restrictReservations"],"description":"No-Show Treatment (pack p.12)"},"cancellationLimit":{"type":"integer","description":"Cancellation Limit: reservation cancellations allowed per 30 days; empty for unlimited (decided 29 September, readiness close-out)","nullable":true},"guestUsage":{"type":"string","enum":["withMemberOnly","independent"],"description":"Guest Usage: whether guest tickets need the member present. Default withMemberOnly (decided 29 September, readiness close-out)"},"benefitConsumption":{"type":"string","enum":["onRedemption","onValidatedVisit"],"description":"Benefit Consumption: when a benefit counter decrements. Default onRedemption (decided 29 September, readiness close-out)"},"walkInAllowed":{"type":"boolean","description":"Walk-In Allowed without a reservation"},"maximumAdvanceBookingDays":{"type":"integer","description":"Maximum Advance Booking Days","nullable":true},"maximumActiveFutureReservations":{"type":"integer","description":"Maximum Active Future Reservations","nullable":true},"membershipCode":{"type":"string","description":"Membership code"},"tier":{"type":"string","description":"Tier","nullable":true},"admissionPeriod":{"type":"string","enum":["perDay","perWeek","perMonth","perMembershipYear"],"description":"Period for maximumAdmissionsPerPeriod","nullable":true},"reEntryPolicy":{"type":"string","enum":["unlimitedSameDay","noReEntry","afterMinutes","venueSpecific"],"description":"Re-entry (pack p.12)"},"reservationRequirement":{"type":"string","enum":["required","optional"],"description":"Advance Reservation (pack pp.11-12)"},"noShowThreshold":{"type":"integer","description":"No-shows that trigger the restriction (pack example: 3)","nullable":true},"noShowWindowDays":{"type":"integer","description":"Window in which no-shows are counted (pack example: 30 days)","nullable":true},"noShowRestrictionDays":{"type":"integer","description":"Days reservation privilege stays restricted. Default 14 (decided 29 September, readiness close-out)","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceList": {"x-ticvai-persistence":"catalogue.price_list","type":"object","required":["id","code","name","venueId","currency","currencyScale","channels"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"priority":{"type":"integer","description":"Where lists overlap, higher priority wins."},"description":{"type":"string","nullable":true,"description":"Price list master fields (29 September, data model DM3), set with `createPriceList` and `updatePriceList` since setPriceListMaster was retired in r2 (BC-008, CHG-CLN-001)."},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"default":"standardRetail"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"scopeLevel":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"default":"venue"},"defaultPriceCategoryId":{"type":"string","format":"uuid","nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"priceResolutionPolicyId":{"type":"string","format":"uuid","nullable":true},"allowOverrides":{"type":"boolean","default":false},"allowInheritance":{"type":"boolean","default":true},"allowMultipleCurrencies":{"type":"boolean","default":false},"allowProductSpecificRates":{"type":"boolean","default":true},"clonedFromPriceListId":{"type":"string","format":"uuid","nullable":true},"currentVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The active `catalogue.price_list_version`."}}},
"RenewalAutoRenewalMembershipContinuityConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_renewal_policy (MembershipRenewalPolicy) (decided 29 September, data model DM4)","description":"**What Renewal, Auto-Renewal & Membership Continuity Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"autoRenewEligible":{"type":"boolean","description":"Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"},"autoRenewTermsVersion":{"type":"string","description":"Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)","nullable":true},"cardOnFileRequired":{"type":"boolean","description":"Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"},"preRenewalNoticeDays":{"type":"integer","description":"Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"},"failureHandling":{"type":"string","enum":["gracePeriod","manualAction","expire"],"description":"Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code"},"renewalModes":{"type":"array","items":{"type":"string","enum":["manual","customerSelfService","agentAssisted","autoRenewal","invitationOnly","nonRenewable"]},"description":"Renewal Modes (pack p.15); nonRenewable excludes the others"},"renewalWindowOpensDaysBefore":{"type":"integer","description":"Renewal Window opens this many days before expiry. Default 60, the pack's example"},"renewalWindowClosesDaysAfter":{"type":"integer","description":"Renewal Window closes this many days after expiry. Default 30, the pack's example"},"earlyRenewalStart":{"type":"string","enum":["immediately","afterCurrentExpiry"],"description":"Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"},"renewalPriceBasis":{"type":"string","enum":["currentMembershipPrice","protectedRenewalPrice","renewalDiscount","loyaltyRate","fixedRenewalRate"],"description":"Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"},"renewalPricingProfile":{"type":"string","description":"Renewal pricing profile id in pricing (Area 10)","nullable":true},"retryIntervalsDays":{"type":"array","items":{"type":"integer"},"description":"Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"},"renewalGraceDays":{"type":"integer","description":"Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"},"revalidateOnRenewal":{"type":"array","items":{"type":"string","enum":["age","residency","membershipStatus","outstandingBalance","qualification","corporateAssociation"]},"description":"Renewal Eligibility (pack p.16): what is revalidated at renewal"},"tierMovementAtRenewal":{"type":"array","items":{"type":"string","enum":["sameTierOnly","upgradeAllowed","downgradeAllowed","suggestedTier"]},"description":"Tier Movement (pack p.16)"},"cancellationPolicyId":{"type":"string","description":"Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)","nullable":true}}},
"RenewalAutoRenewalMembershipContinuityConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Renewal, Auto-Renewal & Membership Continuity Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"autoRenewEligible":{"type":"boolean","description":"Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"},"autoRenewTermsVersion":{"type":"string","description":"Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)","nullable":true},"cardOnFileRequired":{"type":"boolean","description":"Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"},"preRenewalNoticeDays":{"type":"integer","description":"Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"},"failureHandling":{"type":"string","enum":["gracePeriod","manualAction","expire"],"description":"Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"},"membershipCode":{"type":"string","description":"Membership code"},"renewalModes":{"type":"array","items":{"type":"string","enum":["manual","customerSelfService","agentAssisted","autoRenewal","invitationOnly","nonRenewable"]},"description":"Renewal Modes (pack p.15); nonRenewable excludes the others"},"renewalWindowOpensDaysBefore":{"type":"integer","description":"Renewal Window opens this many days before expiry. Default 60, the pack's example"},"renewalWindowClosesDaysAfter":{"type":"integer","description":"Renewal Window closes this many days after expiry. Default 30, the pack's example"},"earlyRenewalStart":{"type":"string","enum":["immediately","afterCurrentExpiry"],"description":"Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"},"renewalPriceBasis":{"type":"string","enum":["currentMembershipPrice","protectedRenewalPrice","renewalDiscount","loyaltyRate","fixedRenewalRate"],"description":"Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"},"renewalPricingProfile":{"type":"string","description":"Renewal pricing profile id in pricing (Area 10)","nullable":true},"retryIntervalsDays":{"type":"array","items":{"type":"integer"},"description":"Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"},"renewalGraceDays":{"type":"integer","description":"Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"},"revalidateOnRenewal":{"type":"array","items":{"type":"string","enum":["age","residency","membershipStatus","outstandingBalance","qualification","corporateAssociation"]},"description":"Renewal Eligibility (pack p.16): what is revalidated at renewal"},"tierMovementAtRenewal":{"type":"array","items":{"type":"string","enum":["sameTierOnly","upgradeAllowed","downgradeAllowed","suggestedTier"]},"description":"Tier Movement (pack p.16)"},"cancellationPolicyId":{"type":"string","description":"Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)","nullable":true}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SetPriceRequest": {"type":"object","required":["variantId","amount"],"properties":{"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid"}}},
"ValidityActivationExpiryConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as subscription.membership_product (MembershipProduct) (decided 29 September, data model DM4)","description":"**What Validity, Activation & Expiry Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"configuredStart":{"type":"string","format":"date","description":"Configured start: start date for fixedCalendar, seasonBased and customPeriod validity, and the start of a future-dated membership (fixedStartDate activation)","nullable":true},"configuredEnd":{"type":"string","format":"date","description":"Configured end: end date for fixedCalendar, seasonBased and customPeriod validity","nullable":true},"membershipCode":{"type":"string","description":"Membership code this configuration belongs to"},"validityMethod":{"type":"string","enum":["fixedCalendar","durationFromPurchase","durationFromActivation","seasonBased","customPeriod"],"description":"Validity Method (pack p.8)"},"durationDays":{"type":"integer","description":"Duration in days for durationFromPurchase / durationFromActivation (the pack's example: 365)","nullable":true},"seasonName":{"type":"string","description":"Season name for seasonBased validity, e.g. the 2026-2027 season","nullable":true},"activationMethod":{"type":"string","enum":["immediateOnPurchase","fixedStartDate","firstVisit","manualActivation","customerActivation","membershipCardCollection","identityVerification","configuredTrigger"],"description":"Activation Method (pack pp.8-9)"},"activationDeadlineDays":{"type":"integer","description":"Activation Deadline: days after purchase by which a membership must be activated. Required when activation is deferred (firstVisit, manualActivation, customerActivation, membershipCardCollection, identityVerification, configuredTrigger); an unactivated membership expires at the deadline so it never stays open indefinitely (MoM 25 Aug fallback expiry for first-use activation). Default 90, the pack's example (decided 29 September, readiness close-out)","nullable":true},"expiryRule":{"type":"string","enum":["exactExpiryDate","endOfDay","endOfSeason","duration"],"description":"Expiry (pack p.9)"},"gracePeriodDays":{"type":"integer","description":"Grace Period: days after expiry during which renewal continues the membership without a gap. Default 0 (decided 29 September, readiness close-out)"},"backdatingAllowed":{"type":"boolean","description":"Backdating: whether authorised staff may backdate activation. Default false (decided 29 September, readiness close-out)"},"backdatingApprovalRequired":{"type":"boolean","description":"Backdating needs a second user's approval. Default true (decided 29 September, readiness close-out)"}}},
"ValidityActivationExpiryConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Validity, Activation & Expiry Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"configuredStart":{"type":"string","format":"date","description":"Configured start: start date for fixedCalendar, seasonBased and customPeriod validity, and the start of a future-dated membership (fixedStartDate activation)","nullable":true},"configuredEnd":{"type":"string","format":"date","description":"Configured end: end date for fixedCalendar, seasonBased and customPeriod validity","nullable":true},"membershipCode":{"type":"string","description":"Membership code this configuration belongs to"},"validityMethod":{"type":"string","enum":["fixedCalendar","durationFromPurchase","durationFromActivation","seasonBased","customPeriod"],"description":"Validity Method (pack p.8)"},"durationDays":{"type":"integer","description":"Duration in days for durationFromPurchase / durationFromActivation (the pack's example: 365)","nullable":true},"seasonName":{"type":"string","description":"Season name for seasonBased validity, e.g. the 2026-2027 season","nullable":true},"activationMethod":{"type":"string","enum":["immediateOnPurchase","fixedStartDate","firstVisit","manualActivation","customerActivation","membershipCardCollection","identityVerification","configuredTrigger"],"description":"Activation Method (pack pp.8-9)"},"activationDeadlineDays":{"type":"integer","description":"Activation Deadline: days after purchase by which a membership must be activated. Required when activation is deferred (firstVisit, manualActivation, customerActivation, membershipCardCollection, identityVerification, configuredTrigger); an unactivated membership expires at the deadline so it never stays open indefinitely (MoM 25 Aug fallback expiry for first-use activation). Default 90, the pack's example (decided 29 September, readiness close-out)","nullable":true},"expiryRule":{"type":"string","enum":["exactExpiryDate","endOfDay","endOfSeason","duration"],"description":"Expiry (pack p.9)"},"gracePeriodDays":{"type":"integer","description":"Grace Period: days after expiry during which renewal continues the membership without a gap. Default 0 (decided 29 September, readiness close-out)"},"backdatingAllowed":{"type":"boolean","description":"Backdating: whether authorised staff may backdate activation. Default false (decided 29 September, readiness close-out)"},"backdatingApprovalRequired":{"type":"boolean","description":"Backdating needs a second user's approval. Default true (decided 29 September, readiness close-out)"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
