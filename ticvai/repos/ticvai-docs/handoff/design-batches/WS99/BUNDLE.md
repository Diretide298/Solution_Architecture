# WS99 — Subscription Licensing AI Self Service board 2

**10 screens · 5 operations · 10 schemas · 2 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `PLATFORM_PLAN_MANAGE, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-379` | Welcome & Start Your TICVAI Journey | B | 4 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `ADM-380` | Customer & Organization Registration | B | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-381` | Venue Type & Business Profile | B | 1 | 12 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-382` | Visitor, Capacity & Operational Scale | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-383` | Sales Channel Assessment | B | 11 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-384` | Ticketing & Product Requirements | B | 15 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-385` | Access, Queue & Visitor Experience Assessment | B | 0 | 0 | 6 | 2 | 1 | 6 | — | notStarted (—) |
| `ADM-386` | Additional Business Module Assessment | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-387` | Integration, Payment & Technical Readiness | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-388` | AI Assessment Summary & Handoff | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-381, ADM-382, ADM-385, ADM-386, ADM-387, ADM-388 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-379` Welcome & Start Your TICVAI Journey

**Provide the entry point for a new customer starting self-service onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-379 |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Starting Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/welcome-start-your-ticvai-journey-adm-379` |

**What the spec says about it.** **Kept as TICVAI's operator-led view of the prospect journey (2 October 2026, CHG-SBO-015; BL-165):** ADM-379 to ADM-388 and SGN-001 to SGN-010 are one journey with two doors. A TICVAI sales operator runs it with or for a prospect on the Console; a prospect runs it alone on the sign-up (P17). The copies stay identical (`source.sameAs`), so the operator sees exactly what the prospect sees.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): The welcome page scores nothing (scoreVsiAssessment is called on the assessment screens SGN-003 to SGN-010); the operator-led copy ADM-379 loses it too, so the …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-001 on the Console.

**Fixed on main** (the package already carries these; draw what it says): ADM-379 to ADM-388 repeat SGN-001 to SGN-010 (same names, same operations). (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start New Setup | select field | — | — | — | — | — | — |
| Continue Saved Setup | select field | — | — | — | — | — | — |
| Sign In | select field | — | — | — | — | — | — |
| Request Enterprise Consultation | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-380` Customer & Organization Registration: *Customer & Organization Registration*
- → `ADM-381` Venue Type & Business Profile: *Venue Type & Business Profile*
- → `ADM-382` Visitor, Capacity & Operational Scale: *Visitor, Capacity & Operational Scale*
- → `ADM-383` Sales Channel Assessment: *Sales Channel Assessment*
- → `ADM-384` Ticketing & Product Requirements: *Ticketing & Product Requirements*
- → `ADM-385` Access, Queue & Visitor Experience Assessment: *Access, Queue & Visitor Experience Assessment*
- → `ADM-386` Additional Business Module Assessment: *Additional Business Module Assessment*
- → `ADM-387` Integration, Payment & Technical Readiness: *Integration, Payment & Technical Readiness*
- → `ADM-388` AI Assessment Summary & Handoff: *AI Assessment Summary & Handoff*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The welcome start your configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the welcome start your untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No welcome start your configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Start New Setup: 11
  Continue Saved Setup: 233
  Sign In: 46
  Request Enterprise Consultation: 312
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-379` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-379`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 1: Opens Welcome & Start Your TICVAI Journey → Provide the entry point for a new customer starting self-service onboarding.
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F208 branch at step 1 (expected): when Nothing has been set up on Welcome & Start Your TICVAI Journey yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F208 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-379?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-380`, `ADM-381`, `ADM-382`, `ADM-383`, `ADM-384`, `ADM-385`, `ADM-386`, `ADM-387`, `ADM-388`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-380` Customer & Organization Registration

**Create the initial customer account and organization profile.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-380 |
| Who uses it | ticvai staff holding `TENANT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/tenants-licensing/customer-organization-registration-adm-380` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-002.

**Known correction pending (do not draw the wrong version)**

