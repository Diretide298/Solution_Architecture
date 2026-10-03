# WS110 — ACCREDITATION board 3

**9 screens · 15 operations · 25 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCREDITATION_APPLY, ACCREDITATION_APPROVE, ACCREDITATION_VIEW, APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_REQUEST, APPROVAL_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |

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
| `BO-635` | Accreditation Review Queue | D | 17 | 26 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-636` | Application Review Workspace | D | 3 | 12 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-637` | Approval Workflow Builder | B | 19 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-638` | Approval Rules & Conditions | B | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-639` | Reviewer Assignment & Delegation | B | 0 | 0 | 6 | 49 | 0 | 0 | — | notStarted (—) |
| `BO-640` | Rejection & Resubmission Management | D | 0 | 20 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-641` | Escalation & Exception Management | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-642` | Approval Decision History | D | 0 | 12 | 6 | 2 | 0 | 3 | — | notStarted (—) |
| `BO-643` | Approval Policy Validation & Publication | B | 20 | 34 | 6 | 2 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-637, BO-638, BO-639, BO-640, BO-641, BO-642 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-635` Accreditation Review Queue

**Central operational queue for applications requiring review.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-635 |
| Who uses it | venue staff holding `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`, `APPROVAL_ACT` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each record shall show) and no metric row |
| Offline | online only |
| Opens with | `instanceId` (navigation), `applicationId` (navigation) |
| Route | `/access-venue/accreditation-review-queue-bo-635` |

**What the spec says about it.** **One queue and one workspace component, used in P11 (ACC-006, ACC-007) and here (decided 2 October 2026 by Chinmay, DEC-368).** The component is `screens/_components.yaml`'s (screens-other). **Renders the shared `accreditationReview` queue** (`screens/_components.yaml` patterns; decided 2 October 2026 by Chinmay, DEC-368; CHG-SOT-018), the same component as ACC-006 on P11: a fix to one is a fix to both.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The back-office review queue: every application awaiting a decision, with the signals a supervisor uses to route work (stage, reviewer, SLA, verification, risk), and the assignment actions. It is the landing of board 3 and the same queue reviewers work in the portal. The one thing to get right: sorted by decision due, with SLA ageing that matches the category's SLA, so a backlog of media passes shows up before it breaches.

**Known correction pending (do not draw the wrong version)**

- **Primary button labelled "Key requirement - 12.1.3"** Why: Pack text turned into a button label; the pack's actions are Open review, Assign reviewer, Reassign, Escalate, Bulk assign. *(source: screens/P08-venue-back-office.yaml#BO-636; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Stage, assigned reviewer, verification and document status, risk are not on AccreditationApplication** Why: They come from the approvals request, the holder and the documents; the queue needs a joined read. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Edge to BO-636 carries nothing** Why: BO-636 needs applicationId. *(source: screens/P08-venue-back-office.yaml#BO-636; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every accreditation review queue", "The selected accreditation review queue"** Why: Generated placeholders. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Assign, reassign, bulk assign and escalate are not bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the SLA clock pause while an application waits on the applicant?** → Drawn default accepted: Paused; the chip shows "Paused - waiting on applicant". *(decided by Chinmay, 2026-10-02; DEC-465 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search accreditation review queue | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by category, event, venue, organization, reviewer, workflow stage and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |

**Form: Assign reviewer** (modal, opened by *Assign reviewer*; *Assign reviewer* calls `actOnWorkflowInstance`, *Cancel* sends nothing)

**Collects what `actOnWorkflowInstance` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Reassign · Retry step · Skip step · Resume · Cancel · Extend sla · Add backup approver · Change priority · Escalate exception | — | What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). | `actOnWorkflowInstance` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | Mandatory for every action (pack 13.2.5, "actions capture a mandatory reason") | `actOnWorkflowInstance` body |
| Workflow step execution `workflowStepExecutionId` | picker: choose a workflow step execution | optional | — | — | shows names, sends the id | The step acted on; for `retryStep` the step to retry from. | `actOnWorkflowInstance` body |
| Workflow exception `workflowExceptionId` | picker: choose a workflow exception | optional | — | — | shows names, sends the id | The exception the action is taken from; required for `escalateException` | `actOnWorkflowInstance` body |
| Assignee principal `assigneePrincipalId` | picker: choose an assignee principal | optional | — | — | shows names, sends the id | Required for `reassign`, `addBackupApprover` and `escalateException` | `actOnWorkflowInstance` body |
| Alternative node `alternativeNodeId` | text field | optional | — | — | — | For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative) | `actOnWorkflowInstance` body |
| Corrected input `correctedInput` | key and value settings | optional | — | — | — | For `resume`, the corrected input of the failed step (Correct Data) | `actOnWorkflowInstance` body |
| Extend by minutes `extendByMinutes` | number field (minutes) | optional | — | min 1; max 43200 | — | Required for `extendSla` | `actOnWorkflowInstance` body |
| Priority `priority` | text field | optional | — | max length 30 | — | Required for `changePriority` | `actOnWorkflowInstance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not …

**Form: Escalate** (modal, opened by *Escalate*; *Escalate* calls `decideAccreditationApplication`, *Cancel* sends nothing)

