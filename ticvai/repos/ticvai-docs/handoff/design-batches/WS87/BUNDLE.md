# WS87 — Game and Ride board 10

**10 screens · 9 operations · 10 schemas · 4 permissions**

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
  `PRODUCT_VIEW, TENANT_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-484` | Self-Service Experience Command Center | B | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-485` | Self-Service Kiosk Profile & Channel Configuration | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-486` | Customer Card / Wallet Identification | D | 0 | 4 | 6 | 2 | 1 | 6 | — | notStarted (—) |
| `BO-487` | Customer Wallet & Balance Summary | C | 0 | 6 | 6 | 16 | 1 | 6 | — | notStarted (—) |
| `BO-488` | Self-Service Wallet Top-Up | C | 0 | 15 | 6 | 33 | 1 | 6 | — | notStarted (—) |
| `BO-489` | Bonus, Free Game & Benefit View | D | 3 | 17 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-490` | Game & Ride Eligibility / “What Can I Play?” | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-491` | Redemption Balance & Prize Discovery | D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-492` | Customer Game & Wallet Transaction History | D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-493` | Self-Service UI Theme, Language & Journey Configuration | D | 4 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-485, BO-486, BO-487, BO-488, BO-490, BO-491, BO-492 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-484` Self-Service Experience Command Center

**Provide administrators with a centralized view of all customer-facing game wallet kiosks, balance stations, and enabled self-service channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-484 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/self-service-experience-command-center-bo-484` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): getGameEligibility answers what one card can play; the overview needs the kiosk devices and session counts, which have no read yet (contract gap CHG-WIR-004) … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of game kiosks and their session counts.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing of the self-service board: every guest-facing game-wallet kiosk and balance station, whether it is online, how much it is used, and how many sessions fail. Administrators open the kiosk profile, journey design and customer-flow previews from here. The pack is firm that this board is an experience layer and never re-creates wallet, price or entitlement rules. The one thing to get right: device health and usage tiles first, then a device list, with "Preview customer flow" one click away.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Five of the pack's eight KPI tiles drawn (CHG-SBO-005)
- Board 10's customer screens have no guest-app counterpart (CHG-SBO-020)