- **Calls tenant-permission operations with no tenant picker and no platform-staff grant: submitOnboardingApplication (TENANT_CONFIGURE).** Why: The Console runs outside every cell; a platform token carries no tenant permission until a time-boxed grant is open, so these calls are refused 403 as drawn. Either add the R098 pattern (tenant picker, Open access grant with step-up, grant panel, grantRequired state, as on ADM-412) or the screen belongs in Venue Management (P08), where the tenant's own staff use it. *(source: R098; contracts/spine/identity.yaml#openPlatformStaffGrant; screens/P09-platform-admin-console.yaml#ADM-412; Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Work email | email field | optional | — | max length 256 | name@example.ae | Step one of the prospect sign-up session (DEC-167, "Email + one-time code"): the code goes to this address; "Continue saved setup" is the same field (CHG-CLN-019). | `StartProspectSignupRequest.email` |
| One-time code | text field | optional | — | pattern `^[0-9]{6}$` | — | Six digits from the email; a right code opens the sign-up session (prospectAuth) the rest of the journey runs on and resumes a saved setup (CHG-CLN-019). | `VerifyProspectSignupCodeRequest.code` |

**Sent by *Send code*** (`startProspectSignup`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Email `email` | email field | required | — | max length 256 | name@example.ae | The prospect's work email; the one-time code goes here. | `startProspectSignup` body |
| Locale `locale` | text field | optional | — | max length 16 | — | The language the code message is written in (BCP 47), default English. | `startProspectSignup` body |

**Sent by *Verify code*** (`verifyProspectSignupCode`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | pattern `^[0-9]{6}$` | — | The six-digit one-time code sent to the email. | `verifyProspectSignupCode` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send code (secondary button) | `startProspectSignup` POST `/auth/prospect/signup` | StartProspectSignupRequest | ProspectSignupChallenge | 400 Validation failed | produces a document or message: Start (or resume) a TICVAI sign-up with an email and a one-time code |
| Verify code (secondary button) | `verifyProspectSignupCode` POST `/auth/prospect/signup/{challengeId}/verify` | VerifyProspectSignupCodeRequest | ProspectSignupSession | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The challenge is spent (`codeExpired`) because the code expired, five wrong codes were tried or it was already … | produces a document or message: Prove the email with the one-time code and receive the prospect sign-up session |
| Submit (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer organization registration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer organization registration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer organization registration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer organization registration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The challenge is spent (`codeExpired`) because the code expired, five wrong codes were tried or it was already used; start a new one with startProspectSignup; 422 The code is wrong (`codeInvalid`); it counts against the challenge |

#### Consistency with other screens

- Match `SGN-002`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
organisation: Marina Leisure Group LLC
contact: aisha@marinaleisure.ae
```

#### Permissions

- `submitOnboardingApplication` → `TENANT_CONFIGURE` (configure) · public, prospect
- `startProspectSignup` → no permission · public, prospect
- `verifyProspectSignupCode` → no permission · public, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-380` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-380`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 2: Works in Customer & Organization Registration → Create the initial customer account and organization profile.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-380?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send code, Verify code, Submit, Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-381` Venue Type & Business Profile

**Understand what type of operation the customer runs.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-381 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Visual cards) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/venue-type-business-profile-adm-381` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-003.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 12 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue type | multi select | — | — | — | — | The venue types the prospect chooses from (Museum, Attraction, Theme Park, Waterpark, Stadium, Theatre, Exhibition / Event Venue, Zoo / Aquarium, Tour Operator, Entertainment Center, Multi-Venue … | — |

#### Outputs: what the screen shows and produces

**Shown**

**The selected venue type business** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Attraction | text | not in the schema: `Attraction` |
| Theme park | text | not in the schema: `Theme Park` |
| Waterpark | text | not in the schema: `Waterpark` |
| Stadium | text | not in the schema: `Stadium` |
| Theatre | text | not in the schema: `Theatre` |
| Exhibition / event venue | text | not in the schema: `Exhibition / Event Venue` |
| Zoo / aquarium | text | not in the schema: `Zoo / Aquarium` |
| Tour operator | text | not in the schema: `Tour Operator` |
| Entertainment center | text | not in the schema: `Entertainment Center` |
| Multi venue operator | text | not in the schema: `Multi-Venue Operator` |
| Other | text | not in the schema: `Other` |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue type business list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue type business untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue type business yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue type business are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-003`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every venue type business:
- Museum: 57
  Attraction: 312
  Theme Park: 312
  Waterpark: 46
  Stadium: 11
  Theatre: 11
  Exhibition / Event Venue: 128
  Zoo / Aquarium: 57
- Museum: 11
  Attraction: 74
  Theme Park: 74
  Waterpark: 312
  Stadium: 128
  Theatre: 128
  Exhibition / Event Venue: 46
  Zoo / Aquarium: 11
- Museum: 128
  Attraction: 19
  Theme Park: 19
  Waterpark: 74
  Stadium: 46
  Theatre: 46
  Exhibition / Event Venue: 312
  Zoo / Aquarium: 128
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operating model question: attraction, museum, park, event, etc. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-810)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-381` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-381`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 4: Works in Venue Type & Business Profile → Understand what type of operation the customer runs.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-381?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-382` Visitor, Capacity & Operational Scale

**Collect the information required to understand venue size and eventually calculate the VSI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-382 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/visitor-capacity-operational-scale-adm-382` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-004.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visitor capacity operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visitor capacity operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visitor capacity operational yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visitor capacity operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-004`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
annualVisitors: 1,200,000
peakDay: 18,000
venues: 3
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visitor capacity and scale: expected annual/monthly visitors, venue capacity, entrances/exits, number of POS and access-control points, user count, estimated transaction volume, growth forecast. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-811)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-382` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-382`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 6: Works in Visitor, Capacity & Operational Scale → Collect the information required to understand venue size and eventually calculate the VSI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-382?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-383` Sales Channel Assessment

**Understand how the customer intends to sell tickets and products.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-383 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/sales-channel-assessment-adm-383` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): listSaleChannel reads a live tenant's configured channels, and a prospect has no cell and no channels; the assessment uses the answers only (scoreVsiAssessment) …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Part of a prospect's assessment for TICVAI licensing: how the customer intends to sell (online, on site, B2C, B2B/OTA) with volumes; it feeds the venue size score and tier. This is TICVAI's own console work.

**Fixed on main** (the package already carries these; draw what it says): The screen also reads listSaleChannel (a live tenant's configured channels) for a prospect who has no tenant. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☐ On-site POS | select field | — | — | — | — | — | — |
| ☐ Own Website / B2C | text field | — | — | — | — | — | — |
| ☐ Mobile App | select field | — | — | — | — | — | — |
| ☐ Tour Operators | select field | — | — | — | — | — | — |
| ☐ Hotels | select field | — | — | — | — | — | — |
| ☐ Resellers | select field | — | — | — | — | — | — |
| ☐ Corporate Customers | select field | — | — | — | — | — | — |
| ☐ Call Center | select field | — | — | — | — | — | — |
| ☐ Kiosk | select field | — | — | — | — | — | — |
| ☐ Flying / Mobile POS | text field | — | — | — | — | — | — |
| ☐ OTA / Third-Party Channels | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **channel answers**: Each channel of interest with an expected annual volume. *(source: contracts/satellite/subscription.yaml#scoreVsiAssessment / DI-812)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales channel assessment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales channel assessment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales channel assessment configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
answers:
  online: 120,000 tickets a year
  onsite: 300,000
  b2bOta: 40,000
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales channels of interest (online, on-site, B2C, B2B/OTA) each with volume estimates. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-812)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-383` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-383`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 8: Works in Sales Channel Assessment → Understand how the customer intends to sell tickets and products.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-383?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-384` Ticketing & Product Requirements

**Understand what the venue intends to sell.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-384 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/ticketing-product-requirements-adm-384` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-006.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| General Admission | select field | — | — | — | — | — | — |
| Dated Admission | select field | — | — | — | — | — | — |
| Timeslot Admission | select field | — | — | — | — | — | — |
| Open-Dated Ticket | select field | — | — | — | — | — | — |
| Multi-Day Ticket | select field | — | — | — | — | — | — |
| Family Ticket | select field | — | — | — | — | — | — |
| Group Ticket | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Annual Pass | select field | — | — | — | — | — | — |
| Season Pass | select field | — | — | — | — | — | — |
| Voucher | select field | — | — | — | — | — | — |
| Bundle | select field | — | — | — | — | — | — |
| Add-On | select field | — | — | — | — | — | — |
| Camp / Course | select field | — | — | — | — | — | — |
| Special Event | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticketing product requirements configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticketing product requirements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticketing product requirements configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-006`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  General Admission: 46
  Dated Admission: 128
  Timeslot Admission: 1.8 s
  Open-Dated Ticket: 19
  Multi-Day Ticket: 19
  Family Ticket: 312
  Group Ticket: 312
  Membership: 46
  Annual Pass: 74
  Season Pass: 19
  Voucher: 46
  Bundle: 46
  Add-On: 312
  Camp / Course: 312
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-384` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-384`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 10: Works in Ticketing & Product Requirements → Understand what the venue intends to sell.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-384?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-385` Access, Queue & Visitor Experience Assessment

**Determine admission and visitor-flow requirements.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-385 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/access-queue-visitor-experience-assessment-adm-385` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-007.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access queue visitor list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access queue visitor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access queue visitor yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access queue visitor are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-007`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gates: 14
turnstiles: true
virtualQueue: wanted
rfidWristbands: true
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-385` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-385`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 12: Works in Access, Queue & Visitor Experience Assessment → Determine admission and visitor-flow requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-385?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-386` Additional Business Module Assessment

**Identify additional TICVAI operational modules based on the customer's business.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-386 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/additional-business-module-assessment-adm-386` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-008.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listModuleCatalogue` (onLoad, Additional modules)

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The additional business module list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the additional business module untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No additional business module yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the additional business module are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-008`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listModuleCatalogue (ModuleListing):
- name: Growth plan
  description: Guest charged twice at Main Gate Till 3
  price: AED 1,250.00
- name: AquaCove Annual Pass Gold
  description: Group of 40 from Desert Gate Tours
  price: AED 48,000.00
```

#### Permissions

- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect
- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Additional modules needed (F&B, retail, membership/CRM, etc.). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-814)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-386` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-386`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 14: Works in Additional Business Module Assessment → Identify additional TICVAI operational modules based on the customer's business.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-386?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-387` Integration, Payment & Technical Readiness

