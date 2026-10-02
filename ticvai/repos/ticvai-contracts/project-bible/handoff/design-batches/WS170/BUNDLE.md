# WS170 — Seat Management Venue Mapping Reference v1.0 board 6

**10 screens · 6 operations · 8 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `APPROVAL_REQUEST, CAPACITY_CONFIGURE`. A control nobody can use must say so,
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
| `BO-1003` | Hold Command Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1004` | Hold Type Master | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1005` | Hold Pool Creation | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1006` | Hold Rule Assignment | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1007` | Expiration Rules | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1008` | Automatic Hold Release | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1009` | Release, Convert & Reassign | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1010` | Hold Approval Workflow | B–D | 0 | 0 | 6 | 5 | 0 | 3 | — | notStarted (—) |
| `BO-1011` | Priority & Conflict Resolution | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1012` | Hold Utilization & Audit | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1003, BO-1004, BO-1005, BO-1006, BO-1007, BO-1010, BO-1011, BO-1012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1003` Hold Command Center

**Provide a complete operational view of held inventory and its risk. Show held seats, hold value, utilization, conversion, upcoming expiry, overdue decisions and inventory at risk. Analyze by tenant, venue, event, performance, hold type, owner, stakeholder, priority and age. Surface high-value unused holds, late release, conflicts and low conversion with direct action links. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/hold-command-center-bo-1003` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Held seat inventory and its risk: held seats and value, utilisation, conversion, upcoming expiry; a sponsor pool never drawn down is seats that were not sold.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSeatHoldPools return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#listSeatHoldPools; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **hold pools**: Pool, type, owner, held, used, remaining, release date; low utilisation highlighted. *(source: contracts/satellite/seating.yaml#listSeatHoldPools)*

**Data it reads**: `listSeatHoldPools` (onLoad, Pools and their utilisation)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1004` Hold Type Master: *Hold Type Master*
- → `BO-1005` Hold Pool Creation: *Hold Pool Creation*
- → `BO-1006` Hold Rule Assignment: *Hold Rule Assignment*
- → `BO-1007` Expiration Rules: *Expiration Rules*
- → `BO-1008` Automatic Hold Release: *Automatic Hold Release*
- → `BO-1009` Release, Convert & Reassign: *Release, Convert & Reassign*
- → `BO-1010` Hold Approval Workflow: *Hold Approval Workflow*
- → `BO-1011` Priority & Conflict Resolution: *Priority & Conflict Resolution*
- → `BO-1012` Hold Utilization & Audit: *Hold Utilization & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pool:
  type: Sponsor
  owner: Emirates Bank
  held: 40
  used: 12
  releases: 72 h before
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1003` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1003`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 1: Opens Hold Command Center → Provide a complete operational view of held inventory and its risk. Show held seats, hold value, utilization, conversion, upcoming expiry, overdue decisions and inventory at risk. Analyze by tenant …
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F279 branch at step 1 (expected): when Nothing has been set up on Hold Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F279 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1004`, `BO-1005`, `BO-1006`, `BO-1007`, `BO-1008`, `BO-1009`, `BO-1010`, `BO-1011`, `BO-1012`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1004` Hold Type Master

**Configure reusable hold categories and their default behavior. Maintain VIP, Sponsor, Artist, Media, Corporate, Internal and custom types with code, color and description. Set default duration, priority, approval, reminder, maximum quantity, permitted channels and auto-release policy. Map type to stakeholder classes, contract requirements, reporting dimensions and permitted roles. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/hold-type-master-bo-1004` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The kinds of hold a venue places (VIP, sponsor, artist, media, corporate, internal) with owner, colour, default duration and who may release them.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSeatHoldTypes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#listSeatHoldTypes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **release rule**: Who may release (role) and when (date or time before performance). *(source: contracts/satellite/seating.yaml#setSeatHoldType)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat hold type (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldTypes` (onLoad, Hold kinds)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold type master list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold type master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold type master yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold type master are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
type:
  code: MEDIA
  name: Media
  colour: '#00B8FF'
  releaseBy: Ticketing manager
  defaultRelease: 48 h before
```

#### Permissions

- `listSeatHoldTypes` → `CAPACITY_CONFIGURE` (configure) · staff
- `setSeatHoldType` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1004` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1004`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 2: Works in Hold Type Master → Configure reusable hold categories and their default behavior. Maintain VIP, Sponsor, Artist, Media, Corporate, Internal and custom types with code, color and description. Set default duration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat hold type, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1005` Hold Pool Creation

**Select and create an explicit pool of held seats or capacity. Choose inventory by map, section, row, seat list, zone quantity or uploaded allocation with current-state validation. Capture event/performance, type, owner, stakeholder, value, purpose, effective time, expiry and notes. Preview available, already held, reserved, sold, blocked and inaccessible inventory before submission. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 26**

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
| Route | `/access-venue/hold-pool-creation-bo-1005` |