**Collects what `decideAccreditationApplication` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Approve · Reject · Return for information · Escalate | — | — | `decideAccreditationApplication` body |
| Reason `reason` | text area | optional | — | — | — | — | `decideAccreditationApplication` body |
| Missing requirements `missingRequirements` | list of values (chips) | optional | — | — | — | — | `decideAccreditationApplication` body |
| Access profile `accessProfileId` | picker: choose an access profile | optional | — | — | shows names, sends the id | — | `decideAccreditationApplication` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideAccreditationApplication` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideAccreditationApplication` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Applicant name, reference, organisation or email. *(source: screens/P08-venue-back-office.yaml#BO-636)*
- **Filters**: Category, Event, Venue, Organisation, Reviewer (including "Unassigned" and "Me"), Workflow stage, SLA status (Within SLA, Due within 24 h, Overdue), Verification status. *(source: screens/P08-venue-back-office.yaml#BO-636)*

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation review queue** (data table)

| Shows | Format | Notes |
|---|---|---|
| Application ID | text | not in the schema: `Application ID` |
| Applicant name | text | not in the schema: `Applicant name` |
| Photo | text | not in the schema: `Photo` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Organization | text | not in the schema: `Organization` |
| Event / venue | text | not in the schema: `Event / venue` |
| Submission date | text | not in the schema: `Submission date` |
| Verification status | text | not in the schema: `Verification status` |
| Document status | text | not in the schema: `Document status` |
| Current workflow stage | text | not in the schema: `Current workflow stage` |
| Assigned reviewer | text | not in the schema: `Assigned reviewer` |
| SLA ageing | text | not in the schema: `SLA ageing` |
| Risk / exception indicator | text | not in the schema: `Risk / exception indicator` |

**The selected accreditation review queue** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”.

| Shows | Format | Notes |
|---|---|---|
| Application ID | text | not in the schema: `Application ID` |
| Applicant name | text | not in the schema: `Applicant name` |
| Photo | text | not in the schema: `Photo` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Organization | text | not in the schema: `Organization` |
| Event / venue | text | not in the schema: `Event / venue` |
| Submission date | text | not in the schema: `Submission date` |
| Verification status | text | not in the schema: `Verification status` |
| Document status | text | not in the schema: `Document status` |
| Current workflow stage | text | not in the schema: `Current workflow stage` |
| Assigned reviewer | text | not in the schema: `Assigned reviewer` |
| SLA ageing | text | not in the schema: `SLA ageing` |
| Risk / exception indicator | text | not in the schema: `Risk / exception indicator` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key requirement: 12.1.3 (primary button) | navigation or local | — | — | — | — |
| Assign reviewer (secondary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | opens modal first |
| Escalate (secondary button) | `decideAccreditationApplication` POST `/accreditation-applications/{applicationId}/decide` | inline | AccreditationApplication | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Review queue table**: Columns: Application ID, Applicant (photo, name), Category, Organisation, Event or venue, Submitted, Verification (identity: Verified, Pending, Failed), Documents ("2 of 3 verified"), Stage ("Security approval - 2 of 3"), Assigned reviewer, SLA ageing (chip: "Due in 2 d", "Due today" amber, "Overdue 1 d" red), Risk (icons with tooltip: possible duplicate, document expires before event, government or VIP, resubmission). Sorted by decision due ascending. Title "Applications to review". Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-635 / screens/P08-venue-back-office.yaml#BO-636 / contracts/satellite/accreditation.yaml#listAccreditationApplications / DI-661)*
- **Board quick links**: Workflow builder (BO-637), Rules and conditions (BO-638), Reviewer assignment (BO-639), Rejections (BO-640), Policy publication (BO-643), each returning here. *(source: DI-653)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open review**: Opens BO-636 with the applicationId. *(source: screens/P08-venue-back-office.yaml#BO-636)*
- **Assign reviewer / Reassign / Bulk assign**: Picker of reviewers eligible for the stage, with their open load ("Maria Santos - 14 open"); reassign asks for a reason, which is audited; bulk assign confirms the count. *(source: screens/P08-venue-back-office.yaml#BO-636 / screens/P08-venue-back-office.yaml#BO-639)*
- **Escalate**: Reason required; sends to the next level; the stage column updates. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / DI-661)*

**Data it reads**: `listAccreditationApplications` (onLoad, The review queue)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-636` Application Review Workspace: *Application Review Workspace*; carries `applicationId`
- → `BO-637` Approval Workflow Builder: *Approval Workflow Builder*
- → `BO-638` Approval Rules & Conditions: *Approval Rules & Conditions*
- → `BO-639` Reviewer Assignment & Delegation: *Reviewer Assignment & Delegation*
- → `BO-640` Rejection & Resubmission Management: *Rejection & Resubmission Management*; carries `applicationId`
- → `BO-641` Escalation & Exception Management: *Escalation & Exception Management*
- → `BO-642` Approval Decision History: *Approval Decision History*
- → `BO-643` Approval Policy Validation & Publication: *Approval Policy Validation & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation review queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation review queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation review queue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation review queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Edge cases to draw

- **Applications waiting on the applicant (informationRequested)**: Listed in a separate "Waiting on applicant" tab with days waiting; they do not count against the reviewer's SLA chip. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*
- **Reviewer lacks rights for a stage**: Assign to self disabled with the permission named (per VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `ACC-006`: Same queue component and SLA chips (per VO-R14).
- Match `BO-623`: SLA buckets match the intake monitor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- id: ACR-2026-004390
  applicant: Sara Al Nuaimi
  category: Media
  organisation: Gulf Lens Media
  submitted: 08 Oct 2026
  verification: Verified
  documents: 3 of 3
  stage: Media manager - 1 of 2
  reviewer: Maria Santos
  sla: Due today
  risk: []
- id: ACR-2026-004402
  applicant: James Carter
  category: VIP
  organisation: Northbridge Events
  submitted: 09 Oct 2026
  verification: Pending
  documents: 1 of 2
  stage: VIP relations - 1 of 1
  reviewer: Unassigned
  sla: Due in 2 d
  risk:
  - Possible duplicate
- id: ACR-2026-004377
  applicant: Khalid Al Zaabi
  category: Government or authority
  organisation: Abu Dhabi Civil Defence
  submitted: 01 Oct 2026
  verification: Verified
  documents: 1 of 2
  stage: Security approval - 2 of 3
  reviewer: Ahmed Al Mansoori
  sla: Overdue 1 d
  risk:
  - Government
```

#### Permissions

- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff
- `decideAccreditationApplication` → `ACCREDITATION_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.3 | Approval Workflow System shall support accreditation review and approval. | Accreditation & Credential Management | CONTRACTED | `decideAccreditationApplication` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-635` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-635`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 1: Opens Accreditation Review Queue → Central operational queue for applications requiring review.
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F219 branch at step 1 (expected): when Nothing has been set up on Accreditation Review Queue yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F219 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-635?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key requirement: 12.1.3, Assign reviewer, Escalate.
- [ ] Every transition is wired: `BO-100`, `BO-636`, `BO-637`, `BO-638`, `BO-639`, `BO-640`, `BO-641`, `BO-642`, `BO-643`.
- [ ] Every gated control is gated: `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`, `APPROVAL_ACT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-636` Application Review Workspace

**Give reviewers a complete decision workspace.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-636 |
| Who uses it | venue staff holding `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `applicationId` (navigation), `documentId` (navigation) |
| Route | `/access-venue/application-review-workspace-bo-636` |

**What the spec says about it.** **One queue and one workspace component, used in P11 (ACC-006, ACC-007) and here (decided 2 October 2026 by Chinmay, DEC-368).** The component is `screens/_components.yaml`'s (screens-other). **Renders the shared `accreditationReview` workspace** (`screens/_components.yaml` patterns; decided 2 October 2026 by Chinmay, DEC-368; CHG-SOT-018), the same component as ACC-007 on P11: a fix to one is a fix to both.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The workspace reads one application (getAccreditationApplication); listAccreditationApplications bound as "The application" is redundant. It shows and verifies …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The decision workspace for one application: the person, their identity and documents, the organisation, what they asked for, the proposed access profile and validity, their history, and the approval path so far. The reviewer approves, rejects, asks for more, escalates or puts on hold. The one thing to get right: the system refuses approval while any mandatory condition is incomplete, and the workspace shows that list instead of an enabled button.

**Known correction pending (do not draw the wrong version)**

- **Primary button has no label; a dataTable with no columns** Why: The pack lists five decision actions and eleven views. *(source: screens/P08-venue-back-office.yaml#BO-636 / screens/P08-venue-back-office.yaml#BO-637; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Put on hold is not a decision; the reason is one field** Why: decideAccreditationApplication has approve, reject, returnForInformation and escalate, and a single reason, while the pack asks for internal comments separate from the applicant-visible explanation. *(source: screens/P08-venue-back-office.yaml#BO-637 / screens/P08-venue-back-office.yaml#BO-640 / contracts/satellite/accreditation.yaml#decideAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listAccreditationApplications bound as "The application" beside getAccreditationApplication (CHG-WIR-001); verifyAccreditationDocument and the history reads are not bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May an approver widen access beyond the category's default profile, or must that be escalated?** → Drawn default accepted: Narrowing allowed; widening only through Escalate. *(decided by Chinmay, 2026-10-02; DEC-466 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

**Form: Verify document** (modal, opened by *Verify document*; *Verify document* calls `verifyAccreditationDocument`, *Cancel* sends nothing)

**Collects what `verifyAccreditationDocument` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Verified · Rejected · Illegible · Wrong document · Expired | — | — | `verifyAccreditationDocument` body |
| Reason `reason` | text area | optional | — | — | — | — | `verifyAccreditationDocument` body |
| Expires at `expiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `verifyAccreditationDocument` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve (access profile, valid from, valid to)**: Access profile pre-filled from the category default, changeable to another allowed for the category; validity pre-filled from the programme, and valid to no later than the earliest mandatory document expiry. A zone preview lists what the person will open. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / DI-662 / DI-663)*
- **Reject**: Reason code from the programme's list (Invalid identity document, Missing documentation, Failed identity verification, Eligibility not met, Duplicate application, Security rejection, Quota exceeded, Ineligible organisation, Other), an explanation the applicant reads, and the requirements to fix. *(source: screens/P08-venue-back-office.yaml#BO-640 / contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Request more information**: Tick the requirements missing or wrong and say what is needed. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Escalate**: Reason from the escalation list (SLA breach, Identity conflict, High-security access, Government or authority, VIP exception, Missing mandatory information, Manual policy override, Senior management decision) and a comment. *(source: screens/P08-venue-back-office.yaml#BO-640)*

#### Outputs: what the screen shows and produces

**Shown**

**History** (data table, from `listAccreditationAudit`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Holder | the name it points at, never the id | — |
| Action | text | — |
| Actor principal | the name it points at, never the id | — |
| Previous value | text | — |
| New value | text | — |
| Reason | text | — |
| Approval request | the name it points at, never the id | — |
| Previous record hash | text | — |
| Record hash | text | — |
| Integrity | chip: Intact, Broken, Unverifiable | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Verify document (secondary button) | `verifyAccreditationDocument` POST `/accreditation-documents/{documentId}/verify` | inline | AccreditationDocument | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Person and identity**: Photo beside ID document image, identity verification status, masked document number, organisation affiliation. *(source: screens/P08-venue-back-office.yaml#BO-636 / ADR-0063)*
- **Request**: Category, requested event or venue, requested validity, proposed access profile with zones. *(source: screens/P08-venue-back-office.yaml#BO-636)*
- **Documents**: Each with state and an inline verify control (same as BO-630). *(source: contracts/satellite/accreditation.yaml#listAccreditationDocuments / contracts/satellite/accreditation.yaml#verifyAccreditationDocument)*
- **History**: Previous accreditations, previous rejections or suspensions, resubmission chain, comments and the approval path as a timeline (stage, approver, decision, time). *(source: screens/P08-venue-back-office.yaml#BO-636 / screens/P08-venue-back-office.yaml#BO-637 / contracts/satellite/accreditation.yaml#listAccreditationAudit)*
- **Blockers**: When Approve is not possible, a red list above the buttons of each unmet approval requirement, unverified document or pending duplicate, each linking to its fix. *(source: screens/P08-venue-back-office.yaml#BO-637 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve**: Disabled while blockers exist; at a non-final stage moves the application to the next stage ("Sent to Security approval"); at the final stage approves and offers Issue credential (BO-645). *(source: screens/P08-venue-back-office.yaml#BO-643 / contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Reject / Request more information / Escalate**: Each confirms with what the applicant will read (for reject and request) and returns to the queue with the next application selected. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Put on hold**: Drawn per the pack and greyed with "Not yet supported" (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-637)*

**Data it reads**: `getAccreditationApplication` (onLoad, The application being decided); `listAccreditationDocuments` (onLoad, The application's documents); `listAccreditationAudit` (onLoad, The applicant's previous accreditations and decisions)

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*; carries `applicationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The application review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the application review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No application review yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the application review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two reviewers in parallel stages**: Each sees the other's stage state; the application approves only when all parallel stages have. *(source: screens/P08-venue-back-office.yaml#BO-637)*
- **Decision fails to record**: "The decision was not recorded" with buttons live; nothing is assumed. *(source: screens/P11-accreditation-portal.yaml#ACC-007)*

#### Consistency with other screens

- Match `ACC-007`: Same workspace (per VO-R14); same reason lists and drawer.
- Match `BO-640`: The rejection reason list is the one configured on BO-640.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
application:
  id: ACR-2026-004377
  applicant: Khalid Al Zaabi
  category: Government or authority
  organisation: Abu Dhabi Civil Defence
  requested: Winter Festival 2026, Summit Peaks
  proposedAccess: All zones - fire safety
  validity: 01-14 Dec 2026
path:
- Initial validation - passed 02 Oct (Maria Santos)
- Department approval - approved 05 Oct (Omar Haddad)
- Security approval - due 12 Oct (Ahmed Al Mansoori)
blockers:
- Sponsor confirmation not verified
```

#### Permissions

- `decideAccreditationApplication` → `ACCREDITATION_APPROVE` (operate) · staff
- `getAccreditationApplication` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff
- `verifyAccreditationDocument` → `ACCREDITATION_APPROVE` (operate) · staff
- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.3 | Approval Workflow System shall support accreditation review and approval. | Accreditation & Credential Management | CONTRACTED | `decideAccreditationApplication` |
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-636` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-636`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 2: Works in Application Review Workspace → Give reviewers a complete decision workspace.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-636?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Verify document.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-637` Approval Workflow Builder

**Design the product approval workflows (who approves a product change, in which order); accreditation approvals are configured with the approvals platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · task VM-BO-637 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/approval-workflow-builder-bo-637` |

**Known gaps.** **Approval Workflow Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Reusable approval workflows for product creation and change: which product types and change types route to it, the stages in order (role or person, sequential or parallel, SLA, escalation), and what rejection and resubmission do.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The operation is named approveWorkflow but it designs (creates or changes) a workflow. (CHG-SBO-005)
- No read operation: the screen declares only approveWorkflow and nothing that returns the current configuration. (CHG-WIR-027)

**Fixed on main** (the package already carries these; draw what it says): The purpose says accreditation approval workflows while the operation (approveWorkflow) is the product approval workflow designer. (CHG-SBO-017).

#### Inputs: what the user enters or picks

**Form: Save product approval workflow** (modal, opened by *Save product approval workflow*; *Save product approval workflow* calls `approveWorkflow`, *Cancel* sends nothing)

**Collects what `approveWorkflow` sends before it is called.** Nothing in the body is required. Optional: `workflowName`, `applicableProductTypes`, `venue`, `department`, `changeTypes`, `approvalStages`, `rejectionBehavior`, `resubmissionBehavior`, `workflowId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workflow name `workflowName` | text field | optional | — | — | — | Workflow name | `approveWorkflow` body |
| Applicable product types `applicableProductTypes` | multi-select chips | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Applicable product types; empty = all | `approveWorkflow` body |
| Venue `venue` | text field | optional | — | — | — | Venue id; empty = all venues | `approveWorkflow` body |
| Department `department` | text field | optional | — | — | — | Department | `approveWorkflow` body |
| Change types `changeTypes` | multi-select chips | optional | — | New product · Description · Price · Validity · Capacity · Entitlement · Eligibility · Tax · Channel · Media · Policy · Relationship … | — | Change types routed to this workflow (Conditional Approval: e.g. | `approveWorkflow` body |
| Approval stages `approvalStages` | repeatable rows | optional | — | — | — | Approval stages, e.g. | `approveWorkflow` body |
| Order `approvalStages[].order` | number field | optional | — | — | — | Stage order; stages sharing an order run in parallel, otherwise sequential | `approveWorkflow` body |
| Name `approvalStages[].name` | text field | optional | — | — | — | — | `approveWorkflow` body |
| Approver role `approvalStages[].approverRole` | text field | optional | — | — | — | — | `approveWorkflow` body |
| Specific approver `approvalStages[].specificApproverId` | text field | optional | — | — | — | — | `approveWorkflow` body |
| Approval group `approvalStages[].approvalGroupId` | text field | optional | — | — | — | — | `approveWorkflow` body |
| Mandatory `approvalStages[].mandatory` | toggle | optional | — | — | — | — | `approveWorkflow` body |
| Sla hours `approvalStages[].slaHours` | number field (hours) | optional | — | — | — | SLA in hours | `approveWorkflow` body |
| Escalate to role `approvalStages[].escalateToRole` | text field | optional | — | — | — | Escalation when the SLA is missed | `approveWorkflow` body |
| Delegation allowed `approvalStages[].delegationAllowed` | toggle | optional | — | — | — | — | `approveWorkflow` body |
| Reminder every hours `approvalStages[].reminderEveryHours` | number field (hours) | optional | — | — | — | Reminder frequency | `approveWorkflow` body |
| Rejection behavior `rejectionBehavior` | segmented control | optional | — | Return to draft · Return to previous stage · Close request | — | What happens on rejection; default returnToDraft (decided 29 September, readiness close-out) | `approveWorkflow` body |
| Resubmission behavior `resubmissionBehavior` | segmented control | optional | — | Restart from first stage · Resume at rejecting stage | — | Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out) | `approveWorkflow` body |
| Workflow `workflowId` | picker: choose a workflow | optional | — | — | shows names, sends the id | Existing workflow to change; empty to create | `approveWorkflow` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **changeTypes**: Conditional routing ("a price change goes to Commercial and Finance") as tags. *(source: contracts/spine/catalogue.yaml#approveWorkflow)*
- **stages**: A horizontal chain of stage cards; rejection default returns to draft, resubmission default restarts at stage 1. *(source: contracts/spine/catalogue.yaml#approveWorkflow)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save product approval workflow (primary button) | `approveWorkflow` PUT `/workflow` | ApprovalWorkflowDesignerInput | ApprovalWorkflowDesignerView | — | opens modal first |

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workflow:
  name: Price change
  productTypes:
  - datedAdmission
  - membership
  changeTypes:
  - price
  stages:
  - Revenue manager
  - Finance manager (SLA 24 h)
```

#### Permissions

- `approveWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-637` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-637`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 4: Works in Approval Workflow Builder → Configure reusable accreditation approval workflows.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-637?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel, Save product approval workflow.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-638` Approval Rules & Conditions

**Define when a particular approval workflow is applied.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · task VM-BO-638 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/approval-rules-conditions-bo-638` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** When a particular approval workflow applies to an accreditation application (conditions on category, organisation, zone).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save visual workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval rules conditions list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval rules conditions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval rules conditions yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval rules conditions are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Media accreditation for Wave Arena final
condition: organisation type = media AND zone includes pitch-side
workflow: Two-stage review
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-638` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-638`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 6: Works in Approval Rules & Conditions → Define when a particular approval workflow is applied.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-638?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save visual workflow, Cancel.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-639` Reviewer Assignment & Delegation

**Manage reviewers and approval responsibilities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · task VM-BO-639 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/reviewer-assignment-delegation-bo-639` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who reviews accreditation applications, by category and level, with delegation.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalMatrix: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalMatrix)*
- **Approval matrix rules**: Ordered; the first matching rule wins. A venue may tighten and never loosen a rule from above: a higher threshold, fewer approvers or a different approver role are each loosening and refused 409 loosensParentRule. Saving creates a new version; requests in flight keep the version they were raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix; R129; R183)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save approval matrix (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reviewer delegation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reviewer delegation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reviewer delegation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reviewer delegation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **setApprovalMatrix answers 409**: Show it as something the person can act on, not a failure: Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold, fewer approvers or a different approver role; audit R129); or `unreachableRule` — a rule can never match because an earlier one always does. `ruleOrder` names the offending r... *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
category: Media
level1: Accreditation officer
level2: Head of security
delegate: Omar Haddad until 15/10/2026
```

#### Permissions

- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-639` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-639`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 8: Works in Reviewer Assignment & Delegation → Manage reviewers and approval responsibilities.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-639?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save approval matrix, Cancel.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-640` Rejection & Resubmission Management

**Control rejected applications and resubmission workflows.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-640 |
| Who uses it | venue staff holding `ACCREDITATION_APPLY`, `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `applicationId` (navigation) |
| Route | `/access-venue/rejection-resubmission-management-bo-640` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where refused and returned applications are managed: the reasons a reviewer can choose, what the applicant may do next, and each refused application's version history from first submission to resubmission. Staff can also resubmit on an applicant's behalf. The one thing to get right: every version is preserved and visible, so "refused twice, approved on the third" is readable at a glance.

**Known correction pending (do not draw the wrong version)**

- **Rejection reasons and the resubmission policy have no configuration operation** Why: The pack makes them configurable; the contract has a free-text reason only and no policy. *(source: screens/P08-venue-back-office.yaml#BO-640 / contracts/satellite/accreditation.yaml#decideAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Primary button has no label** Why: The actions are Resubmit on the applicant's behalf and Amend. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): No list of refused and returned applications is bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is there a limit on resubmissions?** → Drawn default accepted: No limit drawn; the field exists greyed. *(decided by Chinmay, 2026-10-02; DEC-467 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rejection reasons (configuration)**: The pack's nine reasons as a list with Active toggles and an "Add reason"; each has an applicant-facing wording in English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-640)*
- **Resubmission policy**: Per programme, which the applicant may do (Correct information, Replace documents, Upload additional evidence, Resubmit) and how many resubmissions are allowed. *(source: screens/P08-venue-back-office.yaml#BO-640)*
- **Resubmit on behalf (what changed)**: Required note up to 1,000 characters; amended answers optional. *(source: contracts/satellite/accreditation.yaml#resubmitAccreditationApplication)*

#### Outputs: what the screen shows and produces

**Shown**

**Refused and returned** (data table, from `listAccreditationApplications`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Reference | text | — |
| Programme | the name it points at, never the id | — |
| Category code | text | — |
| Applicant type | text | — |
| Submitted by principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Subject | grouped details | Name, date of birth, nationality, contact — shaped by the requirements matrix. |
| Requirement status | list or chips (count when long) | — |
| Requirement code | text | — |
| Satisfied | yes / no (icon or chip) | — |
| Document | the name it points at, never the id | — |
| Status | chip: Draft, Submitted, Under review, Information requested, Approved, Rejected… | — |
| Decision reason | text | — |
| Missing requirements | list or chips (count when long) | The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting |
| Decision due at | 1 Oct 2026, 14:30 | When a decision is due — the approvals request's SLA. |
| Approval request | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Renews holder | the name it points at, never the id | 12.1.37. |
| Resubmission of application | the name it points at, never the id | 12.1.33. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Refused and returned list**: Columns Application, Applicant, Category, Reason, Decided, By, Versions, Waiting on (Applicant or Staff). Filters by reason and category. *(source: screens/P08-venue-back-office.yaml#BO-640)*
- **Version history**: "v1 submitted 01 Oct - refused 02 Oct, Missing documentation; v2 submitted 05 Oct - with a reviewer". Each version opens read-only; differences between versions highlighted. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication / MATRIX 12.1.33)*
- **Internal comments and applicant explanation**: Two separate blocks; the applicant explanation is labelled "The applicant reads this". *(source: screens/P08-venue-back-office.yaml#BO-640)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resubmit on the applicant's behalf**: From returned, the same application goes back to the reviewer; from refused, a new linked application is created and opened. *(source: contracts/satellite/accreditation.yaml#resubmitAccreditationApplication)*
- **Amend a returned application**: Editable only while returned for information; any other state is read-only with the reason. *(source: contracts/satellite/accreditation.yaml#updateAccreditationApplication)*
- **Reject or return (from this screen)**: Same decision dialog as BO-636. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*

**Data it reads**: `getAccreditationApplication` (onLoad, The rejected or returned application); `listAccreditationApplications` (onLoad, Applications refused or returned for information)

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*; carries `applicationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rejection resubmission list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rejection resubmission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rejection resubmission yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rejection resubmission are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not informationRequested or rejected, or the programme's window is closed; 409 The application is not draft or informationRequested; 422 A requirement that blocks submission is still not satisfied; 422 A subject field fails its requirement row's fieldType or validation |

#### Edge cases to draw

- **Resubmission limit reached**: Resubmit disabled with "Limit of 2 resubmissions reached for this programme". *(source: screens/P08-venue-back-office.yaml#BO-640)*
- **Programme closed since the refusal**: Resubmit refused with the closing date. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*

#### Consistency with other screens

- Match `ACC-004`: The applicant explanation and allowed actions are what ACC-004 shows.
- Match `BO-636`: Reason codes come from this list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reasons:
- Invalid identity document
- Missing documentation
- Failed identity verification
- Eligibility not met
- Duplicate application
- Security rejection
- Accreditation quota exceeded
- Ineligible organisation
- Other
row:
  application: ACR-2026-004355
  applicant: Priya Nair
  category: Media
  reason: Missing documentation
  decided: 02 Oct 2026
  by: Maria Santos
  versions: 2
  waitingOn: Staff
```

#### Permissions

- `decideAccreditationApplication` → `ACCREDITATION_APPROVE` (operate) · staff
- `getAccreditationApplication` → `ACCREDITATION_VIEW` (read) · staff
- `resubmitAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `updateAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.3 | Approval Workflow System shall support accreditation review and approval. | Accreditation & Credential Management | CONTRACTED | `decideAccreditationApplication` |
| 12.1.33 | Accreditation Rejection Management - System shall support rejection and resubmission workflows. | Accreditation & Credential Management | CONTRACTED | `resubmitAccreditationApplication` |
| 12.1.2 | Accreditation Registration System shall support accreditation applications through configurable forms. | Accreditation & Credential Management | CONTRACTED | `updateAccreditationApplication` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-640` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-640`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 10: Works in Rejection & Resubmission Management → Control rejected applications and resubmission workflows.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-640?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`, `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-641` Escalation & Exception Management

**Handle applications requiring special review.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · task VM-BO-641 |
| Who uses it | venue staff holding `APPROVAL_REQUEST` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/access-venue/escalation-exception-management-bo-641` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Accreditation applications needing special review: escalated, exceptional, conflicting.

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

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation exception yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalation exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
application: ACC-2026-0193
reason: Name matches watch list
escalatedTo: Head of security
waiting: 2 h 15 min
```

#### Permissions

- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.47 | Multi-Level Escalation - System shall support escalation through multiple organizational levels. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.48 | Escalation History - System shall maintain complete escalation history. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-641` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-641`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 12: Works in Escalation & Exception Management → Handle applications requiring special review.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-641?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-642` Approval Decision History

**Maintain a complete record of every approval decision.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-642 |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/approval-decision-history-bo-642` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-025): A decision history is a read-only record, yet it declared only a write from the promotions contract (approveDecision); the accreditation decision record is …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every approval decision kept as a record: who, what, when, outcome and comment.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only approveDecision and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Decision history** (data table, from `listAccreditationAudit`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Holder | the name it points at, never the id | — |
| Action | text | — |
| Actor principal | the name it points at, never the id | — |
| Previous value | text | — |
| New value | text | — |
| Reason | text | — |
| Approval request | the name it points at, never the id | — |
| Previous record hash | text | — |
| Record hash | text | — |
| Integrity | chip: Intact, Broken, Unverifiable | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **history**: Filter by kind, approver and outcome. *(source: contracts/satellite/promotions.yaml#approveDecision)*

**Data it reads**: `listAccreditationAudit` (onLoad, Every accreditation decision: who granted what to whom, and …)

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval decision history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval decision history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval decision history yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval decision history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
decisions:
- request: Price change Day Pass
  by: Finance manager
  outcome: approved
  at: 2026-11-10 14:02
```

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-642` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-642`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 14: Works in Approval Decision History → Maintain a complete record of every approval decision.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-642?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-643` Approval Policy Validation & Publication

**Validate and publish approval workflow configurations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · task VM-BO-643 |
| Who uses it | venue staff holding `ACCREDITATION_VIEW`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/approval-policy-validation-publication-bo-643` |

**What the spec says about it.** The approvals validation and publication, opened with the accreditation scope (VO-R14): the approvals platform owns the machinery; accreditation does not (design-note correction).

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The gate before an approval workflow goes live: a validation checklist for the workflow (steps, approvers, mandatory stages, SLA and escalation rules, rejection reasons, resubmission policy, linked verification checks, scope, and the credential issuance dependency), a simulation, and the publish, deactivate and clone controls. The one thing to get right: simulation runs inside this screen against sample applications and shows the route each would take before anything is published.

**Fixed on main** (the package already carries these; draw what it says): Only listAccreditationAudit is bound (as "Decision history") (CHG-WIR-001); Possible duplicate of the approvals platform screens (CHG-SBO-016); A dataTable with no columns; gap says nothing can be drawn (CHG-SBO-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is BO-643 kept, or does accreditation link to the approvals module's validation screen?** → Drawn default accepted: Keep the entry on board 3 and open the shared component. *(decided by Chinmay, 2026-10-02; DEC-468 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |
| Module | text field | — | — | `listWorkflow` ?module |
| Status | text field | — | — | `listWorkflow` ?status |
| Priority | text field | — | — | `listWorkflow` ?priority |

**Form: Simulate** (modal, opened by *Simulate*; *Simulate* calls `simulateWorkflowTestingImpact`, *Cancel* sends nothing)

**Collects what `simulateWorkflowTestingImpact` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workflow `workflowId` | text field | required | — | — | — | Workflow under test | `simulateWorkflowTestingImpact` body |
| Test mode `testMode` | radio group | required | — | Manual test case · Sample transaction · Historical replay · Scenario simulation · Batch test | — | How the workflow is tested | `simulateWorkflowTestingImpact` body |
| Version `version` | text field | optional | — | — | — | Version under test | `simulateWorkflowTestingImpact` body |
| Compare with version `compareWithVersion` | text field | optional | — | — | — | Existing version to compare against for regression | `simulateWorkflowTestingImpact` body |
| Input payload `inputPayload` | text field | optional | — | — | — | Sample transaction as a JSON document, for manual and sample tests | `simulateWorkflowTestingImpact` body |
| Replay from `replayFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Historical replay start | `simulateWorkflowTestingImpact` body |
| Replay to `replayTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Historical replay end | `simulateWorkflowTestingImpact` body |

**Form: Publish workflow** (modal, opened by *Publish workflow*; *Publish workflow* calls `setVisualWorkflow`, *Cancel* sends nothing)

**Collects what `setVisualWorkflow` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Definition `definition` | text field | required | — | — | — | The workflow graph (nodes and connections) as a JSON document | `setVisualWorkflow` body |
| Node types `nodeTypes` | multi-select chips | optional | — | Start · Trigger · Task · Decision · Approval · System action · Notification · Wait · Timer · Parallel branch · Merge · Escalation … | — | Node kinds used in this workflow | `setVisualWorkflow` body |
| Workflow name `workflowName` | text field | required | — | — | — | Workflow Name | `setVisualWorkflow` body |
| Module `module` | text field | required | — | — | — | Module | `setVisualWorkflow` body |
| Business process `businessProcess` | text field | optional | — | — | — | Business Process | `setVisualWorkflow` body |
| Owner `owner` | text field | optional | — | — | — | Owner | `setVisualWorkflow` body |
| Version `version` | text field | optional | — | — | — | Version | `setVisualWorkflow` body |
| Priority `priority` | text field | optional | — | — | — | Priority | `setVisualWorkflow` body |
| Effective from `effectiveFrom` | text field | optional | — | — | — | Effective Dates | `setVisualWorkflow` body |
| Validation issues `validationIssues` | multi-select chips | optional | — | Dead ends · Missing outcomes · Circular loops · Missing assignee · Invalid actions | — | Design problems the designer found (read-only) | `setVisualWorkflow` body |
| Workflow `workflowId` | text field | optional | — | — | — | Workflow identifier; absent on input to create a new workflow | `setVisualWorkflow` body |
| Trigger `trigger` | text field | optional | — | — | — | What starts the workflow | `setVisualWorkflow` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Effective to | `setVisualWorkflow` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Workflow and version**: Select the workflow; versions listed with status (Draft, Published, Deactivated) and who published each. *(source: screens/P08-venue-back-office.yaml#BO-643)*
- **Simulation input**: Pick a sample application (or describe one: category, applicant type, event, organisation, requested zones) and run. *(source: screens/P08-venue-back-office.yaml#BO-643)*

#### Outputs: what the screen shows and produces

**Shown**

**Workflows** (data table, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Validation checks** (data table, from `simulateWorkflowTestingImpact`): The ten checks the pack lists, as results of the simulation, before Publish.

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow under test |
| Test mode | chip: Manual test case, Sample transaction, Historical replay, Scenario simulation, Batch … | How the workflow is tested |
| Rules evaluated | 1,234 | Rules Evaluated |
| Conditions matched | 1,234 | Conditions Matched |
| Decisions | 1,234 | Decisions |
| Approval path | text | Approval Path |
| Actions | 1,234 | Actions |
| Notifications | 1,234 | Notifications |
| Sla | text | SLA |
| Expected outcome | text | Expected Outcome |
| Compare with version | text | Existing version to compare against for regression |
| Input payload | text | Sample transaction as a JSON document, for manual and sample tests |
| Replay from | 1 Oct 2026 | Historical replay start |
| Replay to | 1 Oct 2026 | Historical replay end |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Simulate (secondary button) | `simulateWorkflowTestingImpact` PUT `/workflow-testing-impact` | WorkflowTestingSimulationImpactAnalysisInput | WorkflowTestingSimulationImpactAnalysisView | — | opens modal first |
| Publish workflow (secondary button) | `setVisualWorkflow` PUT `/visual-workflow` | VisualWorkflowDesignerInput | VisualWorkflowDesignerView | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validation checklist**: Ten items in the pack's order, each Passed, Missing or Not applicable, with a Fix link to BO-637, BO-638, BO-639 or BO-640. *(source: screens/P08-venue-back-office.yaml#BO-643)*
- **Routing preview**: For the simulated application, the stages it would pass, approvers, SLA per stage and the escalation path, as a horizontal path. *(source: screens/P08-venue-back-office.yaml#BO-643)*
- **Decision history**: A link to the decision history of applications decided under the selected version. *(source: contracts/satellite/accreditation.yaml#listAccreditationAudit)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft / Validate / Simulate / Preview routing**: Validate re-runs the checklist; Simulate and Preview show the route without creating anything. *(source: screens/P08-venue-back-office.yaml#BO-643)*
- **Publish**: Disabled until the checklist passes; confirmation names the programmes and categories that will use it and says applications already in flight keep the version they started under. *(source: screens/P08-venue-back-office.yaml#BO-643)*
- **Deactivate / Clone**: Deactivate blocked while a programme that is open depends on the workflow; Clone creates a new draft version. *(source: screens/P08-venue-back-office.yaml#BO-643)*

**Data it reads**: `listAccreditationAudit` (onLoad, Decision history); `listWorkflow` (onLoad, The approval workflows in force)

**Where the user goes next**

- → `BO-635` Accreditation Review Queue: *Back to Accreditation Review Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval policy validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval policy validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval policy validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval policy validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Rule conflict (two rules match the same application)**: Shown in the checklist with both rules named and their priority. *(source: screens/P08-venue-back-office.yaml#BO-639)*

#### Consistency with other screens

- Match `ADM-326`: The platform approvals module's workflow validation and simulation (P09) does the same job; accreditation should reuse that component, not grow a second one.
- Match `BO-624`: Same checklist component and button row as programme publication.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workflow: Government accreditation - 3 stages
version: v4 (draft)
checklist:
  steps: Passed
  approvers: Passed
  mandatoryStages: Passed
  sla: Passed
  escalation: Missing
  rejectionReasons: Passed
  resubmission: Passed
  verificationChecks: Passed
  scope: Passed
  issuanceDependency: Passed
simulation: 'Government or authority + All zones: Initial validation > Department approval > Security approval (5
  working days)'
```

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff
- `listWorkflow` → `APPROVAL_VIEW` (read) · staff
- `simulateWorkflowTestingImpact` → `APPROVAL_CONFIGURE` (configure) · staff
- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-643` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-643`
- Workshop pack: ACCREDITATION.pdf board 3
- Flow F219 *ACCREDITATION board 3: Accreditation Review Queue*, step 16: Works in Approval Policy Validation & Publication → Validate and publish approval workflow configurations.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-643?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Simulate, Publish workflow.
- [ ] Every transition is wired: `BO-635`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"actOnWorkflowInstance": {"method":"POST","path":"/workflow-instances/{instanceId}/actions","contract":"approvals","summary":"An operator's intervention in a running workflow","permission":"APPROVAL_ACT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowInstanceActionInput","responds":"WorkflowInstance"},
"approveWorkflow": {"method":"PUT","path":"/workflow","contract":"catalogue","summary":"Approval Workflow Designer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalWorkflowDesignerInput","responds":"ApprovalWorkflowDesignerView"},
"decideAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/decide","contract":"accreditation","summary":"Approve, reject, return for more, or escalate","permission":"ACCREDITATION_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"getAccreditationApplication": {"method":"GET","path":"/accreditation-applications/{applicationId}","contract":"accreditation","summary":"One application, with where each requirement stands","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationApplication"},
"listAccreditationApplications": {"method":"GET","path":"/accreditation-applications","contract":"accreditation","summary":"Applications, by state and programme","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"applicantType","in":"query","required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationDocuments": {"method":"GET","path":"/accreditation-documents","contract":"accreditation","summary":"Documents supplied, by holder, application, requirement or state","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"applicationId","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"requirementCode","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflow": {"method":"GET","path":"/workflow","contract":"approvals","summary":"Workflow Operations Command Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"resubmitAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/resubmit","contract":"accreditation","summary":"Send an application back after a return for information or a rejection","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateWorkflowTestingImpact": {"method":"PUT","path":"/workflow-testing-impact","contract":"approvals","summary":"Workflow Testing, Simulation & Impact Analysis","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowTestingSimulationImpactAnalysisInput","responds":"WorkflowTestingSimulationImpactAnalysisView"},
"updateAccreditationApplication": {"method":"PUT","path":"/accreditation-applications/{applicationId}","contract":"accreditation","summary":"Save a draft, or amend an application returned for information","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationApplication","responds":"AccreditationApplication"},
"verifyAccreditationDocument": {"method":"POST","path":"/accreditation-documents/{documentId}/verify","contract":"accreditation","summary":"Accept or refuse a submitted document","permission":"ACCREDITATION_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationDocument"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationApplication": {"type":"object","x-ticvai-persistence":"accreditation.application","description":"Board 1.3. **Usually submitted by an organisation on behalf of its people.**","required":["programmeId"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"applicantType":{"type":"string"},"submittedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"object","additionalProperties":true,"description":"Name, date of birth, nationality, contact — shaped by the requirements matrix."},"requirementStatus":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"requirementCode":{"type":"string"},"satisfied":{"type":"boolean"},"documentId":{"type":"string","format":"uuid","nullable":true}}}},"status":{"type":"string","enum":["draft","submitted","underReview","informationRequested","approved","rejected","withdrawn","expired"]},"decisionReason":{"type":"string","nullable":true},"missingRequirements":{"type":"array","readOnly":true,"description":"The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting","items":{"type":"string"}},"decisionDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a decision is due — the approvals request's SLA. **A date, not a queue position**"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"holderId":{"type":"string","format":"uuid","nullable":true},"renewsHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"},"resubmissionOfApplicationId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.33. The rejected application this one resubmits, so the rejection stays in the record"},"resubmissionNote":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true,"description":"What the applicant changed, from `resubmitAccreditationApplication`"},"submittedAt":{"type":"string","format":"date-time","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"ApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Existing workflow to change; empty to create","format":"uuid","nullable":true}}},
"ApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Workflow id","format":"uuid"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"VisualWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"VisualWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"WorkflowInstance": {"type":"object","x-ticvai-persistence":"approvals.workflow_instance","description":"**One running workflow** (pack 13.2.1, 13.2.3 and 13.2.5; data model for the agreed operations, 29 September). Started by a `WorkflowTrigger`, on the version in force at that moment and kept on it to the end (audit R129). Its steps are `WorkflowStepExecution` rows, keyed by the same `correlationId` the participating services trace with. **The SLA clock and its reminder and escalation timestamps are held here**, not in a table of their own: there is one clock per instance, and the SLA, Escalation & Bottleneck Monitor lists instances. Lifecycle in `states/workflow-instance.yaml`. The engine writes this row; an operator changes it only through `actOnWorkflowInstance`, which keeps each change as a `WorkflowIntervention` (decided 29 September, writers pass).","required":["id","workflowDefinitionId","workflowVersionId","sourceModule","status","correlationId","startedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"workflowDefinitionId":{"type":"string","format":"uuid"},"workflowVersionId":{"type":"string","format":"uuid","description":"The version the instance started on; never changes"},"workflowTriggerId":{"type":"string","format":"uuid","nullable":true},"sourceModule":{"$ref":"#/components/schemas/WorkflowModule"},"businessObjectType":{"type":"string","maxLength":100,"nullable":true},"businessObjectId":{"type":"string","nullable":true,"description":"**A reference, never a copy**, as `ApprovalRequest.subjectId`"},"initiatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Null when a system event or schedule started it"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"string","maxLength":30,"nullable":true},"currentNodeId":{"type":"string","nullable":true,"description":"The node of the version's graph the instance is at"},"status":{"$ref":"#/components/schemas/WorkflowInstanceStatus"},"correlationId":{"type":"string","maxLength":100,"description":"The shared correlation id every participating service logs, for distributed tracing"},"slaPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The `ApprovalSlaPolicy` whose clock runs on this instance"},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean","default":false},"escalationLevel":{"type":"integer","minimum":0,"default":0},"firstReminderAt":{"type":"string","format":"date-time","nullable":true},"secondReminderAt":{"type":"string","format":"date-time","nullable":true},"managerEscalatedAt":{"type":"string","format":"date-time","nullable":true},"executiveEscalatedAt":{"type":"string","format":"date-time","nullable":true},"slaOutcome":{"type":"string","enum":["metWithinTarget","metAfterReminder","metAfterEscalation","breached"],"nullable":true,"description":"How the instance finished against its SLA; set on completion (the monitor's Final Outcome)"},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WorkflowInstanceActionInput": {"type":"object","x-ticvai-persistence":"none — request only; writes approvals.workflow_intervention (schema WorkflowIntervention) (decided 29 September, writers pass)","description":"One operator action on a running workflow instance (decided 29 September, writers pass).","required":["action","reason"],"properties":{"action":{"$ref":"#/components/schemas/WorkflowInterventionAction"},"reason":{"type":"string","minLength":1,"maxLength":500,"description":"Mandatory for every action (pack 13.2.5, \"actions capture a mandatory reason\")"},"workflowStepExecutionId":{"type":"string","format":"uuid","nullable":true,"description":"The step acted on; for `retryStep` the step to retry from. Defaults to the instance's current step"},"workflowExceptionId":{"type":"string","format":"uuid","nullable":true,"description":"The exception the action is taken from; required for `escalateException`"},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `reassign`, `addBackupApprover` and `escalateException`"},"alternativeNodeId":{"type":"string","nullable":true,"description":"For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative)"},"correctedInput":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `resume`, the corrected input of the failed step (Correct Data)"},"extendByMinutes":{"type":"integer","minimum":1,"maximum":43200,"nullable":true,"description":"Required for `extendSla`"},"priority":{"type":"string","maxLength":30,"nullable":true,"description":"Required for `changePriority`"}}},
"WorkflowInstanceStatus": {"type":"string","description":"Where one running workflow stands (pack 13.2.1 and 13.2.3; decided 29 September, readiness close-out). Modelled in `states/workflow-instance.yaml`.","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"]},
"WorkflowInterventionAction": {"type":"string","description":"What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). The effect of each is on `actOnWorkflowInstance`.","enum":["reassign","retryStep","skipStep","resume","cancel","extendSla","addBackupApprover","changePriority","escalateException"]},
"WorkflowModule": {"type":"string","description":"The module a workflow, rule or automation belongs to and a workflow instance originates from. The same values as `WorkflowOperationsCommandCenterView.module` (decided 29 September, readiness close-out), named so the workflow engine's tables share one vocabulary (data model for the agreed operations, 29 September).","enum":["ticketing","pricing","finance","procurement","crm","resourceManagement","fnb","retail","groupSales","customerService","membership","wallet","waiver","subscriptionLicensing"]},
"WorkflowOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance (schema WorkflowInstance) (data model for the agreed operations, 29 September)","description":"**What Workflow Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowInstanceId":{"type":"string","description":"Workflow Instance ID"},"workflow":{"type":"string","description":"Workflow"},"module":{"type":"string","enum":["ticketing","pricing","finance","procurement","crm","resourceManagement","fnb","retail","groupSales","customerService","membership","wallet","waiver","subscriptionLicensing"],"description":"Module the workflow originates from"},"businessObject":{"type":"string","description":"Business Object"},"initiatedBy":{"type":"string","description":"Initiated By"},"started":{"type":"string","format":"date-time","description":"Started"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"priority":{"type":"string","description":"Priority"},"sla":{"type":"string","description":"SLA"},"status":{"type":"string","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"],"description":"Status"}},"required":["workflowInstanceId"]},
"WorkflowOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"workflowsRunning":{"type":"integer","description":"Workflows Running"},"startedToday":{"type":"integer","description":"Started Today"},"completedToday":{"type":"integer","description":"Completed Today"},"pendingApprovals":{"type":"integer","description":"Pending Approvals"},"waitingTasks":{"type":"integer","description":"Waiting Tasks"},"slaAtRisk":{"type":"integer","description":"SLA At Risk"},"slaBreached":{"type":"integer","description":"SLA Breached"},"failedWorkflows":{"type":"integer","description":"Failed Workflows"},"escalated":{"type":"integer","description":"Escalated"},"automatedExecutions":{"type":"integer","description":"Automated Executions"},"averageCompletionTime":{"type":"integer","description":"Minutes"},"automationSuccessRate":{"type":"number","description":"Automation Success Rate"}}},
"WorkflowTestingSimulationImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]},
"WorkflowTestingSimulationImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"rulesEvaluated":{"type":"integer","description":"Rules Evaluated"},"conditionsMatched":{"type":"integer","description":"Conditions Matched"},"decisions":{"type":"integer","description":"Decisions"},"approvalPath":{"type":"string","description":"Approval Path"},"actions":{"type":"integer","description":"Actions"},"notifications":{"type":"integer","description":"Notifications"},"sla":{"type":"string","description":"SLA"},"expectedOutcome":{"type":"string","description":"Expected Outcome"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]}
}
```
