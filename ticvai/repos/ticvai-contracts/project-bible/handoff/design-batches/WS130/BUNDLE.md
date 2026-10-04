# WS130 — Event Management Configuration Backend Structure v1.0 board 6

**6 screens · 6 operations · 6 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `EVENT_CONFIGURE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-710` | Event Resource Command Center | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-711` | Event Resource Requirement Configuration | B | 0 | 20 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-712` | Staff & Role Assignment Configuration | B | 0 | 40 | 6 | 9 | 0 | 5 | — | notStarted (—) |
| `BO-713` | Contractor & External Workforce Configuration | B | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-714` | Event Shift & Roster Configuration | D | 13 | 24 | 6 | 10 | 0 | 6 | — | notStarted (—) |
| `BO-715` | Resource Location & Deployment Configuration | B | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-710, BO-711, BO-713, BO-715 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-710` Event Resource Command Center

**See everything an event needs (staff, equipment, spaces) and whether each has been secured.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29919 (VM-BO-710) |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/sell/event-resource-command-center-bo-710` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether each upcoming event can actually run: its resource plan (rooms, equipment, staff, contractors) and readiness (not planned, planning, at risk, ready), across the three contracts that hold them.

**Fixed on main** (the package already carries these; draw what it says): The purpose text is shared word for word with BO-694, BO-697, BO-700, BO-703 and others and does not describe this screen (Event Resource … (CHG-WIR-026).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **readiness**: Events as rows with a readiness badge and the count of requirements not yet secured; at-risk first. *(source: contracts/spine/catalogue.yaml#getEventResourcePlan)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-711` Event Resource Requirement Configuration: *Event Resource Requirement Configuration*; carries `eventId`
- → `BO-712` Staff & Role Assignment Configuration: *Staff & Role Assignment Configuration*; carries `eventId`
- → `BO-713` Contractor & External Workforce Configuration: *Contractor & External Workforce Configuration*; carries `eventId`
- → `BO-714` Event Shift & Roster Configuration: *Event Shift & Roster Configuration*
- → `BO-715` Resource Location & Deployment Configuration: *Resource Location & Deployment Configuration*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
events:
- event: Gulf Attractions Summit
  readiness: atRisk
  unsecured: 2 AV technicians, 1 interpreter