**Known gaps.** **Hold Pool Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Create a pool of held seats from the map, a section, rows, a seat list, a zone quantity or an uploaded allocation, validated against the current seat state.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createSeatHoldPool and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **seats**: Seats or a count; seats already sold or held are refused, named. *(source: contracts/satellite/seating.yaml#createSeatHoldPool)*

#### Outputs: what the screen shows and produces

**Shown**

**Held seats, by pool, with what is left and when it releases** (data table, from `listSeatHoldPools`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create seat hold pool (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldPools` (onLoad, Held seats, by pool, with what is left and when it releases)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold pool creation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold pool creation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold pool creation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold pool creation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pool:
  type: Artist
  performance: Desert Symphony 22 Nov
  seats: 30
```

#### Permissions

- `createSeatHoldPool` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: reservations/holds are made section-wise (choose section → choose/hold seats within it), not by a freeform polygon selection as in the AI-generated reference mockup. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-415)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1005` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1005`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 4: Works in Hold Pool Creation → Select and create an explicit pool of held seats or capacity. Choose inventory by map, section, row, seat list, zone quantity or uploaded allocation with current-state validation. Capture …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat hold pool, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1006` Hold Rule Assignment

**Automatically apply approved hold policies to eligible performances. Build conditions by tenant, venue, event, product, date, performance, section, category, stakeholder and channel. Define seat set or quantity, type, owner, priority, duration, release rule and exception behavior. Simulate upcoming performances, detect rule collisions and version every activated rule. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/hold-rule-assignment-bo-1006` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Apply hold policies automatically to eligible performances by condition.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatHoldType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **conditions**: Event, section, category, channel conditions on the hold type. *(source: contracts/satellite/seating.yaml#setSeatHoldType)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of hold a venue places, and who may release them** (data table, from `listSeatHoldTypes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Purpose | chip: Production, House, Accessibility, Press, Sponsor, Contractual… | — |
| Owner role | text | — |
| Release rule | chip: Manual, Hours before performance, On date, On sellout threshold | — |
| Release hours before | 1,234 | — |
| Release to | chip: General sale, Another pool, Remains held | — |
| Counts against capacity | yes / no (icon or chip) | Whether held seats are still "sold out". A production hold that reads as availability puts a show on sale it cannot honour. |
| Visible to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat hold type (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldTypes` (onLoad, The kinds of hold a venue places, and who may release them)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: 'Every Desert Symphony performance: 20 house seats in Lower 101 rows A-B'
```

#### Permissions

- `setSeatHoldType` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldTypes` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1006` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1006`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 6: Works in Hold Rule Assignment → Automatically apply approved hold policies to eligible performances. Build conditions by tenant, venue, event, product, date, performance, section, category, stakeholder and channel. Define seat set …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat hold type, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1007` Expiration Rules

**Control when held inventory must be reviewed or released. Set fixed timestamp, time-before-performance, contract milestone, payment condition or manual approval expiry. Configure reminder sequence, grace period, escalation, extension eligibility and maximum extension. Respect venue timezone and daylight-saving behavior and preserve the rule/version applied to each hold. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/expiration-rules-bo-1007` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When held inventory must be reviewed or released: fixed time, time before performance, contract milestone, payment condition, manual approval; reminders and grace.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSeatHoldType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **expiry**: One expiry kind per hold type with reminders. *(source: contracts/satellite/seating.yaml#setSeatHoldType)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of hold a venue places, and who may release them** (data table, from `listSeatHoldTypes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Purpose | chip: Production, House, Accessibility, Press, Sponsor, Contractual… | — |
| Owner role | text | — |
| Release rule | chip: Manual, Hours before performance, On date, On sellout threshold | — |
| Release hours before | 1,234 | — |
| Release to | chip: General sale, Another pool, Remains held | — |
| Counts against capacity | yes / no (icon or chip) | Whether held seats are still "sold out". A production hold that reads as availability puts a show on sale it cannot honour. |
| Visible to guest | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat hold type (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldTypes` (onLoad, The kinds of hold a venue places, and who may release them)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiration rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiration rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiration rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the expiration rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
expiry:
  type: Corporate
  rule: 7 days before, reminders at 14 and 10 days
```

#### Permissions

- `setSeatHoldType` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldTypes` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1007` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1007`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 8: Works in Expiration Rules → Control when held inventory must be reviewed or released. Set fixed timestamp, time-before-performance, contract milestone, payment condition or manual approval expiry. Configure reminder sequence …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat hold type, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1008` Automatic Hold Release

**Release eligible held inventory reliably and in controlled batches. Schedule releases by type, rule, event, performance, stakeholder, age and remaining time. Preview seats, price bands, channel availability, sold-out status and exceptions before execution. Use idempotent processing, partial-failure handling, retry, reconciliation and stakeholder notification. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `poolId` (navigation) |
| Route | `/access-venue/automatic-hold-release-bo-1008` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Release eligible held seats back to sale in controlled batches, with a preview of what returns.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only releaseSeatHoldPool and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Held seats, by pool, with what is left and when it releases** (data table, from `listSeatHoldPools`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Release seat hold pool (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Release batch**: Preview seats and price bands first; release puts them on sale. *(source: contracts/satellite/seating.yaml#releaseSeatHoldPool)*

**Data it reads**: `listSeatHoldPools` (onLoad, Held seats, by pool, with what is left and when it releases)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automatic hold release list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automatic hold release untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automatic hold release yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the automatic hold release are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
batch:
  pools: 3
  seats: 64
  at: 2026-11-19 10:00
```

#### Permissions

- `releaseSeatHoldPool` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1008` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1008`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 10: Works in Automatic Hold Release → Release eligible held inventory reliably and in controlled batches. Schedule releases by type, rule, event, performance, stakeholder, age and remaining time. Preview seats, price bands, channel …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Release seat hold pool, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1009` Release, Convert & Reassign

**Allow authorized users to change the outcome of an active hold. Release all or selected inventory, convert it to reservation/order, reassign owner/stakeholder or extend expiry. Revalidate state, price, eligibility, payment or contract condition before committing the action. Require reason, supporting notes and approval when value, timing or policy threshold is exceeded. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `poolId` (navigation) |
| Route | `/access-venue/release-convert-reassign-bo-1009` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Change the outcome of an active hold: release, convert to a reservation or order, reassign owner, extend.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only releaseSeatHoldPool and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Held seats, by pool, with what is left and when it releases** (data table, from `listSeatHoldPools`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Release seat hold pool (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Convert**: Revalidates state and price; creates the order for the hold owner. *(source: contracts/satellite/seating.yaml#releaseSeatHoldPool)*

**Data it reads**: `listSeatHoldPools` (onLoad, Held seats, by pool, with what is left and when it releases)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The release convert reassign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the release convert reassign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No release convert reassign yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the release convert reassign are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action:
  pool: Sponsor Emirates Bank
  convert: 18
  to: complimentary order
```

#### Permissions

- `releaseSeatHoldPool` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1009` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1009`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 12: Works in Release, Convert & Reassign → Allow authorized users to change the outcome of an active hold. Release all or selected inventory, convert it to reservation/order, reassign owner/stakeholder or extend expiry. Revalidate state …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Release seat hold pool, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1010` Hold Approval Workflow

**Route hold requests and sensitive changes to the correct approvers. Configure requester, venue operations, ticketing, commercial, finance and executive stages by policy. Configuration Scope of Work / Version 1.0 27 Display request details, seats, value, expiry, conflicts, supporting contract and previous decisions. Support approve, reject, request information, delegate and escalate with comments and SLA. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `CAPACITY_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/hold-approval-workflow-bo-1010` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Route seat hold requests to the right approvers with seats, value and expiry shown.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create approval request (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldPools` (onLoad, What is being requested)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold approval workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds CAPACITY_CONFIGURE only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_REQUEST for createApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#createApprovalRequest)*
- **createApprovalRequest answers 409**: Show it as something the person can act on, not a failure: An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. `refusedReason` is `openRequestExists` and `requestId` names the open request, so the caller can point at it rather than raise another. A draft is not an open request. *(source: contracts/spine/approvals.yaml#createApprovalRequest)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listSeatHoldPools (SeatHoldPool):
- seatCount: 12
  usedCount: 12
  releasedCount: 12
  reason: Guest charged twice at Main Gate Till 3
  releaseAt: 01/10/2026 09:14
  status: active
- seatCount: 3
  usedCount: 3
  releasedCount: 3
  reason: Group of 40 from Desert Gate Tours
  releaseAt: 30/09/2026 18:02
  status: pending
```

#### Permissions

- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1010` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1010`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 14: Works in Hold Approval Workflow → Route hold requests and sensitive changes to the correct approvers. Configure requester, venue operations, ticketing, commercial, finance and executive stages by policy. Configuration Scope of Work / …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create approval request, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1011` Priority & Conflict Resolution

**Resolve overlapping or competing hold requests predictably. Maintain priority matrix by hold type, event, stakeholder, contract, quantity, value and time before performance. List exact conflicting seats and compare current and proposed owner, purpose, priority and expiry. Allow automatic winner, supervisor decision, alternative seat suggestion or split allocation with recorded reason. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/priority-conflict-resolution-bo-1011` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Resolve overlapping hold requests by a priority matrix of hold type, stakeholder, contract and time before performance.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSeatHoldPools return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#listSeatHoldPools; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seat hold type (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **conflicts**: Exact conflicting seats with both claims and the winner by priority. *(source: contracts/satellite/seating.yaml#listSeatHoldPools)*

**Data it reads**: `listSeatHoldPools` (onLoad, Competing holds)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The priority conflict resolution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the priority conflict resolution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No priority conflict resolution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the priority conflict resolution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
conflict:
  seats: Lower 101 A-1..6
  claims:
  - Artist
  - Sponsor
  winner: Artist
```

#### Permissions

- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff
- `setSeatHoldType` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1011` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1011`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 16: Works in Priority & Conflict Resolution → Resolve overlapping or competing hold requests predictably. Maintain priority matrix by hold type, event, stakeholder, contract, quantity, value and time before performance. List exact conflicting …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1011?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seat hold type, Cancel.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1012` Hold Utilization & Audit

**Measure whether held inventory creates value or suppresses sale unnecessarily. Report held-to-sold conversion, released and sold, expired unused, average age, value and revenue opportunity. Compare hold type, owner, stakeholder, event, section and release timing over time. Provide immutable creation, approval, extension, conversion, release, conflict and override history with secured export. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 28 Board 7 - Seating Rules, Buffers & Accessibility Figure 7. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 29**

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
| Route | `/access-venue/hold-utilization-audit-bo-1012` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether held inventory creates value: held-to-sold conversion, expired unused, age, revenue opportunity.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSeatHoldPools return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/seating.yaml#listSeatHoldPools; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **utilisation**: By hold type with conversion rate. *(source: contracts/satellite/seating.yaml#listSeatHoldPools)*

**Data it reads**: `listSeatHoldPools` (onLoad, Utilisation and audit)

**Where the user goes next**

- → `BO-1003` Hold Command Center: *Back to Hold Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hold utilization audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hold utilization audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hold utilization audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hold utilization audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
utilisation:
  type: Media
  conversion: 41%
  expiredUnused: 26
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1012` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1012`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 6
- Flow F279 *Seat Management Venue Mapping Reference v1.0 board 6: Hold Command Center*, step 18: Works in Hold Utilization & Audit → Measure whether held inventory creates value or suppresses sale unnecessarily. Report held-to-sold conversion, released and sold, expired unused, average age, value and revenue opportunity. Compare …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createSeatHoldPool": {"method":"POST","path":"/seat-hold-pools","contract":"seating","summary":"Take a set of seats out of sale, for a reason, until a date","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatHoldPool","responds":"SeatHoldPool"},
"listSeatHoldPools": {"method":"GET","path":"/seat-hold-pools","contract":"seating","summary":"Held seats, by pool, with what is left and when it releases","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null}],"requestBody":null,"responds":"SeatHoldPool"},
"listSeatHoldTypes": {"method":"GET","path":"/seat-hold-types","contract":"seating","summary":"The kinds of hold a venue places, and who may release them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatHoldType"},
"releaseSeatHoldPool": {"method":"POST","path":"/seat-hold-pools/{poolId}/release","contract":"seating","summary":"Put held seats back on sale, convert them, or reassign them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatHoldPool"},
"setSeatHoldType": {"method":"PUT","path":"/seat-hold-types","contract":"seating","summary":"Define a hold kind, its owner and its release rule","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatHoldType","responds":"SeatHoldType"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"SeatHoldPool": {"type":"object","x-ticvai-persistence":"seating.hold_pool","description":"Board 6.3. **Utilisation decides next season's allocation.**","required":["holdTypeId","performanceId"],"properties":{"id":{"type":"string","format":"uuid"},"holdTypeId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"seatCount":{"type":"integer","readOnly":true},"usedCount":{"type":"integer","readOnly":true},"releasedCount":{"type":"integer","readOnly":true},"holderName":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"releaseAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","partiallyReleased","released","expired"]},"createdBy":{"type":"string","format":"uuid"},"scopePath":{"type":"string"}}},
"SeatHoldType": {"type":"object","x-ticvai-persistence":"seating.hold_type","description":"Board 6.2. **A hold with no release rule becomes a permanent hole in the map.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"purpose":{"type":"string","enum":["production","house","accessibility","press","sponsor","contractual","maintenance","distancing"]},"ownerRole":{"type":"string","nullable":true},"releaseRule":{"type":"string","enum":["manual","hoursBeforePerformance","onDate","onSelloutThreshold"],"default":"hoursBeforePerformance"},"releaseHoursBefore":{"type":"integer","nullable":true},"releaseTo":{"type":"string","enum":["generalSale","anotherPool","remainsHeld"],"default":"generalSale"},"countsAgainstCapacity":{"type":"boolean","default":true,"description":"**Whether held seats are still \"sold out\".** A production hold that reads as availability puts a show on sale it cannot honour.\n"},"visibleToGuest":{"type":"boolean","default":false},"scopePath":{"type":"string"}}}
}
```
