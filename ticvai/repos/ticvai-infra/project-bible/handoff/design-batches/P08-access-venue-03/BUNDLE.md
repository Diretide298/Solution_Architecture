# P08-access-venue-03 — P08 · Access & Venue (3 of 3)

**5 screens · 15 operations · 24 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, RENTAL_VIEW, REPORT_VIEW_VENUE, RESOURCE_BOOK, RESOURCE_MANAGE, RESOURCE_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-096` | Resource Calendar | A | 10 | 11 | 6 | 27 | 3 | 0 | — | notStarted (generated) |
| `BO-097` | Check Out & Check In | A | 24 | 20 | 5 | 25 | 0 | 0 | — | notStarted (generated) |
| `BO-098` | Qualifications | D | 15 | 7 | 5 | 9 | 0 | 0 | — | notStarted (generated) |
| `BO-099` | Performance Manifest | D | 2 | 8 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-103` | Access & Venue | C | 2 | 22 | 6 | 13 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-096` Resource Calendar

**See what is free, and book it without double-booking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `resources` module |
| Block | Block A · task VM-BO-096 |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getResourceAvailability` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `resourceId` (BO-095) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/resources/calendar` |

**What the spec says about it.** CF-125. **Conflict detection before assignment is the whole point** — two bookings on one cabana is a guest arriving to find somebody in their chair, and it must be impossible rather than unlikely.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The resource calendar: each resource's bookings, holds, blocks, setup/teardown and cleaning bands on Day, Week, Month and Agenda views, and staff booking of a resource without double-booking. Normally resources are booked automatically by selling a product; booking here is for exceptions. The one thing to get right: setup, teardown and cleaning render as their own bands, so a 30-minute turnaround is visible.

**Fixed on main** (the package already carries these; draw what it says): Two primary buttons (Book and Book resource) and an unbound timeline (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceAvailability` ?from |
| To | date and time picker | — | — | `getResourceAvailability` ?to |

**Form: Book resource** (modal, opened by *Book resource*; *Book resource* calls `bookResource`, *Cancel* sends nothing)

**Collects what `bookResource` sends before it is called.** Required: `from`, `to`. Optional: `resourceId`, `resourceKind`, `subjectId`, `orderId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resource `resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | — | `bookResource` body |
| Resource kind `resourceKind` | select | optional | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | — | Supplied instead of `resourceId` when the caller does not care which one; the platform picks and the response names it. | `bookResource` body |
| From `from` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `bookResource` body |
| To `to` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `bookResource` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `bookResource` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | — | `bookResource` body |
| Recurrence `recurrence` | group | optional | — | — | — | A weekly swimming lesson is one booking, not twelve. Conflict detection runs across every occurrence before any of them is written — booking eight of twelve failing after seven … | `bookResource` body |
| Pattern `recurrence.pattern` | segmented control | optional | — | Daily · Weekly · Monthly | — | — | `bookResource` body |
| Days of week `recurrence.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `bookResource` body |
| Until `recurrence.until` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `bookResource` body |

Errors to draw in the form: 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View and window**: Day (hour rows from the venue's day start), Week, Month, Agenda; date navigator with Today; filter by resource kind and category. *(source: DI-919 / contracts/satellite/resources.yaml#getResourceAvailability)*
- **Book resource**: Window (from-to), guest or booking reference, party size, note; the platform picks a specific free unit when booking by kind and says which. *(source: contracts/satellite/resources.yaml#bookResource / F25 step 3)*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getResourceAvailability`): Each resource's bookings, blocks and cleanings placed by hour. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |
| Free windows | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Blocked windows | list or chips (count when long) | With a reason, because they are not the same. Booked and under repair need different responses from an operator looking for something free … |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Reason | chip: Booked, Held, Setup, Teardown, Maintenance, Blackout… | `held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. |

**The resource availability** (detail panel, from `getResourceAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |
| Free windows | list or chips (count when long) | — |
| Blocked windows | list or chips (count when long) | With a reason, because they are not the same. Booked and under repair need different responses from an operator looking for something free … |

**Timeline** (timeline): Setup and teardown render as their own bands, not as part of the booking — **a 30-minute turnaround is invisible if it is drawn inside the booking**

**Banner** (banner): Conflicts, named with times. *Not available* on something a guest can see is not an answer

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Book resource (primary button) | `bookResource` POST `/resource-bookings` | inline | ResourceBooking | 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem) | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Calendar bands**: Booking (solid, guest name), hold (striped, expires time), block (grey, reason), setup/teardown (thin hatched before/after), cleaning (dotted), conflicts (red outline). *(source: screens/P08-venue-back-office.yaml#BO-096 / DI-1012 / contracts/satellite/resources.yaml#getResourceAvailability)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Book**: Refused on conflict including setup and teardown; the conflict banner names the clashing booking and its times. *(source: F25 step 3 / DI-484)*

**Data it reads**: `getResourceAvailability` (onLoad, Free windows)

**Where the user goes next**

- → `BO-097` Check Out & Check In: *The guest arrives;*; carries `bookingId`; calls `bookResource`
- → `BO-099` Performance Manifest: *Performance Manifest*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Calendar grid; today renders first |
| Error (`?state=error`) | Could not load availability. **Do not book blind** — a booking made against a stale calendar is the double-booking this screen exists to prevent. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing booked in this window. **Free is the default state and it is worth showing plainly** — an empty calendar at a venue that takes bookings is either a quiet week or a resource nobody knows exists. |
| Empty, no results (`?state=emptyNoResults`) | No availability in this window. The response says why — booked, setup, teardown, maintenance or closed — because **wait and look elsewhere are different answers**. |
| Permission denied (`?state=emptyNoAccess`) | You do not have `RESOURCE_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_BOOK` for `bookResource`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem) |

