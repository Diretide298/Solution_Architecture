# WS02 — Access Control board 2

**10 screens · 17 operations · 23 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, APPROVAL_REQUEST, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-154` | Access Rule Command Center | C | 0 | 2 | 6 | 7 | 2 | 0 | — | notStarted (generated) |
| `BO-155` | Visual Access Rule Builder | A | 0 | 20 | 6 | 6 | 1 | 0 | — | notStarted (generated) |
| `BO-156` | Entry, Exit & Re-entry Rules | C | 47 | 0 | 6 | 9 | 2 | 0 | — | notStarted (generated) |
| `BO-157` | Anti-Passback & Journey Sequence | C | 15 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-158` | Access Validity & Time Rules | C | 54 | 0 | 5 | 9 | 4 | 0 | — | notStarted (generated) |
| `BO-159` | Entitlement Consumption Engine | C | 10 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-160` | Multi-Park & Crossover Rules | C | 47 | 0 | 6 | 9 | 1 | 0 | — | notStarted (generated) |
| `BO-161` | Guest, Companion & Eligibility Rules | A | 17 | 15 | 5 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-162` | Group Admission & Quantity Validation | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-163` | Rule Simulation, Conflict Check & Publication | C | 11 | 0 | 6 | 5 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-155, BO-156, BO-160, BO-162 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-154` Access Rule Command Center