```

#### Permissions

- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-710` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-710`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 1: Opens Event Resource Command Center → Provide management with a consolidated backend view of the financial, commercial, sponsorship, attendance and operational performance of events.
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F239 branch at step 1 (expected): when Nothing has been set up on Event Resource Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F239 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-710?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-711`, `BO-712`, `BO-713`, `BO-714`, `BO-715`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-711` Event Resource Requirement Configuration

**List the resources an event needs (staff, equipment and spaces) with quantities and times.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29920 (VM-BO-711) |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/sell/event-resource-requirement-configuration-bo-711` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** State what an event needs, by role and by kind, with two assignment models: pre-assigned (a named room, vehicle or instructor per slot) or dynamic (type and quantity, assigned at sale).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setEventResourcePlan and nothing that returns the current configuration. (CHG-WIR-025); The purpose text is shared word for word with BO-701, BO-704, BO-717, BO-721 and does not describe this screen (Event Resource Requirement … (CHG-WIR-026).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **requirements**: Rows of kind, role or item, quantity, when, and assignment model (pre-assigned or dynamic). *(source: contracts/spine/catalogue.yaml#setEventResourcePlan / DI-482)*

#### Outputs: what the screen shows and produces

**Shown**

**Everything an event needs, and whether it has been secured** (detail panel, from `getEventResourcePlan`)

| Shows | Format | Notes |
|---|---|---|
| Event | the name it points at, never the id | — |
| Requirements | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Space, Equipment, Staff, Contractor, Vehicle, Service | — |
| Resource type | the name it points at, never the id | — |
| Role code | text | — |
| Quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Location scope path | text | — |
| Secured count | 1,234 | — |
| Status | chip: Required, Partially secured, Secured, At risk | — |
| Bookings | list or chips (count when long) | — |
| Contractors | list or chips (count when long) | — |
| Organisation | the name it points at, never the id | — |
| Role | text | — |
| Headcount | 1,234 | — |
| Accreditation programme | the name it points at, never the id | — |
| Insurance verified | yes / no (icon or chip) | — |
| Readiness | chip: Not planned, Planning, At risk, Ready | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save event resource plan (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getEventResourcePlan` (onLoad, Everything an event needs, and whether it has been secured)

**Where the user goes next**

- → `BO-710` Event Resource Command Center: *Back to Event Resource Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource requirement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource requirement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource requirement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource requirement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requirements:
- kind: vehicle
  item: 4x4 SUV
  quantity: 3
  model: dynamic
- kind: staff
  role: Safari guide
  quantity: 3
```

#### Permissions

- `setEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-711` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-711`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 2: Works in Event Resource Requirement Configuration → Configure the financial plan and budget against which event performance will be measured.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-711?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save event resource plan, Cancel.
- [ ] Every transition is wired: `BO-710`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-712` Staff & Role Assignment Configuration

**Set the staff roles an event needs and assign people to them on the rota.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29921 (VM-BO-712) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/sell/staff-role-assignment-configuration-bo-712` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Put people on the event's rota by role: who works which position when. An assignment is refused where the person overlaps another assignment or lacks the role.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setEventResourcePlan, createRotaAssignment and nothing that returns the current configuration. (CHG-WIR-025); The purpose text is shared word for word with BO-705, BO-718 and does not describe this screen (Staff & Role Assignment Configuration). (CHG-WIR-026).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Everything an event needs, and whether it has been secured** (detail panel, from `getEventResourcePlan`)

| Shows | Format | Notes |
|---|---|---|
| Event | the name it points at, never the id | — |
| Requirements | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Space, Equipment, Staff, Contractor, Vehicle, Service | — |
| Resource type | the name it points at, never the id | — |
| Role code | text | — |
| Quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Location scope path | text | — |
| Secured count | 1,234 | — |
| Status | chip: Required, Partially secured, Secured, At risk | — |
| Bookings | list or chips (count when long) | — |
| Contractors | list or chips (count when long) | — |
| Organisation | the name it points at, never the id | — |
| Role | text | — |
| Headcount | 1,234 | — |
| Accreditation programme | the name it points at, never the id | — |
| Insurance verified | yes / no (icon or chip) | — |
| Readiness | chip: Not planned, Planning, At risk, Ready | — |

**The rota** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |
| Note | text | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save event resource plan (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Assign**: Refused with the clash named (overlapping shift or missing role); otherwise added as planned. *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*

**Data it reads**: `getEventResourcePlan` (onLoad, Everything an event needs, and whether it has been secured); `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `BO-710` Event Resource Command Center: *Back to Event Resource Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff role list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff role untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff role yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staff role are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role |

#### Consistency with other screens

- Match `BO-711`: Staff requirements from the plan appear as open positions to fill.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
assignment:
  person: Rashid Khan
  position: Usher, Hall B
  from: 14 Nov 17:00
  to: 14 Nov 23:00
```

#### Permissions

- `setEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-712` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-712`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 4: Works in Staff & Role Assignment Configuration → Define how financial performance should be measured and attributed to an event.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-712?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save event resource plan, Cancel.
- [ ] Every transition is wired: `BO-710`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-713` Contractor & External Workforce Configuration

**Plan the contractors and external workers an event needs, as part of its resource plan.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29922 (VM-BO-713) |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/sell/contractor-external-workforce-configuration-bo-713` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** External contractors and their staff an event relies on (security, AV, catering), recorded in the event's resource plan with what they supply.

**Fixed on main** (the package already carries these; draw what it says): The purpose describes sponsors and sponsorship agreements, not contractors. (CHG-WIR-026); No read operation: the screen declares only setEventResourcePlan and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **contractors**: Company, service, headcount, contact, confirmed or not. *(source: contracts/spine/catalogue.yaml#setEventResourcePlan)*

#### Outputs: what the screen shows and produces

**Shown**

**Every contractor external workforce** (data table)

| Shows | Format | Notes |
|---|---|---|
| Contracted → scheduled → delivered → verified | text | not in the schema: `Contracted → Scheduled → Delivered → Verified` |

**Everything an event needs, and whether it has been secured** (detail panel, from `getEventResourcePlan`)

| Shows | Format | Notes |
|---|---|---|
| Event | the name it points at, never the id | — |
| Requirements | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Space, Equipment, Staff, Contractor, Vehicle, Service | — |
| Resource type | the name it points at, never the id | — |
| Role code | text | — |
| Quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Location scope path | text | — |
| Secured count | 1,234 | — |
| Status | chip: Required, Partially secured, Secured, At risk | — |
| Bookings | list or chips (count when long) | — |
| Contractors | list or chips (count when long) | — |
| Organisation | the name it points at, never the id | — |
| Role | text | — |
| Headcount | 1,234 | — |
| Accreditation programme | the name it points at, never the id | — |
| Insurance verified | yes / no (icon or chip) | — |
| Readiness | chip: Not planned, Planning, At risk, Ready | — |

**The selected contractor external workforce** (detail panel): The pack groups this record's detail under its own headings: “Sponsorship levels may include”.

| Shows | Format | Notes |
|---|---|---|
| Contracted → scheduled → delivered → verified | text | not in the schema: `Contracted → Scheduled → Delivered → Verified` |

**Data it reads**: `getEventResourcePlan` (onLoad, Everything an event needs, and whether it has been secured)

**Where the user goes next**

- → `BO-710` Event Resource Command Center: *Back to Event Resource Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contractor external workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contractor external workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contractor external workforce yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contractor external workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
contractors:
- company: Gulf Secure LLC
  service: Security
  headcount: 24
  confirmed: true
```

#### Permissions

- `setEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-713` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-713`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 6: Works in Contractor & External Workforce Configuration → Manage sponsors and sponsorship agreements associated with events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-713?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-710`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-714` Event Shift & Roster Configuration

**Plan the shifts an event needs and roster the people who will work them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block D · task VM-BO-714 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/event-shift-roster-configuration-bo-714` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Event shift and roster configuration (Event Management board 6, screen 6): for one event and its occurrences, define the shifts the event needs (Setup, Pre-opening, Event, Closing), the roles and headcount each needs, and assign people, then see uncovered positions and overlapping shifts before the roster is published. The one thing to get right: it is a visual shift and roster schedule for an event (by role, person, location and time) built on the shared workforce rota, not a second staff master and not the AI event-creation screen its source currently points at.

**Known correction pending (do not draw the wrong version)**

- **No calendar component** Why: A visual shift/roster schedule is a calendar with Day, Week and Month (VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-714; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Module "Sell" and requiresModule ticketing** Why: It is workforce for events; it belongs with the event resource board (BO-710) and needs the workforce module. *(source: screens/P08-venue-back-office.yaml#BO-714; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen's source is pack page 85 (Screen 06 AI-Assisted Event Creation), and its purpose, columns (AI Proposal, Existing / Approved … (CHG-WIR-003); Bound to setShiftTemplate and getStaffingCoverage only (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does a rota assignment record which event and occurrence it serves (RotaAssignment has no eventId)?** → Drawn default accepted: Show the event name on each bar from the position and time; flag "Event link not stored yet" in the detail. *(decided by Chinmay, 2026-10-02; DEC-488 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |

**Form: Add to roster** (modal, opened by *Add to roster*; *Add to roster* calls `createRotaAssignment`, *Cancel* sends nothing)

**Collects what `createRotaAssignment` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rest period before `restPeriodBefore` | number field | optional | — | — | — | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and unsafe in all of them. | `createRotaAssignment` body |
| Labour cost `labourCost` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. | `createRotaAssignment` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Position `position` | text field | required | — | — | — | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota assignment is not a shift. | `createRotaAssignment` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. | `createRotaAssignment` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. | `createRotaAssignment` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Status `status` | select | optional | — | Planned · Published · Confirmed · Swap pending · Cancelled · Completed · No show | — | — | `createRotaAssignment` body |
| Break minutes `breakMinutes` | number field (minutes) | optional | — | — | — | — | `createRotaAssignment` body |
| Note `note` | text area | optional | — | — | — | — | `createRotaAssignment` body |

Errors to draw in the form: 409 Overlaps an existing assignment, or the person lacks the required role

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Event and occurrence**: Event picker, then occurrence (date and session); "Copy roster to another occurrence" works from this pair. *(source: screens/P08-venue-back-office.yaml#BO-714)*
- **Shift**: Name (Setup Shift, Pre-Opening Shift, Event Shift, Closing Shift or custom), start and end in venue time (crossing midnight shown "+1"), venue and space, required roles with headcount per role, break rules, check-in and check-out time, supervisor, and "Handover required" toggle. *(source: screens/P08-venue-back-office.yaml#BO-714)*
- **Assignment**: Drag a person from the candidate list onto a role slot, or bulk-assign several; each placement is a rota assignment (person, position, start, end, venue). Refusals (overlap, missing role) appear on the slot. *(source: screens/P08-venue-back-office.yaml#BO-714 / contracts/satellite/workforce.yaml#createRotaAssignment)*

#### Outputs: what the screen shows and produces

**Shown**

**Every event shift roster** (data table)

| Shows | Format | Notes |
|---|---|---|
| AI proposal | text | not in the schema: `AI Proposal` |
| Existing / approved configuration | text | not in the schema: `Existing / Approved Configuration` |

**Event roster** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |
| Note | text | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected event shift roster** (detail panel): The pack groups this record's detail under its own headings: “Administrators can”, “Critical Governance Principle”.

| Shows | Format | Notes |
|---|---|---|
| AI proposal | text | not in the schema: `AI Proposal` |
| Existing / approved configuration | text | not in the schema: `Existing / Approved Configuration` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add to roster (secondary button) | `createRotaAssignment` POST `/rota-assignments` | RotaAssignment | RotaAssignment | 409 Overlaps an existing assignment, or the person lacks the required role | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Event roster calendar**: Day view of the occurrence split by hour from the venue day start, rows switchable between Role, Employee, Location and Time; Week and Month for multi-day events (per VO-R01). Uncovered role slots are red outlined boxes with "1 Usher short"; overlapping shifts of one person are flagged on both bars. *(source: screens/P08-venue-back-office.yaml#BO-714)*
- **Coverage strip**: Per shift and role, Required / Rostered / Qualified / Gap with severity in words (Covered, Tight, Short, Blocking). *(source: contracts/satellite/workforce.yaml#getStaffingCoverage)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Copy shift / Copy roster to another occurrence**: Preview of what will be created ("12 assignments on Sun 6 Dec, 2 people unavailable"), then creates them as Planned. *(source: screens/P08-venue-back-office.yaml#BO-714)*
- **Publish event roster**: Blocked while blocking gaps or overlaps remain, with the list; otherwise confirmation names the people who will be notified. Only an authorised exception publishes with gaps. *(source: screens/P08-venue-back-office.yaml#BO-714)*

**Data it reads**: `getStaffingCoverage` (onLoad, Where it is short); `listRotaAssignments` (onLoad, Who is rostered for the event)

**Where the user goes next**

- → `BO-710` Event Resource Command Center: *Back to Event Resource Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event shift roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event shift roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event shift roster yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event shift roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role |

#### Edge cases to draw

- **A person is already on the venue rota at that time**: The drop is refused with "Rahul Menon is on Main Plaza Gate 2 07:00-15:00"; offer Replace or another person. *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*
- **Event occurrence moved after the roster was built**: Banner "Occurrence moved to 19:00; 14 shifts no longer match" with Shift all / Review. *(source: designer default)*

#### Consistency with other screens

- Match `BO-917`: Event staff allocation per role is the same placement; draw BO-917 as the candidate side of this roster (per VO-R14).
- Match `BO-879`: Event shifts are shift templates of kind event; same template picker.
- Match `BO-884`: Same roster grid, required vs scheduled columns and gap wording.
- Match `BO-055`: Every placement is a rota assignment and shows on the venue rota.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Winter Lights Festival, Summit Peaks, Fri 4 Dec 2026
shifts:
- name: Setup Shift
  time: 14:00-17:00
  roles: Technical crew 4, Supervisor 1
- name: Pre-Opening Shift
  time: 17:00-18:00
  roles: Ushers 8, Security 6
- name: Event Shift
  time: 18:00-22:00
  roles: Ushers 8 (7 rostered), Security 6, Hosts 2
- name: Closing Shift
  time: 22:00-23:30
  roles: Security 4, Technical crew 4
```

#### Permissions

- `setShiftTemplate` → `WORKFORCE_MANAGE` (configure) · staff
- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-714` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-714`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 8: Works in Event Shift & Roster Configuration → Allow authorized administrators to use AI to accelerate creation of event configuration from natural-language instructions or existing templates.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-714?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add to roster.
- [ ] Every transition is wired: `BO-710`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-715` Resource Location & Deployment Configuration

**Set where and when each of an event's resources is deployed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | Block B · ticket #29923 (VM-BO-715) |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Configure KPI by; Display) and no metric row |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/sell/resource-location-deployment-configuration-bo-715` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where each resource of an event is deployed (which space, gate or zone) and when, part of the event's resource plan.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setEventResourcePlan and nothing that returns the current configuration. (CHG-WIR-025); The purpose text is shared word for word with BO-698, BO-723 and does not describe this screen (Resource Location & Deployment … (CHG-WIR-026).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **location per requirement**: Picked from spaces (BO-700), not typed. *(source: contracts/spine/catalogue.yaml#setEventResourcePlan)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource location deployment** (data table)

| Shows | Format | Notes |
|---|---|---|
| Target vs actual | text | not in the schema: `Target vs Actual` |

**Everything an event needs, and whether it has been secured** (detail panel, from `getEventResourcePlan`)

| Shows | Format | Notes |
|---|---|---|
| Event | the name it points at, never the id | — |
| Requirements | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Space, Equipment, Staff, Contractor, Vehicle, Service | — |
| Resource type | the name it points at, never the id | — |
| Role code | text | — |
| Quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Location scope path | text | — |
| Secured count | 1,234 | — |
| Status | chip: Required, Partially secured, Secured, At risk | — |
| Bookings | list or chips (count when long) | — |
| Contractors | list or chips (count when long) | — |
| Organisation | the name it points at, never the id | — |
| Role | text | — |
| Headcount | 1,234 | — |
| Accreditation programme | the name it points at, never the id | — |
| Insurance verified | yes / no (icon or chip) | — |
| Readiness | chip: Not planned, Planning, At risk, Ready | — |

**The selected resource location deployment** (detail panel): The pack groups this record's detail under its own headings: “Set”.

| Shows | Format | Notes |
|---|---|---|
| Target vs actual | text | not in the schema: `Target vs Actual` |

**Data it reads**: `getEventResourcePlan` (onLoad, Everything an event needs, and whether it has been secured)

**Where the user goes next**

- → `BO-710` Event Resource Command Center: *Back to Event Resource Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource location deployment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource location deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource location deployment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource location deployment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
deployment:
- item: Mobile stage
  location: Main Arena
  from: 13 Nov 08:00
```

#### Permissions

- `setEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-715` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-715`
- Workshop pack: Event_Management_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F239 *Event Management Configuration Backend Structure v1.0 board 6: Event Resource …*, step 10: Works in Resource Location & Deployment Configuration → Configure measurable operational KPIs for staff, instructors and activity operators.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-715?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-710`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"getEventResourcePlan": {"method":"GET","path":"/events/{eventId}/resource-plan","contract":"catalogue","summary":"Everything an event needs, and whether it has been secured","permission":"EVENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"EventResourcePlan"},
"getStaffingCoverage": {"method":"GET","path":"/staffing-coverage","contract":"workforce","summary":"Where the rota is short, and by how much","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"basis","in":"query","required":null}],"requestBody":null,"responds":"StaffingCoverage"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setEventResourcePlan": {"method":"PUT","path":"/events/{eventId}/resource-plan","contract":"catalogue","summary":"State what the event needs, by role and by kind","permission":"EVENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EventResourcePlan","responds":"EventResourcePlan"},
"setShiftTemplate": {"method":"PUT","path":"/shift-templates","contract":"workforce","summary":"Define a shift pattern, its breaks and its qualifications","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ShiftTemplate","responds":"ShiftTemplate"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"EventResourcePlan": {"type":"object","x-ticvai-persistence":"catalogue.event_resource_plan","description":"Event board 6. **Secured against required is the only number an event manager wants.**\n","properties":{"eventId":{"type":"string","format":"uuid"},"requirements":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["space","equipment","staff","contractor","vehicle","service"]},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"roleCode":{"type":"string","nullable":true},"quantity":{"type":"integer"},"from":{"type":"string","format":"date-time","nullable":true},"to":{"type":"string","format":"date-time","nullable":true},"locationScopePath":{"type":"string","nullable":true},"securedCount":{"type":"integer","readOnly":true},"status":{"type":"string","enum":["required","partiallySecured","secured","atRisk"]},"bookingIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"contractors":{"type":"array","items":{"type":"object","properties":{"organisationId":{"type":"string","format":"uuid"},"role":{"type":"string"},"headcount":{"type":"integer"},"accreditationProgrammeId":{"type":"string","format":"uuid","nullable":true},"insuranceVerified":{"type":"boolean","default":false}}}},"readiness":{"type":"string","readOnly":true,"enum":["notPlanned","planning","atRisk","ready"]},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ShiftTemplate": {"type":"object","x-ticvai-persistence":"workforce.shift_template","description":"Resource board 3.7. **The unit a manager actually thinks in.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["early","late","middle","split","double","night","onCall","overtime"]},"startsAt":{"type":"string"},"endsAt":{"type":"string"},"breaks":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"minutes":{"type":"integer"},"paid":{"type":"boolean","default":false}}}},"requiredQualifications":{"type":"array","items":{"type":"string"}},"roleCode":{"type":"string","nullable":true},"costCentre":{"type":"string","nullable":true},"hourlyRate":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}}
}
```