#### Edge cases to draw

- **Exceptional manual booking**: A note reminds that resources are normally booked by selling the product; manual booking needs a reason. *(source: DI-483)*

#### Consistency with other screens

- Match `BO-864`: The resource calendar command centre uses the same calendar component and colours.
- Match `WEB-047`: Guest map holds show as holds here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day: Sat 10 Oct 2026 (day starts 06:00)
rows:
- resource: Cabana B09
  bands: Setup 09:30-10:00, Booking 10:00-17:00 Sara Al Nuaimi, Cleaning 17:00-17:15
- resource: Meeting Room A
  bands: Booking 09:00-12:00 Yas Corporate, Teardown 12:00-12:30, Free 12:30-18:00
```

#### Permissions

- `getResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `bookResource` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** You do not have `RESOURCE_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_BOOK` for `bookResource`.

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.6 | The system should provide a calendar view for all the resources (e.g. instructors) and associated time slots (e.g. ski school session by an instructor). The calendar should support application of … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.7 | The system should show the booked capacity of different time-slots to provide their availability. The capacity can be color-coded to indicate if not busy, moderately busy, or crowded within each … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.13 | Using the calendar view, system should provide an drag and drop interface to reassign the resources from one resource to another available resources. System should automatically assign the next … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.18 | Resource Calendar: Centralized calendar view (daily/weekly/monthly). | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.19 | Availability Management: Check conflicts before assigning resources. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.20 | Recurring Reservations: Block resources for repeated sessions/shows. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.21 | Time Slot Management: Allocate setup, event, teardown, and maintenance times. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.22 | Multi-event Handling: Manage shared resources across parallel events. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.27 | System shall provide centralized resource calendars. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.28 | System shall manage resource time slots and availability. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.29 | System shall manage availability and conflict detection. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.30 | System shall support advance resource reservations. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-096` · status **notStarted** · provenance generated
- Flow F25 *A guest rents a cabana*, step 2: The attendant checks what is free for the requested window. → Free windows, with setup and teardown already subtracted. **A cabana booked until 16:00 with a 30-minute turnaround is not free at 16:00**, and a client computing this from bookings would have …
- Flow F25 *A guest rents a cabana*, step 3: The attendant books it, without choosing which one. → The platform picks a specific cabana and says which. **Refused on conflict, including setup and teardown** — this is the step the whole context exists for.
- Flow F25 branch at step 2 (recoverable): when Nothing is free in the requested window., The response says **why** — booked, setup, teardown, maintenance or closed. An attendant looking for something free needs to know whether to wait or to look elsewhere, and *"not available"* answers …
- Flow F25 branch at step 3 (recoverable): when Two attendants book the same cabana in the same second., One wins and the other is refused with the conflicting window named. **Two bookings on one cabana is a guest arriving to find somebody in their chair**, so this is refused at the server and never …
- Flow F25 branch at step 5 (requiresStaff): when Nobody brings it back., The booking goes `overdue` on a timer, which is **not a failure state** — a guest running late is the normal case and the deposit is already held. Past a threshold the whole deposit captures and …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-096?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Book resource.
- [ ] Every transition is wired: `BO-097`, `BO-099`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-097` Check Out & Check In

**Hand it over with a deposit, take it back, settle.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `resources` module |
| Block | Block A · task VM-BO-097 |
| Who uses it | venue staff holding `ORDER_CREATE`, `RENTAL_VIEW`, `RESOURCE_BOOK` (2 operate, 1 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`checkOutResource`, `checkInResource`, `authoriseStoredValue`) and no read of a population — it is settings, not a list |
| Offline | Queued locally. The deposit is authorised on sync, and **the condition note taken now is the only defence against a dispute later**. |
| Opens with | `authorisationId` (deepLink), `bookingId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/resources/check-out` |

