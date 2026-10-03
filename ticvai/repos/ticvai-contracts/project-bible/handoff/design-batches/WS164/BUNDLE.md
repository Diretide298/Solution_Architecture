# WS164 — Resource Management Configuration board 10

**10 screens · 12 operations · 13 schemas · 6 permissions**

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
  `PLATFORM_TENANT_VIEW, PRODUCT_VIEW, REPORT_VIEW_TENANT, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-943` | Resource Analytics Command Center | D | 0 | 30 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-944` | Resource Utilization & Capacity Analytics | D | 3 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-945` | Resource Cost, Revenue & Efficiency Analytics | D | 11 | 4 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-946` | Demand Forecast Accuracy & Planning Performance | B | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-947` | Resource KPI, SLA & Performance Framework | D | 0 | 44 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-948` | Resource Governance & Policy Center | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-949` | Approval, Exception & Override Control Center | B | 0 | 20 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `BO-950` | Audit Trail & Resource Decision History | D | 23 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-951` | Resource Integration & System Health Center | D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-952` | Executive Resource Intelligence & AI Improvement Center | D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-947, BO-948, BO-949, BO-951 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-943` Resource Analytics Command Center

**Provide executives and operational managers with a single enterprise dashboard showing the overall health and performance of Resource Management.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-943 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-analytics-command-center-bo-943` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The executive dashboard of resource management: a Resource Health score with its components, headline KPIs, breakdown by venue, attraction, event, department, category, type, staff, equipment and space, executive health indicators and an AI executive brief, and the entry to the board 10 screens. The one thing to get right: every tile drills to the screen that explains it, and the health score shows its components and weights.

**Known correction pending (do not draw the wrong version)**