**Central configuration dashboard for all access and entitlement rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-154 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Show) and a per-row directory (§Each rule displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-rule-command-center-bo-154` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The hub of board 2, the admission decision engine: twelve KPI tiles about the rules themselves (active, draft, scheduled, pending approval, venues and products covered, conflicts, biometric, override-allowing, offline-compatible, recently modified, upcoming changes), a rule directory a manager can filter by venue, park, attraction, product, credential, rule type, status and date, and AI findings (duplicates, conflicts, unused rules, risky overrides, missing coverage). The one thing to get right: find, understand, create, clone and govern every admission rule from one place, with conflicts surfaced first.

**Known correction pending (do not draw the wrong version)**

- **Directory titled "Every access rule" with one column holding the five pack headings as a single string** Why: Generated placeholder; the read returns rule, appliesTo, location, validity, ruleType and status as separate columns. *(source: contracts/spine/access.yaml#/components/schemas/AccessRuleCommandCenterView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rule statuses Draft, Scheduled and Pending approval cannot exist for admission profiles** Why: AdmissionRules has no status or version field, so the tiles for drafts, scheduled and pending rules have nothing to count; publishRuleConflictCheck also expects a ruleVersionId. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / contracts/spine/access.yaml#publishRuleConflictCheck; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The summary carries no AI findings** Why: The pack's AI assistant has nowhere to come from; add an advisory array as BO-174 and BO-194 have. *(source: screens/P08-venue-back-office.yaml#BO-154 / contracts/spine/access.yaml#/components/schemas/AccessRuleCommandCenterViewSummary; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **ruleType is a free string** Why: It decides which editor opens; it needs the closed list of rule kinds. *(source: contracts/spine/access.yaml#/components/schemas/AccessRuleCommandCenterView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAccessRule` ?venue |
| Park | text field | — | — | `listAccessRule` ?park |
| Attraction | text field | — | — | `listAccessRule` ?attraction |
| Product | text field | — | — | `listAccessRule` ?product |
| Credential | text field | — | — | `listAccessRule` ?credential |
| Rule type | text field | — | — | `listAccessRule` ?ruleType |
| Status | text field | — | — | `listAccessRule` ?status |
| Date | text field | — | — | `listAccessRule` ?date |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Access Rules** (metric tile)

**Draft Rules** (metric tile)

**Scheduled Rules** (metric tile)

**Rules Pending Approval** (metric tile)

**Venues Covered** (metric tile)

**Products/Tickets Covered** (metric tile)

**Rules with Conflicts** (metric tile)

**Rules Using Biometrics** (metric tile)

**Rules Allowing Override** (metric tile)

**Offline-Compatible Rules** (metric tile)

**Recently Modified Rules** (metric tile)

**Upcoming Rule Changes** (metric tile)

**Every access rule** (data table, from `listAccessRule`)

| Shows | Format | Notes |
|---|---|---|
| Rule applies to location validity status | text | not in the schema: `Rule Applies To Location Validity Status` |

**The selected access rule** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Rule applies to location validity status | text | not in the schema: `Rule Applies To Location Validity Status` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The twelve pack tiles in the pack's order as metric tiles (VO-R02); Rules with Conflicts red when non-zero and opening the directory filtered to them; Upcoming Rule Changes opens the directory filtered to scheduled. *(source: screens/P08-venue-back-office.yaml#BO-154 / contracts/spine/access.yaml#/components/schemas/AccessRuleCommandCenterViewSummary)*
- **Rule directory**: Titled "Access rules" (VO-R12). Columns Rule, Applies to, Location, Validity, Type, Status - the pack's sample rows show the expected plain-language cells ("Day Tickets", "Adventure Park", "Daily", "3 uses"). Rule type tells the manager which editor opens - Admission profile (BO-032 sections), Visual rule (BO-155), Journey / anti-passback (BO-157), Consumption (BO-159), Group admission (BO-162). Status chips Draft, Pending approval, Scheduled, Active, Inactive. Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-154 / contracts/spine/access.yaml#listAccessRule)*
- **Filters**: The eight pack filters as a filter bar (Venue, Park, Attraction, Product, Credential, Rule type, Status, Date); Venue defaults to the switcher's venue (VO-R09). *(source: contracts/spine/access.yaml#listAccessRule)*
- **AI assistant**: Findings as sentences naming the rules involved, each with Open both / Open rule; categories duplicate, conflicting, unused, risky override, unusual restriction, missing coverage; advisory (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-154)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New rule**: Asks which kind (admission profile, visual rule, journey sequence, consumption, group) and opens that editor in create mode. *(source: screens/P08-venue-back-office.yaml#BO-155 / contracts/spine/access.yaml#createAdmissionRules)*
- **Open rule**: Opens the owning editor on that rule; returns here (VO-R13). *(source: F112 step 3 / DI-653)*
- **Clone rule**: Opens the editor pre-filled with "Copy of ..." and no id; drawn but marked "Not yet available" until an operation exists. *(source: contracts/spine/access.yaml#listAccessRule)*

**Data it reads**: `listAccessRule` (onLoad, Access Rule Command Center); `listAdmissionRules` (onLoad, Every admission rule with its scope)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-155` Visual Access Rule Builder: *Works in Visual Access Rule Builder*; calls `listAccessRule`
- → `BO-156` Entry, Exit & Re-entry Rules: *Works in Entry, Exit & Re-entry Rules*; calls `listAccessRule`
- → `BO-158` Access Validity & Time Rules: *Works in Access Validity & Time Rules*; calls `listAccessRule`
- → `BO-159` Entitlement Consumption Engine: *Works in Entitlement Consumption Engine*; calls `listAccessRule`
- → `BO-160` Multi-Park & Crossover Rules: *Works in Multi-Park & Crossover Rules*; calls `listAccessRule`
- → `BO-162` Group Admission & Quantity Validation: *Works in Group Admission & Quantity Validation*; calls `listAccessRule`
- → `BO-163` Rule Simulation, Conflict Check & Publication: *Works in Rule Simulation, Conflict Check & Publication*; calls `listAccessRule`
- → `BO-157` Anti-Passback & Journey Sequence: *Works in Anti-Passback & Journey Sequence*; carries `ruleId`; calls `listAccessRule`
- → `BO-161` Guest, Companion & Eligibility Rules: *Works in Guest, Companion & Eligibility Rules*; carries `productId`; calls `listAccessRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access rule list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No rules yet for the venue**: Empty state "No admission rules - gates admit nothing until a profile is published" with New rule. *(source: designer default)*
- **Viewer without configuration rights**: Directory readable; New, Clone and edit actions disabled with "Needs access configuration rights" (VO-R08). *(source: contracts/spine/access.yaml#createAdmissionRules)*

#### Consistency with other screens

- Match `BO-032`: Admission profile rows open the one profile editor; BO-156, BO-158, BO-159 and BO-160 are anchors into its sections (VO-R14).
- Match `BO-163`: Status values and versions here are the ones the simulation and publication screen moves rules through.
- Match `BO-234`: The dynamic access policy hub uses the same status words and conflict badges.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  active: 38
  draft: 6
  scheduled: 3
  pendingApproval: 2
  venuesCovered: 2
  productsCovered: 64
  conflicts: 2
  biometric: 4
  override: 9
  offlineCompatible: 31
  recentlyModified: 5
  upcoming: 3
rules:
- rule: Standard Park Entry
  appliesTo: Day Tickets
  location: Aqua Park
  validity: Daily
  type: Admission profile
  status: Active
- rule: Annual Pass Entry
  appliesTo: Annual Pass
  location: All parks
  validity: Annual
  type: Admission profile
  status: Active
- rule: Fast Pass Silver
  appliesTo: Silver Wristband
  location: Selected rides
  validity: 3 uses
  type: Consumption
  status: Active
- rule: Ladies Night
  appliesTo: Event products
  location: Aqua Park
  validity: Wednesday PM
  type: Visual rule
  status: Scheduled
- rule: Child Companion
  appliesTo: Junior tickets
  location: Selected attractions
  validity: Always
  type: Eligibility
  status: Active
aiFinding: Fast Pass Silver and Fast Pass Gold both apply at Falcon Coaster with different limits; Gold allows unlimited,
  Silver 3 uses.
```

#### Permissions

- `listAccessRule` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-154` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-154`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 1: Opens Access Rule Command Center → Central configuration dashboard for all access and entitlement rules.
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F112 branch at step 1 (expected): when Nothing has been set up on Access Rule Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F112 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-154?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-155`, `BO-156`, `BO-158`, `BO-159`, `BO-160`, `BO-162`, `BO-163`, `BO-157`, `BO-161`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-155` Visual Access Rule Builder

**Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-155 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/visual-access-rule-builder-bo-155` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The no-code access rule builder: WHEN a guest presents (product, membership, pass, credential type) AT (venue, park, zone, attraction, gate) IF (conditions) THEN (Allow, Deny, Refer to operator, Override eligible) AND (actions such as consume one entry, add to attendance, record scan). It must make complex admission rules readable as sentences, with AND/OR/NOT nesting, and an AI prompt that drafts a rule for review. The one thing to get right: conditions are picked from a closed catalogue, never typed as free text.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- setVisualAccessRule carries conditions and logic as free strings (CHG-SBO-005)
- ruleId is required in the write (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): No read is bound, so the builder cannot open an existing rule; content region is empty (pack "gives nothing that can be drawn") (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the AI rule-drafting prompt in Block A scope, or drawn and disabled until the AI engine ships?** → Drawn default accepted: Draw the prompt box enabled, with the drafted rule always requiring review. *(decided by Chinmay, 2026-10-02; DEC-126 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **appliesTo (WHEN)**: Multi-select of products and credential types (Ticket, Membership, Pass, Accreditation credential) with search. *(source: screens/P08-venue-back-office.yaml#BO-155 / contracts/spine/access.yaml#setVisualAccessRule)*
- **locationIds (AT)**: Topology picker (venue > park > zone > attraction > gate), multi-select. *(source: screens/P08-venue-back-office.yaml#BO-155)*
- **conditions and logic (IF)**: Condition rows built as attribute, operator, value from the Access Attribute Catalog (BO-235) - e.g. Visit date = Today; Ticket status = Valid; Remaining entries > 0 - grouped into AND / OR / NOT blocks that can nest. Never a free-text expression. *(source: screens/P08-venue-back-office.yaml#BO-155 / screens/P08-venue-back-office.yaml#BO-156 / ADR-0068)*
- **decision (THEN)**: Four large choices with colour - Allow (green), Deny (red), Refer to operator (amber), Override eligible (amber outline). *(source: contracts/spine/access.yaml#setVisualAccessRule)*
- **consequences (AND)**: Ordered chips from a closed list (Consume 1 entry, Update attendance +1, Record scan, Trigger alert). *(source: screens/P08-venue-back-office.yaml#BO-155)*
- **AI drafting**: A prompt box "Describe the rule" (e.g. "Allow annual-pass holders into Adventure Park twice per day and permit one re-entry if they previously exited"); AI fills the builder for review; nothing saves until a person presses Save (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-156)*

#### Outputs: what the screen shows and produces

**Shown**

**Rules** (data table, from `listAdmissionRules`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | Server-assigned. Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names. |
| Code | text | — |
| Per product rules | list or chips (count when long) | BL-059. Transaction rules were per profile and a ticket type could not state its own. |
| Product | the name it points at, never the id | — |
| Entries per day | 1,234 | — |
| Minimum gap minutes | 1,234 | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in … |
| Allowed access points | list or chips (count when long) | — |
| Biometric policy | chip: Disabled, Offered, Preferred | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. |
| Max passes per biometric identity | 1,234 | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. |
| Name | text | — |
| Open minutes before | 1,234 | How long before a performance validation opens. |
| Close minutes after | 1,234 | — |
| Max duration minutes | 1,234 | — |
| Requires exit before reentry | yes / no (icon or chip) | — |
| Max reentries | 1,234 | — |
| Entry limit | grouped details | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & … |
| Mode | chip: Unlimited, Once, N times, N per day, N per period | — |
| Count | 1,234 | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) |
| Period days | 1,234 | The period for nPerPeriod |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule as a sentence**: A plain-language rendering above the builder that updates as blocks change ("When an Adventure Day Pass is presented at Main Entrance, if visit date is today and entries remain, allow entry and consume 1 entry"). *(source: screens/P08-venue-back-office.yaml#BO-155)*
- **Test panel**: Virtual scan (product, gate, date-time, prior scans) showing the decision and which condition decided it, before publishing. *(source: DI-629 / DI-722)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Writes the rule on its admission profile; takes effect at gates with the next offline package; confirmation names the gates affected. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / contracts/spine/access.yaml#updateAdmissionRules)*

**Data it reads**: `listAdmissionRules` (onLoad, The admission profiles whose ruleConditions the builder …)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `setVisualAccessRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual access rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual access rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual access rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual access rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two rules give opposite decisions for the same scan**: The test panel shows both and which wins (deny overrides allow); warn before saving. *(source: ADR-0002 / designer default)*
- **AI draft uses an attribute not in the catalogue**: Shown red with "Not available - add it in the attribute catalogue first". *(source: TRACKER Actions row 324 / DI-924)*

#### Consistency with other screens

- Match `BO-032`: The rule is part of an admission profile (ruleConditions); open the builder as a section of the profile editor.
- Match `BO-235`: Condition attributes and operators come only from the attribute catalogue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Adventure Day Pass - main entry
  when: Adventure Day Pass
  at: Adventure Park / Main Entrance
  if: Visit date = Today AND Ticket status = Valid AND Remaining entries > 0
  then: Allow
  and: Consume 1 entry, Update attendance +1, Record scan
```

#### Permissions

- `setVisualAccessRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-155` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-155`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 2: Works in Visual Access Rule Builder → Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-155?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-156` Entry, Exit & Re-entry Rules

**Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit before re-entry, and required entry before exit.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-156 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/entry-exit-re-entry-rules-bo-156` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): listEntryExitRule returns its own rule rows (entryMode, exitMode, designatedGateRequired) while the write is the admission profile; two shapes for one block. The …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Entry, exit and re-entry rules are a section of the admission profile editor (BO-032, per VO-R14); this board entry is an anchor that opens that editor on the "Entries and re-entry" section of the profile passed in. The pack's lifecycle - Entry (Unlimited, Once, N times, N per day, N per period), Exit (scan required, optional, unlimited, N exits), Re-entry (allowed, maximum, same day, designated gate, exit first, window) - is edited there. The one thing to get right: the pack's "Standard Day Ticket - Entry 1, Exit required, Re-entry 1 through the designated gate only" must be quick to set and read back as that sentence.

**Known correction pending (do not draw the wrong version)**

- **Content is an unbound empty table and the save is labelled "Save admission rules" with no permission** Why: Section of BO-032 (Save profile, ACCESS_POINT_CONFIGURE). *(source: screens/P08-venue-back-office.yaml#BO-156; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **updateAdmissionRules purpose names only maxReentries and requiresExitBeforeReentry** Why: Stale; the block now includes entryLimit, exitScan, maxExits, reEntryWindowMinutes, sameDayOnly, designatedAccessPointIds and reEntryVerification. *(source: contracts/spine/access.yaml#updateAdmissionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): A separate read listEntryExitRule returns its own rule rows (entryMode, exitMode, designatedGateRequired, reEntryWindow) while the write is … (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Section anchor**: Opens BO-032 with profileId, scrolled to Entries and re-entry; with no profile passed it opens the profile list first. Field rules are as BO-032 states them; this entry adds only what follows. *(source: screens/P08-venue-back-office.yaml#BO-156)*
- **Re-entry allowed**: The pack's "Allowed / Not allowed" is a switch at the top of the re-entry block; Not allowed hides the other re-entry fields and saves maximum re-entries as 0. Maximum re-entries empty means unlimited and must say "Unlimited". *(source: screens/P08-venue-back-office.yaml#BO-156 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **maxExits**: Shown only when exit scan is Required or Optional; empty = "Unlimited exits", a number = "N exits". *(source: screens/P08-venue-back-office.yaml#BO-156 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Exit not reconciled**: Under "Exit scan required" state the consequence the client asked for - a guest who left through a door without an exit scan is blocked at the next re-entry until reconciled. *(source: DI-461)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle strip**: Entry > Exit > Re-entry as three linked blocks with the current values ("1 entry", "Exit scan required", "1 re-entry, Main Plaza gates only, within 120 min"), above the fields. *(source: screens/P08-venue-back-office.yaml#BO-156 / screens/P08-venue-back-office.yaml#BO-157)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: As BO-032 (whole profile, VO-R04); the confirmation names products and access points affected. *(source: contracts/spine/access.yaml#updateAdmissionRules)*

**Data it reads**: `listAdmissionRules` (onLoad, The admission profiles whose entry, exit and re-entry rules …)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAdmissionRules`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entry exit re-entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entry exit re-entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entry exit re-entry yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **Entry limit Once with re-entry wanted**: Re-entry fields hidden (as BO-032); a re-entry product uses N times or N per day with re-entries. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Exit scan Required while the exit gates run in free rotation**: Warning that exits will never be recorded there and guests could not re-enter. *(source: DI-626 / DI-461)*

#### Consistency with other screens

- Match `BO-032`: Same labels and controls; this is that editor's section, not a second form.
- Match `SCN-003`: Deny labels "Re-entry limit reached" and "Exit scan required before re-entry" are the consequences of these fields (VO-R06).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Standard day ticket
  entry: Once
  exit: Exit scan required
  reentry: 1, same day, within 120 min, Main Plaza Gate 1-3 only
  verification: Credential + UV stamp
```

#### Permissions

- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*
- If a guest exits without a matching checkout scan (e.g. a manually opened door), the system flags it and blocks the next re-entry scan until check-in/check-out is reconciled. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-461)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-156` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-156`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 4: Works in Entry, Exit & Re-entry Rules → Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit …

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-156?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel, Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-157` Anti-Passback & Journey Sequence

**Prevent credential sharing and impossible access sequences.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-157 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure required sequences such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/access-venue/anti-passback-journey-sequence-bo-157` |

**What the spec says about it.** **"Applies to": venue-wide by default, or chosen products or admission profiles (decided 2 October 2026 by Chinmay, DEC-231; CHG-CSP-029, `appliesTo`).**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Prevents credential sharing and impossible journeys: an anti-passback minimum interval between scans at a chosen level (credential, guest, gate, attraction, park, venue), required scan sequences (Entry > Exit > Re-entry; Park A > Crossover > Park B; Main entry > Attraction entry) and what a violation leads to (deny, warn, refer to operator, require supervisor, allow override, trigger security alert). The one thing to get right: build sequences as ordered steps from a closed list, and show the pack's example outcome - the same annual pass at Gate A and again 45 seconds later at Gate B gives a red "Anti-passback violation".

**Known correction pending (do not draw the wrong version)**

- **Three textFields labelled with the pack's sample sequences ("ENTRY -> EXIT -> RE-ENTRY" and two more)** Why: Sample values used as labels; the sequence is one ordered list built from steps. *(source: screens/P08-venue-back-office.yaml#BO-157; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **requiredSequence is an array of free strings** Why: Steps must come from a closed vocabulary (naming a park or attraction where needed) to be evaluated identically online and offline. *(source: contracts/spine/access.yaml#setJourneySequenceRule / ADR-0068; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No deny reason exists for an anti-passback or sequence violation** Why: DenyReason has no passback or journey-violation value, so the pack's "RED - ANTI-PASSBACK VIOLATION" cannot be shown in words (VO-R06). *(source: screens/P08-venue-back-office.yaml#BO-157 / contracts/spine/access.yaml#/components/schemas/DenyReason; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The write requires id and scopePath** Why: Server-owned (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a journey rule apply to every product, or should it name the products or admission profiles it covers?** → Journey rules get an 'Applies to' picker: venue-wide by default, or chosen products/admission profiles. *(decided by Chinmay, 2026-10-02; DEC-231 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ENTRY → EXIT → RE-ENTRY | text field | — | — | — | — | — | — |
| PARK A → CROSSOVER → PARK B | text field | — | — | — | — | — | — |
| MAIN ENTRY → ATTRACTION ENTRY | text field | — | — | — | — | — | — |

**Form: Save journey sequence rule** (modal, opened by *Save journey sequence rule*; *Save journey sequence rule* calls `setJourneySequenceRule`, *Cancel* sends nothing)

**Collects what `setJourneySequenceRule` sends before it is called.** Required: `id`, `scopePath`, `scope`. Optional: `venueId`, `name`, `windowMinutes`, `requiredSequence`, `violationResponses`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setJourneySequenceRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setJourneySequenceRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setJourneySequenceRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setJourneySequenceRule` body |
| Scope `scope` | select | required | — | Credential · Guest · Gate · Attraction · Park · Venue | — | Level the anti-passback check applies at | `setJourneySequenceRule` body |
| Window minutes `windowMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setJourneySequenceRule` body |
| Required sequence `requiredSequence` | list of values (chips) | optional | — | — | — | Ordered steps, e.g. | `setJourneySequenceRule` body |
| Violation responses `violationResponses` | multi-select chips | optional | — | Deny · Warning · Refer to operator · Require supervisor · Allow override · Trigger security alert | — | — | `setJourneySequenceRule` body |
| Applies to `appliesTo` | group | optional | — | — | — | What the rule covers: venue-wide by default, or chosen products or admission profiles (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-157: "An 'Applies to' picker … | `setJourneySequenceRule` body |
| Mode `appliesTo.mode` | segmented control | optional | Venue wide | Venue wide · Selected | — | — | `setJourneySequenceRule` body |
| Products `appliesTo.productIds` | multi-picker: choose products | optional | — | — | — | — | `setJourneySequenceRule` body |
| Admission profiles `appliesTo.admissionProfileIds` | multi-picker: choose admission profiles | optional | — | — | — | — | `setJourneySequenceRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required in practice (the list shows rules by name); max 200, e.g. "Annual pass - 20 min passback". *(source: contracts/spine/access.yaml#setJourneySequenceRule)*
- **scope**: Required single choice Credential / Guest / Gate / Attraction / Park / Venue with one-line meanings (Guest catches one person on two credentials; Credential catches one credential in two hands). *(source: screens/P08-venue-back-office.yaml#BO-157 / contracts/spine/access.yaml#setJourneySequenceRule)*
- **windowMinutes**: Minimum interval between scans in minutes, whole number, 0 allowed (sequence only); the pack's example is 20. *(source: screens/P08-venue-back-office.yaml#BO-157 / contracts/spine/access.yaml#setJourneySequenceRule / DI-626)*
- **requiredSequence**: A step builder - add steps from a closed list (Entry, Exit, Re-entry, Crossover, Attraction entry), each optionally pinned to a place (park, attraction) for the Park A > Crossover > Park B and Main entry > Attraction entry patterns; drag to reorder; arrows between steps. Never typed text. *(source: screens/P08-venue-back-office.yaml#BO-157 / contracts/spine/access.yaml#setJourneySequenceRule)*
- **violationResponses**: Multi-select of the six responses; Deny and Allow override cannot both be chosen; Trigger security alert combines with any. *(source: screens/P08-venue-back-office.yaml#BO-157 / contracts/spine/access.yaml#setJourneySequenceRule)*
- **id, scopePath, venueId, timestamps**: Not inputs (VO-R03); a new rule sends no id. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*
- **Applies to**: Venue-wide by default, or chosen products or admission profiles. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save journey sequence rule (primary button) | `setJourneySequenceRule` PUT `/journey-sequence-rules` | AccessJourneySequenceRule | AccessJourneySequenceRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete journey sequence rule (destructive button) | `deleteJourneySequenceRule` DELETE `/journey-sequence-rules/{ruleId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule list**: Rules with scope, window ("20 min"), sequence as arrow chips and responses as icons. *(source: contracts/spine/access.yaml#listAntiPassbackJourney)*
- **Example result**: A test card beside the form - credential type, first gate, second gate, seconds between - showing Admitted or the red violation with the response that applies. *(source: screens/P08-venue-back-office.yaml#BO-157 / DI-629)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Upsert of the whole rule (VO-R04); applies with the next offline package. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*
- **Delete rule**: Confirmation; scans already judged keep their outcome. *(source: contracts/spine/access.yaml#deleteJourneySequenceRule)*

**Data it reads**: `listAntiPassbackJourney` (onLoad, Anti-Passback & Journey Sequence)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAntiPassbackJourney`

**What opens over it**

- confirmDialog *Delete journey sequence rule*: **Names what `deleteJourneySequenceRule` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The anti-passback journey sequence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the anti-passback journey sequence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No anti-passback journey sequence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Offline gates**: A gate- or credential-level rule can run on one device; a park or venue scope needs other gates' scans, so the rule shows "Checked online only" for offline gates. *(source: screens/P08-venue-back-office.yaml#BO-206)*
- **Access point also has its own anti-passback switch**: The rule list notes which access points have the switch on, so the two do not double-deny. *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint)*

#### Consistency with other screens

- Match `BO-148`: The access point's anti-passback toggle and these rules must be explained together.
- Match `SCN-003`: The scanner's red state for a violation needs a deny label of its own (VO-R06).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- name: Annual pass passback
  scope: Credential
  window: 20 min
  sequence: Entry > Exit > Re-entry
  responses: Deny, Trigger security alert
- name: Two-park hopper order
  scope: Guest
  window: '0'
  sequence: Summit Peaks entry > Crossover > Aqua Park entry
  responses: Refer to operator
example: AP-10452 scanned at Main Plaza Gate 1 at 10:02:10, then at North Entry at 10:02:55 - ANTI-PASSBACK VIOLATION
```

#### Permissions

- `listAntiPassbackJourney` → `SCOPE_VIEW` (read) · staff
- `setJourneySequenceRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteJourneySequenceRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-157` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-157`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 6: Works in Anti-Passback & Journey Sequence → Prevent credential sharing and impossible access sequences.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-157?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save journey sequence rule, Delete journey sequence rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-158` Access Validity & Time Rules

**Determine when access is permitted.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-158 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/access-validity-time-rules-bo-158` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Validity and Time block of an admission profile: fixed or relative validity (From/To, N days after sale, activation or first use, to the end of the day/week/month/year), calendar validity (weekdays, weekends, peak, off-peak, holidays, seasons, event dates, blackout dates), time windows (the pack's Morning Ticket 09:00-13:00 with a 30-minute grace) and no-show expiry (performance 14:00, tolerance 20 min, expires 14:20). Per VO-R14 it is the "Validity" and "Admission window" sections of BO-032. The one thing to get right: the computed result is always shown on a concrete example, because relative validity is easy to misread.

**Known correction pending (do not draw the wrong version)**

- **"From / To" drawn as a primary button and "End of Day", "End of Week", "End of Month" as destructive buttons with confirm dialogs** Why: They are values of the validity basis, not actions; nothing is destroyed. *(source: screens/P08-venue-back-office.yaml#BO-158; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Seven selectFields (weekdays, weekends, peak dates ... event dates)** Why: They are chips of daysOfWeek and dayTypes in one field each. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listAccessValidityTime returns time window, grace period, admission tolerance and no-show expiry, but the write (AdmissionRules) has no time window or grace field** Why: The pack's Morning Ticket example cannot be saved; the read and write must share one shape (the profile's). *(source: screens/P08-venue-back-office.yaml#BO-158 / contracts/spine/access.yaml#listAccessValidityTime / contracts/spine/access.yaml#updateAdmissionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Places validity in time but blackout dates have no calendar component on the screen** Why: VO-R01 - draw blackout dates on a month calendar. *(source: DI-907 / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| weekdays | select field | — | — | — | — | — | — |
| weekends | select field | — | — | — | — | — | — |
| peak dates | select field | — | — | — | — | — | — |
| off-peak dates | select field | — | — | — | — | — | — |
| holidays | select field | — | — | — | — | — | — |
| seasons | select field | — | — | — | — | — | — |
| event dates | select field | — | — | — | — | — | — |

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validity (anchor, days, from, to, endOf)**: BO-032's sentence builder. The pack's "End of Day / End of Week / End of Month / End of Year" are the options of "to the end of that ..." after a relative period, not buttons. *(source: screens/P08-venue-back-office.yaml#BO-158 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Calendar validity (daysOfWeek, dayTypes, blackoutDates)**: Weekday chips Mon-Sun (week starting on the venue's first day, "Weekends" as a shortcut that ticks the venue's weekend days, Fri-Sat in the UAE); day-type chips Peak, Off-peak, Holidays, Seasons, Event dates whose dates come from the venue calendar (BO-152); blackout dates on a month calendar (VO-R01), with "Blackout always wins" under it. *(source: screens/P08-venue-back-office.yaml#BO-158 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Time window and grace**: "Valid from [09:00] to [13:00], grace [30] min" in venue time. The profile has no field for a daily time window (see corrections); until one exists draw it greyed with "Not yet supported". *(source: screens/P08-venue-back-office.yaml#BO-158 / contracts/spine/access.yaml#listAccessValidityTime)*
- **No-show expiry (maxDurationMinutes) and admission window (openMinutesBefore, closeMinutesAfter)**: The admission window group of BO-032, with the pack's example as the live preview "Performance 14:00, tolerance 20 min - expires 14:20". *(source: screens/P08-venue-back-office.yaml#BO-159 / contracts/spine/access.yaml#/components/schemas/AdmissionRules / MATRIX 3.2.10)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| From / To (primary button) | navigation or local | — | — | — | — |
| End of Day (destructive button) | navigation or local | — | — | — | — |
| End of Week (destructive button) | navigation or local | — | — | — | — |
| End of Month (destructive button) | navigation or local | — | — | — | — |
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validity preview**: "Sold 1 Oct 2026, first used 4 Oct 2026: valid 4 Oct to 31 Oct 2026, Fridays and Saturdays excluded, not on 2 Dec (blackout)" - recomputed on every change, with a date picker to try another sale or first-use date. *(source: designer default / DI-171)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Whole-profile save (VO-R04) with the other sections' values; applies to issued tickets that reference the profile after the next package refresh. *(source: contracts/spine/access.yaml#updateAdmissionRules / MATRIX 3.2.34)*

**Data it reads**: `listAccessValidityTime` (onLoad, Access Validity & Time Rules); `listAdmissionRules` (onLoad, The admission profiles whose validity windows are edited …)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAccessValidityTime`

**What opens over it**

- confirmDialog *End of Day*: **End of Day on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End of Week*: **End of Week on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End of Month*: **End of Month on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access validity time configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access validity time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access validity time configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **To date before From date, or relative anchor with no days**: 422 shown against the field ("End date is before start date"; "Enter the number of days"). *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Day type chosen but the venue calendar has no dates of that type**: Warn "No Peak dates are set in the operating calendar - this ticket would never be valid" with a link to BO-152. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*

#### Consistency with other screens

- Match `BO-032`: Same sections and labels, one Save (VO-R14).
- Match `BO-152`: Day types resolve to dates from the operating calendar; blackout dates are per profile.
- Match `SCN-003`: Not yet valid (show from when) and Expired are the deny reasons these fields produce (VO-R06).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Morning Ticket
  validity: Visit date
  window: 09:00-13:00, grace 30 min
  calendar: All days
- name: 30-day pass
  validity: 30 days after first use, to end of day
  calendar: Sun-Thu, not peak dates
  blackout: 2 Dec 2026, 3 Dec 2026
- name: Theatre performance
  admission: Opens 30 min before, closes 60 min after
  noShow: Expires 20 min after 14:00 = 14:20
```

#### Permissions

- `listAccessValidityTime` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-158` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-158`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 8: Works in Access Validity & Time Rules → Determine when access is permitted.

#### Acceptance for the design

- [ ] Every input above is drawn (54), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-158?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: From / To, End of Day, End of Week, End of Month, Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-159` Entitlement Consumption Engine

**Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of carrying park admission, ride entitlement, meal voucher, coupon, photo voucher and re-entry rights.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-159 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entitlement-consumption-engine-bo-159` |

**What the spec says about it.** **Time-bound entitlements belong here (decided 2 October 2026 by Chinmay, DEC-232; CHG-CSP-030):** valid for N minutes from the first scan (for example 60), refused after, offline too.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Decides what a successful scan consumes when one credential carries several entitlements (park admission, ride, Fast Pass, meal, voucher, photo, locker, re-entry), in what order and how many units, and shows the balance left. The pack's example: Silver Fast Pass, 3 uses, 1 per validation, reset daily, selected attractions - Ride 1 remaining 2, Ride 2 remaining 1, Ride 3 remaining 0; Gold Fast Pass unlimited, one access per ride. The one thing to get right: show the consumption order of all rules of one credential together, with the remaining balance worked through.

**Known correction pending (do not draw the wrong version)**

- **Five entitlement types (Attraction Admission, Voucher, Event, Experience, Membership benefit) drawn as action-bar buttons** Why: They are values of entitlementType, not actions. *(source: screens/P08-venue-back-office.yaml#BO-159 / contracts/spine/access.yaml#setEntitlementConsumption; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's Reset (daily) has no field in the write** Why: Silver Fast Pass "3 per day" cannot be configured; a reset period is needed. *(source: screens/P08-venue-back-office.yaml#BO-159 / contracts/spine/access.yaml#/components/schemas/EntitlementConsumptionEngineInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save consumption rule has no permission declared on the screen** Why: The write requires ACCESS_POINT_CONFIGURE; disable with the reason otherwise (VO-R08). *(source: contracts/spine/access.yaml#setEntitlementConsumption; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do time-bound product entitlements (e.g. 60 minutes from first scan) belong to this engine?** → Time-bound product entitlements (validity from first scan, e.g. 60 minutes) belong to the access engine. *(decided by Chinmay, 2026-10-02; DEC-232 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Sent by *Save consumption rule*** (`setEntitlementConsumption`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setEntitlementConsumption` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setEntitlementConsumption` body |
| Credential type `credentialType` | text field | optional | — | — | — | Credential or product type the rule applies to | `setEntitlementConsumption` body |
| Entitlement type `entitlementType` | select | required | — | Park admission · Attraction admission · Ride · Fast pass · Meal · Voucher · Photo · Locker · Event · Experience · Re entry · Membership benefit … | — | — | `setEntitlementConsumption` body |
| Consumption order `consumptionOrder` | number field | optional | 1 | min 1 | — | Where one scan could consume several entitlements, lower is consumed first | `setEntitlementConsumption` body |
| Consumption per validation `consumptionPerValidation` | number field | optional | 1 | min 1 | — | Units one scan consumes | `setEntitlementConsumption` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | Units the entitlement carries; ignored when unlimited | `setEntitlementConsumption` body |
| Unlimited `unlimited` | toggle | optional | off | — | — | — | `setEntitlementConsumption` body |
| One per attraction `onePerAttraction` | toggle | optional | off | — | — | — | `setEntitlementConsumption` body |
| Attractions `attractionIds` | list of values (chips) | optional | — | — | — | Empty means every attraction the entitlement covers | `setEntitlementConsumption` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **entitlementType**: Select of the thirteen types (Park admission, Attraction admission, Ride, Fast Pass, Meal, Voucher, Photo, Locker, Event, Experience, Re-entry, Membership benefit, Custom). *(source: screens/P08-venue-back-office.yaml#BO-159 / contracts/spine/access.yaml#setEntitlementConsumption)*
- **credentialType**: Product or credential picker (Silver wristband, Annual pass, Adventure Day Pass), not free text. *(source: contracts/spine/access.yaml#setEntitlementConsumption)*
- **quantity / unlimited / consumptionPerValidation**: "Carries [3] units" or Unlimited (quantity hidden); "Each scan uses [1]" (min 1, cannot exceed quantity). *(source: screens/P08-venue-back-office.yaml#BO-159 / contracts/spine/access.yaml#setEntitlementConsumption)*
- **attractionIds / onePerAttraction**: Attraction multi-select (empty reads "Every attraction the entitlement covers"); "Once per ride" switch for the Gold Fast Pass case. *(source: screens/P08-venue-back-office.yaml#BO-160 / contracts/spine/access.yaml#setEntitlementConsumption)*
- **consumptionOrder**: Not typed; set by dragging rules of the same credential in the order panel (lower consumed first). *(source: contracts/spine/access.yaml#setEntitlementConsumption)*
- **Reset (daily)**: The pack's "Reset Daily" - draw as None / Daily / Weekly; the contract has no field (see corrections), so greyed until added. *(source: screens/P08-venue-back-office.yaml#BO-159)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Attraction Admission (primary button) | navigation or local | — | — | — | — |
| Voucher (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Experience (secondary button) | navigation or local | — | — | — | — |
| Membership benefit (secondary button) | navigation or local | — | — | — | — |
| Save consumption rule (primary button) | `setEntitlementConsumption` PUT `/entitlement-consumption` | EntitlementConsumptionEngineInput | EntitlementConsumptionEngineView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Neither quantity nor unlimited given | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Consumption order panel**: For the selected credential, its entitlement rules stacked in order with type icon, units and scope. *(source: contracts/spine/access.yaml#listEntitlementConsumption)*
- **Balance walk-through**: The pack's example table (scan 1, 2, 3 and remaining after each) generated from the rule, with the deny reason after the last unit ("No Fast Pass uses left"). *(source: screens/P08-venue-back-office.yaml#BO-160 / DI-628)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save consumption rule**: Upsert keyed by ruleId (absent creates); applies at the next package refresh; units already consumed are not recalculated, which the confirmation says. *(source: contracts/spine/access.yaml#setEntitlementConsumption)*

**Data it reads**: `listEntitlementConsumption` (onLoad, Entitlement Consumption Engine)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listEntitlementConsumption`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement consumption list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement consumption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement consumption yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement consumption are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Neither quantity nor unlimited given |

#### Edge cases to draw

- **Two rules of one credential have the same order number**: Prevented by the drag ordering; if loaded that way, flag the pair. *(source: contracts/spine/access.yaml#setEntitlementConsumption)*
- **Time-bound product entitlement (60 minutes from first scan)**: Configured here: validity from first scan (e.g. 60 minutes); once the window has passed the gate refuses and says when it ended. *(source: DI-458 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Consistency with other screens

- Match `BO-147`: Attraction entitlement requirement names these types.
- Match `SCN-003`: The scanner's remaining-balance line ("Fast Pass 2 of 3 left") uses these units.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- credential: Silver wristband
  type: Fast Pass
  quantity: 3
  perScan: 1
  reset: Daily
  attractions: Falcon Coaster, Wave Rider, Laser Arena
  order: 2
- credential: Silver wristband
  type: Park admission
  quantity: 1
  perScan: 1
  order: 1
- credential: Gold wristband
  type: Fast Pass
  unlimited: true
  oncePerRide: true
- credential: Adventure Day Pass
  type: Meal
  quantity: 1
  attractions: Food court
```

#### Permissions

- `listEntitlementConsumption` → `SCOPE_VIEW` (read) · staff
- `setEntitlementConsumption` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-159` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-159`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 10: Works in Entitlement Consumption Engine → Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-159?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Attraction Admission, Voucher, Event, Experience, Membership benefit, Save consumption rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-160` Multi-Park & Crossover Rules

**Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access based on previous park admission.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-160 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/multi-park-crossover-rules-bo-160` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): listMultiParkCrossover names its fields differently from AdmissionRules.crossover (allowedParks vs allowedParkOrgUnitIds, crossoverTime vs crossoverAfterTime) …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The crossover block of an admission profile: which parks a ticket admits to, in what order, same-day crossover or different-day access, consecutive days from first scan or flexible within validity, park entries, number of crossovers, earliest crossover time, prerequisite park and re-entry after crossover. Per VO-R14 it is the "Crossover" section of BO-032. The pack asks for a visual journey builder (2-Park Hopper: Day 1 Aqua Park > First entry > Crossover allowed > Summit Peaks). The one thing to get right: Entry, Re-entry and Crossover are three different scan kinds and are labelled and reported separately.

**Known correction pending (do not draw the wrong version)**

- **The screen's write is described as saving "which parks a profile admits to (allowedAccessPointIds, scopePath)"** Why: Crossover is its own block of the profile; scopePath is server-owned (VO-R03). *(source: screens/P08-venue-back-office.yaml#BO-160; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Separate screen with an empty table and "Save admission rules"** Why: Section of BO-032 per VO-R14; label "Save profile". *(source: DI-671 / DI-987 / screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listMultiParkCrossover names the fields allowedParks, crossoverTime, prerequisitePark, numberOfParkEntries while AdmissionRules.crossover … (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Crossover fields**: BO-032's crossover field rules apply; this section adds the journey builder that writes the same fields (allowedParkOrgUnitIds, parkOrder, prerequisiteParkOrgUnitId) by placing park cards on a Day 1 / Day 2 timeline. *(source: screens/P08-venue-back-office.yaml#BO-160 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **crossoverAfterTime**: HH:MM venue time ("Crossover from 14:00"); empty = any time. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **dayPattern**: Shown only when different-day access is on - Consecutive days from first scan / Any days within validity. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-628)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey builder**: Park cards connected by arrows labelled Entry, Crossover, Re-entry in three distinct styles (solid, dashed, dotted, each with its word), right-to-left in Arabic; a summary "Two parks, same day, Aqua Park first, crossover after 14:00, one crossover". *(source: screens/P08-venue-back-office.yaml#BO-160 / screens/P08-venue-back-office.yaml#BO-161)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Whole-profile save (VO-R04). *(source: contracts/spine/access.yaml#updateAdmissionRules)*

**Data it reads**: `listAdmissionRules` (onLoad, The admission profiles that carry crossover rules)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAdmissionRules`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-park crossover rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-park crossover rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-park crossover rules yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-park crossover rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **Venue with one park**: Section shows "Crossover needs at least two parks" and stays off. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Prerequisite park not in the allowed parks**: Inline error before save. *(source: designer default)*

#### Consistency with other screens

- Match `BO-032`: Same section and one Save (VO-R14).
- Match `BO-220`: The live crossover screen uses the same crossover block and the same three scan kinds.
- Match `BO-157`: A park-order journey rule (Park A > Crossover > Park B) duplicates parkOrder here; the profile is the place for crossover order.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: 2-Park Hopper
  parks: Aqua Park, Summit Peaks
  order: Aqua Park first
  sameDay: true
  crossovers: 1
  after: '14:00'
  reEntryAfterCrossover: false
```

#### Permissions

- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-160` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-160`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 12: Works in Multi-Park & Crossover Rules → Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access …

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-160?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-161` Guest, Companion & Eligibility Rules

**Apply access conditions based on guest characteristics and relationships.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-161 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/access-venue/guest-companion-eligibility-rules-bo-161` |

**Known gaps.** **Seven pack categories are not age categories and are not carried** (decided 28 September, audit R275 (b): the guest categories map onto the age rules). POD, POD Companion, Nanny, VIP, Member, Staff …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who may take part in a product: age range, height limits and bands, an accompanying adult below an age, guardian signature ages, waiver, required certification. It is declared at booking and verified at the gate. The thing to get right is that guest categories are age bands: choosing Child on a ticket type sets the age range, so the two must never disagree.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listGuestCompanionEligibility return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The screen also lists listGuestCompanionEligibility (access contract, pack Access Control 2.8) next to the product rule. (CHG-SBO-010).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Infant | select field | — | — | — | — | Age band infant (under 3). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Child | select field | — | — | — | — | Age band child (3–12). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Junior | select field | — | — | — | — | Age band junior (13–17). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Adult | select field | — | — | — | — | Age band adult (18–59). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Senior | select field | — | — | — | — | Age band senior (60+). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Accompanied below age | number field | — | — | — | — | **Child Ticket + Assigned Adult Ticket** from the pack — a guest below this age must be accompanied (`accompaniedBelowAge`) (audit R275 (b)). | — |

**Form: Save age rule** (modal, opened by *Save age rule*; *Save age rule* calls `setProductEligibilityRule`, *Cancel* sends nothing)

**Collects what `setProductEligibilityRule` sends before it is called.** The guest categories are the age bands, so the categories chosen become `minAgeYears` and `maxAgeYears`; `accompaniedBelowAge`, the guardian-signature ages, `waiverRequired`, `swimAbility` and the height limits are optional (decided 28 September, audit R275 (b)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Min age years `minAgeYears` | number field | optional | — | min 0 | — | — | `setProductEligibilityRule` body |
| Max age years `maxAgeYears` | number field | optional | — | min 0 | — | — | `setProductEligibilityRule` body |
| Min height cm `minHeightCm` | number field | optional | — | min 50; max 250 | — | — | `setProductEligibilityRule` body |
| Max height cm `maxHeightCm` | number field | optional | — | min 50; max 250 | — | — | `setProductEligibilityRule` body |
| Height bands cm `heightBandsCm` | list of values (chips) | optional | 120, 140 | — | — | Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over. | `setProductEligibilityRule` body |
| Accompanied below age `accompaniedBelowAge` | number field | optional | — | — | — | Under this age an adult must be present, e.g. 8 at the kids club. | `setProductEligibilityRule` body |
| Guardian signature age from `guardianSignatureAgeFrom` | number field | optional | — | — | — | — | `setProductEligibilityRule` body |
| Guardian signature age to `guardianSignatureAgeTo` | number field | optional | — | — | — | Ages needing a guardian's signature, e.g. 12–15 on a thrill ride. | `setProductEligibilityRule` body |
| Waiver required `waiverRequired` | toggle | optional | off | — | — | — | `setProductEligibilityRule` body |
| Refundable if ineligible at gate `refundableIfIneligibleAtGate` | toggle | optional | off | — | — | — | `setProductEligibilityRule` body |
| Required certification code `requiredCertificationCode` | text field | optional | — | max length 60 | — | A certification the participant must hold (decided 29 September, W4; added 30 September), e.g. | `setProductEligibilityRule` body |

Carried, not typed: `productId`

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **age range**: Derived from the guest categories chosen (Child 3-11 gives min 3, max 11); editing the numbers directly warns if they no longer match the category names. *(source: contracts/spine/catalogue.yaml#setProductEligibilityRule / R275)*
- **heightBandsCm**: Band edges as a slider with labels ("under 1.20 m, 1.20 to 1.40 m, 1.40 m and over"), 50 to 250 cm. *(source: contracts/spine/catalogue.yaml#/components/schemas/ProductEligibilityRule)*
- **swim ability**: Not a field here any more; it is a consent question attached to the product (link to the consent questions). *(source: REV3-26 / contracts/spine/catalogue.yaml#/components/schemas/ProductEligibilityRule)*
- **requiredCertificationCode**: For dives and similar, e.g. PADI Open Water; empty means none. *(source: contracts/spine/catalogue.yaml#/components/schemas/ProductEligibilityRule)*

#### Outputs: what the screen shows and produces

**Shown**

**The age rule** (detail panel, from `getProductEligibilityRule`): **The guest categories are the age bands** (decided 28 September, audit R275 (b)) — Infant under 3, Child 3–12, Junior 13–17, Adult 18–59, Senior 60+ (`EligibilityDeclaration.ageBand`). A product admits the bands its `minAgeYears`/`maxAgeYears` cover; height stays its own limit.

| Shows | Format | Notes |
|---|---|---|
| Min age years | 1,234 | — |
| Max age years | 1,234 | — |
| Accompanied below age | 1,234 | Under this age an adult must be present, e.g. 8 at the kids club. |
| Guardian signature age from | 1,234 | — |
| Guardian signature age to | 1,234 | Ages needing a guardian's signature, e.g. 12–15 on a thrill ride. |
| Min height cm | 1,234 | — |
| Max height cm | 1,234 | — |
| Height bands cm | list or chips (count when long) | Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over. |

**Companion and eligibility types (reference)** (detail panel, from `listGuestCompanionEligibility`): Read-only reference: the seven pack categories are credential or entitlement types (R275 b), not editable eligibility.

| Shows | Format | Notes |
|---|---|---|
| Rule | text | — |
| Guest category | chip: Adult, Child, Junior, Senior, Pod, Pod companion… | — |
| Name | text | — |
| Required companion category | text | Category of the qualifying companion, e.g. |
| Companion verification | chip: Linked ticket, Companion biometric | — |
| Verify at | list or chips (count when long) | Where the companion is checked (decided 29 September, VM close-out) |
| Attractions | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save age rule (primary button) | `setProductEligibilityRule` PUT `/products/{productId}/eligibility-rule` | ProductEligibilityRule | ProductEligibilityRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rule summary**: Rendered as the guest will read it: "Ages 8 and over; under 12 with an adult; minimum height 1.20 m; waiver required". *(source: designer default)*

**Data it reads**: `getProductEligibilityRule` (onLoad, A product's age, height and supervision limits); `listGuestCompanionEligibility` (onLoad, Guest, Companion & Eligibility Rules)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listGuestCompanionEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest companion eligibility configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest companion eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest companion eligibility configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Product with no rule set**: Shown as "Anyone may take part" (the read answers with every limit empty, not an error). *(source: contracts/spine/catalogue.yaml#getProductEligibilityRule)*
- **Guest found ineligible at the gate**: Whether the ticket is refundable then is a setting on this rule (refundableIfIneligibleAtGate); show it. *(source: contracts/spine/catalogue.yaml#/components/schemas/ProductEligibilityRule)*

#### Consistency with other screens

- Match `BO-008`: Shown as the eligibility section of the product configuration.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  product: Sandstorm Coaster
  minAge: 8
  accompaniedBelowAge: 12
  minHeightCm: 120
  waiver: true
  refundableIfIneligibleAtGate: true
```

#### Permissions

- `getProductEligibilityRule` → `PRODUCT_VIEW` (read) · staff, guest
- `setProductEligibilityRule` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGuestCompanionEligibility` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.5.11 | Support configurable restrictions governing transfers, spending limits, age restrictions, membership rules, and entitlement usage. | F&B & Guest Management | CONTRACTED | data `ProductEligibilityRule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-161` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-161`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 14: Works in Guest, Companion & Eligibility Rules → Apply access conditions based on guest characteristics and relationships.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-161?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save age rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-162` Group Admission & Quantity Validation

**Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to represent multiple admissions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-162 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-admission-quantity-validation-bo-162` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Rules for admitting groups fast: which group modes a product allows (entire group, partial group, multiple waves, leader plus guests, single QR multi-entry, individual child tickets under a group, pre-validated B2B manifest) and the maximum group size. The pack's gate example: "GROUP TICKET - Authorized guests 50"; the operator enters "Guests entering now 42"; the system records Entered 42, Remaining 8, attendance +42. The one thing to get right: the screen previews exactly what the scanner will show for the chosen modes.

**Known correction pending (do not draw the wrong version)**

- **Two vocabularies for group admission modes** Why: BO-162 has singleQrMultiEntry, leaderGuests, individualChildTicketsUnderGroup, prevalidatedB2bManifest; BO-215 has individualScan, leaderQuantity, manifestBased. Consolidate into one list (VO-R14). *(source: contracts/spine/access.yaml#/components/schemas/GroupAdmissionQuantityValidationView / contracts/spine/access.yaml#setGroupAdmissionProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Read-only screen (listGroupAdmissionQuantity) with an empty table and no write (CHG-WIR-003).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **allowedGroupModes**: Seven mode cards with a one-line description each; at least one; Fast group mode (Scan leader QR > Confirm attendance > Open group lane) shown as a highlighted card. *(source: screens/P08-venue-back-office.yaml#BO-162 / screens/P08-venue-back-office.yaml#BO-163 / contracts/spine/access.yaml#/components/schemas/GroupAdmissionQuantityValidationView)*
- **productIds**: Product picker (group, school, tour and family products). *(source: contracts/spine/access.yaml#listGroupAdmissionQuantity)*
- **maxGroupSize**: Whole number of guests; the authorised quantity per ticket still comes from the ticket. *(source: contracts/spine/access.yaml#listGroupAdmissionQuantity)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scanner preview**: A P07 frame showing "Group ticket - Authorized guests 50 - Guests entering now [42]" and the result "Entered 42, Remaining 8, Attendance +42". *(source: screens/P08-venue-back-office.yaml#BO-162)*
- **Rule list**: Name, Products, Modes (chips), Max group size. *(source: contracts/spine/access.yaml#listGroupAdmissionQuantity)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save group admission rule**: No write exists on this screen (see corrections); draw Save disabled with "Configured in Group & B2B Admission Profile Builder" and a link to BO-215 until one is bound. *(source: contracts/spine/access.yaml#setGroupAdmissionProfile)*

**Data it reads**: `listGroupAdmissionQuantity` (onLoad, Group Admission & Quantity Validation)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listGroupAdmissionQuantity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group admission quantity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group admission quantity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group admission quantity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group admission quantity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Operator enters more guests than remain**: The scanner refuses with "Only 8 guests remain on this group ticket". *(source: screens/P08-venue-back-office.yaml#BO-162 / contracts/spine/access.yaml#validateGroupAccess)*
- **Multiple waves**: Preview shows the second wave starting from the remaining count. *(source: screens/P08-venue-back-office.yaml#BO-162)*

#### Consistency with other screens

- Match `SCN-007`: The group admission screen on the scanner must show these numbers and words.
- Match `BO-215`: Group & B2B admission profiles (setGroupAdmissionProfile) hold an overlapping admission method list; one of the two screens should own group modes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- name: School groups
  products: School Day Visit
  modes: Leader + guests, Multiple waves
  maxGroup: 120
- name: Tour operators
  products: Tour Group Admission
  modes: Prevalidated B2B manifest, Entire group
  maxGroup: 60
gate:
  authorized: 50
  enteringNow: 42
  entered: 42
  remaining: 8
```

#### Permissions

- `listGroupAdmissionQuantity` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-162` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-162`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 16: Works in Group Admission & Quantity Validation → Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-162?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-163` Rule Simulation, Conflict Check & Publication

**No access rule should reach a live gate without being tested.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-163 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `APPROVAL_REQUEST` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/rule-simulation-conflict-check-publication-bo-163` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** No access rule reaches a live gate untested. The manager builds a virtual scan (credential, guest category, date, time, park, gate and the previous journey - "Summit Peaks entered 14:00, exited 17:30"), runs it, and reads a decision trace (credential valid, visit date valid, entitlement, crossover allowed, previous park met, entry quantity, anti-passback, verification method) ending in ALLOW or DENY with the rule that failed. The rule version then goes Draft > Simulate > Validate > Approval > Schedule > Publish, with versions and rollback. The one thing to get right: the trace shows exactly which condition failed, by rule id.

**Known correction pending (do not draw the wrong version)**

- **publishRuleConflictCheck is one PUT whose request carries the outputs (decision, decisionTrace, failedRuleId, conflicts)** Why: The decision and trace are the server's result; simulate needs a POST returning them, separate from the lifecycle step write. *(source: contracts/spine/access.yaml#publishRuleConflictCheck; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **previousJourney is an array of free strings and credentialId expects a real credential** Why: Prior scans need park, gate, direction and time; a simulation should accept a product or credential type. *(source: contracts/spine/access.yaml#publishRuleConflictCheck / DI-629; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buttons labelled "Rule V1.0", "Rule V1.1", "Rule V2.0"** Why: Sample version labels; draw a version picker. *(source: screens/P08-venue-back-office.yaml#BO-163; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Submit for approval is not bound and the navigation exit to BO-154 has no transition (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Submit for approval** (modal, opened by *Submit for approval*; *Submit for approval* calls `createApprovalRequest`, *Cancel* sends nothing)

**Collects what `createApprovalRequest` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createApprovalRequest` body |
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `createApprovalRequest` body |
| Subject contract `subjectContract` | text field | required | — | — | — | Which contract owns the thing being approved. | `createApprovalRequest` body |
| Subject type `subjectType` | text field | required | — | — | — | — | `createApprovalRequest` body |
| Subject `subjectId` | text field | required | — | — | — | A reference, never a copy. A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists. | `createApprovalRequest` body |
| Scope path `scopePath` | text field | required | — | — | — | — | `createApprovalRequest` body |
| Summary `summary` | text area | required | — | max length 300 | — | What the approver sees in their queue before opening it. | `createApprovalRequest` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createApprovalRequest` body |
| Attributes `attributes` | key and value settings | optional | — | — | — | — | `createApprovalRequest` body |
| Justification `justification` | text area | optional | — | max length 1000 | — | — | `createApprovalRequest` body |
| Is draft `isDraft` | toggle | optional | off | — | — | True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129). | `createApprovalRequest` body |

Errors to draw in the form: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scenario**: Credential type or product (not a real guest's credential), guest category, date, time (venue time), park, gate, and the previous journey as rows of prior scans (park, gate, direction, time). A real ticket number may be pasted to replay its history. *(source: screens/P08-venue-back-office.yaml#BO-163 / contracts/spine/access.yaml#publishRuleConflictCheck / DI-629)*
- **ruleVersionId**: A version picker (V1.0, V1.1, V2.0 with status), defaulting to the draft being tested. *(source: screens/P08-venue-back-office.yaml#BO-163 / contracts/spine/access.yaml#publishRuleConflictCheck)*
- **scheduledAt**: For Schedule, a future date-time in venue time. *(source: contracts/spine/access.yaml#publishRuleConflictCheck)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Rule V1.0 (primary button) | navigation or local | — | — | — | — |
| Rule V1.1 (secondary button) | navigation or local | — | — | — | — |
| Rule V2.0 (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Submit for approval (secondary button) | `createApprovalRequest` POST `/approval-requests` | CreateApprovalRequest | ApprovalRequest | 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Decision trace**: Each check as a row with a tick or cross in evaluation order, the final decision as a large green ALLOW or red "DENY - RULE AC-284" naming the failed condition; the deny uses the VO-R06 label the scanner would show. *(source: screens/P08-venue-back-office.yaml#BO-163)*
- **Conflict findings**: Advisory list - contradictory, overlapping, unreachable, duplicate conditions, missing gate coverage, impossible journeys, overly broad overrides, offline-incompatible conditions - each naming the rules (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-163)*
- **Lifecycle rail and versions**: Draft > Simulate > Validate > Approval > Schedule > Publish with the version history and who moved it. *(source: screens/P08-venue-back-office.yaml#BO-163)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run simulation**: Returns decision and trace; no real transaction is created. *(source: contracts/spine/access.yaml#publishRuleConflictCheck / DI-629)*
- **Submit for approval / Publish / Schedule**: The publish gate names what goes live (rule version, gates, from when); approval through the approvals engine. *(source: contracts/spine/approvals.yaml#createApprovalRequest / contracts/spine/access.yaml#publishRuleConflictCheck)*
- **Roll back**: Confirmation naming the version restored and the gates affected (step rollBack). *(source: contracts/spine/access.yaml#publishRuleConflictCheck)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule simulation conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule simulation conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule simulation conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule simulation conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Edge cases to draw

- **Condition that cannot run offline**: Flagged "Online required" in the findings; the trace shows what an offline gate would decide. *(source: screens/P08-venue-back-office.yaml#BO-163 / screens/P08-venue-back-office.yaml#BO-206)*
- **Unresolved blocking conflict**: Publish disabled with the conflict named. *(source: designer default)*

#### Consistency with other screens

- Match `BO-032`: The "Test with a virtual scan" in the profile editor is this simulation in a panel; same inputs and trace.
- Match `BO-153`: Same lifecycle rail and publish gate wording as topology publication.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario:
  credential: Annual Pass
  guest: Adult member
  date: Fri 9 Oct 2026
  time: '18:30'
  park: Aqua Park
  gate: Main Plaza Gate 3
  previous: Summit Peaks entered 14:00, exited 17:30
trace:
- Credential valid - pass
- Visit date valid - pass
- Aqua Park entitlement - pass
- Crossover allowed - pass
- Previous park requirement met - pass
- Entry quantity available - pass
- Anti-passback passed - pass
- Verification method valid - pass
- FINAL - ALLOW
```

#### Permissions

- `publishRuleConflictCheck` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Simulation tool validates a rule (e.g. ticket allowed in Zone A and B, not C or D) via a virtual scan before publishing, without a real transaction. *(client request · MoM 2 Sep 2026, 4.5 Rule Simulation Tool · DI-629)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-163` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-163`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 18: Works in Rule Simulation, Conflict Check & Publication → No access rule should reach a live gate without being tested.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-163?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Rule V1.0, Rule V1.1, Rule V2.0, What publishing changes, Submit for approval.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `APPROVAL_REQUEST`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**17 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"deleteJourneySequenceRule": {"method":"DELETE","path":"/journey-sequence-rules/{ruleId}","contract":"access","summary":"Delete a journey sequence rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getProductEligibilityRule": {"method":"GET","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Who may take part: age, height, supervision","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"ProductEligibilityRule"},
"listAccessRule": {"method":"GET","path":"/access-rule","contract":"access","summary":"Access Rule Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"credential","in":"query","required":false},{"name":"ruleType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessValidityTime": {"method":"GET","path":"/access-validity-time","contract":"access","summary":"Access Validity & Time Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessValidityTimeRulesView"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAntiPassbackJourney": {"method":"GET","path":"/anti-passback-journey","contract":"access","summary":"Anti-Passback & Journey Sequence","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AntiPassbackJourneySequenceView"},
"listEntitlementConsumption": {"method":"GET","path":"/entitlement-consumption","contract":"access","summary":"Entitlement Consumption Engine","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementConsumptionEngineView"},
"listGroupAdmissionQuantity": {"method":"GET","path":"/group-admission-quantity","contract":"access","summary":"Group Admission & Quantity Validation","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupAdmissionQuantityValidationView"},
"listGuestCompanionEligibility": {"method":"GET","path":"/guest-companion-eligibility","contract":"access","summary":"Guest, Companion & Eligibility Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestCompanionEligibilityRulesView"},
"publishRuleConflictCheck": {"method":"PUT","path":"/rule-conflict-check","contract":"access","summary":"Rule Simulation, Conflict Check & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RuleSimulationConflictCheckPublicationInput","responds":"RuleSimulationConflictCheckPublicationView"},
"setEntitlementConsumption": {"method":"PUT","path":"/entitlement-consumption","contract":"access","summary":"Save an entitlement consumption rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EntitlementConsumptionEngineInput","responds":"EntitlementConsumptionEngineView"},
"setJourneySequenceRule": {"method":"PUT","path":"/journey-sequence-rules","contract":"access","summary":"Create or replace an anti-passback / journey sequence rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessJourneySequenceRule","responds":"AccessJourneySequenceRule"},
"setProductEligibilityRule": {"method":"PUT","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Set age, height and supervision limits","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"productId","in":"path","required":true}],"requestBody":"ProductEligibilityRule","responds":"ProductEligibilityRule"},
"setVisualAccessRule": {"method":"PUT","path":"/visual-access-rule","contract":"access","summary":"Visual Access Rule Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualAccessRuleBuilderInput","responds":"VisualAccessRuleBuilderView"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessJourneySequenceRule": {"type":"object","x-ticvai-persistence":"access.journey_sequence_rule","description":"One anti-passback / journey sequence rule - the level it applies at, the time window, the required order of scans and what a violation leads to (declared 29 September, data-model close-out DM1).","required":["id","scopePath","scope"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200,"nullable":true},"scope":{"type":"string","enum":["credential","guest","gate","attraction","park","venue"],"description":"Level the anti-passback check applies at"},"windowMinutes":{"type":"integer","minimum":0,"nullable":true},"requiredSequence":{"type":"array","items":{"type":"string"},"description":"Ordered steps, e.g. entry, exit, reEntry"},"violationResponses":{"type":"array","items":{"type":"string","enum":["deny","warning","referToOperator","requireSupervisor","allowOverride","triggerSecurityAlert"]}},"appliesTo":{"type":"object","nullable":true,"description":"**What the rule covers: venue-wide by default, or chosen products or admission profiles** (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-157: \"An 'Applies to' picker: venue-wide by default, or chosen products/profiles\"; DEC-231; CHG-CSP-029). Null or `mode: venueWide` applies at the rule's scope to every product; `selected` applies only to the products and admission profiles listed (at least one). Validation reads it with the admission rules and it travels in the offline package.","properties":{"mode":{"type":"string","enum":["venueWide","selected"],"default":"venueWide"},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"admissionProfileIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessRuleCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Rule Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"ruleName":{"type":"string","description":"Rule, e.g. Standard Park Entry"},"appliesTo":{"type":"string","description":"Products or credentials the rule applies to"},"location":{"type":"string","description":"Where the rule applies"},"validity":{"type":"string","description":"When the rule applies"},"ruleType":{"type":"string"},"status":{"type":"string","enum":["draft","pendingApproval","scheduled","active","inactive"]}}},
"AccessRuleCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeAccessRules":{"type":"integer","description":"Active Access Rules"},"draftRules":{"type":"integer","description":"Draft Rules"},"scheduledRules":{"type":"integer","description":"Scheduled Rules"},"rulesPendingApproval":{"type":"integer","description":"Rules Pending Approval"},"venuesCovered":{"type":"integer","description":"Venues Covered"},"productsTicketsCovered":{"type":"integer","description":"Products/Tickets Covered"},"rulesWithConflicts":{"type":"integer","description":"Rules with Conflicts"},"rulesUsingBiometrics":{"type":"integer","description":"Rules Using Biometrics"},"rulesAllowingOverride":{"type":"integer","description":"Rules Allowing Override"},"offlineCompatibleRules":{"type":"integer","description":"Offline-Compatible Rules"},"recentlyModifiedRules":{"type":"integer","description":"Recently Modified Rules"},"upcomingRuleChanges":{"type":"integer","description":"Upcoming Rule Changes"}}},
"AccessValidityTimeRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Validity & Time Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"validityBasis":{"type":"string","enum":["fixedRange","daysAfterSale","daysAfterActivation","daysAfterFirstUse","endOfDay","endOfWeek","endOfMonth","endOfYear"]},"dayTypes":{"type":"array","items":{"type":"string","enum":["weekdays","weekends","peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed"},"blackoutDates":{"type":"array","items":{"type":"string"},"description":"ISO dates on which access is refused"},"name":{"type":"string"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"validityDays":{"type":"integer","description":"N for the relative bases"},"timeWindowStart":{"type":"string","description":"Local time HH:MM, e.g. 09:00"},"timeWindowEnd":{"type":"string","description":"Local time HH:MM, e.g. 13:00"},"admissionToleranceMinutes":{"type":"integer"},"gracePeriodMinutes":{"type":"integer"},"noShowExpiryMinutes":{"type":"integer","description":"Credential expires this long after its admission/performance time if unused"},"minutesAfterFirstScan":{"type":"integer","nullable":true,"minimum":1,"maximum":10080,"description":"**A time-bound entitlement: valid for this many minutes from its first scan** (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-159: \"Yes: add time-bound entitlements (validity from first scan)\"; DEC-232; CHG-CSP-030; DI-458). For example 60 for a one-hour pass. The first admitting scan starts the window (`Entitlement.firstEntryAt`), the gate admits until `Entitlement.timeBoundUntil`, and a scan after it is denied (`ValidationResult.denyCause` `timeBoundWindowElapsed`). The window travels in the offline package (ADR-0068), so an offline gate refuses the same scan. Null: no time bound."}},"required":["ruleId","validityBasis"]},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"AntiPassbackJourneySequenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Anti-Passback & Journey Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"scope":{"type":"string","enum":["credential","guest","gate","attraction","park","venue"],"description":"Level the anti-passback check applies at"},"name":{"type":"string"},"windowMinutes":{"type":"integer","description":"Anti-passback time window"},"requiredSequence":{"type":"array","items":{"type":"string"},"description":"Ordered steps, e.g. entry, exit, reEntry"},"violationResponses":{"type":"array","items":{"type":"string"},"description":"Any of deny, warning, referToOperator, requireSupervisor, allowOverride, triggerSecurityAlert"}},"required":["ruleId","scope"]},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"EntitlementConsumptionEngineInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Entitlement Consumption Engine submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["name","entitlementType"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"name":{"type":"string","maxLength":200},"credentialType":{"type":"string","description":"Credential or product type the rule applies to"},"entitlementType":{"type":"string","enum":["parkAdmission","attractionAdmission","ride","fastPass","meal","voucher","photo","locker","event","experience","reEntry","membershipBenefit","custom"]},"consumptionOrder":{"type":"integer","minimum":1,"default":1,"description":"Where one scan could consume several entitlements, lower is consumed first"},"consumptionPerValidation":{"type":"integer","minimum":1,"default":1,"description":"Units one scan consumes"},"quantity":{"type":"integer","minimum":1,"description":"Units the entitlement carries; ignored when unlimited"},"unlimited":{"type":"boolean","default":false},"onePerAttraction":{"type":"boolean","default":false},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Empty means every attraction the entitlement covers"}}},
"EntitlementConsumptionEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entitlement Consumption Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialType":{"type":"string","description":"Credential or product type the rule applies to (decided 29 September, VM close-out)"},"consumptionOrder":{"type":"integer","minimum":1,"description":"Where one scan could consume several entitlements, lower is consumed first (decided 29 September, VM close-out)"},"ruleId":{"type":"string"},"entitlementType":{"type":"string","enum":["parkAdmission","attractionAdmission","ride","fastPass","meal","voucher","photo","locker","event","experience","reEntry","membershipBenefit","custom"]},"quantity":{"type":"integer","description":"Quantity (the pack shows 3)"},"consumptionPerValidation":{"type":"integer","description":"Consumption per validation (the pack shows 1)"},"name":{"type":"string"},"unlimited":{"type":"boolean","description":"No quantity limit, e.g. Gold Fast Pass"},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Attractions where it may be consumed"},"onePerAttraction":{"type":"boolean","description":"At most one use per attraction"}},"required":["ruleId","entitlementType"]},
"GroupAdmissionQuantityValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Admission & Quantity Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"allowedGroupModes":{"type":"array","items":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","leaderGuests","singleQrMultiEntry","individualChildTicketsUnderGroup","prevalidatedB2bManifest"]}},"name":{"type":"string"},"productIds":{"type":"array","items":{"type":"string"},"description":"Group products the rule covers"},"maxGroupSize":{"type":"integer"}},"required":["ruleId","allowedGroupModes"]},
"GuestCompanionEligibilityRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"name":{"type":"string"},"requiredCompanionCategory":{"type":"string","description":"Category of the qualifying companion, e.g. adult"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"]},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"description":"Where the companion is checked (decided 29 September, VM close-out)"},"attractionIds":{"type":"array","items":{"type":"string"}}},"required":["ruleId","guestCategory"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"ProductEligibilityRule": {"type":"object","x-ticvai-persistence":"catalogue.product_eligibility_rule","description":"Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true},"minHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"maxHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"heightBandsCm":{"type":"array","items":{"type":"integer"},"default":[120,140],"description":"Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."},"accompaniedBelowAge":{"type":"integer","nullable":true,"description":"Under this age an adult must be present, e.g. 8 at the kids club."},"guardianSignatureAgeFrom":{"type":"integer","nullable":true},"guardianSignatureAgeTo":{"type":"integer","nullable":true,"description":"Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."},"waiverRequired":{"type":"boolean","default":false},"swimAbility":{"type":"string","enum":["notRequired","confident"],"default":"notRequired","deprecated":true,"description":"**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"},"refundableIfIneligibleAtGate":{"type":"boolean","default":false},"requiredCertificationCode":{"type":"string","nullable":true,"maxLength":60,"description":"**A certification the participant must hold** (decided 29 September, W4; added 30 September), e.g. `padiOpenWater` for a dive. Null means none. Help me choose reads it: an answer whose `filter.certificationCode` names it with `holdsCertification: false` leaves the product out, and with `holdsCertification: true` (or no flag) keeps only products needing that certification or none. Proof, where the venue asks for it, is a consent question on the product (REV3-26), not this field."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"RuleSimulationConflictCheckPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Rule Simulation, Conflict Check & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"step":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"]},"ruleVersionId":{"type":"string","description":"Rule version being simulated or published"},"credentialId":{"type":"string","description":"Credential used for the virtual scan"},"accessPointId":{"type":"string"},"simulatedAt":{"type":"string","format":"date-time"},"previousJourney":{"type":"array","items":{"type":"string"},"description":"Prior scans assumed for the simulation"},"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"]},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Each condition checked and whether it passed"},"failedRuleId":{"type":"string"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Conflicts found (advisory)"},"scheduledAt":{"type":"string","format":"date-time"}},"required":["ruleVersionId","step"]},
"RuleSimulationConflictCheckPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Rule Simulation, Conflict Check & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"step":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"]},"ruleVersionId":{"type":"string","description":"Rule version being simulated or published"},"credentialId":{"type":"string","description":"Credential used for the virtual scan"},"accessPointId":{"type":"string"},"simulatedAt":{"type":"string","format":"date-time"},"previousJourney":{"type":"array","items":{"type":"string"},"description":"Prior scans assumed for the simulation"},"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"]},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Each condition checked and whether it passed"},"failedRuleId":{"type":"string"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Conflicts found (advisory)"},"scheduledAt":{"type":"string","format":"date-time"}},"required":["ruleVersionId","step"]},
"VisualAccessRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Visual Access Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"],"description":"THEN"},"name":{"type":"string"},"ruleId":{"type":"string"},"logic":{"type":"string","description":"Boolean expression combining the conditions with AND / OR / NOT"},"appliesTo":{"type":"array","items":{"type":"string"},"description":"Products or credential types (WHEN)"},"locationIds":{"type":"array","items":{"type":"string"},"description":"Venue, park, zone, attraction or gate IDs (AT)"},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions (IF), e.g. visitDate = today, remainingEntries > 0"},"consequences":{"type":"array","items":{"type":"string"},"description":"Actions performed on the decision, e.g. consumeEntry, incrementAttendance"}},"required":["ruleId","name","decision"]},
"VisualAccessRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Visual Access Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"],"description":"THEN"},"name":{"type":"string"},"ruleId":{"type":"string"},"logic":{"type":"string","description":"Boolean expression combining the conditions with AND / OR / NOT"},"appliesTo":{"type":"array","items":{"type":"string"},"description":"Products or credential types (WHEN)"},"locationIds":{"type":"array","items":{"type":"string"},"description":"Venue, park, zone, attraction or gate IDs (AT)"},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions (IF), e.g. visitDate = today, remainingEntries > 0"},"consequences":{"type":"array","items":{"type":"string"},"description":"Actions performed on the decision, e.g. consumeEntry, incrementAttendance"}},"required":["ruleId","name","decision"]}
}
```
