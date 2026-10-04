# WS30 — Membership   Annual Pass Management board 2

**10 screens · 19 operations · 31 schemas · 6 permissions**

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
  `APPROVAL_REQUEST, GUEST_MANAGE, ORDER_MODIFY, PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-294` | Member Operations Command Center | B | 2 | 264 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-295` | Member 360° Membership Account Workspace | B | 0 | 48 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-296` | Membership Activation, Assignment & Credential Management | B | 5 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | B | 0 | 182 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | B | 7 | 0 | 5 | 4 | 1 | 0 | — | notStarted (generated) |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | B | 4 | 0 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `BO-300` | Renewal Operations & Auto-Renewal Management | B | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | B | 6 | 0 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | B | 0 | 8 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | B | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-300, BO-302 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-294` Member Operations Command Center

**Provide membership teams with a real-time operational dashboard for the complete active member population.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-294 |
| Who uses it | venue staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/member-operations-command-center-bo-294` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The membership team's live view of members: new, activated, pending, expiring, renewal due, suspended, at risk.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMember (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search member operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product, tier, status, member type, activation and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | text field | — | — | `listMember` ?product |
| Customer segment | text field | — | — | `listMember` ?customerSegment |
| Status | radio group | — | Active · Frozen · Suspended · Expired · Cancelled | `listMember` ?status |
| Activation | radio group | — | Purchased · Pending assignment · Pending activation · Activated | `listMember` ?activation |
| Renewal | select | — | Renewal not open · Renewal eligible · Renewal invitation sent · Renewal started · Payment pending · Renewed · Auto renew scheduled · Auto renew failed · Grace period · Expired without renewal | `listMember` ?renewal |
| Usage | radio group | — | None · Low · Regular · High | `listMember` ?usage |
| Member type | segmented control | — | Individual · Family · Corporate | `listMember` ?memberType |
| Expiring within days | number field (days) | — | — | `listMember` ?expiringWithinDays |
| Venue | text field | — | — | `listMember` ?venue |
| Tier | text field | — | — | `listMember` ?tier |
| Acquisition channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listMember` ?acquisitionChannel |
| At risk | toggle | — | — | `listMember` ?atRisk |

#### Outputs: what the screen shows and produces

**Shown**

**Active Members** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**New Members Today** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Activated Today** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Pending Activation** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Expiring in 30 Days** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Renewal due** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Renewed This Month** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Renewal rate** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Suspended Memberships** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Frozen Memberships** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Membership Exceptions** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**At risk members** (metric tile, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |
| Customer | text | Customer ID of the member (CRM profile) |
| Activation stage | chip: Purchased, Pending assignment, Pending activation, Activated | Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation) |
| At risk | yes / no (icon or chip) | Flagged at risk, e.g. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Member Operations Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active members | 1,234 | Active Members |

**Every member operations** (data table, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |

**The selected member operations** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Membership | text | Membership ID |
| Member | text | Member name |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Venue | text | Venue |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Membership status | text | Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Usage level | chip: None, Low, Regular, High | Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness … |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Outstanding issue | text | Outstanding Issue, e.g. |
| Owner | text | Owner |

**Data it reads**: `listMember` (onLoad, Member Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-297` Visit, Admission & Entitlement Usage Monitor: *Works in Visit, Admission & Entitlement Usage Monitor*; calls `listMember`
- → `BO-298` Membership Freeze, Suspension & Reactivation Management: *Works in Membership Freeze, Suspension & Reactivation Management*; calls `listMember`
- → `BO-302` Member Lifecycle History, Audit & Case Timeline: *Works in Member Lifecycle History, Audit & Case Timeline*; calls `listMember`
- → `BO-303` Membership Analytics, Renewal Intelligence & AI Retention Center: *Works in Membership Analytics, Renewal Intelligence & AI Retention Center*; calls `listMember`
- → `BO-295` Member 360° Membership Account Workspace: *Works in Member 360° Membership Account Workspace*; carries `membershipId`; calls `listMember`
- → `BO-296` Membership Activation, Assignment & Credential Management: *Works in Membership Activation, Assignment & Credential Management*; carries `membershipId`; calls `listMember`
- → `BO-299` Membership Upgrade, Downgrade & Product Migration Operations: *Works in Membership Upgrade, Downgrade & Product Migration Operations*; carries `membershipId`; calls `listMember`
- → `BO-300` Renewal Operations & Auto-Renewal Management: *Works in Renewal Operations & Auto-Renewal Management*; carries `membershipId`; calls `listMember`
- → `BO-301` Member Exceptions, Overrides & Service Recovery: *Works in Member Exceptions, Overrides & Service Recovery*; carries `membershipId`; calls `listMember`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member operations yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Members: 128
  New Members Today: 46
  Activated Today: 312
  Pending Activation: 74
  Expiring in 30 Days: 19
  Renewal due: 233
  Renewed This Month: 57
  Renewal rate: 87%
  Suspended Memberships: AED 12,400.00
  Frozen Memberships: 46
Every member operations:
- activationDate: 01/10/2026 09:14
  expiryDate: 01/10/2026 09:14
- activationDate: 30/09/2026 18:02
  expiryDate: 30/09/2026 18:02
- activationDate: 28/09/2026 11:45
  expiryDate: 28/09/2026 11:45
