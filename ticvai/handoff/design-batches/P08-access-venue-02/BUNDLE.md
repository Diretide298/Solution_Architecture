# P08-access-venue-02 — P08 · Access & Venue (2 of 3)

**10 screens · 47 operations · 69 schemas · 19 permissions**

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

- **Every control that can be refused must be gated.** 19 permissions apply here:
  `AI_USE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ASSET_MANAGE, ASSET_VIEW, AUDIT_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, ORDER_MODIFY, ORDER_VIEW, PRODUCT_VIEW`…. A control nobody can use must say so,
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
| `BO-034` | Scan Activity | C | 7 | 10 | 6 | 8 | 0 | 0 | — | notStarted (generated) |
| `BO-035` | Override Audit | C | 7 | 17 | 6 | 8 | 0 | 0 | — | notStarted (generated) |
| `BO-038` | Reconciliation Queue | C | 3 | 20 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-069` | Asset Register | A | 42 | 22 | 6 | 23 | 3 | 0 | — | notStarted (generated) |
| `BO-071` | Planned Maintenance | D | 21 | 21 | 6 | 5 | 2 | 2 | — | notStarted (generated) |
| `BO-072` | Incident Log | D | 35 | 22 | 6 | 10 | 0 | 0 | — | notStarted (generated) |
| `BO-092` | Venue Maps | A | 14 | 14 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-093` | Map Import & Labelling | A | 89 | 57 | 6 | 6 | 3 | 0 | — | notStarted (generated) |
| `BO-094` | Map Editor & Publish | A | 67 | 49 | 5 | 14 | 3 | 0 | — | notStarted (generated) |
| `BO-095` | Resources | D | 27 | 13 | 6 | 19 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-038, BO-092 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-034` Scan Activity

**See what the gates have been doing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block C · task VM-BO-034 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/scan-activity` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Sync, validate, group-validate, override and the offline package are workstation-scoped scanner operations the contract refuses (403) for a back-office browser … Removed 2 October 2026 (CHG-WIR-001): Sync, validate, group-validate, override and the offline package are workstation-scoped scanner operations the contract refuses (403) for a back-office browser … Removed 2 October 2026 (CHG-WIR-001): Sync, validate, group-validate, override and the offline package are workstation-scoped scanner operations the contract refuses (403) for a back-office browser …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The gate log for the venue: every scan with when, where, what was presented, the outcome and the reason, and overrides as their own rows linked to the denial they overrode. A duty manager uses it to answer "what happened at Gate 3 at 10:40" and "show me every scan of this ticket". The one thing to get right: it is a read-only investigation screen; it never scans, validates or syncs.

**Known correction pending (do not draw the wrong version)**

