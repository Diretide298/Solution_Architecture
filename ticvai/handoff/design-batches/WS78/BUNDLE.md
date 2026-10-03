# WS78 — Game and Ride board 1

**10 screens · 15 operations · 12 schemas · 5 permissions**

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
  `DEVICE_CONFIGURE, DEVICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_CONFIGURE`. A control nobody can use must say so,
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
| `BO-394` | Game & Ride Operations Dashboard | D | 0 | 14 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-395` | Game & Ride Directory | A | 28 | 6 | 6 | 1 | 2 | 6 | — | notStarted (—) |
| `BO-396` | Attraction Profile | D | 1 | 15 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-397` | Attraction Type Configuration | D | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-398` | Game & Ride Operational Configuration | D | 6 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-399` | Wallet & Credit Acceptance Mapping | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-400` | Attraction / Reader Mapping | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-401` | Game Package & Entitlement Association | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-402` | Configuration Health & Validation | D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-403` | Attraction Audit, Dependencies & Governed Actions | B | 0 | 11 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-398, BO-399, BO-401, BO-403 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-394` Game & Ride Operations Dashboard

**Provide management with one central view of the operational and configuration status of all games, rides, skill games, video games and redemption games.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-394 |
| Who uses it | venue staff holding `DEVICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-operations-dashboard-bo-394` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Games & Rides board's command centre: one view of every game and ride (in this module an "attraction" is an individual game or ride, never a venue) with its operational and configuration status, for the games manager and duty manager. KPI tiles on top, the alerts that need action, then the Attraction Status Overview list the pack puts on page 4, which the generator dropped. The one thing to get right: a manager must see at a glance which machines cannot take money right now and why (out of service, maintenance, reader offline, configuration error), not just a count.

**Known correction pending (do not draw the wrong version)**

- **The Attraction Status Overview list (pack p4) and the five status indicators are missing from the screen; only the KPI tiles were carried** Why: The pack's acceptance criterion is identifying status from a single screen, which tiles alone cannot do. *(source: screens/P08-venue-back-office.yaml#BO-395 / screens/P08-venue-back-office.yaml#BO-394; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **confirmDisableAttraction says the action is not reversible** Why: outOfService returns to inService through updateGame; only retirement is terminal. *(source: contracts/satellite/games.yaml#updateGame; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **createGame bound as serving "Disable Attraction"** Why: Disable is updateGame (status outOfService); createGame serves Add only. *(source: screens/P08-venue-back-office.yaml#BO-394; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Reader KPIs (Active readers, Reader faults) have no bound read (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should Configuration error in the status chip come from a nightly validateGameConfiguration run, or be computed live on load?** → Drawn default accepted: Show the result of the last run with its time ("Checked 06:00") and a Validate now link to BO-402. *(decided by Chinmay, 2026-10-02; DEC-374 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters (venue, zone, type, status)**: Venue comes from the top-bar venue switcher (per VO-R09), so the filter row is Zone, Attraction type (Ride, Skill game, Video game, Redemption game) and Status chips. Status is sent to listGames; zone and type filter client-side because listGames takes only venueId and status. *(source: screens/P08-venue-back-office.yaml#BO-395 / contracts/satellite/games.yaml#listGames)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Attractions** (metric tile)

**Active Attractions** (metric tile)

**Offline / Unavailable** (metric tile)

**Active Readers** (metric tile)

**Reader Faults** (metric tile)

**Transactions Today** (metric tile)

**Wallet Credits Consumed** (metric tile)

**Redemption Credits Earned** (metric tile)

**Readers** (data table, from `listReaders`)

| Shows | Format | Notes |
|---|---|---|
| Device | the name it points at, never the id | `tenancy.RegisteredDevice`. Enrolment, firmware and tamper state live there. |
| Game | the name it points at, never the id | — |
| Reader profile | the name it points at, never the id | — |
| Accepted credit types | list or chips (count when long) | — |
| Accepts direct pay | yes / no (icon or chip) | — |
| Retap delay seconds | 1,234 | The setting that stops a guest paying twice for one go. A wristband held against a reader for a second and a half is two taps to the … |
| Display rules | grouped details | — |
| Free game glow | yes / no (icon or chip) | What tells a guest their entitlement was used rather than their money. Without it the complaint arrives at the desk. |
| Show balance | yes / no (icon or chip) | — |
| Show price | yes / no (icon or chip) | — |
| Theme code | text | — |
| Languages | list or chips (count when long) | — |
| Io mapping | grouped details | Board 9.6. Which output starts the game, which input reports it finished. |
| Status | chip: Unconfigured, Active, Offline, Maintenance, Disabled | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add Attraction (primary button) | navigation or local | — | — | — | — |
| Open Attraction (secondary button) | navigation or local | — | — | — | — |
| Disable Attraction (destructive button) | navigation or local | — | — | — | — |
| View Configuration (secondary button) | navigation or local | — | — | — | — |
| View Reader (secondary button) | navigation or local | — | — | — | — |
| View Transactions (secondary button) | navigation or local | — | — | — | — |
| Filter by venue/zone/type/status (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Eight metric tiles (per VO-R02), never table columns. Total / Active / Offline-Unavailable attractions count listGames by status (inService = Active; outOfService, maintenance = Offline / Unavailable; retired excluded from Total). Active readers and Reader faults count listReaders by status (active vs offline/disabled/unconfigured). Transactions today counts today's listGameplayTransactions; Wallet credits consumed sums Game.creditsTakenToday; Redemption credits earned sums Game.pointsAwardedToday. Each tile opens the filtered list below. *(source: screens/P08-venue-back-office.yaml#BO-394 / contracts/satellite/games.yaml#/components/schemas/Game / contracts/satellite/games.yaml#listReaders)*
- **Attraction Status Overview**: A compact list under the tiles with the pack's columns - Attraction name, Code, Type, Zone, Reader, Current status, Wallet enabled, Current price, Last transaction. Status is one chip from the pack's five indicators (Active, Inactive, Maintenance, Reader offline, Configuration error) with a precedence order - Maintenance and Inactive come from the game, Reader offline from its reader, Configuration error from the last health check - so a row shows its worst state. Sort worst first. *(source: screens/P08-venue-back-office.yaml#BO-395 / contracts/satellite/games.yaml#validateGameConfiguration)*
- **Alerts**: Above the list - readers offline, games with a blocking health finding, games in maintenance - each with a link to the screen that fixes it (the health finding's fixOn names it). *(source: screens/P08-venue-back-office.yaml#BO-395 / contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*
- **Tiles to the board's screens**: Tiles open BO-395 to BO-403 and those return here (per VO-R13); the dashboard is the seeded configuration of the one command-centre pattern, not a hand-built page. *(source: ADR-0041)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add Attraction**: Opens BO-396 empty (create mode); the created game starts Out of service until configured. *(source: contracts/satellite/games.yaml#createGame / contracts/satellite/games.yaml#cloneGame)*
- **Disable Attraction**: Sets the selected game Out of service via updateGame. Confirmation names the game, that readers will refuse taps with "Game unavailable", and the count of active packages that include it. It is reversible (Return to service), so the dialog must not say "not reversible". *(source: screens/P08-venue-back-office.yaml#BO-403 / contracts/satellite/games.yaml#updateGame)*
- **View Configuration / View Reader / View Transactions**: Row actions navigating to BO-396, BO-405 (filtered to the game's reader) and the transaction monitor filtered to the game. *(source: screens/P08-venue-back-office.yaml#BO-395)*

**Data it reads**: `listGames` (onLoad, Games and rides today); `listGameplayTransactions` (onLoad, Live taps); `listReaders` (onLoad, Readers and their health, for the reader tiles)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-395` Game & Ride Directory: *Game & Ride Directory*; carries `gameId`
- → `BO-396` Attraction Profile: *Attraction Profile*; carries `gameId`
- → `BO-397` Attraction Type Configuration: *Attraction Type Configuration*
- → `BO-398` Game & Ride Operational Configuration: *Game & Ride Operational Configuration*; carries `gameId`
- → `BO-399` Wallet & Credit Acceptance Mapping: *Wallet & Credit Acceptance Mapping*
- → `BO-400` Attraction / Reader Mapping: *Attraction / Reader Mapping*; carries `readerId`
- → `BO-401` Game Package & Entitlement Association: *Game Package & Entitlement Association*
- → `BO-402` Configuration Health & Validation: *Configuration Health & Validation*
- → `BO-403` Attraction Audit, Dependencies & Governed Actions: *Attraction Audit, Dependencies & Governed Actions*

**What opens over it**

- confirmDialog *Disable Attraction*: **Disable Attraction on a game ride operations is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operations are still there. The pack's own statuses are Active — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … |

#### Edge cases to draw