**Understand external systems and technical requirements that could affect complexity, implementation approach and commercial scope.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-387 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/integration-payment-technical-readiness-adm-387` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-009.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration payment technical list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration payment technical untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration payment technical yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration payment technical are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-009`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
paymentProviders:
- Network International
erp: SAP S/4HANA
hosting: cloud
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Payment gateway/device integration needs: select from a supported list or specify an unlisted provider. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-815)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-387` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-387`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 16: Works in Integration, Payment & Technical Readiness → Understand external systems and technical requirements that could affect complexity, implementation approach and commercial scope.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-387?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-388` AI Assessment Summary & Handoff

**Consolidate everything learned during onboarding and prepare the customer for Board 3/4 commercial recommendation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-388 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/ai-assessment-summary-handoff-adm-388` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Duplicate of SGN-010.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-379` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assessment summary handoff list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assessment summary handoff untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assessment summary handoff yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the assessment summary handoff are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-010`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
vsi: 68
profile: Large waterpark operator
modules:
- ticketing
- pos
- fnb
- access
- membership
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The prospect reviews then submits the assessment, which becomes the basis for the system's proposed commercial/licensing model. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-816)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-388` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS154 Subscription Licensing AI Self Service Board 2.dc.html#adm-388`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 2
- Flow F208 *Subscription Licensing AI Self Service board 2: Welcome & Start Your TICVAI …*, step 18: Works in AI Assessment Summary & Handoff → Consolidate everything learned during onboarding and prepare the customer for Board 3/4 commercial recommendation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-388?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-379`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listModuleCatalogue": {"method":"GET","path":"/module-catalogue","contract":"subscription","summary":"Modules, their dependencies and their commercial treatment","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"ModuleListing"},
"scoreVsiAssessment": {"method":"POST","path":"/vsi-assessments","contract":"subscription","summary":"Score a prospect's answers into a tier and a package","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VsiAssessment","responds":"VsiResult"},
"startProspectSignup": {"method":"POST","path":"/auth/prospect/signup","contract":"identity","summary":"Start (or resume) a TICVAI sign-up with an email and a one-time code","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StartProspectSignupRequest","responds":"ProspectSignupChallenge"},
"submitOnboardingApplication": {"method":"POST","path":"/onboarding-applications","contract":"subscription","summary":"A prospect signs themselves up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OnboardingApplication","responds":"OnboardingApplication"},
"verifyProspectSignupCode": {"method":"POST","path":"/auth/prospect/signup/{challengeId}/verify","contract":"identity","summary":"Prove the email with the one-time code and receive the prospect sign-up session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VerifyProspectSignupCodeRequest","responds":"ProspectSignupSession"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BillingEntity": {"type":"object","x-ticvai-persistence":"control.billing_entity","description":"**The company TICVAI invoices for a tenant, with its trade licence and VAT certificate** (Chinmay, 2 October, workbook Q209: \"a new billing-entity record in the subscription contract\"; DI-830; CHG-CSA-030). One per tenant, mastered in the control plane. `legalName` and `countryCode` are required on save (400 otherwise); they are not marked required here so the record can ride, optional, on an onboarding application. **Documents** (workbook Q210, the default): a trade licence always; a VAT certificate when a `trn` is entered. Which documents a country requires is configurable per country (tenancy `RegionSettings`); the default is that rule.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null while it rides on an onboarding application."},"legalName":{"type":"string","maxLength":300},"tradeLicenceNumber":{"type":"string","maxLength":100,"nullable":true},"trn":{"type":"string","maxLength":30,"nullable":true,"description":"The tax registration number; entering one makes the VAT certificate required."},"countryCode":{"type":"string","minLength":2,"maxLength":2},"address":{"type":"string","maxLength":1000,"nullable":true},"invoiceEmail":{"type":"string","format":"email","nullable":true},"documents":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification.","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["tradeLicence","vatCertificate"]},"fileRef":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"verificationStatus":{"type":"string","enum":["missing","uploaded","verified","rejected","expired"]}}}},"missingDocuments":{"type":"array","readOnly":true,"description":"The documents the country's rule requires that are not yet uploaded and verified.","items":{"type":"string"}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ModuleListing": {"type":"object","x-ticvai-persistence":"subscription.module_listing","description":"Board 4.6. **A marketplace without a dependency graph sells combinations that cannot be provisioned.**\n**TICVAI configures each module's price here, and tenants are billed per module (decided 29 September, Chinmay).** A usage-priced module (the AI module's tokens) has `pricingBasis` `metered`: `price` is then per `meteredUnitSize` units of `meteredMetric`, and the invoice carries it as a `metered` line.\n","required":["moduleCode"],"properties":{"moduleCode":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"category":{"type":"string","nullable":true},"requiresModules":{"type":"array","items":{"type":"string"}},"incompatibleWithModules":{"type":"array","items":{"type":"string"}},"includedInTiers":{"type":"array","items":{"type":"string"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"pricingBasis":{"type":"string","enum":["included","flatFee","perVenue","perUnit","revenueShare","metered"]},"meteredMetric":{"allOf":[{"$ref":"#/components/schemas/UsageMetric"}],"nullable":true,"description":"For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise."},"meteredUnitSize":{"type":"integer","minimum":1,"nullable":true,"description":"For `metered`, how many units `price` buys (e.g. 1000 tokens). Null otherwise."},"provisioningMinutes":{"type":"integer","nullable":true},"requiresProfessionalServices":{"type":"boolean","default":false},"status":{"type":"string","enum":["available","beta","deprecated","withdrawn"]}}},
"OnboardingApplication": {"type":"object","x-ticvai-persistence":"control.onboarding_application","description":"BL-165. **`subscription` handles the operator-led path well and has no prospect-led one.** `createTenant` and `provisionCell` assume somebody at Softlabs decided this tenant exists.\nA prospect signing themselves up is a different shape: **nothing is provisioned until they are verified**, because an unverified application that provisions a cell is a cell somebody has to clean up.\n","required":["id","companyName","contactEmail","status"],"properties":{"id":{"type":"string","format":"uuid"},"companyName":{"type":"string"},"contactEmail":{"type":"string","format":"email"},"contactPhone":{"type":"string","nullable":true},"countryCode":{"type":"string"},"venueTypeTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"**A water park and a theatre need different defaults**, and asking a prospect to configure 300 settings from empty is asking them to leave.\n"},"requestedPlanId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["submitted","verifying","approved","provisioning","active","rejected","abandoned"]},"trialEndsAt":{"type":"string","format":"date-time","nullable":true,"description":"**Trial is a state, not a plan.** A tenant on trial has the plan they will pay for and a date by which they must — modelling it as a separate plan means migrating them at conversion, which is the moment least worth adding risk to.\n"},"rejectionReason":{"type":"string","nullable":true},"provisionedTenantId":{"type":"string","format":"uuid","nullable":true},"billingEntity":{"$ref":"#/components/schemas/BillingEntity","description":"**The company to be invoiced, saved on the application before verification** (Chinmay, 2 October, workbook Q209 and Q223; CHG-CSA-030). Nothing is provisioned until the application is verified; on provisioning it becomes the tenant's billing entity (`getBillingEntity`)."}}},
"ProspectSignupChallenge": {"type":"object","x-ticvai-persistence":"none — the challenge is held by identity for its lifetime (CHG-CLN-019)","required":["challengeId","expiresInSeconds"],"properties":{"challengeId":{"type":"string","format":"uuid"},"expiresInSeconds":{"type":"integer"},"resendAfterSeconds":{"type":"integer"}}},
"ProspectSignupSession": {"type":"object","x-ticvai-persistence":"none — a session token, not a table the package reads (CHG-CLN-019)","required":["token","expiresAt","resumed"],"properties":{"token":{"type":"string","description":"The `prospectAuth` bearer token, scoped to one onboarding application."},"expiresAt":{"type":"string","format":"date-time"},"onboardingApplicationId":{"type":"string","format":"uuid","nullable":true,"description":"The application in progress for this email, or null until the first `submitOnboardingApplication`."},"resumed":{"type":"boolean","description":"True when the email already had an application in progress (\"Continue saved setup\")."}}},
"StartProspectSignupRequest": {"type":"object","x-ticvai-persistence":"none — request only (DEC-167; CHG-CLN-019)","required":["email"],"properties":{"email":{"type":"string","format":"email","maxLength":256,"description":"The prospect's work email; the one-time code goes here."},"locale":{"type":"string","maxLength":16,"nullable":true,"description":"The language the code message is written in (BCP 47), default English."}}},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]},
"VerifyProspectSignupCodeRequest": {"type":"object","x-ticvai-persistence":"none — request only (CHG-CLN-019)","required":["code"],"properties":{"code":{"type":"string","pattern":"^[0-9]{6}$","description":"The six-digit one-time code sent to the email."}}},
"VsiAssessment": {"type":"object","x-ticvai-persistence":"subscription.vsi_assessment","description":"Board 2 — the ten-screen questionnaire, as data.","properties":{"id":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"contactEmail":{"type":"string","nullable":true},"venueType":{"type":"string","nullable":true},"answers":{"type":"object","additionalProperties":true},"requestedModules":{"type":"array","items":{"type":"string"}},"submittedAt":{"type":"string","format":"date-time","nullable":true}}},
"VsiResult": {"type":"object","description":"Board 2.10. **A prospect told only their price has been told nothing they can argue with.**\n","properties":{"assessmentId":{"type":"string","format":"uuid"},"score":{"type":"number"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"factors":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"answer":{"type":"string"},"points":{"type":"number"}}}},"recommendedModules":{"type":"array","items":{"type":"string"}},"recommendedPlanId":{"type":"string","format":"uuid","nullable":true},"indicativePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}
}
```