- **Filters are free-text id fields (Access point id, Ticket id, Outcome)** Why: Ids are not typed by people; outcome is a closed set. *(source: contracts/spine/access.yaml#/components/schemas/ScanOutcome; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Action bar carries Sync scans, Validate access, Validate group access, Override access and a scanTarget, plus getOfflinePackage (CHG-WIR-001); Navigation exit to BO-001 Queue Directory (inferred) (CHG-WIR-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Access point picker (tree by park and zone, not an id text box), ticket number or media code search (also by scanning with a handheld into the field), outcome chips Admitted / Denied / Overridden, deny reason multi-select with VO-R06 labels, direction, date-time range defaulting to today in venue time. *(source: contracts/spine/access.yaml#listScans)*

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected scan event** (detail panel, from `listScans`): **An override is its own row** (decided 28 September, audit R228): outcome `overridden`, `operatorPrincipalId` is the supervisor who overrode, and `overridesScanId` links it to the denied scan, which is never updated. Selecting either row shows the other.

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | produces a document or message: Read-only validity check without admitting |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan table**: Time (to the second), access point and direction, ticket number and product, media type icon, outcome badge (green Admitted, red Denied, amber Overridden), reason label, operator name, device name, Recorded offline flag with sync time where the scan was journalled. Live-updating at the top with cursor paging (VO-R12). *(source: contracts/spine/access.yaml#listScans / MATRIX 3.1.6 / DI-065)*
- **Selected scan**: Detail with the ticket's other scans that day as a mini timeline; an override row shows "Overrode denial at 10:41 - Already used" with the supervisor and reason, and the denial row links to its override. *(source: contracts/spine/access.yaml#overrideAccess)*
- **Totals strip**: Admitted, denied, overridden counts for the filter, and admitted guests (sum of admitted counts, since one group scan admits several). *(source: MATRIX 3.2.54 / contracts/spine/access.yaml#/components/schemas/ValidationResult)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Look up ticket**: Opens the ticket's validity and full history read-only (no scan created). *(source: contracts/spine/access.yaml#lookupTicket)*
- **Export**: CSV of the filtered rows; not in the contract, draw greyed unless reporting export is bound. *(source: designer default)*

**Data it reads**: `listScans` (onLoad, List scan events)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scan activity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scan activity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scan activity yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the scan activity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied |

#### Edge cases to draw

- **Late offline sync**: Rows arrive with an old time; mark them "Synced 14:02, scanned 10:40" so the order is understood. *(source: DI-065 / F06 step 6)*
- **Viewer without venue report permission**: No-access state naming it (VO-R08). *(source: contracts/spine/access.yaml#listScans)*

#### Consistency with other screens

- Match `BO-035`: Same table; BO-035 is this screen filtered to overrides (consolidate per VO-R14).
- Match `BO-226`: Ticket lookup on the back office shows the same history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scans:
- time: '10:40:12'
  point: Main Plaza Gate 2 - Entry
  ticket: VT0010 Aqua Park Day Pass
  media: QR
  outcome: Denied
  reason: Already used (09:58, Gate 1)
  operator: Rahul Menon
- time: '10:41:03'
  point: Main Plaza Gate 2 - Entry
  ticket: VT0010
  outcome: Overridden
  reason: Guest had stroller, turnstile re-locked
  operator: Fatima Al Hashimi
- time: '10:42:55'
  point: North Entry
  ticket: VT0512 School Group (30)
  outcome: Admitted
  admitted: 28
  operator: Maria Santos
```

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-034` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-035` Override Audit

**Review every admission that broke a rule.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block C · task VM-BO-035 |
| Who uses it | venue staff holding `AUDIT_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (1 read, 2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/override-audit` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): An audit screen performs none of override, validate, group-validate or sync; the scanner operations are refused for a back-office session, and overriding belongs … Removed 2 October 2026 (CHG-WIR-001): An audit screen performs none of override, validate, group-validate or sync; the scanner operations are refused for a back-office session, and overriding belongs … Removed 2 October 2026 (CHG-WIR-001): An audit screen performs none of override, validate, group-validate or sync; the scanner operations are refused for a back-office session, and overriding belongs …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Every admission that broke a rule: each override with the denial it overrode, who overrode it, the justification and the gate, for the duty manager and auditors after an incident. The one thing to get right: the denial and the override are two rows that must be read together, and patterns (one supervisor, one gate, one reason) must stand out.

**Fixed on main** (the package already carries these; draw what it says): Override access, Validate access, Validate group access and Sync scans buttons, scanTarget and the offline package panel (CHG-WIR-001); Navigation exit to BO-001 Queue Directory (inferred) (CHG-WIR-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Action | text field | — | — | `listAuditRecords` ?action |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| From | date and time picker | — | — | `listAuditRecords` ?from |
| To | date and time picker | — | — | `listAuditRecords` ?to |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Date range (default last 7 days), supervisor, access point, original deny reason; outcome is fixed to Overridden. *(source: contracts/spine/access.yaml#listScans)*

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**Every audit** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |

**The selected scan event** (detail panel, from `listScans`): **An override is its own row** (decided 28 September, audit R228): outcome `overridden`, `operatorPrincipalId` is the supervisor who overrode, and `overridesScanId` links it to the denied scan, which is never updated. Selecting either row shows the other.

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | produces a document or message: Read-only validity check without admitting |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Override list**: One line per override: time, gate, ticket, original denial reason (VO-R06 label), overriding supervisor, justification text, minutes between denial and override. Group-by toggle for supervisor or gate with counts. *(source: contracts/spine/access.yaml#overrideAccess / DI-649)*
- **Audit trail**: The audit records for the same override (who viewed, who exported) appear in the detail, read-only. *(source: contracts/spine/tenancy.yaml#listAuditRecords)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open ticket history**: Read-only lookup of the ticket. *(source: contracts/spine/access.yaml#lookupTicket)*

**Data it reads**: `listScans` (onLoad, List scan events); `listAuditRecords` (onLoad, Who did what, where, and when)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The override audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the override audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No override audit yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the override audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied |

#### Edge cases to draw

- **Override recorded offline**: Shows "Recorded offline at 10:41, synced 11:05". *(source: contracts/spine/access.yaml#overrideAccess / DI-065)*

#### Consistency with other screens

- Match `BO-034`: Same row design and labels; consider one screen with an Overrides tab (VO-R14).
- Match `BO-244`: Fraud board uses the same override counts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
overrides:
- time: 1 Oct 2026 10:41
  gate: Main Plaza Gate 2
  ticket: VT0010
  denial: Already used
  by: Fatima Al Hashimi
  why: Stroller, turnstile re-locked; scan history shows no entry
- time: 1 Oct 2026 15:12
  gate: North Entry
  ticket: VT0933
  denial: Wrong gate
  by: Omar Haddad
  why: North Entry used for accessible access
```

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-035` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-038` Reconciliation Queue

**Handle scans the server disagreed with.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block C · task VM-BO-038 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueues` reads the population and `getQueue` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `rejectionId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/reconciliation-queue` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Every operation bound was a ride virtual-queue operation while the purpose is scan reconciliation; the sync-rejection read and resolve action named by F06 step 6 … Removed 2 October 2026 (CHG-WIR-001): Every operation bound was a ride virtual-queue operation while the purpose is scan reconciliation; the sync-rejection read and resolve action named by F06 step 6 … Removed 2 October 2026 (CHG-WIR-001): Every operation bound was a ride virtual-queue operation while the purpose is scan reconciliation; the sync-rejection read and resolve action named by F06 step 6 …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The duty manager's queue of offline scans the server rejected after a device had already admitted the guest (sync and reconciliation): what was admitted, where and when offline, why the server disagreed, and the decision taken. It is a revenue and audit task, not a gate event. The one thing to get right: each rejection is resolved with a recorded outcome, and the list empties.

**Fixed on main** (the package already carries these; draw what it says): Every operation bound is a ride virtual-queue operation (listQueues, createQueue, callNextParties, setWaitTime, listQueueEntries) (CHG-WIR-001); listSyncRejections and resolveSyncRejection live in the orders contract (till sales), while F06 step 6 names them for scans (CHG-WIR-001); Screen sits under the Virtual Queue module (CHG-WIR-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listSyncRejections` ?workstationId |
| Kind | radio group | — | Order · Payment · Refund · Void · Scan | `listSyncRejections` ?kind |
| Resolved | toggle | — | — | `listSyncRejections` ?resolved |

**Form: Mark resolved** (modal, opened by *Mark resolved*; *Mark resolved* calls `resolveSyncRejection`, *Cancel* sends nothing)

**Collects what `resolveSyncRejection` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | segmented control | required | — | Posted · Voided · Refunded | — | `posted` — the sale was entered with `createOrder` (F33 step 8); `voided` — with `voidOrder`; `refunded` — with `createRefund`. | `resolveSyncRejection` body |
| Resolved record `resolvedRecordId` | picker: choose a resolved record | required | — | — | shows names, sends the id | The id of the order, void or refund that resolution produced. | `resolveSyncRejection` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveSyncRejection` body |

Errors to draw in the form: 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Refused on replay** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Type | text | The problem type URI, `https://api.ticvai.com/problems/<slug>`. The slug is one of the shared types in `x-ticvai-problem-types` on this … |
| Title | text | — |
| Status | 1,234 | — |
| Detail | text | — |
| Instance | text | — |
| Trace | text | — |
| Errors | list or chips (count when long) | — |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolution | chip: Posted, Voided, Refunded | What `resolveSyncRejection` recorded. Null while the rejection waits. |
| Resolved record | the name it points at, never the id | The order, void or refund the resolution produced — what stops the entry being posted twice. |
| Next cursor | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Mark resolved (secondary button) | `resolveSyncRejection` POST `/sync/rejections/{rejectionId}/resolve` | ResolveSyncRejectionRequest | SyncRejection | 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rejections**: Device, access point, scanned at (offline, device time) and synced at, ticket, the server's reason (VO-R06 labels, e.g. Already used at 09:58 Gate 1), age; oldest first. *(source: F06 step 6 / DI-065)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resolve**: Record the outcome (e.g. accepted as genuine, guest charged, fraud suspected, blacklisted) with a note. *(source: contracts/spine/orders.yaml#resolveSyncRejection / F06 step 6)*

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused on replay)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation queue yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the reconciliation queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `resolveSyncRejection`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already resolved, differently (`alreadyResolved`). (OrderRefusedProblem) |

#### Edge cases to draw

- **Same ticket rejected at several gates**: Grouped under the ticket with a fraud hint. *(source: designer default)*

#### Consistency with other screens

- Match `SCN-014`: The scanner shows the same rejections after sync; the manager resolves them here.
- Match `BO-034`: Resolved rows link to the scan in Scan Activity.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rejections:
- device: Handheld HH-07
  point: North Entry
  scanned: 10:12 (offline)
  synced: '10:40'
  ticket: VT0933
  reason: Already used at 09:58, Main Plaza Gate 1
```

#### Permissions

- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `resolveSyncRejection` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `resolveSyncRejection`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-038` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Mark resolved.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-069` Asset Register

**Know what equipment exists and where.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `maintenance` module |
| Block | Block A · ticket #28667 (VM-BO-069) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAssets` reads the population and `getAsset` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `assetId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/asset-register` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): recordGamePlay and syncGamePlays are device-audience operations and game configuration belongs to the games boards (BO-395); keep only the asset register … Removed 2 October 2026 (CHG-WIR-001): recordGamePlay and syncGamePlays are device-audience operations and game configuration belongs to the games boards (BO-395); keep only the asset register … Removed 2 October 2026 (CHG-WIR-001): recordGamePlay and syncGamePlays are device-audience operations and game configuration belongs to the games boards (BO-395); keep only the asset register …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The venue's asset register: every ride, turnstile, plant item, vehicle and IT device with its criticality, status, warranty, documents and full history, and the fault priority override that says "if this goes down, raise this priority". Taking an asset out of service closes the loop into operations (ride shown closed, access point blocked, product stops selling). The one thing to get right: status changes are deliberate, reasoned acts, and return to service requires a completed inspection where the asset demands it.

**Fixed on main** (the package already carries these; draw what it says): Games operations (listGames, updateGame, recordGamePlay, syncGamePlays) bound on the asset register (CHG-WIR-001); Filters are id text fields (Venue id, Category id, Status) (CHG-SBO-009); Duplicate of BO-031 (CHG-WIR-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | picker: choose a category | optional | — | — | shows names, sends the id | Asset categories by name. | `Asset.categoryId` |
| Status | select | optional | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | — | Asset statuses in words. | `Asset.status` |
| Maintenance due | toggle | optional | — | — | — | Sends `?maintenanceDue=` to `listAssets`. | `listAssets` ?maintenanceDue |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |
| Fault priority override | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | **"If this goes down, raise this priority"** (decided 17 September, M17-01). A fault raised on this asset takes this priority instead of the venue's score. Empty means the score decides. | `Asset.priorityOverride` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |

**Form: Create asset** (modal, opened by *Create asset*; *Create asset* calls `createAsset`, *Cancel* sends nothing)

**Collects what `createAsset` sends before it is called.** Required: `assetTag`, `name`, `venueId`, `criticality`. Optional: `categoryId`, `locationDescription`, `manufacturer`, `model`, `serialNumber`, `commissionedAt`, `warrantyExpiresAt`, `supplierId`, `linkedProductIds`, `linkedAccessPointId`, `requiresInspectionToReturn`, `documents` and 1 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Asset tag `assetTag` | text field | required | — | max length 64 | — | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. | `createAsset` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAsset` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createAsset` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createAsset` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `createAsset` body |
| Criticality `criticality` | radio group | required | — | Safety critical · Revenue critical · Standard · Low | — | — | `createAsset` body |
| Priority override `priorityOverride` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | "If this device goes down, raise this priority" (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. | `createAsset` body |
| Manufacturer `manufacturer` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Model `model` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Serial number `serialNumber` | text field | optional | — | max length 128 | — | — | `createAsset` body |
| Commissioned at `commissionedAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAsset` body |
| Warranty expires at `warrantyExpiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAsset` body |
| Supplier `supplierId` | picker: choose a supplier | optional | — | — | shows names, sends the id | — | `createAsset` body |
| Linked products `linkedProductIds` | multi-picker: choose linked products | optional | — | — | — | Products this asset delivers. A fault here can stop them selling. | `createAsset` body |
| Linked access point `linkedAccessPointId` | picker: choose a linked access point | optional | — | — | shows names, sends the id | Access point this asset controls. Out of service blocks it. | `createAsset` body |
| Requires inspection to return `requiresInspectionToReturn` | toggle | optional | off | — | — | True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe. | `createAsset` body |
| Documents `documents` | repeatable rows | optional | — | — | — | Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from. | `createAsset` body |
| Ref `documents[].ref` | text field | required | — | — | — | The document in the media store. | `createAsset` body |
| Name `documents[].name` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Kind `documents[].kind` | select | required | — | Manual · Sop · Certificate · Warranty · Drawing · Risk assessment | — | — | `createAsset` body |
| Document refs `documentRefs` | list of values (chips) | optional | — | — | — | The refs alone, kept for callers that predate `documents`. Each ref sent here is stored as an `asset_document` row with no name and no kind. | `createAsset` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Save asset status** (modal, opened by *Save asset status*; *Save asset status* calls `setAssetStatus`, *Cancel* sends nothing)

**Collects what `setAssetStatus` sends before it is called.** Required: `status`, `reason`, `recordedAt`. Optional: `inspectionId`, `raiseWorkOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | — | — | `setAssetStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `setAssetStatus` body |
| Inspection `inspectionId` | picker: choose an inspection | optional | — | — | shows names, sends the id | Required for return to service where the asset demands it. | `setAssetStatus` body |
| Raise work order `raiseWorkOrder` | toggle | optional | off | — | — | — | `setAssetStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setAssetStatus` body |

Errors to draw in the form: 409 Return to service attempted without the inspection this asset category requires.

**Form: Save asset** (modal, opened by *Save asset*; *Save asset* calls `updateAsset`, *Cancel* sends nothing)

**Collects what `updateAsset` sends before it is called.** Nothing in the body is required. Optional: `name`, `locationDescription`, `categoryId`, `warrantyExpiresAt`, `supplierId`, `documents`, `documentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAsset` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `updateAsset` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateAsset` body |
| Warranty expires at `warrantyExpiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAsset` body |
| Supplier `supplierId` | picker: choose a supplier | optional | — | — | shows names, sends the id | — | `updateAsset` body |
| Priority override `priorityOverride` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | See `Asset.priorityOverride` (M17-01, 29 September). Null clears it. | `updateAsset` body |
| Documents `documents` | repeatable rows | optional | — | — | — | Replaces the asset's documents. One `asset_document` row each. | `updateAsset` body |
| Ref `documents[].ref` | text field | required | — | — | — | The document in the media store. | `updateAsset` body |
| Name `documents[].name` | text field | optional | — | max length 200 | — | — | `updateAsset` body |
| Kind `documents[].kind` | select | required | — | Manual · Sop · Certificate · Warranty · Drawing · Risk assessment | — | — | `updateAsset` body |
| Document refs `documentRefs` | list of values (chips) | optional | — | — | — | The refs alone, kept for callers that predate `documents`. Each becomes a document with no name and no kind. | `updateAsset` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **assetTag**: Unique per venue (max 64); duplicate refused with the existing asset named; printed as a QR label. *(source: contracts/satellite/maintenance.yaml#createAsset)*
- **criticality**: Safety critical / Revenue critical / Standard / Low, as a coloured select; Safety critical defaults "Inspection required to return to service" on. *(source: contracts/satellite/maintenance.yaml#createAsset)*
- **Fault priority override**: Optional select of the work-order priorities (Low, Normal, High, Urgent, Emergency) with the hint "If this asset goes down, raise this priority"; empty means the venue's scoring applies. *(source: DI-909 / DI-923 / contracts/satellite/maintenance.yaml#updateAsset)*
- **Links**: Linked products (a fault can stop them selling) and linked access point (out of service blocks it), as pickers. *(source: contracts/satellite/maintenance.yaml#createAsset)*
- **Documents**: Upload with a name and kind (Manual, SOP, Certificate, Warranty, Drawing, Risk assessment); replaces the list as a whole on save. *(source: contracts/satellite/maintenance.yaml#updateAsset / MATRIX 17.1.6)*
- **Status change**: In service / Out of service / Under maintenance / Awaiting parts / Retired / Disposed with a required reason; returning to In service asks for the inspection when the asset requires one; optional "Raise a work order". *(source: contracts/satellite/maintenance.yaml#setAssetStatus)*

#### Outputs: what the screen shows and produces

**Shown**

**Every asset** (data table, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Location description | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |

**The selected asset** (detail panel, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Location description | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Manufacturer | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |

**The asset history entry** (detail panel, from `getAssetHistory`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Work order, Inspection, Incident, Status change, Part replaced, Plan completed | — |
| Reference | the name it points at, never the id | The source row's id: a work order, inspection or incident, or an `asset_status_change` id. |
| Summary | text | — |
| Principal | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |

**The asset** (detail panel, from `getAsset`)

| Shows | Format | Notes |
|---|---|---|
| Open work orders | list or chips (count when long) | — |
| Maintenance plans | list or chips (count when long) | — |
| Documents | list or chips (count when long) | Manuals, procedures, certificates. What a technician needs on site. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create asset (primary button) | `createAsset` POST `/assets` | CreateAssetRequest | Asset | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Lookup asset (secondary button) | `lookupAsset` GET `/assets/lookup` | — | AssetDetail | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save asset status (secondary button) | `setAssetStatus` PUT `/assets/{assetId}/status` | SetAssetStatusRequest | AssetStatusResult | 409 Return to service attempted without the inspection this asset category requires. | opens modal first |
| Save asset (secondary button) | `updateAsset` PATCH `/assets/{assetId}` | inline | Asset | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Register**: Tag, name, category, location, criticality, status chip, warranty expiry (amber within 60 days), maintenance due flag, open work orders count; filter by category per team (DI-908). *(source: contracts/satellite/maintenance.yaml#listAssets / DI-908)*
- **Asset 360**: As BO-031 summary - documents, warranty, lifecycle history in sequence, location view. *(source: DI-910)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan tag**: Opens the asset directly (lookup by tag or serial). *(source: contracts/satellite/maintenance.yaml#lookupAsset)*
- **Take out of service**: Confirm names what it stops (ride on the map, Gate 2 access point, 3 products) - per VO-R16. *(source: contracts/satellite/maintenance.yaml#setAssetStatus)*

**Data it reads**: `listAssets` (onLoad, List assets)

**Where the user goes next**

- → `BO-070` Work Orders: *Work Orders*; carries `workOrderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset register list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset register untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset register yet. Offers Create asset (`createAsset`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, categoryId, status, maintenanceDue and the asset register are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ASSET_VIEW`, which `listAssets` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_MANAGE` for `createAsset`, `setAssetStatus`, `updateAsset`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Return to service attempted without the inspection this asset category requires. |

#### Edge cases to draw

- **Return to service without an inspection on an asset that needs one**: Refused with "Complete the inspection first" and a link to start it. *(source: contracts/satellite/maintenance.yaml#setAssetStatus)*
- **Asset retired with open work orders**: Warn and list them. *(source: designer default)*

#### Consistency with other screens

- Match `BO-070`: Priority source shown on work orders (Scored / Asset override / Manual) refers back to this override.
- Match `BO-394`: Games link to assets (assetId); game configuration stays in the games module.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
assets:
- tag: AP-RIDE-0007
  name: Falcon Coaster
  category: Rides
  location: Adventure Zone, Bay 3
  criticality: Safety critical
  override: Emergency
  status: In service
  warranty: 31 Mar 2027
- tag: AP-GATE-0102
  name: Main Plaza Gate 2 turnstile
  category: Access control
  criticality: Revenue critical
  status: Under maintenance
  linkedAccessPoint: Main Plaza Gate 2
- tag: AP-IT-0331
  name: Receipt printer TM-T88VII (Retail 1)
  category: IT
  criticality: Standard
  status: In service
```

#### Permissions

- `listAssets` → `ASSET_VIEW` (read) · staff
- `getAsset` → `ASSET_VIEW` (read) · staff
- `createAsset` → `ASSET_MANAGE` (configure) · staff
- `getAssetHistory` → `ASSET_VIEW` (read) · staff
- `lookupAsset` → `ASSET_VIEW` (read) · staff
- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff
- `updateAsset` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ASSET_VIEW`, which `listAssets` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_MANAGE` for `createAsset`, `setAssetStatus`, `updateAsset`.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.1.6 | Asset Documentation - System shall maintain manuals and technical documents. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 17.5.10 | Safety Documentation - System shall support safety document management. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 17.1.1 | Asset Master - System shall support centralized asset management. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.2 | Asset Categories - System shall support asset categorization. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.3 | Asset Location Management - System shall maintain asset locations. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.5 | Asset Warranty Management - System shall maintain warranty information. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 16.5.27 | Maintenance History - System shall maintain maintenance history. | Device Management | CONTRACTED | `getAssetHistory` |
| 17.1.8 | Asset History - System shall maintain complete asset history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 17.3.7 | Service History - System shall maintain service history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 18.3.4 | Asset History - Users shall view maintenance history. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.5 | Asset Documentation - Users shall access manuals and documents. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.1 | QR Asset Scanning - Users shall scan asset QR codes. | Employee Mobile App & AI Assistant | CONTRACTED | `lookupAsset` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- A 360-degree asset view, searchable via QR code, consolidates all asset details: attached documentation (installation manuals, wiring diagrams, safety inspection reports), warranty period and full lifecycle history (installed, maintained, operational, upcoming maintenance); a location view shows where each asset physically sits. *(client request · MoM 17 Sep 2026, 4.1 Asset Registry & Classification · DI-910)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-069` · status **notStarted** · provenance generated
- Flow F12 *Asset fails and closes a queue*, step 5: Asset returns to service → The queue reopens and the guest app offers it again
- Flow F12 branch at step 5 (requiresStaff): when Queue does not reopen after the asset returns, The cascade failed. `maintenance.assetReturnedToService` has two critical consumers for this reason — a ride verified and back in service whose queue never reopened is a closed attraction nobody …

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create asset, Lookup asset, Save asset status, Save asset.
- [ ] Every transition is wired: `BO-070`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-071` Planned Maintenance

**Schedule the work that stops the emergencies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `maintenance` module |
| Block | Block D · task VM-BO-071 |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMaintenancePlans` reads the population and `getDueMaintenance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `planId` (navigation) · cold entry: A role opened from the directory. **Permissions are set per role, not per person** — ADR-0002 makes authorisation user-driven through roles. |
| Route | `/venue-operations/planned-maintenance` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Bulk-attach residue: role permissions are tenant identity administration and have nothing to do with maintenance plans. Only createMaintenancePlan was bound …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The venue's planned (preventive) maintenance: the library of plans that say "service this every 90 days or every 500 operating hours, whichever comes first", and the due list that turns them into work orders a week ahead. A maintenance supervisor maintains plans for rides, gates, plant and IT devices, and opens each morning on what is due and overdue. The one thing to get right: plans are shown in time - a calendar of due dates with day, week and month views filtered by asset category - not only as a table of interval numbers, and overdue safety-critical work is on top.

**Known correction pending (do not draw the wrong version)**

- **No calendar although the screen places plans in time** Why: getDueMaintenance was given from, to and categoryId for calendars (M17-03); every calendar has day, week and month (per VO-R01). *(source: contracts/satellite/maintenance.yaml#getDueMaintenance / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **MaintenancePlan requires assetId while assetCategoryId "applies to every asset in the category"** Why: A category-wide plan cannot be created if one asset is mandatory; assetId should be required only when no category is given. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table and detail show id, assetId, assetCategoryId and the raw taskTemplate object; titles "Every maintenance plan", "The selected maintenance plan"** Why: Server values and placeholders (per VO-R03, VO-R12); show names and a readable interval. *(source: screens/P08-venue-back-office.yaml#BO-071; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No entry into the screen (entryFrom empty) and an inferred exit only** Why: It should be reached from the Venue Operations hub (BO-108) and the work order desk (BO-070). *(source: screens/P08-venue-back-office.yaml#BO-071 / screens/P08-venue-back-office.yaml#BO-108; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): "Save role permissions" (setRolePermissions) bound and entry parameter roleId (CHG-WIR-001); Only createMaintenancePlan is bound; no edit or suspend (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack asks for fixed-date plans (every 1 Jan and 1 Jul), a grace window (due 15 Sep plus or minus 3 days) and plan approval (Draft, Pending approval, Active, Suspended, Archived). None is in the plan. In scope?** → Drawn default accepted: Draw Active/Suspended only; show "Fixed dates" and "Grace window" greyed with "Not yet available". *(decided by Chinmay, 2026-10-02; DEC-372 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Is there a "Raise now" for a plan whose job is needed early (before an event), or must the supervisor raise a separate work order?** → Drawn default accepted: Not drawn; the due row links to New work order pre-filled from the plan. *(decided by Chinmay, 2026-10-02; DEC-373 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

**Form: Create maintenance plan** (modal, opened by *Create maintenance plan*; *Create maintenance plan* calls `createMaintenancePlan`, *Cancel* sends nothing)

**Collects what `createMaintenancePlan` sends before it is called.** Required: `id`, `name`, `assetId`, `taskTemplate`. Optional: `assetCategoryId`, `intervalDays`, `usageInterval`, `leadTimeDays`, `lastCompletedAt`, `nextDueAt`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createMaintenancePlan` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMaintenancePlan` body |
| Asset `assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createMaintenancePlan` body |
| Asset category `assetCategoryId` | picker: choose an asset category | optional | — | — | shows names, sends the id | Applies to every asset in the category rather than one. | `createMaintenancePlan` body |
| Interval days `intervalDays` | number field (days) | optional | — | — | — | Elapsed-time trigger. | `createMaintenancePlan` body |
| Usage interval `usageInterval` | number field | optional | — | — | — | Usage trigger — cycles, hours, kilometres. Whichever comes first when both are set. | `createMaintenancePlan` body |
| Lead time days `leadTimeDays` | number field (days) | optional | 7 | — | — | How far ahead the work order is generated, so parts can be ordered before the job is already late. | `createMaintenancePlan` body |
| Task template `taskTemplate` | group | required | — | — | — | — | `createMaintenancePlan` body |
| Title `taskTemplate.title` | text field | required | — | — | — | — | `createMaintenancePlan` body |
| Description `taskTemplate.description` | text area | optional | — | — | — | — | `createMaintenancePlan` body |
| Priority `taskTemplate.priority` | radio group | required | — | Low · Normal · High · Urgent · Emergency | — | — | `createMaintenancePlan` body |
| Estimated minutes `taskTemplate.estimatedMinutes` | number field (minutes) | optional | — | — | — | — | `createMaintenancePlan` body |
| Inspection template `taskTemplate.inspectionTemplateId` | picker: choose an inspection template | optional | — | — | shows names, sends the id | — | `createMaintenancePlan` body |
| Required parts `taskTemplate.requiredPartIds` | multi-picker: choose required parts | optional | — | — | — | — | `createMaintenancePlan` body |
| Last completed at `lastCompletedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createMaintenancePlan` body |
| Next due at `nextDueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createMaintenancePlan` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createMaintenancePlan` body |

Errors to draw in the form: 400 Neither an interval nor a usage trigger supplied

**Form: Change plan** (modal, opened by *Change plan*; *Change plan* calls `updateMaintenancePlan`, *Cancel* sends nothing)

**Collects what `updateMaintenancePlan` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Interval days `intervalDays` | number field (days) | optional | — | min 1 | — | — | `updateMaintenancePlan` body |
| Usage interval `usageInterval` | number field | optional | — | min 0 | — | — | `updateMaintenancePlan` body |
| Lead time days `leadTimeDays` | number field (days) | optional | — | min 0 | — | — | `updateMaintenancePlan` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMaintenancePlan` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Applies to**: Either one asset (asset picker with tag search) or a whole category ("All turnstiles - 96 assets"), chosen with a two-way switch; the count of assets covered is shown live. *(source: screens/P08-venue-back-office.yaml#BO-071 / contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **Every (interval and usage)**: A sentence builder - "Every [90] days" with presets Daily, Weekly, Monthly (30), Quarterly (90), Half-yearly (182), Annual (365), Custom; "or every [500] [operating hours]" where the unit follows the asset's usage counter; "whichever comes first" appears when both are set. At least one of the two is required; interval minimum 1, usage minimum 0 exclusive. *(source: contracts/satellite/maintenance.yaml#createMaintenancePlan / contracts/satellite/maintenance.yaml#updateMaintenancePlan / DI-902)*
- **Raise the work order ahead by**: "[7] days before it is due, so parts can be ordered" - whole days, 0 allowed, default 7. *(source: screens/P08-venue-back-office.yaml#BO-071 / contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **The job (task template)**: Work order title (required), description, priority (planned work takes this priority; it is not scored), estimated duration in minutes, checklist (picker of inspection templates for the category, "Create a checklist" link to the template builder), parts usually needed (inventory item picker) - shown as the work order the plan will raise. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan / DI-923)*
- **Active**: A Suspend switch with a reason, not a bare checkbox; a suspended plan raises nothing and is greyed in the list and calendar. *(source: screens/P08-venue-back-office.yaml#BO-071 / contracts/satellite/maintenance.yaml#updateMaintenancePlan)*

#### Outputs: what the screen shows and produces

**Shown**

**Every maintenance plan** (data table, from `listMaintenancePlans`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Interval days | 1,234 | Elapsed-time trigger. |
| Usage interval | 1,234.5 | Usage trigger — cycles, hours, kilometres. Whichever comes first when both are set. |
| Lead time days | 1,234 | How far ahead the work order is generated, so parts can be ordered before the job is already late. |
| Last completed at | 1 Oct 2026, 14:30 | — |
| Next due at | 1 Oct 2026, 14:30 | — |

**The selected maintenance plan** (detail panel, from `listMaintenancePlans`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Interval days | 1,234 | Elapsed-time trigger. |
| Usage interval | 1,234.5 | Usage trigger — cycles, hours, kilometres. Whichever comes first when both are set. |
| Lead time days | 1,234 | How far ahead the work order is generated, so parts can be ordered before the job is already late. |
| Task template | grouped details | — |
| Last completed at | 1 Oct 2026, 14:30 | — |
| Next due at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |

**The due maintenance task** (detail panel, from `getDueMaintenance`)

| Shows | Format | Notes |
|---|---|---|
| Plan name | text | — |
| Asset name | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Due at | 1 Oct 2026, 14:30 | — |
| Is overdue | yes / no (icon or chip) | — |
| Days overdue | 1,234 | — |
| Triggered by | chip: Interval, Usage | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create maintenance plan (primary button) | `createMaintenancePlan` POST `/maintenance-plans` | MaintenancePlan | MaintenancePlan | 400 Neither an interval nor a usage trigger supplied | opens modal first |
| Change plan (secondary button) | `updateMaintenancePlan` PATCH `/maintenance-plans/{planId}` | inline | MaintenancePlan | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Plan library**: Columns - Plan, Applies to ("Falcon Coaster" or "All turnstiles (96)"), Every ("90 days or 500 h"), Lead time, Last done, Next due (amber inside the lead time, red overdue), Status. Never id, assetId, assetCategoryId or a raw taskTemplate object. *(source: contracts/satellite/maintenance.yaml#listMaintenancePlans)*
- **Due and overdue**: The morning view - overdue safety-critical first, then by due date; each row "Due 15 Oct - triggered by usage" with the generated work order number and its status, or "No work order yet". *(source: contracts/satellite/maintenance.yaml#getDueMaintenance / MATRIX 17.2.4)*
- **Calendar**: A List / Calendar toggle. Calendar has Day (hours from the venue day start), Week, Month and Agenda views, an asset-category filter so the IT team sees turnstiles, printers and POS only, and cards coloured Scheduled, Due soon, Overdue, Completed, Suspended. *(source: DI-907 / DI-908 / contracts/satellite/maintenance.yaml#getDueMaintenance)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New plan**: Opens the editor empty with lead time 7 and Active on; no id field. Saving a plan whose first due date is inside the lead time says "A work order will be raised today". *(source: contracts/satellite/maintenance.yaml#createMaintenancePlan)*
- **Save changes**: Sends only the changed fields (PATCH); the confirm says how many assets and future occurrences are affected. *(source: contracts/satellite/maintenance.yaml#updateMaintenancePlan)*
- **Open work order**: From a due row, opens BO-070 at that work order. *(source: screens/P08-venue-back-office.yaml#BO-071)*

**Data it reads**: `listMaintenancePlans` (onLoad, List planned maintenance schedules); `getDueMaintenance` (onLoad, Planned tasks due or overdue)

**Where the user goes next**

- → `BO-070` Work Orders: *Work Orders*; carries `workOrderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The planned maintenance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the planned maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No planned maintenance yet. Offers Create maintenance plan (`createMaintenancePlan`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMaintenancePlans` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ASSET_VIEW`, which `listMaintenancePlans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_MANAGE` for `createMaintenancePlan`, `updateMaintenancePlan`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither an interval nor a usage trigger supplied |

#### Edge cases to draw

- **Usage-based plan on an asset that has no usage counter**: Warn "Falcon Coaster has no cycle counter - this plan will only trigger by days" before save. *(source: contracts/satellite/maintenance.yaml#/components/schemas/Asset / designer default)*
- **Category plan and a new asset added to the category**: The asset is covered from its commissioning date; the plan's asset count rises. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **Viewer without ASSET_MANAGE**: Library and calendar read-only; New plan and Save disabled with "Needs asset management rights" (per VO-R08). *(source: contracts/satellite/maintenance.yaml#createMaintenancePlan)*

#### Consistency with other screens

- Match `BO-575`: The rental board's service-plan configuration edits the same MaintenancePlan; one editor, rental products shown as a category (per VO-R14).
- Match `BO-576`: Same calendar component, views and category filter.
- Match `BO-070`: Generated work orders appear there with kind Planned and the plan named as source.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plans:
- plan: Turnstile quarterly service
  appliesTo: All turnstiles - Main Plaza (12)
  every: 90 days
  leadTime: 7 days
  nextDue: 15 Oct 2026
  status: Active
- plan: Falcon Coaster wheel assembly check
  appliesTo: Falcon Coaster
  every: 30 days or 10,000 cycles, whichever first
  lastDone: 12 Sep 2026
  nextDue: 9 Oct 2026 (8,420 cycles used)
  status: Active
- plan: Receipt printer clean and test
  appliesTo: All IT - receipt printers (15)
  every: Half-yearly
  status: Active
- plan: Wave Rider pump seasonal overhaul
  appliesTo: Wave Rider pump P-08
  every: Annual
  status: Suspended (pump replaced Aug 2026)
```

#### Permissions

- `listMaintenancePlans` → `ASSET_VIEW` (read) · staff
- `createMaintenancePlan` → `ASSET_MANAGE` (configure) · staff
- `getDueMaintenance` → `ASSET_VIEW` (read) · staff
- `updateMaintenancePlan` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ASSET_VIEW`, which `listMaintenancePlans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_MANAGE` for `createMaintenancePlan`, `updateMaintenancePlan`.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.24 | Preventive Maintenance - System shall support preventive maintenance schedules. | Device Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.1 | Maintenance Plans - System shall support preventive maintenance plans. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.2 | Maintenance Schedules - System shall support maintenance scheduling. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.3 | Maintenance Frequencies - System shall support daily, weekly, monthly and annual schedules. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-071` · status **notStarted** · provenance generated
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-071?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create maintenance plan, Change plan.
- [ ] Every transition is wired: `BO-070`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-072` Incident Log

**Record what happened, while it is fresh.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `maintenance` module |
| Block | Block D · task VM-BO-072 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW` (1 configure, 1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listIncidents` reads the population and `getIncident` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/incident-log` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The incident log: anything that happened to a person or a place (guest or staff injury, near miss, property damage, equipment failure, security, fire or evacuation, food safety, environmental), reported by any staff member while it is fresh, investigated, escalated and closed with findings. An incident is not a work order; it may raise one. The one thing to get right: reportable incidents show their statutory notification deadline as a countdown until the authority notification is recorded.

**Known correction pending (do not draw the wrong version)**

- **Filters Severity and Status are free text fields** Why: Both are closed sets. *(source: contracts/satellite/maintenance.yaml#listIncidents; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation exit to BO-070 is inferred and carries nothing** Why: Raise-a-work-order from an incident should carry the incident and asset. *(source: screens/P08-venue-back-office.yaml#BO-072; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Form: Report incident** (modal, opened by *Report incident*; *Report incident* calls `reportIncident`, *Cancel* sends nothing)

**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Kind `kind` | select | required | — | Guest injury · Staff injury · Near miss · Property damage · Equipment failure · Security incident · Fire or evacuation · Food safety · Environmental · Other | — | — | `reportIncident` body |
| Severity `severity` | radio group | required | — | Near miss · Minor · Moderate · Major · Critical | — | — | `reportIncident` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `reportIncident` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `reportIncident` body |
| Description `description` | text area | required | — | min length 3; max length 10000 | — | — | `reportIncident` body |
| Involved subjects `involvedSubjectIds` | multi-picker: choose involved subjects | optional | — | — | — | Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact. | `reportIncident` body |
| Involved staff principals `involvedStaffPrincipalIds` | multi-picker: choose involved staff principals | optional | — | — | — | — | `reportIncident` body |
| Witness count `witnessCount` | number field | optional | — | — | — | — | `reportIncident` body |
| First aid given `firstAidGiven` | toggle | optional | off | — | — | — | `reportIncident` body |
| Emergency services called `emergencyServicesCalled` | toggle | optional | off | — | — | — | `reportIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `reportIncident` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |

Errors to draw in the form: 400 Validation failed

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |
| Escalate `escalate` | group | optional | — | — | — | Escalate an incident under investigation (the optional Escalated step; CHG-RUL-011). | `updateIncident` body |
| To principal `escalate.toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `updateIncident` body |
| Reason `escalate.reason` | text area | required | — | min length 3; max length 1000 | — | — | `updateIncident` body |
| Reason `reason` | text area | optional | — | min length 3; max length 1000 | — | Why the status changes. Required to reopen a closed incident (back to `underInvestigation`) and to close a `reported` one straight away (CHG-RUL-011). | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Report**: Kind and severity (Near miss, Minor, Moderate, Major, Critical) as chips; when it happened (venue time, defaults now); where (asset or location); description; first aid given, emergency services called, witnesses; photos first. People involved are referenced, not typed as personal details here. *(source: contracts/satellite/maintenance.yaml#reportIncident)*
- **Investigation**: Status (Reported, Under investigation, Action required, Closed), assignee, an investigation note that appends to the history (never overwrites), root cause, corrective actions. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Authority notification**: Authority, reference, notified at, by whom, attachments; each notification is a new row. *(source: contracts/satellite/maintenance.yaml#recordAuthorityNotification)*

#### Outputs: what the screen shows and produces

**Shown**

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Occurred at | 1 Oct 2026, 14:30 | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Occurred at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Report incident (primary button) | `reportIncident` POST `/incidents` | ReportIncidentRequest | Incident | 400 Validation failed | opens modal first |
| Record authority notification (secondary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Log**: Incident number, kind, severity badge, status, location, reported at, and for reportable ones "Notify authority by 14:30 (2 h 05 min left)" in red until notified. *(source: contracts/satellite/maintenance.yaml#listIncidents)*
- **Original report**: Shown read-only at the top; investigation entries below as a timeline. *(source: contracts/satellite/maintenance.yaml#updateIncident)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Close incident**: Requires findings and, where a corrective action was identified, a linked work order. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Raise work order from incident**: Opens the work-order form pre-filled with the asset and location. *(source: contracts/satellite/maintenance.yaml#reportIncident)*

**Data it reads**: `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `BO-070` Work Orders: *Work Orders*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incident log list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incident log untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No incident log yet. Offers Record authority notification (`recordAuthorityNotification`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the incident log are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `recordAuthorityNotification`, `updateIncident`; `INCIDENT_REPORT` for `reportIncident`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 400 Validation failed; 409 The incident is not reportable (`isReportable` false, audit R106 (6)).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a … |

#### Edge cases to draw

- **Notification attempted on a non-reportable incident**: Refused; the action is hidden unless the incident is reportable. *(source: contracts/satellite/maintenance.yaml#recordAuthorityNotification)*

#### Consistency with other screens

- Match `EMP-026`: Staff App incident report uses the same kinds and severities.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incidents:
- false: INC-2026-0213
  kind: Guest injury
  severity: Moderate
  where: Wave Rider exit stairs
  reported: 1 Oct 2026 11:05
  reportable: true
  notifyBy: 1 Oct 2026 14:05
- false: INC-2026-0214
  kind: Near miss
  severity: Near miss
  where: Main Plaza Gate 3
  status: Under investigation
```

#### Permissions

- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `recordAuthorityNotification`, `updateIncident`; `INCIDENT_REPORT` for `reportIncident`.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.4 | Safety Inspections - Users shall perform inspections. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.5 | Safety Checklists - Users shall complete safety checklists. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.6 | Corrective Actions - Users shall submit corrective actions. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-072` · status **notStarted** · provenance generated
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-072?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Report incident, Record authority notification, Save incident.
- [ ] Every transition is wired: `BO-070`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-092` Venue Maps

**Every map for this venue, and which is published.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `seating` module |
| Block | Block A · ticket #28077 (APP-SETUP-BO-092) |
| Who uses it | venue staff holding `VENUE_MAP_MANAGE`, `VENUE_MAP_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listVenueMaps` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-mapping/venue-maps` |

**What the spec says about it.** CF-123. **A venue may have several maps** — a park map and a floor plan per building are different maps, not layers of one, because a guest on the second floor should not be shown the ground floor toilets. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2e`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every venue map of the venue (park map, a floor per building, zones, parking) and which version guests see. A park map and a building floor are separate maps, never layers of one. The list must make draft and published, and whether a map is navigable, obvious.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listVenueMaps return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The create form asks for id and status as required fields. (CHG-SBO-010).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What image formats and sizes may tenants upload for the illustrated base map (benchmark an interactive 3D-style map)?** → Drawn default accepted: Accept PDF, SVG, DWG, DXF and raster for geometry; show a guidance panel with a placeholder recommendation until agreed. *(decided by Chinmay, 2026-10-02; DEC-103 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**Form: Create venue map** (modal, opened by *Create venue map*; *Create venue map* calls `createVenueMap`, *Cancel* sends nothing)

**Collects what `createVenueMap` sends before it is called.** Required: `name`, `venueId`. Optional: `kind`, `floorLevel`, `baseAssetId`, `baseImageAlignment`, `boundsGeoJson`. and scope are the server's; the form asks only for the map's own fields. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `status` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createVenueMap` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createVenueMap` body |
| Kind `kind` | radio group | optional | — | Park · Floor · Zone · Parking | — | — | `createVenueMap` body |
| Floor level `floorLevel` | number field | optional | — | — | — | — | `createVenueMap` body |
| Base image `baseAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The illustrated map a guest actually sees, held in `assets` like any other media. | `createVenueMap` body |
| Base image alignment `baseImageAlignment` | group | optional | — | — | — | How the illustration lines up with the geometry. They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting … | `createVenueMap` body |
| Image width px `baseImageAlignment.imageWidthPx` | number field | optional | — | — | — | — | `createVenueMap` body |
| Image height px `baseImageAlignment.imageHeightPx` | number field | optional | — | — | — | — | `createVenueMap` body |
| Anchors `baseImageAlignment.anchors` | repeatable rows | optional | — | at least 2; at most 4 | — | — | `createVenueMap` body |
| Plan x `baseImageAlignment.anchors[].planX` | number field | optional | — | — | — | — | `createVenueMap` body |
| Plan y `baseImageAlignment.anchors[].planY` | number field | optional | — | — | — | — | `createVenueMap` body |
| Image x `baseImageAlignment.anchors[].imageX` | number field | optional | — | — | — | — | `createVenueMap` body |
| Image y `baseImageAlignment.anchors[].imageY` | number field | optional | — | — | — | — | `createVenueMap` body |
| Bounds geo json `boundsGeoJson` | text field | optional | — | — | — | — | `createVenueMap` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **new map**: Only name, kind and floor level are asked; id, status and scope are the server's. The upload happens next on BO-093. *(source: contracts/satellite/venue-map.yaml#createVenueMap / F26 step 1)*

#### Outputs: what the screen shows and produces

**Shown**

**Every venue map** (data table, from `listVenueMaps`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Park, Floor, Zone, Parking | — |
| Floor level | 1,234 | — |
| Status | chip: Draft, Published, Archived | `draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value. |
| Published version | 1,234 | The `VenueMapVersion.version` guests are served. Null until the first publish. |
| Tile set ref | text | Where a base image is large enough to need zoom levels. A 12,000-pixel park map is not something a phone downloads on arrival, and a guest … |

**The selected venue map** (detail panel, from `listVenueMaps`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Park, Floor, Zone, Parking | — |
| Floor level | 1,234 | — |
| Status | chip: Draft, Published, Archived | `draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value. |
| Published version | 1,234 | The `VenueMapVersion.version` guests are served. Null until the first publish. |
| Base image alignment | grouped details | How the illustration lines up with the geometry. They are drawn at different scales by different people, and a point placed on the plan … |
| Tile set ref | text | Where a base image is large enough to need zoom levels. A 12,000-pixel park map is not something a phone downloads on arrival, and a guest … |
| Graph status | chip: Not built, Connected, Disconnected, Partial | Whether every public point can actually be reached. Computed at publish. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create venue map (primary button) | `createVenueMap` POST `/venue-maps` | VenueMap | VenueMap | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **map list**: Name, kind (Park, Floor and level, Zone, Parking), status, published version, graph status (Connected, Partial, Disconnected, Not built) and whether it is georeferenced ("guests can be located"). *(source: contracts/satellite/venue-map.yaml#createVenueMap / screens/P08-venue-back-office.yaml#BO-092)*

**Data it reads**: `listVenueMaps` (onLoad, Maps)

**Where the user goes next**

- → `BO-094` Map Editor & Publish: *Map Editor & Publish*; carries `mapId`
- → `BO-093` Map Import & Labelling: *The plan is uploaded and read*; carries `mapId`; calls `createVenueMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue maps list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue maps untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue maps yet. Offers Create venue map (`createVenueMap`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listVenueMaps` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `VENUE_MAP_VIEW`, which `listVenueMaps` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `VENUE_MAP_MANAGE` for `createVenueMap`. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-093`: Creating a map continues straight into import and labelling.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
maps:
- name: Dune Park, park map
  kind: park
  status: published
  version: 7
  graph: connected
  georeferenced: true
- name: Main Building, level 1
  kind: floor
  floorLevel: 1
  status: draft
  graph: notBuilt
```

#### Permissions

- `listVenueMaps` → `VENUE_MAP_VIEW` (read) · staff
- `createVenueMap` → `VENUE_MAP_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `VENUE_MAP_VIEW`, which `listVenueMaps` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `VENUE_MAP_MANAGE` for `createVenueMap`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-092` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2e`
- Flow F26 *A venue maps its site*, step 1: The manager creates a map. → A draft, with the kind and floor level set. Nothing is live.
- Flow F26 branch at step 1 (recoverable): when The plan is a scan or a photograph with no vector geometry., `rasterOnly` is a **warning, not an error**. The manifest still gives seats and the image still works as a map; only automatic geometry is lost. **Refusing a venue that sent everything it had is the …
- Flow F26 branch at step 1 (recoverable): when No layer matched any role., `noLayersMatched`, separated from `nothingFound` deliberately. **It almost always means a role needed a second entry or a name needed decoding**, not that the file is wrong — and `layersFound` lists …

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-092?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create venue map.
- [ ] Every transition is wired: `BO-094`, `BO-093`.
- [ ] Every gated control is gated: `VENUE_MAP_MANAGE`, `VENUE_MAP_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-093` Map Import & Labelling

**Upload a plan, check what was read, and review what the assistant suggests; on a map that carries bookable places, also read the cabanas, loungers and tables and join them to what they sell as (decided 29 September, rev 3 REV3-15 and GAP-C2).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `seating` module |
| Block | Block A · ticket #28078 (APP-SETUP-BO-093) |
| Who uses it | venue staff holding `AI_USE`, `ASSET_LIBRARY_MANAGE`, `VENUE_MAP_MANAGE`, `VENUE_MAP_VIEW` (1 operate, 2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`importVenueGeometry`, `proposeVenueLabels`, `acceptVenueLabelProposals`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `mapId` (deepLink), `jobId` (navigation), `uploadId` (navigation), `actionId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-mapping/map-import` |

**What the spec says about it.** CF-123. **Two failure modes on one screen, kept visually apart.** Extraction is deterministic and reports which layers it found; labelling is a proposal with a confidence. **A mis-parsed layer and a bad suggestion look identical if the screen blurs them**, and the operator is left saying only that the map is wrong. **Low-confidence proposals are shown, not filtered** — the shape the assistant is unsure about is the one most worth a human looking at. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **decideProposedAction bound 4 October 2026: accepting or rejecting a proposal closes it, so the open proposals that block the publish clear** (CHG-FXS-003)

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Upload a drawing, see what was read, then review what the assistant suggests each shape is. Two failure modes must stay visually apart: extraction (deterministic, reports layers found and unmapped) and labelling (a proposal with a confidence). On a map with bookable places, also read cabanas, loungers and tables and join them to what they sell as.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Plan, model or navigation file | file upload | — | — | — | — | The file being imported, uploaded before `importVenueGeometry` is called: `assets.createUpload` gives a signed URL (it refuses a GLB over 40 MB, or any file over the limit for its kind, before the … | — |
| Format | select field | — | — | — | — | Required. Four source kinds (3 October 2026, r1 additions): DWG or DXF (preferred); PDF (a vector page by its layers, a scanned page through the OCR step); PNG or JPG, with or without hand-marked … | — |
| Source ref | text field | — | — | — | — | Required. | — |
| Layer mapping | text field | — | — | — | — | — | — |
| Digit normalisation | toggle | — | — | — | — | — | — |
| Georeference | text field | — | — | — | — | — | — |
| Manifest ref | text field | — | — | — | — | — | — |
| Read text on a scanned plan (OCR) | segmented control | optional | Auto | Auto · Off | — | `ocr.mode`, on (`auto`) by default for a scanned PDF or an image; off for a dimensioned drawing whose text is noise. The text found becomes hints for the label proposals, never labels. | `VenueMapOcrOptions.mode` |
| Paths marked by hand, marker colour | colour picker | optional | — | — | #RRGGBB | `handMarkedPaths`, for a PNG, JPG or scanned PDF with the walkways drawn in marker: a tick that the paths are marked, the marker colour if known (optional) and a note on what the marks mean. | `VenueMapHandMarkedPaths.markColour` |
| Resource layer | text field | — | — | — | — | `layerMapping.resourceLayer`: the drawing layers that hold the bookable places (decided 29 September, rev 3 REV3-15). Absent, the accepted names in the venue-map input spec are matched. | — |
| Resource manifest | file upload | — | — | — | — | `resourceManifestRef`: one sheet, header on row 3, five columns (Label, Kind, Zone, Capacity, Price band), uploaded through the asset library like the drawing. **Kind is cabana, lounger, table, pitch … | — |
| Create missing resources | toggle | — | — | — | — | `createMissingResources`, **off by default**: where a manifest label has no resource with that code at this venue, create one instead of reporting `resourceCodeUnmatched`. Off, a mistyped label is a … | — |

**Form: Accept venue label proposals** (modal, opened by *Accept venue label proposals*; *Accept venue label proposals* calls `acceptVenueLabelProposals`, *Cancel* sends nothing)

**Collects what `acceptVenueLabelProposals` sends before it is called.** Required: `decisions` — one per proposal, each `accept`, `edit` or `reject` (decided 28 September, audit R275 (f)). An `edit` carries the corrected `point`; a reject writes nothing to the map. Decisions are per proposal, never all-or-nothing. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decisions `decisions` | repeatable rows | required | — | — | — | — | `acceptVenueLabelProposals` body |
| Proposal `decisions[].proposalId` | picker: choose a proposal | required | — | — | shows names, sends the id | — | `acceptVenueLabelProposals` body |
| Decision `decisions[].decision` | segmented control | required | — | Accept · Edit · Reject | — | — | `acceptVenueLabelProposals` body |
| Point `decisions[].point` | group | optional | — | — | — | 19.2.57 to 19.2.60. What a venue places on the map, and what a guest taps. | `acceptVenueLabelProposals` body |
| Kind `decisions[].point.kind` | select | required | — | Ride · Attraction · Show · Restaurant · Cafe · Shop · Kiosk · Toilet · Baby care · Prayer room · First aid · Atm … | — | A closed set, and `emergencyExit` is separate from `exit` on purpose. An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them … | `acceptVenueLabelProposals` body |
| Name `decisions[].point.name` | text field | required | — | — | — | Unique per venue (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` … | `acceptVenueLabelProposals` body |
| Name localised `decisions[].point.nameLocalised` | key and value settings | optional | — | — | — | — | `acceptVenueLabelProposals` body |
| Position `decisions[].point.position` | group | required | — | — | — | Drawing coordinates. Latitude and longitude are derived from the georeference, not stored, so a map that is re-georeferenced does not need every point moved. | `acceptVenueLabelProposals` body |
| Outlet `decisions[].point.outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | For a restaurant, cafe, shop or kiosk. Tapping it should open the menu, and that only works if the map knows which outlet it is. | `acceptVenueLabelProposals` body |
| Product `decisions[].point.productId` | picker: choose a product | optional | — | — | shows names, sends the id | For a ride or show — links to wait times and to booking. What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer` (29 September, MOB-4); this … | `acceptVenueLabelProposals` body |
| Access point `decisions[].point.accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | For an entrance or exit. This is what makes 3.2.64 work — live admission statistics drawn on the point they came from. | `acceptVenueLabelProposals` body |
| Is step free `decisions[].point.isStepFree` | toggle | optional | on | — | — | Whether the point itself can be reached without steps. The same name as `VenuePath.isStepFree`, because it is the same concept (it was `isAccessible` until the 26 September audit). | `acceptVenueLabelProposals` body |
| Opening hours `decisions[].point.openingHours` | text field | optional | — | — | — | — | `acceptVenueLabelProposals` body |
| Icon ref `decisions[].point.iconRef` | text field | optional | — | — | — | — | `acceptVenueLabelProposals` body |
| Is active `decisions[].point.isActive` | toggle | optional | on | — | — | — | `acceptVenueLabelProposals` body |
| Is navigable `decisions[].point.isNavigable` | toggle | optional | on | — | — | Whether a route may pass through it. False for a point that marks a place without being reachable — a stage a guest cannot walk onto, a zone label. | `acceptVenueLabelProposals` body |
| Is destination `decisions[].point.isDestination` | toggle | optional | on | — | — | Whether a guest may be routed *to* it, and whether it appears in a list of places. | `acceptVenueLabelProposals` body |
| Description `decisions[].point.description` | key and value settings | optional | — | — | — | What the guest reads on Item Detail (29 September, MOB-4). Keyed by locale, like `nameLocalised`. | `acceptVenueLabelProposals` body |
| Media `decisions[].point.media` | repeatable rows | optional | — | at most 12 | — | The gallery on Item Detail (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. | `acceptVenueLabelProposals` body |
| Featured offer `decisions[].point.featuredOffer` | group | optional | — | — | — | The product card on Item Detail, for every kind of point (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from … | `acceptVenueLabelProposals` body |
| Typical duration minutes `decisions[].point.typicalDurationMinutes` | number field (minutes) | optional | — | min 1; max 600 | — | How long a visit to this point usually takes, ride time and queue excluded (29 September, MOB-6). | `acceptVenueLabelProposals` body |
| Interest tags `decisions[].point.interestTags` | multi-select chips | optional | — | Thrill · Family · Kids · Water · Animals · Shows · Culture · Shopping · Dining · Relaxing · Photo · Adventure …; at most 12 | — | What a guest who says they like this would like here (29 September, MOB-6): the planner matches the guest's interests against these. | `acceptVenueLabelProposals` body |
| Cuisine tags `decisions[].point.cuisineTags` | list of values (chips) | optional | — | at most 8 | — | For dining points (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. | `acceptVenueLabelProposals` body |
| Retail tags `decisions[].point.retailTags` | list of values (chips) | optional | — | at most 8 | — | For retail points (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). | `acceptVenueLabelProposals` body |

**Sent by *Import venue geometry*** (`importVenueGeometry`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | select | required | — | Pdf plan · Svg plan · Dwg plan · Dxf plan · Raster plan · Glb model · Navigation file | — | `glbModel` and `navigationFile` added 3 October 2026 (r1 additions, ADR-0069): a GLB with its navigation file, or the navigation file alone. | `importVenueGeometry` body |
| Source ref `sourceRef` | picker: choose a source ref | required | — | — | shows names, sends the id | The drawing, as the `MediaAsset.id` from `assets.completeUpload`. Not a URL and not a storage path; the file itself is never posted through this API. | `importVenueGeometry` body |
| Navigation file ref `navigationFileRef` | picker: choose a navigation file ref | optional | — | — | shows names, sends the id | The navigation (pathway) file that goes with a GLB (ADR-0069 section 2; the `VenueNavigationFile` schema), uploaded like `sourceRef` as JSON. | `importVenueGeometry` body |
| Ocr `ocr` | group | optional | — | — | — | The OCR step (3 October 2026, r1 additions); `VenueMapOcrOptions`. | `importVenueGeometry` body |
| Mode `ocr.mode` | segmented control | optional | Auto | Auto · Off | — | `off` skips it, for a plan whose text is noise (a dimensioned drawing). | `importVenueGeometry` body |
| Languages `ocr.languages` | multi-select chips | optional | — | En · Ar | — | The scripts to read. Absent means both. | `importVenueGeometry` body |
| Hand marked paths `handMarkedPaths` | group | optional | — | — | — | A raster plan with hand-marked paths (3 October 2026, r1 additions); `VenueMapHandMarkedPaths`. | `importVenueGeometry` body |
| Mark colour `handMarkedPaths.markColour` | colour picker | optional | — | — | #RRGGBB | The marker's colour, where the operator knows it (`#E53935` for a red pen). Absent, the import looks for the strokes that differ from the printed plan. | `importVenueGeometry` body |
| Note `handMarkedPaths.note` | text area | optional | — | max length 300 | — | Anything the marks mean that the image does not say ("dashed = staff only"). | `importVenueGeometry` body |
| Layer mapping `layerMapping` | group | optional | — | — | — | Each role takes a list. A drawing office names layers by habit, not by convention, and a single string keeps one and drops the rest silently. | `importVenueGeometry` body |
| Building layer `layerMapping.buildingLayer` | list of values (chips) | optional | — | — | — | — | `importVenueGeometry` body |
| Path layer `layerMapping.pathLayer` | list of values (chips) | optional | — | — | — | Optional, and the platform derives paths without it. Where a drawing has no walkway layer — which is most drawings prepared for ticketing — walkable space is the negative space … | `importVenueGeometry` body |
| Zone layer `layerMapping.zoneLayer` | list of values (chips) | optional | — | — | — | — | `importVenueGeometry` body |
| Label layer `layerMapping.labelLayer` | list of values (chips) | optional | — | — | — | — | `importVenueGeometry` body |
| Boundary layer `layerMapping.boundaryLayer` | list of values (chips) | optional | — | — | — | — | `importVenueGeometry` body |
| Exit layer `layerMapping.exitLayer` | list of values (chips) | optional | — | — | — | — | `importVenueGeometry` body |
| Emergency exit layer `layerMapping.emergencyExitLayer` | list of values (chips) | optional | — | — | — | Separate from `exitLayer`, and drawings usually blur them. An exit is where a guest leaves; an emergency exit is where they are sent. | `importVenueGeometry` body |
| Poi layers `layerMapping.poiLayers` | group | optional | — | — | — | Where a drawing already marks toilets, first aid and the rest. Keyed by `VenuePoint.kind`. | `importVenueGeometry` body |
| Resource layer `layerMapping.resourceLayer` | list of values (chips) | optional | — | — | — | The bookable resources drawn on the plan — cabanas, loungers, tables (decided 29 September, rev 3 REV3-15). | `importVenueGeometry` body |
| Keep out layer `layerMapping.keepOutLayer` | list of values (chips) | optional | — | — | — | Water, planting, back-of-house, plant rooms. Subtracted from the walkable space along with buildings, and the difference between a usable derived path network and one that routes … | `importVenueGeometry` body |
| Digit normalisation `digitNormalisation` | toggle | optional | on | — | — | `A١` and `A1` are one section to a person and two to a computer, and the failure is silent — the seats simply do not join, and you get geometry with no seats or seats with no … | `importVenueGeometry` body |
| Georeference `georeference` | group | optional | — | — | — | 19.2.56. Two known points turn drawing coordinates into real ones, and without it the map is a picture rather than something a guest can be located on. | `importVenueGeometry` body |
| Origin lat `georeference.originLat` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Origin lng `georeference.originLng` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Scale metres per unit `georeference.scaleMetresPerUnit` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Rotation degrees `georeference.rotationDegrees` | number field | optional | 0 | — | — | — | `importVenueGeometry` body |
| Anchors `georeference.anchors` | repeatable rows | optional | — | at least 2; at most 4 | — | Two points far apart. Two close together give an accurate scale and a rotation that drifts across the site — which reads as a map that is right near the entrance and wrong at the … | `importVenueGeometry` body |
| Label `georeference.anchors[].label` | text field | optional | — | — | — | — | `importVenueGeometry` body |
| Plan x `georeference.anchors[].planX` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Plan y `georeference.anchors[].planY` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Lat `georeference.anchors[].lat` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Lng `georeference.anchors[].lng` | number field | optional | — | — | — | — | `importVenueGeometry` body |
| Manifest ref `manifestRef` | picker: choose a manifest ref | optional | — | — | shows names, sends the id | The seating manifest, where this map has seats, as the `MediaAsset.id` from `assets.completeUpload`, uploaded the same way as `sourceRef`. | `importVenueGeometry` body |
| Resource manifest ref `resourceManifestRef` | picker: choose a resource manifest ref | optional | — | — | shows names, sends the id | The resource manifest, where this map carries bookable resources (decided 29 September, rev 3 REV3-15), uploaded like `manifestRef`. | `importVenueGeometry` body |
| Price bands `priceBands` | repeatable rows | optional | — | — | — | What each price band sells as, so a placed resource can be bought: the band code the manifest uses and the `catalogue.ProductVariant` that prices it (Family 6, Medium 10, Large … | `importVenueGeometry` body |
| Code `priceBands[].code` | text field | required | — | max length 40 | — | — | `importVenueGeometry` body |
| Name `priceBands[].name` | text field | optional | — | — | — | — | `importVenueGeometry` body |
| Variant `priceBands[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `importVenueGeometry` body |
| Create missing resources `createMissingResources` | toggle | optional | off | — | — | Where a manifest label has no `resources.Resource` with that `code` at this venue, create one through `resources.createResource` (kind, capacity and zone as attributes) instead of … | `importVenueGeometry` body |

**Sent by *Propose walkways*** (`proposeWalkways`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Import job `importJobId` | picker: choose an import job | optional | — | — | shows names, sends the id | The `venue-map` import job whose raster (and hand-marked strokes) to read. Absent, the map's latest import. | `proposeWalkways` body |
| Basis `basis` | segmented control | optional | Auto | Auto · Hand marked · Seen | — | `auto` follows the hand marks where the import found any and sees the paths otherwise; `handMarked` refuses (422) when there are no marks; `seen` ignores the marks. | `proposeWalkways` body |

**Sent by *Accept or reject segment*** (`acceptWalkwayProposals`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decisions `decisions` | repeatable rows | required | — | — | — | — | `acceptWalkwayProposals` body |
| Proposal `decisions[].proposalId` | picker: choose a proposal | required | — | — | shows names, sends the id | — | `acceptWalkwayProposals` body |
| Decision `decisions[].decision` | segmented control | required | — | Accept · Edit · Reject | — | — | `acceptWalkwayProposals` body |
| Path `decisions[].path` | group | optional | — | — | — | 19.2.56. The navigation graph. | `acceptWalkwayProposals` body |
| From point `decisions[].path.fromPointId` | picker: choose a from point | required | — | — | shows names, sends the id | — | `acceptWalkwayProposals` body |
| To point `decisions[].path.toPointId` | picker: choose a to point | required | — | — | shows names, sends the id | — | `acceptWalkwayProposals` body |
| Geometry `decisions[].path.geometry` | text field | optional | — | — | — | The centreline this edge follows, as an encoded polyline. A walkway in a drawing is a polygon and a route is a line down the middle of it, so extraction thins the polygon to a … | `acceptWalkwayProposals` body |
| Is step free `decisions[].path.isStepFree` | toggle | optional | on | — | — | The single most important attribute on this object. A wheelchair user routed up a staircase has been failed by the map, not by the venue. | `acceptWalkwayProposals` body |
| Is indoor `decisions[].path.isIndoor` | toggle | optional | off | — | — | — | `acceptWalkwayProposals` body |
| Restricted by point `decisions[].path.restrictedByPointId` | picker: choose a restricted by point | optional | — | — | shows names, sends the id | Where a path is one-way, it is because of a thing on it — not because of the path. | `acceptWalkwayProposals` body |

**Sent by *Close proposal*** (`decideProposedAction`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `decideProposedAction` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `decideProposedAction` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **decisions**: Per proposal Accept, Edit (move the point or change the kind) or Reject; never all-or-nothing, though "accept all above 90%" is allowed as a bulk selection that still lists what it accepts. *(source: contracts/satellite/venue-map.yaml#acceptVenueLabelProposals / R275)*
- **import file**: Native CAD (DWG, DXF) preferred because PDF loses layer names; PDF and raster accepted with a note that results will be weaker. *(source: contracts/satellite/venue-map.yaml#importVenueGeometry / DI-145)*

#### Outputs: what the screen shows and produces

**Shown**

**Upload progress** (progress indicator, from `completeUpload`): The transfer to storage, per file; when it ends the screen confirms it with `assets.completeUpload` and holds the `MediaAsset.id` the import takes. A file refused at `createUpload` (too large for its kind) says so before anything is sent.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Category | the name it points at, never the id | The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. |
| Venue | the name it points at, never the id | — |
| URL | text | Signed and expiring for private assets; stable CDN URL for public ones. |
| Thumbnail URL | text | — |
| Reference count | 1,234 | How many surfaces reference this asset. Non-zero refuses deletion. |

**Progress indicator** (progress indicator): Import is long enough to leave the screen. **A spinner with no proportion is a screen people reload**, and reloading an import is how a venue gets two of everything.

**Price bands** (data table, from `importVenueGeometry`): `priceBands`: each band code the manifest uses and the catalogue product variant that prices it (Family 6, Medium 10, Large 15, XL 20 on the Coastal Aqua map). **The price is the variant's**; the map holds none.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Map | the name it points at, never the id | — |
| Status | chip: Parsing, Preview ready, Committed, Failed | — |
| Outcome | chip: Parsed, Parsed with findings, Nothing found, No layers matched, Unreadable | — |
| Shapes found | 1,234 | — |
| Layers found | list or chips (count when long) | Every layer name in the source, decoded. Shown whether or not extraction worked, so an operator maps a role by reading rather than guessing. |
| Unmapped layers | list or chips (count when long) | — |
| Manifest rows read | 1,234 | — |
| Resources found | 1,234 | Bookable resource shapes found on the resource layer (rev 3 REV3-15). Null where the map has none. |
| Resource rows joined | 1,234 | Resource manifest rows that joined a shape and a `resources.Resource`. The number to check against your own count, as `manifestRowsJoined` … |
| Manifest rows joined | 1,234 | The number to check against your own count. A manifest of 396 seats that joins 220 is the digit problem in §4, or a section code that … |
| Findings | list or chips (count when long) | Named against the spec, so a finding maps to a section of `handoff/venue-map-input-spec.md` rather than to a stack trace. |
| Code | chip: Duplicate layer name, Geometry on layer zero, Unmapped layer, Mixed layer content … | A closed set, and each one names a rule in the spec. Free-text findings are findings a drawing office cannot act on. |
| Severity | chip: Error, Warning, Info | `warning` is the important level here. `rasterOnly` and `noGeoreference` are warnings — the map still works, with less — and treating them … |
| Message | text | — |
| Spec section | text | Which part of the spec covers it — `§2 Layers`, `§4 Digits`. |
| Affected | list or chips (count when long) | The layers, sections or rows involved. Named, not counted. |
| Ocr | grouped details | What the OCR step read off a scanned PDF or a raster (3 October 2026, r1 additions). |
| Pages read | 1,234 | — |
| Mean confidence | 1,234.5 | — |

**What the import read** (detail panel, from `getVenueMapImportJob`): Polled while the import runs. **The resource findings are listed apart** from the geometry ones (a manifest row with no shape, a shape with no row, a label with no resource, a band with no variant), each naming the row or the label, so an operator can fix the sheet rather than guess.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Parsing, Preview ready, Committed, Failed | — |
| Outcome | chip: Parsed, Parsed with findings, Nothing found, No layers matched, Unreadable | — |
| Shapes found | 1,234 | — |
| Layers found | list or chips (count when long) | Every layer name in the source, decoded. Shown whether or not extraction worked, so an operator maps a role by reading rather than guessing. |
| Unmapped layers | list or chips (count when long) | — |
| Manifest rows read | 1,234 | — |
| Resources found | 1,234 | Bookable resource shapes found on the resource layer (rev 3 REV3-15). Null where the map has none. |
| Resource rows joined | 1,234 | Resource manifest rows that joined a shape and a `resources.Resource`. The number to check against your own count, as `manifestRowsJoined` … |
| Manifest rows joined | 1,234 | The number to check against your own count. A manifest of 396 seats that joins 220 is the digit problem in §4, or a section code that … |
| Findings | list or chips (count when long) | Named against the spec, so a finding maps to a section of `handoff/venue-map-input-spec.md` rather than to a stack trace. |

**What the scan, the marks and the model gave** (detail panel, from `getVenueMapImportJob`): The text the OCR step read (with its confidence, offered to the label proposals as hints), the hand-marked strokes found, and for a GLB the measured budget line by line with the model findings and whether the 3D layer will publish (3 October 2026, CHG-RONEC-001). Each part shows only when the source had it.

| Shows | Format | Notes |
|---|---|---|
| Ocr | grouped details | What the OCR step read off a scanned PDF or a raster (3 October 2026, r1 additions). |
| Hand marked paths | grouped details | The hand-marked strokes the import found on a raster plan sent with `handMarkedPaths` (3 October 2026, r1 additions). |
| Model | grouped details | The GLB and navigation file, measured (`glbModel` and `navigationFile` imports; ADR-0069 sections 1, 2, 3 and 6; 3 October 2026). |

**Open walkway proposals** (card list, from `listProposedActions`): The walkway segments `proposeWalkways` proposed and nobody has decided yet (one `ai.proposed_action` each), read again when the operator comes back to the import; each is accepted or rejected on its own with `acceptWalkwayProposals` (3 October 2026, CHG-RONEC-001).

| Shows | Format | Notes |
|---|---|---|
| Summary | text | — |
| Status | chip: Proposed, Approved, Rejected, Applied, Expired | Expiry (decided 28 September, audit R213): a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires … |
| Proposed at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import venue geometry (primary button) | `importVenueGeometry` POST `/venue-maps/{mapId}/import` | inline | VenueMapImportJob | 422 Refused before any parsing (3 October 2026, r1 additions): `glbModel` with no `navigationFileRef` (`navigationFileMissing`), a `sourceRef` whose asset kind … (VenueMapImportProblem) | — |
| Propose venue labels (secondary button) | `proposeVenueLabels` POST `/ai/venue-map/{mapId}/propose-labels` | — | VenueLabelProposal[] | — | — |
| Accept venue label proposals (secondary button) | `acceptVenueLabelProposals` POST `/venue-maps/{mapId}/proposals` | inline | VenuePoint[] | — | opens modal first |
| Propose walkways (secondary button) | `proposeWalkways` POST `/ai/venue-map/{mapId}/propose-walkways` | inline | WalkwayProposal[] | 409 The map has vector geometry. Refused deliberately — subtraction is available and better, and running a model where geometry exists is how a worse answer gets …; 422 `basis: handMarked` on an import that found no … | — |
| Accept or reject segment (secondary button) | `acceptWalkwayProposals` POST `/venue-maps/{mapId}/walkway-proposals` | inline | GraphValidation | — | — |
| Close proposal (secondary button) | `decideProposedAction` POST `/proposed-actions/{actionId}/decide` | inline | ProposedAction | 403 The caller may not decide this proposal (audit R213 (3)): a level 2 proposal and the caller lacks `AI_APPROVE` (`approval-level-requires-manager`), a level 2 …; 409 The action is no longer `proposed` — already … | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **extraction report**: Outcome (parsed, parsed with findings, nothing found, no layers matched, unreadable), shapes found, layers found and unmapped layers as chips, manifest rows read and joined. *(source: contracts/satellite/venue-map.yaml#getVenueMapImportJob / F26 step 2)*
- **proposals**: Each with the proposed kind and its confidence; low-confidence proposals are shown, not filtered, sorted to the top. *(source: screens/P08-venue-back-office.yaml#BO-093 / F26 step 3)*

**Where the user goes next**

- → `BO-094` Map Editor & Publish: *The operator places what the drawing did not carry and links each point to what it is*; carries `mapId`, `uploadId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved map import labelling. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the map import labelling untouched. |
| Empty, no results (`?state=emptyNoResults`) | An import that read no resources on a map meant to carry them says so (`resourcesFound` 0) and names the resource layer it looked for, rather than showing an empty price-band table. |
| Empty, first run (`?state=emptyFirstRun`) | No map import labelling configured. The form opens empty and `importVenueGeometry` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMapImportJob` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `listProposedActions`, `decideProposedAction`; `ASSET_LIBRARY_MANAGE` for `createUpload`, `completeUpload`; `VENUE_MAP_MANAGE` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 The map has vector geometry. Refused deliberately — subtraction is available and better, and running a model where geometry exists is … |

#### Edge cases to draw

- **File yields nothing**: Says "nothing found" or "no layers matched" with the layers it did see, not an empty success. *(source: contracts/satellite/venue-map.yaml#importVenueGeometry)*
- **Walkway proposals**: A stricter gate than labels; accepted walkways are validated as paths immediately and any unreachable point is reported. *(source: contracts/satellite/venue-map.yaml#acceptWalkwayProposals)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  file: coastal-aqua-site-plan.dwg
  outcome: parsedWithFindings
  shapes: 412
  layers:
  - WALKWAYS
  - TOILETS
  - F&B
  - RIDES
  - CABANAS
  unmapped:
  - LANDSCAPE-TREES
  resourcesFound: 38
  resourcesJoined: 36
proposal:
  shape: polygon near Gate 1
  proposed: toilet
  confidence: 0.64
```

#### Permissions

- `importVenueGeometry` → `VENUE_MAP_MANAGE` (configure) · staff
- `proposeVenueLabels` → `VENUE_MAP_MANAGE` (configure) · staff
- `acceptVenueLabelProposals` → `VENUE_MAP_MANAGE` (configure) · staff
- `getVenueMapImportJob` → `VENUE_MAP_VIEW` (read) · staff
- `acceptWalkwayProposals` → `VENUE_MAP_MANAGE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `proposeWalkways` → `VENUE_MAP_MANAGE` (configure) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMapImportJob` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `listProposedActions`, `decideProposedAction`; `ASSET_LIBRARY_MANAGE` for `createUpload`, `completeUpload`; `VENUE_MAP_MANAGE` …

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.2.3 | CAD Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importVenueGeometry` |
| 21.2.4 | Image Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importVenueGeometry` |
| 1.4.24 | Automated Seat Map Creation Generate a complete seat map from venue drawings, CAD files, PDFs, or architectural plans. Automatically identify seating sections, rows, and individual seats. Convert … | Ticketing Catalogue | CONTRACTED | `proposeVenueLabels` |
| 8.8.13 | The AI assistant can configure: Seating zones Price categories Seat holds Reserved seating Accessibility seating Example: "Create VIP seating in the first three rows with a 30% premium." | Unified Operations Dashboard | CONTRACTED | `proposeVenueLabels` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The 3D seat view needs the venue's actual CAD file with defined seating sections uploaded; setup is more involved than the 2D seat map. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-890)*
- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-093` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 1.dc.html`
- Client design-board frames: `Seat Board 1.dc.html#seat-1a`
- Flow F26 *A venue maps its site*, step 2: The plan is uploaded and read. → Shapes extracted, **deterministically**. Every layer name reported back, decoded, mapped or not — and **a file that yields nothing says `nothingFound` rather than reporting success**, which is the …
- Flow F26 *A venue maps its site*, step 3: The assistant proposes what each shape is; the operator accepts, edits or rejects. → Points created from accepted proposals. **Low-confidence proposals are shown, not filtered** — the shape the assistant is unsure about is the one most worth a human looking at. On a raster plan (or a …
- Flow F26 branch at step 3 (requiresStaff): when The assistant proposes a fire exit as an ordinary exit., The operator rejects it and places it correctly. **A map that cannot tell them apart routes a normal departure through a fire door**, which is why `emergencyExit` is a separate kind and why proposals …
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (89), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (57 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-093?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import venue geometry, Propose venue labels, Accept venue label proposals, Propose walkways, Accept or reject segment, Close proposal.
- [ ] Every transition is wired: `BO-094`.
- [ ] Every gated control is gated: `AI_USE`, `ASSET_LIBRARY_MANAGE`, `VENUE_MAP_MANAGE`, `VENUE_MAP_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-094` Map Editor & Publish

**Place booths, toilets, exits, rides and restaurants, and the cabanas, loungers and tables guests book from the map, then publish.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `seating` module |
| Block | Block A · ticket #28079 (APP-SETUP-BO-094) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE`, `VENUE_MAP_PUBLISH`, `VENUE_MAP_VIEW` (3 configure, 3 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getVenueMap` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `mapId` (deepLink), `pathId` (deepLink), `uploadId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-mapping/map-editor` |

**What the spec says about it.** CF-123. **Publishing is a separate act from saving**, and the screen makes that visible — editing a live map under a guest standing in front of it is how a route ends at a wall. **Refuses to publish a point linked to a closed outlet**, naming which one: a restaurant point pointing nowhere is worse than no point, because a guest walks there. **`isStepFree` on a path is the field to get right** — a wheelchair user routed up a staircase was failed by the map, not the venue. **Graph validation runs before publish and on demand.** The screen separates two findings that read the same and are not: **an unreachable point is a defect, and a point reachable only by steps is a map that works until a wheelchair user opens it.** **Critical points — first aid, emergency exits, assembly points — are listed apart**, because an unreachable gift shop and an unreachable assembly point should not sit in one list of two hundred. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Place and link what the drawing did not carry (toilets, exits, rides, restaurants, shops, prayer rooms, first aid) and the cabanas, loungers and tables guests book, then validate and publish. Publishing is separate from saving and the screen must make that visible; a closure of a path is an operational act that takes effect in seconds without republishing.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCatalogueBundles return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do rental booths and stations appear on the live map as points, or does the map builder need a booth/station kind?** → Drawn default accepted: Draw them as kiosk points linked to the rental outlet until decided. *(decided by Chinmay, 2026-10-02; DEC-104 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Guest map artwork | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | **The illustrated map guests see** (input spec section 6; the F26 brief's open item, closed 3 October 2026 here, CHG-RONEC-001): PNG or JPG up to about 12,000 px wide, uploaded through … | `VenueMap.baseAssetId` |
| Item description | key and value settings | optional | — | — | — | **What the guest reads on Item Detail** (decided 29 September, MOB-4): rides, shows, restaurants and shops. Per language. | `VenuePoint.description` |
| Photos and video | repeatable rows | optional | — | at most 12 | — | From the asset library; the first is the gallery cover on GST-004 Item Detail (MOB-4). | `VenuePoint.media` |
| Featured offer | group | optional | — | — | — | **The product or bundle the item detail proposes** (decided 29 September, MOB-4), on any kind of point, e.g. a restaurant's *meal combo with admission* (a bundle from BO-011). Products from … | `VenuePoint.featuredOffer` |
| Typical visit (minutes) | number field (minutes) | optional | — | min 1; max 600 | — | What the Plan tab's planner allows for this stop (MOB-6). | `VenuePoint.typicalDurationMinutes` |
| Interests | multi-select chips | optional | — | Thrill · Family · Kids · Water · Animals · Shows · Culture · Shopping · Dining · Relaxing · Photo · Adventure …; at most 12 | — | Matched against the guest's interests on the Plan tab (MOB-6). | `VenuePoint.interestTags` |
| Cuisine | list of values (chips) | optional | — | at most 8 | — | For restaurants and kiosks; matched against the guest's cuisine choice on the Plan tab (MOB-6), for this venue's days only (client meeting 30 September, MoM 4.7). | `VenuePoint.cuisineTags` |
| Retail | list of values (chips) | optional | — | at most 8 | — | For shops and kiosks that sell goods (souvenirs, toys, apparel ...); matched against the guest's shop choice on the Plan tab for this venue's days only (client meeting 30 September, MoM 4.7: retail … | `VenuePoint.retailTags` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, as on `getVenueMap`. | `getVenueMapGraph` ?draft |
| Step free only | toggle | off | — | `getVenueMapGraph` ?stepFreeOnly |

**Form: Save artwork and alignment** (modal, opened by *Save artwork and alignment*; *Save artwork and alignment* calls `setVenueMapArtwork`, *Cancel* sends nothing)

**Collects what `setVenueMapArtwork` sends before it is called.** Required: `baseAssetId` (the uploaded artwork, or none to remove it) and, with an image, `baseImageAlignment`: the image size and two to four alignment pairs, each a point clicked on the artwork and the same point clicked on the plan. Dismissing sends nothing; the map keeps the artwork it had.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base image `baseAssetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The illustrated map (an `image` asset, PNG or JPG, up to about 12,000 px wide). Null removes it. | `setVenueMapArtwork` body |
| Base image alignment `baseImageAlignment` | group | optional | — | — | — | Required with an image. Pixel positions on the image matched to plan coordinates. | `setVenueMapArtwork` body |
| Image width px `baseImageAlignment.imageWidthPx` | number field | required | — | min 1 | — | — | `setVenueMapArtwork` body |
| Image height px `baseImageAlignment.imageHeightPx` | number field | required | — | min 1 | — | — | `setVenueMapArtwork` body |
| Anchors `baseImageAlignment.anchors` | repeatable rows | required | — | at least 2; at most 4 | — | — | `setVenueMapArtwork` body |
| Plan x `baseImageAlignment.anchors[].planX` | number field | required | — | — | — | — | `setVenueMapArtwork` body |
| Plan y `baseImageAlignment.anchors[].planY` | number field | required | — | — | — | — | `setVenueMapArtwork` body |
| Image x `baseImageAlignment.anchors[].imageX` | number field | required | — | — | — | — | `setVenueMapArtwork` body |
| Image y `baseImageAlignment.anchors[].imageY` | number field | required | — | — | — | — | `setVenueMapArtwork` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The map is archived (`map-archived`); an archived map takes no new artwork.; 422 An image with no `baseImageAlignment`, an asset that is not an image, or alignment points too close together to place the plan (`artwork-alignment-required` …

**Form: Save venue point** (modal, opened by *Save venue point*; *Save venue point* calls `setVenuePoint`, *Cancel* sends nothing)

**Collects what `setVenuePoint` sends before it is called.** Required: `kind`, `name`, `position`. Optional: `nameLocalised`, `outletId`, `productId`, `accessPointId`, `isStepFree`, `openingHours`, `iconRef`, `isActive`, `isNavigable`, `isDestination`, `pointId`; and the item details decided 29 September (MOB-4, MOB-6): `description`, `media`, `featuredOffer` (a product or a bundle, on any kind of point), `typicalDurationMinutes`, `interestTags`, `cuisineTags`; and `retailTags` (30 September, MoM 4.7). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `mapId` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Ride · Attraction · Show · Restaurant · Cafe · Shop · Kiosk · Toilet · Baby care · Prayer room · First aid · Atm … | — | A closed set, and `emergencyExit` is separate from `exit` on purpose. An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them … | `setVenuePoint` body |
| Name `name` | text field | required | — | — | — | Unique per venue (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` … | `setVenuePoint` body |
| Name localised `nameLocalised` | key and value settings | optional | — | — | — | — | `setVenuePoint` body |
| Position `position` | group | required | — | — | — | Drawing coordinates. Latitude and longitude are derived from the georeference, not stored, so a map that is re-georeferenced does not need every point moved. | `setVenuePoint` body |
| X `position.x` | number field | required | — | — | — | — | `setVenuePoint` body |
| Y `position.y` | number field | required | — | — | — | — | `setVenuePoint` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | For a restaurant, cafe, shop or kiosk. Tapping it should open the menu, and that only works if the map knows which outlet it is. | `setVenuePoint` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | For a ride or show — links to wait times and to booking. What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer` (29 September, MOB-4); this … | `setVenuePoint` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | For an entrance or exit. This is what makes 3.2.64 work — live admission statistics drawn on the point they came from. | `setVenuePoint` body |
| Is step free `isStepFree` | toggle | optional | on | — | — | Whether the point itself can be reached without steps. The same name as `VenuePath.isStepFree`, because it is the same concept (it was `isAccessible` until the 26 September audit). | `setVenuePoint` body |
| Opening hours `openingHours` | text field | optional | — | — | — | — | `setVenuePoint` body |
| Icon ref `iconRef` | text field | optional | — | — | — | — | `setVenuePoint` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setVenuePoint` body |
| Is navigable `isNavigable` | toggle | optional | on | — | — | Whether a route may pass through it. False for a point that marks a place without being reachable — a stage a guest cannot walk onto, a zone label. | `setVenuePoint` body |
| Is destination `isDestination` | toggle | optional | on | — | — | Whether a guest may be routed *to* it, and whether it appears in a list of places. | `setVenuePoint` body |
| Description `description` | key and value settings | optional | — | — | — | What the guest reads on Item Detail (29 September, MOB-4). Keyed by locale, like `nameLocalised`. | `setVenuePoint` body |
| Media `media` | repeatable rows | optional | — | at most 12 | — | The gallery on Item Detail (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. | `setVenuePoint` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setVenuePoint` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `setVenuePoint` body |
| Is primary `media[].isPrimary` | toggle | optional | off | — | — | — | `setVenuePoint` body |
| Alt text `media[].altText` | text field | optional | — | max length 200 | — | — | `setVenuePoint` body |
| Featured offer `featuredOffer` | group | optional | — | — | — | The product card on Item Detail, for every kind of point (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from … | `setVenuePoint` body |
| Kind `featuredOffer.kind` | segmented control | required | — | Product · Bundle | — | — | `setVenuePoint` body |
| ID `featuredOffer.id` | picker: choose an id | required | — | — | shows names, sends the id | The `catalogue.product` id or the `promotions.bundle` id, by `kind`. | `setVenuePoint` body |
| Label `featuredOffer.label` | text field | optional | — | max length 40 | — | The button text, e.g. *Buy meal combo*. | `setVenuePoint` body |
| Typical duration minutes `typicalDurationMinutes` | number field (minutes) | optional | — | min 1; max 600 | — | How long a visit to this point usually takes, ride time and queue excluded (29 September, MOB-6). | `setVenuePoint` body |
| Interest tags `interestTags` | multi-select chips | optional | — | Thrill · Family · Kids · Water · Animals · Shows · Culture · Shopping · Dining · Relaxing · Photo · Adventure …; at most 12 | — | What a guest who says they like this would like here (29 September, MOB-6): the planner matches the guest's interests against these. | `setVenuePoint` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | For dining points (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. | `setVenuePoint` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | For retail points (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). | `setVenuePoint` body |
| Point `pointId` | picker: choose a point | optional | — | — | shows names, sends the id | The point to amend. Absent or null places a new point. | `setVenuePoint` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Publish venue map** (modal, opened by *Publish venue map*; *Publish venue map* calls `publishVenueMap`, *Cancel* sends nothing)

**Collects what `publishVenueMap` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | — | `publishVenueMap` body |

Errors to draw in the form: 409 Unresolved proposals, a broken link, or a disconnected area (audit R106 (8)). The reason names which point, in `blockers`, because *"cannot publish"* on a map … (VenueMapPublishProblem)

**Form: Save path closure** (modal, opened by *Save path closure*; *Save path closure* calls `setPathClosure`, *Cancel* sends nothing)

**Collects what `setPathClosure` sends before it is called.** Required: `isClosed`. Optional: `reason` (maintenance, incident, event, weather, crowding, other), `note`, `force`, `expectedReopenAt`. **Choosing Other makes the note required** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is closed `isClosed` | toggle | required | — | — | — | — | `setPathClosure` body |
| Reason `reason` | select | optional | — | Maintenance · Incident · Event · Weather · Crowding · Other | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222); refused `400` without one, and the notes are reviewed quarterly so the common … | `setPathClosure` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setPathClosure` body |
| Force `force` | toggle | optional | off | — | — | Close it even though something becomes unreachable. | `setPathClosure` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPathClosure` body |

Errors to draw in the form: 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem)

**Form: Place resource** (modal, opened by *Place resource*; *Place resource* calls `setPlacedResource`, *Cancel* sends nothing)

**Collects what `setPlacedResource` sends before it is called.** `resourceId` (the resource it is), `label` (what the guest taps, e.g. B09; unique on the map), `kind` (cabana, lounger, table, pitch, other), `zone`, `capacity` (1 to 500, checked against the party at hold), `priceBandCode` (one of the bands given at import; its variant prices it), `position` or `boundary`, `isBookable`; `placedResourceId` to amend one. Decided 29 September, rev 3 REV3-15. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resource `resourceId` | picker: choose a resource | required | — | — | shows names, sends the id | The `resources.Resource` this is. Availability, holds and bookings are keyed by this, so a republished map with the cabana moved keeps its bookings. | `setPlacedResource` body |
| Label `label` | text field | required | — | max length 40 | — | What the guest sees and taps, e.g. `B09`. | `setPlacedResource` body |
| Kind `kind` | radio group | required | — | Cabana · Lounger · Table · Pitch · Other | — | A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay … | `setPlacedResource` body |
| Zone `zone` | text field | required | — | max length 80 | — | The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`. | `setPlacedResource` body |
| Capacity `capacity` | number field | required | — | min 1; max 500 | — | Guests it takes, e.g. 15. | `setPlacedResource` body |
| Price band code `priceBandCode` | text field | required | — | max length 40 | — | The band it sells in, e.g. `Large`, one of the `priceBands` given at import. | `setPlacedResource` body |
| Position `position` | group | required | — | — | — | Drawing coordinates of its label anchor, as on `VenuePoint`. | `setPlacedResource` body |
| X `position.x` | number field | required | — | — | — | — | `setPlacedResource` body |
| Y `position.y` | number field | required | — | — | — | — | `setPlacedResource` body |
| Boundary `boundary` | repeatable rows | optional | — | — | — | The shape drawn, as a polygon in drawing coordinates. Null for a pin. | `setPlacedResource` body |
| X `boundary[].x` | number field | optional | — | — | — | — | `setPlacedResource` body |
| Y `boundary[].y` | number field | optional | — | — | — | — | `setPlacedResource` body |
| Is bookable `isBookable` | toggle | optional | on | — | — | False keeps it on the map and off sale, e.g. a cabana kept for staff use. | `setPlacedResource` body |
| Placed resource `placedResourceId` | picker: choose a placed resource | optional | — | — | shows names, sends the id | The placed resource to amend. Absent or null places a new one. | `setPlacedResource` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **point link**: The link field depends on the kind (outlet for restaurant, cafe, shop, kiosk; product for ride and show; access point for entrance and exit); a featured offer (product or bundle) can be set on any kind. *(source: contracts/satellite/venue-map.yaml#setVenuePoint / F26 step 4)*
- **point name**: Unique per venue across all its maps, compared without case; English and Arabic. *(source: contracts/satellite/venue-map.yaml#setVenuePoint / R108)*
- **isStepFree**: The field to get right; default yes, and the validator reports points reachable only by steps. *(source: contracts/satellite/venue-map.yaml#validateVenueMapGraph)*
- **bookable place**: Label unique on the map (B09), kind, zone, capacity 1 to 500, price band from the import's bands; "not bookable" keeps it on the map greyed. The map holds no price. *(source: contracts/satellite/venue-map.yaml#setPlacedResource / REV3-15)*
- **path closure reason**: Maintenance, incident, event, weather, crowding, other (note required); expected reopen time. *(source: contracts/satellite/venue-map.yaml#setPathClosure / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**The venue map** (detail panel, from `getVenueMap`)

| Shows | Format | Notes |
|---|---|---|
| Map | grouped details | A park map, or a floor plan. Several per venue — a guest on the second floor should not be shown the ground floor's toilets. |
| Points | list or chips (count when long) | — |
| Paths | list or chips (count when long) | — |

**The venue map graph** (detail panel, from `getVenueMapGraph`)

| Shows | Format | Notes |
|---|---|---|
| Map | the name it points at, never the id | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Nodes | list or chips (count when long) | — |
| Edges | list or chips (count when long) | — |
| Components | 1,234 | How many disconnected parts. One is the answer for a park. |

**Bookable places on the map** (detail panel, from `getVenueMap`): **Each placed resource with its label, kind, zone, capacity and price band** (decided 29 September, rev 3 REV3-15, superseding audit R073 (c) for resources on an ingested map). Guests pick one of these on the map and buy it. A place with no linked resource or no price band is marked, because publishing will refuse it.

| Shows | Format | Notes |
|---|---|---|
| Resources | list or chips (count when long) | The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none. |

**Artwork upload** (progress indicator, from `completeUpload`): The transfer to storage; when it ends the screen confirms it with `assets.completeUpload` and holds the `MediaAsset.id` that `setVenueMapArtwork` takes.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Category | the name it points at, never the id | The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. |
| Venue | the name it points at, never the id | — |
| URL | text | Signed and expiring for private assets; stable CDN URL for public ones. |
| Thumbnail URL | text | — |
| Reference count | 1,234 | How many surfaces reference this asset. Non-zero refuses deletion. |

**3D layer** (banner, from `getVenueMap`): None, publishable or blocked (ADR-0069 as amended 3 October 2026). Blocked names the import job's model findings on BO-093; the 2D map still publishes and guests see 2D until a corrected model is imported.

| Shows | Format | Notes |
|---|---|---|
| Map | grouped details | A park map, or a floor plan. Several per venue — a guest on the second floor should not be shown the ground floor's toilets. |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Park, Floor, Zone, Parking | — |
| Floor level | 1,234 | — |
| Status | chip: Draft, Published, Archived | `draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value. |
| Published version | 1,234 | The `VenueMapVersion.version` guests are served. Null until the first publish. |
| Graph version | 1,234 | Bumped by a publish or a closure, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the … |
| Is georeferenced | yes / no (icon or chip) | Whether a guest can be located on it. Without a georeference the map is a picture — useful, and not navigable. |
| Base image | the image or video | The illustrated map a guest actually sees, held in `assets` like any other media. |
| Base image alignment | grouped details | How the illustration lines up with the geometry. They are drawn at different scales by different people, and a point placed on the plan … |
| Image width px | 1,234 | — |
| Image height px | 1,234 | — |
| Anchors | list or chips (count when long) | — |
| Tile set ref | text | Where a base image is large enough to need zoom levels. A 12,000-pixel park map is not something a phone downloads on arrival, and a guest … |
| Bounds geo json | text | — |
| Graph status | chip: Not built, Connected, Disconnected, Partial | Whether every public point can actually be reached. Computed at publish. |
| Model image | the image or video | The 3D layer of the working draft (ADR-0069, contract item closed 3 October 2026): the GLB (`model3d` asset) the last `glbModel` import … |
| Navigation file image | the image or video | The navigation file imported with the model, kept so the import can be re-run and audited. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Save venue point (primary button) | `setVenuePoint` POST `/venue-maps/{mapId}/points` | SetVenuePointRequest | VenuePoint | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Publish venue map (secondary button) | `publishVenueMap` POST `/venue-maps/{mapId}/publish` | inline | VenueMap | 409 Unresolved proposals, a broken link, or a disconnected area (audit R106 (8)). The reason names which point, in `blockers`, because *"cannot publish"* on a map … (VenueMapPublishProblem) | opens modal first |
| Validate venue map graph (secondary button) | `validateVenueMapGraph` POST `/venue-maps/{mapId}/validate-graph` | — | GraphValidation | — | — |
| Save path closure (secondary button) | `setPathClosure` POST `/venue-maps/{mapId}/paths/{pathId}/closure` | inline | PathClosureResult | 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem) | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Place resource (secondary button) | `setPlacedResource` POST `/venue-maps/{mapId}/resources` | SetPlacedResourceRequest | PlacedResource | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope … | opens modal first |
| Export navigation file (secondary button) | `getVenueNavigationFile` GET `/venue-maps/{mapId}/navigation-file` | — | VenueNavigationFile | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save artwork and alignment (secondary button) | `setVenueMapArtwork` POST `/venue-maps/{mapId}/artwork` | inline | VenueMap | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The map is archived (`map-archived`); an archived map takes no new artwork.; 422 An image with no … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **validation**: Unreachable points, points reachable only by steps, dead-end paths and critical unreachable points (exits, first aid) listed with "show on map". *(source: contracts/satellite/venue-map.yaml#validateVenueMapGraph / F26 step 5)*
- **draft vs published**: A persistent banner "Editing draft. Guests see version 7 (published 2 Oct)" with the number of unpublished changes. *(source: contracts/satellite/venue-map.yaml#publishVenueMap)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Publish**: Runs validation; refuses a point linked to a closed outlet, naming it; creates a new version while guests mid-route finish on theirs. *(source: contracts/satellite/venue-map.yaml#publishVenueMap / F26 step 6)*
- **Close path**: Immediate, no republish; reports the points it strands. *(source: contracts/satellite/venue-map.yaml#setPathClosure)*

**Data it reads**: `getVenueMap` (onLoad, The draft); `getVenueMapGraph` (onLoad, The navigation graph, ready to route over)

**Where the user goes next**

- → `GST-021` Interactive Map: *A guest opens the map and is routed*; carries `mapId`; calls `publishVenueMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The map editor publish, read by `getVenueMap`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the map editor publish untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No map editor publish yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_LIBRARY_VIEW` for `searchMedia`; `PRODUCT_VIEW` for `listProducts`, `listCatalogueBundles`; `VENUE_MAP_MANAGE` for `setVenuePoint` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 400 Validation failed; 409 A business code the request names is already used within its … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
points:
- kind: toilet
  name: Toilets near Splash Zone
  nameAr: دورات مياه قرب منطقة الرذاذ
  stepFree: true
- kind: restaurant
  name: Harbour Kitchen
  outlet: Harbour Kitchen
  featuredOffer: Family Fun Bundle
- kind: emergencyExit
  name: Emergency exit East 3
bookable:
  label: B09
  kind: cabana
  zone: Beach
  capacity: 6
  priceBand: Large
closure:
  path: Riverwalk 4 to 5
  reason: maintenance
  reopens: 2026-11-15 09:00
```

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `setVenuePoint` → `VENUE_MAP_MANAGE` (configure) · staff
- `publishVenueMap` → `VENUE_MAP_PUBLISH` (configure) · staff
- `validateVenueMapGraph` → `VENUE_MAP_MANAGE` (configure) · staff
- `setPathClosure` → `VENUE_MAP_MANAGE` (configure) · staff
- `getVenueMapGraph` → `VENUE_MAP_VIEW` (read) · staff, guest
- `setPlacedResource` → `VENUE_MAP_MANAGE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `setVenueMapArtwork` → `VENUE_MAP_MANAGE` (configure) · staff
- `getVenueNavigationFile` → `VENUE_MAP_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ASSET_LIBRARY_VIEW` for `searchMedia`; `PRODUCT_VIEW` for `listProducts`, `listCatalogueBundles`; `VENUE_MAP_MANAGE` for `setVenuePoint` …

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.55 | Interactive Venue Map - System shall provide interactive venue maps. | Guest Mobile App & Branding | CONTRACTED | `getVenueMap` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |
| 19.2.57 | Attraction Mapping - System shall display attractions on maps. | Guest Mobile App & Branding | CONTRACTED | data `VenuePoint` |
| 19.2.58 | Restaurant Mapping - System shall display restaurants on maps. | Guest Mobile App & Branding | CONTRACTED | data `VenuePoint` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- The 3D seat view needs the venue's actual CAD file with defined seating sections uploaded; setup is more involved than the 2D seat map. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-890)*
- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-094` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 1.dc.html`
- Client design-board frames: `Seat Board 1.dc.html#seat-1b`
- Flow F26 *A venue maps its site*, step 4: The operator places what the drawing did not carry and links each point to what it is. → A restaurant point carries its outlet id, a ride its product id, a gate its access point. **Tapping a restaurant on the map should open its menu, and that only works if the map knows which outlet it …
- Flow F26 *A venue maps its site*, step 5: The graph is validated before anybody publishes. → Unreachable points, dead-end paths, orphan components — and **points reachable only by steps**, which is the finding nothing in the drawing makes visible.
- Flow F26 *A venue maps its site*, step 6: The manager publishes. → A new version. **The previous one stays readable** so a guest mid-route on version 3 finishes on version 3.
- Flow F26 branch at step 5 (requiresStaff): when A point is reachable only by steps., Listed separately from unreachable points. **The map works perfectly until a wheelchair user opens it**, and nothing in the drawing makes it visible — which is the whole reason this check runs before …
- Flow F26 branch at step 6 (recoverable): when A point links to an outlet that has closed., Publish is refused and **the response names which point**. A restaurant point pointing nowhere is worse than no point, because a guest walks there.
- Flow F26 branch at step 6 (recoverable): when A placed cabana has no linked resource or no price band, or two places share a label., Publish is refused with `resourceUnlinked`, `resourcePriceBandMissing` or `duplicateResourceLabel`, naming the place (decided 29 September, rev 3 REV3-15). **A cabana a guest can tap and cannot buy …
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (67), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (49 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-094?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Save venue point, Publish venue map, Validate venue map graph, Save path closure, What publishing changes, Place resource, Export navigation file, Save artwork and alignment.
- [ ] Every transition is wired: `GST-021`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE`, `VENUE_MAP_PUBLISH`, `VENUE_MAP_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-095` Resources

**Every bookable object at this venue, and whether it is free.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `resources` module |
| Block | Block D · task VM-BO-095 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listResources` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/resources/directory` |

**What the spec says about it.** CF-125. **A resource is a specific object, not a quantity** — forty identical strollers are forty rows, because guest twelve returned stroller twelve.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The register of bookable resources at the venue - each a specific object (forty strollers are forty rows, because guest twelve returned stroller twelve), of a kind (cabana, lounger, locker, wheelchair, stroller, equipment, room, vehicle, instructor, staff, table, pitch, studio), with its status and the reason. The one thing to get right: status carries its reason - booked and under repair need different responses from someone looking for something free.

**Known correction pending (do not draw the wrong version)**

- **Kind filter appears twice (a textField and a multiSelect) and an unlabelled empty table** Why: One kind filter (closed enum); the status-with-reason table is the main list. *(source: contracts/satellite/resources.yaml#listResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Columns include id, venueId, scopePath, principalId and raw attributes** Why: Spec leakage (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select | optional | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | — | Sends `?kind=` to `listResources`. | `listResources` ?kind |
| Available from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?availableFrom=` to `listResources`. | `listResources` ?availableFrom |
| Available to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?availableTo=` to `listResources`. | `listResources` ?availableTo |
| Search resources | search field | — | — | — | — | — | — |
| Kind | multi select | — | — | — | — | — | — |

**Form: Create resource** (modal, opened by *Create resource*; *Create resource* calls `createResource`, *Cancel* sends nothing)

**Collects what `createResource` sends before it is called.** Required: `id`, `code`, `name`, `kind`, `venueId`. Optional: `scopePath`, `parentResourceId`, `principalId`, `attributes`, `setupMinutes`, `teardownMinutes`, `requiresQualification`, `depositAmount`, `status`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createResource` body |
| Code `code` | text field | required | — | — | — | — | `createResource` body |
| Name `name` | text field | required | — | — | — | — | `createResource` body |
| Kind `kind` | select | required | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | — | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. | `createResource` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createResource` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `createResource` body |
| Parent resource `parentResourceId` | picker: choose a parent resource | optional | — | — | shows names, sends the id | A pool cabana belongs to the pool area; a seat belongs to an auditorium. Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise … | `createResource` body |
| Principal `principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | For a resource of kind `instructor` or `staff`. `workforce` still owns their rota — this says whether they are qualified and whether they are already committed. | `createResource` body |
| Attributes `attributes` | key and value settings | optional | — | — | — | Configurable per kind — capacity, size, shade, power, poolside. | `createResource` body |
| Setup minutes `setupMinutes` | number field (minutes) | optional | 0 | — | — | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every … | `createResource` body |
| Teardown minutes `teardownMinutes` | number field (minutes) | optional | 0 | — | — | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no … | `createResource` body |
| Cleaning policy `cleaningPolicy` | group | optional | — | — | — | How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`. | `createResource` body |
| Mode `cleaningPolicy.mode` | segmented control | required | — | After every booking · Times per day | — | — | `createResource` body |
| Buffer minutes `cleaningPolicy.bufferMinutes` | number field (minutes) | required | — | min 5; max 240 | — | Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct). | `createResource` body |
| Cleanings per day `cleaningPolicy.cleaningsPerDay` | stepper or slider | optional | — | min 1; max 24 | — | Required for `timesPerDay`; ignored for `afterEveryBooking`. | `createResource` body |
| Window start `cleaningPolicy.windowStart` | time picker | optional | — | — | HH:mm, 24-hour | Venue-local time the cleaning window opens. Null means the resource's opening time. | `createResource` body |
| Window end `cleaningPolicy.windowEnd` | time picker | optional | — | — | HH:mm, 24-hour | Venue-local time the cleaning window closes. Null means the resource's closing time. | `createResource` body |
| Requires qualification `requiresQualification` | list of values (chips) | optional | — | — | — | Qualification codes a person must hold to be assigned to this. | `createResource` body |
| Deposit amount `depositAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResource` body |
| Status `status` | radio group | optional | — | Available · Booked · Checked out · Maintenance · Retired | — | — | `createResource` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `createResource` body |
| Resource type `resourceTypeId` | picker: choose a resource type | optional | — | — | shows names, sends the id | The configurable resource type (`resources.resource_type`, 4 October 2026, CHG-FXC-003). | `createResource` body |

Errors to draw in the form: 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Kind as chips (multi), availability window (from-to date-time), search by name or code; no free-text kind field. *(source: contracts/satellite/resources.yaml#listResources)*
- **New resource**: Kind first (it decides the attribute fields: capacity, size, shade, power, poolside), code and name, parent (a cabana under its pool area), setup and teardown minutes, cleaning policy, required qualifications (for instructor/staff kinds, with the staff member picked), deposit in AED. No id or scopePath fields (VO-R03). *(source: contracts/satellite/resources.yaml#createResource)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource** (data table, from `listResources`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |

**Data table** (data table): Status column carries the reason — **booked and under repair need different responses from somebody looking for something free**

**The selected resource** (detail panel, from `listResources`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Attributes | grouped details | Configurable per kind — capacity, size, shade, power, poolside. |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |
| Deposit amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create resource (primary button) | `createResource` POST `/resources` | Resource | Resource | 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September). | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource list**: Code, name, kind icon, parent, status with reason (Available, Booked until 16:00, Checked out to guest, Maintenance - pump fault, Retired), next booking. *(source: contracts/satellite/resources.yaml#listResources / screens/P08-venue-back-office.yaml#BO-095)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open calendar / qualifications / check-out**: Goes to BO-096, BO-098 or BO-097 with the resource selected. *(source: screens/P08-venue-back-office.yaml#BO-095)*

**Data it reads**: `listResources` (onLoad, Resources with status)

**Where the user goes next**

- → `BO-096` Resource Calendar: *Resource Calendar*; carries `resourceId`
- → `BO-097` Check Out & Check In: *Check Out & Check In*
- → `BO-098` Qualifications: *Qualifications*; carries `resourceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | List skeleton; the count renders first |
| Error (`?state=error`) | Could not load resources. Existing bookings are unaffected. |
| Empty, first run (`?state=emptyFirstRun`) | No bookable resources yet. **A cabana sold as a product sells a slot** — define the object here and it becomes something a guest can be handed and can return. |
| Empty, no results (`?state=emptyNoResults`) | No resource matches this kind or window. Widen the window rather than the kind — availability moves, definitions do not. |
| Permission denied (`?state=emptyNoAccess`) | You do not have `RESOURCE_VIEW`. The list is not empty. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_MANAGE` for `createResource`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September). |

#### Consistency with other screens

- Match `BO-855`: Resource types, categories and profiles on the resource board must use the same kinds and attributes.
- Match `BO-069`: An asset is maintenance's view of a physical item; a resource is what is booked. Link, do not duplicate.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resources:
- code: CAB-B09
  name: Cabana B09
  kind: Cabana
  parent: Beach
  status: Booked until 17:00
  next: Sat 10 Oct 10:00
- code: STR-012
  name: Stroller 12
  kind: Stroller
  status: Checked out to Sara Al Nuaimi
- code: INS-SKI-04
  name: Maria Santos
  kind: Instructor
  status: Available
  quals: Ski L3, First aid
- code: VEH-SUV-02
  name: SUV 2 (Dubai 45821)
  kind: Vehicle
  status: Maintenance - tyre
```

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `createResource` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** You do not have `RESOURCE_VIEW`. The list is not empty. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_MANAGE` for `createResource`.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.1 | The system should allow management of all types of resources: - Areas with limited capacity (e.g. Meeting rooms, Cabanas, etc.) - Staff (e.g. Ski School Instructors, etc.) - Objects (e.g. Strollers … | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.2 | The system should allow easy creation and tracking of resources, and link them to individual attraction experiences, so that a ticket is not only based on available time-slots but also on relevant … | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.14 | Ability to define resources required for each event along with the availability schedule. The resources could be of any type: | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.15 | Venues & Spaces: Auditoriums, halls, rooms, stages, breakout areas. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.16 | Equipment & Assets: AV systems, lighting, sound systems, projectors, chairs, booths. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.17 | Staff & Personnel: Event managers, ushers, security, performers, technical crew, mascots, hosts. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.23 | System shall support configurable resource types including staff, venues, equipment, rooms and rental items. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.24 | System shall support categorization of resources. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.25 | System shall support parent-child resource relationships. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.26 | System shall support configurable resource attributes. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.67 | System shall provide resource utilization dashboards. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.68 | System shall provide resource cost analytics. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-095` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-095?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create resource.
- [ ] Every transition is wired: `BO-096`, `BO-097`, `BO-098`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptVenueLabelProposals": {"method":"POST","path":"/venue-maps/{mapId}/proposals","contract":"venue-map","summary":"Accept, edit or reject what the assistant suggested","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VenuePoint"},
"acceptWalkwayProposals": {"method":"POST","path":"/venue-maps/{mapId}/walkway-proposals","contract":"venue-map","summary":"Accept or reject proposed walkways","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GraphValidation"},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createAsset": {"method":"POST","path":"/assets","contract":"maintenance","summary":"Register an asset","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAssetRequest","responds":"Asset"},
"createMaintenancePlan": {"method":"POST","path":"/maintenance-plans","contract":"maintenance","summary":"Create a planned maintenance schedule","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MaintenancePlan","responds":"MaintenancePlan"},
"createResource": {"method":"POST","path":"/resources","contract":"resources","summary":"Define a bookable resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"createVenueMap": {"method":"POST","path":"/venue-maps","contract":"venue-map","summary":"Start a map","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueMap","responds":"VenueMap"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getAsset": {"method":"GET","path":"/assets/{assetId}","contract":"maintenance","summary":"Read an asset with history and documents","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AssetDetail"},
"getAssetHistory": {"method":"GET","path":"/assets/{assetId}/history","contract":"maintenance","summary":"Service history","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getDueMaintenance": {"method":"GET","path":"/maintenance-plans/due","contract":"maintenance","summary":"Planned tasks due or overdue","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"withinDays","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null}],"requestBody":null,"responds":"DueMaintenanceTask"},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getVenueMapGraph": {"method":"GET","path":"/venue-maps/{mapId}/graph","contract":"venue-map","summary":"The navigation graph, ready to route over","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"draft","in":"query","required":null},{"name":"stepFreeOnly","in":"query","required":null}],"requestBody":null,"responds":"VenueMapGraph"},
"getVenueMapImportJob": {"method":"GET","path":"/venue-maps/{mapId}/import/{jobId}","contract":"venue-map","summary":"Import progress and findings","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueMapImportJob"},
"getVenueNavigationFile": {"method":"GET","path":"/venue-maps/{mapId}/navigation-file","contract":"venue-map","summary":"The map's graph and points as a navigation file","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":false}],"requestBody":null,"responds":"VenueNavigationFile"},
"importVenueGeometry": {"method":"POST","path":"/venue-maps/{mapId}/import","contract":"venue-map","summary":"Read a drawing into shapes","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMaintenancePlans": {"method":"GET","path":"/maintenance-plans","contract":"maintenance","summary":"List planned maintenance schedules","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueMaps": {"method":"GET","path":"/venue-maps","contract":"venue-map","summary":"Maps for this venue","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueMap"},
"lookupAsset": {"method":"GET","path":"/assets/lookup","contract":"maintenance","summary":"Find an asset by tag or QR","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assetTag","in":"query","required":null},{"name":"serialNumber","in":"query","required":null}],"requestBody":null,"responds":"AssetDetail"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"proposeVenueLabels": {"method":"POST","path":"/ai/venue-map/{mapId}/propose-labels","contract":"ai","summary":"Suggest what each extracted shape is","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"proposeWalkways": {"method":"POST","path":"/ai/venue-map/{mapId}/propose-walkways","contract":"ai","summary":"Find walkable space in a drawing that has no vectors","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishVenueMap": {"method":"POST","path":"/venue-maps/{mapId}/publish","contract":"venue-map","summary":"Make the draft the one guests see","permission":"VENUE_MAP_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VenueMap"},
"recordAuthorityNotification": {"method":"POST","path":"/incidents/{incidentId}/notify-authority","contract":"maintenance","summary":"Record notification to an external authority","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"reportIncident": {"method":"POST","path":"/incidents","contract":"maintenance","summary":"Report an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportIncidentRequest","responds":"Incident"},
"resolveSyncRejection": {"method":"POST","path":"/sync/rejections/{rejectionId}/resolve","contract":"orders","summary":"Record what was done about a refused entry","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResolveSyncRejectionRequest","responds":"SyncRejection"},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"},
"setPathClosure": {"method":"POST","path":"/venue-maps/{mapId}/paths/{pathId}/closure","contract":"venue-map","summary":"Close a route during works or an incident","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PathClosureResult"},
"setPlacedResource": {"method":"POST","path":"/venue-maps/{mapId}/resources","contract":"venue-map","summary":"Place or amend a bookable resource on the map","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetPlacedResourceRequest","responds":"PlacedResource"},
"setVenueMapArtwork": {"method":"POST","path":"/venue-maps/{mapId}/artwork","contract":"venue-map","summary":"Set the illustrated map guests see, and how it lines up with the plan","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VenueMap"},
"setVenuePoint": {"method":"POST","path":"/venue-maps/{mapId}/points","contract":"venue-map","summary":"Place or amend a point of interest","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetVenuePointRequest","responds":"VenuePoint"},
"updateAsset": {"method":"PATCH","path":"/assets/{assetId}","contract":"maintenance","summary":"Amend an asset","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Asset"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate, close or reopen an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"updateMaintenancePlan": {"method":"PATCH","path":"/maintenance-plans/{planId}","contract":"maintenance","summary":"Amend or suspend a plan","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MaintenancePlan"},
"validateVenueMapGraph": {"method":"POST","path":"/venue-maps/{mapId}/validate-graph","contract":"venue-map","summary":"What is unreachable, before anyone publishes it","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GraphValidation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetCriticality": {"type":"string","enum":["safetyCritical","revenueCritical","standard","low"]},
"AssetDetail": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/Asset"},{"type":"object","properties":{"openWorkOrders":{"type":"array","items":{"$ref":"#/components/schemas/WorkOrder"}},"maintenancePlans":{"type":"array","items":{"$ref":"#/components/schemas/MaintenancePlan"}},"documents":{"type":"array","description":"Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n","items":{"$ref":"#/components/schemas/AssetDocument"}}}}]},
"AssetDocument": {"x-ticvai-persistence":"maintenance.asset_document","type":"object","description":"A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n","required":["id","assetId","ref"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200,"nullable":true},"kind":{"allOf":[{"$ref":"#/components/schemas/AssetDocumentKind"}],"nullable":true,"description":"Null where the document arrived as a bare ref in `documentRefs`."}}},
"AssetDocumentInput": {"x-ticvai-persistence":"none — request only","type":"object","required":["ref","kind"],"properties":{"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/AssetDocumentKind"}}},
"AssetDocumentKind": {"type":"string","enum":["manual","sop","certificate","warranty","drawing","riskAssessment"]},
"AssetHistoryEntry": {"x-ticvai-persistence":"none — union view over work orders, inspections, incidents and asset status changes","type":"object","description":"**Every kind has a source.** `workOrder` is a work-order row, `inspection` an inspection, `incident` an incident, `statusChange` a `maintenance.asset_status_change` row. `partReplaced` is a completed work order whose `resolutionCode` is `partReplaced`, and `planCompleted` a completed work order with a `sourcePlanId` — both read from `maintenance.work_order`, not stored twice.\n","required":["kind","occurredAt","summary"],"properties":{"kind":{"type":"string","enum":["workOrder","inspection","incident","statusChange","partReplaced","planCompleted"]},"referenceId":{"type":"string","format":"uuid","nullable":true,"description":"The source row's id: a work order, inspection or incident, or an `asset_status_change` id. A uuid, as every id is (ADR-0056).\n"},"summary":{"type":"string"},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"DueMaintenanceTask": {"x-ticvai-persistence":"none — computed","type":"object","required":["planId","assetId","assetName","dueAt","isOverdue","criticality"],"properties":{"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"assetName":{"type":"string"},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"dueAt":{"type":"string","format":"date-time"},"isOverdue":{"type":"boolean"},"daysOverdue":{"type":"integer"},"triggeredBy":{"type":"string","enum":["interval","usage"]},"workOrderId":{"type":"string","format":"uuid","nullable":true}}},
"GraphValidation": {"type":"object","description":"**What breaks before a guest finds it.** Run at publish and on demand.\n","required":["isValid","components"],"properties":{"isValid":{"type":"boolean"},"components":{"type":"integer"},"unreachablePoints":{"type":"array","description":"No path at all. **Usually a point placed after the paths were drawn.**","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"}}}},"stepOnlyPoints":{"type":"array","description":"Reachable, and only by steps. **The map works perfectly until a wheelchair user opens it**, and nothing in the drawing makes this visible — which is the whole reason for this list.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"deadEndPaths":{"type":"array","items":{"type":"string","format":"uuid"}},"criticalUnreachable":{"type":"array","description":"**First aid, emergency exits and assembly points that cannot be reached.** Separated from the rest because an unreachable gift shop is a defect and an unreachable assembly point is a safety finding, and a single list of two hundred items buries it.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"}}}},"resourceFindings":{"type":"array","description":"**Placed resources a guest could not buy** (rev 3 REV3-15), named by label. Any entry here makes `isValid` false, and `publishVenueMap` refuses with the matching blocker.\n","items":{"type":"object","required":["placedResourceId","label","reason"],"properties":{"placedResourceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"reason":{"type":"string","enum":["resourceUnlinked","resourcePriceBandMissing","duplicateResourceLabel"]}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"kind":{"type":"string","enum":["note","statusChange","escalation","reopen"],"default":"note","description":"**Every change is logged here** (CHG-RUL-011): an investigator's note, or a row the server writes for a status change, an escalation or a reopen, with `note` as its reason.\n"},"fromStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"toStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."},"role":{"type":"string","nullable":true,"enum":["injured","involved","witness","reporter",null],"description":"The person's part in the incident, from `addIncidentPerson` (CHG-RUL-013)."},"contactStored":{"type":"boolean","readOnly":true,"description":"Whether a contact is held for the person: only with their consent to be contacted (`AddIncidentPersonRequest.contactConsent`; CHG-RUL-013).\n"}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive","model3d"],"description":"`model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. No rendition or derivative is generated for it; the guest app downloads the file as uploaded.\n"},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PathClosureResult": {"description":"What `setPathClosure` returns: the path, and **what a forced closure cut off**, named.\n","allOf":[{"$ref":"#/components/schemas/VenuePath"},{"type":"object","properties":{"strandedPoints":{"type":"array","readOnly":true,"description":"Points no longer reachable because of this closure. Empty unless `force` was used.\n","items":{"$ref":"#/components/schemas/StrandedPoint"}}}}]},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"ReportIncidentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","kind","severity","venueId","description","occurredAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"description":{"type":"string","minLength":3,"maxLength":10000},"involvedSubjectIds":{"type":"array","description":"Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n","items":{"type":"string","format":"uuid"}},"involvedStaffPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"witnessCount":{"type":"integer"},"firstAidGiven":{"type":"boolean","default":false},"emergencyServicesCalled":{"type":"boolean","default":false},"attachmentRefs":{"type":"array","items":{"type":"string"}},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"ResolveSyncRejectionRequest": {"type":"object","x-ticvai-persistence":"none — request only; lands on sync.rejection","required":["resolution","resolvedRecordId"],"properties":{"resolution":{"type":"string","enum":["posted","voided","refunded"],"description":"`posted` — the sale was entered with `createOrder` (F33 step 8); `voided` — with `voidOrder`; `refunded` — with `createRefund`.\n"},"resolvedRecordId":{"type":"string","format":"uuid","description":"The id of the order, void or refund that resolution produced."},"note":{"type":"string","maxLength":500,"nullable":true}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003). `kind` is the fixed family a type belongs to; this is the tenant's own type within it, and the `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it."}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}},
"SetPlacedResourceRequest": {"description":"What `setPlacedResource` takes: a `PlacedResource` without its server-owned fields. **`placedResourceId` absent places a new one; present amends that one**, as `setVenuePoint`.\n","allOf":[{"$ref":"#/components/schemas/PlacedResource"},{"type":"object","properties":{"placedResourceId":{"type":"string","format":"uuid","nullable":true,"description":"The placed resource to amend. Absent or null places a new one."}}}]},
"SetVenuePointRequest": {"description":"What `setVenuePoint` takes: a `VenuePoint` without its server-owned fields, plus the point to amend. **`pointId` absent places a new point; present amends that one**, and it must be a point on the map in the path.\n","allOf":[{"$ref":"#/components/schemas/VenuePoint"},{"type":"object","properties":{"pointId":{"type":"string","format":"uuid","nullable":true,"description":"The point to amend. Absent or null places a new point."}}}]},
"StrandedPoint": {"type":"object","x-ticvai-persistence":"none — computed from the graph","required":["pointId","name","kind","isCritical"],"properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"},"isCritical":{"type":"boolean","description":"First aid, an emergency exit or an assembly point, the same set as `GraphValidation.criticalUnreachable`. **The one the operator must read first.**\n"}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"},"modelAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"**The 3D layer of the working draft** (ADR-0069, contract item closed 3 October 2026): the GLB (`model3d` asset) the last `glbModel` import brought in. Set by `importVenueGeometry`, never by sending a value. Null for a 2D-only map, which is the default and needs nothing. The 3D model is a rendering of the map, never the source of its truth: routes come from the graph.\n"},"navigationFileAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"The navigation file imported with the model, kept so the import can be re-run and audited."},"modelTransform":{"readOnly":true,"description":"**How the model's local frame sits on the earth** (ADR-0069 section 3): the navigation file's anchor, stored once and used both ways. Null without a model. It maps onto the plan's georeference as the ADR says, so a map with a model is georeferenced.\n","allOf":[{"$ref":"#/components/schemas/VenueModelTransform"}]},"model3dStatus":{"type":"string","readOnly":true,"enum":["none","publishable","blocked"],"description":"**Whether the next publish carries the 3D layer.** `none`: no model. `publishable`: the last model import had no `error` finding. `blocked`: it had one (over 300,000 triangles at LOD0, uncompressed textures, a control point more than 10 m out, an invalid navigation file), named in that job's `model.findings`; the 2D map still publishes and guests see 2D until a corrected model is imported (ADR-0069 sections 3 and 6).\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}},"model3d":{"nullable":true,"description":"**The 3D layer of the version read** (ADR-0069; 3 October 2026, r1 additions). Null when that version has none, and then the guest app shows the 2D map with the same route, as it does on a phone that cannot hold 30 fps.\n","allOf":[{"$ref":"#/components/schemas/VenueModel3d"}]}}},
"VenueMapGraph": {"type":"object","description":"19.2.56. **What a client needs to route, and nothing more.** Small enough to cache, versioned so a stale route is detectable.\n","required":["mapId","version","nodes","edges"],"properties":{"mapId":{"type":"string","format":"uuid"},"version":{"type":"integer","description":"**Bumped by a publish or a closure**, and stored as `VenueMap.graphVersion`. A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"},"generatedAt":{"type":"string","format":"date-time"},"nodes":{"type":"array","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"x":{"type":"number"},"y":{"type":"number"},"kind":{"type":"string"},"isStepFree":{"type":"boolean"}}}},"edges":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"uuid"},"to":{"type":"string","format":"uuid"},"distanceMetres":{"type":"number"},"isStepFree":{"type":"boolean"},"throughPointId":{"type":"string","nullable":true,"description":"Where an access point restricts this edge. **The direction lives on that point**, not here, so a gate reconfigured to bidirectional changes routing without a map edit.\n"},"isClosed":{"type":"boolean"}}}},"components":{"type":"integer","description":"How many disconnected parts. **One is the answer for a park.** More than one on a map that should be a single site means something is unreachable and the client can say so without walking the graph.\n"}}},
"VenueMapHandMarkedPaths": {"x-ticvai-persistence":"none — part of the importVenueGeometry request","type":"object","description":"**A raster plan (or a scanned PDF) with the walkways marked by hand** (3 October 2026, r1 additions). The import finds the marks and reports them (`VenueMapImportJob.handMarkedPaths`); `ai.proposeWalkways` then proposes a path segment per marked stretch, and each segment is accepted or rejected on its own with `acceptWalkwayProposals`. Nothing becomes a path without a person.\n","properties":{"markColour":{"type":"string","nullable":true,"pattern":"^#[0-9A-Fa-f]{6}$","description":"The marker's colour, where the operator knows it (`#E53935` for a red pen). Absent, the import looks for the strokes that differ from the printed plan.\n"},"note":{"type":"string","nullable":true,"maxLength":300,"description":"Anything the marks mean that the image does not say (\"dashed = staff only\")."}}},
"VenueMapImportJob": {"type":"object","x-ticvai-persistence":"venuemap.import_job","description":"**Two-phase, following `seating.ImportJob`**, and carrying its lesson: a job that finds nothing is not a successful job.\n","required":["id","status","outcome"],"properties":{"id":{"type":"string","format":"uuid"},"mapId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["parsing","previewReady","committed","failed"]},"outcome":{"type":"string","enum":["parsed","parsedWithFindings","nothingFound","noLayersMatched","unreadable"]},"shapesFound":{"type":"integer"},"layersFound":{"type":"array","description":"**Every layer name in the source, decoded.** Shown whether or not extraction worked, so an operator maps a role by reading rather than guessing.\n","items":{"type":"string"}},"unmappedLayers":{"type":"array","items":{"type":"string"}},"manifestRowsRead":{"type":"integer","nullable":true},"resourcesFound":{"type":"integer","nullable":true,"description":"Bookable resource shapes found on the resource layer (rev 3 REV3-15). Null where the map has none.\n"},"resourceRowsJoined":{"type":"integer","nullable":true,"description":"Resource manifest rows that joined a shape and a `resources.Resource`. **The number to check against your own count**, as `manifestRowsJoined` is for seats: 34 cabanas on the plan and 30 joined is four labels that differ.\n"},"manifestRowsJoined":{"type":"integer","nullable":true,"description":"**The number to check against your own count.** A manifest of 396 seats that joins 220 is the digit problem in §4, or a section code that differs by a space — and both look like success without this figure.\n"},"findings":{"type":"array","description":"**Named against the spec**, so a finding maps to a section of `handoff/venue-map-input-spec.md` rather than to a stack trace.\n","items":{"type":"object","required":["code","severity","message"],"properties":{"code":{"type":"string","enum":["duplicateLayerName","geometryOnLayerZero","unmappedLayer","mixedLayerContent","sectionCodeMismatch","digitScriptMismatch","mergedCells","totalRowDetected","manifestSectionMissingFromPlan","planSectionMissingFromManifest","exitLayerNotSplit","noGeoreference","layerNameUndecodable","rasterOnly","resourceLabelMissing","resourceLabelDuplicate","resourceManifestMissingFromPlan","resourcePlanMissingFromManifest","resourceCodeUnmatched","resourcePriceBandUnknown"],"description":"**A closed set, and each one names a rule in the spec.** Free-text findings are findings a drawing office cannot act on. The six `resource*` codes check placed resources (rev 3 REV3-15): a shape with no label, two with one label, a manifest row with no shape or the reverse, a label with no `resources.Resource`, and a price band not in `priceBands`.\n"},"severity":{"type":"string","enum":["error","warning","info"],"description":"**`warning` is the important level here.** `rasterOnly` and `noGeoreference` are warnings — the map still works, with less — and treating them as errors would refuse a venue that sent everything it had.\n"},"message":{"type":"string"},"specSection":{"type":"string","nullable":true,"description":"Which part of the spec covers it — `§2 Layers`, `§4 Digits`."},"affected":{"type":"array","description":"The layers, sections or rows involved. **Named, not counted.**","items":{"type":"string"}}}}},"ocr":{"type":"object","nullable":true,"description":"**What the OCR step read** off a scanned PDF or a raster (3 October 2026, r1 additions). Null for a vector source or with `ocr.mode: off`. Each block sits on the plan, so `ai.proposeVenueLabels` can use the text near a shape as a hint; the text names nothing by itself. Low-confidence blocks are returned, not dropped.\n","properties":{"pagesRead":{"type":"integer"},"meanConfidence":{"type":"number","minimum":0,"maximum":1,"nullable":true},"textBlocks":{"type":"array","items":{"type":"object","required":["text","confidence"],"properties":{"text":{"type":"string","maxLength":500},"language":{"type":"string","enum":["en","ar"],"nullable":true},"confidence":{"type":"number","minimum":0,"maximum":1},"planX":{"type":"number","nullable":true},"planY":{"type":"number","nullable":true},"widthUnits":{"type":"number","nullable":true},"heightUnits":{"type":"number","nullable":true}}}}}},"handMarkedPaths":{"type":"object","nullable":true,"description":"**The hand-marked strokes the import found** on a raster plan sent with `handMarkedPaths` (3 October 2026, r1 additions). `ai.proposeWalkways` reads them and proposes one segment per marked stretch; nothing is a path until a person accepts it.\n","properties":{"strokesFound":{"type":"integer"},"markColourUsed":{"type":"string","nullable":true,"description":"The colour the import matched."},"totalLengthUnits":{"type":"number","nullable":true,"description":"In drawing units."}}},"model":{"type":"object","nullable":true,"description":"**The GLB and navigation file, measured** (`glbModel` and `navigationFile` imports; ADR-0069 sections 1, 2, 3 and 6; 3 October 2026). Every budget line is a number, so an over-budget model is a finding a 3D studio can act on, not a slow app. Null for any other source.\n","properties":{"sizeBytes":{"type":"integer","nullable":true,"description":"The GLB. Over 41","943":null,"040 (40 MB) is refused before import.":null},"lod0TrianglesMaxZone":{"type":"integer","nullable":true,"description":"The most LOD0 triangles any one zone carries, which is what is on screen near the camera. Over 300,000 is an error."},"trianglesTotal":{"type":"integer","nullable":true,"description":"Across every zone and LOD. Over 1,500,000 is a warning."},"drawCalls":{"type":"integer","nullable":true,"description":"Over 150 is a warning."},"textureMemoryBytes":{"type":"integer","nullable":true,"description":"After KTX2 transcoding. Over 128 MB is a warning."},"maxTexturePx":{"type":"integer","nullable":true,"description":"Over 2048 is a warning."},"zones":{"type":"integer","nullable":true},"nodes":{"type":"integer"},"edges":{"type":"integer"},"locations":{"type":"integer"},"anchorResidualMaxMetres":{"type":"number","nullable":true,"description":"The worst control point. Over 3 m warns; over 10 m is an error."},"publishable3d":{"type":"boolean","description":"**True when no finding below is an `error`**: the next publish carries the 3D layer. False keeps it out (`VenueMap.model3dStatus` `blocked`); the 2D map still publishes.\n"},"findings":{"type":"array","items":{"type":"object","required":["code","severity","message"],"properties":{"code":{"type":"string","enum":["modelOverDownloadBudget","zoneOverDownloadBudget","triangleBudgetExceeded","triangleTotalExceeded","drawCallBudgetExceeded","textureBudgetExceeded","textureTooLarge","uncompressedTextures","missingLevelsOfDetail","notMetres","anchorResidualHigh","anchorResidualTooHigh","controlPointsTooClose","unresolvedCatalogueCode","unknownNodeInEdge","locationNodeMissing","navigationFileInvalid","navigationFileMismatch","nodeRefWithoutLocation"],"description":"**A closed set, separate from `findings`** so the plan importer's codes stay as they were. Errors (keep the 3D layer out of the publish): `triangleBudgetExceeded` (over 300,000 at LOD0 in a zone), `uncompressedTextures`, `anchorResidualTooHigh` (over 10 m), `navigationFileInvalid`, `unknownNodeInEdge`, `locationNodeMissing`. Warnings: the other budget lines, `anchorResidualHigh` (over 3 m), `controlPointsTooClose`, `unresolvedCatalogueCode`, `missingLevelsOfDetail`, `notMetres`, `navigationFileMismatch` (venue, map or model file differ). Info: `nodeRefWithoutLocation` (a named GLB node with no location is scenery).\n"},"severity":{"type":"string","enum":["error","warning","info"]},"message":{"type":"string"},"measured":{"type":"number","nullable":true,"description":"The number found."},"limit":{"type":"number","nullable":true,"description":"The budget it was measured against."},"affected":{"type":"array","description":"The zones, nodes, locations or codes involved. Named, not counted.","items":{"type":"string"}}}}}}}}},
"VenueMapOcrOptions": {"x-ticvai-persistence":"none — part of the importVenueGeometry request","type":"object","description":"**The OCR step for a scanned PDF or a raster plan** (3 October 2026, r1 additions). Absent means `auto`: a PDF page with no vector geometry, and every raster, is read for text; a vector page is read by its layers and never OCR'd. The text found is returned on the job (`VenueMapImportJob.ocr`) and offered to `ai.proposeVenueLabels` as hints; it never names a point by itself.\n","properties":{"mode":{"type":"string","enum":["auto","off"],"default":"auto","description":"`off` skips it, for a plan whose text is noise (a dimensioned drawing)."},"languages":{"type":"array","items":{"type":"string","enum":["en","ar"]},"description":"The scripts to read. Absent means both."}}},
"VenueModel3d": {"type":"object","x-ticvai-persistence":"none — jsonb column","description":"**The 3D layer a guest app loads** (ADR-0069): the model and the transform of the version it read. The app downloads the GLB through the asset delivery rules (UAE-hosted for a UAE tenant, ADR-0069 section 7) and caches it with the graph.\n","required":["modelAssetId","transform"],"properties":{"modelAssetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.MediaAsset"},"sizeBytes":{"type":"integer","nullable":true},"transform":{"$ref":"#/components/schemas/VenueModelTransform"}}},
"VenueModelTransform": {"type":"object","x-ticvai-persistence":"none — jsonb column","description":"ADR-0069 section 3: the navigation file's `anchor`. Local to WGS84: rotate (x, z) by `headingDegrees` into east/north metres, scale, offset from the origin on a local tangent plane; GPS to local is the inverse, done on the phone for every fix.\n","required":["originLat","originLng","headingDegrees"],"properties":{"originLat":{"type":"number","minimum":-90,"maximum":90},"originLng":{"type":"number","minimum":-180,"maximum":180},"originAltitudeMetres":{"type":"number","default":0},"headingDegrees":{"type":"number","minimum":0,"exclusiveMaximum":360,"description":"True-north bearing of the model's -Z axis, clockwise."},"scale":{"type":"number","default":1,"description":"Metres per model unit; 1 for a model in metres."},"controlPoints":{"type":"array","minItems":2,"maxItems":8,"description":"Surveyed checks, far apart. They verify the anchor; they do not define it.","items":{"type":"object","required":["label","x","z","lat","lng"],"properties":{"label":{"type":"string"},"x":{"type":"number"},"z":{"type":"number"},"lat":{"type":"number"},"lng":{"type":"number"},"residualMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Measured at import. Over 3 m is a warning; over 10 m blocks the 3D layer."}}}}}},
"VenueNavigationFile": {"x-ticvai-schema-id":"urn:ticvai:venue-navigation-file:1.0","type":"object","x-ticvai-persistence":"none — a file format: imported by importVenueGeometry, exported by getVenueNavigationFile","description":"**The navigation (pathway) file of ADR-0069 section 2**, fixed as a contract schema on 3 October 2026 (the ADR's `$id` open item: `urn:ticvai:venue-navigation-file:1.0`). JSON, UTF-8, one per venue map, in the model's local frame (metres, +Y up). Codes, not ids: `productCode`, `outletCode` and `facilityCode` resolve at import, and an unresolved code is a finding (`unresolvedCatalogueCode`), never a silent drop. Point names stay unique per venue (audit R108).\n","required":["formatVersion","venueCode","mapName","anchor","nodes","edges","locations"],"properties":{"formatVersion":{"type":"string","enum":["1.0"]},"venueCode":{"type":"string","description":"The venue's code on the platform."},"mapName":{"type":"string","description":"Matches VenueMap.name; a floor plan is its own file."},"floorLevel":{"type":"integer","nullable":true},"modelFile":{"type":"string","nullable":true,"description":"The GLB this file belongs to (park-2026-10.glb). Null in a file exported from a 2D map."},"anchor":{"$ref":"#/components/schemas/VenueModelTransform"},"nodes":{"type":"array","minItems":2,"description":"Graph vertices in model coordinates. A junction, or the door of a location.","items":{"type":"object","required":["id","x","z"],"properties":{"id":{"type":"string","pattern":"^[A-Za-z0-9_-]{1,64}$"},"x":{"type":"number"},"y":{"type":"number","default":0},"z":{"type":"number"},"zone":{"type":"string","nullable":true,"description":"The GLB zone node it sits in."}}}},"edges":{"type":"array","minItems":1,"description":"Walkable connections. Undirected; a one-way passage names the access point that makes it one-way.","items":{"type":"object","required":["from","to"],"properties":{"from":{"type":"string"},"to":{"type":"string"},"polyline":{"type":"array","description":"Intermediate [x, z] or [x, y, z] points along the centreline; straight when absent.","items":{"type":"array","minItems":2,"maxItems":3,"items":{"type":"number"}}},"isStepFree":{"type":"boolean","default":true},"isIndoor":{"type":"boolean","default":false},"throughAccessPointCode":{"type":"string","nullable":true}}}},"locations":{"type":"array","description":"Points of interest. Each becomes a VenuePoint.","items":{"type":"object","required":["ref","kind","name","nodeId"],"properties":{"ref":{"type":"string","description":"Stable key; also the name of the GLB node drawn for it."},"kind":{"type":"string","description":"One of VenuePoint.kind; junction is not allowed here."},"name":{"type":"string"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"nodeId":{"type":"string","description":"The node a guest is routed to: the entrance, not the centre."},"labelPosition":{"type":"array","minItems":3,"maxItems":3,"items":{"type":"number"}},"catalogue":{"type":"object","properties":{"productCode":{"type":"string","nullable":true},"outletCode":{"type":"string","nullable":true},"facilityCode":{"type":"string","nullable":true}}}}}}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]}
}
```
