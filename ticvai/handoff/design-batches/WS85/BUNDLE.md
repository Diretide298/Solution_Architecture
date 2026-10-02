# WS85 — Game and Ride board 8

**9 screens · 8 operations · 11 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, DEVICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-464` | Game & Ride Operations Control Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-465` | Live Gameplay Transaction Monitor | B–D | 0 | 24 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-466` | Reader & Device Health Monitor | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-467` | Tap Validation & Decision Trace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-468` | Rejected Transaction & Reason Analysis | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-469` | Wallet & Deduction Transaction Monitor | B–D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-470` | Entitlement & Free-Play Consumption Monitor | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-471` | Offline, Synchronization & Recovery Monitor | B–D | 14 | 24 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-473` | Operational Analytics & Reconciliation Dashboard | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-464, BO-465, BO-466, BO-467, BO-469 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-464` Game & Ride Operations Control Center

**Provide the main real-time operational dashboard for the entire game/ride ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-ride-operations-control-center-bo-464` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The real-time control room for games and rides: today's taps, approvals, refusals and value consumed, the live state of every attraction and reader, and where there is a problem. It is the landing of the monitoring board and opens every monitor behind it. It monitors and never configures. The one thing to get right: this is a command centre (VO-R02), KPI tiles and a live status grid with problems surfaced first, not a list-detail screen.

**Known correction pending (do not draw the wrong version)**

- **Drawn as listDetail with no KPI tiles** Why: The pack gives eight KPI cards and a live grid; a board landing is a command centre (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-464; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The only bound read is the raw tap list** Why: Today's totals would have to be counted from every tap on the client; per-game counts already exist on Game (playsToday, creditsTakenToday, pointsAwardedToday) and reader status on listReaders, neither bound. *(source: contracts/satellite/games.yaml#listGameplayTransactions / contracts/satellite/games.yaml#listGames / contracts/satellite/games.yaml#listReaders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Client" filter** Why: P08 is one tenant's back office; a cross-client filter belongs to the platform console. *(source: screens/P08-venue-back-office.yaml#BO-465; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by client, venue, zone, attraction type, attraction, reader and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Zone, Attraction type, Attraction, Reader, Status. Venue is the top-bar venue; the pack's "Client" filter does not apply in a single tenant's back office and is left out. *(source: screens/P08-venue-back-office.yaml#BO-465)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles (today)**: Total taps, Authorised plays, Rejected plays (with rejection rate), Wallet value consumed (AED), Bonus value consumed (AED), Entitlement plays, Redemption credits earned, Reader / device issues. Deltas against the same time yesterday; Rejected and Issues tiles turn amber or red over a threshold. *(source: screens/P08-venue-back-office.yaml#BO-464 / screens/P08-venue-back-office.yaml#BO-465 / DI-881)*
- **Zone health**: One chip per zone (Main Park Healthy, Arcade Healthy, Fun Zone Warning), worst first; clicking filters the grid. *(source: screens/P08-venue-back-office.yaml#BO-465)*
- **Live status grid**: Columns Attraction, Reader, Status, Last tap ("10:42"), Plays today, Issues. Rows with an offline reader or open issues sort first and carry a red edge. Refreshes on its own every few seconds with "Updated 10:42:18" visible; a pause control stops it for reading. *(source: screens/P08-venue-back-office.yaml#BO-465 / contracts/satellite/games.yaml#/components/schemas/Game)*
- **Board tiles**: Tiles to Live transactions (BO-465), Reader health (BO-466), Decision trace (BO-467), Refusals (BO-468), Wallet deductions (BO-469), Entitlement use (BO-470), Offline sync (BO-471), Alerts (BO-141), Analytics (BO-473). *(source: screens/P08-venue-back-office.yaml#BO-464 / R276)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open attraction or reader row**: Opens the live feed filtered to that reader, or reader health for an offline reader. *(source: F194 step 2 / F194 step 4)*

**Data it reads**: `listGameplayTransactions` (onLoad, Live operations)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-465` Live Gameplay Transaction Monitor: *Live Gameplay Transaction Monitor*
- → `BO-466` Reader & Device Health Monitor: *Reader & Device Health Monitor*
- → `BO-467` Tap Validation & Decision Trace: *Tap Validation & Decision Trace*
- → `BO-468` Rejected Transaction & Reason Analysis: *Rejected Transaction & Reason Analysis*
- → `BO-469` Wallet & Deduction Transaction Monitor: *Wallet & Deduction Transaction Monitor*
- → `BO-470` Entitlement & Free-Play Consumption Monitor: *Entitlement & Free-Play Consumption Monitor*
- → `BO-471` Offline, Synchronization & Recovery Monitor: *Offline, Synchronization & Recovery Monitor*
- → `BO-141` Operational Alerts, AI Replenishment & Action Center: *Operational Alerts & Exception Center (BO-141, absorbed BO-472, audit R276)*
- → `BO-473` Operational Analytics & Reconciliation Dashboard: *Operational Analytics & Reconciliation Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The data feed stops updating**: The "Updated" time turns amber after a minute and red after five with "Live data delayed"; tiles are not left looking current. *(source: designer default)*
- **No plays yet today (venue just opened)**: Tiles show 0 with "since 10:00 opening", not empty states. *(source: designer default)*

#### Consistency with other screens

- Match `BO-394`: The board-1 Game & Ride Operations Dashboard is the configuration view of the same estate; status words (Online, Offline, Maintenance) must match.
- Match `BO-141`: Operational alerts for games were absorbed into the alerts centre (BO-472 into BO-141); the alert tile opens it filtered to games.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  taps: 18420
  authorised: 17660
  rejected: 760 (4.1%)
  walletConsumed: AED 182,440.00
  bonusConsumed: AED 21,300.00
  entitlementPlays: 5210
  creditsEarned: 1284000
  issues: 3
grid:
- attraction: Prize Crane
  reader: R-031
  status: Offline
  lastTap: '10:25'
  playsToday: 321
  issues: 1
- attraction: Basketball Pro
  reader: R-023
  status: Online
  lastTap: '10:42'
  playsToday: 612
  issues: 2
- attraction: VR Racing
  reader: R-014
  status: Online
  lastTap: '10:42'
  playsToday: 842
  issues: 0
- attraction: Falcon Coaster
  reader: R-001
  status: Online
  lastTap: '10:41'
  playsToday: 1025
  issues: 0
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-464` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-464`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 1: Opens Game & Ride Operations Control Center → Provide the main real-time operational dashboard for the entire game/ride ecosystem.
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F194 branch at step 1 (expected): when Nothing has been set up on Game & Ride Operations Control Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F194 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-464?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-465`, `BO-466`, `BO-467`, `BO-468`, `BO-469`, `BO-470`, `BO-471`, `BO-141`, `BO-473`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-465` Live Gameplay Transaction Monitor