**What the spec says about it.** CF-125, CF-126. **The deposit is held, not taken** — a deposit taken and refunded is two transactions and a fee. **Damage routes the resource to maintenance directly**, because routing through available leaves a window where the next guest books a broken item. **The deposit operations are declared here because this screen calls them** — F25 named them at steps 4 and 5 and the screen did not, which the flow checker refused. **A step calling an operation its screen does not declare is one of the two out of step**, and in this case it was the screen.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Hand a rental over and take it back: check out with a deposit held (not taken) against the item, check in with its condition, then release the hold or capture part of it for damage. Damage sends the item to maintenance directly so the next guest cannot book a broken one.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only checkOutResource, checkInResource, authoriseStoredValue, relinquishStoredValue … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| amount | text field | optional | — | pattern `^-?\d+(\.\d{1,4})?$` | — | Decimal string, never a float. Up to 4 decimal places. | `Money.amount` |
| currency | text field | optional | — | pattern `^[A-Z]{3}$` | — | Resolved from the region, not stored on the row (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate. | `Money.currency` |
| scale | stepper or slider | optional | — | min 0; max 4 | — | Resolved from the region alongside `currency`. | `Money.scale` |
| Condition note | text field | — | — | — | — | — | — |
| Condition photos | file upload | — | — | — | — | Taken on the way out, not only on the way back | — |

**Form: Capture stored value** (modal, opened by *Capture stored value*; *Capture stored value* calls `captureStoredValue`, *Cancel* sends nothing)

**Collects what `captureStoredValue` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `captureStoredValue` body |

Errors to draw in the form: 409 The hold is no longer live — `captured`, `released` or `expired` (`authorisationNotHeld`) — or the amount is more than what remains held (`aboveHeldAmount`). (StoredValueProblem)

**Form: Check in resource** (modal, opened by *Check in resource*; *Check in resource* calls `checkInResource`, *Cancel* sends nothing)

**Collects what `checkInResource` sends before it is called.** Required: `condition`, `recordedAt`. Optional: `captureAmount`, `note`, `blockFurtherBookings`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Condition `condition` | radio group | required | — | Good · Minor damage · Major damage · Not returned | — | — | `checkInResource` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device took it back, not when the write reached the server. Stored as the booking's `returnedAt`, so an overdue charge is judged against the counter time rather than the … | `checkInResource` body |
| Capture amount `captureAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `checkInResource` body |
| Note `note` | text area | optional | — | — | — | — | `checkInResource` body |
| Block further bookings `blockFurtherBookings` | toggle | optional | off | — | — | Blocks a `good` return from further booking too. Ignored for a damaged return, which always blocks until inspected (audit R106 (4)). | `checkInResource` body |

**Form: Authorise stored value** (modal, opened by *Authorise stored value*; *Authorise stored value* calls `authoriseStoredValue`, *Cancel* sends nothing)

**Collects what `authoriseStoredValue` sends before it is called.** Required: `kind`, `instrumentId`, `amount`. Optional: `reference`, `holdSeconds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Wallet · Gift card · Game card · Voucher · Loyalty · Prepaid entitlement | — | Six things in this package hold a balance and behave the same way — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. | `authoriseStoredValue` body |
| Instrument `instrumentId` | picker: choose an instrument | required | — | — | shows names, sends the id | — | `authoriseStoredValue` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `authoriseStoredValue` body |
| Reference `reference` | text field | optional | — | — | — | — | `authoriseStoredValue` body |
| Hold seconds `holdSeconds` | number field (seconds) | optional | 300 | — | — | An arcade play is seconds and a table tab is hours. Held balance is balance a guest cannot spend elsewhere, so the window belongs to the caller. | `authoriseStoredValue` body |

Errors to draw in the form: 409 Insufficient balance after existing holds. The reason says which — the balance itself is too low (`insufficientBalance`), or enough is there but other holds … (StoredValueProblem)

**Sent by *Check out resource*** (`checkOutResource`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `checkOutResource` body |
| Deposit amount `depositAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `checkOutResource` body |
| Deposit instrument `depositInstrument` | select | optional | — | Wallet · Gift card · Game card · Voucher · Loyalty · Prepaid entitlement | — | Six things in this package hold a balance and behave the same way — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. | `checkOutResource` body |
| Deposit instrument `depositInstrumentId` | picker: choose a deposit instrument | optional | — | Required whenever `depositAmount` is supplied. | shows names, sends the id | Which wallet, card, voucher or position the deposit is held against. `depositInstrument` says what kind it is and this says which one — the pair is `kind` and `instrumentId` on … | `checkOutResource` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device handed it over, not when the write reached the server. This operation is offline-capable, and a check-out replayed from the outbox an hour later still went out at … | `checkOutResource` body |
| Condition note `conditionNote` | text field | optional | — | — | — | — | `checkOutResource` body |
| Condition photo refs `conditionPhotoRefs` | list of values (chips) | optional | — | — | — | — | `checkOutResource` body |
| Due back at `dueBackAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `checkOutResource` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **deposit hold**: Instrument (card, TICVAI wallet, gift card) and amount; shown as "held until" with the hold expiry. *(source: contracts/spine/orders.yaml#authoriseStoredValue / F25 step 4)*
- **check-in condition**: Condition (good, minor wear, damaged, missing), capture amount only when not good, note, and "block further bookings" pre-ticked when damaged. *(source: contracts/satellite/resources.yaml#checkInResource / F25 step 5)*

#### Outputs: what the screen shows and produces

**Shown**

**One booking, its timeline and its readiness** (detail panel, from `getRentalBooking`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Reference | text | — |
| Product | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Return location | the name it points at, never the id | — |
| Customer | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Quantity | 1,234 | — |
| Status | chip: Draft, Confirmed, Awaiting arrival, Checked out, Overdue, Partially returned… | — |
| Checked out at | 1 Oct 2026, 14:30 | — |
| Due back at | 1 Oct 2026, 14:30 | — |
| Returned at | 1 Oct 2026, 14:30 | — |
| Deposit authorisation | the name it points at, never the id | The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). |
| Accrued late fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Readiness | list or chips (count when long) | Computed, not stored — agreement, requirements, deposit, equipment. |
| Check | text | — |
| Satisfied | yes / no (icon or chip) | — |
| Detail | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Check out (primary button) | navigation or local | — | — | — | — |
| Check in (secondary button) | navigation or local | — | — | — | — |
| Check out resource (primary button) | `checkOutResource` POST `/resource-bookings/{bookingId}/check-out` | inline | ResourceBooking | — | — |
| Check in resource (secondary button) | `checkInResource` POST `/resource-bookings/{bookingId}/check-in` | inline | ResourceBooking | — | opens modal first |
| Authorise stored value (secondary button) | `authoriseStoredValue` POST `/stored-value/authorisations` | inline | StoredValueAuthorisation | 409 Insufficient balance after existing holds. The reason says which — the balance itself is too low (`insufficientBalance`), or enough is there but other holds … (StoredValueProblem) | opens modal first |
| Release stored value (secondary button) | `relinquishStoredValue` POST `/stored-value/authorisations/{authorisationId}/release` | — | StoredValueAuthorisation | 409 Nothing is held to release — the hold is already `captured`, `released` or `expired` (`authorisationNotHeld`). (StoredValueProblem) | — |
| Capture stored value (secondary button) | `captureStoredValue` POST `/stored-value/authorisations/{authorisationId}/capture` | inline | StoredValueAuthorisation | 409 The hold is no longer live — `captured`, `released` or `expired` (`authorisationNotHeld`) — or the amount is more than what remains held (`aboveHeldAmount`). (StoredValueProblem) | opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Check in**: Releases the hold or captures part of it; the remainder is released in the same act and the result says both amounts. *(source: contracts/spine/orders.yaml#captureStoredValue / contracts/spine/orders.yaml#relinquishStoredValue)*

**Data it reads**: `getRentalBooking` (onLoad, One booking, its timeline and its readiness)

**Where the user goes next**

- → `BO-096` Resource Calendar: *Resource Calendar*; carries `resourceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking and its condition history |
| Error (`?state=error`) | Could not load. **Check-out and check-in work offline** — the deposit hold reconciles on sync. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing is out. **The list a poolside attendant checks at close** — anything still here at the end of the day is a conversation. |
| Permission denied (`?state=emptyNoAccess`) | Without `RENTAL_VIEW`, which `getRentalBooking` requires, the screen does not load and this state names that permission. You do not have `RESOURCE_BOOK`. |
| Offline (`?state=offline`) | Queued locally. The deposit is authorised on sync, and **the condition note taken now is the only defence against a dispute later**. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient balance after existing holds. The reason says which — the balance itself is too low (`insufficientBalance`), or enough is there but other holds … (StoredValueProblem); 409 Nothing is held to release — the hold is already `captured`, `released` or `expired` (`authorisationNotHeld`). (StoredValueProblem); 409 The hold is no longer live — `captured`, `released` or `expired` … |

#### Edge cases to draw

- **Item overdue**: Booking shows Overdue with the due-back time; check-in still works and the late fee, if any, is a separate charge. *(source: contracts/satellite/resources.yaml#checkOutResource)*
- **Hold expired before return**: Say the hold has lapsed and offer a new authorisation before capture. *(source: contracts/spine/orders.yaml#relinquishStoredValue)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking:
  item: Cabana B09, Coastal Aqua
  guest: Omar Haddad / عمر حداد
  out: 2026-11-14 10:00
  due: 2026-11-14 14:00
  deposit: AED 300.00 held on Visa •••• 2210
checkIn:
  condition: minor wear
  capture: AED 0.00
  released: AED 300.00
```

#### Permissions

- `checkOutResource` → `RESOURCE_BOOK` (operate) · staff
- `checkInResource` → `RESOURCE_BOOK` (operate) · staff
- `authoriseStoredValue` → `ORDER_CREATE` (operate) · staff, guest, device
- `relinquishStoredValue` → `ORDER_CREATE` (operate) · staff, device
- `captureStoredValue` → `ORDER_CREATE` (operate) · staff, device
- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Without `RENTAL_VIEW`, which `getRentalBooking` requires, the screen does not load and this state names that permission. You do not have `RESOURCE_BOOK`.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.8 | The system should allow check out & check in feature for rental resources. For example, towels in the water park. Inventory management of these resources should be handled in the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.9 | The system should allow configuration of deposit requirement for rental resources. The collection and return of the deposit at the time of check-in and check-out should be handled within the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.10 | The system should allow linking of a checked-out resource object to a guest profile. Specification of a rental time period for a checked-out resource object should be supported. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 7.4.10 | The system can manage Cabins rental | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.36 | Lockers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.37 | Wheelchairs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.38 | Strollers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.51 | Track serial numbers for RFID wristbands, devices, lockers, tablets and rental assets. Record assignment, location, status and movement history. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.52 | Manage deposits for rented assets such as lockers, strollers, wheelchairs and equipment. Support collection, refund, partial refund and forfeiture workflows. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.1 | Functional Requirements Ability to create and manage rental products (Bike, Kayak, Watercraft, Stroller, Cabana, Locker, Wheelchair, etc.). Configure: - Product Code - Product Name - Description - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.2 | Serial Number Management Support unique serial number assignment for each rental item. Ability to: - Create serial numbers - Activate/Deactivate serial numbers Mark item as: - Available - Rented - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.3 | Functional Requirements Real-time inventory tracking. Maintain available inventory by: - Product - Date - Time Slot - Location Automatically reduce inventory upon reservation. Automatically restore … | F&B POS | CONTRACTED | `checkOutResource` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-097` · status **notStarted** · provenance generated
- Flow F25 *A guest rents a cabana*, step 4: The guest arrives; the attendant hands it over and holds a deposit. → **The deposit is held, not taken.** A deposit taken and refunded is two transactions and a fee; held and released is neither, and a guest who returns a lounger intact should not wait three days for …
- Flow F25 *A guest rents a cabana*, step 5: The guest leaves; the attendant checks it in and settles the deposit. → Released in full, or partly captured against damage. **Partial capture is the normal case for a damaged item** and the reason two-phase spend was worth building.
- Flow F25 branch at step 4 (requiresStaff): when The guest has no card, or the hold is declined., The booking stands and the check-out does not. **A declined deposit is not a cancelled booking** — the guest may pay another way, and voiding their afternoon because a card failed is the wrong …
- Flow F25 branch at step 5 (requiresStaff): when The item comes back damaged., Part of the deposit is captured and **the resource routes to `maintenance` directly from `checkedOut`**, not through `available`. Routing it through available leaves a window in which the next guest …
- Flow F25 branch at step 5 (requiresStaff): when Nobody brings it back., The booking goes `overdue` on a timer, which is **not a failure state** — a guest running late is the normal case and the deposit is already held. Past a threshold the whole deposit captures and …
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-097?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Check out, Check in, Check out resource, Check in resource, Authorise stored value, Release stored value, Capture stored value.
- [ ] Every transition is wired: `BO-096`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `RENTAL_VIEW`, `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-098` Qualifications

**What a person is certified to do, and until when.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `resources` module |
| Block | Block D · task VM-BO-098 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setResourceQualifications`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `resourceId` (BO-095) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/resources/qualifications` |

**What the spec says about it.** CF-125. **Expiry is the field that makes this worth having** — a certification with no expiry is one nobody renews.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What a person resource (instructor, lifeguard, driver) is certified to do and until when, sorted by expiry, with a warning for expired qualifications held by staff on today's rota. The one thing to get right: expiry is the headline - a lapsed lifeguard certificate is a safety failure.

**Known correction pending (do not draw the wrong version)**

- **Text fields for issuedAt, expiresAt, documentAssetId and scopePath** Why: Dates need pickers, the document an upload, scopePath is server-owned (VO-R03). *(source: screens/P08-venue-back-office.yaml#BO-098; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Write-only screen (setResourceQualifications) with no read of current qualifications (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| code | text field | optional | — | — | — | — | `Qualification.code` |
| name | text field | optional | — | — | — | — | `Qualification.name` |
| issuedAt | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `Qualification.issuedAt` |
| expiresAt | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | The field that makes this worth having. A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one. | `Qualification.expiresAt` |
| issuer | text field | optional | — | — | — | — | `Qualification.issuer` |
| documentAssetId | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `Qualification.documentAssetId` |
| scopePath | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row could be written at … | `Qualification.scopePath` |

**Sent by *Save resource qualifications*** (`setResourceQualifications`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Qualifications `qualifications` | repeatable rows | required | — | — | — | — | `setResourceQualifications` body |
| Code `qualifications[].code` | text field | required | — | — | — | — | `setResourceQualifications` body |
| Name `qualifications[].name` | text field | required | — | — | — | — | `setResourceQualifications` body |
| Issued at `qualifications[].issuedAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setResourceQualifications` body |
| Expires at `qualifications[].expiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | The field that makes this worth having. A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a … | `setResourceQualifications` body |
| Issuer `qualifications[].issuer` | text field | optional | — | — | — | — | `setResourceQualifications` body |
| Document image `qualifications[].documentAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setResourceQualifications` body |
| Scope path `qualifications[].scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setResourceQualifications` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Qualification rows**: Code (picked from the qualification list), name, issued date, expiry date (date pickers), issuer, document upload; not raw text fields for dates and document ids. *(source: contracts/satellite/resources.yaml#setResourceQualifications)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): Sorted by expiry, not by name — **a lifeguard certificate that lapsed last month is a safety failure, not a data-quality one**

**Banner** (banner): Expired qualifications held by staff on today rota

**Qualifications** (data table, from `getResourceQualifications`)

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | The resource that holds this qualification. Set from the path of `setResourceQualifications`; without it a stored qualification belongs to … |
| Code | text | — |
| Name | text | — |
| Issued at | 1 Oct 2026 | — |
| Expires at | 1 Oct 2026 | The field that makes this worth having. A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last … |
| Issuer | text | — |
| Document image | the image or video | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resource qualifications (primary button) | `setResourceQualifications` PUT `/resources/{resourceId}/qualifications` | inline | Qualification[] | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **List**: Sorted by expiry ascending; Expired red, within 30 days amber, valid green; a banner lists expired qualifications of people rostered today. *(source: screens/P08-venue-back-office.yaml#BO-098 / DI-486)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save qualifications**: Replaces the person's qualification set. *(source: contracts/satellite/resources.yaml#setResourceQualifications)*

**Data it reads**: `getResourceQualifications` (onLoad, The qualifications as saved)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Qualifications with their expiry |
| Error (`?state=error`) | Could not load. |
| Empty, first run (`?state=emptyFirstRun`) | No qualifications recorded. **A role is not a skill** — 1.2.36 requires the check before assignment, not after. |
| Permission denied (`?state=emptyNoAccess`) | Without `RESOURCE_VIEW`, which `getResourceQualifications` requires, the screen does not load and this state names that permission. You do not have `RESOURCE_MANAGE`. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-876`: Skills and certification expiry on the workforce board use the same records.
- Match `BO-877`: Assignment rules test these qualifications.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
person: Maria Santos (Instructor)
qualifications:
- code: SKI-L3
  name: Ski instructor level 3
  issued: 12 Jan 2026
  expires: 11 Jan 2027
  issuer: Ski Dubai Academy
- code: FA-1
  name: First aid
  issued: 3 Nov 2024
  expires: 2 Nov 2026
  status: Expires in 32 days
```

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff
- `getResourceQualifications` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Without `RESOURCE_VIEW`, which `getResourceQualifications` requires, the screen does not load and this state names that permission. You do not have `RESOURCE_MANAGE`.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.3 | The system should allow management of the schedules of the staff resources with the possibility to set the parameters such as total hours, breaks, leave plan, absences. This data can be captured via … | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.4 | The system should allow linking of staff resources in different combinations and time-slot capacity with individual attraction experiences such as group lessons and private lessons. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.5 | The system should allow selection of specific instructors, staff skillset and/or specific timeslots for the staff offering experiences. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.12 | System should allow to assign the resources dynamically based on the resources availability and piority. The same functionality should be available over API / Online websites | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.34 | System shall maintain employee skill profiles. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.35 | System shall track certifications and expiry dates. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.36 | System shall validate qualifications before assignment. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.52 | System shall support priority-based allocation. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 17.2.6 | Maintenance Resource Planning - System shall support maintenance resource planning. | Maintenance & Safety Management | CONTRACTED | data `Qualification` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-098` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-098?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resource qualifications.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-099` Performance Manifest

**Who is in a performance, in what order. Opened from a Performance (renamed from session, decided 28 September, audit R165).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `resources` module |
| Block | Block D · task VM-BO-099 |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getPerformanceManifest` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | The cached manifest. **An instructor at the water edge needs this more than anyone**, and that is where the signal is worst. |
| Opens with | `performanceId` (BO-015) · cold entry: **Opened from a Performance** (decided 28 September, audit R165) — BO-015 Performance Calendar supplies `performanceId`, the path parameter of … |
| Route | `/resources/session-manifest` |

**What the spec says about it.** CF-125, CF-129. Distinct from duration, which variants already handle.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The manifest of a performance (a lesson, tour or session): who is in it, in running order, with experience level, package, notes and waiver status; an instructor reorders it (beginners first) and sees unsigned waivers before starting. It must work offline at the water's edge. The one thing to get right: unsigned waivers are named at the top.

**Known correction pending (do not draw the wrong version)**

- **Reorder opens a modal form** Why: Reordering is drag-and-drop in the list with Save; a modal adds nothing. *(source: screens/P08-venue-back-office.yaml#BO-099; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Form: Reorder performance manifest** (modal, opened by *Reorder performance manifest*; *Reorder performance manifest* calls `reorderPerformanceManifest`, *Cancel* sends nothing)

**Collects what `reorderPerformanceManifest` sends before it is called.** Required: `order`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `order` | multi-picker: choose order | required | — | — | — | — | `reorderPerformanceManifest` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device made the change, not when it reached the server. This is a `lastWriterWins` write that can arrive from an offline outbox, and without the device time "last" could … | `reorderPerformanceManifest` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**The performance participant** (detail panel, from `getPerformanceManifest`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | The `catalogue.performance` this participant is on (audit R165). |
| Subject | the name it points at, never the id | — |
| Position | 1,234 | — |
| Experience level | chip: First time, Beginner, Intermediate, Advanced | — |
| Package name | text | — |
| Notes | text | — |
| Has signed waiver | yes / no (icon or chip) | 2.15.9. Shown on the manifest because that is where it is acted on — an instructor about to start does not want to discover an unsigned … |

**Data table** (data table): Drag to reorder. **The running order is operational** — an instructor takes beginners first, and booking order puts one between two advanced riders

**Banner** (banner): Unsigned waivers, named. **An instructor about to start does not want to discover one at the water edge**

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Reorder performance manifest (primary button) | `reorderPerformanceManifest` PUT `/performances/{performanceId}/manifest` | inline | PerformanceParticipant[] | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Manifest**: Position, guest name, experience level (First time, Beginner, Intermediate, Advanced), package, notes, waiver signed tick or red "Waiver missing". *(source: contracts/satellite/resources.yaml#getPerformanceManifest / DI-574)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reorder**: Drag to reorder; saves the running order (offline-capable, syncs later). *(source: contracts/satellite/resources.yaml#reorderPerformanceManifest)*

**Data it reads**: `getPerformanceManifest` (onLoad, The manifest)

**Where the user goes next**

- → `BO-096` Resource Calendar: *Resource Calendar*
- → `BO-015` Performance Calendar: *Back to Performance Calendar*; carries `performanceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Participants in running order |
| Error (`?state=error`) | Could not load the manifest. |
| Empty, first run (`?state=emptyFirstRun`) | Nobody booked into this performance yet. |
| Empty, no results (`?state=emptyNoResults`) | No participants match. |
| Permission denied (`?state=emptyNoAccess`) | You do not have `RESOURCE_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_BOOK` for `reorderPerformanceManifest`. |
| Offline (`?state=offline`) | The cached manifest. **An instructor at the water edge needs this more than anyone**, and that is where the signal is worst. |

#### Edge cases to draw

- **Offline**: Cached manifest with "Updated 07:55"; reorder queues. *(source: screens/P08-venue-back-office.yaml#BO-099)*

#### Consistency with other screens

- Match `BO-015`: Opened from the performance calendar (cross-process, ticketing back office).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
performance: Private Ski Lesson - Sat 10 Oct 2026 10:00 - Instructor Maria Santos
participants:
- pos: 1
  name: Omar Haddad
  level: First time
  waiver: signed
- pos: 2
  name: Priya Nair
  level: Beginner
  waiver: missing
- pos: 3
  name: James Carter
  level: Advanced
  package: Ski + Lift + Rental
```

#### Permissions

- `getPerformanceManifest` → `RESOURCE_VIEW` (read) · staff
- `reorderPerformanceManifest` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** You do not have `RESOURCE_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_BOOK` for `reorderPerformanceManifest`.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.41 | Manage check-in process. The system needs to have the ability to be “told” that the person has arrived, Waivered, class sheets and in which session…Process driven. | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.43 | Each 30 min session can be either fully with Pro flyers only , or could be a mixture of 1st time flyers and Pro flyers. 1st time flyer products will have a “uplift” attached to them… ie for 2 x 1 … | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.44 | The system does this, both prior to flight and during the flight session. You can organize which flyers fly in which order depending on what package they have bought.. ( balances the whole 30 min … | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.45 | Show current flyers and upcoming flyers for the future sessions. | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.46 | Manager order of flyers in the session | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.47 | Adding options dynamically in the manifest/list of flyers such as repeat flights of Hi Flys | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |
| 1.3.48 | Assign photos and videos to flyers | Ticketing Catalogue | CONTRACTED | data `PerformanceParticipant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-099` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-099?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Reorder performance manifest.
- [ ] Every transition is wired: `BO-096`, `BO-015`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-103` Access & Venue

**Everything in access & venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `core` module |
| Block | Block C · task VM-BO-103 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE`, `SCOPE_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAccessPoints` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/access-venue` |

**What the spec says about it.** Section landing. **24 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Venue settings are not access state and getVenueSettings carries no module enablement (R279); the hub's "What is enabled here" panel cannot be filled from it …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Access & Venue section landing: today's admissions and takings, the gates and their state, live admissions, and tiles into the 24 screens of the section. A venue manager lands here in the morning. The one thing to get right: it shows the section's live state (gates, admissions) before it shows the menu.

**Known correction pending (do not draw the wrong version)**

- **Hub groups Queue, Parking, Resources and Maintenance screens under "Access & Venue"** Why: Acceptable as a section, but label the groups so a queue screen is not mistaken for gate access. *(source: designer default; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): "Venue id" text field filter and venue settings panel listing currency and quiet hours (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listAccessPoints`. | `listAccessPoints` ?venueId |
| Search access & venue | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Access point | picker: choose an access point | — | — | `listScans` ?accessPointId |
| Ticket | picker: choose a ticket | — | — | `listScans` ?ticketId |
| Outcome | segmented control | — | Admitted · Denied · Overridden | `listScans` ?outcome |
| Recorded from | date and time picker | — | — | `listScans` ?recordedFrom |
| Recorded to | date and time picker | — | — | `listScans` ?recordedTo |

#### Outputs: what the screen shows and produces

**Shown**

**Every access point** (data table, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 24 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**The selected access point** (detail panel, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Admissions today and takings today with comparison to the same day last week; values in venue time and AED (VO-R10). *(source: contracts/satellite/reporting.yaml#getKpiValues / R283)*
- **Gates strip**: Each access point as a chip with direction and operating mode (Normal, Free flow, Drop arm, Closed, Podium, Maintenance) and online/offline; problems first. *(source: contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / DI-648)*
- **Live admissions**: The last 20 scans, auto-updating, same row design as BO-034. *(source: contracts/spine/access.yaml#listScans)*
- **Section tiles**: Grouped Access (profiles, blacklist, scans, overrides, reconciliation), Queues (directory, configuration, integration, wait times, monitor), Resources, Maintenance, Parking. No attention counts until a summary read exists. *(source: screens/P08-venue-back-office.yaml#BO-103)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `listAccessPoints` (onLoad, Gates and lanes in this venue); `listScans` (onLoad, Admissions as they happen)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*
- → `BO-002` Queue Configuration: *Queue Configuration*
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*
- → `BO-005` Queue Monitor: *Queue Monitor*
- → `BO-006` Parking Configuration: *Parking Configuration*
- → `BO-030` Work Order Verification: *Work Order Verification*
- → `BO-032` Admission Profiles: *Admission Profiles*
- → `BO-033` Blacklist Management: *Blacklist Management*; carries `mediaCode`
- → `BO-038` Reconciliation Queue: *Reconciliation Queue*
- → `BO-069` Asset Register: *Asset Register*
- → `BO-071` Planned Maintenance: *Planned Maintenance*
- → `BO-072` Incident Log: *Incident Log*
- → `BO-093` Map Import & Labelling: *Map Import & Labelling*
- → `BO-094` Map Editor & Publish: *Map Editor & Publish*
- → `BO-096` Resource Calendar: *Resource Calendar*
- → `BO-097` Check Out & Check In: *Check Out & Check In*
- → `BO-098` Qualifications: *Qualifications*
- → `BO-099` Performance Manifest: *Performance Manifest*
- → `BO-1045` Price Bands & Categories: *Opens Price Bands & Categories*
- → `BO-1062` Tenant & Brand Context: *Opens Tenant & Brand Context*
- → `BO-151` Access Location Grouping: *Opens Access Location Grouping*
- → `BO-155` Visual Access Rule Builder: *Opens Visual Access Rule Builder*
- → `BO-161` Guest, Companion & Eligibility Rules: *Opens Guest, Companion & Eligibility Rules*
- → `BO-166` Credential Activation & Display Rules: *Opens Credential Activation & Display Rules*
- → `BO-167` Device Binding & Session Security: *Opens Device Binding & Session Security*
- → `BO-168` BLE Beacon & Geofence Configuration: *Opens BLE Beacon & Geofence Configuration*
- → `BO-185` Biometric Verification Profile Builder: *Opens Biometric Verification Profile Builder*
- → `BO-186` Face Pass Enrollment Configuration: *Opens Face Pass Enrollment Configuration*
- → `BO-188` Face Tag Temporary Enrollment: *Opens Face Tag Temporary Enrollment*
- → `BO-189` Face Matching & Verification Thresholds: *Opens Face Matching & Verification Thresholds*
- → `BO-201` Gate Modes, Free Spin & Emergency Controls: *Opens Gate Modes, Free Spin & Emergency Controls*
- → `BO-230` Live Gate Mode & Lane Control: *Opens Live Gate Mode & Lane Control*; carries `accessPointId`
- → `BO-335` Virtual Ticket Identity & Master Record Configuration: *Opens Virtual Ticket Identity & Master Record Configuration*
- → `BO-346` PDF, Printable & POS Ticket Designer: *Opens PDF, Printable & POS Ticket Designer*
- → `BO-618` Accreditation Form Builder: *Opens Accreditation Form Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in access & venue yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for access & venue. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-144`: The access command centre is the deeper dashboard; this hub links to it.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  admissionsToday: 6,482 (+8.7%)
  takingsToday: AED 412,350
gates:
- Main Plaza Gate 1 - Normal, online
- Gate 3 - Exit, Free flow
- North Entry - Offline 4 min
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have permission for access & venue. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 19.2.77 | Parking Locator - System shall help guests locate vehicles. | Guest Mobile App & Branding | CONTRACTED | data `AccessPoint` |
| 3.1.8 | The system shall detect suspicious QR usage patterns including device sharing, multiple simultaneous sessions, excessive activations, and abnormal access attempts, with configurable security … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.32 | Real-time fraud-monitoring & unified identity lock (one media per visit, Face-change audit, POD/Nanny linkage) | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.57 | In case of emergency, a drop arm mode can be activated at turnstiles. No scan and no count are being performed. | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.61 | It is possible for the system to integrate with hotels room card management system in order to read the room card at access control points and have the ability to interface to the hotels property … | Admission and Access | CONTRACTED | data `AccessPoint` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-103` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-103?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-003`, `BO-004`, `BO-005`, `BO-006`, `BO-030`, `BO-032`, `BO-033`, `BO-038`, `BO-069`, `BO-071`, `BO-072`, `BO-093`, `BO-094`, `BO-096`, `BO-097`, `BO-098`, `BO-099`, `BO-1045`, `BO-1062`, `BO-151`, `BO-155`, `BO-161`, `BO-166`, `BO-167`, `BO-168`, `BO-185`, `BO-186`, `BO-188`, `BO-189`, `BO-201`, `BO-230`, `BO-335`, `BO-346`, `BO-618`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`, `SCOPE_VIEW`.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"authoriseStoredValue": {"method":"POST","path":"/stored-value/authorisations","contract":"orders","summary":"Hold a balance on any stored-value instrument","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StoredValueAuthorisation"},
"bookResource": {"method":"POST","path":"/resource-bookings","contract":"resources","summary":"Reserve a specific resource for a window — staff only","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"captureStoredValue": {"method":"POST","path":"/stored-value/authorisations/{authorisationId}/capture","contract":"orders","summary":"Take some or all of a held balance","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StoredValueAuthorisation"},
"checkInResource": {"method":"POST","path":"/resource-bookings/{bookingId}/check-in","contract":"resources","summary":"Take it back, and settle the deposit","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"checkOutResource": {"method":"POST","path":"/resource-bookings/{bookingId}/check-out","contract":"resources","summary":"Hand it over, with a deposit against it","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getPerformanceManifest": {"method":"GET","path":"/performances/{performanceId}/manifest","contract":"resources","summary":"Who is in a performance, in what order","permission":"RESOURCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PerformanceParticipant"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"getResourceAvailability": {"method":"GET","path":"/resources/{resourceId}/availability","contract":"resources","summary":"When it is free, with conflicts already resolved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"ResourceAvailability"},
"getResourceQualifications": {"method":"GET","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What an instructor or staff resource is certified to do, and until when — as saved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Qualification"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"relinquishStoredValue": {"method":"POST","path":"/stored-value/authorisations/{authorisationId}/release","contract":"orders","summary":"Give a hold back","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StoredValueAuthorisation"},
"reorderPerformanceManifest": {"method":"PUT","path":"/performances/{performanceId}/manifest","contract":"resources","summary":"Change the running order","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceParticipant"},
"setResourceQualifications": {"method":"PUT","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What a person resource is certified to do, and until when","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Qualification"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PerformanceParticipant": {"type":"object","x-ticvai-persistence":"resources.performance_participant","description":"1.3.44. **The running order is operational.** An instructor takes beginners first, and a manifest sorted by booking time puts one between two advanced riders.\nFormerly `SessionParticipant` on `resources.session_participant`: a session is a Performance and the manifest hangs off one (decided 28 September, audit R165).\n","required":["id","performanceId","subjectId","position"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid","description":"The `catalogue.performance` this participant is on (audit R165)."},"subjectId":{"type":"string","format":"uuid"},"position":{"type":"integer"},"experienceLevel":{"type":"string","enum":["firstTime","beginner","intermediate","advanced"],"nullable":true},"packageName":{"type":"string","nullable":true},"notes":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the device made the running-order change that set `position` — the `recordedAt` of the last `reorderPerformanceManifest`. Null until the order is first changed.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When that change reached the server (naming-and-style 5.2)."},"hasSignedWaiver":{"type":"boolean","readOnly":true,"description":"2.15.9. **Shown on the manifest because that is where it is acted on** — an instructor about to start does not want to discover an unsigned waiver at the water's edge.\n"}}},
"Qualification": {"type":"object","x-ticvai-persistence":"resources.qualification","description":"1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n","required":["code","name"],"properties":{"resourceId":{"type":"string","format":"uuid","readOnly":true,"description":"**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"},"code":{"type":"string"},"name":{"type":"string"},"issuedAt":{"type":"string","format":"date","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"},"issuer":{"type":"string","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"ResourceAvailability": {"type":"object","description":"**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"freeWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"}}}},"blockedWindows":{"type":"array","description":"**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","held","setup","teardown","maintenance","blackout","closed","cleaning"],"description":"`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"}}}}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"StoredValueAuthorisation": {"type":"object","x-ticvai-persistence":"orders.stored_value_authorisation","description":"A hold against any stored-value instrument. **Two-phase by necessity, not by preference** — an arcade machine, a kitchen and a gate all take time between committing to a spend and knowing it succeeded, and a balance that cannot be held is a balance that gets double-spent or refunded by hand.\n","required":["id","kind","instrumentId","amount","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/StoredValueKind"},"instrumentId":{"type":"string","format":"uuid","description":"The wallet, card, voucher or position being held against."},"amount":{"$ref":"#/components/schemas/Money"},"status":{"type":"string","enum":["held","partiallyCaptured","captured","released","expired"],"description":"**Mirrors `cross-region.WalletAuthorisation` exactly**, which is the point — one lifecycle rather than six.\n"},"capturedAmount":{"$ref":"#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","description":"**Released automatically.** A hold nobody releases is a guest whose balance is short with no explanation, and the arcade is where that happens most.\n"},"reference":{"type":"string","description":"What the hold is for — an order, a play, a table visit."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"StoredValueKind": {"type":"string","description":"**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n","enum":["wallet","giftCard","gameCard","voucher","loyalty","prepaidEntitlement"]},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]}
}
```