**Fixed on main** (the package already carries these; draw what it says): getGameEligibility is the bound read (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search self-service experience | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by client, venue, zone, device type, status — which are present is a decision the pack already made. | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Zone, Device type (Self-service kiosk, Balance station, Operator kiosk), Status. Venue from the top bar; the pack's Client filter belongs to the platform console. *(source: screens/P08-venue-back-office.yaml#BO-485)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Self-Service Devices** (metric tile)

**Online Devices** (metric tile)

**Offline Devices** (metric tile)

**Customer Sessions Today** (metric tile)

**Balance Checks** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: All eight of the pack's - Total self-service devices, Online, Offline, Customer sessions today, Balance checks, Top-ups (count and AED), Wallets viewed, Failed sessions. *(source: screens/P08-venue-back-office.yaml#BO-484 / screens/P08-venue-back-office.yaml#BO-485)*
- **Channel overview**: Columns Device, Type, Zone, Sessions today, Last activity, Status. Offline devices first. *(source: screens/P08-venue-back-office.yaml#BO-485)*
- **Board tiles**: Kiosk profile (BO-485), Identification (BO-486), Balance summary (BO-487), Top-up (BO-488), Benefits (BO-489), What can I play (BO-490), Prize discovery (BO-491), History (BO-492), Theme and journey (BO-493). *(source: screens/P08-venue-back-office.yaml#BO-484)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Configure experience**: Opens BO-493 for the selected kiosk or group. *(source: screens/P08-venue-back-office.yaml#BO-485)*
- **View device**: Opens the device in the device register (status, firmware, heartbeat). *(source: ADR-0067)*
- **Preview customer flow**: Opens a kiosk-sized preview walking the configured steps with a test card. *(source: screens/P08-venue-back-office.yaml#BO-485)*
- **View sessions**: Greyed until session records exist (VO-R13). *(source: DI-653)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-485` Self-Service Kiosk Profile & Channel Configuration: *Self-Service Kiosk Profile & Channel Configuration*
- → `BO-486` Customer Card / Wallet Identification: *Customer Card / Wallet Identification*
- → `BO-487` Customer Wallet & Balance Summary: *Customer Wallet & Balance Summary*
- → `BO-488` Self-Service Wallet Top-Up: *Self-Service Wallet Top-Up*
- → `BO-489` Bonus, Free Game & Benefit View: *Bonus, Free Game & Benefit View*
- → `BO-490` Game & Ride Eligibility / “What Can I Play?”: *Game & Ride Eligibility / “What Can I Play?”*
- → `BO-491` Redemption Balance & Prize Discovery: *Redemption Balance & Prize Discovery*
- → `BO-492` Customer Game & Wallet Transaction History: *Customer Game & Wallet Transaction History*
- → `BO-493` Self-Service UI Theme, Language & Journey Configuration: *Self-Service UI Theme, Language & Journey Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The self-service experience list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the self-service experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No self-service experience yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the self-service experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Kiosk online but its last session failed repeatedly**: Failed sessions tile links to the device; row shows "5 failed sessions in the last hour" in amber. *(source: screens/P08-venue-back-office.yaml#BO-485)*

#### Consistency with other screens

- Match `BO-036`: Kiosks are devices in the one device register (ADR-0067); status matches the device registry.
- Match `KSK-001`: The general guest kiosk (P05) is a separate journey for tickets, food and shop; if one physical kiosk runs both, its home menu must offer the game wallet as one entry.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  devices: 14
  online: 13
  offline: 1
  sessions: 2693
  balanceChecks: 1890
  topUps: 412, AED 41,850
  walletsViewed: 2210
  failed: 23
devices:
- device: KSK-01
  type: Self-service kiosk
  zone: Main Park
  sessions: 842
  lastActivity: '10:42'
  status: Online
- device: BAL-05
  type: Balance station
  zone: Summit Peaks Arcade
  sessions: 1240
  lastActivity: '10:42'
  status: Online
- device: KSK-08
  type: Self-service kiosk
  zone: Family Zone
  sessions: 611
  lastActivity: 09:58
  status: Offline
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-484` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-484`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 1: Opens Self-Service Experience Command Center → Provide administrators with a centralized view of all customer-facing game wallet kiosks, balance stations, and enabled self-service channels.
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F196 branch at step 1 (expected): when Nothing has been set up on Self-Service Experience Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F196 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-484?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-485`, `BO-486`, `BO-487`, `BO-488`, `BO-489`, `BO-490`, `BO-491`, `BO-492`, `BO-493`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-485` Self-Service Kiosk Profile & Channel Configuration

**Define the business role of each kiosk or customer-facing station.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-485 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/self-service-kiosk-profile-channel-configuration-bo-485` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the game kiosk configuration.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Defines each kiosk's role: which game-wallet functions it offers, how a guest identifies, which languages it speaks. A balance station in the arcade may only show balances; a kiosk at the entrance may top up and sell packages. The one thing to get right: the functions list is a set of switches in the guest's words, and it decides which journey steps the kiosk shows.

**Known correction pending (do not draw the wrong version)**

- **Only Save and Cancel are drawn** Why: The kiosk profile, function switches and access methods in the pack are not drawn. *(source: screens/P08-venue-back-office.yaml#BO-485; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read for the kiosk configuration** Why: setGameKioskConfiguration is a whole-record PUT with no GET, so the editor cannot open pre-filled (VO-R04). *(source: contracts/satellite/games.yaml#setGameKioskConfiguration; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No step for buying gaming products, card expiry, replacing a card or asking for help** Why: DI-883 asks for buying gaming products at the kiosk; the steps enum has none of these. *(source: DI-883 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Kiosk**: Pick a registered kiosk or balance station; its id, name, zone, device type and status come from the device register and are read-only here. Currency is the region's (VO-R10), not a field. *(source: screens/P08-venue-back-office.yaml#BO-485 / ADR-0067)*
- **Available functions**: Switches - Check balance, View bonus, View redemption credits, View free games, View entitlements, Top up wallet, View recent transactions, View card expiry; optional Replace or issue card, Customer support request. Mapped to the journey steps identify, balance, topUp, entitlements, whatCanIPlay, redemption, history; switches with no step (card expiry, replace card, support request) greyed. *(source: screens/P08-venue-back-office.yaml#BO-485 / screens/P08-venue-back-office.yaml#BO-486 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*
- **Require PIN for top-up**: Shown under Top up wallet, default off. *(source: contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*
- **Access methods**: Checkboxes RFID tap, NFC tap, QR, Card number, Digital wallet credential; only those the device's reader supports; greyed until held (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-486)*
- **Languages**: Multi-select, English and Arabic on by default; first one is the start language. *(source: contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Kiosk list**: Columns Kiosk, Type, Zone, Functions (icons), Languages, Status. *(source: screens/P08-venue-back-office.yaml#BO-485)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the kiosk's whole configuration (VO-R04), including the steps also ordered on BO-493. *(source: contracts/satellite/games.yaml#setGameKioskConfiguration)*

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The self-service kiosk profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the self-service kiosk profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No self-service kiosk profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the self-service kiosk profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Top up switched on but the kiosk has no payment device**: Warn "No payment terminal paired with KSK-08; top-up will fail". *(source: designer default)*
- **Every function switched off**: Save refused; a kiosk must offer at least Check balance. *(source: designer default)*

#### Consistency with other screens

- Match `BO-493`: Same kiosk configuration record; the order of steps is set there, the on/off here. One Save path (VO-R14).
- Match `BO-462`: Which data a function shows is the channel visibility defined there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kiosk:
  kiosk: KSK-01
  zone: Main Park
  functions: Check balance, Top up, What can I play, Redemption, History
  pinForTopUp: 'Off'
  languages: English, Arabic
```

#### Permissions

- `setGameKioskConfiguration` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-485` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-485`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 2: Works in Self-Service Kiosk Profile & Channel Configuration → Define the business role of each kiosk or customer-facing station.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-485?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-486` Customer Card / Wallet Identification

**Configure the first customer step: identifying the customer's game card or digital wallet securely.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-486 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Validate Card Status; Card recognized) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/customer-card-wallet-identification-bo-486` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures and previews the first step of the kiosk journey: the guest taps or scans their card, TICVAI identifies the wallet and checks the card, and a session opens only if it is valid. The one thing to get right: each failure (card not found, blocked, expired, replaced, wallet inactive) has its own guest message and next step, and the welcome never exposes more than a first name on a public screen.

**Known correction pending (do not draw the wrong version)**

- **Table "Every customer card wallet" with columns "4321" and an arrow** Why: The pack's example parsed as columns; this is a configuration form with a kiosk preview. *(source: screens/P08-venue-back-office.yaml#BO-486; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field for welcome text, methods or failure messages** Why: The kiosk configuration holds steps, languages, theme, timeout and PIN only. *(source: contracts/satellite/games.yaml#/components/schemas/GameKioskConfig; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should manual card-number entry need a PIN before balances show, since anyone who knows a number could read it?** → Drawn default accepted: Card number entry shows balances only after the PIN when "Require PIN" is on. *(decided by Chinmay, 2026-10-02; DEC-431 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Welcome screen text**: Title and instruction, English and Arabic, defaults "WELCOME" and "Tap your card to continue". *(source: screens/P08-venue-back-office.yaml#BO-486)*
- **Identification methods**: RFID, NFC, QR, Card number, Digital credential; only methods enabled on the kiosk profile (BO-485) appear. *(source: screens/P08-venue-back-office.yaml#BO-486)*
- **Invalid result messages**: One row each for Card not found, Card blocked, Card expired, Card replaced, Wallet inactive: guest message (English and Arabic) and next step (Try again, See guest services, Use your new card). *(source: screens/P08-venue-back-office.yaml#BO-486 / contracts/satellite/games.yaml#/components/schemas/GameCard)*

#### Outputs: what the screen shows and produces

**Shown**

**Every customer card wallet** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| 4321 | text | not in the schema: `4321` |

**The selected customer card wallet** (detail panel): The pack groups this record's detail under its own headings: “WELCOME”, “Identification Methods”, “Customer Tap”, “Invalid Results”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| 4321 | text | not in the schema: `4321` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Runtime flow**: Guest taps, Reader captures credential, TICVAI identifies wallet, Card status checked, Session opens. *(source: screens/P08-venue-back-office.yaml#BO-486)*
- **Kiosk preview**: Kiosk-size frame with tenant brand and "Powered by TICVAI" (VO-R15); states Welcome, Recognised ("Card ****4321 / Welcome, John"), and each failure. *(source: screens/P08-venue-back-office.yaml#BO-486 / screens/P08-venue-back-office.yaml#BO-487)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Try a card**: Reads a real card and shows which state the kiosk would reach; read-only. *(source: contracts/satellite/games.yaml#getGameCard)*

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer card wallet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer card wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer card wallet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer card wallet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Card read while the network is down**: The read is offline-capable; the kiosk shows the balance with "as of 10:41" and disables top-up. *(source: contracts/satellite/games.yaml#getGameCard / MATRIX 10.2.3)*
- **Unregistered card**: Session opens with "Welcome" and no name. *(source: contracts/satellite/games.yaml#/components/schemas/GameCard)*

#### Consistency with other screens

- Match `BO-460`: The blocked message here matches the reader's blocked message (BO-480).
- Match `KSK-002`: Language choice follows the guest kiosk's language select pattern.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recognised:
  card: '****4321'
  greeting: Welcome, Khalid
failures:
- result: Card expired
  message: This card expired on 04 Sep 2026
  next: See guest services
- result: Card replaced
  message: This card was replaced
  next: Use your new card
```

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-486` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-486`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 4: Works in Customer Card / Wallet Identification → Configure the first customer step: identifying the customer's game card or digital wallet securely.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-486?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-487` Customer Wallet & Balance Summary

**Present all relevant wallet balances clearly to the customer. The source specifically requires customers' stored credits to be viewable through self-service kiosks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block C · task VM-BO-487 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Information) and no metric row |
| Offline | online only |
| Opens with | `subjectId` (navigation), `walletId` (navigation) |
| Route | `/games-rides/customer-wallet-balance-summary-bo-487` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The wallet balances a guest sees at a self-service kiosk, and the exit settlement.

**Known correction pending (do not draw the wrong version)**

- **A guest self-service kiosk screen sits on Venue Management (P08).** Why: Kiosk screens belong to the kiosk app (P05); the back office needs only the operator view (BO-416). *(source: screens/P08-venue-back-office.yaml#BO-487; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer wallet balance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Card status | text | not in the schema: `Card Status` |
| Card expiry | text | not in the schema: `Card Expiry` |
| Last recharge | text | not in the schema: `Last Recharge` |

**The selected customer wallet balance** (detail panel): The pack groups this record's detail under its own headings: “AED 25”, “Redemption Credits”, “Free Games”, “Active Entitlements”.

| Shows | Format | Notes |
|---|---|---|
| Card status | text | not in the schema: `Card Status` |
| Card expiry | text | not in the schema: `Card Expiry` |
| Last recharge | text | not in the schema: `Last Recharge` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **balances**: Money balances and points separated, expiring lots flagged. *(source: contracts/satellite/wallet.yaml#getWallet / contracts/satellite/wallet.yaml#getWalletExitBalance)*

**Data it reads**: `getWalletExitBalance` (onLoad, Balance due / refundable at exit)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer wallet balance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer wallet balance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer wallet balance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer wallet balance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing is due or refundable, or the action does not match the balance (`collect` on a wallet in credit), or `waive` by a guest.; 422 The card was declined, or `waive` without a reason. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
balance:
  cash: AED 42.00
  bonus: AED 12.00
  points: 320
```

#### Permissions

- `getWallet` → `WALLET_VIEW` (read) · staff, guest
- `getWalletExitBalance` → `WALLET_VIEW` (read) · staff, guest
- `settleWalletAtExit` → `WALLET_OPERATE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.23 | Support gift card balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-487` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-487`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 6: Works in Customer Wallet & Balance Summary → Present all relevant wallet balances clearly to the customer. The source specifically requires customers' stored credits to be viewable through self-service kiosks.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-487?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-488` Self-Service Wallet Top-Up

**Allow customers to add value to their game wallet through an enabled kiosk/channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block C · task VM-BO-488 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/games-rides/self-service-wallet-top-up-bo-488` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A guest adds value to their game wallet at a kiosk.

**Known correction pending (do not draw the wrong version)**

- **A guest self-service top-up screen sits on Venue Management (P08).** Why: As BO-487. *(source: screens/P08-venue-back-office.yaml#BO-488; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only topUpWallet and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Read a guest wallet** (detail panel, from `getWallet`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | — |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Credits | list or chips (count when long) | 4.3.5 and 4.3.19. One balance and one bonus balance with one expiry could not express what the requirement asks for — cash, bonus and … |
| Kind | chip: Cash, Bonus, Redemption, Refund, Goodwill | `cash` is money the guest paid and the others are not. That distinction decides what is refundable, what expires, and what shows as a … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Source ref | text | — |
| Is refundable | yes / no (icon or chip) | True only for `cash`. A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice. |
| Bonus balance | AED 1,234.50 | Promotional value. Typically non-refundable and spent first. |
| Currency | text | — |
| Status | chip: Active, Suspended, Closed | — |
| Home cell name | text | Where the authoritative balance lives. Present when the guest is linked across cells. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last activity at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Top up**: Creates a liability, not revenue; bonus applied by the funding rules. *(source: contracts/satellite/wallet.yaml#topUpWallet)*

**Data it reads**: `getWallet` (onLoad, Read a guest wallet)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The self-service wallet top-up list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the self-service wallet top-up untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No self-service wallet top-up yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the self-service wallet top-up are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
topUp:
  amount: AED 100.00
  bonus: AED 25.00
```

#### Permissions

- `topUpWallet` → `WALLET_OPERATE` (operate) · staff, guest
- `getWallet` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

33 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.55 | Stored value entitlement management | Ticketing Catalogue | CONTRACTED | `topUpWallet` |
| 1.1.107 | Balance top-up | Ticketing Catalogue | CONTRACTED | `topUpWallet` |
| 2.1.21 | POS shall support wallet top-up, wallet payment, wallet refund, balance inquiry, and wallet transaction history linked to RFID, QR, wristband, membership card, or guest profile. | Ticketing Sales | CONTRACTED | `topUpWallet` |
| 2.7.8 | Enable real-time top-up and automatic balance updates to reduce dependency on finance confirmations and speed up transactions. | Ticketing Sales | CONTRACTED | `topUpWallet` |
| 4.3.9 | The system should support multiple methods to fund value to a digital wallet. The final list of the payment methods will be dependent on the capabilities of the payment service provider. Expected … | Bundles and Promotions | CONTRACTED | `topUpWallet` |
| 4.4.28 | Support wallet payments, wallet refunds, balance inquiries, top-ups, and mixed payment methods. | Bundles and Promotions | CONTRACTED | `topUpWallet` |
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| … 21 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-488` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-488`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 8: Works in Self-Service Wallet Top-Up → Allow customers to add value to their game wallet through an enabled kiosk/channel.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (402, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-488?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-489` Bonus, Free Game & Benefit View

**Help customers understand promotional value and benefits available in their wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-489 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/bonus-free-game-benefit-view-bo-489` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Previews and checks how the kiosk explains promotional value to a guest: bonus credit and where it can be used, free plays and where, and passes valid today. Guests misread bonus as cash; this screen must make the restriction visible ("Games and rides only, not F&B or Retail"). The one thing to get right: every benefit shows what it is, where it works, and until when.

**Known correction pending (do not draw the wrong version)**

- **The bound read has no bonus balance, bonus validity or usage restriction** Why: getGameEligibility returns games with cost kind and remaining plays; bonus balance and expiry are on the wallet and the where-usable rule is the credit type's eligibility rule. *(source: contracts/satellite/games.yaml#/components/schemas/GameEligibility / contracts/satellite/wallet.yaml#getWalletBalance / contracts/satellite/wallet.yaml#setCreditEligibilityRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Venue drawn as a filter** Why: The venue is the top-bar venue (VO-R09). *(source: screens/P08-venue-back-office.yaml#BO-489; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Card number | text field | — | — | — | — | Sends `?cardId=`. | — |
| Guest | search field | — | — | — | — | Sends `?subjectId=`. | `getGameEligibility` |
| Venue | select field | — | — | — | — | Sends `?venueId=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Card | picker: choose a card | — | — | `getGameEligibility` ?cardId |
| Subject | picker: choose a subject | — | — | `getGameEligibility` ?subjectId |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test card**: Card number or guest search to fill the preview; venue from the top bar. *(source: contracts/satellite/games.yaml#getGameEligibility)*

#### Outputs: what the screen shows and produces

**Shown**

**Bonus credit** (metric tile): The pack's Bonus Section (AED 25, valid until 30 Sep 2026); the eligibility read carries no wallet balance.

| Shows | Format | Notes |
|---|---|---|
| Bonus credit | text | not in the schema: `Bonus credit` |

**Free plays remaining** (metric tile, from `getGameEligibility`): Summed where `costKind` is freeWithEntitlement.

| Shows | Format | Notes |
|---|---|---|
| Remaining plays | 1,234 | — |

**What this card can play** (data table, from `getGameEligibility`): `costKind` maps to the pack's Included / Free / Pay to Play / Not Eligible.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Cost kind | chip: Free with entitlement, Credit, Direct pay, Not playable | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Playable | yes / no (icon or chip) | — |
| Remaining plays | 1,234 | — |
| Entitlement | the name it points at, never the id | — |
| Blocked reason | text | — |

**The selected game or benefit** (detail panel, from `getGameEligibility`): The benefit name (e.g. Birthday Free Play), its validity and where bonus value is accepted are pack labels.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Playable | yes / no (icon or chip) | — |
| Cost kind | chip: Free with entitlement, Credit, Direct pay, Not playable | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Remaining plays | 1,234 | — |
| Blocked reason | text | — |
| Tickets typically earned | 1,234 | — |
| Benefit name | text | not in the schema: `Benefit name` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Bonus section**: "Bonus credit AED 25.00, valid until 30 Sep 2026", then two lists with ticks and crosses - Can be used at Games, Rides; Cannot be used at F&B, Retail. *(source: screens/P08-venue-back-office.yaml#BO-489 / screens/P08-venue-back-office.yaml#BO-490)*
- **Free plays**: Each free-play benefit by name ("Birthday Free Play"), remaining count, and the games it covers. *(source: screens/P08-venue-back-office.yaml#BO-490)*
- **Entitlements**: Passes with validity ("Kids Unlimited Ride Pass, valid today, unlimited"). *(source: screens/P08-venue-back-office.yaml#BO-490)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview on kiosk**: Shows the section in the kiosk frame, English and Arabic (right-to-left). *(source: ADR-0011 / DI-019 / DI-296 / DI-297)*

**Data it reads**: `getGameEligibility` (onLoad, Bonus, free game and benefits)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bonus free game list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bonus free game untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bonus free game yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bonus free game are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Bonus expires today**: Amber "Expires today at 23:59" in the guest's view. *(source: designer default)*
- **No benefits**: The kiosk shows "No bonus or free plays right now" with the current top-up offer from the wallet rules, not an empty page. *(source: screens/P08-venue-back-office.yaml#BO-489)*

#### Consistency with other screens

- Match `BO-421`: Free plays shown are those managed on the free-game credit screen; names match.
- Match `BO-490`: Free plays here and "Free play" status there come from the same eligibility answer.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bonus:
  amount: AED 25.00
  validUntil: 30 Sep 2026
  usableAt: Games, Rides
  notUsableAt: F&B, Retail
freePlays:
  benefit: Birthday Free Play
  remaining: 2
  games: VR Racing, Basketball Pro, Bumper Cars
entitlement:
  pass: Kids Unlimited Ride Pass
  validity: Today
  usage: Unlimited
```

#### Permissions

- `getGameEligibility` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-489` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-489`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 10: Works in Bonus, Free Game & Benefit View → Help customers understand promotional value and benefits available in their wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-489?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-490` Game & Ride Eligibility / “What Can I Play?”

**Allow guests to see which games and rides they can currently access based on their wallet, packages, free plays and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-490 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-ride-eligibility-what-can-i-play-bo-490` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** "What can I play?": for one card, every game and ride with its normal price, what this guest would pay (included, free, a price, or not eligible and why). The contract calls it the most useful screen in the pack, because a guest holding a card cannot otherwise know what it is good for. The one thing to get right: the answer per game is one of four plain statuses, playable ones first, and "Not eligible" always says why.

**Known correction pending (do not draw the wrong version)**

- **One price per game** Why: GameEligibility.price is what this guest pays; the pack's Normal price column has no field. *(source: screens/P08-venue-back-office.yaml#BO-490 / contracts/satellite/games.yaml#/components/schemas/GameEligibility; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Included and Free cannot be told apart, and type filters have no field** Why: costKind freeWithEntitlement covers both a package play and a free play, and the answer carries no attraction type for the Rides / Video / Skill filters. *(source: contracts/satellite/games.yaml#/components/schemas/GameEligibility; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride eligibility | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by rides, video games, skill games, free for me, included in my package — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Card | picker: choose a card | — | — | `getGameEligibility` ?cardId |
| Subject | picker: choose a subject | — | — | `getGameEligibility` ?subjectId |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test card**: Card number for the preview; on the kiosk the identified card. *(source: contracts/satellite/games.yaml#getGameEligibility)*
- **Filters**: Rides, Video games, Skill games, Free for me, Included in my package. *(source: screens/P08-venue-back-office.yaml#BO-490)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Customer position**: Header strip - Wallet AED 125, Bonus AED 25, Free plays 2, Package Arcade Pass. *(source: screens/P08-venue-back-office.yaml#BO-490)*
- **Attraction results**: Columns Attraction, Normal price, Your access, Status. Status Included ("Included, 2 plays left"), Free (free play), Pay to play (AED 35.00), Pay at machine (direct pay), Not eligible with the reason ("Needs 120 cm", "Not in your pass"). Order Included, Free, Pay, Not eligible. Earned credits hint where typical ("Earn about 200 credits"). *(source: screens/P08-venue-back-office.yaml#BO-490 / contracts/satellite/games.yaml#/components/schemas/GameEligibility)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview on kiosk**: Shows the list in the kiosk frame with large touch rows. *(source: DI-296 / DI-297)*

**Data it reads**: `getGameEligibility` (onLoad, What can I play)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride eligibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride eligibility are still there. The pack's own statuses are Included — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Short of balance for a game**: Shown "Pay to play AED 35.00, top up AED 10.00 more" with a Top up shortcut when the kiosk offers top-up. *(source: contracts/satellite/games.yaml#getGameEligibility / designer default)*
- **Game out of service**: Not eligible, "Closed for maintenance". *(source: contracts/satellite/games.yaml#/components/schemas/Game)*

#### Consistency with other screens

- Match `BO-442`: The price shown is resolved by the same priority as the pricing preview; same card, same time, same price.
- Match `BO-470`: Plays remaining equal the consumption monitor's remaining.
- Match `GST-011`: If the guest app shows game eligibility, it uses the same four statuses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
position:
  wallet: AED 125.00
  bonus: AED 25.00
  freePlays: 2
  package: Arcade Pass
results:
- attraction: VR Racing
  normal: AED 20.00
  access: Included, 2 plays left
  status: Play
- attraction: Basketball Pro
  normal: AED 20.00
  access: Free play
  status: Play
- attraction: Falcon Coaster
  normal: AED 35.00
  access: AED 35.00
  status: Play
- attraction: Premium Crane 01
  normal: AED 15.00
  access: Pay at machine
  status: Play
- attraction: Wave Rider
  normal: AED 30.00
  access: Needs 120 cm
  status: Not eligible
```

#### Permissions

- `getGameEligibility` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-490` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-490`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 12: Works in Game & Ride Eligibility / “What Can I Play?” → Allow guests to see which games and rides they can currently access based on their wallet, packages, free plays and entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-490?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-491` Redemption Balance & Prize Discovery

**Allow customers to check redemption credits and browse prizes they can afford before visiting the redemption counter.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-491 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/redemption-balance-prize-discovery-bo-491` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Lets a guest see their redemption credits and which prizes they can afford before walking to the counter, and how many more credits a locked prize needs. View only: redemption itself stays at the counter. The one thing to get right: "Affordable now" and "Need more credits" are two groups, and out-of-stock prizes stay visible with their stock state so a child is not promised something that is gone.

**Known correction pending (do not draw the wrong version)**

- **listPrizes is staff-only** Why: The kiosk is a guest surface; the prize list must be guest-callable like getGameEligibility, or the kiosk cannot show it. *(source: contracts/satellite/games.yaml#listPrizes / contracts/satellite/games.yaml#getGameEligibility; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No low-stock threshold on the prize** Why: The Low stock indicator needs a reorder level; Prize carries only onHand and isAvailable. *(source: screens/P08-venue-back-office.yaml#BO-491 / contracts/satellite/games.yaml#/components/schemas/Prize; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search redemption balance prize | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by available now, prize category, credit range, venue — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Max points | number field | — | — | `listPrizes` ?maxPoints |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test card**: Card for the preview; on the kiosk the identified card. *(source: contracts/satellite/games.yaml#getGameCard)*
- **Filters**: Available now, Prize category, Credit range. Venue from the top bar. *(source: screens/P08-venue-back-office.yaml#BO-491)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Balance**: "2,450 credits" large; credits, never AED. *(source: screens/P08-venue-back-office.yaml#BO-491)*
- **Affordable now**: Prize cards with image, name, cost, stock indicator (Available, Low stock, Out of stock), cheapest last so the best affordable prize comes first. *(source: screens/P08-venue-back-office.yaml#BO-491 / contracts/satellite/games.yaml#listPrizes)*
- **Need more credits**: "Headphones, 3,500 credits. You need 1,050 more." A progress bar of balance against cost. *(source: screens/P08-venue-back-office.yaml#BO-491)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview on kiosk**: Kiosk-size prize wall laid out by prize tier. *(source: contracts/satellite/games.yaml#/components/schemas/Prize)*

**Data it reads**: `listPrizes` (onLoad, Prize discovery)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption balance prize list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption balance prize untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption balance prize yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption balance prize are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Prize out of stock**: Shown greyed "Out of stock" in its group, never hidden. *(source: contracts/satellite/games.yaml#listPrizes)*
- **Guest asks to redeem at the kiosk**: No redeem button; "Take your card to the prize counter". *(source: screens/P08-venue-back-office.yaml#BO-491)*

#### Consistency with other screens

- Match `BO-449`: Same prizes, costs and stock as the counter.
- Match `BO-450`: Images and tiers come from the catalogue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
balance: 2450
affordable:
- prize: Football
  cost: 1000
  stock: Low stock
- prize: Teddy Bear
  cost: 800
  stock: Available
- prize: Water Bottle
  cost: 300
  stock: Available
locked:
  prize: Headphones
  cost: 3500
  needMore: 1050
```

#### Permissions

- `listPrizes` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-491` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-491`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 14: Works in Redemption Balance & Prize Discovery → Allow customers to check redemption credits and browse prizes they can afford before visiting the redemption counter.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-491?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-492` Customer Game & Wallet Transaction History

**Allow the customer to review recent activity associated with the card/wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-492 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/customer-game-wallet-transaction-history-bo-492` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Lets a guest review recent activity on their card at the kiosk: plays, top-ups, bonus, redemption credits earned and spent. The one thing to get right: money and credits are different units with different signs ("-AED 20.00" for a play, "+200 credits" earned, "Free play" with no amount), and the list is short and recent, because it is shown on a public screen.

**Known correction pending (do not draw the wrong version)**

- **The bound read is staff-only, plays-only and cannot filter by card** Why: listGameplayTransactions takes from, readerId and outcome; top-ups and bonus are wallet transactions and redemptions are prize redemptions, none of which it returns. *(source: contracts/satellite/games.yaml#listGameplayTransactions / contracts/satellite/wallet.yaml#listWalletTransactions; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search customer game wallet | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by games/rides, top-ups, bonus, redemption, free play — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test card**: Card for the preview; on the kiosk the identified card. *(source: screens/P08-venue-back-office.yaml#BO-492)*
- **Filters**: Games and rides, Top-ups, Bonus, Redemption, Free play. *(source: screens/P08-venue-back-office.yaml#BO-493)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Recent transactions**: Columns Time, Activity, Amount. Plays "-AED 20.00", top-ups "+AED 100.00", bonus "+AED 25.00 bonus", free plays "Free play", credits "+200 credits". Last 30 days at most, newest first. *(source: screens/P08-venue-back-office.yaml#BO-493)*
- **Transaction detail**: Attraction, reader, type, price, funding source, credits earned, remaining balance, date and time. *(source: screens/P08-venue-back-office.yaml#BO-493)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview on kiosk**: Kiosk-size history with large rows and a Done button. *(source: DI-296 / DI-297)*

**Data it reads**: `listGameplayTransactions` (onLoad, Transaction history)

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer game wallet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer game wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer game wallet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer game wallet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A play reversed after a machine fault**: Shown as "+AED 20.00 refunded, Basketball Pro" next to the play. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*

#### Consistency with other screens

- Match `BO-465`: Plays carry the same attraction names and amounts as the staff feed.
- Match `GST-011`: The guest app's wallet history uses the same activity words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
history:
- time: '10:42'
  activity: VR Racing
  amount: -AED 20.00
- time: '10:30'
  activity: Bonus added
  amount: +AED 25.00 bonus
- time: '10:30'
  activity: Top-up
  amount: +AED 100.00
- time: '10:15'
  activity: Basketball Pro
  amount: Free play
- time: 09:50
  activity: Prize credits earned
  amount: +200 credits
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-492` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-492`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 16: Works in Customer Game & Wallet Transaction History → Allow the customer to review recent activity associated with the card/wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-492?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-493` Self-Service UI Theme, Language & Journey Configuration

**Allow TICVAI administrators to configure the customer-facing kiosk experience without changing business logic.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-493 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Session Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/self-service-ui-theme-language-journey-configuration-bo-493` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Brands and shapes the kiosk journey centrally without touching business rules: logo, welcome, hero image, languages, the order of the home menu, session timeouts, accessibility, with a draft, preview and publish cycle applied to a kiosk, a venue, a kiosk group or all of the tenant's kiosks. The one thing to get right: the live kiosk preview beside the controls, in English and Arabic, and a publish step that names how many kiosks change.

**Known correction pending (do not draw the wrong version)**

- **Session Timeout, Auto Logout and Confirmation Timeout are select fields; Privacy Reset is a text field** Why: Timeouts are numbers in seconds; auto logout and privacy reset are switches. *(source: screens/P08-venue-back-office.yaml#BO-493; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The kiosk configuration holds only steps, languages, theme code, idle timeout and PIN** Why: Welcome text, hero image, confirmation timeout, privacy reset, accessibility, draft and publish, and applying to a group or the venue have no field; the record is per kiosk. *(source: screens/P08-venue-back-office.yaml#BO-493 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Session Timeout | select field | — | — | — | — | — | — |
| Auto Logout | select field | — | — | — | — | — | — |
| Confirmation Timeout | select field | — | — | — | — | — | — |
| Privacy Reset After Session | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Branding**: Client logo, background, welcome message (English and Arabic), hero image from the asset library. Tenant brand with "Powered by TICVAI" (VO-R15; on unless the venue switched it off on CMS-104). *(source: screens/P08-venue-back-office.yaml#BO-493)*
- **Languages**: English and Arabic by default; other configured languages addable. *(source: screens/P08-venue-back-office.yaml#BO-493 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*
- **Home menu order**: Drag-to-order list - Check balance, Top up, My benefits, What can I play, Redemption, Transactions. Only functions enabled on the kiosk profile appear. *(source: screens/P08-venue-back-office.yaml#BO-493 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*
- **Session**: Session timeout in seconds (number, default 30), Confirmation timeout in seconds, Auto logout and Privacy reset after session as switches (default on). Not select or text fields. *(source: screens/P08-venue-back-office.yaml#BO-493 / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*
- **Accessibility**: Large text, High contrast, Audio guidance (only where the device has audio). *(source: screens/P08-venue-back-office.yaml#BO-493)*
- **Apply to**: Selected kiosk, Venue, Kiosk group, All tenant kiosks; the count of kiosks affected shown. *(source: screens/P08-venue-back-office.yaml#BO-493)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Kiosk preview**: "WELCOME TO THE PARK / Tap your card" at kiosk size, switchable English and Arabic (right-to-left) and normal or high contrast. *(source: screens/P08-venue-back-office.yaml#BO-493)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft, Preview, Publish**: Publish confirms "Applies to 6 kiosks at Summit Peaks; guests see it on their next session". Sessions in progress are not interrupted. *(source: screens/P08-venue-back-office.yaml#BO-493)*

**Where the user goes next**

- → `BO-484` Self-Service Experience Command Center: *Back to Self-Service Experience Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The self-service theme language configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the self-service theme language untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No self-service theme language configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Arabic welcome missing when Arabic is enabled**: Publish blocked with "Add the Arabic welcome message". *(source: ADR-0011 / DI-019)*
- **Timeout shorter than a top-up payment takes**: Warn that sessions under 30 seconds may end during card payment. *(source: contracts/satellite/games.yaml#/components/schemas/GameKioskConfig)*

#### Consistency with other screens

- Match `BO-485`: Same kiosk configuration record; functions on/off there, order here (VO-R14).
- Match `CMS-001`: Brand assets and themes are the tenant's white-label theme; reference it by theme rather than uploading logos twice.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
theme:
  logo: Yas Leisure Group
  welcome: Welcome to Summit Peaks
  welcomeAr: مرحبا بكم في سوميت بيكس
  menu: Check balance, Top up, What can I play, My benefits, Redemption, Transactions
  timeout: 30 s
  applyTo: 'Venue: Summit Peaks (6 kiosks)'
```

#### Permissions

- `setGameKioskConfiguration` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-493` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS67 Game and Ride Board 10.dc.html#bo-493`
- Workshop pack: Game_and_Ride_Module.pdf board 10
- Flow F196 *Game and Ride board 10: Self-Service Experience Command Center*, step 18: Works in Self-Service UI Theme, Language & Journey Configuration → Allow TICVAI administrators to configure the customer-facing kiosk experience without changing business logic.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-493?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-484`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getGameCard": {"method":"GET","path":"/game-cards/{cardCode}","contract":"games","summary":"Read a card's balances","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameCard"},
"getGameEligibility": {"method":"GET","path":"/game-eligibility","contract":"games","summary":"What this guest can play right now, and what it would cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"cardId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"GameEligibility"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWalletExitBalance": {"method":"GET","path":"/wallets/{walletId}/exit-balance","contract":"wallet","summary":"What the holder owes or is owed on leaving","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WalletExitBalance"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listPrizes": {"method":"GET","path":"/prizes","contract":"games","summary":"The prize catalogue","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"maxPoints","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setGameKioskConfiguration": {"method":"PUT","path":"/game-kiosk-config","contract":"games","summary":"The self-service journey, its theme and its languages","permission":"TENANT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameKioskConfig","responds":"GameKioskConfig"},
"settleWalletAtExit": {"method":"POST","path":"/wallets/{walletId}/exit-settlement","contract":"wallet","summary":"Settle a short balance, or refund a credit, when the holder leaves","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletExitSettlement"},
"topUpWallet": {"method":"POST","path":"/wallets/{subjectId}/top-ups","contract":"wallet","summary":"Add value to a wallet","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"GameCard": {"x-ticvai-persistence":"games.card","type":"object","required":["cardCode","venueId","credits","bonusCredits","points","status","issuedAt"],"properties":{"cardCode":{"type":"string","description":"**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"credits":{"type":"integer","description":"Bought with money. Buys plays."},"bonusCredits":{"type":"integer","description":"From a promotion. Typically non-refundable and spent before paid credits.\n"},"points":{"type":"integer","description":"Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"},"status":{"type":"string","enum":["active","blocked","expired","transferred"]},"blockedReason":{"type":"string","nullable":true},"transferredToCardCode":{"type":"string","nullable":true},"lastPlayedAt":{"type":"string","format":"date-time","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**The card's own id** (4 October 2026, CHG-FXC-006): the `{cardId}` of `setGameCardLifecycle`, which had no column to match, and the `id` of the Wallet view `wallet.loadGameCredits` and `wallet.adjustGameCard` return for a card with no wallet."},"walletId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Where the card's credits are held** (4 October 2026, CHG-FXC-006). Set when the card is registered to a guest who has a wallet: credits loaded to it are wallet credit lots. Null for an anonymous card, whose credits are held on the card row itself (`credits`, `bonusCredits`)."}}},
"GameEligibility": {"type":"object","description":"Board 10.7 — *\"What Can I Play?\"*, and every fact in it lives somewhere different.","properties":{"gameId":{"type":"string","format":"uuid"},"name":{"type":"string"},"playable":{"type":"boolean"},"costKind":{"type":"string","enum":["freeWithEntitlement","credit","directPay","notPlayable"]},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingPlays":{"type":"integer","nullable":true},"blockedReason":{"type":"string","nullable":true},"ticketsTypicallyEarned":{"type":"integer","nullable":true}}},
"GameKioskConfig": {"type":"object","x-ticvai-persistence":"games.kiosk_config","description":"Boards 10.2 and 10.10. **Used by a child holding a wristband.**","properties":{"kioskDeviceId":{"type":"string","format":"uuid"},"steps":{"type":"array","items":{"type":"string","enum":["identify","balance","topUp","entitlements","whatCanIPlay","redemption","history"]}},"languages":{"type":"array","items":{"type":"string"}},"themeCode":{"type":"string","nullable":true},"idleTimeoutSeconds":{"type":"integer","default":30},"requiresPinForTopUp":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Prize": {"x-ticvai-persistence":"games.prize","type":"object","required":["id","name","venueId","pointCost","onHand"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid"},"merchandiseId":{"type":"string","format":"uuid","nullable":true,"description":"Links to retail. Redemption depletes stock through the inventory ledger — a prize wall running out is a stock problem and should look like one.\n"},"pointCost":{"type":"integer","minimum":1},"onHand":{"type":"integer"},"isAvailable":{"type":"boolean"},"tier":{"type":"string","nullable":true,"description":"Small, medium, large, jackpot. Drives prize-wall layout."},"imageAssetRef":{"type":"string","nullable":true},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"The prize's own barcode, read by `lookupPrize` before the linked retail item's barcode or SKU. Unique within the venue (VM close-out, 29 September)."},"isActive":{"type":"boolean"}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletExitBalance": {"type":"object","x-ticvai-persistence":"none — computed from wallet.wallet, wallet.credit_lot and held offline transactions","required":["walletId","balance","amountDue","refundable"],"properties":{"walletId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"pendingOfflineAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountDue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nonRefundableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"waiveAllowedUpTo":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"asAt":{"type":"string","format":"date-time"}}},
"WalletExitSettlement": {"type":"object","x-ticvai-persistence":"wallet.exit_settlement","description":"4.3.4. One settlement of a wallet at exit.","required":["id","walletId","action","amount","settledAt"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"action":{"type":"string","enum":["collect","refund","waive"]},"method":{"type":"string","nullable":true,"enum":["card","cash","storedCard","originalPayment"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceBefore":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paymentId":{"type":"string","format":"uuid","nullable":true},"refundId":{"type":"string","format":"uuid","nullable":true},"walletTransactionId":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"settledByPrincipalId":{"type":"string","format":"uuid","nullable":true},"settledAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}}
}
```