**Display gameplay transactions as they occur across all connected readers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Selecting a transaction should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/live-gameplay-transaction-monitor-bo-465` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The live feed of every gameplay tap across the venue's readers, as it happens: who tapped which reader, what it cost, what paid for it, and whether it was approved. Supervisors watch it during peaks and open a single tap to investigate a complaint. The one thing to get right: a readable live feed (new rows arrive at the top without moving what the user is reading) with a detail drawer that shows the money before and after.

**Known correction pending (do not draw the wrong version)**

- **The transaction record lacks most drawer fields** Why: GameplayTransaction has no before or after balance, price rule, wallet or response time; the authorisation record holds some (remainingBalance) but no read returns it. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's "Processing" status and its source list** Why: Outcomes are allowed, refused, reversed (no processing, and the pack has no reversed). VIP and Retry are price rules, not funding sources; the source column shows what paid (wallet, bonus, free play, entitlement). *(source: screens/P08-venue-back-office.yaml#BO-466 / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No attraction filter** Why: The read filters by reader, outcome and from-time only. *(source: contracts/satellite/games.yaml#listGameplayTransactions; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Result (Approved, Rejected, Reversed), Reader, Attraction, From time. Default last 15 minutes, all results. *(source: screens/P08-venue-back-office.yaml#BO-466 / contracts/satellite/games.yaml#listGameplayTransactions)*

#### Outputs: what the screen shows and produces

**Shown**

**Every live gameplay transaction** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transaction ID | text | not in the schema: `Transaction ID` |
| Card/credential | text | not in the schema: `Card/credential` |
| Wallet | text | not in the schema: `Wallet` |
| Reader | text | not in the schema: `Reader` |
| Attraction | text | not in the schema: `Attraction` |
| Price rule | text | not in the schema: `Price rule` |
| Funding source | text | not in the schema: `Funding source` |
| Before balance | text | not in the schema: `Before balance` |
| Deduction | text | not in the schema: `Deduction` |
| After balance | text | not in the schema: `After balance` |
| Authorization result | text | not in the schema: `Authorization result` |
| Response time | text | not in the schema: `Response time` |

**The selected live gameplay transaction** (detail panel): The pack groups this record's detail under its own headings: “Live Transaction Feed”, “Transaction Sources”, “Live Status”.

| Shows | Format | Notes |
|---|---|---|
| Transaction ID | text | not in the schema: `Transaction ID` |
| Card/credential | text | not in the schema: `Card/credential` |
| Wallet | text | not in the schema: `Wallet` |
| Reader | text | not in the schema: `Reader` |
| Attraction | text | not in the schema: `Attraction` |
| Price rule | text | not in the schema: `Price rule` |
| Funding source | text | not in the schema: `Funding source` |
| Before balance | text | not in the schema: `Before balance` |
| Deduction | text | not in the schema: `Deduction` |
| After balance | text | not in the schema: `After balance` |
| Authorization result | text | not in the schema: `Authorization result` |
| Response time | text | not in the schema: `Response time` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Live feed**: Columns Time (HH:mm:ss), Card (****4321), Reader, Attraction, Price (AED or "--" when an entitlement paid), Source ("Bonus + Wallet", "All Games Pass"), Result chip. New rows slide in at the top with a brief highlight; when the user has scrolled, a "12 new" pill appears instead of moving the list. Rows decided offline carry an "Offline" tag and their sync time. *(source: screens/P08-venue-back-office.yaml#BO-465 / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Transaction drawer**: Transaction id, card, wallet, reader, attraction, price rule, funding source, before balance, deduction, after balance, result, response time (ms). Rejected rows show the reason in plain words and the guest message the reader showed. *(source: screens/P08-venue-back-office.yaml#BO-466 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Pause / Resume live**: Freezes the feed for reading; resuming loads what arrived meanwhile. *(source: designer default)*
- **Open decision trace**: From the drawer, opens BO-467 for that tap. *(source: screens/P08-venue-back-office.yaml#BO-467)*

**Data it reads**: `listGameplayTransactions` (onLoad, Every tap)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live gameplay transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live gameplay transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live gameplay transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live gameplay transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Very high tap rate during a peak**: The feed batches arrivals (refresh every few seconds) rather than repainting per tap; counts stay exact. *(source: designer default)*
- **A reversed play**: Shown as its own row "Reversed" linked to the original, never by editing the original row. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*

#### Consistency with other screens

- Match `BO-469`: The wallet deduction monitor shows the same taps from the money side; transaction ids must match.
- Match `BO-468`: Reasons use the same plain labels as the rejection analysis.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
feed:
- time: '10:42:18'
  card: '****4321'
  reader: R-014
  attraction: VR Racing
  price: AED 20.00
  source: Bonus + Wallet
  result: Approved
- time: '10:42:16'
  card: '****7621'
  reader: R-001
  attraction: Falcon Coaster
  price: --
  source: All Games Pass
  result: Approved
- time: '10:42:12'
  card: '****9912'
  reader: R-023
  attraction: Basketball Pro
  price: AED 20.00
  source: Wallet
  result: Rejected, insufficient balance
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-465` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-465`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 2: Works in Live Gameplay Transaction Monitor → Display gameplay transactions as they occur across all connected readers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-465?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-466` Reader & Device Health Monitor

