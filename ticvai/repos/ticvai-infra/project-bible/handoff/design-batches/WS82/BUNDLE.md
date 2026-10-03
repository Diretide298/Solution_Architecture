# WS82 — Game and Ride board 5

**10 screens · 7 operations · 14 schemas · 4 permissions**

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
  `PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-434` | Game & Ride Pricing Command Center | D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-435` | Standard Game & Ride Price Configuration | D | 11 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-436` | Group Pricing Configuration | D | 12 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-437` | Peak / Non-Peak Dynamic Pricing | D | 10 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-438` | Pricing Calendar & Exception Dates | D | 8 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-439` | Normal & VIP Pricing Configuration | D | 1 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-440` | Retry Price Configuration | D | 0 | 2 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-441` | Price Priority & Conflict Rules | B | 20 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-442` | Effective Pricing & Reader Price Preview | D | 6 | 10 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-443` | Pricing Audit, Approval & Publication | B | 16 | 0 | 6 | 11 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-439, BO-440, BO-441 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-434` Game & Ride Pricing Command Center

**Provide a central view of all game and ride pricing configurations, active pricing rules, upcoming changes, and pricing issues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-434 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-ride-pricing-command-center-bo-434` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The pricing command centre for games and rides: KPI tiles (priced attractions, active price rules, peak pricing active, VIP enabled, retry enabled, upcoming changes, missing prices, conflicts), a pricing overview per attraction (standard, current, VIP, pricing mode, status), filters and the board's tiles. The backend, not the reader, decides the price. The one thing to get right: "Current price" is the price a tap would be charged now, with the rule that produced it, next to the standard price - the difference is what managers look for.

**Known correction pending (do not draw the wrong version)**

- **getGamePricing requires one gameId, so the overview across all attractions has no list read** Why: The overview, Active price rules, Upcoming changes and Conflicts KPIs need a venue-wide read of pricing configuration and resolutions. *(source: screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#getGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Three of the pack's eight KPI tiles are missing (Upcoming Price Changes, Missing Prices, Pricing Conflicts) and the Pricing Overview table is absent** Why: Pack p43-p44 list all eight and give the overview with four sample rows. *(source: screens/P08-venue-back-office.yaml#BO-434 / screens/P08-venue-back-office.yaml#BO-435; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does Publish exist as a separate step (draft prices vs live prices), or are prices live on save?** → Drawn default accepted: Live on save, delivered to readers on the next deployment; Publish = deploy now. *(decided by Chinmay, 2026-10-02; DEC-404 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, attraction, attraction type, pricing type, vip enabled and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Game | picker: choose a game | — | — | `getGamePricing` ?gameId |
| Reader | picker: choose a reader | — | — | `getGamePricing` ?readerId |
| At | date and time picker | — | — | `getGamePricing` ?at |
| Guest tier | text field | — | — | `getGamePricing` ?guestTier |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters**: Zone, Attraction, Attraction type, Pricing type (Standard, Group, Peak, Non-peak, VIP, Retry, Exception), VIP enabled, Effective date (default now - changes "Current price" to the price at that moment), Status. Venue from the switcher. *(source: screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#getGamePricing)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Priced Attractions** (metric tile)

**Active Price Rules** (metric tile)

**Peak Pricing Active** (metric tile)

**VIP Pricing Enabled** (metric tile)

**Retry Pricing Enabled** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Eight metric tiles (per VO-R02) - the generator carried five; Upcoming price changes, Missing prices and Pricing conflicts are missing. Missing prices = attractions in service with no price that resolves (same as the health check's price finding). *(source: screens/P08-venue-back-office.yaml#BO-434 / screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#validateGameConfiguration)*
- **Pricing overview**: Attraction, Type, Standard, Current price, VIP, Pricing mode (Standard / Peak / Non-peak / Exception / Retry enabled), Status. Current price comes from the resolution (effectivePrice and appliedRule) and is highlighted when it differs from Standard; "—" for VIP where none is set. Money as AED 20.00. *(source: screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#/components/schemas/GamePriceResolution)*
- **Upcoming changes**: The next scheduled changes in a short list ("Sat 04 Oct 17:00 - Falcon Coaster peak AED 45.00"), linking to the pricing calendar. *(source: screens/P08-venue-back-office.yaml#BO-434)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create Price / Edit Price**: Opens the attraction's pricing editor (BO-435 onwards) and returns here (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-435)*
- **View Calendar**: Opens BO-438 in week view. *(source: screens/P08-venue-back-office.yaml#BO-435)*
- **Validate / Publish**: Validate runs the price checks for all attractions; Publish pushes the prices to readers through deployment and says how many readers will update. *(source: screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#deployReaderConfiguration)*

**Data it reads**: `getGamePricing` (onLoad, Effective prices)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-435` Standard Game & Ride Price Configuration: *Standard Game & Ride Price Configuration*
- → `BO-436` Group Pricing Configuration: *Group Pricing Configuration*
- → `BO-437` Peak / Non-Peak Dynamic Pricing: *Peak / Non-Peak Dynamic Pricing*
- → `BO-438` Pricing Calendar & Exception Dates: *Pricing Calendar & Exception Dates*
- → `BO-439` Normal & VIP Pricing Configuration: *Normal & VIP Pricing Configuration*
- → `BO-440` Retry Price Configuration: *Retry Price Configuration*
- → `BO-441` Price Priority & Conflict Rules: *Price Priority & Conflict Rules*
- → `BO-442` Effective Pricing & Reader Price Preview: *Effective Pricing & Reader Price Preview*
- → `BO-443` Pricing Audit, Approval & Publication: *Pricing Audit, Approval & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Attraction with no resolvable price**: Row shows "No price" in red and counts in Missing prices; the reader would refuse with "Game unavailable". *(source: contracts/satellite/games.yaml#validateGameConfiguration)*

#### Consistency with other screens

- Match `BO-442`: Effective Pricing & Reader Price Preview shows the same resolution trace for one attraction.
- Match `BO-441`: Pricing conflicts KPI opens Price Priority & Conflict Rules.
- Match `BO-394`: Current price on the games dashboard is this column.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  pricedAttractions: 40
  activePriceRules: 63
  peakActive: 6
  vipEnabled: 18
  retryEnabled: 9
  upcomingChanges: 4
  missingPrices: 2
  conflicts: 1
rows:
- attraction: VR Racing 01
  type: Video game
  standard: AED 20.00
  current: AED 20.00
  vip: AED 15.00
  mode: Standard
  status: Active
- attraction: Falcon Coaster
  type: Ride
  standard: AED 35.00
  current: AED 45.00
  vip: AED 30.00
  mode: Peak
  status: Active
- attraction: Basketball Pro 02
  type: Skill game
  standard: AED 20.00
  current: AED 20.00
  vip: AED 15.00
  mode: Standard
  status: Active
- attraction: Prize Crane 04
  type: Skill game
  standard: AED 15.00
  current: AED 15.00
  vip: —
  mode: Retry enabled
  status: Active
```

#### Permissions

- `getGamePricing` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-434` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-434`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 1: Opens Game & Ride Pricing Command Center → Provide a central view of all game and ride pricing configurations, active pricing rules, upcoming changes, and pricing issues.
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F191 branch at step 1 (expected): when Nothing has been set up on Game & Ride Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F191 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-434?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-435`, `BO-436`, `BO-437`, `BO-438`, `BO-439`, `BO-440`, `BO-441`, `BO-442`, `BO-443`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-435` Standard Game & Ride Price Configuration

**Define the normal base price charged to play a specific game or ride. The source requires that prices be defined for each game.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-435 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/standard-game-ride-price-configuration-bo-435` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The normal base price to play one game or ride, with its wallet credit equivalent and effective dates ("VR Racing - Standard price AED 20 - 20 credits"). The reader receives the applicable price from TICVAI at runtime. The one thing to get right: Standard price is the floor every other rule (group, peak, VIP, retry, exception) is compared against, and all six pricing screens edit one pricing record per attraction - so draw them as tabs of one Attraction pricing editor with one Save (per VO-R14).

**Known correction pending (do not draw the wrong version)**

- **setGamePricing is a whole-record PUT bound without any read of the stored pricing** Why: getGamePricing returns a resolution (effective price and trace), not the configuration; editing standard price would wipe group, peak, VIP, retry and exception prices left out (per VO-R04). *(source: contracts/satellite/games.yaml#setGamePricing / contracts/satellite/games.yaml#getGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Effective from / to, status, rule name and credit equivalent have no field on GamePricing** Why: standardPrice is a single Money value per game with no dates; the credit amount lives separately as Game.creditCost. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricing / contracts/satellite/games.yaml#/components/schemas/Game; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **All eleven fields drawn as select fields, including Standard price and Currency** Why: Price is a money input, currency is fixed by the region, dates are pickers. *(source: screens/P08-venue-back-office.yaml#BO-435 / ADR-0011; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which is authoritative at the reader - Game.creditCost (credits) or GamePricing.standardPrice (AED)?** → Drawn default accepted: GamePricing in AED, with credits derived at the venue's rate and shown read-only. *(decided by Chinmay, 2026-10-02; DEC-405 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Price Rule Name | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Attraction Type | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Zone | select field | — | — | — | — | — | — |
| Standard Price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Wallet/Credit Equivalent | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attraction**: Picker; Attraction type, Venue and Zone are shown from the attraction, not entered (the generator drew them as selects). *(source: screens/P08-venue-back-office.yaml#BO-435)*
- **standard price**: Money in the region's currency and decimal scale (AED 20.00); greater than zero. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricing)*
- **currency**: Shown, not chosen - the region owns the currency. *(source: ADR-0011)*
- **wallet / credit equivalent**: Whole credits charged when the guest pays in game credits; defaults to the price at the venue's credit rate (AED 1.00 = 1 credit) and can be overridden. *(source: screens/P08-venue-back-office.yaml#BO-435 / contracts/satellite/games.yaml#/components/schemas/Game)*
- **effective from / to, status, rule name**: Date pickers (to after from, empty = open-ended); status Draft / Active / Inactive. Rule name is optional here because the standard price is one per attraction. *(source: screens/P08-venue-back-office.yaml#BO-435)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader relationship note**: "Readers at VR Racing 01 (R-014) get this price on their next deployment" with the last deployment time. *(source: screens/P08-venue-back-office.yaml#BO-436 / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Effective now**: The resolved price right now and which rule wins, so a standard price hidden by a peak rule is not mistaken for the charge. *(source: contracts/satellite/games.yaml#getGamePricing)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save Draft / Validate / Activate**: Save writes the whole pricing record for the attraction (PUT, per VO-R04) - group, peak, VIP, retry and exceptions included - so the form must hold every current value. Validate checks for overlaps. *(source: screens/P08-venue-back-office.yaml#BO-436 / contracts/satellite/games.yaml#setGamePricing)*
- **Clone**: Copies this attraction's pricing to selected attractions of the same type (as cloneGame does with includePricing). *(source: screens/P08-venue-back-office.yaml#BO-436 / contracts/satellite/games.yaml#cloneGame)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The standard game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the standard game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No standard game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Price changed while plays are in flight**: The new price applies to taps after it reaches the reader; a guest mid-game is not re-charged. *(source: contracts/satellite/games.yaml#updateGame)*

#### Consistency with other screens

- Match `BO-396`: Game.creditCost and GamePricing.standardPrice are two prices of the same play; show them together and keep one as derived.
- Match `BO-407`: The reader's Required credit is this price.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
price:
  attraction: VR Racing 01
  type: Video game
  venue: Summit Peaks
  zone: Arcade
  standard: AED 20.00
  currency: AED
  credits: 20
  from: 01 Oct 2026
  to: ''
  status: Active
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-435` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-435`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 2: Works in Standard Game & Ride Price Configuration → Define the normal base price charged to play a specific game or ride. The source requires that prices be defined for each game.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-435?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-436` Group Pricing Configuration

**Allow multiple games or rides to share a common pricing rule instead of configuring each attraction individually.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-436 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Group Setup; Configuration Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/group-pricing-configuration-bo-436` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Group pricing as the pack means it: several games or rides share one pricing rule ("Arcade Standard Group - AED 20 - VR Racing, Space Shooter, Moto Racing, Flight Simulator"), inherited by every linked attraction unless an approved attraction override exists (Attraction override beats Group price). The one thing to get right: show for each member whether it inherits or overrides, and what changing the group price will change.

**Known correction pending (do not draw the wrong version)**

- **The contract's groupPricing means a party of players, not a group of attractions** Why: GamePricing.groupPricing is minimumPlayers and pricePerPlayer on one game (a price for groups of people); the pack and the matrix line "Assign prices for the Group" mean one price shared by a group of games. No pricing-group entity, membership or override exists. *(source: screens/P08-venue-back-office.yaml#BO-436 / contracts/satellite/games.yaml#/components/schemas/GamePricing / contracts/satellite/games.yaml#/components/schemas/GamePricingException / MATRIX 10.2.7; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Add Attraction and Remove Attraction drawn as select fields; Apply price to all and Individual override allowed as text fields** Why: Two are actions, one is an action with confirmation, one is a switch. *(source: screens/P08-venue-back-office.yaml#BO-436; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **setGamePricing is per game** Why: Changing a group price would need one PUT per member game, each replacing that game's whole pricing record. *(source: contracts/satellite/games.yaml#setGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are party-size prices (group of players, as the contract has it) also wanted, alongside attraction groups?** → Drawn default accepted: Draw attraction groups as the pack asks; show party-size pricing as a separate "Party price" tab greyed until confirmed. *(decided by Chinmay, 2026-10-02; DEC-406 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pricing Group Name | select field | — | — | — | — | — | — |
| Group Code | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction Type | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Add Attraction | select field | — | — | — | — | — | — |
| Remove Attraction | select field | — | — | — | — | — | — |
| Apply price to all | text field | — | — | — | — | — | — |
| Individual override allowed: Yes/No | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **pricing group name / group code**: Text (Arabic variant for the name) and a unique code; the generator drew selects. *(source: screens/P08-venue-back-office.yaml#BO-436)*
- **attraction type, price, effective period, status**: Attraction type limits which attractions can join; price is money (AED 20.00, currency from the region); effective period as from / to pickers. *(source: screens/P08-venue-back-office.yaml#BO-436)*
- **members**: A member list with Add attraction / Remove attraction (actions, not select fields), "Apply price to all" (resets overrides after confirmation) and "Individual override allowed" switch. *(source: screens/P08-venue-back-office.yaml#BO-436)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Member table**: Attraction, Inherits / Overrides, Effective price - overrides badged and their own price shown. *(source: screens/P08-venue-back-office.yaml#BO-436 / screens/P08-venue-back-office.yaml#BO-437)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Confirmation names the effect - "Price changes for 4 attractions; 1 override (Flight Simulator AED 25.00) is kept". *(source: screens/P08-venue-back-office.yaml#BO-437)*
- **Apply price to all**: Removes member overrides after a confirmation naming them (per VO-R16). *(source: screens/P08-venue-back-office.yaml#BO-436)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **An attraction in two groups**: Refused - one pricing group per attraction - or the priority rule decides; say which. *(source: screens/P08-venue-back-office.yaml#BO-441 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Consistency with other screens

- Match `BO-435`: An attraction's standard price tab shows "Inherited from Arcade Standard Group" when it is a member.
- Match `BO-441`: Group sits below attraction-specific price in the pack's priority example.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group:
  name: Arcade Standard Group
  nameAr: مجموعة الألعاب القياسية
  code: ARC-STD
  venue: Summit Peaks
  type: Video game
  price: AED 20.00
  effective: 01 Oct 2026 -
  status: Active
  overrideAllowed: true
members:
- attraction: VR Racing 01
  mode: Inherits
  price: AED 20.00
- attraction: Space Shooter
  mode: Inherits
  price: AED 20.00
- attraction: Moto Racing
  mode: Inherits
  price: AED 20.00
- attraction: Flight Simulator
  mode: Override
  price: AED 25.00
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-436` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-436`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 4: Works in Group Pricing Configuration → Allow multiple games or rides to share a common pricing rule instead of configuring each attraction individually.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-436?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-437` Peak / Non-Peak Dynamic Pricing

**Configure different game/ride prices based on date and time. The source explicitly requires peak/non-peak pricing for games/rides based on specific date/time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-437 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Rule Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/peak-non-peak-dynamic-pricing-bo-437` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Peak and non-peak prices by day of week and time of day ("Falcon Coaster - Standard AED 35 - Peak Fri-Sun 17:00-23:00 AED 45 - Non-peak Mon-Thu 10:00-17:00 AED 30"), applied automatically by the backend. The pack asks for a calendar view Mon to Sun with the peak and non-peak periods. The one thing to get right: the week grid shows at a glance which price applies at any hour, and overlapping windows are impossible to save silently.

**Known correction pending (do not draw the wrong version)**

- **No calendar view on the screen, though the pack asks for a Mon-Sun view of peak and non-peak periods** Why: A screen placing prices in time needs a calendar with Day, Week and Month views (per VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-437; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Peak price and Non-peak price as two fields of one rule; Specific date as a field of a weekly rule** Why: The contract stores one price per window (daysOfWeek, from, to, price); a date is a calendar exception. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricingException / contracts/satellite/games.yaml#/components/schemas/GamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rule name, Peak / Non-peak label and effective from / to have no field on a peak window** Why: Windows carry days, times and price only. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricingException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Attraction / Group target is not possible** Why: Peak windows hang off one gameId; there is no attraction group to target (see BO-436). *(source: contracts/satellite/games.yaml#/components/schemas/GamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a window be labelled Peak or Non-peak explicitly, or derived from being above or below standard?** → Drawn default accepted: Explicit label chosen by the user. *(decided by Chinmay, 2026-10-02; DEC-407 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rule Name | select field | — | — | — | — | — | — |
| Attraction / Group | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Days of Week | select field | — | — | — | — | — | — |
| Specific Date | select field | — | — | — | — | — | — |
| Start Time | select field | — | — | — | — | — | — |
| End Time | select field | — | — | — | — | — | — |
| Peak Price | select field | — | — | — | — | — | — |
| Non-Peak Price | select field | — | — | — | — | — | — |
| Effective From / To | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **rule name, attraction / group**: Name text; target is one attraction or a pricing group. *(source: screens/P08-venue-back-office.yaml#BO-437)*
- **pricing mode**: Peak or Non-peak per window (a label the reader and reports use), not inferred from the price. *(source: screens/P08-venue-back-office.yaml#BO-437)*
- **days of week, start time, end time**: Weekday chips starting on the venue's first day; HH:MM in venue time, end after start (a window across midnight is split into two). *(source: screens/P08-venue-back-office.yaml#BO-437 / contracts/satellite/games.yaml#/components/schemas/GamePricingException)*
- **price**: One price per window (Peak AED 45.00 or Non-peak AED 30.00) - not two price fields on one rule. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricingException)*
- **specific date**: Not here - a specific date is an exception on BO-438; link "Add a date exception". *(source: screens/P08-venue-back-office.yaml#BO-438)*
- **effective from / to**: Date pickers bounding when the rule applies (e.g. summer season). *(source: screens/P08-venue-back-office.yaml#BO-437)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Week view**: Mon-Sun columns by hour from the venue's day start hour, peak blocks in one colour, non-peak in another, standard as the background, each block labelled with its price; Day and Month views as well (per VO-R01). Right-to-left in Arabic. *(source: screens/P08-venue-back-office.yaml#BO-437)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the peak windows as part of the attraction's whole pricing record (per VO-R04); overlaps are refused with the overlapping windows named. *(source: contracts/satellite/games.yaml#setGamePricing)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The peak non-peak dynamic configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the peak non-peak dynamic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No peak non-peak dynamic configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two windows overlap on Friday 17:00-18:00**: Blocked "Peak Fri 17:00-23:00 overlaps Non-peak Fri 10:00-18:00". *(source: screens/P08-venue-back-office.yaml#BO-438)*
- **Window outside the attraction's operating hours**: Warning; the price would never apply. *(source: contracts/satellite/games.yaml#/components/schemas/GameOperationalConfig)*

#### Consistency with other screens

- Match `BO-438`: The same calendar component, with exceptions as an extra layer; the week view here is the pricing calendar filtered to peak and non-peak.
- Match `BO-152`: Operating Calendar & Special Access Days uses the same calendar view and day start hour.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attraction: Falcon Coaster
standard: AED 35.00
windows:
- mode: Peak
  days:
  - Fri
  - Sat
  - Sun
  from: '17:00'
  to: '23:00'
  price: AED 45.00
- mode: Non-peak
  days:
  - Mon
  - Tue
  - Wed
  - Thu
  from: '10:00'
  to: '17:00'
  price: AED 30.00
effective: 01 Oct 2026 - 31 Mar 2027
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-437` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-437`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 6: Works in Peak / Non-Peak Dynamic Pricing → Configure different game/ride prices based on date and time. The source explicitly requires peak/non-peak pricing for games/rides based on specific date/time.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-437?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-438` Pricing Calendar & Exception Dates

**Provide a visual calendar for understanding and overriding time-based pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-438 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Exception Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/pricing-calendar-exception-dates-bo-438` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A visual pricing calendar with layers (Standard, Peak, Non-peak, Special day, Temporary override) and date exceptions (public holiday, school holiday, special event, promotional day, venue date) that override time-based pricing without changing the underlying rule ("National Day - Falcon Coaster 12:00-23:00 - Special price AED 50"). The one thing to get right: the calendar is the screen - Day, Week and Month views with layer toggles - and an exception that overlaps a rule says so before saving.

**Known correction pending (do not draw the wrong version)**

- **The screen has no calendar component (calendarView absent)** Why: A pricing calendar must offer Day, Week and Month views (per VO-R01); the generator drew a plain form of selects. *(source: screens/P08-venue-back-office.yaml#BO-438; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Calendar exceptions have no start / end time, exception type, reason or priority** Why: GamePricingException for calendarException carries date, price and closed only; the pack's National Day 12:00-23:00 example cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-438 / contracts/satellite/games.yaml#/components/schemas/GamePricingException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The contract's Closed flag (game does not run that day) is not on the screen** Why: It is a calendar exception value the pack does not mention; draw it as a pricing type. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricingException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Date, Price, Start / End time and Reason drawn as select fields** Why: Pickers, money input and text. *(source: screens/P08-venue-back-office.yaml#BO-438; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should public and school holidays come from a venue holiday calendar rather than being entered per attraction?** → Drawn default accepted: Offer "Apply to all attractions in a group" and a holiday picker sourced from the operating calendar, greyed until it exists. *(decided by Chinmay, 2026-10-02; DEC-408 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | select field | — | — | — | — | — | — |
| Attraction / Group | select field | — | — | — | — | — | — |
| Pricing Type | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Start Time | select field | — | — | — | — | — | — |
| End Time | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **calendar**: Day, Week (default) and Month views, Agenda for a list of exceptions (per VO-R01); day split into hours from the venue's day start hour; filters Attraction / Group and Attraction type; layer toggles for the five layers. *(source: screens/P08-venue-back-office.yaml#BO-438)*
- **exception date and type**: Date picker (or a range of days created as one exception per day); type from the pack's five as a select (Public holiday, School holiday, Special event, Promotional day, Venue-specific date). *(source: screens/P08-venue-back-office.yaml#BO-438)*
- **attraction / group, pricing type, price, start / end time**: Pricing type Special day price / Temporary override / Closed (the game does not run that day). Price as money, hidden when Closed. Start and end in venue time; empty = all day. *(source: screens/P08-venue-back-office.yaml#BO-438 / contracts/satellite/games.yaml#/components/schemas/GamePricingException)*
- **priority, reason**: Priority shown from the price priority rules (BO-441) rather than typed per exception; reason text required. *(source: screens/P08-venue-back-office.yaml#BO-438 / screens/P08-venue-back-office.yaml#BO-441)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Calendar cells**: Each cell shows the price that applies with its layer colour; an exception cell shows its name ("National Day AED 50.00") and the price it replaced struck through. *(source: screens/P08-venue-back-office.yaml#BO-438)*
- **Conflict warning**: Inline before save - "Existing Peak pricing rule overlaps this period. The exception wins on 02 Dec 12:00-23:00." *(source: screens/P08-venue-back-office.yaml#BO-438)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add exception (click a day or drag a time range)**: Opens the exception form pre-filled with the date and times. *(source: designer default)*
- **Save**: Saves exceptions as part of the attraction's whole pricing record (per VO-R04); the underlying standard and peak rules are unchanged. *(source: contracts/satellite/games.yaml#setGamePricing)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing calendar exception configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing calendar exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing calendar exception configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Exception for New Year's Eve that excludes peak pricing (DI-876)**: The exception sets the standard price for that date and the calendar shows peak suppressed. *(source: DI-876)*
- **Exception on a date the attraction is closed**: Warn that the price will never apply. *(source: contracts/satellite/games.yaml#/components/schemas/GamePricingException)*

#### Consistency with other screens

- Match `BO-437`: Same calendar component and colours; peak and non-peak layers come from BO-437.
- Match `BO-152`: Operating Calendar & Special Access Days - holidays and special days should come from one venue calendar, not be retyped here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  name: National Day
  type: Public holiday
  date: 02 Dec 2026
  attraction: Falcon Coaster
  pricingType: Special day price
  price: AED 50.00
  from: '12:00'
  to: '23:00'
  reason: UAE National Day demand
closed:
  name: Annual maintenance
  date: 15 Jan 2027
  attraction: Wave Rider
  pricingType: Closed
conflict: Existing Peak pricing rule overlaps this period.
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-438` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-438`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 8: Works in Pricing Calendar & Exception Dates → Provide a visual calendar for understanding and overriding time-based pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-438?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-439` Normal & VIP Pricing Configuration

**Configure different prices for Normal and VIP guests for the same game/ride and reader. The source explicitly requires one reader to show both Normal Price and VIP Price for a specific game, with VIP eligibility obtained through purchase of a VIP product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-439 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/normal-vip-pricing-configuration-bo-439` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Normal and VIP prices for the same game and reader ("VR Racing - Normal AED 20 - VIP AED 15"), with VIP eligibility coming from a VIP product, membership, package or entitlement. Before identification the reader shows "Normal AED 20 / VIP AED 15"; after a VIP card tap "VIP RECOGNIZED - YOUR PRICE AED 15". The one thing to get right: who counts as VIP is a rule (what makes a guest VIP, valid when, for which games), not a flag typed on the guest.

**Known correction pending (do not draw the wrong version)**

- **VIP eligibility and the VIP rule (qualifying product / membership / package / entitlement, validity, applicable games) have no contract** Why: GamePricing has a single vipPrice and getGamePricing a free-text guestTier; nothing says what makes a card VIP. *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#/components/schemas/GamePricing / contracts/satellite/games.yaml#getGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen has only a select labelled "Attraction VR Racing" and a Save button** Why: A sample value used as a label; the pack gives the price table, four eligibility sources, the VIP rule and the reader display logic. *(source: screens/P08-venue-back-office.yaml#BO-440; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The reader cannot be told to show both prices** Why: displayRules has showPrice only, not "Normal and VIP". *(source: contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is VIP a guest tier from loyalty / membership, or only a purchased VIP product?** → Drawn default accepted: Any of the four sources the pack lists, configured as rules. *(decided by Chinmay, 2026-10-02; DEC-409 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Attraction: VR Racing | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attraction and prices**: Attraction picker (not a label "Attraction VR Racing"); a two-row table Customer type / Price - Normal (the standard price, read-only, link to BO-435) and VIP (money, lower than or equal to Normal unless confirmed). *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#/components/schemas/GamePricing)*
- **VIP eligibility**: Chips - VIP product, VIP membership, VIP package, VIP entitlement - each with a picker of the qualifying products / tiers. *(source: screens/P08-venue-back-office.yaml#BO-440)*
- **VIP rule**: Product / entitlement, valid from, valid to, applicable games / rides (multi-select), status. *(source: screens/P08-venue-back-office.yaml#BO-440)*
- **reader display**: Switch "Show both prices before a card is tapped" (default on) with a preview. *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#/components/schemas/Reader)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save game pricing (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader preview**: Idle "Normal AED 20 / VIP AED 15" and after-tap "VIP RECOGNIZED - YOUR PRICE AED 15", English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-440)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save game pricing**: Saves vipPrice in the attraction's whole pricing record (per VO-R04). *(source: contracts/satellite/games.yaml#setGamePricing)*
- **Preview for a guest**: Resolves the price with guestTier VIP at now, showing the trace (VIP beats Peak per the priority rules). *(source: contracts/satellite/games.yaml#getGamePricing)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The normal vip pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the normal vip pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No normal vip pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **VIP guest at peak time**: Per the pack's priority example, VIP AED 15 beats Peak AED 25; the preview states "VIP price has higher priority than Peak price". *(source: screens/P08-venue-back-office.yaml#BO-442)*
- **VIP eligibility expired yesterday**: Guest charged Normal; the reader shows the normal price, no VIP banner. *(source: screens/P08-venue-back-office.yaml#BO-440)*

#### Consistency with other screens

- Match `BO-441`: VIP's place in the price priority comes from Price Priority & Conflict Rules.
- Match `BO-411`: The VIP RECOGNIZED message is a reader display state; same theme component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
prices:
  attraction: VR Racing 01
  normal: AED 20.00
  vip: AED 15.00
rule:
  eligibility: VIP product
  product: Summit Peaks VIP Day (AED 350.00)
  validFrom: 01 Oct 2026
  validTo: 31 Dec 2026
  games:
  - VR Racing 01
  - Space Shooter
  - Basketball Pro 02
  status: Active
reader:
  idle: Normal AED 20 | VIP AED 15
  afterTap: 'VIP RECOGNIZED - YOUR PRICE: AED 15'
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-439` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-439`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 10: Works in Normal & VIP Pricing Configuration → Configure different prices for Normal and VIP guests for the same game/ride and reader. The source explicitly requires one reader to show both Normal Price and VIP Price for a specific game, with VIP …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-439?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save game pricing, Cancel.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-440` Retry Price Configuration

**Configure a discounted repeat-play price for applicable skill games. Requirement 10.2.16 describes a skill game where, before the game ends, the guest is offered: “Do you want to continue?” A subsequent RFID tap should deduct a lower amount than the original price.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-440 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Guest taps card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/retry-price-configuration-bo-440` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists stored retry prices.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A discounted repeat-play price for skill games (requirement 10.2.16): as the game approaches its end the reader offers "CONTINUE? - RETRY AED 10"; a tap within the retry window validates balance and retry eligibility, deducts the lower price and the game continues or restarts. Example Basketball Challenge - original AED 20, retry AED 10, window 30 seconds. The one thing to get right: a retry is a separate, recognisable transaction at the retry price, never a second full-price play and never confused with the free re-run after a machine fault.

**Known correction pending (do not draw the wrong version)**

- **Two different "retry" settings exist in the games contract** Why: ReaderProfile.retryPricing is a free re-run after a machine fault (isFree, withinSeconds, maxRetries); GamePricing.retryPrice is the commercial discounted continue. The screen must say which it sets and the names should differ. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderProfile / contracts/satellite/games.yaml#/components/schemas/GamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Maximum retry count, retry validity after first play and retry enabled have no field on GamePricing** Why: Only retryPrice and retryWindowSeconds exist. *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#/components/schemas/GamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A retry is not recognisable as such in the transaction record** Why: GameplayTransaction has no retry marker, so "recognized separately from a new gameplay transaction" (pack acceptance) cannot be reported. *(source: screens/P08-venue-back-office.yaml#BO-441 / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table titled "Every retry price"; gap says no operation returns a described schema** Why: Placeholder label (per VO-R12); and there is no read of stored retry prices to list. *(source: contracts/satellite/games.yaml#getGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the retry offer appear before the game ends (pack) or after it (DI-877), and does a retry consume an entitlement play?** → Drawn default stands (answer: "Retry charged in money at the retry price; offered in the last seconds of play and a short window after"): Offer shown in the last seconds of play and for the window after; a retry is charged in money at the retry price, never from an entitlement. *(decided by Chinmay, 2026-10-02; DEC-410 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attraction**: Picker limited to attractions whose type supports retry (Skill game = Yes is shown, not entered). *(source: screens/P08-venue-back-office.yaml#BO-440 / screens/P08-venue-back-office.yaml#BO-398)*
- **retry enabled, retry price**: Switch; retry price as money, lower than the standard price (shown beside it read-only). *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#/components/schemas/GamePricing)*
- **retry offer window**: Seconds (default 30) during which the offer is shown and a tap counts as a retry; must be longer than the retap delay on the reader. *(source: screens/P08-venue-back-office.yaml#BO-441 / contracts/satellite/games.yaml#/components/schemas/GamePricing / DI-877)*
- **maximum retry count, retry validity after first play**: Whole number (e.g. 2 retries per play) and seconds / minutes after the first play during which retries are allowed. *(source: screens/P08-venue-back-office.yaml#BO-440)*

#### Outputs: what the screen shows and produces

**Shown**

**Every retry price** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected retry price** (detail panel): The pack groups this record's detail under its own headings: “Basketball Challenge”, “Runtime Flow”, “Game approaching completion”, “Reader displays”, “RETRY AED 10”, “AED 10 deducted”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Retry prices list**: Titled "Retry prices" (not "Every retry price") - Attraction, Standard, Retry, Window, Max retries, Status. *(source: screens/P08-venue-back-office.yaml#BO-440)*
- **Runtime flow**: The pack's sequence as a strip - Initial play AED 20 - Game approaching completion - Reader shows CONTINUE? RETRY AED 10 - Guest taps - Balance and retry eligibility checked - AED 10 deducted - Game continues - with the reader mock-up. *(source: screens/P08-venue-back-office.yaml#BO-441)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves retryPrice and retryWindowSeconds in the attraction's whole pricing record (per VO-R04) and offers deployment to the reader. *(source: contracts/satellite/games.yaml#setGamePricing)*

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retry price list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retry price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retry price yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the retry price are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Guest taps for retry with an entitlement (e.g. 3 plays on Basketball Pro)**: A retry is charged in money at the retry price, never from an entitlement play; the offer shows in the last seconds of play and for a short window after. Show the rule on the screen. *(source: screens/P08-venue-back-office.yaml#BO-430 / screens/P08-venue-back-office.yaml#BO-441 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Retry tap inside the retap delay**: Treated as the same retry, not a second one (retap protection still applies). *(source: DI-867)*

#### Consistency with other screens

- Match `BO-409`: Show the reader's retap delay next to the retry window; window must exceed it.
- Match `BO-412`: The retry tap is a distinct outcome in the tap flow ("RETRY AUTHORIZED AED 10").
- Match `BO-441`: Retry is first in the pack's price priority example.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- attraction: Basketball Challenge
  standard: AED 20.00
  retry: AED 10.00
  windowSeconds: 30
  maxRetries: 2
  validityAfterFirstPlay: 2 minutes
  status: Active
- attraction: Prize Crane 04
  standard: AED 15.00
  retry: AED 8.00
  windowSeconds: 20
  maxRetries: 1
  status: Active
reader: CONTINUE? RETRY AED 10
```

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-440` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-440`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 12: Works in Retry Price Configuration → Configure a discounted repeat-play price for applicable skill games. Requirement 10.2.16 describes a skill game where, before the game ends, the guest is offered: “Do you want to continue?” A …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-440?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-441` Price Priority & Conflict Rules

**Define which pricing rule wins when several valid prices apply simultaneously. This is required to make the source pricing models operational because Standard, Group, Peak, VIP and Retry prices can overlap.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-441 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/price-priority-conflict-rules-bo-441` |

**What the spec says about it.** **Core, not games (2 October 2026, CHG-SBO-023):** the rule order governs every price at the venue, so a tenant without the games licence still needs it; filed under Sell (CHG-SBO-010).

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The order in which pricing rules apply when several are valid at once (standard, group, peak, VIP, retry) and the method that resolves two of them, with a test console that prices a scenario against the order. The client was explicit: the configured hierarchy decides; there is no automatic lowest-price-wins.

**Fixed on main** (the package already carries these; draw what it says): The screen's module is Games & Rides while the rule order governs every price at the venue. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Case type | select | — | Low demand · High demand · Near sell out · Early bird · Last minute · Weekend peak · Member purchase · B2B contract · Custom | `listRulePriorityConflict` ?caseType |
| Conflict code | select | — | Contradictory rules · Same priority · Impossible condition · Overlapping strategy · Circular dependency · Missing fallback · Guardrail conflict | `listRulePriorityConflict` ?conflictCode |
| Strategy | text field | — | — | `listRulePriorityConflict` ?strategyId |

**Sent by *Reorder / Validate / Test / Save*** (`setRulePriorityConflict`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Ordered rules `orderedRuleIds` | list of values (chips) | optional | — | — | — | The rules in priority order, highest first. Reorder is this list. | `setRulePriorityConflict` body |
| Resolution method `resolutionMethod` | select | optional | Highest priority wins | Highest priority wins · Most specific rule wins · Cumulative adjustment · Maximum adjustment wins · Minimum adjustment wins · Weighted combination · Stop processing · Custom governed resolution | — | How two applicable rules are resolved; the same vocabulary as `RulePriorityConflictResolutionDynamicPricingTestConsSummary.resolutionMethod`. | `setRulePriorityConflict` body |
| Priority hierarchy `priorityHierarchy` | multi-select chips | optional | — | Commercial protection · Contract member protection · Event specific strategy · Inventory occupancy · Booking velocity · Time to event · Season day timeslot · Base price | — | The priority matrix, highest first; defaults to the pack's order. | `setRulePriorityConflict` body |
| Mode `mode` | segmented control | required | — | Save · Validate · Test | — | `validate` checks the order and returns conflicts without saving; `test` runs `testScenario` against the order and saves it as a test case; `save` stores the order and method … | `setRulePriorityConflict` body |
| Test scenario `testScenario` | group | optional | — | — | — | A sample booking for the conflict test console (pack p.90), the same inputs as a saved test case. | `setRulePriorityConflict` body |
| Case name `testScenario.caseName` | text field | optional | — | max length 120 | — | — | `setRulePriorityConflict` body |
| Case type `testScenario.caseType` | select | optional | — | Low demand · High demand · Near sell out · Early bird · Last minute · Weekend peak · Member purchase · B2B contract · Custom | — | — | `setRulePriorityConflict` body |
| Product `testScenario.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Event `testScenario.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Performance `testScenario.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Date `testScenario.date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setRulePriorityConflict` body |
| Timeslot `testScenario.timeslot` | text field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Channel `testScenario.channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setRulePriorityConflict` body |
| Customer segment `testScenario.customerSegment` | text field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Base price `testScenario.basePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setRulePriorityConflict` body |
| Occupancy `testScenario.occupancy` | stepper or slider | optional | — | min 0; max 100 | — | — | `setRulePriorityConflict` body |
| Inventory `testScenario.inventory` | number field | optional | — | min 0 | — | — | `setRulePriorityConflict` body |
| Booking velocity `testScenario.bookingVelocity` | number field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Time to event `testScenario.timeToEvent` | number field | optional | — | min 0 | — | — | `setRulePriorityConflict` body |
| Expected price `testScenario.expectedPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setRulePriorityConflict` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **orderedRuleIds**: Drag-to-order list, highest priority first, with a rank number shown on each row. *(source: contracts/spine/catalogue.yaml#setRulePriorityConflict)*
- **resolutionMethod**: One of eight methods, each with a one-line worked example (Highest priority wins, Most specific wins, Cumulative, Maximum adjustment, Minimum adjustment, Weighted, Stop processing, Custom governed). *(source: contracts/spine/catalogue.yaml#setRulePriorityConflict / DI-595)*
- **test scenario**: Product, ticket type, date and time, channel, party; the result shows every rule considered, which applied and the final price. *(source: contracts/spine/catalogue.yaml#setRulePriorityConflict)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Reorder / Validate / Test / Save (primary button) | `setRulePriorityConflict` PUT `/rule-priority-conflict` | RulePriorityConflictInput | RulePriorityConflictView | 409 `save` while a critical conflict is open (`criticalConflictOpen`); the conflicts are named in the problem.; 422 `test` without a `testScenario` (`testScenarioRequired`), or `orderedRuleIds` naming a rule that does … | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Validate / Test / Save**: Three buttons over one body; Validate returns conflicts without saving, Test runs the scenario and keeps it as a test case, Save stores the order. *(source: contracts/spine/catalogue.yaml#setRulePriorityConflict)*

**Data it reads**: `listRulePriorityConflict` (onLoad, Rule Priority, Conflict Resolution & Dynamic Pricing Test …)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price priority conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price priority conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price priority conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price priority conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `save` while a critical conflict is open (`criticalConflictOpen`); the conflicts are named in the problem.; 422 `test` without a `testScenario` (`testScenarioRequired`), or `orderedRuleIds` naming a rule that does not exist or is archived (`unknownRule`). |

#### Consistency with other screens

- Match `ADM-097`: The same operation serves the P09 console screen; same order list and test console.
- Match `ADM-055`: Price hierarchy (which source of a price wins) is a different question from rule priority (which adjustment wins); label both explicitly.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
- Commercial protection
- Contract / member protection
- Event strategy
- Occupancy
- Booking pace
- Time to event
- Season / day / time slot
- Base price
test:
  product: Sandstorm Coaster retry
  date: 2026-11-14 16:00
  channel: Point of sale
  result: 'AED 25.00 (Retry price; Peak uplift not applied: Stop processing)'
```

#### Permissions

- `listRulePriorityConflict` → `PRODUCT_VIEW` (read) · staff
- `setRulePriorityConflict` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-441` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-441`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F147 *Pricing Revenue Management board 5: Dynamic Pricing Strategy Command Center*, step 18: Works in Rule Priority, Conflict Resolution & Dynamic Pricing Test Console → Determine the final dynamic price when multiple strategies and rules are simultaneously applicable. This is the final and most important control screen of Board 5.
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 14: Works in Price Priority & Conflict Rules → Define which pricing rule wins when several valid prices apply simultaneously. This is required to make the source pricing models operational because Standard, Group, Peak, VIP and Retry prices can …

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-441?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Reorder / Validate / Test / Save.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-442` Effective Pricing & Reader Price Preview

**Allow an administrator to preview what price will actually be presented/applied for a selected game before publishing configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-442 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/effective-pricing-reader-price-preview-bo-442` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The pricing simulator for games and rides: an administrator picks a game, a reader, a moment and a kind of guest and sees the one price TICVAI will charge, every rule that was considered, and what the physical reader will show. It answers the board's single question ("when this customer taps this reader at this game at this time, what do we charge?"). The one thing to get right: the screen must visibly connect the backend decision (rule evaluation) to the reader mockup; TICVAI calculates, the reader only displays.

**Known correction pending (do not draw the wrong version)**

- **Retry status and Package / entitlement are drawn as live filters** Why: The price read takes only gameId, readerId, at and guestTier; these two inputs change nothing on the wire. Grey them or route them through the tap simulation. *(source: screens/P08-venue-back-office.yaml#BO-442 / contracts/satellite/games.yaml#getGamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reader preview binds a "Normal price on reader" field** Why: No such field exists; the normal price is a second resolution without guestTier. Say so in the binding rather than inventing a property. *(source: contracts/satellite/games.yaml#/components/schemas/GamePriceResolution; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's priority list names Date/Time Override and Attraction-Specific Price** Why: The contract's priority vocabulary is calendarException, peak, group, vip, retry, standard; there is no attraction-specific tier (every price is per game). Use the contract's names on this screen and BO-441. *(source: screens/P08-venue-back-office.yaml#BO-441 / contracts/satellite/games.yaml#/components/schemas/GamePricing; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack says "before publishing configuration"; should the preview evaluate a draft price change, not only what is live?** → Drawn default accepted: Show a "Published pricing" badge and a greyed "Include draft changes" toggle until the price read accepts a draft or version parameter. *(decided by Chinmay, 2026-10-02; DEC-411 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Game or attraction | select field | — | — | — | — | Sends `?gameId=` (required). | — |
| Reader | select field | — | — | — | — | Sends `?readerId=`; the preview shows what this reader will display. | — |
| Date and time | date picker | — | — | — | — | Sends `?at=`; covers the pack's Date and Time inputs. | — |
| Customer type / VIP status | select field | — | — | — | — | Sends `?guestTier=`. | — |
| Retry status | select field | — | — | — | — | A pack simulation input with no query parameter. | — |
| Package / entitlement | select field | — | — | — | — | A pack simulation input with no query parameter. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Game | picker: choose a game | — | — | `getGamePricing` ?gameId |
| Reader | picker: choose a reader | — | — | `getGamePricing` ?readerId |
| At | date and time picker | — | — | `getGamePricing` ?at |
| Guest tier | text field | — | — | `getGamePricing` ?guestTier |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Venue**: Not a field. The pack lists Venue as a simulation input, but the venue is the one in the top-bar venue switcher; show it as read-only context above the inputs ("Simulating at Summit Peaks"). *(source: screens/P08-venue-back-office.yaml#BO-442)*
- **Game (gameId)**: Required, searchable select of games in the venue grouped by attraction type (Rides, Skill games, Video games); nothing is evaluated until a game is chosen. Show the game's status beside it; a game that is out of service still simulates but carries an "Out of service" warning. *(source: contracts/satellite/games.yaml#getGamePricing / DI-863)*
- **Reader (readerId)**: Optional select filtered to readers mapped to the chosen game; defaults to the game's mapped reader. With no reader chosen the preview shows a generic reader frame. *(source: contracts/satellite/games.yaml#getGamePricing / contracts/satellite/games.yaml#/components/schemas/Game)*
- **Date and time (at)**: One date-time picker in venue local time, default "Now"; quick chips for "Now", "This Saturday 20:00" and "Next public holiday" so peak and calendar-exception rules can be tried in one click. The pack's Date and Time inputs are one value on the wire. *(source: screens/P08-venue-back-office.yaml#BO-442 / contracts/satellite/games.yaml#getGamePricing)*
- **Customer type / VIP status (guestTier)**: One segmented control (Normal, VIP), not two fields: the pack's Customer Type and VIP Status are the same parameter. Default Normal. *(source: screens/P08-venue-back-office.yaml#BO-440 / contracts/satellite/games.yaml#getGamePricing)*
- **Retry status, Package / entitlement**: Draw them, greyed, with "Not yet part of the simulation" (per VO-R13): the price read takes no retry or entitlement parameter. Offer instead "Simulate with a real card" which runs the full tap decision (entitlement, funding and price) for a card number and shows the outcome beside the price. *(source: contracts/satellite/games.yaml#getGamePricing / contracts/satellite/games.yaml#simulateGameplayAuthorisation)*

#### Outputs: what the screen shows and produces

**Shown**

**Final price** (metric tile, from `getGamePricing`)

| Shows | Format | Notes |
|---|---|---|
| Effective price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Applied rule** (metric tile, from `getGamePricing`)

| Shows | Format | Notes |
|---|---|---|
| Applied rule | text | — |

**Rule evaluation** (data table, from `getGamePricing`): Every candidate rule in evaluation order, the winner marked; matches the pack's Standard / Peak / VIP walk-through.

| Shows | Format | Notes |
|---|---|---|
| Rule | text | — |
| Applied | yes / no (icon or chip) | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Skipped because | text | — |

**Reader preview** (detail panel, from `getGamePricing`): The pack's reader mockup ("SKY COASTER / Normal AED 45 / VIP AED 30 / TAP TO PLAY"). The normal price can be read from the trace's untiered rule, but no field names it.

| Shows | Format | Notes |
|---|---|---|
| Game | the name it points at, never the id | — |
| Effective price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Normal price on reader | text | not in the schema: `Normal price on reader` |
| Reader display text | text | not in the schema: `Reader display text` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Final price tile**: Large "AED 30.00" with the applied rule in words under it ("VIP pricing"); never a bare rule code. When the game is closed by a calendar exception show "Closed on 31 Dec 2026" instead of a price. *(source: contracts/satellite/games.yaml#/components/schemas/GamePriceResolution / contracts/satellite/games.yaml#/components/schemas/GamePricingException)*
- **Rule evaluation table**: One row per candidate rule in the configured priority order (the order set on BO-441), columns Rule, Price, Result. The winner carries a tick and "Applied"; the others show skippedBecause in plain words ("Lower priority than VIP", "Not peak at 20:00 on Saturday", "Group needs 4 players"). Rules that did not match stay visible; hiding them hides why a price is what it is. *(source: screens/P08-venue-back-office.yaml#BO-442 / contracts/satellite/games.yaml#/components/schemas/GamePriceResolution)*
- **Reader preview**: A physical reader mockup in two states, side by side: before identification ("SKY COASTER / Normal AED 45 / VIP AED 30 / TAP TO PLAY") and after a VIP tap ("VIP RECOGNIZED / YOUR PRICE AED 30"). The Normal line comes from a second price read without guestTier; the reader frame uses the reader's theme and the tenant brand, in English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-440 / screens/P08-venue-back-office.yaml#BO-443 / DI-862)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Simulate**: Runs the price read with the chosen inputs; re-runs automatically when any input changes. A failed read keeps the last result greyed with "Could not recalculate, retry". *(source: contracts/satellite/games.yaml#getGamePricing)*
- **Simulate with a real card**: Asks for a card number and runs the tap simulation; shows Allowed or the refusal reason with the guest message the reader would show. It changes nothing on the card. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*
- **Open the rule**: Each rule row links to the screen that owns it (BO-435 standard, BO-436 group, BO-437 peak, BO-438 calendar, BO-439 VIP, BO-440 retry, BO-441 priority). *(source: F191 step 16 / screens/P08-venue-back-office.yaml#BO-434)*

**Data it reads**: `getGamePricing` (onLoad, What the reader will charge)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The effective pricing reader list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the effective pricing reader untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No effective pricing reader yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the effective pricing reader are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No rule produces a price for this game and time**: Show "No price at this time; the reader would refuse this tap" in red with a link to BO-435, rather than AED 0.00. A zero price is a free game, which is a different statement. *(source: screens/P08-venue-back-office.yaml#BO-468 / contracts/satellite/games.yaml#/components/schemas/GameConfigurationHealth)*
- **Two rules of equal priority both match**: Cannot happen by construction (priority is an ordered list), so the table always has exactly one Applied row; if the read returns none, treat it as no price. *(source: screens/P08-venue-back-office.yaml#BO-442 / contracts/satellite/games.yaml#/components/schemas/GamePricing)*
- **Simulated date in the past**: Allowed (for investigating a complaint), with a note that rules are evaluated as configured now, not as they were then. *(source: designer default)*
- **Viewer without price rights**: The screen is read-only by nature; without PRICE_VIEW show the no-access state naming the permission. *(source: contracts/satellite/games.yaml#getGamePricing)*

#### Consistency with other screens

- Match `BO-441`: The rule order in the evaluation table is the order defined on Price Priority & Conflict Rules; use the same rule names (Retry, VIP, Calendar exception, Peak, Group, Standard).
- Match `BO-480`: The reader mockup is the same component as the Reader Screen, LED & Sound preview; one drawing, two uses.
- Match `BO-490`: The guest's "What can I play?" price is resolved by the same priority, so the same card at the same time must show the same price on both.
- Match `BO-443`: Publication governs what the reader receives; this screen previews pricing before it is published (see open question).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation:
  game: Sky Coaster
  reader: R-001
  at: Sat 03 Oct 2026 20:00
  guestTier: VIP
evaluation:
- rule: VIP pricing
  price: AED 30.00
  result: Applied
- rule: Peak (Fri-Sat 18:00-23:00)
  price: AED 45.00
  result: Lower priority than VIP
- rule: Standard
  price: AED 35.00
  result: Lower priority than VIP
reader:
  line1: SKY COASTER
  line2: Normal AED 45 | VIP AED 30
  line3: TAP TO PLAY
```

#### Permissions

- `getGamePricing` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-442` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-442`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 16: Works in Effective Pricing & Reader Price Preview → Allow an administrator to preview what price will actually be presented/applied for a selected game before publishing configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-442?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-443` Pricing Audit, Approval & Publication

**Govern pricing changes and maintain a full historical record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-443 |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/games-rides/pricing-audit-approval-publication-bo-443` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-025): listPricing is the AI pricing intelligence view, not the population of a pricing audit and publication screen; the screen keeps listDynamicPriceRules (the rules …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Governs pricing changes with a full history: what is approved, what becomes effective when, and only approved prices reaching runtime. Publication can be immediate, scheduled, from a future effective date or staged by market, venue or channel; never retroactive.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listDynamicPriceRules return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The screen sits in the Games & Rides module and lists listPricing (an AI pricing intelligence view) as its population. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Sent by *What publishing changes*** (`publishPricingEffectiveDate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | optional | — | — | — | Approved pricing version to publish | `publishPricingEffectiveDate` body |
| Publication date `publicationDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish configuration at (empty for immediate) | `publishPricingEffectiveDate` body |
| Effective date `effectiveDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sales effective from; must not be in the past (never retroactive) | `publishPricingEffectiveDate` body |
| Expiry date `expiryDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Expiry; empty for open-ended | `publishPricingEffectiveDate` body |
| Venue `venue` | text field | optional | — | — | — | Scope: venue; empty for all venues in the version | `publishPricingEffectiveDate` body |
| Market `market` | text field | optional | — | — | — | Scope: market; empty for all | `publishPricingEffectiveDate` body |
| Channel `channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Scope: channel; empty for all | `publishPricingEffectiveDate` body |
| Change request `changeRequestId` | text field | optional | — | — | — | Change request being published | `publishPricingEffectiveDate` body |
| Publication mode `publicationMode` | radio group | optional | — | Immediate · Scheduled · Future effective date · Staged | — | Publication Mode (pack p.66) | `publishPricingEffectiveDate` body |
| Visit effective from `visitEffectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Visit dates from which the new prices apply, when different from the sales effective date | `publishPricingEffectiveDate` body |
| Stages `stages` | repeatable rows | optional | — | — | — | Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel) | `publishPricingEffectiveDate` body |
| Dimension `stages[].dimension` | segmented control | optional | — | Market · Venue · Channel | — | Staged by | `publishPricingEffectiveDate` body |
| Target `stages[].target` | text field | optional | — | — | — | Market, venue or channel ID | `publishPricingEffectiveDate` body |
| Publication date `stages[].publicationDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at | `publishPricingEffectiveDate` body |
| Effective date `stages[].effectiveDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Effective from | `publishPricingEffectiveDate` body |
| Cancel `cancel` | toggle | optional | — | — | — | True cancels this scheduled publication; allowed only before activation | `publishPricingEffectiveDate` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **effectiveDate**: Cannot be in the past; visit dates may differ from sales dates ("prices for visits from 1 Jan, on sale from 1 Dec"). *(source: contracts/spine/catalogue.yaml#publishPricingEffectiveDate)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule Publication (secondary button) | navigation or local | — | — | — | — |
| Deactivate Rule (destructive button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | `publishPricingEffectiveDate` PUT `/pricing-effective-date` | PricingPublicationEffectiveDateSchedulerInput | PricingPublicationEffectiveDateSchedulerView | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **pre-publication checks and collisions**: The checks with pass or fail and any collision with another scheduled publication, before Publish. *(source: contracts/spine/catalogue.yaml#publishPricingEffectiveDate)*

**Data it reads**: `listDynamicPriceRules` (onLoad, The dynamic price rules reviewed and published here)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

**What opens over it**

- confirmDialog *Deactivate Rule*: **Deactivate Rule on a pricing audit approval is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing audit approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing audit approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing audit approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing audit approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
publication:
  version: Games pricing v12
  mode: futureEffectiveDate
  effective: 2026-12-01 00:00
  channel: Point of sale
  checks: 6 of 6 passed
```

#### Permissions

- `publishPricingEffectiveDate` → `PRODUCT_CONFIGURE` (configure) · staff
- `setDynamicPriceRule` → `PRICE_CONFIGURE` (configure) · staff
- `listDynamicPriceRules` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.17 | - Dynamic Pricing | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.9.10 | The system should have the ability to setup dynamic pricing rules of onsite and digital tickets based on seasonality, day of the week, guest type, time of day, capacity and group size. | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.13.39 | Dynamic Pricing Support | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 8.5.5 | System shall support seasonal pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.6 | System shall support event-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.7 | System shall support day-of-week pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.8 | System shall support time-slot pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.9 | System shall support customer-segment pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.10 | System shall support channel-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.11 | System shall support location-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 2.1.23 | POS shall retrieve real-time prices from the Dynamic Pricing Engine based on date, timeslot, demand, capacity, promotions, customer segment, and channel. | Ticketing Sales | CONTRACTED | `listDynamicPriceRules` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-443` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-443`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 18: Works in Pricing Audit, Approval & Publication → Govern pricing changes and maintain a full historical record.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-443?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule Publication, Deactivate Rule, What publishing changes.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
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
"getGamePricing": {"method":"GET","path":"/game-pricing","contract":"games","summary":"The effective price at a reader, and why","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"gameId","in":"query","required":true},{"name":"readerId","in":"query","required":null},{"name":"at","in":"query","required":null},{"name":"guestTier","in":"query","required":null}],"requestBody":null,"responds":"GamePriceResolution"},
"listDynamicPriceRules": {"method":"GET","path":"/pricing/dynamic-rules","contract":"catalogue","summary":"Dynamic pricing rules","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PricingDynamicPriceRule"},
"listRulePriorityConflict": {"method":"GET","path":"/rule-priority-conflict","contract":"catalogue","summary":"Rule Priority, Conflict Resolution & Dynamic Pricing Test Console","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"caseType","in":"query","required":false},{"name":"conflictCode","in":"query","required":false},{"name":"strategyId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishPricingEffectiveDate": {"method":"PUT","path":"/pricing-effective-date","contract":"catalogue","summary":"Pricing Publication & Effective-Date Scheduler","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingPublicationEffectiveDateSchedulerInput","responds":"PricingPublicationEffectiveDateSchedulerView"},
"setDynamicPriceRule": {"method":"PUT","path":"/pricing/dynamic-rules/{ruleId}","contract":"catalogue","summary":"Replace a rule, its conditions and its actions","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"DynamicPriceRuleDetail","responds":"DynamicPriceRuleDetail"},
"setGamePricing": {"method":"PUT","path":"/game-pricing","contract":"games","summary":"Standard, group, peak, VIP, retry and calendar prices","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GamePricing","responds":"GamePricing"},
"setRulePriorityConflict": {"method":"PUT","path":"/rule-priority-conflict","contract":"catalogue","summary":"Reorder, validate, test or save the pricing rule priority","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RulePriorityConflictInput","responds":"RulePriorityConflictView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"DynamicPriceRuleDetail": {"type":"object","x-ticvai-persistence":"none — composed from a rule, its conditions and its actions","description":"**A rule is unreadable without both halves.** The conditions say when it fires, the actions say what it does to the price, and `minPrice`/`maxPrice` on the action are the guard rails a reviewer looks for first.\n","required":["rule"],"properties":{"rule":{"$ref":"#/components/schemas/PricingDynamicPriceRule"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceCondition"}},"actions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceAction"}}}},
"GamePriceResolution": {"type":"object","description":"Board 5.9. **What will this actually charge.**","properties":{"gameId":{"type":"string","format":"uuid"},"effectivePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedRule":{"type":"string"},"trace":{"type":"array","items":{"type":"object","properties":{"rule":{"type":"string"},"applied":{"type":"boolean"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"skippedBecause":{"type":"string","nullable":true}}}}}},
"GamePricing": {"type":"object","x-ticvai-persistence":"games.pricing","description":"Board 5. **Priority is explicit**, because evaluation order is not a decision anybody made.\n`groupPricing`, `peakPricing` and `calendarExceptions` are stored one row per entry in `games.pricing_exception` (`GamePricingException`); the rest of this shape is `games.pricing`.\n","properties":{"gameId":{"type":"string","format":"uuid"},"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"vipPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"groupPricing":{"type":"array","items":{"type":"object","properties":{"minimumPlayers":{"type":"integer"},"pricePerPlayer":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"peakPricing":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"calendarExceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closed":{"type":"boolean","default":false}}}},"retryPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"retryWindowSeconds":{"type":"integer","nullable":true,"description":"How long after the game ends the retry offer stays open."},"retryOfferLeadSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"**When the retry offer appears** (Chinmay, 2 October, workbook Q410, default accepted; DI-877; CHG-CSA-028): this many seconds before the game ends, and it stays open `retryWindowSeconds` after. A retry is charged in money at `retryPrice`, never from an entitlement; a retry after a machine fault is the reader's `retryPricing`, not this."},"priority":{"type":"array","items":{"type":"string","enum":["calendarException","peak","group","vip","retry","standard"]}},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PricingDynamicPriceAction": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_action","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price action.","required":["dynamicPriceRuleId","type","value"],"properties":{"id":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":30},"value":{"type":"number"},"minPrice":{"type":"number","nullable":true},"maxPrice":{"type":"number","nullable":true}}},
"PricingDynamicPriceCondition": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_condition","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule condition.","required":["actionId","dynamicPriceRuleId","type","ruleOperator","valueJson","sequenceNo"],"properties":{"actionId":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":50},"ruleOperator":{"type":"string","maxLength":20},"valueJson":{"type":"string"},"sequenceNo":{"type":"integer"}}},
"PricingDynamicPriceRule": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_rule","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule.","required":["pricingRuleCode","name","priority","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"pricingRuleCode":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"integer"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"dynamicPricingStrategyId":{"type":"string","format":"uuid","nullable":true,"description":"The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). Null for a static pricing rule."},"ruleType":{"type":"string","maxLength":40,"nullable":true,"description":"Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`."},"inputMetric":{"type":"string","maxLength":40,"nullable":true},"conditionLogic":{"type":"string","enum":["all","any"],"default":"all"},"cooldownMinutes":{"type":"integer","nullable":true,"minimum":0},"minimumDurationMinutes":{"type":"integer","nullable":true,"minimum":0},"exitThresholdOffset":{"type":"number","nullable":true},"rangeMinPercent":{"type":"number","nullable":true},"rangeMaxPercent":{"type":"number","nullable":true},"isProtected":{"type":"boolean","default":false,"description":"A protected segment or channel: dynamic adjustments never apply."}}},
"PricingPublicationEffectiveDateSchedulerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Pricing Publication & Effective-Date Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"version":{"type":"string","description":"Approved pricing version to publish"},"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"}}},
"PricingPublicationEffectiveDateSchedulerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Publication & Effective-Date Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"version":{"type":"string","description":"Approved pricing version to publish"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"},"prePublicationChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["approvalComplete","validationPassed","noCriticalConflicts","dependenciesAvailable","channelsReady","effectiveDatesValid"],"description":"Pre-Publication Check (pack p.67)"},"passed":{"type":"boolean","description":"Passed"},"message":{"type":"string","description":"Detail, e.g. the colliding version","nullable":true}},"description":"One check"},"description":"Pre-publication check results"},"collisions":{"type":"array","items":{"type":"string"},"description":"Other versions scheduled to become effective for the same object and date"},"status":{"type":"string","description":"Status: scheduled, blocked, published, cancelled or failed"}}},
"RulePriorityConflictInput": {"type":"object","x-ticvai-persistence":"none — request only; the saved hierarchy and test cases are the rows listRulePriorityConflict reads","description":"What `setRulePriorityConflict` takes (decided 29 September, readiness close-out; VM close-out for BO-441 Reorder, Validate, Test, Save).","required":["mode"],"properties":{"orderedRuleIds":{"type":"array","description":"The rules in priority order, highest first. Reorder is this list.","items":{"type":"string"}},"resolutionMethod":{"type":"string","enum":["highestPriorityWins","mostSpecificRuleWins","cumulativeAdjustment","maximumAdjustmentWins","minimumAdjustmentWins","weightedCombination","stopProcessing","customGovernedResolution"],"default":"highestPriorityWins","description":"How two applicable rules are resolved; the same vocabulary as `RulePriorityConflictResolutionDynamicPricingTestConsSummary.resolutionMethod`. Never lowest-price-wins by default (decided 29 September, readiness close-out)."},"priorityHierarchy":{"type":"array","description":"The priority matrix, highest first; defaults to the pack's order.","items":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"]}},"mode":{"type":"string","enum":["save","validate","test"],"description":"`validate` checks the order and returns conflicts without saving; `test` runs `testScenario` against the order and saves it as a test case; `save` stores the order and method, refused with `409` while a critical conflict is open."},"testScenario":{"$ref":"#/components/schemas/RulePriorityTestScenario"}}},
"RulePriorityConflictResolutionDynamicPricingTestConsSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Rule Priority, Conflict Resolution & Dynamic Pricing Test Console.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"contradictoryRules":{"type":"integer","description":"Open contradictoryRules conflicts detected across active and draft rules"},"samePriority":{"type":"integer","description":"Open samePriority conflicts detected across active and draft rules"},"impossibleCondition":{"type":"integer","description":"Open impossibleCondition conflicts detected across active and draft rules"},"overlappingStrategy":{"type":"integer","description":"Open overlappingStrategy conflicts detected across active and draft rules"},"circularDependency":{"type":"integer","description":"Open circularDependency conflicts detected across active and draft rules"},"missingFallback":{"type":"integer","description":"Open missingFallback conflicts detected across active and draft rules"},"guardrailConflict":{"type":"integer","description":"Open guardrailConflict conflicts detected across active and draft rules"},"resolutionMethod":{"type":"string","enum":["highestPriorityWins","mostSpecificRuleWins","cumulativeAdjustment","maximumAdjustmentWins","minimumAdjustmentWins","weightedCombination","stopProcessing","customGovernedResolution"],"description":"Resolution Method in force (pack p.89); defaults to highestPriorityWins (decided 29 September, readiness close-out)"},"priorityHierarchy":{"type":"array","items":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"]},"description":"Priority Matrix, highest first; defaults to the pack's order (decided 29 September, readiness close-out)"}}},
"RulePriorityConflictResolutionDynamicPricingTestConsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Rule Priority, Conflict Resolution & Dynamic Pricing Test Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Test input: product"},"event":{"type":"string","description":"Test input: event","nullable":true},"performance":{"type":"string","description":"Test input: performance","nullable":true},"date":{"type":"string","format":"date","description":"Test input: visit/event date"},"timeslot":{"type":"string","description":"Test input: timeslot","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Test input: channel"},"customerSegment":{"type":"string","description":"Test input: customer segment"},"basePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Test input: base price"},"occupancy":{"type":"number","description":"Test input: occupancy percent"},"inventory":{"type":"integer","description":"Test input: remaining inventory"},"bookingVelocity":{"type":"number","description":"Test input: booking velocity, percent against expected pace"},"timeToEvent":{"type":"integer","description":"Test input: days to event (0 = same day)"},"calculationPath":{"type":"array","items":{"type":"string"},"description":"Explainability: the complete calculation path, one step per line"},"testCaseId":{"type":"string","description":"Test case ID"},"caseName":{"type":"string","description":"Test case name"},"caseType":{"type":"string","enum":["lowDemand","highDemand","nearSellOut","earlyBird","lastMinute","weekendPeak","memberPurchase","b2bContract","custom"],"description":"Test case type (pack p.91)"},"rulesMatched":{"type":"array","items":{"type":"object","properties":{"ruleId":{"type":"string","description":"Rule"},"ruleName":{"type":"string","description":"Rule name"},"priorityLevel":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"],"description":"Hierarchy level"},"adjustmentPercent":{"type":"number","description":"Adjustment in percent","nullable":true},"applied":{"type":"boolean","description":"Applied after resolution"}},"description":"One matched rule"},"description":"Rules matched"},"rawCalculatedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Raw calculated price"},"ladderPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Nearest allowed band"},"guardrailOutcome":{"type":"string","enum":["passed","cappedAtMaximum","raisedToMinimum","protectedRateApplied"],"description":"Guardrail result"},"finalPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Final dynamic price"},"conflicts":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["contradictoryRules","samePriority","impossibleCondition","overlappingStrategy","circularDependency","missingFallback","guardrailConflict"],"description":"Conflict type (pack p.90)"},"message":{"type":"string","description":"Message"},"ruleIds":{"type":"array","items":{"type":"string"},"description":"Rules involved"}},"description":"One conflict"},"description":"Conflicts met while resolving this case"},"lastRunAt":{"type":"string","format":"date-time","description":"Last run"},"passed":{"type":"boolean","description":"Final price matched the expected price saved with the case","nullable":true},"expectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Expected final price for regression","nullable":true}}},
"RulePriorityConflictView": {"type":"object","x-ticvai-persistence":"none — projection over the saved priority order and test cases","description":"What `setRulePriorityConflict` returns: the order in force, the conflicts it has and, in `test` mode, the result.","properties":{"mode":{"type":"string","enum":["save","validate","test"]},"saved":{"type":"boolean"},"orderedRuleIds":{"type":"array","items":{"type":"string"}},"resolutionMethod":{"type":"string"},"priorityHierarchy":{"type":"array","items":{"type":"string"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["contradictoryRules","samePriority","impossibleCondition","overlappingStrategy","circularDependency","missingFallback","guardrailConflict"]},"severity":{"type":"string","enum":["critical","warning"]},"ruleIds":{"type":"array","items":{"type":"string"}},"message":{"type":"string"}}}},"testResult":{"nullable":true,"allOf":[{"$ref":"#/components/schemas/RulePriorityConflictResolutionDynamicPricingTestConsView"}],"description":"The saved test case with its deterministic result, in `test` mode."},"savedAt":{"type":"string","format":"date-time","nullable":true}}},
"RulePriorityTestScenario": {"type":"object","description":"A sample booking for the conflict test console (pack p.90), the same inputs as a saved test case.","properties":{"caseName":{"type":"string","maxLength":120},"caseType":{"type":"string","enum":["lowDemand","highDemand","nearSellOut","earlyBird","lastMinute","weekendPeak","memberPurchase","b2bContract","custom"]},"productId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date"},"timeslot":{"type":"string","nullable":true},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"customerSegment":{"type":"string","nullable":true},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"occupancy":{"type":"number","minimum":0,"maximum":100},"inventory":{"type":"integer","minimum":0},"bookingVelocity":{"type":"number"},"timeToEvent":{"type":"integer","minimum":0},"expectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true}}}
}
```