- **Game in maintenance from a work order**: Chip shows Maintenance with the work-order reference; Disable is not offered (status is owned by maintenance until verified back). *(source: contracts/satellite/games.yaml#updateGame)*
- **Reader offline but deciding from its edge package**: Status Reader offline (amber, not red) with "deciding offline, last sync HH:MM"; transactions keep arriving after sync. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Viewer without PRODUCT_CONFIGURE**: Add and Disable disabled with "Needs product configuration rights" (per VO-R08); list stays readable with PRODUCT_VIEW. *(source: contracts/satellite/games.yaml#createGame)*

#### Consistency with other screens

- Match `BO-404`: Reader tiles and reader status chips use the same labels and colours as the Reader Management Dashboard.
- Match `BO-424`: Transactions today here equals Gameplay requests today on BO-424 for the same venue and day.
- Match `BO-069`: Maintenance status is set from the Asset Register / work orders; same chip and wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  totalAttractions: 42
  activeAttractions: 37
  offlineUnavailable: 5
  activeReaders: 46
  readerFaults: 2
  transactionsToday: 3184
  walletCreditsConsumed: AED 41,260.00
  redemptionCreditsEarned: 186400
rows:
- name: Falcon Coaster
  code: RIDE-FALCON
  type: Ride
  zone: Thrill Zone
  reader: R-001
  status: Active
  wallet: Enabled
  price: AED 35.00
  last: '10:42'
- name: VR Racing
  code: VID-VRRACE-01
  type: Video game
  zone: Arcade
  reader: R-014
  status: Active
  wallet: Enabled
  price: AED 20.00
  last: '10:41'
- name: Basketball Pro
  code: SKL-BBALL-02
  type: Skill game
  zone: Sports Arcade
  reader: —
  status: Configuration error
  wallet: Enabled
  price: AED 20.00
  last: 09:58
- name: Prize Crane
  code: RED-CRANE-04
  type: Redemption game
  zone: Fun Zone
  reader: R-031
  status: Reader offline
  wallet: Enabled
  price: AED 15.00
  last: '10:15'
- name: Bumper Cars
  code: RIDE-BUMPER
  type: Ride
  zone: Family Zone
  reader: R-007
  status: Maintenance
  wallet: Enabled
  price: AED 25.00
  last: 08:30
```

#### Permissions

- `listGames` → `PRODUCT_VIEW` (read) · staff
- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `listReaders` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-394` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-394`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 1: Opens Game & Ride Operations Dashboard → Provide management with one central view of the operational and configuration status of all games, rides, skill games, video games and redemption games.
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F187 branch at step 1 (expected): when Nothing has been set up on Game & Ride Operations Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F187 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-394?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add Attraction, Open Attraction, Disable Attraction, View Configuration, View Reader, View Transactions, Filter by venue/zone/type/status.
- [ ] Every transition is wired: `BO-100`, `BO-395`, `BO-396`, `BO-397`, `BO-398`, `BO-399`, `BO-400`, `BO-401`, `BO-402`, `BO-403`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-395` Game & Ride Directory

**Maintain the master catalogue of all attractions participating in the payment/redemption ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 1 · needs the `games` module |
| Block | Block A · task VM-BO-395 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as guest, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Field Description) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-directory-bo-395` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The master catalogue of games and rides - the one list a games administrator searches, filters, creates, clones, activates and deactivates attractions from. It is the list half of the attraction editor (BO-396 is its detail). The one thing to get right: Clone, because a venue adds a row of identical machines by copying one, and a clone must arrive out of service and unbound to any reader.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Type, Reader type, Wallet enabled and Redemption have no contract field on Game (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Redemption drawn as a text field "Redemption Earn / Spend / N/A" (CHG-SBO-009); apisNote says cloneGame is "still owed by a contract change" (CHG-SBO-009); Activate/Deactivate from the pack actions is missing from the action bar (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the directory venue-scoped only, or does a group operator need a cross-venue catalogue (all parks of Yas Leisure Group)?** → Drawn default accepted: Venue-scoped from the switcher, as listGames is. *(decided by Chinmay, 2026-10-02; DEC-375 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, attraction type, reader type, wallet enabled, redemption enabled and 1 more — which are present is a decision the pack already made. | — |
| Redemption | select field | — | — | — | — | Earn, Spend or N/A: a chip column in the directory and a select in the editor; the pack's "Earn / Spend / N/A" was a sample value in the label. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |

**Form: Create** (modal, opened by *Create*; *Create* calls `createGame`, *Cancel* sends nothing)

**Collects what `createGame` sends before it is called.** Required: `code`, `name`, `venueId`, `creditCost`, `status`. Optional: `zone`, `assetId`, `readerId`, `minPointsAwarded`, `maxPointsAwarded`, `heightRequirementCm`, `playsToday`, `creditsTakenToday`, `pointsAwardedToday`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGame` body |
| Code `code` | text field | required | — | max length 64 | — | — | `createGame` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createGame` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createGame` body |
| Zone `zone` | text field | optional | — | — | — | — | `createGame` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits. | `createGame` body |
| Reader `readerId` | picker: choose a reader | optional | — | — | shows names, sends the id | — | `createGame` body |
| Credit cost `creditCost` | number field | required | — | min 1 | — | — | `createGame` body |
| Min points awarded `minPointsAwarded` | number field | optional | — | — | — | — | `createGame` body |
| Max points awarded `maxPointsAwarded` | number field | optional | — | — | — | — | `createGame` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createGame` body |
| Status `status` | radio group | required | — | In service · Out of service · Maintenance · Retired | — | — | `createGame` body |
| Plays today `playsToday` | number field | optional | — | — | — | — | `createGame` body |
| Credits taken today `creditsTakenToday` | number field | optional | — | — | — | — | `createGame` body |
| Points awarded today `pointsAwardedToday` | number field | optional | — | — | — | — | `createGame` body |

**Form: Edit** (modal, opened by *Edit*; *Edit* calls `updateGame`, *Cancel* sends nothing)

**Collects what `updateGame` sends before it is called.** Nothing in the body is required. Optional: `name`, `creditCost`, `minPointsAwarded`, `maxPointsAwarded`, `heightRequirementCm`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateGame` body |
| Credit cost `creditCost` | number field | optional | — | min 1 | — | — | `updateGame` body |
| Min points awarded `minPointsAwarded` | number field | optional | — | min 0 | — | — | `updateGame` body |
| Max points awarded `maxPointsAwarded` | number field | optional | — | min 0 | — | — | `updateGame` body |
| Status `status` | radio group | optional | — | In service · Out of service · Maintenance · Retired | — | — | `updateGame` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateGame` body |

Errors to draw in the form: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move …

**Form: Clone** (modal, opened by *Clone*; *Clone* calls `cloneGame`, *Cancel* sends nothing)

**Collects what `cloneGame` sends before it is called.** Required: `code`, `name`. Optional: `includeReaders`, `includePricing`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `cloneGame` body |
| Name `name` | text field | required | — | max length 200 | — | — | `cloneGame` body |
| Include readers `includeReaders` | toggle | optional | off | — | — | — | `cloneGame` body |
| Include pricing `includePricing` | toggle | optional | on | — | — | — | `cloneGame` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` already used by another game in the venue.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **search**: Matches attraction name (English and Arabic) and code; code match ranks first. *(source: designer default)*
- **filters**: Seven filters from the pack as chips - Zone, Attraction type, Reader type, Wallet enabled, Redemption enabled, Status (Venue comes from the venue switcher). Type and Reader type are closed sets (Ride, Skill game, Video game, Redemption game; reader types add Balance check), never free text. *(source: screens/P08-venue-back-office.yaml#BO-396)*
- **Clone dialog (code, name, includeReaders, includePricing)**: Code required and unique in the venue (max 64), name required (max 200). "Copy pricing" ticked by default, "Copy reader settings" unticked by default with the help "Reader settings are copied but assigned to no reader until you assign one". Plays and history are never copied - say so. *(source: contracts/satellite/games.yaml#cloneGame)*

#### Outputs: what the screen shows and produces

**Shown**

**Games and rides** (data table, from `listGames`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Zone | text | — |
| Credit cost | 1,234 | — |
| Status | chip: In service, Out of service, Maintenance, Retired | — |
| Plays today | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | `createGame` POST `/games` | Game | Game | — | opens modal first |
| Edit (secondary button) | `updateGame` PATCH `/games/{gameId}` | inline | Game | 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … | opens modal first |
| Clone (secondary button) | `cloneGame` POST `/games/{gameId}/clone` | inline | Game | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` already used by another game in the venue. | opens modal first |
| Activate or deactivate (secondary button) | `updateGame` PATCH `/games/{gameId}` | inline | Game | 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Main grid**: Columns per the pack - Code, Name, Type, Zone, Reader type, Wallet (Enabled / Disabled), Redemption (Earn / Spend / N/A), Status. Attraction ID is never a column (system id, shown only in the detail footer). Redemption is a three-value chip, not the text field the generator drew. *(source: screens/P08-venue-back-office.yaml#BO-395 / screens/P08-venue-back-office.yaml#BO-396)*
- **Status chip**: Pack statuses Active / Inactive / Maintenance map to inService / outOfService / maintenance; retired rows are hidden by default behind a "Show retired" toggle. *(source: screens/P08-venue-back-office.yaml#BO-396 / contracts/satellite/games.yaml#/components/schemas/GameStatus)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create**: Opens BO-396 in create mode. *(source: contracts/satellite/games.yaml#createGame)*
- **Clone**: Dialog as above; on success the new row appears with status Inactive and a banner "Copied from VR Racing 01 - out of service until you put it in service" with a link to BO-396. 409 shows "This code is already used by another game in Summit Peaks" against the code field. *(source: contracts/satellite/games.yaml#cloneGame)*
- **Activate / Deactivate**: Row action; Deactivate sets Out of service with a reason (audited), Activate returns it to service. Refused with the reason when the game is in maintenance (only the work order's verification returns it). *(source: screens/P08-venue-back-office.yaml#BO-396 / contracts/satellite/games.yaml#updateGame)*
- **Export**: Exports the filtered grid (CSV/XLSX) through reporting; the export carries the filters used. *(source: screens/P08-venue-back-office.yaml#BO-395)*

**Data it reads**: `listGames` (onLoad, The directory)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move …; 409 `code` already used by another game in the venue. |

#### Edge cases to draw

- **Bulk machines of one kind**: Clone allows a quantity with an auto-incremented code suffix (VR-RACE-02, -03) only if the contract allows it; until then one clone per action. *(source: contracts/satellite/games.yaml#cloneGame)*
- **Directory with hundreds of machines**: Reference list, normal paging allowed (per VO-R12), sticky header, type grouping optional. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039)*

#### Consistency with other screens

- Match `BO-394`: Same status chips, same type names; the dashboard's overview list is this grid filtered and sorted worst-first.
- Match `BO-396`: Edit opens the same editor; the grid's columns are the editor's General Information fields.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- code: VID-VRRACE-01
  name: VR Racing 01
  nameAr: سباق الواقع الافتراضي 01
  type: Video game
  zone: Arcade
  readerType: Video game reader
  wallet: Enabled
  redemption: N/A
  status: Active
- code: SKL-BBALL-02
  name: Basketball Pro 02
  type: Skill game
  zone: Sports Arcade
  readerType: Skill game reader
  wallet: Enabled
  redemption: Earn
  status: Active
- code: RED-CRANE-04
  name: Prize Crane 04
  type: Redemption game
  zone: Fun Zone
  readerType: Redemption game reader
  wallet: Enabled
  redemption: Earn
  status: Active
- code: RIDE-WAVE
  name: Wave Rider
  type: Ride
  zone: Aqua Park Splash Zone
  readerType: Ride reader
  wallet: Enabled
  redemption: N/A
  status: Inactive
```

#### Permissions

- `listGames` → `PRODUCT_VIEW` (read) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `cloneGame` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*
- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-395` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-395`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F18 *A guest plays an arcade game*, step 3: Machine records the play → **Offline, journalled, synced later**
- Flow F18 *A guest plays an arcade game*, step 4: Machine goes out of service → The asset cascade closes it
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 2: Works in Game & Ride Directory → Maintain the master catalogue of all attractions participating in the payment/redemption ecosystem.
- Flow F18 branch at step 3 (recoverable): when The card has no credits, Refused at the machine. **Offline, so the machine must know the balance** — which means the balance is on the card as well as the server, and they will disagree.
- Flow F18 branch at step 3 (requiresStaff): when The card balance and the server disagree after sync, **The card wins for plays already taken** — the guest played, and reversing it is not possible. The difference is a reconciliation item.
- Flow F18 branch at step 4 (requiresStaff): when The machine fails mid-play, A credit was taken and no play happened. **Refund or replay is a policy nobody has stated**, and it happens often enough to matter.

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-395?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Edit, Clone, Activate or deactivate.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-396` Attraction Profile

**Create or maintain the master record for an individual game or ride.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-396 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Transaction Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/attraction-profile-bo-396` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): getGameCard reads a guest card's balances (guest audience, by cardCode) and has nothing to do with an attraction; the editor reads the Game from listGames …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The attraction editor: the master record of one game or ride and how it takes part in payment, entitlement and redemption. The pack sections are General information, Transaction configuration (what value it accepts) and Device association, with Save draft / Validate / Activate / Deactivate. The one thing to get right: the type's defaults flow into the attraction and each override is visible as an override (pack p7 "Type default / Attraction override"), so nobody has to configure 40 machines one switch at a time.

**Known correction pending (do not draw the wrong version)**

- **Only "Wallet Payment Enabled" was carried; 1 of 28 pack bullets on the screen** Why: Description, type, operator, the other five transaction switches and the device association panel are all on pack pages 5-6. *(source: screens/P08-venue-back-office.yaml#BO-396 / screens/P08-venue-back-office.yaml#BO-397; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Game has no attractionTypeId, description, operator or transaction switches** Why: Without a type link, type defaults (BO-397) cannot flow into the attraction, which is the pack's inheritance requirement and DI-864's template ask. *(source: screens/P08-venue-back-office.yaml#BO-398 / contracts/satellite/games.yaml#/components/schemas/Game / DI-864; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **createGame lists id and the counters playsToday, creditsTakenToday, pointsAwardedToday as request fields** Why: Server-owned and computed (per VO-R03); a create sends none of them. *(source: contracts/satellite/games.yaml#createGame; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen's load read is getGameCard ("The attraction profile") (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does "Save draft" exist as a distinct state, or is draft simply Out of service before first activation?** → Drawn default accepted: Treat draft as Out of service with a "Never activated" badge; no separate status. *(decided by Chinmay, 2026-10-02; DEC-376 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet Payment Enabled | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Attraction ID**: System generated; never an input (per VO-R03); shown read-only in the header after create. *(source: screens/P08-venue-back-office.yaml#BO-396)*
- **code / name / description**: Code unique in the venue, max 64, upper-case suggested; name max 200 with Arabic variant (per VO-R10); description multi-line. Code read-only once the game has transactions. *(source: contracts/satellite/games.yaml#/components/schemas/Game)*
- **attraction type**: Select from BO-397's types (Ride, Skill game, Video game, Redemption game at minimum). Changing type re-applies type defaults to every field not overridden and warns with the list of changed defaults. *(source: screens/P08-venue-back-office.yaml#BO-396 / screens/P08-venue-back-office.yaml#BO-398 / DI-864)*
- **zone / location, operator, asset**: Zone is a pick from the venue topology, not free text; Operator is the concession or team running it; Asset links the maintenance record so maintenance takes it out of service. *(source: screens/P08-venue-back-office.yaml#BO-396 / contracts/satellite/games.yaml#createGame)*
- **price and payout (creditCost, minPointsAwarded, maxPointsAwarded, heightRequirementCm)**: Credit cost at least 1; min points not above max points; height in cm only when the type has a height restriction. Price itself is set on the pricing board (BO-435); show the current effective price read-only with a link. *(source: contracts/satellite/games.yaml#/components/schemas/Game / contracts/satellite/games.yaml#getGamePricing)*
- **transaction configuration**: Six switches from the pack - Wallet payment, Credit payment, Bonus accepted, Entitlement accepted, Redemption credits generated, Free play supported - each showing "Type default - On" with an Override control. *(source: screens/P08-venue-back-office.yaml#BO-396 / screens/P08-venue-back-office.yaml#BO-397 / screens/P08-venue-back-office.yaml#BO-398)*

#### Outputs: what the screen shows and produces

**Shown**

**Attraction** (data table, from `listGames`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Zone | text | — |
| Asset | the image or video | The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits. |
| Reader | the name it points at, never the id | — |
| Credit cost | 1,234 | — |
| Min points awarded | 1,234 | — |
| Max points awarded | 1,234 | — |
| Height requirement cm | 1,234 | — |
| Status | chip: In service, Out of service, Maintenance, Retired | — |
| Plays today | 1,234 | — |
| Credits taken today | 1,234 | — |
| Points awarded today | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save game (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Device association panel**: Read-only - assigned reader, reader profile, device id, connection status with last heartbeat - with "Change reader" opening BO-408. Never edited here (the pack keeps reader detail on Board 2). *(source: screens/P08-venue-back-office.yaml#BO-397 / screens/P08-venue-back-office.yaml#BO-399)*
- **Status header**: Status chip, "Last changed by <name>, <time>" and the latest health result (Ready / Warning / Configuration error). *(source: screens/P08-venue-back-office.yaml#BO-402)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft**: Saves without putting the game in service; a new game stays Out of service. *(source: screens/P08-venue-back-office.yaml#BO-397 / contracts/satellite/games.yaml#createGame)*
- **Validate**: Runs validateGameConfiguration for this game and shows the findings inline with links to the fixing screen. *(source: contracts/satellite/games.yaml#validateGameConfiguration)*
- **Activate**: Puts the game in service; blocked while any blocking finding exists ("Wallet enabled but no valid price configuration found"), with the finding named. *(source: screens/P08-venue-back-office.yaml#BO-402 / contracts/satellite/games.yaml#updateGame)*
- **Deactivate**: Takes the game out of service with a reason; confirmation names packages and entitlements that reference it. *(source: screens/P08-venue-back-office.yaml#BO-403)*

**Data it reads**: `listGames` (onLoad, The attraction being edited (filtered to gameId))

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … |

#### Edge cases to draw

- **Credit cost changed while plays are in flight**: 409 shown as "Plays on this game are in progress; the new price applies once they finish. Try again in a moment." *(source: contracts/satellite/games.yaml#updateGame)*
- **Type changed on a game with an active entitlement restricted to the old type**: Warn with the entitlement names before save. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Consistency with other screens

- Match `BO-397`: Same six transaction switches and the same names as the type's defaults; inheritance shown identically.
- Match `BO-398`: Operational state and the transaction-availability switches are the live overlay of these defaults; draw BO-398 as the Operations tab of this editor (per VO-R14).
- Match `BO-399`: Accepted value types and their priority are the Wallet & Credit Acceptance tab of the same editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attraction:
  code: SKL-BBALL-02
  name: Basketball Pro 02
  nameAr: كرة السلة برو 02
  description: Two-hoop timed shooting game, 60 seconds
  type: Skill game
  zone: Sports Arcade
  operator: Summit Peaks Arcade team
  creditCost: 20
  minPoints: 10
  maxPoints: 400
  status: Active
transaction:
  walletPayment: On (type default)
  bonusAccepted: On (type default)
  entitlementAccepted: On (type default)
  redemptionGenerated: On (override)
  freePlay: Off (type default)
device:
  reader: R-023
  profile: Skill Game Standard
  deviceId: GRD-SP-0023
  connection: Online, heartbeat 10:40
```

#### Permissions

- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGames` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-396` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-396`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 4: Works in Attraction Profile → Create or maintain the master record for an individual game or ride.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-396?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save game, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-397` Attraction Type Configuration

**Configure reusable categories for games and rides so common rules do not have to be configured separately for every attraction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-397 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/attraction-type-configuration-bo-397` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The attraction type library: reusable categories (Ride, Skill game, Video game, Redemption game) that carry the defaults every attraction of that type inherits - default reader type, which value types are allowed, retry and VIP pricing support, free play. The one thing to get right: the type decides which settings even apply (a ride has height and cycle time, a redemption game has a ticket payout), so the type editor shows both the pack's commercial switches and the contract's applicability flags.

**Known correction pending (do not draw the wrong version)**

- **Type name, Type code and Description drawn as select fields; Wallet allowed as a select** Why: Name, code and description are text the administrator types; Wallet allowed is a switch. *(source: screens/P08-venue-back-office.yaml#BO-397; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **AttractionType has none of the pack's commercial defaults (default reader type, wallet, bonus, entitlement, redemption earning, retry, VIP, free play)** Why: The contract's flags are applicability (payout, direct pay, cycle time, height); the pack's inheritance needs the commercial defaults on the type and an override on the game. *(source: screens/P08-venue-back-office.yaml#BO-398 / contracts/satellite/games.yaml#/components/schemas/AttractionType; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **setAttractionType lists id and scopePath as request fields** Why: Server-owned (per VO-R03). *(source: contracts/satellite/games.yaml#setAttractionType; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are attraction types tenant-wide (as setAttractionType's scope says) or per venue?** → Drawn default accepted: Tenant-wide, read-only to venue users without tenant configuration rights. *(decided by Chinmay, 2026-10-02; DEC-377 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Type Name | select field | — | — | — | — | — | — |
| Type Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Default Reader Type | select field | — | — | — | — | — | — |
| Wallet Allowed | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **type name / type code / description**: Free text name with Arabic variant and a unique code - these are text inputs, not the select fields the generator drew. Code read-only once any attraction uses the type. *(source: screens/P08-venue-back-office.yaml#BO-397 / contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **family**: Closed set from the contract (Ride, Arcade game, Redemption game, Crane, VR experience, Soft play, Attraction, Show); drives which flags default on. *(source: contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **default reader type**: Select from the reader types (Ride, Skill game, Video game, Redemption game, Balance check reader). *(source: screens/P08-venue-back-office.yaml#BO-397 / screens/P08-venue-back-office.yaml#BO-405)*
- **commercial defaults**: Switches - Wallet allowed, Bonus allowed, Entitlement allowed, Redemption earning, Retry supported, VIP pricing supported, Free play supported. Retry supported defaults on only for Skill games (pack example); Redemption earning for Skill and Redemption games. *(source: screens/P08-venue-back-office.yaml#BO-397 / screens/P08-venue-back-office.yaml#BO-398)*
- **applicability flags**: Has ticket payout, Has direct pay, Has cycle time (default on), Has height restriction, Supports entitlements (default on) - shown as "Settings that apply to this type". *(source: contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **id, scopePath**: Never inputs (per VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Type directory**: Cards or rows per type listing its enabled behaviours as chips (Ride - Wallet payment, Entitlement, Free ride, VIP pricing; Skill game - Wallet payment, Retry pricing, Redemption earning), plus the count of attractions using it. *(source: screens/P08-venue-back-office.yaml#BO-397)*
- **Inheritance preview**: A two-column "Type default / Attraction override" table listing attractions that override any default, so a type change shows who is not affected. *(source: screens/P08-venue-back-office.yaml#BO-398)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save type**: Sends the whole type (PUT, per VO-R04). Confirmation says "Applies to 18 attractions that use the default; 3 attractions with overrides keep their own value". *(source: contracts/satellite/games.yaml#setAttractionType)*
- **New type**: Opens an empty type with family-driven defaults; no id field. *(source: contracts/satellite/games.yaml#setAttractionType)*

**Data it reads**: `listAttractionTypes` (onLoad, Types defined)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Turning off Has height restriction while attractions of the type carry a height requirement**: Warn that those requirements will no longer be enforced at the reader, with the list. *(source: contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **Type written at tenant scope**: setAttractionType is tenant-scoped while the list is venue-scoped; show "Shared by all venues of Yas Leisure Group" on the editor and restrict Save to tenant administrators. *(source: contracts/satellite/games.yaml#setAttractionType / ADR-0018)*

#### Consistency with other screens

- Match `BO-396`: Same switch names and order as the attraction's Transaction configuration.
- Match `BO-405`: Reader type list identical to the Reader Directory's reader types.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
types:
- name: Ride
  code: RIDE
  family: ride
  defaultReader: Ride reader
  wallet: true
  entitlement: true
  freePlay: true
  vip: true
  retry: false
  cycleTime: true
  height: true
  attractions: 14
- name: Skill game
  code: SKILL
  family: arcadeGame
  defaultReader: Skill game reader
  wallet: true
  retry: true
  redemption: true
  attractions: 11
- name: Video game
  code: VIDEO
  family: arcadeGame
  defaultReader: Video game reader
  wallet: true
  bonus: true
  attractions: 9
- name: Redemption game
  code: REDEMPTION
  family: redemptionGame
  defaultReader: Redemption game reader
  wallet: true
  redemption: true
  ticketPayout: true
  attractions: 8
```

#### Permissions

- `listAttractionTypes` → `PRODUCT_VIEW` (read) · staff
- `setAttractionType` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-397` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-397`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 6: Works in Attraction Type Configuration → Configure reusable categories for games and rides so common rules do not have to be configured separately for every attraction.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-397?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-398` Game & Ride Operational Configuration

**Configure whether an attraction is currently available for customer transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-398 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-operational-configuration-bo-398` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of a game's operational configuration (no GET /games/{gameId}/operations).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Whether an attraction can take customer transactions right now, without deleting or rebuilding its configuration: operational state, which value types are allowed at this moment, an effective period, a message shown to guests and operators, and the reason. It is also where cycle time, capacity, height and age restrictions and operating hours live in the contract. The one thing to get right: a time-boxed unavailability ("Ride temporarily unavailable", maintenance until 14:00) that ends by itself.

**Known correction pending (do not draw the wrong version)**

- **The screen has no content region; the gap says the pack gives it nothing that can be drawn** Why: Pack p7 lists Operational state, five Transaction availability switches, Effective from/to, Operational message and Governance fields; the extraction missed them. *(source: screens/P08-venue-back-office.yaml#BO-398; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A PUT bound with no read of the current operational configuration** Why: Whole-row PUT (per VO-R04) needs the stored values to pre-fill; there is no GET on /games/{gameId}/operations. *(source: contracts/satellite/games.yaml#setGameOperationalConfiguration; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only setGameOperationalConfiguration (capacity, cycle, restrictions) is bound; nothing sets the state, period, message or availability … (CHG-WIR-001); DI-864 maintenance mode "for a defined period" cannot be set from this board (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should an operator be able to put a game into maintenance for a defined period without a work order (DI-864), or is Out of service with an effective period the answer?** → Drawn default accepted: Draw Out of service with an end time and offer "Raise a work order" for real maintenance. *(decided by Chinmay, 2026-10-02; DEC-378 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Form: Change availability** (modal, opened by *Change availability*; *Change availability* calls `updateGame`, *Cancel* sends nothing)

**Collects what `updateGame` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateGame` body |
| Credit cost `creditCost` | number field | optional | — | min 1 | — | — | `updateGame` body |
| Min points awarded `minPointsAwarded` | number field | optional | — | min 0 | — | — | `updateGame` body |
| Max points awarded `maxPointsAwarded` | number field | optional | — | min 0 | — | — | `updateGame` body |
| Status `status` | radio group | optional | — | In service · Out of service · Maintenance · Retired | — | — | `updateGame` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateGame` body |

Errors to draw in the form: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **operational state**: Active / Inactive / Maintenance (pack). Active and Inactive map to inService / outOfService. Maintenance cannot be chosen here - only a work order puts a game in maintenance - so show it read-only with the work-order link when set, and offer "Raise a work order" instead. *(source: screens/P08-venue-back-office.yaml#BO-398 / contracts/satellite/games.yaml#updateGame)*
- **transaction availability**: Five switches (Allow wallet payment, bonus, entitlement, free play, redemption earning). Each can only narrow what BO-396 / the type allows; a switch the attraction does not support is shown disabled with "Not enabled on this attraction". *(source: screens/P08-venue-back-office.yaml#BO-398)*
- **effective from / to**: Date-time pickers in venue time; To after From; empty To = until changed. When To passes, the state returns to the previous one automatically - say so under the fields. *(source: screens/P08-venue-back-office.yaml#BO-398 / DI-864)*
- **operational message**: Optional, max one short line, English and Arabic, shown on the reader and the guest app; preset "Ride temporarily unavailable". *(source: screens/P08-venue-back-office.yaml#BO-398)*
- **reason for status change**: Required whenever the state changes; Changed by and Changed at are shown, never entered. *(source: screens/P08-venue-back-office.yaml#BO-398)*
- **operations (cycleSeconds, riderCapacity, min/max height, minimumAge, supervisionRequiredBelowAge, healthRestrictions …**: A second section "Capacity and restrictions". Throughput per hour is computed and read-only (riderCapacity x 3600 / cycleSeconds). Max height not below min height. Health restrictions as chips (pregnancy, heart condition, back or neck problems). Operating hours as weekly windows (days chips + HH:MM from/to); empty = follows the venue's hours. *(source: contracts/satellite/games.yaml#/components/schemas/GameOperationalConfig)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Change availability (secondary button) | `updateGame` PATCH `/games/{gameId}` | inline | Game | 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Current state banner**: "In service" / "Out of service until 14:00 today - Ride temporarily unavailable - by Omar Haddad" with the reason. *(source: screens/P08-venue-back-office.yaml#BO-398)*
- **Status history**: Last five state changes with who, when and reason; full history on BO-403. *(source: screens/P08-venue-back-office.yaml#BO-398 / screens/P08-venue-back-office.yaml#BO-403)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the state (updateGame) and the operations block (setGameOperationalConfiguration, a whole-row PUT, per VO-R04). Confirmation names live effect: "Readers at Falcon Coaster will refuse taps from now until 14:00". *(source: contracts/satellite/games.yaml#updateGame / contracts/satellite/games.yaml#setGameOperationalConfiguration)*

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … |

#### Edge cases to draw

- **Game in maintenance and the operator tries to make it Active**: Refused (409) with "Returned to service only when the work order is verified" and the work-order link. *(source: contracts/satellite/games.yaml#updateGame)*
- **Cycle time left blank**: Warn that wait-time estimates and throughput will show nothing for this ride. *(source: contracts/satellite/games.yaml#setGameOperationalConfiguration)*

#### Consistency with other screens

- Match `BO-396`: The operations tab of the one attraction editor (per VO-R14); this board entry anchors into it.
- Match `BO-001`: Cycle time and capacity feed the virtual queue's wait-time estimate; same units (seconds, riders per cycle).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
state:
  attraction: Falcon Coaster
  state: Inactive
  from: 01 Oct 2026 11:00
  to: 01 Oct 2026 14:00
  message: Ride temporarily unavailable
  messageAr: اللعبة غير متاحة مؤقتاً
  reason: Wind speed above 45 km/h
  changedBy: Omar Haddad
operations:
  cycleSeconds: 150
  riderCapacity: 24
  throughputPerHour: 576
  minimumHeightCm: 132
  maximumHeightCm: 196
  minimumAge: 10
  supervisionRequiredBelowAge: 14
  staffPositions: 3
  operatingHours: Mon-Sun 10:00-22:00
```

#### Permissions

- `setGameOperationalConfiguration` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-398` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-398`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 8: Works in Game & Ride Operational Configuration → Configure whether an attraction is currently available for customer transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-398?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel, Change availability.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-399` Wallet & Credit Acceptance Mapping

**Define at attraction level which payment/value mechanisms are accepted. The source specifically requires digital-wallet credits to support pay-as-you-go for redemption games, skill games, rides and video games.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block C · task VM-BO-399 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/games-rides/wallet-credit-acceptance-mapping-bo-399` |

**What the spec says about it.** **Superseded by `BO-1106` Credit Usage & Eligibility Rules** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the credit eligibility (where a credit may be spent; CreditType does not carry it) that setCreditEligibilityRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where each credit type may be spent at attraction level (games, skill games, rides): the acceptance mapping, now part of credit eligibility rules.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setCreditEligibilityRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **eligibility**: Credit type rows by spend category and attraction columns, ticks in cells. *(source: contracts/satellite/wallet.yaml#setCreditEligibilityRules)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet credit acceptance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet credit acceptance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet credit acceptance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet credit acceptance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1106`: Same record and editor (credit eligibility rules).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
  Bonus:
  - arcade games
  - rides
  Cash:
  - everything
  Free game:
  - redemption games
```

#### Permissions

- `setCreditEligibilityRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per game: which credit types are accepted (cash/wallet, bonus, redemption) and a configurable consumption priority (bonus first, then prepaid/cash, then others). *(agreed · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-865)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-399` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-399`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 10: Works in Wallet & Credit Acceptance Mapping → Define at attraction level which payment/value mechanisms are accepted. The source specifically requires digital-wallet credits to support pay-as-you-go for redemption games, skill games, rides and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-399?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-400` Attraction / Reader Mapping

**Provide a high-level association between games/rides and their reader configurations. Important: This screen only performs the mapping. Detailed reader properties belong to Board 2 – Game Reader & Device Configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-400 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/attraction-reader-mapping-bo-400` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The mapping of games and rides to their readers - which reader (and reader profile) opens which attraction - with Assign, Replace, Remove and Test. Detailed reader properties stay on Board 2. The one thing to get right: incompatible or invalid mappings are refused before they are saved (wrong reader type, inactive reader, invalid profile, duplicate where prohibited), so a machine never goes live with a reader that cannot serve it.

**Known correction pending (do not draw the wrong version)**

- **Video Game Reader, Skill Game Reader and Ride Reader drawn as primary/secondary buttons** Why: They are the pack's reader categories (a filter or a column value), not actions. *(source: screens/P08-venue-back-office.yaml#BO-399; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No reader-type field exists to validate compatibility** Why: Reader carries deviceId, gameId, readerProfileId and settings; neither Reader nor ReaderProfile nor the tenancy device has a game reader category, so "Incompatible attraction type" cannot be checked. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap says the pack gives this screen nothing that can be drawn** Why: Pack p8-p9 give the mapping table columns, three reader categories, five actions and four validations. *(source: screens/P08-venue-back-office.yaml#BO-399 / screens/P08-venue-back-office.yaml#BO-401; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **confirmRemoveAssignment says the removal is not reversible** Why: Re-assigning restores it; only the guest-facing effect (taps refused) needs stating. *(source: screens/P08-venue-back-office.yaml#BO-400; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which reader/attraction combinations are "duplicate where prohibited" - one reader per game, or several readers per ride allowed?** → Drawn default accepted: Several readers per ride and per multi-station game; one game per reader. *(decided by Chinmay, 2026-10-02; DEC-379 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **reader category filter**: Video game reader, Skill game reader, Ride reader (at least) as filter chips - the generator drew them as three action buttons, which they are not. *(source: screens/P08-venue-back-office.yaml#BO-399 / screens/P08-venue-back-office.yaml#BO-401)*
- **Assign / Replace reader**: A picker showing only readers in the same venue that are active and unassigned (or assigned elsewhere, with a warning), filtered to the reader type compatible with the attraction's type. *(source: screens/P08-venue-back-office.yaml#BO-401)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Video Game Reader (primary button) | navigation or local | — | — | — | — |
| Skill Game Reader (secondary button) | navigation or local | — | — | — | — |
| Ride Reader (secondary button) | navigation or local | — | — | — | — |
| Assign Reader (secondary button) | navigation or local | — | — | — | — |
| Replace Reader (secondary button) | navigation or local | — | — | — | — |
| Remove Assignment (destructive button) | navigation or local | — | — | — | — |
| View Reader Configuration (secondary button) | navigation or local | — | — | — | — |
| Test Mapping (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Mapping table**: Attraction, Attraction type, Zone, Reader ID, Reader profile, Reader type, Status; one row per attraction, "No reader" in amber for attractions without one; an attraction with two readers (entry and exit side of a ride) shows two rows grouped. *(source: screens/P08-venue-back-office.yaml#BO-399)*
- **Compatibility result**: Inline line under the picker: "Compatible - Skill game reader on a Skill game" or the refusal reason. *(source: screens/P08-venue-back-office.yaml#BO-408)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Assign Reader / Replace Reader**: Writes the reader's gameId (setReaderConfiguration, whole Reader row per VO-R04). Replace moves the configuration from the old reader to the new one and leaves the old one unassigned; confirmation names both readers. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Remove Assignment**: Clears gameId; confirmation says "Taps at R-023 will be refused until a reader is assigned to Basketball Pro" and is reversible by re-assigning (the generated dialog's "not reversible" is wrong). *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test Mapping**: Runs testReader and shows the per-check results (connectivity, card read, display, game trigger, game complete signal). *(source: contracts/satellite/games.yaml#testReader)*
- **View Reader Configuration**: Navigates to BO-406 / BO-407 for the reader and returns here. *(source: screens/P08-venue-back-office.yaml#BO-401)*

**Data it reads**: `listReaders` (onLoad, Readers on this attraction)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

**What opens over it**

- confirmDialog *Remove Assignment*: **Remove Assignment on a attraction reader mapping is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction reader mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction reader mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction reader mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction reader mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader assigned but its configuration not deployed**: Status shows "Assigned, not deployed" because a change nobody deployed did not happen; link to deployment. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Duplicate assignment**: Refused where prohibited ("R-014 already opens VR Racing 01"); allowed for multi-reader rides. *(source: screens/P08-venue-back-office.yaml#BO-401)*

#### Consistency with other screens

- Match `BO-408`: BO-408 (Reader / Attraction Assignment) edits the same reader-to-game link from the reader side; draw one assignment dialog used by both, keep the board entries as anchors (per VO-R14).
- Match `BO-405`: Reader IDs and reader types match the Reader Directory.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- attraction: Basketball Pro 02
  type: Skill game
  zone: Sports Arcade
  reader: R-023
  profile: Skill Game Standard
  readerType: Skill game reader
  status: Active
- attraction: VR Racing 01
  type: Video game
  zone: Arcade
  reader: R-014
  profile: Video Standard
  readerType: Video game reader
  status: Active
- attraction: Falcon Coaster
  type: Ride
  zone: Thrill Zone
  reader: R-001
  profile: Ride Standard
  readerType: Ride reader
  status: Active
- attraction: Laser Arena
  type: Ride
  zone: Arcade
  reader: No reader
  status: Configuration error
refusal: Ride reader cannot be assigned to this Video game under the selected configuration profile.
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `testReader` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-400` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-400`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 12: Works in Attraction / Reader Mapping → Provide a high-level association between games/rides and their reader configurations. Important: This screen only performs the mapping. Detailed reader properties belong to Board 2 – Game Reader & …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-400?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Video Game Reader, Skill Game Reader, Ride Reader, Assign Reader, Replace Reader, Remove Assignment, View Reader Configuration, Test Mapping.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-401` Game Package & Entitlement Association

**Show which packages, tickets and entitlements provide access to each game or ride. The source requires packages containing specific games with configurable entitlement validity, plus products that can allow all games/rides, specific games/rides unlimited times, or specific games/rides a limited number of times.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-401 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-package-entitlement-association-bo-401` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The pack keeps entitlement creation on Board 4 (BO-427 to BO-430); this screen reads and navigates, and a create here duplicates them (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A read-mostly view of which packages, tickets and entitlements give access to each game or ride and under what usage model (pay per play, included in package, free play, unlimited, limited). Package and entitlement creation stays on Board 4. The one thing to get right: answer "what grants access to Falcon Coaster, and how many plays" per attraction, including the attractions no product covers (pay per play only).

**Known correction pending (do not draw the wrong version)**

- **The data table has no columns; gap says the pack gives nothing to draw** Why: Pack p9 lists seven columns, five access types and a worked example. *(source: screens/P08-venue-back-office.yaml#BO-401; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A package cannot express per-attraction usage (VR 2, Basketball 3, Coaster unlimited)** Why: GameEntitlement has one playCount for all its gameIds, so the pack's example package cannot be stored or shown. *(source: screens/P08-venue-back-office.yaml#BO-401 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createGameEntitlement bound as "Associate one" (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should Check Impact count guests currently holding an entitlement, which needs a read the games contract does not have?** → Drawn default accepted: Show active products and entitlement definitions only, with the guest count greyed. *(decided by Chinmay, 2026-10-02; DEC-380 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attraction filter**: Pick one attraction (or All); a package filter as the second axis. *(source: screens/P08-venue-back-office.yaml#BO-401)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| View Package (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Association table**: Attraction, Package, Entitlement, Access type, Usage limit, Validity, Status. Access type is a chip from the pack's five (Pay per play, Included in package, Free play, Unlimited play, Limited play), derived from GameEntitlement.kind and playCount. Usage limit "Unlimited" or "2 plays", plus daily cap and cooldown where set. Validity in words ("4 hours from first tap", "Same day"). *(source: screens/P08-venue-back-office.yaml#BO-401 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*
- **Package view**: Grouped by package, the pack's example reads as one card - Adventure Package - Falcon Coaster Unlimited, VR Racing 2 plays, Basketball Pro 3 plays, Prize Crane Pay per play. *(source: screens/P08-venue-back-office.yaml#BO-401)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View Package / View Entitlement**: Opens the package in BO-430 or the entitlement in BO-427/428/429 and returns here. *(source: screens/P08-venue-back-office.yaml#BO-401 / screens/P08-venue-back-office.yaml#BO-402)*
- **Associate Package / Remove Association**: Opens the package builder (BO-430) with the attraction pre-selected; this screen does not write, per the pack ("Detailed package creation and entitlement logic will remain in Board 4"). *(source: screens/P08-venue-back-office.yaml#BO-402)*
- **Check Impact**: Shows, for the selected attraction, active products, issued-and-unexpired entitlements and the count of guests holding them. *(source: screens/P08-venue-back-office.yaml#BO-402)*

**Data it reads**: `listGameEntitlements` (onLoad, Packages and entitlements)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game package entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game package entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game package entitlement yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game package entitlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **All-games pass with excluded attractions**: An all-games pass appears against every attraction of its included types except the excluded ones; the exclusion is listed as "Excluded". *(source: screens/P08-venue-back-office.yaml#BO-427)*
- **Entitlement inactive**: Row greyed with status Inactive, not hidden. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Consistency with other screens

- Match `BO-430`: Same package and per-attraction usage wording as the package builder.
- Match `BO-427`: Access type names identical to Board 4 kinds.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- attraction: Falcon Coaster
  package: Adventure Package
  entitlement: ADV-PKG-26
  accessType: Included in package
  limit: Unlimited
  validity: Same day
  status: Active
- attraction: VR Racing 01
  package: Adventure Package
  entitlement: ADV-PKG-26
  accessType: Limited play
  limit: 2 plays
  validity: Same day
  status: Active
- attraction: Basketball Pro 02
  package: Arcade Adventure
  entitlement: ARC-ADV-4H
  accessType: Limited play
  limit: 3 plays
  validity: 4 hours from first tap
  status: Active
- attraction: Prize Crane 04
  package: —
  entitlement: —
  accessType: Pay per play
  limit: —
  validity: —
  status: Active
```

#### Permissions

- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-401` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-401`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 14: Works in Game Package & Entitlement Association → Show which packages, tickets and entitlements provide access to each game or ride. The source requires packages containing specific games with configurable entitlement validity, plus products that …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-401?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: View Package.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-402` Configuration Health & Validation

**Prevent incomplete or conflicting game/ride configurations from becoming operational.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-402 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/configuration-health-validation-bo-402` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The readiness check for the whole games estate: for every attraction, does it have a type and zone, an active compatible reader, accepted value types, a price that resolves, a valid package mapping and a redemption rule where it pays out. Health is Ready / Warning / Configuration error, each finding names the screen that fixes it. The one thing to get right: findings are actionable rows ("Basketball Pro - No active reader assigned - Fix on BO-408"), grouped by attraction, worst first.

**Known correction pending (do not draw the wrong version)**

- **The content region is empty; gap says the pack gives nothing to draw** Why: Pack p10 lists six check families with eleven checks, three health statuses and two worked errors. *(source: screens/P08-venue-back-office.yaml#BO-402; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **simulateGameplayAuthorisation bound onAction as "Would a tap work here"** Why: The screen's read is validateGameConfiguration (bound only on the button); there is no onLoad call, so the list is empty until somebody presses Validate Again. Run it on load and keep simulate as a per-row link to BO-433. *(source: contracts/satellite/games.yaml#validateGameConfiguration / screens/P08-venue-back-office.yaml#BO-402; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Health enum healthy / warning / blocking versus the pack's Ready / Warning / Configuration error** Why: Same three states; the screen uses the pack's words. *(source: screens/P08-venue-back-office.yaml#BO-402 / contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Checks "Attraction type assigned", "Compatible reader type" and "Accepted value configured" have no contract check** Why: The findings enum has priceResolves, readerMapped, readerDeployed, edgePackageCurrent, entitlementCoverage, redemptionRule, assetInService; type and value-acceptance checks are missing because Game has no type link. *(source: screens/P08-venue-back-office.yaml#BO-402 / contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should Activate on BO-396 be blocked by a blocking finding, or only warned?** → Drawn default accepted: Blocked, with the finding named and a link here. *(decided by Chinmay, 2026-10-02; DEC-381 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Sent by *Validate Again*** (`validateGameConfiguration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `validateGameConfiguration` body |
| Games `gameIds` | multi-picker: choose games | optional | — | at most 500 | — | Empty or absent means every game in the venue. | `validateGameConfiguration` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **scope**: All attractions in the venue (default) or a selection; sent as gameIds (empty = all, max 500). *(source: contracts/satellite/games.yaml#validateGameConfiguration)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fix Issue (primary button) | navigation or local | — | — | — | — |
| Open Configuration (secondary button) | navigation or local | — | — | — | — |
| Validate Again (secondary button) | `validateGameConfiguration` POST `/game-configuration-validations` | inline | GameConfigurationHealth | — | — |
| View Dependencies (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Summary tiles**: Ready / Warning / Configuration error counts and "Checked at HH:MM". *(source: contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*
- **Findings list**: Per attraction, its health chip (healthy = Ready, warning = Warning, blocking = Configuration error) and findings grouped under the pack's check families - Attraction, Reader, Payment, Pricing, Entitlement, Redemption - each with severity, message and the fixOn screen as a link. *(source: screens/P08-venue-back-office.yaml#BO-402 / contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate Again**: Re-runs the checks; nothing is changed; results replace the list with the new time. *(source: contracts/satellite/games.yaml#validateGameConfiguration)*
- **Fix Issue / Open Configuration**: Opens the finding's fixOn screen with the game (and reader) pre-selected; returning re-validates that game. *(source: contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*
- **View Dependencies**: Opens the dependency view on BO-403 for the attraction. *(source: screens/P08-venue-back-office.yaml#BO-403)*

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The health validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the health validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No health validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the health validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader configuration older than the edge package expiry**: Blocking finding "Reader R-031 is running an expired rule package - deploy again". *(source: contracts/satellite/games.yaml#validateGameConfiguration)*
- **Asset not in service**: Finding "Asset under maintenance" with the work order; Fix opens the asset, not a games screen. *(source: contracts/satellite/games.yaml#validateGameConfiguration)*
- **AI-assisted diagnosis (pack enhancement)**: Suggested fix shown as a suggestion with its reason and an explicit Apply (per VO-R11), never applied automatically. *(source: screens/P08-venue-back-office.yaml#BO-403)*

#### Consistency with other screens

- Match `BO-394`: The dashboard's Configuration error status and alerts come from this result.
- Match `BO-433`: BO-433 tests one tap; this tests the whole set-up. Cross-link "Simulate a tap" per attraction.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checkedAt: 01 Oct 2026 10:45
findings:
- attraction: Basketball Pro 02
  health: Configuration error
  check: Reader assigned
  message: No active reader assigned.
  fixOn: BO-408
- attraction: Falcon Coaster
  health: Configuration error
  check: Valid price available
  message: Wallet enabled but no valid price configuration found.
  fixOn: BO-435
- attraction: Prize Crane 04
  health: Warning
  check: Redemption earning configuration
  message: Pays out tickets but has no redemption rule.
  fixOn: BO-445
```

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff
- `validateGameConfiguration` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-402` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-402`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 16: Works in Configuration Health & Validation → Prevent incomplete or conflicting game/ride configurations from becoming operational.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-402?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fix Issue, Open Configuration, Validate Again, View Dependencies.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-403` Attraction Audit, Dependencies & Governed Actions

**Provide traceability and controlled management of attraction configuration changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-403 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/attraction-audit-dependencies-governed-actions-bo-403` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Gameplay transactions are guest taps, not configuration changes; the audit timeline has no read in the games contract yet (contract gap CHG-WIR-004) (DI-866 … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of attraction configuration changes and their dependencies.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governance for an attraction: an audit timeline of configuration changes (created, type changed, reader assigned or replaced, wallet acceptance changed, package association changed, status changed, activated or deactivated) with who, when, previous and new value; a dependency view (reader, credit rules, pricing, packages, entitlements, redemption, inventory); and governed actions with an impact warning. The one thing to get right: before a critical change the user sees what depends on it - "Deactivate VR Racing? 3 active packages and 2 entitlement rules currently reference this attraction."

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Archive / Restore have no contract path (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The audit timeline is bound to listGameplayTransactions (CHG-WIR-001); Timeline fields (Attraction created, Type changed, User, Date/time, Previous value, New value) drawn as eleven select fields (CHG-SBO-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Archive" the same as retire (terminal), or a reversible hide?** → Drawn default accepted: Archive = retire with approval; Restore disabled. *(decided by Chinmay, 2026-10-02; DEC-382 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **timeline filters**: Event type chips (the pack's seven), user, date range. These are filters on a read-only timeline, not the eleven select fields the generator drew. *(source: screens/P08-venue-back-office.yaml#BO-403)*
- **governed action reason**: Required for Deactivate, Put into maintenance, Archive; recorded on the audit row. *(source: screens/P08-venue-back-office.yaml#BO-403)*

#### Outputs: what the screen shows and produces

**Shown**

**Change history** (timeline): Event types and columns of a read-only timeline; no read exists yet (logged).

| Shows | Format | Notes |
|---|---|---|
| Attraction created | text | not in the schema: `Attraction created` |
| Type changed | text | not in the schema: `Type changed` |
| Reader assigned/replaced | text | not in the schema: `Reader assigned/replaced` |
| Wallet acceptance changed | text | not in the schema: `Wallet acceptance changed` |
| Package association changed | text | not in the schema: `Package association changed` |
| Operational status changed | text | not in the schema: `Operational status changed` |
| Activation/deactivation | text | not in the schema: `Activation/deactivation` |
| User | text | not in the schema: `User` |
| Date/time | text | not in the schema: `Date/time` |
| Previous value | text | not in the schema: `Previous value` |
| New value | text | not in the schema: `New value` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Audit timeline**: Newest first, cursor-paged (per VO-R12); each entry - event, user, date/time (venue time), previous value -> new value in words ("Reader R-019 -> R-023", "Wallet acceptance: Bonus off -> on"). *(source: screens/P08-venue-back-office.yaml#BO-403)*
- **Dependency view**: The attraction at the centre with its dependants - Reader, Wallet/credit rules, Pricing, Packages, Entitlements, Redemption, Inventory where applicable - each with a count and a link. A graphical map is the pack's enhancement; a grouped list is acceptable first. *(source: screens/P08-venue-back-office.yaml#BO-403)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Activate / Deactivate**: Impact warning first ("3 active packages and 2 entitlement rules reference VR Racing"), then reason, then updateGame. *(source: screens/P08-venue-back-office.yaml#BO-403 / contracts/satellite/games.yaml#updateGame)*
- **Put into Maintenance**: Raises a work order against the attraction's asset (only maintenance moves a game to maintenance); disabled with that reason if no asset is linked. *(source: contracts/satellite/games.yaml#updateGame)*
- **Clone**: As BO-395 (cloneGame). *(source: contracts/satellite/games.yaml#cloneGame)*
- **Archive / Restore**: Archive = retire (requires approval; terminal). Restore is not possible for a retired game in the contract; draw Restore disabled with "Retired games cannot be restored - clone it instead". *(source: contracts/satellite/games.yaml#updateGame)*

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction audit dependencies configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction audit dependencies untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction audit dependencies configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Retire with active entitlements that name the game**: Blocked until the entitlements are amended, with their names; approval request otherwise. *(source: screens/P08-venue-back-office.yaml#BO-403 / contracts/satellite/games.yaml#updateGame)*

#### Consistency with other screens

- Match `BO-402`: View Dependencies on BO-402 opens this screen's dependency view.
- Match `BO-396`: The editor's "Last changed by" and status history link here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
timeline:
- at: 01 Oct 2026 09:12
  user: Fatima Al Hashimi
  event: Reader assigned/replaced
  previous: R-019
  new: R-023
- at: 30 Sep 2026 18:40
  user: Rahul Menon
  event: Wallet acceptance changed
  previous: 'Bonus accepted: Off'
  new: 'Bonus accepted: On'
- at: 28 Sep 2026 11:05
  user: Ahmed Al Mansoori
  event: Attraction created
  previous: —
  new: Basketball Pro 02 (clone of Basketball Pro 01)
impact: Deactivate "VR Racing"? 3 active packages and 2 entitlement rules currently reference this attraction.
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-403` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-403`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 18: Works in Attraction Audit, Dependencies & Governed Actions → Provide traceability and controlled management of attraction configuration changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-403?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-394`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneGame": {"method":"POST","path":"/games/{gameId}/clone","contract":"games","summary":"Copy a game or ride as a new one","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Game"},
"createGame": {"method":"POST","path":"/games","contract":"games","summary":"Register a game","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Game","responds":"Game"},
"listAttractionTypes": {"method":"GET","path":"/attraction-types","contract":"games","summary":"The classes of game and ride","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AttractionType"},
"listGameEntitlements": {"method":"GET","path":"/game-entitlements","contract":"games","summary":"Passes, packages and per-game entitlements","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameEntitlement"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listGames": {"method":"GET","path":"/games","contract":"games","summary":"List games","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Game"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"setAttractionType": {"method":"PUT","path":"/attraction-types","contract":"games","summary":"Define a class of attraction","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AttractionType","responds":"AttractionType"},
"setCreditEligibilityRules": {"method":"PUT","path":"/credit-types/{creditTypeId}/eligibility","contract":"wallet","summary":"Where this credit may be spent, and on what","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditEligibility","responds":"CreditEligibility"},
"setGameOperationalConfiguration": {"method":"PUT","path":"/games/{gameId}/operations","contract":"games","summary":"Capacity, cycle time, restrictions and staffing","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameOperationalConfig","responds":"GameOperationalConfig"},
"setReaderConfiguration": {"method":"PUT","path":"/readers/{readerId}","contract":"games","summary":"What this reader charges, opens, shows and refuses","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Reader","responds":"Reader"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"},
"testReader": {"method":"POST","path":"/readers/{readerId}/test","contract":"games","summary":"Prove a reader works before a guest finds out it does not","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReaderTestResult"},
"updateGame": {"method":"PATCH","path":"/games/{gameId}","contract":"games","summary":"Amend a game","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Game"},
"validateGameConfiguration": {"method":"POST","path":"/game-configuration-validations","contract":"games","summary":"Re-run the configuration health checks for some or all games","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GameConfigurationHealth"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AttractionType": {"type":"object","x-ticvai-persistence":"games.attraction_type","description":"Board 1.4. **The type decides which settings apply.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"family":{"type":"string","enum":["ride","arcadeGame","redemptionGame","crane","vrExperience","softPlay","attraction","show"]},"hasTicketPayout":{"type":"boolean","default":false},"hasDirectPay":{"type":"boolean","default":false},"hasCycleTime":{"type":"boolean","default":true},"hasHeightRestriction":{"type":"boolean","default":false},"supportsEntitlements":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"CreditEligibility": {"type":"object","x-ticvai-persistence":"wallet.credit_eligibility","description":"Board 3.4. **Where credit may be spent** — acceptance, not funding.","properties":{"creditTypeId":{"type":"string","format":"uuid"},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedOutletKinds":{"type":"array","items":{"type":"string"}},"allowedProductCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"excludedProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedChannels":{"type":"array","items":{"type":"string"}},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumPercentOfBasket":{"type":"number","nullable":true,"description":"**Caps how much of a purchase one credit type may cover.** A venue that lets promotional credit pay for everything has run a free day it did not intend.\n"},"validDaysOfWeek":{"type":"array","items":{"type":"string"}},"scopePath":{"type":"string"}}},
"Game": {"x-ticvai-persistence":"games.game","type":"object","required":["id","code","name","venueId","creditCost","status"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"zone":{"type":"string","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits.\n"},"readerId":{"type":"string","format":"uuid","nullable":true},"creditCost":{"type":"integer","minimum":1},"minPointsAwarded":{"type":"integer"},"maxPointsAwarded":{"type":"integer"},"heightRequirementCm":{"type":"integer","nullable":true},"status":{"$ref":"#/components/schemas/GameStatus"},"playsToday":{"type":"integer"},"creditsTakenToday":{"type":"integer"},"pointsAwardedToday":{"type":"integer"}}},
"GameConfigurationHealth": {"x-ticvai-persistence":"none — computed","type":"object","description":"Board 1, p.10. The result of `validateGameConfiguration`; nothing is stored.","required":["venueId","checkedAt","games"],"properties":{"venueId":{"type":"string","format":"uuid"},"checkedAt":{"type":"string","format":"date-time"},"games":{"type":"array","items":{"type":"object","required":["gameId","health"],"properties":{"gameId":{"type":"string","format":"uuid"},"health":{"type":"string","enum":["healthy","warning","blocking"]},"findings":{"type":"array","items":{"type":"object","required":["check","severity"],"properties":{"check":{"type":"string","enum":["priceResolves","readerMapped","readerDeployed","edgePackageCurrent","entitlementCoverage","redemptionRule","assetInService"]},"severity":{"type":"string","enum":["warning","blocking"]},"message":{"type":"string"},"readerId":{"type":"string","format":"uuid","nullable":true},"fixOn":{"type":"string","nullable":true,"description":"The screen that fixes it, e.g. BO-407."}}}}}}}}},
"GameEntitlement": {"type":"object","x-ticvai-persistence":"games.entitlement","description":"Board 4. **A right to play, not money** — consumed before money is.","required":["code","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["allGamesPass","unlimitedSingleGame","limitedSingleGame","package","freePlay"]},"gameIds":{"type":"array","items":{"type":"string","format":"uuid"}},"attractionTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"includesGamesAddedLater":{"type":"boolean","default":true,"description":"**Whether a pass sold today covers a game added tomorrow** (Chinmay, 2 October, workbook Q397: \"venue configures; default yes\"; CHG-CSA-028). True, the default: an `allGamesPass`, or a pass bound by `attractionTypeIds`, covers games added after it was sold that match it; the coverage summary says so. False: it covers only the games that existed at sale. A pass listing `gameIds` covers those games only, whatever this says."},"playCount":{"type":"integer","nullable":true,"description":"For `limitedSingleGame` and `package`. Null means unlimited."},"validityKind":{"type":"string","enum":["sameDay","days","untilDate","untilUsed"]},"validityDays":{"type":"integer","nullable":true},"activationKind":{"type":"string","enum":["onPurchase","onFirstUse","onDate"],"default":"onFirstUse","description":"**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"},"dailyPlayCap":{"type":"integer","nullable":true},"cooldownMinutes":{"type":"integer","nullable":true,"description":"**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"},"linkedProductId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"GameOperationalConfig": {"type":"object","x-ticvai-persistence":"games.operational_config","description":"Board 1.5. **Cycle time is the number everything else derives from.**","properties":{"gameId":{"type":"string","format":"uuid"},"cycleSeconds":{"type":"integer","nullable":true},"riderCapacity":{"type":"integer","nullable":true},"throughputPerHour":{"type":"integer","readOnly":true},"minimumHeightCm":{"type":"integer","nullable":true},"maximumHeightCm":{"type":"integer","nullable":true},"minimumAge":{"type":"integer","nullable":true},"supervisionRequiredBelowAge":{"type":"integer","nullable":true},"healthRestrictions":{"type":"array","items":{"type":"string"}},"staffPositions":{"type":"integer","nullable":true},"operatingHours":{"type":"array","nullable":true,"description":"Weekly opening windows, in venue local time, in the same window shape as `GamePricing.peakPricing`. Null means the game follows the venue's hours.\n","items":{"type":"object","required":["daysOfWeek","from","to"],"properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string","description":"Local time, HH:MM."},"to":{"type":"string","description":"Local time, HH:MM."}}}},"scopePath":{"type":"string"}}},
"GameStatus": {"type":"string","enum":["inService","outOfService","maintenance","retired"]},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderTestResult": {"type":"object","description":"Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n","properties":{"readerId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["connectivity","cardRead","balanceCheck","display","sound","gameTrigger","gameCompleteSignal"]},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}}
}
```