**Monitor communication and operational status of the physical Chinese readers and other connected devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/games-rides/reader-device-health-monitor-bo-466` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shows whether each reader and connected device is alive, talking and running the right configuration. Operations use it to catch a dead reader before guests do. It monitors the connection; it does not set business rules. The one thing to get right: heartbeat age and configuration version are the two facts that matter, and both come from the one device register.

**Known correction pending (do not draw the wrong version)**

- **Empty-label table and detail panel** Why: Generated placeholders; title them "Readers and devices" and the reader name. *(source: screens/P08-venue-back-office.yaml#BO-466; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Health states cannot be read from listReaders** Why: Reader.status is unconfigured, active, offline, maintenance, disabled; heartbeat, firmware, serial and configuration version live in the device register (ADR-0067), which is not bound. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / ADR-0067 / contracts/spine/tenancy.yaml#listDevices; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Entry parameter deviceId taken from the session** Why: The screen is a list reached from the control centre; a device is selected on the screen, not carried in the session. *(source: screens/P08-venue-back-office.yaml#BO-466; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Telemetry read centred on battery** Why: Game readers are mains-powered; show signal, response and uptime, and battery only for handheld devices. *(source: contracts/spine/tenancy.yaml#getDeviceTelemetry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |
| From | date and time picker | — | — | `getDeviceTelemetry` ?from |
| To | date and time picker | — | — | `getDeviceTelemetry` ?to |
| Metric | text field | — | — | `getDeviceTelemetry` ?metric |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Health (Online, Offline, Degraded, Synchronising, Configuration out of sync, Device error), Zone, Attraction. *(source: screens/P08-venue-back-office.yaml#BO-467)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Device table**: Columns Reader, Attraction, Connection, Last heartbeat ("5 sec ago"), Last tap ("2 sec ago"), Health (Healthy / Warning / Critical). Critical first. Relative times tick live. *(source: screens/P08-venue-back-office.yaml#BO-466)*
- **Device details**: Reader id, serial number, IP, firmware, configuration version (with "Target 28" when behind), last sync, last heartbeat, response time; a small heartbeat and signal sparkline for the last hour. *(source: screens/P08-venue-back-office.yaml#BO-467 / contracts/spine/tenancy.yaml#getDeviceTelemetry)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test connection**: Runs the reader test and shows each check (connectivity, card read, display, trigger) passed or failed. *(source: contracts/satellite/games.yaml#testReader)*
- **Resync configuration**: Deploys the current configuration to that reader; the row shows Pending until acknowledged. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **View logs**: Opens BO-482 for the reader. *(source: screens/P08-venue-back-office.yaml#BO-467)*

**Data it reads**: `listReaders` (onLoad, Reader and device health); `getDeviceTelemetry` (onLoad, Telemetry behind it)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader device health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader device health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader device health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader device health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader stops reporting but was not switched off**: Status becomes Unreachable once its last report is older than its heartbeat interval; shown as Critical. *(source: contracts/satellite/games.yaml#reportReaderQueue)*
- **Reader in maintenance**: Shown greyed "Maintenance" and excluded from issue counts. *(source: contracts/satellite/games.yaml#/components/schemas/Reader)*

#### Consistency with other screens

- Match `BO-404`: The reader management dashboard on board 2 uses the same health words and colours.
- Match `BO-036`: Firmware, serial and heartbeat are the device register's (ADR-0067); show the same values as the device registry.
- Match `BO-471`: Readers holding offline plays show a "12 pending" badge linking there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
devices:
- reader: R-014
  attraction: VR Racing
  connection: Online
  heartbeat: 5 sec ago
  lastTap: 2 sec ago
  health: Healthy
  firmware: GR-X10 3.2.1
  config: '28'
- reader: R-023
  attraction: Basketball Pro
  connection: Online
  heartbeat: 4 sec ago
  lastTap: 8 sec ago
  health: Warning
  config: 27 (target 28)
- reader: R-031
  attraction: Prize Crane
  connection: Offline
  heartbeat: 8 min ago
  lastTap: 9 min ago
  health: Critical
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `getDeviceTelemetry` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.4.21 | Battery Monitoring - System shall monitor battery levels where applicable. | Device Management | CONTRACTED | `getDeviceTelemetry` |
| 16.4.22 | Device Performance Monitoring - System shall monitor device performance. | Device Management | CONTRACTED | `getDeviceTelemetry` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-466` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-466`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 4: Works in Reader & Device Health Monitor → Monitor communication and operational status of the physical Chinese readers and other connected devices.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-466?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-467` Tap Validation & Decision Trace

**Allow operations to understand exactly how TICVAI reached an approval or rejection decision for an individual customer tap. This relates directly to the requirement that balance, bonus and entitlements be validated in real time before gameplay.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/tap-validation-decision-trace-bo-467` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Explains one tap: every check TICVAI ran, in order, with the result and the value involved, ending in the decision and what the reader and game did. Used to answer "why was I refused" and "why was I charged". The one thing to get right: it shows the decision as it was made at the time of the tap; re-running with today's configuration is a separate, labelled comparison.

**Known correction pending (do not draw the wrong version)**

- **Only the simulation is bound** Why: Simulation answers what would happen now; the screen must show the stored decision of a past tap. The authorisation record keeps its trace, but no operation reads one back by id. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A primary button with an empty label and Cancel are the only components** Why: Generated placeholders; the trace and runtime result are not drawn. *(source: screens/P08-venue-back-office.yaml#BO-467; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Transaction**: Arrives from the live feed or the rejection list; or search by transaction id or card plus time. *(source: screens/P08-venue-back-office.yaml#BO-467)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Transaction TX-982411, Card ****4321, Reader R-014, Attraction VR Racing, time, decision chip. *(source: screens/P08-venue-back-office.yaml#BO-467)*
- **Decision trace**: Numbered steps in the configured check order: 1 Reader valid, 2 Card active, 3 Card expiry valid, 4 Attraction active, 5 Entitlement not applicable, 6 Bonus AED 10 available, 7 Paid wallet AED 75 available, 8 Price AED 20, 9 Deduction AED 10 bonus + AED 10 wallet, 10 Decision AUTHORISED. Passed steps green, the failing step red with its reason, steps after a failure greyed "Not reached". *(source: screens/P08-venue-back-office.yaml#BO-467 / screens/P08-venue-back-office.yaml#BO-468 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **Runtime result**: Reader response APPROVE, Game trigger SENT, Game started (time); a missing game-start shows "No start confirmation received" in amber. *(source: screens/P08-venue-back-office.yaml#BO-468 / screens/P08-venue-back-office.yaml#BO-482)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Re-run with current configuration**: Runs the simulation for the same card, reader and time and shows the two traces side by side, differences highlighted ("Price then AED 20, now AED 25"). *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*
- **Open the rule**: Each step links to the screen that owns the rule (expiry BO-456, entitlement BO-401, price BO-442, deduction order BO-426). *(source: designer default)*

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tap validation decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tap validation decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tap validation decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tap validation decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Tap decided offline by the reader**: Trace says "Decided by the reader from its offline package (version 27)"; only the steps the edge package covers are shown. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation / contracts/satellite/games.yaml#authoriseGameplay)*

#### Consistency with other screens

- Match `BO-433`: The validation simulator on board 4 uses the same trace component and step names.
- Match `BO-459`: Same component; the expiry screen highlights steps 2 and 3.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trace:
  tx: TX-982411
  card: '****4321'
  reader: R-014
  attraction: VR Racing
  price: AED 20.00
  deduction: AED 10.00 bonus + AED 10.00 wallet
  decision: AUTHORISED
  reader_response: APPROVE
  gameTrigger: SENT
```

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-467` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-467`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 6: Works in Tap Validation & Decision Trace → Allow operations to understand exactly how TICVAI reached an approval or rejection decision for an individual customer tap. This relates directly to the requirement that balance, bonus and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-467?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-468` Rejected Transaction & Reason Analysis

**Centralize all rejected gameplay transactions and identify why customers are being denied.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Rejection KPIs) and a per-row directory (§Time Attraction Card Reason Reader; Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/rejected-transaction-reason-analysis-bo-468` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Every refused tap in one place, and why: so operations can tell whether a spike comes from guests (balance, expired cards), from configuration (no price, game not in the package) or from technology (reader offline). The one thing to get right: reasons are grouped by origin (Guest, Configuration, Technical), because that grouping tells the user who has to act.