- **The fourteen KPIs are drawn as columns of a table titled "Every resource analytics", and the breakdown dimensions as action buttons** Why: KPIs are tiles (VO-R02); breakdown is a control, not six buttons. *(source: screens/P08-venue-back-office.yaml#BO-943; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Readiness, conflicts, unfulfilled demand, overtime, downtime, cost, forecast vs actual and the health score have no source among the bound reads** Why: Only listResources and getResourceUtilisation are bound. *(source: contracts/satellite/resources.yaml#getResourceUtilisation / contracts/satellite/resources.yaml#listResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who sets the Resource Health score weights, and where?** → Drawn default accepted: Show the weights read-only under the gauge with "Set in Governance & Policy" (BO-948). *(decided by Chinmay, 2026-10-02; DEC-519 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Breakdown and period**: Breakdown as a segmented control (Venue, Attraction, Event, Resource category, Resource type, Equipment...); tenant and region only for tenant users; date range. *(source: screens/P08-venue-back-office.yaml#BO-943)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource analytics** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total active resources | text | not in the schema: `Total active resources` |
| Available resources | text | not in the schema: `Available resources` |
| Currently assigned | text | not in the schema: `Currently assigned` |
| Utilization % | text | not in the schema: `Utilization %` |
| Resource readiness % | text | not in the schema: `Resource readiness %` |
| Staff utilization | text | not in the schema: `Staff utilization` |
| Physical asset utilization | text | not in the schema: `Physical asset utilization` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Unfulfilled resource demand | text | not in the schema: `Unfulfilled resource demand` |
| Overtime | text | not in the schema: `Overtime` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Resource related operational cost | text | not in the schema: `Resource-related operational cost` |
| Forecast vs actual demand | text | not in the schema: `Forecast vs actual demand` |
| AI recommendations implemented | text | not in the schema: `AI recommendations implemented` |
| Resource breakdown | text | not in the schema: `Resource Breakdown` |

**The selected resource analytics** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Total active resources | text | not in the schema: `Total active resources` |
| Available resources | text | not in the schema: `Available resources` |
| Currently assigned | text | not in the schema: `Currently assigned` |
| Utilization % | text | not in the schema: `Utilization %` |
| Resource readiness % | text | not in the schema: `Resource readiness %` |
| Staff utilization | text | not in the schema: `Staff utilization` |
| Physical asset utilization | text | not in the schema: `Physical asset utilization` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Unfulfilled resource demand | text | not in the schema: `Unfulfilled resource demand` |
| Overtime | text | not in the schema: `Overtime` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Resource related operational cost | text | not in the schema: `Resource-related operational cost` |
| Forecast vs actual demand | text | not in the schema: `Forecast vs actual demand` |
| AI recommendations implemented | text | not in the schema: `AI recommendations implemented` |
| Resource breakdown | text | not in the schema: `Resource Breakdown` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Resource category (secondary button) | navigation or local | — | — | — | — |
| Resource type (secondary button) | navigation or local | — | — | — | — |
| Equipment (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource health score**: Gauge 0-100 with band label (Excellent, Good, At risk) and components - Availability, Utilisation, Workforce coverage, Asset reliability, Event readiness, Forecast accuracy, Compliance - each clickable. *(source: screens/P08-venue-back-office.yaml#BO-952 / screens/P08-venue-back-office.yaml#BO-943)*
- **KPI tiles**: Total active resources, Available, Currently assigned, Utilisation %, Readiness %, Staff utilisation, Physical asset utilisation, Conflicts, Unfulfilled demand, Overtime (h), Maintenance downtime, Resource-related cost (AED), Forecast vs actual, AI recommendations implemented - tiles with deltas (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-943)*
- **AI executive brief**: Three or four sentences ("Utilisation up 7% this week; Ski School near optimal; Event Operations has 18% under-used equipment; three staffing gaps predicted for the weekend"), labelled AI with data freshness. *(source: screens/P08-venue-back-office.yaml#BO-943)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Board tiles**: Utilisation (BO-944), Cost and efficiency (BO-945), Forecast accuracy, KPI and SLA (BO-947), Governance (BO-948), Approvals, Audit (BO-950), Integration health, Executive intelligence (BO-952). *(source: screens/P08-venue-back-office.yaml#BO-943)*

**Data it reads**: `listResources` (onLoad, Resources at this venue); `getResourceUtilisation` (onLoad, Utilisation across the estate)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-944` Resource Utilization & Capacity Analytics: *Resource Utilization & Capacity Analytics*
- → `BO-945` Resource Cost, Revenue & Efficiency Analytics: *Resource Cost, Revenue & Efficiency Analytics*
- → `BO-946` Demand Forecast Accuracy & Planning Performance: *Demand Forecast Accuracy & Planning Performance*
- → `BO-947` Resource KPI, SLA & Performance Framework: *Resource KPI, SLA & Performance Framework*
- → `BO-948` Resource Governance & Policy Center: *Resource Governance & Policy Center*
- → `BO-949` Approval, Exception & Override Control Center: *Approval, Exception & Override Control Center*
- → `BO-950` Audit Trail & Resource Decision History: *Audit Trail & Resource Decision History*; carries `resourceId`
- → `BO-951` Resource Integration & System Health Center: *Resource Integration & System Health Center*
- → `BO-952` Executive Resource Intelligence & AI Improvement Center: *Executive Resource Intelligence & AI Improvement Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A component of the health score has no data**: The score is computed over the components that have data and says "Forecast accuracy not available - excluded". *(source: screens/P08-venue-back-office.yaml#BO-952)*

#### Consistency with other screens

- Match `BO-854`: Total active resources must match the master-data command centre for the same scope.
- Match `ANL-001`: The venue analytics executive command centre uses the same tile and brief components.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
health:
  score: 94/100 Excellent
  availability: 97%
  utilisation: 88%
  workforceCoverage: 98%
  assetReliability: 91%
  eventReadiness: 96%
  forecastAccuracy: 93%
  compliance: 100%
tiles:
  totalResources: 12,458
  assignedNow: 7,821
  utilisation: 78%
  readiness: 96%
  conflicts: 12
  overtime: 182 h
```

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-943` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-943`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 1: Opens Resource Analytics Command Center → Provide executives and operational managers with a single enterprise dashboard showing the overall health and performance of Resource Management.
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F273 branch at step 1 (expected): when Nothing has been set up on Resource Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F273 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-943?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Attraction, Event, Resource category, Resource type, Equipment.
- [ ] Every transition is wired: `BO-100`, `BO-944`, `BO-945`, `BO-946`, `BO-947`, `BO-948`, `BO-949`, `BO-950`, `BO-951`, `BO-952`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-944` Resource Utilization & Capacity Analytics

**Measure how effectively resources are being utilized and identify overused or underused capacity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-944 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-utilization-capacity-analytics-bo-944` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How well resources are used: available, scheduled and actual hours, idle and blocked time, utilisation against a target, with rankings of under- and over-used resources, a trend, venue comparison and a day-by-hour heatmap. Over-utilisation is capacity risk, not success ("Level 3 instructors above 92% for five weekends"). The one thing to get right: utilisation is over operationally available time (after schedules, blocks, setup and travel), and the target line is always drawn.

**Known correction pending (do not draw the wrong version)**

- **Actual usage, reserved vs assigned time, idle and maintenance time have no field** Why: The read returns available, booked and blocked minutes; the pack's formula uses actual utilised hours. *(source: screens/P08-venue-back-office.yaml#BO-944 / contracts/satellite/resources.yaml#/components/schemas/ResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Trend, heatmap and day/time analysis cannot be fed** Why: The read returns one row per group for the whole window, with no time buckets. *(source: contracts/satellite/resources.yaml#getResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Utilisation target has no field** Why: Under/over-utilisation is judged against a configured target that nothing stores. *(source: screens/P08-venue-back-office.yaml#BO-944; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Group by | select field | — | — | — | — | Sends `?groupBy=`; venue gives the pack's venue comparison. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and grouping**: Period presets and range; group by Resource / Type / Category / Venue as tabs (Overview, By resource, By venue, Heatmap). *(source: screens/P08-venue-back-office.yaml#BO-944 / contracts/satellite/resources.yaml#getResourceUtilisation)*

#### Outputs: what the screen shows and produces

**Shown**

**Available capacity** (metric tile, from `getResourceUtilisation`): Summed and shown in hours.

| Shows | Format | Notes |
|---|---|---|
| Available minutes | 1,234 | — |

**Scheduled** (metric tile, from `getResourceUtilisation`): Summed and shown in hours.

| Shows | Format | Notes |
|---|---|---|
| Booked minutes | 1,234 | — |

**Utilization** (metric tile, from `getResourceUtilisation`)

| Shows | Format | Notes |
|---|---|---|
| Utilisation percent | 1,234.5 | — |

**Actual usage** (metric tile): The pack's formula is actual utilised hours over available; the contract has booked, not actual.

| Shows | Format | Notes |
|---|---|---|
| Actual usage | text | not in the schema: `Actual usage` |

**Resource ranking by utilization** (chart, from `getResourceUtilisation`): Under- and over-utilised resources stand out against the configured target, which has no field.

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Utilisation percent | 1,234.5 | — |

**Utilization by resource** (data table, from `getResourceUtilisation`)

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Available minutes | 1,234 | — |
| Booked minutes | 1,234 | — |
| Blocked minutes | 1,234 | — |
| Utilisation percent | 1,234.5 | — |
| Booking count | 1,234 | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tiles**: Available capacity (h), Scheduled (h), Actual usage (h), Utilisation % ; plus Underutilised % and Overutilised % of resources against target. *(source: screens/P08-venue-back-office.yaml#BO-944)*
- **Trend and ranking**: 30-day trend with the target as a dashed line (80% default); ranking bars sorted by utilisation with resources under target in one colour and over the risk threshold in another. *(source: screens/P08-venue-back-office.yaml#BO-944)*
- **Under- and over-utilisation lists**: Top 5 underutilised (Meeting Room C 21% over 90 days) and top 5 overutilised with trend arrows; AI recommendation as advice ("Consider more Level 3 capacity at weekends"). *(source: screens/P08-venue-back-office.yaml#BO-944 / screens/P08-venue-back-office.yaml#BO-945)*
- **Table**: Label, available h, booked h, blocked h, utilisation %, bookings - hours not minutes. *(source: contracts/satellite/resources.yaml#getResourceUtilisation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Click a resource**: Opens the resource calendar on the period (BO-864) filtered to it. *(source: designer default)*

**Data it reads**: `getResourceUtilisation` (onLoad, Utilisation and capacity)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource utilization capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource utilization capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource utilization capacity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource utilization capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Resource with zero available hours in the period (retired, closed)**: Excluded from rankings with a note, never shown as 0% underutilised. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceUtilisation)*

#### Consistency with other screens

- Match `BO-586`: Same definition and visuals as rental utilisation.
- Match `BO-947`: The target line is the Resource utilisation KPI target.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example:
  group: Ski instructors - Sat 10 Oct 2026
  available: 420 h
  scheduled: 376 h
  actual: 354 h
  utilisation: 84.3%
underutilised:
- Meeting Room C 21%
- Projector P-41 24%
- Booth B-12 29%
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-944` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-944`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 2: Works in Resource Utilization & Capacity Analytics → Measure how effectively resources are being utilized and identify overused or underused capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-944?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-945` Resource Cost, Revenue & Efficiency Analytics

**Measure the financial and operational efficiency of resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-945 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `costId` (navigation) |
| Route | `/rentals/resource-cost-revenue-efficiency-analytics-bo-945` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What resources cost and earn: labour, overtime, maintenance, rental, external, transfer, operating and replacement costs against ticket, experience, rental and event revenue, with efficiency ratios (revenue per resource hour, cost per participant, revenue/cost) and the cost ledger behind them. Finance remains the system of record. The one thing to get right: insights are advice only, and a wrong cost entry is removed and re-entered, never edited.

**Known correction pending (do not draw the wrong version)**

- **"Transfer cost", "Asset operating cost", "Resource replacement cost" are drawn as action buttons, and "Resource id" as a text filter** Why: They are the kind filter (and the kind on create); the resource filter is a picker. *(source: screens/P08-venue-back-office.yaml#BO-945; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The cost table lists id, resourceId, fromVenueId, toVenueId and scopePath** Why: Show names, not ids (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labour, overtime, maintenance, rental and external costs and ticket/experience/event revenue association are not in the cost analytics read** Why: It returns transfer, operating and replacement cost and booking revenue; labour comes from workforce and is not bound; DI-501 asks for cost and revenue by event, which is not a grouping. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCostAnalytics / contracts/satellite/workforce.yaml#getLabourCost / DI-501; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource id | picker: choose a resource (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?resourceId=` to `listResourceCosts`. | `listResourceCosts` ?resourceId |
| Kind | segmented control | optional | — | Transfer · Operating · Replacement | — | Sends `?kind=` to `listResourceCosts`. | `listResourceCosts` ?kind |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listResourceCosts`. | `listResourceCosts` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listResourceCosts`. | `listResourceCosts` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |
| From | date and time picker | — | — | `getResourceCostAnalytics` ?from |
| To | date and time picker | — | — | `getResourceCostAnalytics` ?to |
| Group by | radio group | Resource type | Resource · Resource type · Category · Venue | `getResourceCostAnalytics` ?groupBy |

**Form: Create resource cost** (modal, opened by *Create resource cost*; *Create resource cost* calls `createResourceCost`, *Cancel* sends nothing)

**Collects what `createResourceCost` sends before it is called.** Required: `resourceId`, `kind`, `amount`, `incurredOn`. Optional: `fromVenueId`, `toVenueId`, `note`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resource `resourceId` | picker: choose a resource | required | — | — | shows names, sends the id | — | `createResourceCost` body |
| Kind `kind` | segmented control | required | — | Transfer · Operating · Replacement | — | — | `createResourceCost` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResourceCost` body |
| Incurred on `incurredOn` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createResourceCost` body |
| From venue `fromVenueId` | picker: choose a from venue | optional | — | — | shows names, sends the id | A `transfer` only, with `toVenueId`. | `createResourceCost` body |
| To venue `toVenueId` | picker: choose a to venue | optional | — | — | shows names, sends the id | — | `createResourceCost` body |
| Note `note` | text area | optional | — | — | — | — | `createResourceCost` body |

Errors to draw in the form: 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and grouping**: Period; group by Resource / Type / Category / Venue as tabs. *(source: contracts/satellite/resources.yaml#getResourceCostAnalytics)*
- **Cost entry (create)**: Kind as one choice Transfer / Operating / Replacement; resource picker (not an id field); amount in AED, positive; incurred on date; From and To venue only for Transfer, and they must differ; note. *(source: contracts/satellite/resources.yaml#createResourceCost)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource cost entry** (data table, from `listResourceCosts`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Transfer, Operating, Replacement | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Incurred on | 1 Oct 2026 | — |
| Note | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer cost (primary button) | navigation or local | — | — | — | — |
| Asset operating cost (secondary button) | navigation or local | — | — | — | — |
| Resource replacement cost (secondary button) | navigation or local | — | — | — | — |
| Create resource cost (secondary button) | `createResourceCost` POST `/resource-costs` | ResourceCostEntry | ResourceCostEntry | 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. | gated `RESOURCE_MANAGE`; opens modal first |
| Delete resource cost (destructive button) | `deleteResourceCost` DELETE `/resource-costs/{costId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `RESOURCE_MANAGE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tiles**: Total resource cost, Revenue attributed, Cost/revenue %, with deltas; efficiency tiles Revenue per resource hour, Labour cost per participant, Revenue/cost ratio. *(source: screens/P08-venue-back-office.yaml#BO-945)*
- **Cost breakdown**: Donut and table by cost kind in AED with percent. *(source: screens/P08-venue-back-office.yaml#BO-945)*
- **Cost ledger**: Date, resource name, kind, amount, from-to venue for transfers, note, entered by; newest first, cursor paging (VO-R12); no ids or scope paths. *(source: contracts/satellite/resources.yaml#listResourceCosts)*
- **AI insight**: "Private lessons earn 34% more per instructor hour than group lessons on weekday afternoons" labelled as insight, no Apply button. *(source: screens/P08-venue-back-office.yaml#BO-946)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add cost**: Books the entry; analytics refresh. A transfer with the same venue twice is refused against the field. *(source: contracts/satellite/resources.yaml#createResourceCost)*
- **Remove cost entry**: Confirm naming the amount and period affected ("September analytics will change by AED 450.00"); removal is audited (VO-R16). *(source: contracts/satellite/resources.yaml#deleteResourceCost)*

**Data it reads**: `getResourceUtilisation` (onLoad, Cost and efficiency against use); `getResourceCostAnalytics` (onLoad, What resources cost and earn, grouped); `listResourceCosts` (onLoad, Cost entries booked against resources)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

**What opens over it**

- confirmDialog *Delete resource cost*: **Names what `deleteResourceCost` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource cost revenue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource cost revenue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource cost revenue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource cost revenue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. |

#### Edge cases to draw

- **Group with no booked hours**: Cost per booked hour shows a dash, not zero or infinity. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCostAnalytics)*

#### Consistency with other screens

- Match `BO-862`: Transfers between venues set there are what Transfer cost entries record.
- Match `BO-910`: Maintenance costs are booked as Operating from the maintenance screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example:
  group: Private Ski Lessons - Sep 2026
  revenue: AED 420,000.00
  instructorCost: AED 112,000.00
  hours: 1,480 h
  revenuePerHour: AED 284.00
ledger:
- date: 28 Sep 2026
  resource: Projector P-17
  kind: Operating
  amount: AED 450.00
  note: Lamp replacement
- date: 25 Sep 2026
  resource: Portable stage S-2
  kind: Transfer
  amount: AED 1,200.00
  from: Aqua Park
  to: Summit Peaks
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff
- `getResourceCostAnalytics` → `RESOURCE_VIEW` (read) · staff
- `listResourceCosts` → `RESOURCE_VIEW` (read) · staff
- `createResourceCost` → `RESOURCE_MANAGE` (configure) · staff
- `deleteResourceCost` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-945` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-945`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 4: Works in Resource Cost, Revenue & Efficiency Analytics → Measure the financial and operational efficiency of resources.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 404, 422).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-945?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer cost, Asset operating cost, Resource replacement cost, Create resource cost, Delete resource cost.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-946` Demand Forecast Accuracy & Planning Performance

**Measure how accurately TICVAI's forecasting and planning engines predicted actual resource demand.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-946 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display; Track) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/demand-forecast-accuracy-planning-performance-bo-946` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read of resource demand forecasts against actual resource use; listDemandBookingCurve is the ticket booking curve.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How accurate resource demand forecasts were against what actually happened.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The only read is the ticket demand forecast (booking curve), not resource demand. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Forecast Demand** (metric tile)

**Planned Resources** (metric tile)

**Actual Demand** (metric tile)

**Actual Resources Used** (metric tile)

**Attendance forecast accuracy** (metric tile)

**Resource demand forecast accuracy** (metric tile)

**Staffing forecast accuracy** (metric tile)

**Equipment forecast accuracy** (metric tile)

**Forecast shortage rate** (metric tile)

**Overstaffing rate** (metric tile)

**Understaffing rate** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **accuracy**: Forecast vs actual by period with the error percentage. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve)*

**Data it reads**: `listDemandBookingCurve` (onLoad, Forecast accuracy)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demand forecast accuracy list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demand forecast accuracy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demand forecast accuracy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demand forecast accuracy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
accuracy:
  period: October 2026
  forecastError: 8.4%
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-946` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-946`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 6: Works in Demand Forecast Accuracy & Planning Performance → Measure how accurately TICVAI's forecasting and planning engines predicted actual resource demand.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-946?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-947` Resource KPI, SLA & Performance Framework

**Allow organizations to define measurable Resource Management performance standards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-947 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Library; Each KPI shall support) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-kpi-sla-performance-framework-bo-947` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where the organisation defines what good looks like: a KPI and SLA library (utilisation, assignment fulfilment, staffing coverage, readiness, equipment availability, downtime, conflict resolution time, replacement time, attendance compliance, overtime, rental return rate, forecast accuracy) with target, warning and critical thresholds, scope, period and owner, and a scorecard of target vs actual. The one thing to get right: each KPI says whether higher or lower is better, so status colours are never inverted.

**Known correction pending (do not draw the wrong version)**

- **The KPI library names and the KPI configuration fields are all drawn as 22 columns of one table** Why: KPI names are rows; configuration fields are a form; the scorecard is its own table. *(source: screens/P08-venue-back-office.yaml#BO-947; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only getResourceUtilisation is bound; no operation stores KPI or SLA definitions or computes actuals** Why: The pack requires configurable KPIs, thresholds and continuous monitoring. *(source: screens/P08-venue-back-office.yaml#BO-947 / contracts/satellite/resources.yaml#getResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI definition**: Name (Arabic variant), description, formula (picked from defined measures, not free text), direction (Higher is better / Lower is better), target, warning and critical thresholds consistent with the direction, applicable venue and resource scope, effective period, owner. *(source: screens/P08-venue-back-office.yaml#BO-947)*
- **SLA**: Event-based target ("Replacement identified within 10 minutes") with the event it measures and the time limit. *(source: screens/P08-venue-back-office.yaml#BO-948)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource kpi sla** (data table)

| Shows | Format | Notes |
|---|---|---|
| Resource utilization | text | not in the schema: `Resource utilization` |
| Assignment fulfillment | text | not in the schema: `Assignment fulfillment` |
| Staffing coverage | text | not in the schema: `Staffing coverage` |
| Resource readiness | text | not in the schema: `Resource readiness` |
| Equipment availability | text | not in the schema: `Equipment availability` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Conflict resolution time | text | not in the schema: `Conflict resolution time` |
| Resource replacement time | text | not in the schema: `Resource replacement time` |
| Attendance compliance | text | not in the schema: `Attendance compliance` |
| Overtime | text | not in the schema: `Overtime` |
| Rental return rate | text | not in the schema: `Rental return rate` |
| Forecast accuracy | text | not in the schema: `Forecast accuracy` |
| Name | text | not in the schema: `Name` |
| Description | text | not in the schema: `Description` |
| Formula | text | not in the schema: `Formula` |
| Target | text | not in the schema: `Target` |
| Warning threshold | text | not in the schema: `Warning threshold` |
| Critical threshold | text | not in the schema: `Critical threshold` |
| Applicable venue | text | not in the schema: `Applicable venue` |
| Applicable resource | text | not in the schema: `Applicable resource` |
| Effective period | text | not in the schema: `Effective period` |
| Owner | text | not in the schema: `Owner` |

**The selected resource kpi sla** (detail panel): The pack groups this record's detail under its own headings: “Target”.

| Shows | Format | Notes |
|---|---|---|
| Resource utilization | text | not in the schema: `Resource utilization` |
| Assignment fulfillment | text | not in the schema: `Assignment fulfillment` |
| Staffing coverage | text | not in the schema: `Staffing coverage` |
| Resource readiness | text | not in the schema: `Resource readiness` |
| Equipment availability | text | not in the schema: `Equipment availability` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Conflict resolution time | text | not in the schema: `Conflict resolution time` |
| Resource replacement time | text | not in the schema: `Resource replacement time` |
| Attendance compliance | text | not in the schema: `Attendance compliance` |
| Overtime | text | not in the schema: `Overtime` |
| Rental return rate | text | not in the schema: `Rental return rate` |
| Forecast accuracy | text | not in the schema: `Forecast accuracy` |
| Name | text | not in the schema: `Name` |
| Description | text | not in the schema: `Description` |
| Formula | text | not in the schema: `Formula` |
| Target | text | not in the schema: `Target` |
| Warning threshold | text | not in the schema: `Warning threshold` |
| Critical threshold | text | not in the schema: `Critical threshold` |
| Applicable venue | text | not in the schema: `Applicable venue` |
| Applicable resource | text | not in the schema: `Applicable resource` |
| Effective period | text | not in the schema: `Effective period` |
| Owner | text | not in the schema: `Owner` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scorecard**: KPI/SLA, Target, Actual, Variance, Trend arrow, Status (green/amber/red) - rows sorted by status, critical first. *(source: screens/P08-venue-back-office.yaml#BO-948 / screens/P08-venue-back-office.yaml#BO-947)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add / Edit KPI**: Opens the definition form; saving starts measuring from the effective date. *(source: screens/P08-venue-back-office.yaml#BO-947)*

**Data it reads**: `getResourceUtilisation` (onLoad, The KPI base)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource kpi sla list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource kpi sla untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource kpi sla yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource kpi sla are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Warning threshold on the wrong side of critical**: Refused against the field ("For Higher is better, warning must be above critical"). *(source: designer default)*

#### Consistency with other screens

- Match `BO-944`: The utilisation target drawn there is this KPI's target.
- Match `BO-943`: Health indicators use these thresholds for their colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
- kpi: Resource assignment fulfilment
  direction: Higher
  target: '>= 98%'
  warning: 95-97.9%
  critical: < 95%
  actual: 98.4%
  status: green
- kpi: Maintenance downtime
  direction: Lower
  target: <= 5%
  actual: 4.2%
  status: green
- kpi: Resource conflicts
  direction: Lower
  target: <= 10
  actual: 12
  status: red
- kpi: Critical replacement time
  direction: Lower
  target: <= 10 min
  actual: 8.4 min
  status: green
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-947` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-947`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 8: Works in Resource KPI, SLA & Performance Framework → Allow organizations to define measurable Resource Management performance standards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-947?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-948` Resource Governance & Policy Center

**Centralize the administrative policies controlling how Resource Management behaves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-948 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-governance-policy-center-bo-948` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One place for the policies that govern resource behaviour (assignment, availability, booking, priority, customer selection, qualification, certification, overtime, maintenance blocking, rental, deposits, replacement, event allocation, AI autonomy, overrides), each with scope, version, effective dates, owner and approval, inherited Global > Tenant > Region > Venue > Category > Resource. The one thing to get right: show for every value whether it is inherited or overridden here ("Automatic staff replacement - Global: Allowed; Venue B: Manager approval required").

**Known correction pending (do not draw the wrong version)**

- **Only the allocation policy is bound, with Save and Cancel; the gap note says nothing is drawable** Why: The pack lists fifteen policy areas, a ten-field policy structure and a six-level hierarchy; one of fifteen has an operation and none has versions, effective dates or inheritance. *(source: screens/P08-venue-back-office.yaml#BO-948 / screens/P08-venue-back-office.yaml#BO-949 / contracts/satellite/resources.yaml#setResourceAllocationPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The allocation policy has no inheritance read** Why: The screen must show inherited versus local values, but the read returns only the venue's effective policy. *(source: contracts/satellite/resources.yaml#getResourceAllocationPolicy / ADR-0018; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policy**: Name, policy area (one of fifteen), scope level and target, effective and expiry dates, owner, approval requirement; the policy's own settings below (e.g. the allocation policy's strategy and weights). *(source: screens/P08-venue-back-office.yaml#BO-948 / screens/P08-venue-back-office.yaml#BO-949)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Active policies**: Table - policy, area, scope, status, version, owner; filter by area. *(source: screens/P08-venue-back-office.yaml#BO-948)*
- **Policy hierarchy**: For a selected policy, the six levels with the value at each, inherited values in grey with "From Tenant", local overrides in bold with Reset to inherited. *(source: screens/P08-venue-back-office.yaml#BO-949 / ADR-0018)*
- **Effective calendar**: Month view of when policy versions start and end (VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-948)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New policy / Save as new version**: Creates a version effective from a date; earlier versions stay in history; approval where required. *(source: screens/P08-venue-back-office.yaml#BO-949)*
- **Open allocation policy**: The resource assignment policy opens its editor (BO-901) and saves through the allocation policy write. *(source: contracts/satellite/resources.yaml#setResourceAllocationPolicy)*

**Data it reads**: `getResourceAllocationPolicy` (onLoad, Policy in force)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource governance policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource governance policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource governance policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource governance policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A venue override contradicts a non-overridable global policy (safety)**: Override control disabled with "Locked at Global - safety". *(source: screens/P08-venue-back-office.yaml#BO-949)*

#### Consistency with other screens

- Match `BO-901`: Same allocation policy record (VO-R14).
- Match `ADM-529`: AI autonomy policy is set in the platform AI governance; show it here read-only with a link.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- name: Staff replacement rule
  area: Resource replacement
  scope: Global
  status: Active
  version: '2.3'
  owner: Operations
- name: Overtime policy
  area: Overtime
  scope: All venues
  version: '1.6'
  owner: HR
- name: Customer selection policy
  area: Customer selection
  scope: Tenant
  version: '1.1'
  owner: Operations
hierarchy: 'Automatic staff replacement - Global: Allowed; Aqua Park: Allowed; Summit Peaks: Manager approval required
  (override)'
```

#### Permissions

- `getResourceAllocationPolicy` → `RESOURCE_VIEW` (read) · staff
- `setResourceAllocationPolicy` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-948` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-948`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 10: Works in Resource Governance & Policy Center → Centralize the administrative policies controlling how Resource Management behaves.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-948?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-949` Approval, Exception & Override Control Center

**Provide one centralized workspace for governed Resource Management exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-949 |
| Who uses it | venue staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each request shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/approval-exception-override-control-center-bo-949` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Resource-management exceptions and overrides waiting for a decision, with operational and financial impact.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: listMemberExceptionOverride (PLATFORM_TENANT_VIEW). (CHG-SBO-005)
- The table's columns are the workshop pack's labels with no bound response field (0 of 10 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Exception type | select | — | Eligibility override · Activation extension · Expiry extension · Complimentary renewal · Complimentary benefit · Entitlement adjustment · Freeze exception · Suspension override · Replacement credential · Renewal exception · Dependent exception | `listMemberExceptionOverride` ?exceptionType |
| Approval status | radio group | — | Pending · Approved · Rejected · Applied | `listMemberExceptionOverride` ?approvalStatus |
| Membership | text field | — | — | `listMemberExceptionOverride` ?membershipId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every approval exception override** (data table)

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| Resource | text | not in the schema: `Resource` |
| Requester | text | not in the schema: `Requester` |
| Venue | text | not in the schema: `Venue` |
| Reason | text | not in the schema: `Reason` |
| Operational impact | text | not in the schema: `Operational impact` |
| Financial impact | text | not in the schema: `Financial impact` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI recommendation` |
| Required approver | text | not in the schema: `Required approver` |

**The selected approval exception override** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Request”, “Issue”.

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| Resource | text | not in the schema: `Resource` |
| Requester | text | not in the schema: `Requester` |
| Venue | text | not in the schema: `Venue` |
| Reason | text | not in the schema: `Reason` |
| Operational impact | text | not in the schema: `Operational impact` |
| Financial impact | text | not in the schema: `Financial impact` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI recommendation` |
| Required approver | text | not in the schema: `Required approver` |

**Data it reads**: `listMemberExceptionOverride` (onLoad, Member Exceptions, Overrides & Service Recovery)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval exception override list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval exception override untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval exception override yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval exception override are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every approval exception override:
- Request: 11
  Resource: 128
  Requester: Rahul Menon
  Venue: AquaCove Abu Dhabi
  Reason: 57
  Operational impact: 312
  Financial impact: 128
  Risk: 3
- Request: 128
  Resource: 46
  Requester: Fatima Al Mansoori
  Venue: AquaCove Dubai
  Reason: 11
  Operational impact: 74
  Financial impact: 46
  Risk: 2
- Request: 46
  Resource: 312
  Requester: Omar Haddad
  Venue: AquaCove Muscat
  Reason: 128
  Operational impact: 19
  Financial impact: 312
  Risk: 0
```

#### Permissions

- `listMemberExceptionOverride` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-949` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-949`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 12: Works in Approval, Exception & Override Control Center → Provide one centralized workspace for governed Resource Management exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-949?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-950` Audit Trail & Resource Decision History

**Provide immutable traceability of significant Resource Management changes and decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-950 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Each event shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/audit-trail-resource-decision-history-bo-950` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The immutable history of material resource decisions - creation, changes, availability, assignment and reassignment, cancellations, overrides, maintenance blocks, rental and deposit actions, event allocation, AI recommendations and executions, approvals and policy changes - each with who, what, when, where, before, after, reason, approval and source. The one thing to get right: the source says whether a person, the Staff App, POS, an API, an integration, an automated rule or TICVAI AI started it, and AI lines link to their reasoning.

**Known correction pending (do not draw the wrong version)**

- **The fifteen event kinds and nine record fields are drawn as 23 selectFields** Why: Event kinds are filter chips; record fields are table columns and the detail panel. *(source: screens/P08-venue-back-office.yaml#BO-950; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The only read is per resource (opened with a resourceId), with no search** Why: The pack searches by employee, event, user, date, action, venue and source across all resources. *(source: screens/P08-venue-back-office.yaml#BO-951 / contracts/satellite/resources.yaml#getResourceAuditTrail; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The audit entry has no approval and no explicit initiator type** Why: The pack requires the approval and that AI-executed actions are distinguishable from manual ones; sourceChannel is free text. *(source: screens/P08-venue-back-office.yaml#BO-932 / contracts/satellite/resources.yaml#/components/schemas/ResourceAuditEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource creation | select field | — | — | — | — | — | — |
| Resource modification | select field | — | — | — | — | — | — |
| Availability change | select field | — | — | — | — | — | — |
| Assignment | select field | — | — | — | — | — | — |
| Reassignment | select field | — | — | — | — | — | — |
| Cancellation | select field | — | — | — | — | — | — |
| Staff override | select field | — | — | — | — | — | — |
| Maintenance block | select field | — | — | — | — | — | — |
| Rental transaction | select field | — | — | — | — | — | — |
| Deposit adjustment | select field | — | — | — | — | — | — |
| Event allocation | select field | — | — | — | — | — | — |
| AI recommendation | select field | — | — | — | — | — | — |
| AI execution | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Policy change | select field | — | — | — | — | — | — |
| Who | select field | — | — | — | — | — | — |
| What | select field | — | — | — | — | — | — |
| When | select field | — | — | — | — | — | — |
| Where | select field | — | — | — | — | — | — |
| Previous Value | select field | — | — | — | — | — | — |
| New Value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Source | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Search by resource, employee, event, user, date range, action, venue and source; chips for the fifteen event kinds and seven sources. *(source: screens/P08-venue-back-office.yaml#BO-951)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Audit table**: Date/time, User (or System / TICVAI AI), Action, Resource and details ("Maria Santos - Private lesson Zone A -> Group lesson Zone B"), Source; newest first, cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-950)*
- **Entry detail**: Before and after side by side, reason, approval (approved by, when), correlation id; for AI-initiated entries "Initiated by TICVAI AI recommendation, approved by Operations Manager" and a link to the decision trace. *(source: screens/P08-venue-back-office.yaml#BO-951 / contracts/satellite/resources.yaml#/components/schemas/ResourceAuditEntry / contracts/satellite/ai.yaml#getAiDecisionTrace)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export**: CSV/PDF of the filter, permission-checked and itself audited. *(source: screens/P08-venue-back-office.yaml#BO-950)*

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit trail resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit trail resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit trail resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Entry from an action made offline**: Shows when it happened on the device and when it synced. *(source: contracts/satellite/resources.yaml#setResourceBookingProgress)*
- **Viewer without audit rights**: "Needs audit access" empty state (VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-592`: The rental audit log is a filtered view of this table.
- Match `BO-863`: The per-resource audit timeline uses the same entries.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- at: 10 Oct 2026 09:41
  user: Fatima Al Hashimi
  action: Assignment changed
  details: Maria Santos - Private lesson Zone A -> Group lesson Zone B
  source: Back office
- at: 10 Oct 2026 09:37
  user: TICVAI AI
  action: Recommendation
  details: Reallocate 4 instructors Zone B -> Zone A
  source: AI engine (approved by Ahmed Al Mansoori)
- at: 10 Oct 2026 09:30
  user: System
  action: Resource status
  details: Projector P-17 -> Under maintenance
  source: Integration
```

#### Permissions

- `getResourceAuditTrail` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-950` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-950`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 14: Works in Audit Trail & Resource Decision History → Provide immutable traceability of significant Resource Management changes and decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-950?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-951` Resource Integration & System Health Center

**Monitor all technical integrations and synchronization services supporting Resource Management.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-951 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-integration-system-health-center-bo-951` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Health of the integrations that feed resource management (HR system, workforce provider, booking sync): last success, failures, records affected and what that failure means operationally.

**Known correction pending (do not draw the wrong version)**

- **The screen reads the analytics data pipelines (feeds into the reporting replica), not the resource integrations it describes.** Why: Wrong source; it also duplicates P16's pipeline monitor. *(source: contracts/satellite/reporting.yaml#listAnalyticsPipelines / screens/P16-venue-analytics.yaml#ANL-067; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource integration system** (data table)

| Shows | Format | Notes |
|---|---|---|
| System | text | not in the schema: `System` |
| Status | text | not in the schema: `Status` |
| Last sync | text | not in the schema: `Last Sync` |
| Transactions | text | not in the schema: `Transactions` |
| Errors | text | not in the schema: `Errors` |
| Latency | text | not in the schema: `Latency` |

**The selected resource integration system** (detail panel): The pack groups this record's detail under its own headings: “Potential connections include”, “HRMS”, “Workforce Provider”, “Operational Impact”, “It should explain”.

| Shows | Format | Notes |
|---|---|---|
| System | text | not in the schema: `System` |
| Status | text | not in the schema: `Status` |
| Last sync | text | not in the schema: `Last Sync` |
| Transactions | text | not in the schema: `Transactions` |
| Errors | text | not in the schema: `Errors` |
| Latency | text | not in the schema: `Latency` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Retry, View error, Inspect payload/reference, Reprocess, Escalate, Open affected records. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listAnalyticsPipelines` (onLoad, Integration and data health)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource integration system list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource integration system untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource integration system yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource integration system are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- HR system roster sync · failed 03:00 · 214 records not updated · tomorrow's roster may miss 6 new starters
```

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-951` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-951`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 16: Works in Resource Integration & System Health Center → Monitor all technical integrations and synchronization services supporting Resource Management.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-951?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-952` Executive Resource Intelligence & AI Improvement Center

**Complete the Resource Management module with an executive AI workspace that converts operational data into management recommendations. This should be the hero screen of Board 10.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-952 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Track) and a per-row directory (§Each recommendation shall show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/executive-resource-intelligence-ai-improvement-center-bo-952` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The executive AI workspace that closes the module: ask "How did our resources perform this month?" and get the headline numbers, AI findings and recommended actions with evidence, confidence, expected benefit, risk, affected resources and financial and operational impact; plus how the AI itself is performing (recommendations generated, accepted, rejected, savings predicted vs realised). The one thing to get right: management reviews, simulates, assigns an owner or dismisses - the AI never makes a strategic change by itself.

**Known correction pending (do not draw the wrong version)**

- **The seven governance fields are drawn as columns of a table titled "Every executive resource intelligence"** Why: They are a strip on each recommendation card. *(source: screens/P08-venue-back-office.yaml#BO-952; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only getResourceUtilisation is bound; the nine AI performance tiles and the findings have no source** Why: Insights, their decisions and forecast accuracy live in the AI contract (listAiInsights, decideAiInsight, getForecastAccuracy) and are not bound. *(source: contracts/satellite/ai.yaml#listAiInsights / contracts/satellite/ai.yaml#decideAiInsight / contracts/satellite/ai.yaml#getForecastAccuracy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Executive question**: A question box with suggested questions; the answer is a structured summary, not free chat. *(source: screens/P08-venue-back-office.yaml#BO-952)*
- **Period**: Month selector (default last full month). *(source: screens/P08-venue-back-office.yaml#BO-952)*

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations generated** (metric tile)

**Recommendations accepted** (metric tile)

**Recommendations rejected** (metric tile)

**Auto-actions executed** (metric tile)

**Forecast accuracy** (metric tile)

**Optimization savings predicted** (metric tile)

**Optimization savings realized** (metric tile)

**Replacement success** (metric tile)

**Conflict-resolution success** (metric tile)

**Every executive resource intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| Evidence | text | not in the schema: `Evidence` |
| Confidence | text | not in the schema: `Confidence` |
| Expected benefit | text | not in the schema: `Expected benefit` |
| Risk | text | not in the schema: `Risk` |
| Affected resources | text | not in the schema: `Affected resources` |
| Financial impact | text | not in the schema: `Financial impact` |
| Operational impact | text | not in the schema: `Operational impact` |

**The selected executive resource intelligence** (detail panel): The pack groups this record's detail under its own headings: “Executive Question”, “Overall Utilization”, “Resource Readiness”, “Assignment Fulfillment”, “Overtime”, “Resource-Related Cost”.

| Shows | Format | Notes |
|---|---|---|
| Evidence | text | not in the schema: `Evidence` |
| Confidence | text | not in the schema: `Confidence` |
| Expected benefit | text | not in the schema: `Expected benefit` |
| Risk | text | not in the schema: `Risk` |
| Affected resources | text | not in the schema: `Affected resources` |
| Financial impact | text | not in the schema: `Financial impact` |
| Operational impact | text | not in the schema: `Operational impact` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Performance summary**: Overall utilisation with change, readiness, assignment fulfilment, forecast accuracy, overtime change, resource-related cost change - tiles (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-952)*
- **Findings and recommended actions**: Cards with an impact tag (High, Medium, Low), the finding, the action and expected effect ("Replace projectors P-17, P-22, P-31 - AED 18,400 a year less maintenance"), and a governance strip Evidence / Confidence / Expected benefit / Risk / Affected resources / Financial impact / Operational impact. *(source: screens/P08-venue-back-office.yaml#BO-952)*
- **AI performance**: Tiles Recommendations generated, Accepted %, Rejected %, Expired/no action %, Auto-actions executed, Forecast accuracy, Savings predicted, Savings realised (validated), Replacement success, Conflict-resolution success. *(source: screens/P08-venue-back-office.yaml#BO-952)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Review / Simulate / Create action / Assign owner / Dismiss**: Dismiss asks for a reason (it is the signal that judges the recommender); Create action assigns an owner and a due date; nothing changes resources directly. *(source: screens/P08-venue-back-office.yaml#BO-952 / contracts/satellite/ai.yaml#decideAiInsight)*

**Data it reads**: `getResourceUtilisation` (onLoad, Executive resource view)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The executive resource intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the executive resource intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No executive resource intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the executive resource intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Savings not yet measured**: Realised shows "Measuring - available after 30 days" instead of zero. *(source: contracts/satellite/ai.yaml#decideAiInsight)*

#### Consistency with other screens

- Match `BO-923`: Same recommendation card and governance strip.
- Match `ANL-019`: The platform's AI management insights use the same insight lifecycle (new, reviewed, accepted/rejected, actioned, measured).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
month: September 2026
summary:
  utilisation: 78% (+6%)
  readiness: 96%
  fulfilment: 98.4%
  forecastAccuracy: 92%
  overtime: -14%
  cost: +4.8%
findings:
- impact: High
  finding: Level 3 instructors above 90% utilisation on four weekends
  action: Increase Level 3 capacity
  effect: +8% peak availability
- impact: Medium
  finding: Three projectors account for 41% of AV maintenance spend
  action: Replace P-17, P-22, P-31
  effect: AED 18,400 a year
aiPerformance:
  recommendations: 1,284
  accepted: 81%
  rejected: 12%
  expired: 7%
  forecastAccuracy: 92.4%
  predicted: AED 148,000
  validated: AED 121,000
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-952` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-952`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 18: Works in Executive Resource Intelligence & AI Improvement Center → Complete the Resource Management module with an executive AI workspace that converts operational data into management recommendations. This should be the hero screen of Board 10.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-952?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createResourceCost": {"method":"POST","path":"/resource-costs","contract":"resources","summary":"Book a transfer, operating or replacement cost against a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCostEntry","responds":"ResourceCostEntry"},
"deleteResourceCost": {"method":"DELETE","path":"/resource-costs/{costId}","contract":"resources","summary":"Remove a cost entry booked in error","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getResourceAllocationPolicy": {"method":"GET","path":"/resource-allocation-policy","contract":"resources","summary":"How the platform chooses between equally valid resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAllocationPolicy"},
"getResourceAuditTrail": {"method":"GET","path":"/resources/{resourceId}/audit","contract":"resources","summary":"Every material change, with who and why","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAuditEntry"},
"getResourceCostAnalytics": {"method":"GET","path":"/resource-cost-analytics","contract":"resources","summary":"What resources cost and earn, grouped","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceCostAnalytics"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMemberExceptionOverride": {"method":"GET","path":"/member-exception-override","contract":"subscription","summary":"Member Exceptions, Overrides & Service Recovery","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"exceptionType","in":"query","required":false},{"name":"approvalStatus","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResourceCosts": {"method":"GET","path":"/resource-costs","contract":"resources","summary":"Cost entries booked against resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"setResourceAllocationPolicy": {"method":"PUT","path":"/resource-allocation-policy","contract":"resources","summary":"Rotation, priority and scoring","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceAllocationPolicy","responds":"ResourceAllocationPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"MemberExceptionsOverridesServiceRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Member Exceptions, Overrides & Service Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"member":{"type":"string","description":"Member"},"membership":{"type":"string","description":"Membership"},"requestedAction":{"type":"string","description":"Requested Action"},"standardPolicyResult":{"type":"string","description":"Standard Policy Result"},"requestedException":{"type":"string","description":"Requested Exception"},"reason":{"type":"string","description":"Reason"},"supportingDocumentation":{"type":"array","items":{"type":"string"},"description":"Supporting Documentation: document ids"},"financialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Financial Impact of the exception"},"entitlementImpact":{"type":"string","description":"Entitlement Impact"},"requestor":{"type":"string","description":"Requestor"},"exceptionType":{"type":"string","enum":["eligibilityOverride","activationExtension","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential","renewalException","dependentException"],"description":"Exception Type (pack p.32)"},"exceptionValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Value used for approval routing"},"durationDays":{"type":"integer","description":"Duration in days, for extensions","nullable":true},"membershipTier":{"type":"string","description":"Membership Tier"},"exceptionId":{"type":"string","description":"Exception ID"},"approvalStatus":{"type":"string","description":"Approval status: pending, approved, rejected or applied"},"approver":{"type":"string","description":"Approver; must differ from the requestor for high-value exceptions","nullable":true},"remedy":{"type":"string","enum":["extendMembership","guestTicket","complimentaryVisit","feeWaiver","benefitCredit","renewalDiscount","alternativeEntitlement"],"description":"Service Recovery remedy (pack p.33)","nullable":true},"aiSuggestion":{"type":"string","description":"AI suggestion, advisory","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceAllocationPolicy": {"type":"object","x-ticvai-persistence":"resources.allocation_policy","description":"Board 5.08, and the 26 August rotation decision. **Named rather than hidden in the allocator**, so somebody can answer why cabana three never gets used.\n","properties":{"strategy":{"type":"string","enum":["rotate","leastUtilised","priorityOrder","nearestFirst"],"default":"rotate","description":"**`rotate` is the default because 26 August made it one.** *\"rotate across all available resources… rather than repeatedly reusing the same resource, to avoid overburdening any single resource while others remain unused.\"*\n"},"respectResourcePriority":{"type":"boolean","default":true},"scoringWeights":{"type":"object","additionalProperties":{"type":"number"}},"allowPartialAllocation":{"type":"boolean","default":false,"description":"**False by default.** A stage allocated without its sound system is worse than no allocation, because it looks finished.\n"},"scopePath":{"type":"string"}}},
"ResourceAuditEntry": {"type":"object","x-ticvai-persistence":"resources.resource_audit","description":"Board 1.10. **Immutable, and it carries the previous value.**","properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"actorId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"field":{"type":"string","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"sourceChannel":{"type":"string","nullable":true},"apiOrigin":{"type":"string","nullable":true},"correlationId":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceCostAnalytics": {"type":"object","x-ticvai-persistence":"none — projection over resources.resource_cost, bookings and maintenance work orders, computed at read time","description":"One group's cost and revenue for the window (decided 29 September, readiness close-out; BO-945).","required":["key","label"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"transferCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"operatingCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"replacementCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"bookedHours":{"type":"number"},"costPerBookedHour":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total cost over booked hours; null when nothing was booked."}}},
"ResourceCostEntry": {"type":"object","x-ticvai-persistence":"resources.resource_cost","description":"**One cost booked against a resource**: a transfer between locations, an operating cost or a replacement. `getResourceCostAnalytics` sums these per group and window (decided 29 September, data model DM4).\n","required":["id","resourceId","kind","amount","incurredOn"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"resourceId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["transfer","operating","replacement"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incurredOn":{"type":"string","format":"date"},"fromVenueId":{"type":"string","format":"uuid","nullable":true,"description":"A `transfer` only, with `toVenueId`."},"toVenueId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}}
}
```