```

#### Permissions

- `listMember` → `PLATFORM_TENANT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-294` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-294`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 1: Opens Member Operations Command Center → Provide membership teams with a real-time operational dashboard for the complete active member population.
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F139 branch at step 1 (expected): when Nothing has been set up on Member Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F139 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (264 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-294?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-297`, `BO-298`, `BO-302`, `BO-303`, `BO-295`, `BO-296`, `BO-299`, `BO-300`, `BO-301`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-295` Member 360° Membership Account Workspace

**Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-295 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `PLATFORM_CELL_MANAGE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) · cold entry: Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/sell/member-360-membership-account-workspace-bo-295` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One member's whole membership: product, tier, status, dates, usage, renewal, household and cases; the screen a membership-service agent opens first.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: setMemberMembershipAccount (PLATFORM_CELL_MANAGE). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every member 360° membership** (data table, from `setMemberMembershipAccount`)

| Shows | Format | Notes |
|---|---|---|
| Member name | text | Member Name |
| Customer | text | Customer ID |
| Membership | text | Membership ID |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Status | text | Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Primary venue | text | Primary Venue |
| Credential status | text | Credential Status: notIssued, active, disabled or replaced |
| Primary member | text | Primary Member |
| Secondary adult | text | Secondary Adult name |
| Dependents | list or chips (count when long) | Dependents on the membership |
| Shared benefits | list or chips (count when long) | Shared Benefits with allocation, used and remaining |
| Individual benefits | list or chips (count when long) | Individual Benefits with allocation, used and remaining |
| Membership version | 1,234 | Membership Version the contract is on |
| Purchase date | 1 Oct 2026 | Purchase Date |
| Purchase channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Purchase Channel |
| Original order | text | Original Order id |
| Validity | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method |
| Renewal policy | text | Renewal Policy: the product's renewal modes, e.g. |
| Auto renew status | text | Auto-Renew Status: off, optedIn, scheduled or failed; only the member's explicit opt-in sets optedIn |

**The selected member 360° membership** (detail panel): The pack groups this record's detail under its own headings: “Guest Tickets”, “Free Parking”, “F&B Benefit”, “Retail Benefit”, “Link to”.

| Shows | Format | Notes |
|---|---|---|
| Member name | text | Member Name |
| Customer | text | Customer ID |
| Membership | text | Membership ID |
| Membership product | text | Membership Product |
| Tier | text | Tier |
| Status | text | Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue … |
| Activation date | 1 Oct 2026 | Activation Date |
| Expiry date | 1 Oct 2026 | Expiry Date |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |
| Primary venue | text | Primary Venue |
| Credential status | text | Credential Status: notIssued, active, disabled or replaced |
| Primary member | text | Primary Member |
| Secondary adult | text | Secondary Adult name |
| Dependents | list or chips (count when long) | Dependents on the membership |
| Shared benefits | list or chips (count when long) | Shared Benefits with allocation, used and remaining |
| Individual benefits | list or chips (count when long) | Individual Benefits with allocation, used and remaining |
| Membership version | 1,234 | Membership Version the contract is on |
| Purchase date | 1 Oct 2026 | Purchase Date |
| Purchase channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Purchase Channel |
| Original order | text | Original Order id |
| Validity | chip: Fixed calendar, Duration from purchase, Duration from activation, Season based … | Validity method |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method |
| Renewal policy | text | Renewal Policy: the product's renewal modes, e.g. |
| Auto renew status | text | Auto-Renew Status: off, optedIn, scheduled or failed; only the member's explicit opt-in sets optedIn |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Activate, Freeze, Suspend, Resume, Renew, Replace Credential, Add Note, Review Eligibility, Manage Dependents. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `setMemberMembershipAccount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member 360° membership list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member 360° membership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member 360° membership yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member 360° membership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The benefit is exhausted for this period, or the membership is not active |

#### Edge cases to draw

- **Agent without personal-data permission**: Contact details masked; usage and status visible. *(source: ADR-0023)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **recordBenefitUsage answers 409**: Show it as something the person can act on, not a failure: The benefit is exhausted for this period, or the membership is not active *(source: contracts/spine/identity.yaml#recordBenefitUsage)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every member 360° membership:
- status: active
  activationDate: 01/10/2026 09:14
  expiryDate: 01/10/2026 09:14
- status: pending
  activationDate: 30/09/2026 18:02
  expiryDate: 30/09/2026 18:02
- status: suspended
  activationDate: 28/09/2026 11:45
  expiryDate: 28/09/2026 11:45
```

#### Permissions

- `setMemberMembershipAccount` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `recordBenefitUsage` → `GUEST_MANAGE` (configure) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-295` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-295`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 2: Works in Member 360° Membership Account Workspace → Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-295?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `PLATFORM_CELL_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-296` Membership Activation, Assignment & Credential Management

**Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-296 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) |
| Route | `/sell/membership-activation-assignment-credential-management-bo-296` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Turning a purchased membership into an active one assigned to a person, with credential issue, replace, link or block.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMembershipActivationCredential (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Queue stage | radio group | — | Awaiting member assignment · Awaiting identity verification · Awaiting document verification · Awaiting activation · Activation failed | `listMembershipActivationCredential` ?queueStage |
| Membership product | text field | — | — | `listMembershipActivationCredential` ?membershipProduct |
| Venue | text field | — | — | `listMembershipActivationCredential` ?venue |
| Search | text field | — | — | `listMembershipActivationCredential` ?search |

**Sent by *Block*** (`resolveMembershipActivation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Activate · Block · Review · Replace · Link · Escalate | — | The activation-queue action (decided 29 September, readiness close-out). | `resolveMembershipActivation` body |
| Credential `credentialId` | picker: choose a credential | optional | — | — | shows names, sends the id | The credential being replaced. Required for `replace`. | `resolveMembershipActivation` body |
| Media code `mediaCode` | text field | optional | — | max length 100 | — | The new media's code. Required for `replace`. | `resolveMembershipActivation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the membership is linked to. Required for `link`. | `resolveMembershipActivation` body |
| Reason `reason` | text area | optional | — | min length 3; max length 500 | — | Required for `block` and `escalate`. | `resolveMembershipActivation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every membership activation credential** (data table, from `listMembershipActivationCredential`)

| Shows | Format | Notes |
|---|---|---|
| Purchase date | 1 Oct 2026 | Purchase Date |
| Eligible activation date | 1 Oct 2026 | Eligible Activation Date |
| Activation deadline | 1 Oct 2026 | Activation Deadline; an unactivated membership expires here |
| Selected start date | 1 Oct 2026 | Selected Start Date |
| Calculated expiry | 1 Oct 2026 | Calculated Expiry |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method |

**The selected membership activation credential** (detail panel): The pack groups this record's detail under its own headings: “Show memberships”, “Purchased Membership”, “Associate membership with”, “Record reason”.

| Shows | Format | Notes |
|---|---|---|
| Purchase date | 1 Oct 2026 | Purchase Date |
| Eligible activation date | 1 Oct 2026 | Eligible Activation Date |
| Activation deadline | 1 Oct 2026 | Activation Deadline; an unactivated membership expires here |
| Selected start date | 1 Oct 2026 | Selected Start Date |
| Calculated expiry | 1 Oct 2026 | Calculated Expiry |
| Activation method | chip: Immediate on purchase, Fixed start date, First visit, Manual activation, Customer … | Activation Method |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Block (primary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Review (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Replace (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Link (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Escalate (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |

**Data it reads**: `listMembershipActivationCredential` (onLoad, Membership Activation, Assignment & Credential Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipActivationCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership activation credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership activation credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership activation credential yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership activation credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without a `reason` (`activation-action-incomplete`). |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ORDER_MODIFY for Block. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/orders.yaml#resolveMembershipActivation)*
- **resolveMembershipActivation answers 422**: Show it as something the person can act on, not a failure: `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without a `reason` (`activation-action-incomplete`). *(source: contracts/spine/orders.yaml#resolveMembershipActivation)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every membership activation credential:
- purchaseDate: 01/10/2026 09:14
  eligibleActivationDate: 01/10/2026 09:14
  selectedStartDate: 01/10/2026 09:14
- purchaseDate: 30/09/2026 18:02
  eligibleActivationDate: 30/09/2026 18:02
  selectedStartDate: 30/09/2026 18:02
- purchaseDate: 28/09/2026 11:45
  eligibleActivationDate: 28/09/2026 11:45
  selectedStartDate: 28/09/2026 11:45
```

#### Permissions

- `listMembershipActivationCredential` → `PLATFORM_TENANT_VIEW` (read) · staff
- `resolveMembershipActivation` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-296` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-296`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 4: Works in Membership Activation, Assignment & Credential Management → Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-296?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Block, Review, Replace, Link, Escalate.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-297` Visit, Admission & Entitlement Usage Monitor

**Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-297 |
| Who uses it | venue staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/visit-admission-entitlement-usage-monitor-bo-297` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How a member uses admission and benefits: visits, guest tickets, parking, no-shows.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listVisitAdmissionEntitlement (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | text field | — | — | `listVisitAdmissionEntitlement` ?membershipId |
| From | date picker | — | — | `listVisitAdmissionEntitlement` ?from |
| To | date picker | — | — | `listVisitAdmissionEntitlement` ?to |
| Venue | text field | — | — | `listVisitAdmissionEntitlement` ?venue |
| Validation result | select | — | Admitted · Usage above limit · Invalid re entry · Benefit exhausted · Blackout attempt · Expired membership usage · Suspended membership attempt | `listVisitAdmissionEntitlement` ?validationResult |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Visits** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Visits This Month** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Last Visit** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Upcoming Reservation start** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Guest Tickets Used** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Guest Tickets Remaining** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Parking Uses** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Benefit usage** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**No-Shows** (metric tile, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Date | 1 Oct 2026 | Date of the visit |
| Venue | text | Venue |
| Attraction | text | Attraction |
| Gate | text | Gate |
| Entry time | 1 Oct 2026, 14:30 | Entry Time |
| Exit time | 1 Oct 2026, 14:30 | Exit time where the venue records exits |
| Credential | text | Credential presented (credential id) |
| Reservation | text | Reservation id, where the visit was booked |
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |
| Membership | text | Membership ID |
| Visit | text | Visit (access event) id |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Visit, Admission & Entitlement Usage Monitor. The pack's KPI cards, split out of the row (decided 29 September … |
| Total visits | 1,234 | Total Visits |
| Visits this month | 1,234 | Visits This Month |
| Last visit | 1 Oct 2026, 14:30 | Last Visit |
| Upcoming reservation | 1 Oct 2026, 14:30 | Upcoming Reservation start |
| Guest tickets used | 1,234 | Guest Tickets Used |

**Every visit admission entitlement** (data table, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |

**The selected visit admission entitlement** (detail panel): The pack groups this record's detail under its own headings: “Benefit”, “Guest”, “Parking 18 Unlimited”, “Manual Adjustment”, “Require”.

| Shows | Format | Notes |
|---|---|---|
| Validation result | chip: Admitted, Usage above limit, Invalid re entry, Benefit exhausted, Blackout attempt … | Validation Result from Access Control |

**Data it reads**: `listVisitAdmissionEntitlement` (onLoad, Visit, Admission & Entitlement Usage Monitor)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listVisitAdmissionEntitlement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visit admission entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visit admission entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visit admission entitlement yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visit admission entitlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Total Visits: 128
  Visits This Month: 46
  Last Visit: 312
  Upcoming Reservation start: 74
  Guest Tickets Used: 19
  Guest Tickets Remaining: 233
  Parking Uses: 57
  Benefit usage: 42 min
  No-Shows: 128
```

#### Permissions

- `listVisitAdmissionEntitlement` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*
- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-297` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-297`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 6: Works in Visit, Admission & Entitlement Usage Monitor → Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (182 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-297?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-298` Membership Freeze, Suspension & Reactivation Management

**Manage temporary interruption of membership rights without necessarily terminating the membership contract.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-298 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Freeze Configuration Consumption; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `entitlementId` (navigation) · cold entry: Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty … |
| Route | `/sell/membership-freeze-suspension-reactivation-management-bo-298` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Interrupt a membership without ending it. Freeze is the guest's request (travel, injury): consumption stops and validity extends by the frozen days. Suspension is a sanction (fraud, chargeback): entry is denied and the time lost is not given back. The two must look different.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start Date | select field | — | — | — | — | — | — |
| End Date | select field | — | — | — | — | — | — |
| Duration | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | The freeze reasons of `freezeEntitlement`: travelling, injury, personal, seasonal, other. **Choosing Other makes Note required** (decided 28 September, audit R222). | — |
| Note | text field | — | — | — | — | **Required, at least 3 characters, when the reason is Other** — the form will not submit without it, and `freezeEntitlement` refuses 400 (decided 28 September, audit R222). Optional for every other … | — |
| Requested By | select field | — | — | — | — | — | — |
| Approved By | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Interruption type | segmented control | — | Freeze · Suspension · Administrative hold | `listMembershipFreezeSuspension` ?interruptionType |
| Membership | text field | — | — | `listMembershipFreezeSuspension` ?membershipId |
| Active only | toggle | — | — | `listMembershipFreezeSuspension` ?activeOnly |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Freeze (primary button) | navigation or local | — | — | — | — |
| Suspend (destructive button) | navigation or local | — | — | — | — |
| Resume (secondary button) | navigation or local | — | — | — | — |
| Reactivate (secondary button) | navigation or local | — | — | — | — |
| Administrative Hold (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Freeze**: Reason (travelling, injury, personal, seasonal, other) and dates; shows the new expiry. *(source: contracts/spine/catalogue.yaml#freezeEntitlement)*
- **Suspend**: Sanction with a reason an operator can read out at the gate; the confirmation says validity will not be extended. *(source: contracts/spine/catalogue.yaml#suspendEntitlement / contracts/spine/catalogue.yaml#reinstateEntitlement)*

**Data it reads**: `listMembershipFreezeSuspension` (onLoad, Membership Freeze, Suspension & Reactivation Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipFreezeSuspension`

**What opens over it**

- confirmDialog *Suspend*: **Suspend on a membership freeze suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership freeze suspension configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership freeze suspension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership freeze suspension configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
member:
  name: Yousef Al Hammadi / يوسف الحمادي
  pass: Annual Pass Gold
  validTo: '2027-03-31'
  freeze:
    reason: travelling
    days: 45
    newValidTo: '2027-05-15'
```

#### Permissions

- `listMembershipFreezeSuspension` → `PLATFORM_TENANT_VIEW` (read) · staff
- `freezeEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff, guest
- `reinstateEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `suspendEntitlement` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.13 | Allow temporary suspension of memberships. | Ticketing Sales | CONTRACTED | `freezeEntitlement` |
| 1.1.100 | Membership reactivation | Ticketing Catalogue | CONTRACTED | `reinstateEntitlement` |
| 1.1.99 | Membership suspension | Ticketing Catalogue | CONTRACTED | `suspendEntitlement` |
| 3.2.22 | The system should allow manual disabling of access for an individual guest ticket. | Admission and Access | CONTRACTED | `suspendEntitlement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-298` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-298`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 8: Works in Membership Freeze, Suspension & Reactivation Management → Manage temporary interruption of membership rights without necessarily terminating the membership contract.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-298?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Freeze, Suspend, Resume, Reactivate, Administrative Hold.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-299` Membership Upgrade, Downgrade & Product Migration Operations

**Manage operational movement of an active member between membership products or tiers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-299 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `membershipId` (navigation) |
| Route | `/sell/membership-upgrade-downgrade-product-migration-operation-bo-299` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Move an active member between products or tiers now, at the next visit, renewal or end of term, with price difference shown.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMembershipUpgradeDowngrade (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Movement type | segmented control | — | Upgrade · Downgrade · Migration | `listMembershipUpgradeDowngrade` ?movementType |
| Membership product | text field | — | — | `listMembershipUpgradeDowngrade` ?membershipProduct |
| Bulk migration | text field | — | — | `listMembershipUpgradeDowngrade` ?bulkMigrationId |

**Sent by *Migrate membership*** (`migrateMembership`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target product `targetProductId` | picker: choose a target product | required | — | — | shows names, sends the id | The membership product it moves to. | `migrateMembership` body |
| Direction `direction` | segmented control | required | — | Upgrade · Downgrade · Migration | — | Which way it moves (decided 29 September, readiness close-out). | `migrateMembership` body |
| Effective timing `effectiveTiming` | radio group | required | — | Immediate · Next visit · Next renewal · End of current term | — | When the move takes effect (decided 29 September, readiness close-out). | `migrateMembership` body |
| Pro rata `proRata` | toggle | optional | off | — | — | Charge or credit the difference for the remaining term. | `migrateMembership` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Next Visit (primary button) | navigation or local | — | — | — | — |
| Next Renewal (secondary button) | navigation or local | — | — | — | — |
| End of Current Term (destructive button) | navigation or local | — | — | — | — |
| Migrate membership (primary button) | `migrateMembership` POST `/memberships/{membershipId}/migrations` | MembershipMigrationInput | MembershipMigrationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The membership is not active (`membershipNotActive`), the target is the product it already holds … | — |

**Data it reads**: `listMembershipUpgradeDowngrade` (onLoad, Membership Upgrade, Downgrade & Product Migration Operations)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipUpgradeDowngrade`

**What opens over it**

- confirmDialog *End of Current Term*: **End of Current Term on a membership upgrade downgrade is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership upgrade downgrade list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership upgrade downgrade untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership upgrade downgrade yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership upgrade downgrade are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The membership is not active (`membershipNotActive`), the target is the product it already holds (`sameProduct`), or a migration is already scheduled … (MembershipMigrationProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ORDER_MODIFY for Migrate membership. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/orders.yaml#migrateMembership)*
- **migrateMembership answers 409**: Show it as something the person can act on, not a failure: The membership is not active (`membershipNotActive`), the target is the product it already holds (`sameProduct`), or a migration is already scheduled (`migrationAlreadyScheduled`). *(source: contracts/spine/orders.yaml#migrateMembership)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMembershipUpgradeDowngrade (MembershipUpgradeDowngradeProductMigrationOperationsView):
- customerQualification: eligible
  usage: 12
  remainingValidity: 12
  effectiveDate: 01/10/2026 09:14
- customerQualification: notEligible
  usage: 3
  remainingValidity: 3
  effectiveDate: 30/09/2026 18:02
```

#### Permissions

- `listMembershipUpgradeDowngrade` → `PLATFORM_TENANT_VIEW` (read) · staff
- `migrateMembership` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.21 | System shall allow members to downgrade from one membership tier to another according to configurable business rules, effective dates, and entitlement adjustment policies. | Ticketing Sales | CONTRACTED | `migrateMembership` |
| 13.3.3 | APIs shall support membership creation, renewal, upgrade, downgrade, freeze, entitlement validation and membership status retrieval. | Developer & API Management | CONTRACTED | `migrateMembership` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-299` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-299`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 10: Works in Membership Upgrade, Downgrade & Product Migration Operations → Manage operational movement of an active member between membership products or tiers.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-299?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Next Visit, Next Renewal, End of Current Term, Migrate membership.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-300` Renewal Operations & Auto-Renewal Management

**Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-300 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) · cold entry: Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/sell/renewal-operations-auto-renewal-management-bo-300` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Memberships approaching expiry and the renewal actions: auto-renew status, payment method validity, renewal price.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listRenewalAuto (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Renewal status | select | — | Renewal not open · Renewal eligible · Renewal invitation sent · Renewal started · Payment pending · Renewed · Auto renew scheduled · Auto renew failed · Grace period · Expired without renewal | `listRenewalAuto` ?renewalStatus |
| Membership product | text field | — | — | `listRenewalAuto` ?membershipProduct |
| Tier | text field | — | — | `listRenewalAuto` ?tier |
| Auto renew | toggle | — | — | `listRenewalAuto` ?autoRenew |
| Expiring from | date picker | — | — | `listRenewalAuto` ?expiringFrom |
| Expiring to | date picker | — | — | `listRenewalAuto` ?expiringTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every renewal operations auto-renewal** (data table, from `listRenewalAuto`)

| Shows | Format | Notes |
|---|---|---|
| Member | text | Member |
| Membership | text | Membership |
| Tier | text | Tier |
| Expiry | 1 Oct 2026 | Expiry |
| Renewal window | grouped details | Renewal Window |
| Renewal price | AED 1,234.50 | Renewal Price from pricing (Area 10) |
| Auto renew | yes / no (icon or chip) | Auto-Renew: the member has explicitly opted in |
| Payment method status | text | Payment Method Status: none, valid, expiringSoon, expired or failed |
| Eligibility | chip: Eligible, Not eligible, Review required | Eligibility for renewal |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |

**The selected renewal operations auto-renewal** (detail panel): The pack groups this record's detail under its own headings: “Segment members into”, “Validate”, “Final failure”, “Renewal Grace”, “Renewal Continuity”, “Current expiry”.

| Shows | Format | Notes |
|---|---|---|
| Member | text | Member |
| Membership | text | Membership |
| Tier | text | Tier |
| Expiry | 1 Oct 2026 | Expiry |
| Renewal window | grouped details | Renewal Window |
| Renewal price | AED 1,234.50 | Renewal Price from pricing (Area 10) |
| Auto renew | yes / no (icon or chip) | Auto-Renew: the member has explicitly opted in |
| Payment method status | text | Payment Method Status: none, valid, expiringSoon, expired or failed |
| Eligibility | chip: Eligible, Not eligible, Review required | Eligibility for renewal |
| Renewal status | text | Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled … |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (renewalPrice)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listRenewalAuto` (onLoad, Renewal Operations & Auto-Renewal Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listRenewalAuto`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal operations auto-renewal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal operations auto-renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal operations auto-renewal yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the renewal operations auto-renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Outside the grace period (`outsideGracePeriod`), or already renewed for this term (`alreadyRenewedForTerm`). (MembershipRenewalProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ORDER_MODIFY for renewMembership. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/orders.yaml#renewMembership)*
- **renewMembership answers 409**: Show it as something the person can act on, not a failure: Outside the grace period (`outsideGracePeriod`), or already renewed for this term (`alreadyRenewedForTerm`). *(source: contracts/spine/orders.yaml#renewMembership)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listRenewalAuto (RenewalOperationsAutoRenewalManagementView):
- expiry: 01/10/2026 09:14
  renewalPrice: AED 1,250.00
  autoRenew: true
  eligibility: eligible
- expiry: 30/09/2026 18:02
  renewalPrice: AED 48,000.00
  autoRenew: false
  eligibility: notEligible
```

#### Permissions

- `listRenewalAuto` → `PLATFORM_TENANT_VIEW` (read) · staff
- `renewMembership` → `ORDER_MODIFY` (operate) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.96 | The system shall support subscription creation, renewal, upgrade, downgrade, suspension, cancellation, expiry, and reactivation. Applicable to memberships, annual passes, recurring services, and … | F&B & Guest Management | CONTRACTED | `renewMembership` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-300` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-300`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 12: Works in Renewal Operations & Auto-Renewal Management → Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-300?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-301` Member Exceptions, Overrides & Service Recovery

**Provide controlled handling of member-specific situations that fall outside normal membership policy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-301 |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE` (2 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `membershipId` (navigation), `entitlementId` (navigation) · cold entry: Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty … |
| Route | `/sell/member-exceptions-overrides-service-recovery-bo-301` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Member situations outside policy, each recorded with its reason and author: eligibility override, expiry extension, complimentary renewal or benefit, entitlement adjustment, freeze exception, suspension override, replacement credential. Complimentary renewal and benefit move money and need an approved request first.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Exception type | select | — | Eligibility override · Activation extension · Expiry extension · Complimentary renewal · Complimentary benefit · Entitlement adjustment · Freeze exception · Suspension override · Replacement credential · Renewal exception · Dependent exception | `listMemberExceptionOverride` ?exceptionType |
| Approval status | radio group | — | Pending · Approved · Rejected · Applied | `listMemberExceptionOverride` ?approvalStatus |
| Membership | text field | — | — | `listMemberExceptionOverride` ?membershipId |

**Sent by *Eligibility Override*** (`createMemberException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Eligibility override · Expiry extension · Complimentary renewal · Complimentary benefit · Entitlement adjustment · Freeze exception · Suspension override · Replacement credential | — | The exception kind (decided 29 September, readiness close-out). `complimentaryRenewal` and `complimentaryBenefit` move money and need an approved `approvalRequestId`. | `createMemberException` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createMemberException` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The approved request in `approvals`. Required for `complimentaryRenewal` and `complimentaryBenefit`. | `createMemberException` body |
| Extend days `extendDays` | number field (days) | optional | — | min 1; max 366 | — | Required for `expiryExtension`. | `createMemberException` body |
| Benefit `benefitId` | picker: choose a benefit | optional | — | — | shows names, sends the id | The plan benefit (`catalogue.membership_benefit`). Required for `complimentaryBenefit` and `entitlementAdjustment`. | `createMemberException` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | How many of the benefit. Required with `benefitId`. | `createMemberException` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kind**: The kind decides the extra field (days to extend, benefit and quantity); money-moving kinds show "needs approval" and submit an approval request. *(source: contracts/spine/orders.yaml#createMemberException / contracts/spine/approvals.yaml#createApprovalRequest)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Eligibility Override (primary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Expiry Extension (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Complimentary Renewal (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Complimentary Benefit (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Entitlement Adjustment (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Freeze Exception (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Suspension Override (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Replacement Credential (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |

**Data it reads**: `listMemberExceptionOverride` (onLoad, Member Exceptions, Overrides & Service Recovery)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMemberExceptionOverride`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member exceptions overrides list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member exceptions overrides untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member exceptions overrides yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member exceptions overrides are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222).; 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem); 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). (MemberExceptionProblem); 422 A money-moving kind (`complimentaryRenewal`, `complimentaryBenefit`) with … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  member: Fatima Al Nuaimi
  kind: expiryExtension
  days: 30
  reason: Park closed 3 weeks for refurbishment
```

#### Permissions

- `listMemberExceptionOverride` → `PLATFORM_TENANT_VIEW` (read) · staff
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `freezeEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff, guest
- `reinstateEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `createMemberException` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 2.14.13 | Allow temporary suspension of memberships. | Ticketing Sales | CONTRACTED | `freezeEntitlement` |
| 1.1.100 | Membership reactivation | Ticketing Catalogue | CONTRACTED | `reinstateEntitlement` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-301` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-301`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 14: Works in Member Exceptions, Overrides & Service Recovery → Provide controlled handling of member-specific situations that fall outside normal membership policy.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-301?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Eligibility Override, Expiry Extension, Complimentary Renewal, Complimentary Benefit, Entitlement Adjustment, Freeze Exception, Suspension Override, Replacement Credential.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-302` Member Lifecycle History, Audit & Case Timeline

**Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-302 |
| Who uses it | venue staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/member-lifecycle-history-audit-case-timeline-bo-302` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Everything that happened to a membership from purchase to expiry, as a timeline.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMemberLifecycleCase (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | text field | — | — | `listMemberLifecycleCase` ?membershipId |
| Event type | select | — | Purchase · Assignment · Activation · Visit · Benefit usage · Dependent change · Credential change · Freeze · Suspension · Reactivation · Upgrade · Downgrade … | `listMemberLifecycleCase` ?eventType |
| Actor type | select | — | Customer · Agent · Manager · System · API · Integration | `listMemberLifecycleCase` ?actorType |
| From | date and time picker | — | — | `listMemberLifecycleCase` ?from |
| To | date and time picker | — | — | `listMemberLifecycleCase` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every member lifecycle history** (data table, from `listMemberLifecycleCase`)

| Shows | Format | Notes |
|---|---|---|
| Event type | chip: Purchase, Assignment, Activation, Visit, Benefit usage, Dependent change… | Event (pack pp.33-34) |
| Freeze | text | not in the schema: `Freeze` |
| Upgrade | text | not in the schema: `Upgrade` |
| Downgrade | text | not in the schema: `Downgrade` |

**The selected member lifecycle history** (detail panel): The pack groups this record's detail under its own headings: “Before/After Audit”, “Expiry”, “Reason”, “Record”, “Link to”, “Case Notes”.

| Shows | Format | Notes |
|---|---|---|
| Event type | chip: Purchase, Assignment, Activation, Visit, Benefit usage, Dependent change… | Event (pack pp.33-34) |
| Freeze | text | not in the schema: `Freeze` |
| Upgrade | text | not in the schema: `Upgrade` |
| Downgrade | text | not in the schema: `Downgrade` |

**Data it reads**: `listMemberLifecycleCase` (onLoad, Member Lifecycle History, Audit & Case Timeline)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMemberLifecycleCase`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member lifecycle history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member lifecycle history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member lifecycle history yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member lifecycle history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every member lifecycle history:
- Freeze: 57
  Upgrade: 11
  Downgrade: 46
- Freeze: 11
  Upgrade: 128
  Downgrade: 312
- Freeze: 128
  Upgrade: 46
  Downgrade: 74
```

#### Permissions

- `listMemberLifecycleCase` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-302` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-302`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 16: Works in Member Lifecycle History, Audit & Case Timeline → Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-302?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-303` Membership Analytics, Renewal Intelligence & AI Retention Center

**Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | Block B · task VM-BO-303 |
| Who uses it | venue staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display; Forecast) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-analytics-renewal-intelligence-ai-retention-c-bo-303` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Membership retention and renewal analytics with AI churn signals and suggested offers.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMembershipRenewalRetention (PLATFORM_TENANT_VIEW). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search membership analytics renewal | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by membership product, tier, purchase month, venue, acquisition channel, customer segment and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership product | text field | — | — | `listMembershipRenewalRetention` ?membershipProduct |
| Tier | text field | — | — | `listMembershipRenewalRetention` ?tier |
| Venue | text field | — | — | `listMembershipRenewalRetention` ?venue |
| Customer segment | text field | — | — | `listMembershipRenewalRetention` ?customerSegment |
| Geography | text field | — | — | `listMembershipRenewalRetention` ?geography |
| Renewal cohort | text field | — | — | `listMembershipRenewalRetention` ?renewalCohort |
| Purchase month | text field | — | pattern `^[0-9]{4}-[0-9]{2}$` | `listMembershipRenewalRetention` ?purchaseMonth |
| Acquisition channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listMembershipRenewalRetention` ?acquisitionChannel |
| Churn flag | toggle | — | — | `listMembershipRenewalRetention` ?churnFlag |
| Max renewal probability | number field | — | — | `listMembershipRenewalRetention` ?maxRenewalProbability |

#### Outputs: what the screen shows and produces

**Shown**

**Active Members** (metric tile)

**New Memberships** (metric tile)

**Renewal Rate** (metric tile)

**Churn Rate** (metric tile)

**Auto-Renew Success** (metric tile)

**Average Membership Tenure** (metric tile)

**Average Visits per Member** (metric tile)

**Revenue per Member** (metric tile)

**Membership Utilization** (metric tile)

**Benefit Utilization** (metric tile)

**Upgrade Rate** (metric tile)

**Freeze/Suspension Rate** (metric tile)

**Expected Renewals** (metric tile)

**Expected Churn** (metric tile)

**Renewal Revenue** (metric tile)

**Upgrade Revenue** (metric tile)

**Membership Base Growth** (metric tile)

**Data it reads**: `listMembershipRenewalRetention` (onLoad, Membership Analytics, Renewal Intelligence & AI Retention …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership analytics renewal list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership analytics renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership analytics renewal are still there. The pack's own statuses are 5 Management — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Members: 128
  New Memberships: 46
  Renewal Rate: 71%
  Churn Rate: 94%
  Auto-Renew Success: 87%
  Average Membership Tenure: 1.8 s
  Average Visits per Member: 3 h 20 min
  Revenue per Member: AED 96,750.00
  Membership Utilization: 71%
  Benefit Utilization: 94%
```

#### Permissions

- `listMembershipRenewalRetention` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-303` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-303`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 18: Works in Membership Analytics, Renewal Intelligence & AI Retention Center → Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-303?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createMemberException": {"method":"POST","path":"/memberships/{membershipId}/exceptions","contract":"orders","summary":"Record a member exception, override or service-recovery act","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MemberExceptionInput","responds":"MemberExceptionView"},
"freezeEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/freeze","contract":"catalogue","summary":"Pause a membership at the guest's request","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Entitlement"},
"listMember": {"method":"GET","path":"/member","contract":"subscription","summary":"Member Operations Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"product","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"activation","in":"query","required":false},{"name":"renewal","in":"query","required":false},{"name":"usage","in":"query","required":false},{"name":"memberType","in":"query","required":false},{"name":"expiringWithinDays","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"tier","in":"query","required":false},{"name":"acquisitionChannel","in":"query","required":false},{"name":"atRisk","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMemberExceptionOverride": {"method":"GET","path":"/member-exception-override","contract":"subscription","summary":"Member Exceptions, Overrides & Service Recovery","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"exceptionType","in":"query","required":false},{"name":"approvalStatus","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMemberLifecycleCase": {"method":"GET","path":"/member-lifecycle-case","contract":"subscription","summary":"Member Lifecycle History, Audit & Case Timeline","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipId","in":"query","required":false},{"name":"eventType","in":"query","required":false},{"name":"actorType","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipActivationCredential": {"method":"GET","path":"/membership-activation-credential","contract":"subscription","summary":"Membership Activation, Assignment & Credential Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"queueStage","in":"query","required":false},{"name":"membershipProduct","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipFreezeSuspension": {"method":"GET","path":"/membership-freeze-suspension","contract":"subscription","summary":"Membership Freeze, Suspension & Reactivation Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"interruptionType","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":"activeOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipRenewalRetention": {"method":"GET","path":"/membership-renewal-retention","contract":"subscription","summary":"Membership Analytics, Renewal Intelligence & AI Retention Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipProduct","in":"query","required":false},{"name":"tier","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"geography","in":"query","required":false},{"name":"renewalCohort","in":"query","required":false},{"name":"purchaseMonth","in":"query","required":false},{"name":"acquisitionChannel","in":"query","required":false},{"name":"churnFlag","in":"query","required":false},{"name":"maxRenewalProbability","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMembershipUpgradeDowngrade": {"method":"GET","path":"/membership-upgrade-downgrade","contract":"subscription","summary":"Membership Upgrade, Downgrade & Product Migration Operations","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"movementType","in":"query","required":false},{"name":"membershipProduct","in":"query","required":false},{"name":"bulkMigrationId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRenewalAuto": {"method":"GET","path":"/renewal-auto","contract":"subscription","summary":"Renewal Operations & Auto-Renewal Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"renewalStatus","in":"query","required":false},{"name":"membershipProduct","in":"query","required":false},{"name":"tier","in":"query","required":false},{"name":"autoRenew","in":"query","required":false},{"name":"expiringFrom","in":"query","required":false},{"name":"expiringTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVisitAdmissionEntitlement": {"method":"GET","path":"/visit-admission-entitlement","contract":"subscription","summary":"Visit, Admission & Entitlement Usage Monitor","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"membershipId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"validationResult","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"migrateMembership": {"method":"POST","path":"/memberships/{membershipId}/migrations","contract":"orders","summary":"Upgrade, downgrade or migrate an active membership to another product","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipMigrationInput","responds":"MembershipMigrationView"},
"recordBenefitUsage": {"method":"POST","path":"/memberships/{membershipId}/benefit-usage","contract":"identity","summary":"Consume a benefit","permission":"GUEST_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"membershipId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"IdentityBenefitUsage","responds":"IdentityBenefitUsage"},
"reinstateEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/reinstate","contract":"catalogue","summary":"Lift a suspension","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Entitlement"},
"renewMembership": {"method":"POST","path":"/memberships/{membershipId}/renewals","contract":"orders","summary":"Renew a membership","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"membershipId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"OrdersMembershipRenewal","responds":"OrdersMembershipRenewal"},
"resolveMembershipActivation": {"method":"POST","path":"/memberships/{membershipId}/activation/resolve","contract":"orders","summary":"Act on a membership in the activation queue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipActivationActionInput","responds":"MembershipActivationView"},
"setMemberMembershipAccount": {"method":"PUT","path":"/member-membership-account","contract":"subscription","summary":"Member 360° Membership Account Workspace","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Member360MembershipAccountWorkspaceInput","responds":"Member360MembershipAccountWorkspaceView"},
"suspendEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/suspend","contract":"catalogue","summary":"Suspend or reinstate an entitlement","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
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
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). **Null for an entitlement an invitation issued** (`invitationId`; 4 October 2026, CHG-FXC-007)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"},"invitationId":{"type":"string","format":"uuid","nullable":true,"description":"**The invitation that issued it** (4 October 2026, CHG-FXC-007): `orders.issueInvitation` issues the entitlement without an order, because an invitation never enters the order path. Exactly one of `orderId` and `invitationId` is set."}}},
"IdentityBenefitUsage": {"type":"object","x-ticvai-persistence":"identity.benefit_usage","description":"**Taken from the backend workbook, 20 September.** Tracks each use of a customer's membership benefit and the remaining allowance.","required":["customerMembershipId","membershipBenefitId","quantity","usedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"customerMembershipId":{"type":"string","format":"uuid"},"membershipBenefitId":{"type":"string","format":"uuid"},"quantity":{"type":"number"},"sourceType":{"type":"string","maxLength":30,"nullable":true},"sourceOrderId":{"type":"string","format":"uuid","nullable":true},"usedAt":{"type":"string","format":"date-time"},"remainingQuantity":{"type":"number","nullable":true,"readOnly":true,"description":"Written on the row by the server when the usage is recorded; ignored in a request."},"notes":{"type":"string","maxLength":500,"nullable":true}}},
"Member360MembershipAccountWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Member 360° Membership Account Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"membershipId":{"type":"string","description":"Membership ID the action applies to"},"action":{"type":"string","enum":["activate","freeze","suspend","resume","renew","replaceCredential","addNote","reviewEligibility","manageDependents"],"description":"Operational Action (pack pp.23-24)"},"reason":{"type":"string","description":"Reason; required for freeze, suspend and resume","nullable":true},"note":{"type":"string","description":"Case note text, for addNote","nullable":true},"effectiveDate":{"type":"string","format":"date","description":"Effective date, e.g. freeze start","nullable":true},"endDate":{"type":"string","format":"date","description":"Freeze end date","nullable":true}}},
"Member360MembershipAccountWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Member 360° Membership Account Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"memberName":{"type":"string","description":"Member Name"},"customerId":{"type":"string","description":"Customer ID"},"membershipId":{"type":"string","description":"Membership ID"},"membershipProduct":{"type":"string","description":"Membership Product"},"tier":{"type":"string","description":"Tier"},"status":{"type":"string","description":"Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"},"activationDate":{"type":"string","format":"date","description":"Activation Date","nullable":true},"expiryDate":{"type":"string","format":"date","description":"Expiry Date","nullable":true},"renewalStatus":{"type":"string","description":"Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"},"primaryVenue":{"type":"string","description":"Primary Venue"},"credentialStatus":{"type":"string","description":"Credential Status: notIssued, active, disabled or replaced"},"primaryMember":{"type":"string","description":"Primary Member"},"secondaryAdult":{"type":"string","description":"Secondary Adult name","nullable":true},"dependents":{"type":"array","items":{"type":"object","properties":{"customerId":{"type":"string"},"name":{"type":"string"},"role":{"type":"string","enum":["primaryMember","secondaryAdult","dependent","child","guardian","authorizedManager"]}}},"description":"Dependents on the membership"},"sharedBenefits":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"]},"allocation":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"used":{"type":"integer"},"remaining":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"value":{"type":"string","nullable":true,"description":"Display value of a discount benefit, from its pricing rule"}}},"description":"Shared Benefits with allocation, used and remaining"},"individualBenefits":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"]},"allocation":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"used":{"type":"integer"},"remaining":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"value":{"type":"string","nullable":true,"description":"Display value of a discount benefit, from its pricing rule"}}},"description":"Individual Benefits with allocation, used and remaining"},"membershipVersion":{"type":"integer","description":"Membership Version the contract is on"},"purchaseDate":{"type":"string","format":"date","description":"Purchase Date"},"purchaseChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Purchase Channel"},"originalOrder":{"type":"string","description":"Original Order id"},"validity":{"type":"string","enum":["fixedCalendar","durationFromPurchase","durationFromActivation","seasonBased","customPeriod"],"description":"Validity method"},"activationMethod":{"type":"string","enum":["immediateOnPurchase","fixedStartDate","firstVisit","manualActivation","customerActivation","membershipCardCollection","identityVerification","configuredTrigger"],"description":"Activation Method"},"renewalPolicy":{"type":"string","description":"Renewal Policy: the product's renewal modes, e.g. customerSelfService and autoRenewal"},"autoRenewStatus":{"type":"string","description":"Auto-Renew Status: off, optedIn, scheduled or failed; only the member's explicit opt-in sets optedIn"},"frozenDays":{"type":"integer","description":"Days lost to a freeze and added back to the expiry (follows catalogue GuestMembership.frozenDays)"},"relatedTransactions":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["order","payment","renewal","upgrade","refund","membershipChange"]},"id":{"type":"string"},"occurredAt":{"type":"string","format":"date-time"}}},"description":"Related Transactions (pack p.23)"},"aiSummary":{"type":"string","description":"AI Member Summary, advisory","nullable":true}}},
"MemberExceptionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `createMemberException` takes. The eight kinds are the pack's own labels on BO-301 (decided 29 September, readiness close-out).\n","required":["kind","reason"],"properties":{"kind":{"type":"string","description":"The exception kind (decided 29 September, readiness close-out). `complimentaryRenewal` and `complimentaryBenefit` move money and need an approved `approvalRequestId`.","enum":["eligibilityOverride","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential"]},"reason":{"type":"string","minLength":3,"maxLength":500},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The approved request in `approvals`. Required for `complimentaryRenewal` and `complimentaryBenefit`."},"extendDays":{"type":"integer","minimum":1,"maximum":366,"nullable":true,"description":"Required for `expiryExtension`."},"benefitId":{"type":"string","format":"uuid","nullable":true,"description":"The plan benefit (`catalogue.membership_benefit`). Required for `complimentaryBenefit` and `entitlementAdjustment`."},"quantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many of the benefit. Required with `benefitId`."}}},
"MemberExceptionView": {"type":"object","x-ticvai-persistence":"orders.member_exception","description":"**One exception made to a membership, and who made it.** Written by `createMemberException` (decided 29 September, readiness close-out); the audit trail a membership that behaves outside its plan is explained from.\n","required":["id","membershipId","kind","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true,"description":"The membership in the path."},"kind":{"type":"string","enum":["eligibilityOverride","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential"]},"reason":{"type":"string","maxLength":500},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"extendDays":{"type":"integer","nullable":true},"benefitId":{"type":"string","format":"uuid","nullable":true},"quantity":{"type":"integer","nullable":true},"newExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"With `expiryExtension` or `complimentaryRenewal`, the membership's expiry after the exception."},"recordedBy":{"type":"string","format":"uuid","readOnly":true,"description":"The principal who made the exception."},"recordedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MemberExceptionsOverridesServiceRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Member Exceptions, Overrides & Service Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"member":{"type":"string","description":"Member"},"membership":{"type":"string","description":"Membership"},"requestedAction":{"type":"string","description":"Requested Action"},"standardPolicyResult":{"type":"string","description":"Standard Policy Result"},"requestedException":{"type":"string","description":"Requested Exception"},"reason":{"type":"string","description":"Reason"},"supportingDocumentation":{"type":"array","items":{"type":"string"},"description":"Supporting Documentation: document ids"},"financialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Financial Impact of the exception"},"entitlementImpact":{"type":"string","description":"Entitlement Impact"},"requestor":{"type":"string","description":"Requestor"},"exceptionType":{"type":"string","enum":["eligibilityOverride","activationExtension","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential","renewalException","dependentException"],"description":"Exception Type (pack p.32)"},"exceptionValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Value used for approval routing"},"durationDays":{"type":"integer","description":"Duration in days, for extensions","nullable":true},"membershipTier":{"type":"string","description":"Membership Tier"},"exceptionId":{"type":"string","description":"Exception ID"},"approvalStatus":{"type":"string","description":"Approval status: pending, approved, rejected or applied"},"approver":{"type":"string","description":"Approver; must differ from the requestor for high-value exceptions","nullable":true},"remedy":{"type":"string","enum":["extendMembership","guestTicket","complimentaryVisit","feeWaiver","benefitCredit","renewalDiscount","alternativeEntitlement"],"description":"Service Recovery remedy (pack p.33)","nullable":true},"aiSuggestion":{"type":"string","description":"AI suggestion, advisory","nullable":true}}},
"MemberLifecycleHistoryAuditCaseTimelineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Member Lifecycle History, Audit & Case Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventId":{"type":"string","description":"Event id"},"membershipId":{"type":"string","description":"Membership ID"},"occurredAt":{"type":"string","format":"date-time","description":"When it happened"},"eventType":{"type":"string","enum":["purchase","assignment","activation","visit","benefitUsage","dependentChange","credentialChange","freeze","suspension","reactivation","upgrade","downgrade","renewal","exception","expiry","cancellation","caseNote"],"description":"Event (pack pp.33-34)"},"field":{"type":"string","description":"Changed field for configuration-sensitive changes, e.g. expiry","nullable":true},"previousValue":{"type":"string","description":"Previous Value","nullable":true},"newValue":{"type":"string","description":"New Value","nullable":true},"reason":{"type":"string","description":"Reason","nullable":true},"actorType":{"type":"string","enum":["customer","agent","manager","system","api","integration"],"description":"Actor (pack p.34)"},"actorName":{"type":"string","description":"Actor name or id","nullable":true},"relatedTransactions":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["order","payment","ticket","reservation","accessEvent","approval","case","credential"]},"id":{"type":"string"}}},"description":"Related Transactions (pack p.34)"},"note":{"type":"string","description":"Case note text, for caseNote events","nullable":true}}},
"MemberOperationsCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Member Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeMembers":{"type":"integer","description":"Active Members"},"newMembersToday":{"type":"integer","description":"New Members Today"},"activatedToday":{"type":"integer","description":"Activated Today"},"pendingActivation":{"type":"integer","description":"Pending Activation"},"expiringIn30Days":{"type":"integer","description":"Expiring in 30 Days"},"renewalDue":{"type":"integer","description":"Renewal Due: memberships inside their renewal window and not yet renewed"},"renewedThisMonth":{"type":"integer","description":"Renewed This Month"},"renewalRate":{"type":"number","description":"Renewal Rate: percentage of memberships that expired in the last 12 months and were renewed (decided 29 September, readiness close-out)"},"suspendedMemberships":{"type":"integer","description":"Suspended Memberships"},"frozenMemberships":{"type":"integer","description":"Frozen Memberships"},"membershipExceptions":{"type":"integer","description":"Membership Exceptions"},"atRiskMembers":{"type":"integer","description":"At-Risk Members: includes annual-pass holders with no visit in the last 90 days, flagged for churn follow-up (MoM 8 Sep)"},"operationalAlerts":{"type":"array","items":{"type":"string"},"description":"Operational Alerts (pack p.21), e.g. memberships expiring within seven days, purchases unactivated over 30 days, dependents needing eligibility review"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Assistance: advisory observations only; never applied automatically (pack AI sections)"}}},
"MemberOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Member Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"membershipId":{"type":"string","description":"Membership ID"},"member":{"type":"string","description":"Member name"},"membershipProduct":{"type":"string","description":"Membership Product"},"tier":{"type":"string","description":"Tier"},"venue":{"type":"string","description":"Venue"},"activationDate":{"type":"string","format":"date","description":"Activation Date","nullable":true},"expiryDate":{"type":"string","format":"date","description":"Expiry Date","nullable":true},"membershipStatus":{"type":"string","description":"Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not; empty until activated (see activationStage)","nullable":true},"usageLevel":{"type":"string","enum":["none","low","regular","high"],"description":"Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness close-out)"},"renewalStatus":{"type":"string","description":"Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"},"outstandingIssue":{"type":"string","description":"Outstanding Issue, e.g. dependent eligibility review or failed payment","nullable":true},"owner":{"type":"string","description":"Owner"},"customerId":{"type":"string","description":"Customer ID of the member (CRM profile)"},"activationStage":{"type":"string","enum":["purchased","pendingAssignment","pendingActivation","activated"],"description":"Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation)"},"atRisk":{"type":"boolean","description":"Flagged at risk, e.g. no visit in the last 90 days (MoM 8 Sep)"}}},
"MembershipActivationActionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `resolveMembershipActivation` takes (decided 29 September, readiness close-out).","required":["action"],"properties":{"action":{"type":"string","description":"The activation-queue action (decided 29 September, readiness close-out).","enum":["activate","block","review","replace","link","escalate"]},"credentialId":{"type":"string","format":"uuid","nullable":true,"description":"The credential being replaced. Required for `replace`."},"mediaCode":{"type":"string","maxLength":100,"nullable":true,"description":"The new media's code. Required for `replace`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the membership is linked to. Required for `link`."},"reason":{"type":"string","minLength":3,"maxLength":500,"nullable":true,"description":"Required for `block` and `escalate`."}}},
"MembershipActivationAssignmentCredentialManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Activation, Assignment & Credential Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"purchaseDate":{"type":"string","format":"date","description":"Purchase Date"},"eligibleActivationDate":{"type":"string","format":"date","description":"Eligible Activation Date"},"activationDeadline":{"type":"string","format":"date","description":"Activation Deadline; an unactivated membership expires here","nullable":true},"selectedStartDate":{"type":"string","format":"date","description":"Selected Start Date","nullable":true},"calculatedExpiry":{"type":"string","format":"date","description":"Calculated Expiry","nullable":true},"activationMethod":{"type":"string","enum":["immediateOnPurchase","fixedStartDate","firstVisit","manualActivation","customerActivation","membershipCardCollection","identityVerification","configuredTrigger"],"description":"Activation Method"},"failureReason":{"type":"string","enum":["eligibilityFailed","missingDocumentation","duplicateMembership","credentialFailure","configurationIssue"],"description":"Vocabulary listed under Record reason."},"membershipId":{"type":"string","description":"Membership ID"},"membershipProduct":{"type":"string","description":"Membership product name"},"purchaserCustomerId":{"type":"string","description":"Customer who bought it"},"memberCustomerId":{"type":"string","description":"Customer it is assigned to; empty until assigned","nullable":true},"queueStage":{"type":"string","enum":["awaitingMemberAssignment","awaitingIdentityVerification","awaitingDocumentVerification","awaitingActivation","activationFailed"],"description":"Activation Queue stage (pack p.24)"},"requiredChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["eligibility","age","residency","identity","photograph","requiredDocuments","dependentRelationship","termsAcceptance"]},"result":{"type":"string","enum":["pending","passed","failed","notRequired"]}}},"description":"Required Checks per Board 1 configuration (pack p.24)"},"credentialTypes":{"type":"array","items":{"type":"string","enum":["dynamicQr","barcode","rfid","nfc","digitalMembershipCard","walletPass","physicalCard"]},"description":"Credential Assignment (pack p.25)"},"duplicateOf":{"type":"string","description":"Duplicate Membership Detection: the membership ID the customer already holds","nullable":true},"duplicateAction":{"type":"string","enum":["block","review","replace","link","escalate"],"description":"Configured action on a duplicate","nullable":true}}},
"MembershipActivationView": {"type":"object","x-ticvai-persistence":"orders.membership_activation_action","description":"**One action taken on a membership in the activation queue.** Written by `resolveMembershipActivation` (decided 29 September, readiness close-out).\n","required":["id","membershipId","action","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true},"action":{"type":"string","enum":["activate","block","review","replace","link","escalate"]},"credentialId":{"type":"string","format":"uuid","nullable":true},"mediaCode":{"type":"string","maxLength":100,"nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","maxLength":500,"nullable":true},"membershipStatus":{"type":"string","maxLength":30,"readOnly":true,"description":"The membership's status after the action."},"recordedBy":{"type":"string","format":"uuid","readOnly":true},"recordedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Membership Analytics, Renewal Intelligence & AI Retention Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeMembers":{"type":"integer","description":"Active Members"},"newMemberships":{"type":"integer","description":"New Memberships"},"renewalRate":{"type":"number","description":"Renewal Rate"},"churnRate":{"type":"number","description":"Churn Rate"},"autoRenewSuccess":{"type":"number","description":"Auto-Renew Success: percentage of auto-renew attempts that succeeded"},"averageMembershipTenure":{"type":"number","description":"Average Membership Tenure in months"},"averageVisitsPerMember":{"type":"number","description":"Average Visits per Member"},"revenuePerMember":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Member"},"membershipUtilization":{"type":"number","description":"Membership Utilization"},"benefitUtilization":{"type":"number","description":"Benefit Utilization"},"freezeSuspensionRate":{"type":"number","description":"Freeze/Suspension Rate"},"expectedRenewals":{"type":"integer","description":"Expected Renewals in the forecast period"},"expectedChurn":{"type":"integer","description":"Expected Churn in the forecast period"},"renewalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Renewal Revenue"},"membershipBaseGrowth":{"type":"number","description":"Membership Base Growth, percent"},"upgradeRate":{"type":"number","description":"Upgrade Rate, percent (pack p.35)"},"upgradeRevenue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Upgrade Revenue forecast (pack p.37)"},"renewalFunnel":{"type":"object","description":"Renewal Funnel (pack p.36)","properties":{"eligibleForRenewal":{"type":"integer"},"contacted":{"type":"integer"},"renewalStarted":{"type":"integer"},"paymentAttempted":{"type":"integer"},"renewed":{"type":"integer"},"failed":{"type":"integer"},"expired":{"type":"integer"}}}}},
"MembershipAnalyticsRenewalIntelligenceAiRetentionCenView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Analytics, Renewal Intelligence & AI Retention Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"visits":{"type":"integer","description":"Visits in the current term"},"benefitUsage":{"type":"number","description":"Benefit usage, percent of allocation used"},"guestTicketUsage":{"type":"integer","description":"Guest tickets used this term"},"complaintsExceptions":{"type":"integer","description":"Complaints/Exceptions this term"},"confidence":{"type":"number","description":"Confidence of the prediction, 0-1"},"keyDrivers":{"type":"array","items":{"type":"string"},"description":"Key Drivers, e.g. visits down 58%, no visits in 90 days"},"modelVersion":{"type":"string","description":"Model Version"},"dataFreshness":{"type":"string","format":"date-time","description":"Data Freshness: when the inputs were last refreshed"},"membershipId":{"type":"string","description":"Membership ID"},"memberName":{"type":"string","description":"Member name"},"membershipProduct":{"type":"string","description":"Membership product"},"tier":{"type":"string","description":"Tier","nullable":true},"expiryDate":{"type":"string","format":"date","description":"Expiry date"},"lastVisitDate":{"type":"string","format":"date","description":"Last visit","nullable":true},"renewalProbability":{"type":"number","description":"Member Renewal Probability, 0-1 (advisory)"},"churnFlag":{"type":"boolean","description":"No visit in the last 90 days: flagged for churn follow-up (MoM 8 Sep)"},"recommendedActions":{"type":"array","items":{"type":"string","enum":["renewalReminder","benefitReminder","membershipEducation","upgradeOffer","retentionOffer","serviceFollowUp"]},"description":"Recommended Actions (pack p.36), advisory"}}},
"MembershipFreezeSuspensionReactivationManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Freeze, Suspension & Reactivation Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"startDate":{"type":"string","format":"date","description":"Start Date"},"endDate":{"type":"string","format":"date","description":"End Date; empty for open-ended suspension","nullable":true},"durationDays":{"type":"integer","description":"Duration in days","nullable":true},"reason":{"type":"string","description":"Reason in the requester's words"},"requestedBy":{"type":"string","description":"Requested By (member, agent or system)"},"approvedBy":{"type":"string","description":"Approved By","nullable":true},"membershipId":{"type":"string","description":"Membership ID"},"memberName":{"type":"string","description":"Member name"},"interruptionType":{"type":"string","enum":["freeze","suspension","administrativeHold"],"description":"Freeze (member's permitted pause), Suspension (administrative restriction) or Administrative Hold (pack p.27)"},"suspensionReason":{"type":"string","enum":["paymentIssue","membershipMisuse","credentialMisuse","eligibilityIssue","chargeback","administrativeReview","other"],"description":"Suspension Reason (pack p.28)","nullable":true},"validityTreatment":{"type":"string","enum":["extendExpiry","doNotExtend"],"description":"Validity Treatment (pack p.28). Default extendExpiry for a freeze and doNotExtend for a suspension, as the membership state model sets"},"newExpiryDate":{"type":"string","format":"date","description":"Expiry after the extension, when validityTreatment is extendExpiry","nullable":true},"entitlementTreatment":{"type":"object","description":"Entitlement Treatment during the interruption (pack p.28). Defaults: admission, reservations, benefits and credential blocked; renewal allowed during a freeze and blocked during a suspension (decided 29 September, readiness close-out)","properties":{"admissionBlocked":{"type":"boolean"},"reservationsRestricted":{"type":"boolean"},"benefitsRestricted":{"type":"boolean"},"renewalAllowed":{"type":"boolean"},"credentialDisabled":{"type":"boolean"}}},"interruptionStatus":{"type":"string","description":"Interruption status: scheduled, active, ended or cancelled"}}},
"MembershipMigrationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `migrateMembership` takes (decided 29 September, readiness close-out).","required":["targetProductId","direction","effectiveTiming"],"properties":{"targetProductId":{"type":"string","format":"uuid","description":"The membership product it moves to."},"direction":{"type":"string","description":"Which way it moves (decided 29 September, readiness close-out).","enum":["upgrade","downgrade","migration"]},"effectiveTiming":{"type":"string","description":"When the move takes effect (decided 29 September, readiness close-out).","enum":["immediate","nextVisit","nextRenewal","endOfCurrentTerm"]},"proRata":{"type":"boolean","default":false,"description":"Charge or credit the difference for the remaining term."}}},
"MembershipMigrationView": {"type":"object","x-ticvai-persistence":"orders.membership_migration","description":"**One move of a membership to another product.** Written by `migrateMembership` (decided 29 September, readiness close-out).\n","required":["id","membershipId","fromProductId","targetProductId","direction","effectiveTiming","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true},"fromProductId":{"type":"string","format":"uuid","readOnly":true},"targetProductId":{"type":"string","format":"uuid"},"direction":{"type":"string","enum":["upgrade","downgrade","migration"]},"effectiveTiming":{"type":"string","enum":["immediate","nextVisit","nextRenewal","endOfCurrentTerm"]},"proRata":{"type":"boolean"},"proRataAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"description":"With `proRata`, the difference charged (positive) or credited (negative)."},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order the pro-rata difference went through."},"effectiveAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When it took, or will take, effect. Null for `nextVisit` until the visit."},"status":{"type":"string","readOnly":true,"enum":["scheduled","applied"]},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"MembershipUpgradeDowngradeProductMigrationOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Membership Upgrade, Downgrade & Product Migration Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"currentMembership":{"type":"string","description":"Current Membership product and tier"},"targetMembership":{"type":"string","description":"Target Membership product and tier"},"customerQualification":{"type":"string","enum":["eligible","notEligible","reviewRequired"],"description":"Customer Qualification for the target"},"usage":{"type":"integer","description":"Usage: visits in the current term"},"remainingValidity":{"type":"integer","description":"Remaining Validity in days"},"entitlementComparison":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"]},"current":{"type":"string"},"target":{"type":"string"}}},"description":"Entitlement Comparison (pack pp.29-30)"},"outstandingBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Outstanding Balance on the member's account"},"effectiveDate":{"type":"string","format":"date","description":"Effective date, for effectiveTiming fixedDate or once resolved","nullable":true},"membershipId":{"type":"string","description":"Membership ID"},"memberName":{"type":"string","description":"Member name"},"movementType":{"type":"string","enum":["upgrade","downgrade","migration"],"description":"Upgrade, downgrade or product migration"},"effectiveTiming":{"type":"string","enum":["immediately","nextVisit","nextRenewal","fixedDate","endOfCurrentTerm"],"description":"Effective Date option (pack p.29)"},"proRataCredit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Pro-rata credit for the unused part of the current term, calculated by pricing (MoM 1 Sep §4.9)"},"priceDifference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Balance to charge after the credit, calculated by pricing (Area 10)"},"consumedBenefitTreatment":{"type":"string","enum":["reset","carryForward","adjust"],"description":"Consumed Benefits (pack p.30): per the target product's rules"},"orderId":{"type":"string","description":"Resulting order (Area 12)","nullable":true},"bulkMigrationId":{"type":"string","description":"Bulk Migration batch, when part of one (pack p.30)","nullable":true},"requestStatus":{"type":"string","description":"Request status: quoted, pendingPayment, scheduled, completed or cancelled"}}},
"OrdersMembershipRenewal": {"type":"object","x-ticvai-persistence":"orders.membership_renewal","description":"**Taken from the backend workbook, 20 September.** Stores membership renewal transactions and the result of each renewal attempt.","required":["customerMembershipId","entitlementTemplateId","type","status","attemptedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"customerMembershipId":{"type":"string","format":"uuid","description":"The membership in the path. Taken from the path on `renewMembership`."},"entitlementTemplateId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order the renewal charged through. Set by the server."},"type":{"type":"string","maxLength":30},"status":{"type":"string","maxLength":30,"readOnly":true},"previousExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"newExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Computed from the entitlement template's term and grace period."},"attemptedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"failureReason":{"type":"string","maxLength":500,"nullable":true,"readOnly":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RenewalOperationsAutoRenewalManagementSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Renewal Operations & Auto-Renewal Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"renewalNotOpen":{"type":"integer","description":"Renewal Not Open"},"renewalEligible":{"type":"integer","description":"Renewal Eligible"},"renewalInvitationSent":{"type":"integer","description":"Renewal Invitation Sent"},"renewalStarted":{"type":"integer","description":"Renewal Started"},"paymentPending":{"type":"integer","description":"Payment Pending"},"renewed":{"type":"integer","description":"Renewed"},"autoRenewScheduled":{"type":"integer","description":"Auto-Renew Scheduled"},"autoRenewFailed":{"type":"integer","description":"Auto-Renew Failed"},"gracePeriod":{"type":"integer","description":"Grace Period"},"expiredWithoutRenewal":{"type":"integer","description":"Expired Without Renewal"}}},
"RenewalOperationsAutoRenewalManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Renewal Operations & Auto-Renewal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"member":{"type":"string","description":"Member"},"membership":{"type":"string","description":"Membership"},"tier":{"type":"string","description":"Tier"},"expiry":{"type":"string","format":"date","description":"Expiry"},"renewalWindow":{"type":"object","description":"Renewal Window","properties":{"opens":{"type":"string","format":"date"},"closes":{"type":"string","format":"date"}}},"renewalPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Renewal Price from pricing (Area 10)"},"autoRenew":{"type":"boolean","description":"Auto-Renew: the member has explicitly opted in"},"paymentMethodStatus":{"type":"string","description":"Payment Method Status: none, valid, expiringSoon, expired or failed"},"eligibility":{"type":"string","enum":["eligible","notEligible","reviewRequired"],"description":"Eligibility for renewal"},"renewalStatus":{"type":"string","description":"Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"},"membershipStatus":{"type":"string","description":"Current membership status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"},"outstandingIssues":{"type":"string","description":"Outstanding Issues","nullable":true},"autoRenewConsentAt":{"type":"string","format":"date-time","description":"Consent: when the member accepted the auto-renewal terms; empty means no consent and auto-renew will not run","nullable":true},"membershipVersion":{"type":"integer","description":"Membership Version the renewal will be on"},"membershipId":{"type":"string","description":"Membership ID"},"preNotificationSentAt":{"type":"string","format":"date-time","description":"Pre-renewal reminder sent","nullable":true},"paymentAttempts":{"type":"integer","description":"Auto-renew payment attempts so far"},"nextAttemptAt":{"type":"string","format":"date-time","description":"Next scheduled payment attempt","nullable":true}}},
"VisitAdmissionEntitlementUsageMonitorSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Visit, Admission & Entitlement Usage Monitor.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalVisits":{"type":"integer","description":"Total Visits"},"visitsThisMonth":{"type":"integer","description":"Visits This Month"},"lastVisit":{"type":"string","format":"date-time","description":"Last Visit","nullable":true},"upcomingReservation":{"type":"string","format":"date-time","description":"Upcoming Reservation start","nullable":true},"guestTicketsUsed":{"type":"integer","description":"Guest Tickets Used"},"guestTicketsRemaining":{"type":"integer","description":"Guest Tickets Remaining","nullable":true},"parkingUses":{"type":"integer","description":"Parking Uses"},"benefitUsage":{"type":"array","items":{"type":"object","properties":{"entitlementType":{"type":"string","enum":["unlimitedAdmission","limitedAdmissions","attractionAccess","eventAccess","zoneAccess","fastTrack","priorityEntry","guestTickets","parking","fnbBenefit","retailBenefit","rentalBenefit","specialEventAccess","bookingPrivileges","other"]},"allocation":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"used":{"type":"integer"},"remaining":{"type":"integer","nullable":true,"description":"Empty for unlimited"},"value":{"type":"string","nullable":true,"description":"Display value of a discount benefit, from its pricing rule"}}},"description":"Entitlement Consumption (pack p.26): allocation, used and remaining per benefit"},"noShows":{"type":"integer","description":"No-Shows"},"usageExceptions":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["usageAboveLimit","invalidReEntry","benefitExhausted","blackoutAttempt","expiredMembershipUsage","suspendedMembershipAttempt"]},"count":{"type":"integer"}}},"description":"Usage Exceptions (pack pp.26-27) counted over the filtered visits"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Assistance: advisory observations only; never applied automatically (pack AI sections)"}}},
"VisitAdmissionEntitlementUsageMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Visit, Admission & Entitlement Usage Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"date":{"type":"string","format":"date","description":"Date of the visit"},"venue":{"type":"string","description":"Venue"},"attraction":{"type":"string","description":"Attraction","nullable":true},"gate":{"type":"string","description":"Gate","nullable":true},"entryTime":{"type":"string","format":"date-time","description":"Entry Time"},"exitTime":{"type":"string","format":"date-time","description":"Exit time where the venue records exits","nullable":true},"credential":{"type":"string","description":"Credential presented (credential id)"},"reservation":{"type":"string","description":"Reservation id, where the visit was booked","nullable":true},"validationResult":{"type":"string","enum":["admitted","usageAboveLimit","invalidReEntry","benefitExhausted","blackoutAttempt","expiredMembershipUsage","suspendedMembershipAttempt"],"description":"Validation Result from Access Control"},"membershipId":{"type":"string","description":"Membership ID"},"visitId":{"type":"string","description":"Visit (access event) id"}}}
}
```