**Known correction pending (do not draw the wrong version)**

- **The pack's reason codes do not match the contract's** Why: The authorisation reasons are cardNotFound, cardExpired, cardBlocked, retapTooSoon, heightRestriction, ageRestriction, insufficientFunds, entitlementExhausted, entitlementNotValidHere, cooldownActive, dailyCapReached, readerNotConfigured, gameUnavailable; the pack's PRICE_NOT_FOUND and READER_OFFLINE have no code, and ENTITLEMENT_EXPIRED / GAME_NOT_INCLUDED / USAGE_LIMIT_REACHED map only … *(source: screens/P08-venue-back-office.yaml#BO-468 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The stored refusal reason is free text** Why: GameplayTransaction.reason is a plain string while the authorisation reason is an enum; analysis by reason needs the enum on the stored row. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table columns are the pack's sample rows and chart names** Why: The generator turned example rows and the analysis list into columns of "Every rejected transaction reason". *(source: screens/P08-venue-back-office.yaml#BO-468; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No aggregate read** Why: Rates and counts need every tap of the day counted on the client; a summary by reason, reader and hour is missing. *(source: contracts/satellite/games.yaml#listGameplayTransactions; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Date (default today), Attraction, Reader, Reason, Origin (Guest, Configuration, Technical). *(source: screens/P08-venue-back-office.yaml#BO-468 / screens/P08-venue-back-office.yaml#BO-469)*

#### Outputs: what the screen shows and produces

**Shown**

**Rejections Today** (metric tile)

**Rejection Rate** (metric tile)

**Insufficient Balance** (metric tile)

**Invalid/Expired Card** (metric tile)

**Entitlement Failure** (metric tile)

**Retap Protection** (metric tile)

**Reader/Technical Failure** (metric tile)

**Every rejected transaction reason** (data table)

| Shows | Format | Notes |
|---|---|---|
| 10:42 VR racing ****3321 insufficient balance r 014 | text | not in the schema: `10:42 VR Racing ****3321 Insufficient Balance R-014` |
| 10:40 bumper cars ****2178 card expired r 007 | text | not in the schema: `10:40 Bumper Cars ****2178 Card Expired R-007` |
| 10:38 basketball ****6621 retap too soon r 023 | text | not in the schema: `10:38 Basketball ****6621 Retap Too Soon R-023` |
| Rejections by attraction | text | not in the schema: `Rejections by attraction` |
| Rejections by reader | text | not in the schema: `Rejections by reader` |
| Rejections by reason | text | not in the schema: `Rejections by reason` |
| Rejection trend | text | not in the schema: `Rejection trend` |

**The selected rejected transaction reason** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| 10:42 VR racing ****3321 insufficient balance r 014 | text | not in the schema: `10:42 VR Racing ****3321 Insufficient Balance R-014` |
| 10:40 bumper cars ****2178 card expired r 007 | text | not in the schema: `10:40 Bumper Cars ****2178 Card Expired R-007` |
| 10:38 basketball ****6621 retap too soon r 023 | text | not in the schema: `10:38 Basketball ****6621 Retap Too Soon R-023` |
| Rejections by attraction | text | not in the schema: `Rejections by attraction` |
| Rejections by reader | text | not in the schema: `Rejections by reader` |
| Rejections by reason | text | not in the schema: `Rejections by reason` |
| Rejection trend | text | not in the schema: `Rejection trend` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rejection KPIs**: Tiles Rejections today, Rejection rate, Insufficient balance, Invalid or expired card, Entitlement failure, Retap protection, Reader or technical failure; each with the delta to yesterday. *(source: screens/P08-venue-back-office.yaml#BO-468)*
- **Reason vocabulary**: Plain labels with the origin - Insufficient balance (Guest), Card expired (Guest), Card blocked (Guest), No plays left on the pass (Guest), Not valid on this game (Configuration), Daily limit reached (Guest), Retap too soon (Guest, protective), Height or age restriction (Guest), Reader not configured (Configuration), Game unavailable (Technical), Price not found (Configuration), Reader offline (Technical). *(source: screens/P08-venue-back-office.yaml#BO-468 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*
- **Analysis**: Four charts - by attraction (bar), by reader (bar), by reason (bar, coloured by origin), trend (line by hour, stacked by origin). *(source: screens/P08-venue-back-office.yaml#BO-469)*
- **Rejection table**: Columns Time, Attraction, Card, Reason, Reader; cursor paging; clicking a row opens its decision trace. *(source: screens/P08-venue-back-office.yaml#BO-468)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open trace**: Opens BO-467 for the tap. *(source: screens/P08-venue-back-office.yaml#BO-467)*
- **Open configuration**: For configuration-origin reasons, a link to the screen that fixes it (price, entitlement, reader mapping). *(source: contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*

**Data it reads**: `listGameplayTransactions` (onLoad, Refusals, by reason)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rejected transaction reason list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rejected transaction reason untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rejected transaction reason yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rejected transaction reason are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **One reader refuses 40 percent of taps**: A spike suggestion appears ("R-023 refusing 38% since 10:05, mostly Price not found") with an Investigate action; a person decides (VO-R11). *(source: contracts/satellite/games.yaml#listGameplayTransactions)*
- **Retap protection refusals**: Counted, but shown as protective (grey, not red), since they prevent double charges. *(source: DI-867)*

#### Consistency with other screens

- Match `BO-433`: The validation simulator's exception analysis uses the same reason labels.
- Match `BO-480`: The guest message for each reason is the reader text configured in the output mapping.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  rejections: 760
  rate: 4.1%
  insufficient: 402
  cardInvalid: 96
  entitlement: 118
  retap: 120
  technical: 24
rows:
- time: '10:42'
  attraction: VR Racing
  card: '****3321'
  reason: Insufficient balance
  reader: R-014
- time: '10:40'
  attraction: Bumper Cars
  card: '****2178'
  reason: Card expired
  reader: R-007
- time: '10:38'
  attraction: Basketball Pro
  card: '****6621'
  reason: Retap too soon
  reader: R-023
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-468` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-468`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 8: Works in Rejected Transaction & Reason Analysis → Centralize all rejected gameplay transactions and identify why customers are being denied.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-468?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-469` Wallet & Deduction Transaction Monitor

**Monitor the financial/value movement generated by game and ride activity. The source requires the customer's amount to be deducted after the card tap based on available balance and the remaining balance to be updated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/games-rides/wallet-deduction-transaction-monitor-bo-469` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Value deducted by game and ride taps, with balance after each tap.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **deduction stream**: Tap time, device, game, amount, balance after. *(source: contracts/satellite/wallet.yaml#listWalletTransactions)*

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet deduction transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet deduction transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet deduction transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet deduction transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tap:
  device: Arcade reader 12
  game: Dune Racer
  amount: AED 6.00
  balanceAfter: AED 42.00
```

#### Permissions

- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-469` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-469`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 10: Works in Wallet & Deduction Transaction Monitor → Monitor the financial/value movement generated by game and ride activity. The source requires the customer's amount to be deducted after the card tap based on available balance and the remaining …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-469?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-470` Entitlement & Free-Play Consumption Monitor

**Monitor consumption of packages, passes, limited plays, unlimited entitlements and free-game credits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/entitlement-free-play-consumption-monitor-bo-470` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Watches how passes, packages, limited plays, unlimited entitlements and free-game credits are being used today, and what remains on each card. It traces use without changing any entitlement. The one thing to get right: the five entitlement kinds behave differently (unlimited has no "remaining"), so each row says what kind it is and shows remaining in that kind's terms.

**Known correction pending (do not draw the wrong version)**

- **The bound read returns entitlement definitions, not consumption** Why: listGameEntitlements lists products (kind, play count, validity); per-card use and remaining are not in it. Use only follows from taps carrying entitlementId, which give no before or remaining. *(source: contracts/satellite/games.yaml#listGameEntitlements / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's third example row is garbled** Why: "****9102 Free Game 0 Basketball 1 1" reads as card ****9102, Free game credit, Basketball, before 1, used 1, remaining 0; sample data above uses that. *(source: screens/P08-venue-back-office.yaml#BO-470; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Product type (All games pass, Unlimited specific games, Limited specific games, Package, Free game credit), Attraction, Card. *(source: screens/P08-venue-back-office.yaml#BO-470 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Outputs: what the screen shows and produces

**Shown**

**Entitlement Plays Today** (metric tile)

**Free Plays** (metric tile)

**Package Plays** (metric tile)

**Unlimited Pass Uses** (metric tile)

**Limited Plays Remaining** (metric tile)

**Failed Entitlement Attempts** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Entitlement plays today, Free plays, Package plays, Unlimited pass uses, Limited plays remaining (across active cards), Failed entitlement attempts (links to BO-468 filtered). *(source: screens/P08-venue-back-office.yaml#BO-470)*
- **Consumption table**: Columns Card, Product, Kind, Attraction, Before, Used, Remaining. Unlimited shows "Unlimited" in Before and Remaining; a limited entitlement that reaches 0 shows "Used up"; time-limited passes show "Valid until 18:00". *(source: screens/P08-venue-back-office.yaml#BO-470)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open card**: Opens the card profile (BO-455) with its entitlements. *(source: designer default)*

**Data it reads**: `listGameEntitlements` (onLoad, Entitlement consumption)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement free-play consumption list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement free-play consumption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement free-play consumption yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement free-play consumption are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A daily cap or cooldown stops an unlimited pass**: Shown as "Unlimited, daily cap 10 reached" so staff understand why an unlimited pass was refused. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Consistency with other screens

- Match `BO-427`: Kind names match the entitlement configuration screens (BO-427 to BO-430).
- Match `BO-490`: Remaining plays shown here equal what the guest sees as "Included, 2 plays remaining".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  entitlementPlays: 5210
  freePlays: 640
  packagePlays: 2100
  unlimitedUses: 2470
  limitedRemaining: 18300
  failed: 118
rows:
- card: '****4321'
  product: Arcade Pack
  kind: Limited
  attraction: VR Racing
  before: 2
  used: 1
  remaining: 1
- card: '****7122'
  product: Kids Pass
  kind: Unlimited specific games
  attraction: Bumper Cars
  before: Unlimited
  used: 1
  remaining: Unlimited
- card: '****9102'
  product: Free game credit
  kind: Free play
  attraction: Basketball Pro
  before: 1
  used: 1
  remaining: Used up
```

#### Permissions

- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-470` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-470`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 12: Works in Entitlement & Free-Play Consumption Monitor → Monitor consumption of packages, passes, limited plays, unlimited entitlements and free-game credits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-470?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-471` Offline, Synchronization & Recovery Monitor

**Monitor readers or edge components that temporarily lose connectivity with TICVAI and manage recovery/synchronization. This is a TICVAI Recommended Enhancement, based on the architecture we agreed for physical readers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/offline-synchronization-recovery-monitor-bo-471` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Watches readers that lost their connection and are holding plays they approved offline, and the recovery when they reconnect. Plays held offline are revenue TICVAI has not seen and balances a guest may have spent twice. The one thing to get right: pending count, pending value and how long it has been waiting are the three numbers per reader, and the offline limits that bound the exposure sit beside them.

**Known correction pending (do not draw the wrong version)**

- **The pack's statuses Synchronizing, Synchronized, Conflict, Failed sync** Why: The read returns online, offline, degraded, unreachable; sync progress has no state. Derive "Holding offline plays" from pendingTransactions and drop Conflict until it exists. *(source: screens/P08-venue-back-office.yaml#BO-470 / contracts/satellite/games.yaml#/components/schemas/ReaderSyncStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Offline Since" bound to oldestPendingAt** Why: The oldest held play is not when the reader went offline; a reader can be online and still holding plays. Label the column "Oldest pending play". *(source: contracts/satellite/games.yaml#/components/schemas/ReaderSyncStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The three offline controls shown as per-reader fields** Why: Offline allowed and maximum value are venue-wide validation rules, and maximum duration has no field at all. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a maximum offline duration needed, after which the reader refuses offline taps?** → The venue sets a maximum offline duration; readers then refuse offline taps. *(decided by Chinmay, 2026-10-02; DEC-426 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select field | — | — | — | — | Filters the returned readers client-side by `status` (online, offline, degraded, unreachable). The pack's statuses Synchronizing, Synchronized, Conflict and Failed Sync have no value in the enum. | — |

**Form: Set maximum offline duration** (modal, opened by *Set maximum offline duration*; *Set maximum offline duration* calls `setGateOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setGateOfflinePolicy` sends before it is called.** Required: `venueId`. Optional: `maxOfflineDurationHours`, `offlineChecks`, `afterThresholdBehavior`, `revocationTriggerEvents`, `revocationMaxAllowedAgeMinutes`, `revocationStalenessAction`, `operatingModes`, `centralUnavailableAfterSeconds`, `edgeUnavailableAfterSeconds`, `automaticSwitch`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setGateOfflinePolicy` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setGateOfflinePolicy` body |
| Max offline duration hours `maxOfflineDurationHours` | number field (hours) | optional | — | min 0 | — | Hours a reader may validate offline; past it, readers refuse offline taps (decided 2 October 2026, Chinmay, critical set 1, BO-471: "Yes: the venue sets a maximum offline … | `setGateOfflinePolicy` body |
| Offline checks `offlineChecks` | multi-select chips | optional | — | Credential authenticity · Digital signature · Ticket ID · Venue · Park · Zone · Visit date · Time window · Credential status snapshot · Ticket type · Guest category · Seat … | — | What a gate may validate locally | `setGateOfflinePolicy` body |
| After threshold behavior `afterThresholdBehavior` | radio group | optional | — | Continue restricted validation · Operator warning · Supervisor mode · Fail closed · Fallback | — | — | `setGateOfflinePolicy` body |
| Revocation trigger events `revocationTriggerEvents` | multi-select chips | optional | — | Fraud lock · Refund · Cancellation · Lost credential · Transfer · Reissue · Manual invalidation | — | Events that push an invalidation into the offline cache | `setGateOfflinePolicy` body |
| Revocation max allowed age minutes `revocationMaxAllowedAgeMinutes` | number field (minutes) | optional | — | min 0 | — | Maximum allowed revocation cache age | `setGateOfflinePolicy` body |
| Revocation staleness action `revocationStalenessAction` | select | optional | — | Continue · Continue with warning · Restricted products only · Supervisor mode · Deny selected credential classes · Fail closed | — | What devices do when the cache is older than the maximum allowed age | `setGateOfflinePolicy` body |
| Operating modes `operatingModes` | multi-select chips | optional | — | Online · Degraded · Edge mode · Local offline · Unsafe expired | — | Operating modes a device moves through as connectivity fails | `setGateOfflinePolicy` body |
| Central unavailable after seconds `centralUnavailableAfterSeconds` | number field (seconds) | optional | — | min 0 | — | Seconds without central services before switching to edge mode | `setGateOfflinePolicy` body |
| Edge unavailable after seconds `edgeUnavailableAfterSeconds` | number field (seconds) | optional | — | min 0 | — | Seconds without the venue edge before switching to local offline | `setGateOfflinePolicy` body |
| Automatic switch `automaticSwitch` | toggle | optional | on | — | — | Switch modes automatically without stopping guest flow | `setGateOfflinePolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setGateOfflinePolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The edge threshold is shorter than the central one.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Status filter**: Online, Offline, Degraded, Unreachable, plus "Holding offline plays" (pending above zero). *(source: contracts/satellite/games.yaml#/components/schemas/ReaderSyncStatus)*
- **Offline controls**: Offline operation allowed (on/off) and Maximum offline value (AED) are venue-wide validation settings; shown here read-only with a link to BO-425 where they are edited. Maximum offline duration is a venue setting (hours); past it, a reader refuses offline taps. *(source: screens/P08-venue-back-office.yaml#BO-470 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Readers offline** (metric tile, from `getGameplaySyncStatus`): Count of readers whose `status` is offline or unreachable.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**Pending offline transactions** (metric tile, from `getGameplaySyncStatus`): Summed across readers.

| Shows | Format | Notes |
|---|---|---|
| Pending transactions | 1,234 | — |

**Pending offline value** (metric tile, from `getGameplaySyncStatus`): Summed across readers.

| Shows | Format | Notes |
|---|---|---|
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Stale edge packages** (metric tile, from `getGameplaySyncStatus`): Count where `edgePackageStale` is true.

| Shows | Format | Notes |
|---|---|---|
| Edge package stale | yes / no (icon or chip) | — |

**Readers and their sync state** (data table, from `getGameplaySyncStatus`): The pack's device table: Offline Since is `oldestPendingAt`, Config Version is `edgePackageVersion`.

| Shows | Format | Notes |
|---|---|---|
| Reader | the name it points at, never the id | — |
| Reader name | text | — |
| Oldest pending at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Edge package version | 1,234 | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**The selected reader** (detail panel, from `getGameplaySyncStatus`): The three offline controls are the pack's; no field or operation carries them.

| Shows | Format | Notes |
|---|---|---|
| Reader | the name it points at, never the id | — |
| Reader name | text | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Oldest pending at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Edge package version | 1,234 | — |
| Edge package stale | yes / no (icon or chip) | — |
| Offline operation allowed | text | not in the schema: `Offline operation allowed` |
| Maximum offline duration | text | not in the schema: `Maximum offline duration` |
| Maximum offline transaction value | text | not in the schema: `Maximum offline transaction value` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Force synchronization (secondary button) | navigation or local | — | — | — | — |
| Block offline operation (destructive button) | navigation or local | — | — | — | — |
| Set maximum offline duration (secondary button) | `setGateOfflinePolicy` PUT `/offline-policies` | AccessOfflinePolicy | AccessOfflinePolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The edge threshold is shorter than the central one. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Readers offline, Pending offline transactions, Pending offline value (AED), Stale edge packages. *(source: contracts/satellite/games.yaml#getGameplaySyncStatus)*
- **Readers table**: Columns Reader, Status, Pending plays, Pending value, Oldest pending ("10:22, 38 min ago"), Last sync, Edge package version (amber "Stale" when out of date). Largest pending value first. *(source: screens/P08-venue-back-office.yaml#BO-470 / contracts/satellite/games.yaml#/components/schemas/ReaderSyncStatus)*
- **Recovery flow**: Reader offline, Operate on cached rules, Store plays, Connection restored, Upload plays, TICVAI reconciles, Synchronised; the selected reader's current step highlighted. *(source: screens/P08-venue-back-office.yaml#BO-470)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Force synchronisation**: Greyed with "Readers send their plays when they reconnect; TICVAI cannot pull them" until an operation exists. *(source: contracts/satellite/games.yaml#syncGamePlays / contracts/satellite/games.yaml#reportReaderQueue)*
- **Block offline operation**: Turns offline decisions off venue-wide and deploys to readers; confirmation per VO-R16 names the readers affected and that offline readers will refuse every tap. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules / contracts/satellite/games.yaml#deployReaderConfiguration)*

**Data it reads**: `getGameplaySyncStatus` (onLoad, What is held offline)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline synchronization recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline synchronization recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline synchronization recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline synchronization recovery are still there. The pack's own statuses are Online — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Edge cases to draw

- **Plays synced against a card with too little balance**: Accepted (the guest already played) and listed as shortfalls for reconciliation, never rejected on sync. *(source: R106 / contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest)*
- **Plays arrive out of order**: Applied in the reader's sequence order with original time and sync time both shown. *(source: DI-065 / contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest)*
- **Edge package expired on an offline reader**: The reader stops approving offline; the row reads "Package expired, refusing taps". *(source: contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*

#### Consistency with other screens

- Match `BO-481`: The offline package and its limits are defined there; the stale flag here refers to that package.
- Match `BO-942`: The resource-management mobile sync monitor uses the same pending, oldest and last-sync pattern.
- Match `BO-132`: Access control's offline reconciliation uses the same words (Sync and reconciliation, per the vocabulary).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
readers:
- reader: R-031 Prize Crane
  status: Offline
  pending: 12
  value: AED 180.00
  oldest: '10:22'
  lastSync: '10:21'
  package: 27, Stale
- reader: R-042 Wave Rider
  status: Offline
  pending: 4
  value: AED 60.00
  oldest: '10:35'
  lastSync: '10:34'
  package: '28'
```

#### Permissions

- `getGameplaySyncStatus` → `PRODUCT_VIEW` (read) · staff
- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-471` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-471`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 14: Works in Offline, Synchronization & Recovery Monitor → Monitor readers or edge components that temporarily lose connectivity with TICVAI and manage recovery/synchronization. This is a TICVAI Recommended Enhancement, based on the architecture we agreed …

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-471?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Force synchronization, Block offline operation, Set maximum offline duration.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-473` Operational Analytics & Reconciliation Dashboard

**Provide management and operations with consolidated performance analytics across gameplay, readers, wallets and redemption.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/operational-analytics-reconciliation-dashboard-bo-473` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No games analytics or reconciliation read (plays, rates, revenue, uptime).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The management view of the games and rides operation over a period: plays, players, money, entitlements, device performance and redemption, with a reconciliation of authorised plays against deductions and confirmed game starts. The one thing to get right: the reconciliation is three numbers and a variance you can click into, and all KPIs are tiles grouped by area, never a table of figures.

**Known correction pending (do not draw the wrong version)**

- **Drawn as listDetail** Why: An analytics dashboard of KPI areas and charts is the command-centre pattern (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-473; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only the offline sync status is bound** Why: Total plays, rates, revenue, uptime and the reconciliation have no operation; the screen's own notes say so for each tile. *(source: contracts/satellite/games.yaml#getGameplaySyncStatus / screens/P08-venue-back-office.yaml#BO-473; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reader performance table built from sync status** Why: Sync status has no uptime or response time; reader performance needs the device register's health and telemetry. *(source: contracts/spine/tenancy.yaml#getDeviceTelemetry / ADR-0067; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period**: Today, Yesterday, Last 7 days, This month, Custom range; compare-to-previous toggle. *(source: designer default)*
- **Filters**: Zone, Attraction type, Attraction. *(source: screens/P08-venue-back-office.yaml#BO-465)*

#### Outputs: what the screen shows and produces

**Shown**

**Total plays** (metric tile): The pack asks for total plays; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Total plays | text | not in the schema: `Total plays` |

**Authorization rate** (metric tile): The pack asks for authorization rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Authorization rate | text | not in the schema: `Authorization rate` |

**Rejection rate** (metric tile): The pack asks for rejection rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Rejection rate | text | not in the schema: `Rejection rate` |

**Reader uptime** (metric tile): The pack asks for reader uptime; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Reader uptime | text | not in the schema: `Reader uptime` |

**Offline readers** (metric tile, from `getGameplaySyncStatus`): The one device KPI the bound read supports: count of readers offline or unreachable.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**Pending offline transactions** (metric tile, from `getGameplaySyncStatus`): Summed across readers; feeds the reconciliation variance.

| Shows | Format | Notes |
|---|---|---|
| Pending transactions | 1,234 | — |

**Plays by attraction and rejection trend** (chart): The pack's analytics set (plays by attraction, revenue by game/ride, peak usage times, rejection trend). No operation returns gameplay aggregates.

| Shows | Format | Notes |
|---|---|---|
| Attraction | text | not in the schema: `Attraction` |
| Plays | text | not in the schema: `Plays` |
| Revenue | text | not in the schema: `Revenue` |
| Rejection rate | text | not in the schema: `Rejection rate` |
| Hour of day | text | not in the schema: `Hour of day` |

**Reconciliation summary** (data table): Clicking the variance drills to missing deduction, missing game-start confirmation, duplicate event or reader communication issue. No operation reconciles these three counts.

| Shows | Format | Notes |
|---|---|---|
| Authorized plays | text | not in the schema: `Authorized plays` |
| Wallet / entitlement transactions | text | not in the schema: `Wallet / entitlement transactions` |
| Confirmed game starts | text | not in the schema: `Confirmed game starts` |
| Variance | text | not in the schema: `Variance` |

**Reader performance** (data table, from `getGameplaySyncStatus`)

| Shows | Format | Notes |
|---|---|---|
| Reader name | text | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Edge package version | 1,234 | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI areas**: Five tile groups - Gameplay (Total plays, Unique players, Authorisation rate, Rejection rate), Revenue and wallet (Paid credit consumed, Bonus consumed, Average spend per play), Entitlements (Package, Free, VIP, Retry plays), Devices (Reader uptime, Offline readers, Average response time), Redemption (Credits earned, Credits redeemed, Outstanding credits). *(source: screens/P08-venue-back-office.yaml#BO-473 / DI-882)*
- **Analytics**: Plays by attraction, Revenue by game or ride, Peak usage (hour by weekday heat map), Reader performance, Rejection trend, Wallet consumption mix, Redemption earned vs redeemed. *(source: screens/P08-venue-back-office.yaml#BO-473)*
- **Reconciliation**: Three numbers in a row - 10,240 Authorised plays, 10,238 Wallet or entitlement transactions, 10,238 Confirmed game starts - and a variance chip "2". Clicking the variance lists the items under Missing deduction, Missing game-start confirmation, Duplicate event, Reader communication issue. *(source: screens/P08-venue-back-office.yaml#BO-473)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Drill into variance**: Opens the list of unmatched plays with links to each decision trace. *(source: screens/P08-venue-back-office.yaml#BO-473)*
- **Export**: Exports the KPI set and charts' data for the period. *(source: designer default)*

**Data it reads**: `getGameplaySyncStatus` (onLoad, Reconciliation)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational analytics reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational analytics reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational analytics reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational analytics reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Offline plays not yet synced**: The reconciliation strip states "Excludes 16 plays still held offline" with a link to BO-471, so the variance is not mistaken for loss. *(source: contracts/satellite/games.yaml#getGameplaySyncStatus)*
- **Anomaly flagged**: Shown as a suggestion with reason; never corrects figures automatically (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-473)*

#### Consistency with other screens

- Match `BO-453`: Same reconciliation strip component as the redemption ledger.
- Match `ANL-003`: Venue analytics' operational performance must report the same play and revenue figures for the same period.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gameplay:
  plays: 10240
  players: 3110
  authRate: 95.9%
  rejectRate: 4.1%
wallet:
  paid: AED 182,440.00
  bonus: AED 21,300.00
  avgPerPlay: AED 19.90
reconciliation:
  authorised: 10240
  deducted: 10238
  started: 10238
  variance: 2
```

#### Permissions

- `getGameplaySyncStatus` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-473` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-473`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 18: Works in Operational Analytics & Reconciliation Dashboard → Provide management and operations with consolidated performance analytics across gameplay, readers, wallets and redemption.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-473?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getDeviceTelemetry": {"method":"GET","path":"/devices/{deviceId}/telemetry","contract":"tenancy","summary":"Battery, performance and consumables over time","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"metric","in":"query","required":null}],"requestBody":null,"responds":"DeviceTelemetryPoint"},
"getGameplaySyncStatus": {"method":"GET","path":"/gameplay-sync-status","contract":"games","summary":"What readers took offline and have not sent","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReaderSyncStatus"},
"listGameEntitlements": {"method":"GET","path":"/game-entitlements","contract":"games","summary":"Passes, packages and per-game entitlements","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameEntitlement"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setGateOfflinePolicy": {"method":"PUT","path":"/offline-policies","contract":"access","summary":"Set the offline policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOfflinePolicy","responds":"AccessOfflinePolicy"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessOfflinePolicy": {"type":"object","x-ticvai-persistence":"access.offline_policy","description":"The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)","required":["id","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"maxOfflineDurationHours":{"type":"integer","minimum":0,"nullable":true,"description":"**Hours a reader may validate offline; past it, readers refuse offline taps** (decided 2 October 2026, Chinmay, critical set 1, BO-471: \"Yes: the venue sets a maximum offline duration; readers then refuse offline taps\"; DEC-426; CHG-CSP-035). Counted from the reader's last successful sync. Past the limit an access gate, a handheld and a games reader refuse every tap they would have validated from their local package (`ValidationResult.denyCause` `offlineLimitExceeded`) until they reconnect; `afterThresholdBehavior` decides only what the operator is shown and whether a supervisor may admit by hand (`supervisorMode`), and none of its values lets a reader keep validating unattended. The limit travels in the offline package (ADR-0068), so a reader that has lost the platform still knows it. Null sets no limit beyond the package's own expiry."},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"],"nullable":true},"revocationTriggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"revocationMaxAllowedAgeMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum allowed revocation cache age"},"revocationStalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"nullable":true,"description":"What devices do when the cache is older than the maximum allowed age"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","default":true,"description":"Switch modes automatically without stopping guest flow"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DeviceTelemetryPoint": {"type":"object","x-ticvai-persistence":"tenancy.device_telemetry","description":"16.4.21 and 16.4.22. **A series, because degradation is not visible in a point-in-time reading.**\n","properties":{"deviceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"batteryPercent":{"type":"integer","nullable":true},"batteryHealthPercent":{"type":"integer","nullable":true},"charging":{"type":"boolean","nullable":true},"signalStrength":{"type":"integer","nullable":true},"cpuPercent":{"type":"number","nullable":true},"memoryPercent":{"type":"number","nullable":true},"storageFreeMb":{"type":"integer","nullable":true},"consumables":{"type":"object","additionalProperties":true,"description":"Paper, ribbon, wristband stock — whatever the device kind reports."},"uptimeSeconds":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"GameEntitlement": {"type":"object","x-ticvai-persistence":"games.entitlement","description":"Board 4. **A right to play, not money** — consumed before money is.","required":["code","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["allGamesPass","unlimitedSingleGame","limitedSingleGame","package","freePlay"]},"gameIds":{"type":"array","items":{"type":"string","format":"uuid"}},"attractionTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"coversGamesAddedLater":{"type":"boolean","default":true,"description":"**Whether a pass sold today covers a game added tomorrow** (Chinmay, 2 October, workbook Q397: \"venue configures; default yes\"; CHG-CSA-028). True, the default: an `allGamesPass`, or a pass bound by `attractionTypeIds`, covers games added after it was sold that match it; the coverage summary says so. False: it covers only the games that existed at sale. A pass listing `gameIds` covers those games only, whatever this says."},"playCount":{"type":"integer","nullable":true,"description":"For `limitedSingleGame` and `package`. Null means unlimited."},"validityKind":{"type":"string","enum":["sameDay","days","untilDate","untilUsed"]},"validityDays":{"type":"integer","nullable":true},"activationKind":{"type":"string","enum":["onPurchase","onFirstUse","onDate"],"default":"onFirstUse","description":"**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"},"dailyPlayCap":{"type":"integer","nullable":true},"cooldownMinutes":{"type":"integer","nullable":true,"description":"**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"},"linkedProductId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderSyncStatus": {"type":"object","description":"Board 8.8. **Revenue the platform has not seen.**","properties":{"readerId":{"type":"string","format":"uuid"},"readerName":{"type":"string"},"pendingTransactions":{"type":"integer"},"pendingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oldestPendingAt":{"type":"string","format":"date-time","nullable":true},"lastSyncAt":{"type":"string","format":"date-time","nullable":true},"edgePackageVersion":{"type":"integer","nullable":true},"edgePackageStale":{"type":"boolean"},"status":{"type":"string","enum":["online","offline","degraded","unreachable"]}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]}
}
```
