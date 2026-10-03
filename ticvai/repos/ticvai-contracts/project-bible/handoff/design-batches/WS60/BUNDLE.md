# WS60 — Ticket Media   Credential Management board 2

**10 screens · 19 operations · 27 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, ORDER_REPRINT, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-344` | Media Design Studio Command Center | C | 8 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-345` | Digital QR & Barcode Ticket Designer | C | 15 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-346` | PDF, Printable & POS Ticket Designer | A | 20 | 8 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-347` | Apple Wallet Pass Designer | C | 24 | 0 | 5 | 0 | 2 | 6 | — | notStarted (generated) |
| `BO-348` | Google Wallet Pass Designer | C | 18 | 0 | 5 | 0 | 2 | 6 | — | notStarted (generated) |
| `BO-349` | RFID, NFC, Card & Wristband Media Designer | C | 20 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-350` | Digital Card, Membership & Wearable Designer | C | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-351` | Dynamic Fields, Data Mapping & Content Builder | C | 7 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-352` | Branding, Localization & Template Inheritance | C | 16 | 12 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-353` | Multi-Media Preview, Testing, Approval & Publication | C | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-344` Media Design Studio Command Center

**Provide administrators with the central workspace for creating and managing all ticket and credential media templates. This should be the entry point for the entire no-code Media Design Studio.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-344 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each template should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/access-venue/media-design-studio-command-center-bo-344` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The entry point of the media design studio: every ticket and credential template, cloned, imported or archived.

**Known correction pending (do not draw the wrong version)**

- **Two template stores (orders ticket templates and access media templates) on one gallery.** Why: Same correction as BO-346. *(source: contracts/spine/access.yaml#archiveMediaTemplate / contracts/spine/orders.yaml#listTicketTemplates; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Media type | text field | — | — | `listMediaDesign` ?mediaType |
| Status | text field | — | — | `listMediaDesign` ?status |
| Brand | text field | — | — | `listMediaDesign` ?brand |
| Venue | text field | — | — | `listMediaDesign` ?venue |
| Media type | select | — | Thermal ticket · A4 pdf · Wristband · RFID card · Wallet pass · QR only · SMS | `listTicketTemplates` ?mediaType |
| Include inactive | toggle | off | — | `listTicketTemplates` ?includeInactive |

**Sent by *Duplicate Existing*** (`cloneTicketTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 120 | — | — | `cloneTicketTemplate` body |
| Source `source` | segmented control | required | — | Existing template · Venue template · Product template | — | What the template in the path is (decided 29 September, readiness close-out). | `cloneTicketTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue whose template is copied. Required for `venueTemplate`. | `cloneTicketTemplate` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | The product the template issues for. Required for `productTemplate`. | `cloneTicketTemplate` body |

**Sent by *Import supported template definition*** (`importTicketTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | text field | required | — | max length 30 | — | The definition format of the file. One the service does not read is a 422. | `importTicketTemplate` body |
| File ref `fileRef` | picker: choose a file ref | required | — | — | shows names, sends the id | The uploaded definition file. | `importTicketTemplate` body |
| Name `name` | text field | required | — | max length 120 | — | — | `importTicketTemplate` body |

**Sent by *Archive media template*** (`archiveMediaTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 500 | — | — | `archiveMediaTemplate` body |

#### Outputs: what the screen shows and produces

**Shown**

**Total Media Templates** (metric tile)

**Published** (metric tile)

**Draft** (metric tile)

**Pending Approval** (metric tile)

**Scheduled** (metric tile)

**Archived** (metric tile)

**QR / Digital Templates** (metric tile)

**PDF / Print Templates** (metric tile)

**Apple Wallet Templates** (metric tile)

**Google Wallet Templates** (metric tile)

**RFID / NFC Templates** (metric tile)

**Card / Wristband Templates** (metric tile)

**Templates Requiring Review** (metric tile)

**Templates with Validation Errors** (metric tile)

**Every media design** (data table, from `listMediaDesign`)

| Shows | Format | Notes |
|---|---|---|
| Template name | text | Template Name |
| Media type | chip: QR ticket, Dynamic QR ticket, Barcode ticket, Mobile ticket, Pdf, A4 A5… | Media the template is for |
| Brand | text | Brand |
| Venue | text | Venue |
| Effective from | 1 Oct 2026, 14:30 | Effective From |
| Status | chip: Draft, Pending approval, Scheduled, Published, Archived | Template status |

**The selected media design** (detail panel): The pack groups this record's detail under its own headings: “Primary action”, “Digital”, “Print”, “Wallet”, “Physical”.

| Shows | Format | Notes |
|---|---|---|
| Template name | text | Template Name |
| Media type | chip: QR ticket, Dynamic QR ticket, Barcode ticket, Mobile ticket, Pdf, A4 A5… | Media the template is for |
| Brand | text | Brand |
| Venue | text | Venue |
| Product event association | text | Product / Event association |
| Language | text | Language |
| Effective from | 1 Oct 2026, 14:30 | Effective From |
| Status | chip: Draft, Pending approval, Scheduled, Published, Archived | Template status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Duplicate Existing (primary button) | `cloneTicketTemplate` POST `/ticket-templates/{templateId}/clone` | CloneTicketTemplateInput | TicketTemplate | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `venueTemplate` with no `venueId`, or `productTemplate` with no `productId` (`clone-source-incomplete`). | produces a document or message: Create a ticket template from an existing one |
| Use Venue Template (secondary button) | navigation or local | — | — | — | — |
| Use Product Template (secondary button) | navigation or local | — | — | — | — |
| Import supported template definition (secondary button) | `importTicketTemplate` POST `/ticket-templates/imports` | TicketTemplateImportInput | TicketTemplate | 422 The format is not one the service reads (`unsupported-template-format`), or the file does not parse as that format (`template-definition-invalid`). | produces a document or message: Import a ticket template definition |
| Archive media template (destructive button) | `archiveMediaTemplate` POST `/media-templates/{templateId}/archive` | inline | AccessMediaTemplate | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **template gallery**: Cards with a thumbnail, media type, status, used by. *(source: contracts/spine/orders.yaml#listTicketTemplates / contracts/spine/access.yaml#listMediaDesign)*

**Data it reads**: `listMediaDesign` (onLoad, Media Design Studio Command Center); `listTicketTemplates` (onLoad, The ticket templates to duplicate or start from)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-345` Digital QR & Barcode Ticket Designer: *Works in Digital QR & Barcode Ticket Designer*; calls `listMediaDesign`
- → `BO-347` Apple Wallet Pass Designer: *Works in Apple Wallet Pass Designer*; calls `listMediaDesign`
- → `BO-348` Google Wallet Pass Designer: *Works in Google Wallet Pass Designer*; calls `listMediaDesign`
- → `BO-349` RFID, NFC, Card & Wristband Media Designer: *Works in RFID, NFC, Card & Wristband Media Designer*; calls `listMediaDesign`
- → `BO-350` Digital Card, Membership & Wearable Designer: *Works in Digital Card, Membership & Wearable Designer*; calls `listMediaDesign`
- → `BO-351` Dynamic Fields, Data Mapping & Content Builder: *Works in Dynamic Fields, Data Mapping & Content Builder*; calls `listMediaDesign`
- → `BO-352` Branding, Localization & Template Inheritance: *Works in Branding, Localization & Template Inheritance*; calls `listMediaDesign`
- → `BO-353` Multi-Media Preview, Testing, Approval & Publication: *Works in Multi-Media Preview, Testing, Approval & Publication*; calls `listMediaDesign`
- → `BO-346` PDF, Printable & POS Ticket Designer: *Works in PDF, Printable & POS Ticket Designer*; carries `templateId`; calls `listMediaDesign`

**What opens over it**

- confirmDialog *Archive media template*: **Names what `archiveMediaTemplate` changes and what it leaves alone**, in the consequence rather than the verb. A access media template this affects should be identified in the dialog, not just counted. **Collects what `archiveMediaTemplate` sends before it is called.** Nothing in the body is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media design list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media design untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media design yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media design are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `template-in-flight`: the template is awaiting approval or scheduled.; 422 The format is not one the service reads (`unsupported-template-format`), or the file does not parse as that format (`template-definition-invalid`).; 422 `venueTemplate` with no `venueId`, or `productTemplate` with no `productId` (`clone-source-incomplete`). |

#### Consistency with other screens

- Match `BO-346`: Same template records.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- name: Thermal ticket 80 mm
  status: published
- name: Wristband Dune Park
  status: draft
```

#### Permissions

- `listMediaDesign` → `SCOPE_VIEW` (read) · staff
- `listTicketTemplates` → `PRODUCT_VIEW` (read) · staff
- `cloneTicketTemplate` → `PRODUCT_CONFIGURE` (configure) · staff
- `importTicketTemplate` → `PRODUCT_CONFIGURE` (configure) · staff
- `archiveMediaTemplate` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-344` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-344`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 1: Opens Media Design Studio Command Center → Provide administrators with the central workspace for creating and managing all ticket and credential media templates. This should be the entry point for the entire no-code Media Design Studio.
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F169 branch at step 1 (expected): when Nothing has been set up on Media Design Studio Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F169 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-344?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Duplicate Existing, Use Venue Template, Use Product Template, Import supported template definition, Archive media template.
- [ ] Every transition is wired: `BO-100`, `BO-345`, `BO-347`, `BO-348`, `BO-349`, `BO-350`, `BO-351`, `BO-352`, `BO-353`, `BO-346`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-345` Digital QR & Barcode Ticket Designer

**Provide a visual no-code designer specifically for digital QR and barcode tickets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-345 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Barcode Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/digital-qr-barcode-ticket-designer-bo-345` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of digital QR and barcode ticket designs.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The no-code designer for the customer-facing QR and barcode ticket (mobile ticket, e-mail ticket): drag components (logo, event, holder, date, entrance, seat, price, Virtual Ticket ID, QR, barcode, terms, waiver status, sponsor) onto a canvas and set the QR payload profile and barcode presentation, previewed on mobile, tablet and desktop. It is opened from the Media Design Studio hub (BO-344) with a template. The one thing to get right: the Virtual Ticket ID and the media code are two different printed values (one ticket id, a media code that may cover a group), and the designer controls presentation only - the resolver decides what the code means.

**Known correction pending (do not draw the wrong version)**

- **No read of the design** Why: setDigitalBarcodeTicket is the only operation; the designer cannot open an existing template's working design (VO-R04). *(source: contracts/spine/access.yaml#setDigitalBarcodeTicket; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Static / Dynamic / Signed / Tokenised QR drawn as four selects; size, position, quiet zone, expiry, refresh and barcode type are free strings in the write** Why: One qrMode choice; the rest need units or closed sets to validate readability. *(source: contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The canvas and components list are not on the screen, and Show price is missing** Why: The pack's designer canvas and price toggle are the heart of the screen; the write has both (components, showPriceOnOff). *(source: screens/P08-venue-back-office.yaml#BO-345 / screens/P08-venue-back-office.yaml#BO-346; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Preview has no operation** Why: Responsive preview is required by the pack; it needs a render-preview operation (the contract notes "no operation yet"). *(source: contracts/spine/access.yaml#setDigitalBarcodeTicket; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Static QR | select field | — | — | — | — | — | — |
| Dynamic QR | select field | — | — | — | — | — | — |
| Signed QR | select field | — | — | — | — | — | — |
| Tokenized QR | select field | — | — | — | — | — | — |
| Rotation behavior where supported | text field | — | — | — | — | — | — |
| Size | select field | — | — | — | — | — | — |
| Position | select field | — | — | — | — | — | — |
| Quiet zone | select field | — | — | — | — | — | — |
| Error correction | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Refresh behavior | select field | — | — | — | — | — | — |
| Barcode type | select field | — | — | — | — | — | — |
| Orientation | select field | — | — | — | — | — | — |
| Human-readable value | select field | — | — | — | — | — | — |
| Hide/show encoded reference | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **components**: A palette of the 22 components on the left, a canvas in the middle; each placed component shows its sample value from the field library (BO-351) and has position and size handles. Virtual Ticket ID and QR/Barcode are separate components and both are required on an admission ticket. *(source: screens/P08-venue-back-office.yaml#BO-345 / contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput / DI-180)*
- **qrMode**: One segmented choice Static / Dynamic / Signed / Tokenised (the screen drew four separate selects). Dynamic shows the rotation step as the venue's setting (default 30 s) and a note that a dynamic code appears only in the app; Signed and Tokenised say what the gate checks offline. *(source: contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput / DI-1083 / DI-635)*
- **size / position / quietZone / errorCorrection / expiration / refreshBehavior**: Size and position by dragging, with a numeric box (mm on print, % of width on mobile); quiet zone in modules (minimum 4, default 4); error correction L / M / Q / H (default M); expiration and refresh as selects (At end of validity / At performance end; On rotation step / On every app open). Warn when the QR is below the readable minimum for the target. *(source: screens/P08-venue-back-office.yaml#BO-345 / contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput / designer default)*
- **barcodeType / orientation / humanReadableValue / hideShowEncodedReference**: Symbology select (Code 128, PDF417, Aztec, Data Matrix, as the platform's symbology list), orientation Horizontal / Vertical, two toggles "Print the value under the barcode" and "Show the encoded reference". *(source: screens/P08-venue-back-office.yaml#BO-346 / contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput / …)*
- **showPriceOnOff**: "Show price on the ticket" toggle, prominent (the pack calls it an important existing requirement); may differ by delivery context, so show "Off for B2B and complimentary" as a hint. *(source: screens/P08-venue-back-office.yaml#BO-346 / contracts/spine/access.yaml#/components/schemas/DigitalQrBarcodeTicketDesignerInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Responsive preview**: Mobile / Tablet / Desktop tabs above the canvas, rendered with the sample Virtual Ticket (VO-R17), in English and Arabic (right-to-left mirrored layout). *(source: screens/P08-venue-back-office.yaml#BO-346)*
- **Template header**: Template name, status (Draft / Pending approval / Scheduled / Published / Archived), version in force, and "Editing creates a new draft; the published version stays in force until the next publication". *(source: contracts/spine/access.yaml#archiveMediaTemplate / contracts/spine/access.yaml#approveMultiMediaPreview)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save design**: Sends the whole design for the template (PUT); a published template's working copy goes back to Draft. A template pending approval or scheduled is refused (409 template-in-flight) - show the save disabled with "In approval - wait for the decision". *(source: contracts/spine/access.yaml#setDigitalBarcodeTicket / contracts/spine/access.yaml#archiveMediaTemplate)*
- **Send to preview and approval**: Opens BO-353 with this template. *(source: screens/P08-venue-back-office.yaml#BO-344)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setDigitalBarcodeTicket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital barcode ticket configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital barcode ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital barcode ticket configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Dynamic QR selected for a template used on PDF or e-mail**: Block with "Dynamic QR is shown only in the app; e-mail and PDF show 'Open the app to activate'". *(source: DI-635 / DI-633)*
- **Price shown on a complimentary ticket**: Preview shows "AED 0.00"; warn and suggest turning price off. *(source: screens/P08-venue-back-office.yaml#BO-346 / designer default)*

#### Consistency with other screens

- Match `BO-351`: Every component value comes from the field library; no designer-local fields.
- Match `GST-055`: The guest's scan screen shows the same ticket number under the code and the same rotation step.
- Match `BO-346`: The PDF/print designer shares the canvas component and field palette.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
design:
  template: Aqua Park Mobile Ticket v3
  qr: Dynamic, 30 s, error correction M, quiet zone 4
  barcode: Code 128, value printed
  price: 'Off'
  components: Logo, Event name, Holder Sara Al Nuaimi, Date Sat 10 Oct 2026, Entrance Main Plaza Gate 1, Virtual
    Ticket ID VT-2026-009821, QR, Terms
```

#### Permissions

- `setDigitalBarcodeTicket` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-345` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-345`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 2: Works in Digital QR & Barcode Ticket Designer → Provide a visual no-code designer specifically for digital QR and barcode tickets.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-345?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-346` PDF, Printable & POS Ticket Designer

**Design tickets intended for printing, PDF generation, POS, box office and other physical/document outputs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-346 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `ORDER_REPRINT`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/access-venue/pdf-printable-pos-ticket-designer-bo-346` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The venue's ticket templates: thermal ticket, A4 PDF, wristband, RFID card, wallet pass, QR only, SMS, each with its artwork, dynamic fields and which sales it is selected for. Selection is automatic by priority, media type, product kind and channel, so the screen must show which template a given sale would use.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Two models of a ticket template, orders.TicketTemplate and access setPdfPrintablePos (page size, margins, printer profile as free strings). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Orientation | select field | — | — | — | — | — | — |
| Margins | select field | — | — | — | — | — | — |
| Header | select field | — | — | — | — | — | — |
| Footer | select field | — | — | — | — | — | — |
| Background | select field | — | — | — | — | — | — |
| Logo | select field | — | — | — | — | — | — |
| Images | select field | — | — | — | — | — | — |
| Text | select field | — | — | — | — | — | — |
| Dynamic fields | select field | — | — | — | — | — | — |
| QR/barcode | select field | — | — | — | — | — | — |
| Terms | select field | — | — | — | — | — | — |
| Perforation indicators where applicable | text field | — | — | — | — | — | — |
| Print-safe zones | select field | — | — | — | — | — | — |
| Printer profile | select field | — | — | — | — | — | — |
| DPI | select field | — | — | — | — | — | — |
| Paper/stock type | select field | — | — | — | — | — | — |
| Thermal layout | select field | — | — | — | — | — | — |
| Cut behavior | select field | — | — | — | — | — | — |
| Print margins | select field | — | — | — | — | — | — |
| Supported printer integration | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Media type | select | — | Thermal ticket · A4 pdf · Wristband · RFID card · Wallet pass · QR only · SMS | `listTicketTemplates` ?mediaType |
| Include inactive | toggle | off | — | `listTicketTemplates` ?includeInactive |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **dynamic fields**: Placed by drag and drop on the background image (guest name, ticket number, media code, QR, date, terms); ticket ID and media code are different fields and both are offered. *(source: DI-184 / DI-180)*
- **selection**: Media type, product kinds, channels and a priority; two active templates with the same priority for the same kind, channel and media type are refused, so show the clash inline. *(source: contracts/spine/orders.yaml#createTicketTemplate)*
- **localeVariants**: English and Arabic layouts (RTL mirrored) or a bilingual layout. *(source: contracts/spine/orders.yaml#createTicketTemplate / DI-019)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the design as saved** (detail panel, from `getPdfPrintablePos`)

| Shows | Format | Notes |
|---|---|---|
| Output format | chip: Pdf, A4, A5, Custom dimensions, POS receipt, Thermal ticket… | Print output this template produces |
| Page size | text | Page size |
| Orientation | text | Orientation |
| Margins | text | Margins |
| Header | text | Header |
| Footer | text | Footer |
| QR barcode | text | QR/barcode |
| Paper stock type | text | Paper/stock type |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| POS receipt (primary button) | navigation or local | — | — | — | — |
| Thermal ticket (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Print proof**: Produces a sample clearly marked PROOF on the artefact itself, so it can never be presented at a gate. *(source: contracts/spine/orders.yaml#printTicketProof)*
- **Retire template**: Sets it inactive rather than deleting; tickets already issued keep it. *(source: contracts/spine/orders.yaml#updateTicketTemplate)*

**Data it reads**: `listTicketTemplates` (onLoad, The templates this venue issues from); `getPdfPrintablePos` (onLoad, Load the design as saved)

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setPdfPrintablePos`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pdf printable pos configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pdf printable pos untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pdf printable pos configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Another active template has the same priority for the same product kind, channel and media type (`duplicateSelectionPriority`). (TicketTemplateConflictProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- name: Thermal ticket 80 mm
  mediaType: thermalTicket
  kinds:
  - datedAdmission
  - timedAdmission
  channels:
  - Point of sale
  - Kiosk
  priority: 100
- name: E-ticket A4 bilingual
  mediaType: a4Pdf
  channels:
  - Website
  - App
  priority: 100
```

#### Permissions

- `listTicketTemplates` → `PRODUCT_VIEW` (read) · staff
- `createTicketTemplate` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateTicketTemplate` → `PRODUCT_CONFIGURE` (configure) · staff
- `printTicketProof` → `ORDER_REPRINT` (operate) · staff
- `setPdfPrintablePos` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `getPdfPrintablePos` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*
- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-346` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-346`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 4: Works in PDF, Printable & POS Ticket Designer → Design tickets intended for printing, PDF generation, POS, box office and other physical/document outputs.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-346?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: POS receipt, Thermal ticket.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `ORDER_REPRINT`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-347` Apple Wallet Pass Designer

**Provide an Apple Wallet-specific configuration experience for eligible TICVAI credentials. This should not simply be a PDF ticket rendered inside a wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-347 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Pass Configuration; Configure the appropriate; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/apple-wallet-pass-designer-bo-347` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of Apple Wallet pass designs and no preview operation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Apple Wallet pass designer: a wallet-specific editor (not a PDF inside a wallet) for the pass's identity, organisation, colours, logo and icon, the header, primary, secondary, auxiliary and back field slots, how the credential is carried (QR, barcode or token reference) and which ticket changes push an update to issued passes. The one thing to get right: draw it as a live pass preview with slots, because Apple's layout is fixed - the administrator chooses what goes in each slot, not where.

**Known correction pending (do not draw the wrong version)**

- **Twenty-four selectFields with no options, including colours, logo, field slots and text** Why: Colour pickers, asset picks, slot editors and text inputs as above. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Revocation, notification behaviour and expiry are free strings in the write** Why: Each decides what happens to a guest's pass; they need closed sets. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the design and no preview operation** Why: The designer cannot open an existing template (VO-R04) and the pack requires a wallet-style preview before publication. *(source: screens/P08-venue-back-office.yaml#BO-347 / contracts/spine/access.yaml#setAppleWalletPass; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Apple and Google Wallet designers use two different update-trigger vocabularies** Why: Apple has eventChange, seatChange, ticketStatusChange; Google has eventTimeChange, venueChange, seatReassignment, ticketStatusChange, otherTicketInformationChange. The same ticket change must push both passes; use one list (Google's, which includes venue change) on both screens. *(source: contracts/spine/access.yaml#setAppleWalletPass / contracts/spine/access.yaml#setGoogleWalletPass; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **NFC in the wallet pass - direct Apple certification or the reader vendor's SDK?** → Drawn default accepted: QR passes only; NFC greyed "Pending decision". *(decided by Chinmay, 2026-10-02; DEC-271 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pass identity | select field | — | — | — | — | — | — |
| Organization | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Logo | select field | — | — | — | — | — | — |
| Icon | select field | — | — | — | — | — | — |
| Images where supported | select field | — | — | — | — | — | — |
| Background appearance | select field | — | — | — | — | — | — |
| Foreground appearance | select field | — | — | — | — | — | — |
| Label appearance | select field | — | — | — | — | — | — |
| Primary fields | select field | — | — | — | — | — | — |
| Secondary fields | select field | — | — | — | — | — | — |
| Auxiliary fields | select field | — | — | — | — | — | — |
| Header fields | select field | — | — | — | — | — | — |
| Back fields | select field | — | — | — | — | — | — |
| QR | select field | — | — | — | — | — | — |
| Barcode | select field | — | — | — | — | — | — |
| Token/reference | select field | — | — | — | — | — | — |
| Dynamic updates | select field | — | — | — | — | — | — |
| Event changes | select field | — | — | — | — | — | — |
| Seat changes | select field | — | — | — | — | — | — |
| Ticket status changes | select field | — | — | — | — | — | — |
| Relevant notification/update behavior | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Revocation/invalidation behavior where supported | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **passIdentity / organization / description**: Pass type and organisation name (the tenant brand; "Powered by TICVAI" is not on the pass), description (read by VoiceOver), each a text field with an Arabic variant. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput)*
- **logo / icon / imagesWhereSupported**: Picks from the brand asset library with size guidance (icon square, logo wide); inherited from BO-352 unless overridden. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput / DI-609)*
- **backgroundAppearance / foregroundAppearance / labelAppearance**: Three colour pickers (hex) with a contrast check between foreground/label and background; defaults from the brand. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput / DI-609)*
- **headerFields / primaryFields / secondaryFields / auxiliaryFields / backFields**: Slots on the pass preview; each takes field keys from the library (Event name, Date / time, Venue, Holder, Ticket type, Seat, Entrance, Membership, Virtual Ticket reference). A slot shows how many fields fit and truncation in Arabic. *(source: screens/P08-venue-back-office.yaml#BO-347 / contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput)*
- **credentialEncoding**: QR / Barcode / Token reference, limited to what the credential profile allows. NFC-in-wallet is not an option until the certification question is decided; show it greyed with that reason. *(source: contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput / DI-610 / TRACKER Actions row 210)*
- **dynamicUpdates / updateTriggers / relevantNotificationUpdateBehavior / expiry / revocation**: "Keep issued passes up to date" toggle; when on, chips Event change, Seat change, Ticket status change; notification behaviour (Silent update / Lock-screen notice); expiry select (End of validity / End of event day); revocation select (Void the pass / Remove the code / Mark expired). Not free text. *(source: screens/P08-venue-back-office.yaml#BO-347 / contracts/spine/access.yaml#/components/schemas/AppleWalletPassDesignerInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Pass preview**: Front and back of the pass in an iPhone frame with the sample ticket (VO-R17), English and Arabic; the code area shows the chosen encoding. *(source: screens/P08-venue-back-office.yaml#BO-347)*
- **Architecture note**: "This pass is a media representation of the Virtual Ticket; it is not a separate ticket." *(source: screens/P08-venue-back-office.yaml#BO-347 / DI-652)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save pass design**: Whole-design PUT; editing a published template returns its working copy to Draft; refused while in approval (409 template-in-flight). *(source: contracts/spine/access.yaml#setAppleWalletPass / contracts/spine/access.yaml#archiveMediaTemplate)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setAppleWalletPass`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The apple wallet pass configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the apple wallet pass untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No apple wallet pass configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Ticket for a dynamic-QR event**: The guest's Add to Apple Wallet is hidden until the ticket is activated in the app; the designer shows this on the preview. *(source: DI-635 / contracts/spine/orders.yaml#issueWalletPass)*
- **Ticket cancelled after the pass was added**: Pass updated per the revocation choice and the BO-340 wallet target; preview shows the voided state. *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*

#### Consistency with other screens

- Match `BO-348`: Same slot vocabulary and update triggers where the platforms overlap; one field library.
- Match `WEB-018`: The guest's Add to Apple Wallet action produces this pass.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pass:
  organization: Yas Leisure Group
  description: Aqua Park Day Pass
  colours: 'Background #0B4F6C, Foreground #FFFFFF, Label #9FD3E6'
  header: Date Sat 10 Oct
  primary: Aqua Park Day Pass - Adult
  secondary: Holder Sara Al Nuaimi, Entrance Main Plaza Gate 1
  auxiliary: Ticket VT-2026-009821
  encoding: QR
  updates: Event change, Ticket status change
```

#### Permissions

- `setAppleWalletPass` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-347` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-347`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 6: Works in Apple Wallet Pass Designer → Provide an Apple Wallet-specific configuration experience for eligible TICVAI credentials. This should not simply be a PDF ticket rendered inside a wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-347?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-348` Google Wallet Pass Designer

**Provide a dedicated Google Wallet configuration environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-348 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure supported; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/google-wallet-pass-designer-bo-348` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of Google Wallet pass designs and no preview operation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Google Wallet pass designer: pass class and template, issuer, title, logo and hero image, the event, venue, date-time, holder, seat and ticket type mappings, custom fields, links, how the credential is carried and which changes update issued passes. One template serves many products through field mapping. The one thing to get right: content fields are mappings to library keys, not values typed in, and the update triggers are settings, not buttons.

**Known correction pending (do not draw the wrong version)**

- **Update triggers drawn as action buttons ("Event time change" primary, others secondary)** Why: They are settings (updateTriggers), not actions. *(source: contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pass class and pass template merged into one select; content fields drawn as empty selects** Why: Two separate fields in the write; content fields are field-key mappings. *(source: contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the design and no preview operation** Why: Same gap as the other designers (VO-R04). *(source: contracts/spine/access.yaml#setGoogleWalletPass; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pass class/template | select field | — | — | — | — | — | — |
| Issuer | select field | — | — | — | — | — | — |
| Title | select field | — | — | — | — | — | — |
| Logo | select field | — | — | — | — | — | — |
| Hero/image assets where applicable | text field | — | — | — | — | — | — |
| Event information | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Ticket holder | select field | — | — | — | — | — | — |
| Seat | select field | — | — | — | — | — | — |
| Ticket type | select field | — | — | — | — | — | — |
| Custom fields | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Links | select field | — | — | — | — | — | — |
| Additional information | select field | — | — | — | — | — | — |
| QR | select field | — | — | — | — | — | — |
| Barcode | select field | — | — | — | — | — | — |
| Credential/token reference | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **passClass / passTemplate**: Two selects (the screen merged them into one) - pass class (event ticket, generic) and the template within it. *(source: screens/P08-venue-back-office.yaml#BO-348 / contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput)*
- **issuer / title / logo / heroImageAssetsWhereApplicable / links / additionalInformation**: Issuer from the tenant's Google issuer account, title text with Arabic variant, logo and hero image from the asset library, links as label + URL rows. *(source: contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput)*
- **eventInformation / venue / dateTime / ticketHolder / seat / ticketType / status / customFields**: Each is a field-key picker from the library (BO-351) with the sample value shown ("{{event.start}} - 19:30"); dateTime is a mapping, not a timestamp. *(source: screens/P08-venue-back-office.yaml#BO-348 / contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput)*
- **credentialEncoding**: QR / Barcode / Credential token reference, limited by the credential profile. *(source: contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput)*
- **updateTriggers**: Chips Event time change, Venue change, Seat reassignment, Ticket status change, Other ticket information change. *(source: screens/P08-venue-back-office.yaml#BO-348 / contracts/spine/access.yaml#/components/schemas/GoogleWalletPassDesignerInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event time change (primary button) | navigation or local | — | — | — | — |
| Venue change (secondary button) | navigation or local | — | — | — | — |
| Ticket status change (secondary button) | navigation or local | — | — | — | — |
| Relevant ticket information changes (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Device preview**: Android device frame with the pass, English and Arabic; a "Used by 4 products" line under the template name to show reuse. *(source: screens/P08-venue-back-office.yaml#BO-348)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save pass design**: Whole-design PUT; a published template returns to Draft; refused while in approval (409). *(source: contracts/spine/access.yaml#setGoogleWalletPass / contracts/spine/access.yaml#archiveMediaTemplate)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setGoogleWalletPass`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The google wallet pass configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the google wallet pass untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No google wallet pass configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Seat reassignment for a deferred-seat event**: With the Seat reassignment trigger on, issued passes update when seats are released; the preview shows "Seat to be assigned" before. *(source: DI-423)*
- **Ticket for a dynamic-QR event**: Add to Google Wallet hidden until activation in the app, as for Apple Wallet. *(source: DI-635)*

#### Consistency with other screens

- Match `BO-347`: Same update trigger names and encoding choices as Apple Wallet.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pass:
  class: Event ticket
  issuer: Yas Leisure Group
  title: Summer Concert - Etihad Park
  dateTime: '{{event.start}} -> 15 Oct 2026 19:30'
  holder: '{{customer.name}} -> Priya Nair'
  seat: '{{ticket.seat}} -> Section A Row 3 Seat 18'
  encoding: QR
  triggers: Event time change, Seat reassignment, Ticket status change
```

#### Permissions

- `setGoogleWalletPass` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-348` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-348`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 8: Works in Google Wallet Pass Designer → Provide a dedicated Google Wallet configuration environment.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-348?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event time change, Venue change, Ticket status change, Relevant ticket information changes.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-349` RFID, NFC, Card & Wristband Media Designer

**Configure both the visual and technical profile of physical electronic credentials. This is important because RFID/NFC media are not merely artwork.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-349 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/rfid-nfc-card-wristband-media-designer-bo-349` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of RFID, NFC, card and wristband media designs.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Designs physical electronic media - RFID and NFC cards and wristbands, membership cards, staff/guest cards, custom wearables - as both artwork (front, back, printable area, logo, printed personal fields, sponsor branding) and a technical profile (chip, UID handling, encoding profile, provider, reader compatibility, printer/encoder). The one thing to get right: the medium only carries a secure reference that resolves through its binding to the Virtual Ticket; the technical half is not decoration, and a template with no encoder profile cannot be published.

**Known correction pending (do not draw the wrong version)**

- **Medium kinds and wristband options drawn as action buttons ("RFID Card", "NFC Card", "Size where applicable", "Deposit/reference where applicable")** Why: They are fields (mediaKind enum, size, deposit Money), not actions. *(source: contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Technology, chip, encoding, provider and encoder are free strings in the write** Why: They must reference the registry and the encoding profiles or the medium cannot be encoded consistently. *(source: contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput / contracts/spine/access.yaml#setMediaIssuanceEncoding; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the design** Why: Same as the other designers (VO-R04). *(source: contracts/spine/access.yaml#setRfidNfcCard; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Media dimensions | select field | — | — | — | — | — | — |
| Front | select field | — | — | — | — | — | — |
| Back | select field | — | — | — | — | — | — |
| Printable area | select field | — | — | — | — | — | — |
| Logo | select field | — | — | — | — | — | — |
| Customer name | select field | — | — | — | — | — | — |
| Photo | select field | — | — | — | — | — | — |
| Membership tier | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Serial number | select field | — | — | — | — | — | — |
| QR/barcode if combined | select field | — | — | — | — | — | — |
| Custom artwork | select field | — | — | — | — | — | — |
| Sponsor/venue branding | select field | — | — | — | — | — | — |
| RFID/NFC technology | select field | — | — | — | — | — | — |
| Chip/profile | select field | — | — | — | — | — | — |
| UID/reference handling | select field | — | — | — | — | — | — |
| Encoding profile | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Reader compatibility | select field | — | — | — | — | — | — |
| Printer/encoder integration | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mediaKind**: The first choice, as cards: RFID card, RFID wristband, NFC card, NFC wristband, Membership card, Staff/guest card, Custom wearable. It changes the canvas shape (card CR80 vs wristband strip). The generated action buttons "RFID Card", "NFC Card", "Membership Card", "Staff/guest card" are this choice. *(source: screens/P08-venue-back-office.yaml#BO-349 / contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput)*
- **Wristband options (reusability, printed, encoded, colorCategory, sizeWhereApplicable, activationAtCollection …**: Shown for wristbands: Disposable / Reusable; Printed and Encoded toggles; colour or category (colour swatch + label, e.g. "Orange - Child"); size (Adult / Child / Adjustable); "Activate when handed over" toggle; deposit as money in AED for reusable bands (VO-R10). *(source: screens/P08-venue-back-office.yaml#BO-350 / contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput / DI-644)*
- **Artwork (mediaDimensions, front, back, printableArea, logo, customArtwork, sponsorVenueBranding)**: Front and back canvases with the printable area outlined and bleed shown; logo and artwork from the asset library; dimensions preset by medium, editable for custom wearables. *(source: screens/P08-venue-back-office.yaml#BO-349 / contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput)*
- **printedFields**: Chips Customer name, Photo, Membership tier, Expiry, Serial number, QR/barcode (if combined). Photo and name are marked "Personal data" and need the field library's permission for printed media. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput)*
- **Technology profile (rfidNfcTechnology, chipProfile, uidReferenceHandling, encodingProfile, provider …**: Picks, not text: technology and provider from the media registry (BO-337), encoding profile from the issuance and encoding profiles, reader compatibility as a multi-select of reader models, UID handling Read-only UID / Encoded reference / Both. Every pick shows its source screen. *(source: screens/P08-venue-back-office.yaml#BO-350 / contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput / contracts/spine/access.yaml#setMediaIssuanceEncoding)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| RFID Card (primary button) | navigation or local | — | — | — | — |
| NFC Card (secondary button) | navigation or local | — | — | — | — |
| Membership Card (secondary button) | navigation or local | — | — | — | — |
| Staff/guest card where applicable (secondary button) | navigation or local | — | — | — | — |
| Size where applicable (secondary button) | navigation or local | — | — | — | — |
| Deposit/reference where applicable (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Two-sided preview**: Front/back flip with the sample holder (VO-R17) and a technical summary strip ("NFC, NTAG 216, encoded reference, HID, encoder Main Plaza Desk 1"). *(source: screens/P08-venue-back-office.yaml#BO-349)*
- **Resolution note**: "This medium carries a reference: Credential binding > Virtual Ticket. No entitlement is stored on it." *(source: screens/P08-venue-back-office.yaml#BO-350)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save media design**: Whole-design PUT; published template returns to Draft; refused while in approval (409). *(source: contracts/spine/access.yaml#setRfidNfcCard / contracts/spine/access.yaml#archiveMediaTemplate)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setRfidNfcCard`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rfid nfc card configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rfid nfc card untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rfid nfc card configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No encoder profile chosen**: Save allowed as draft, but a red check "RFID template has no encoder profile" blocks publication on BO-353. *(source: screens/P08-venue-back-office.yaml#BO-353)*
- **Reusable wristband with deposit**: Deposit shows on the POS line when issued and is refunded on return; the designer shows "Deposit AED 10.00 refundable". *(source: contracts/spine/access.yaml#/components/schemas/RfidNfcCardWristbandMediaDesignerInput / designer default)*

#### Consistency with other screens

- Match `BO-180`: RFID & NFC Configuration (access board) uses the same write; one of the two survives (VO-R14).
- Match `BO-178`: Media Issuance & Encoding Profile supplies the encoding profiles picked here.
- Match `BO-647`: The accreditation badge designer is a separate template type (badge); keep the same canvas component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
design:
  kind: RFID wristband
  reusable: Reusable
  deposit: AED 10.00
  colour: Blue - Adult
  size: Adjustable
  printed: true
  encoded: true
  printedFields: Serial number, QR
  technology: RFID ISO 15693
  provider: HID
  encoder: Main Plaza Desk 1 encoder
  activation: At collection
```

#### Permissions

- `setRfidNfcCard` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-349` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-349`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 10: Works in RFID, NFC, Card & Wristband Media Designer → Configure both the visual and technical profile of physical electronic credentials. This is important because RFID/NFC media are not merely artwork.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-349?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: RFID Card, NFC Card, Membership Card, Staff/guest card where applicable, Size where applicable, Deposit/reference where applicable.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-350` Digital Card, Membership & Wearable Designer

**Provide specialized configuration for persistent credentials that may represent longer-lived relationships rather than a single event ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-350 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/digital-card-membership-wearable-designer-bo-350` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of digital card, membership and wearable designs and no preview operation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Designs persistent credentials - annual pass, membership card, season pass, VIP, partner credential, digital membership card, wearable - whose look changes with the relationship: artwork per tier (Silver, Gold, Platinum), member photo, number, validity, benefits summary and dynamic messages, and a different presentation on renewal, tier change, expiry, suspension or benefit change. The one thing to get right: one template with variants (tier x membership type x brand x venue x age category), not one template per tier.

**Known correction pending (do not draw the wrong version)**

- **Content fields are selectFields and free strings (status, validity, tier) and the variant dimensions are buttons** Why: Content maps field keys; variants are a grid; "Tier designs" and "Membership types" are not actions. *(source: contracts/spine/access.yaml#/components/schemas/DigitalCardMembershipWearableDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the design and no preview operation** Why: Same gap as the other designers (VO-R04). *(source: contracts/spine/access.yaml#setDigitalCardMembership; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Brand | select field | — | — | — | — | — | — |
| Card artwork | select field | — | — | — | — | — | — |
| Member photograph | select field | — | — | — | — | — | — |
| Member name | select field | — | — | — | — | — | — |
| Membership number | select field | — | — | — | — | — | — |
| Tier | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| QR/barcode | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Benefits summary | select field | — | — | — | — | — | — |
| Dynamic messaging | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card content (brand, cardArtwork, memberPhotograph, memberName, membershipNumber, tier, validity, qrBarcode, status …**: Placed on a card canvas as components mapped to field-library keys (membership.tier, membership.expiry); benefits summary is a short list from the membership product, not typed. *(source: screens/P08-venue-back-office.yaml#BO-350 / screens/P08-venue-back-office.yaml#BO-351 / contracts/spine/access.yaml#/components/schemas/DigitalCardMembershipWearableDesignerInput)*
- **Variants (tierDesigns, membershipTypes, brands, venues, ageCategories)**: A variant grid: rows are tiers, columns the other dimensions, each cell an artwork thumbnail with "Inherits" or "Own artwork". The generated "Tier designs" and "Membership types" buttons become tabs of this grid. *(source: screens/P08-venue-back-office.yaml#BO-351 / contracts/spine/access.yaml#/components/schemas/DigitalCardMembershipWearableDesignerInput)*
- **stateTriggers**: Chips Membership renewal, Tier change, Expiry, Suspension, Benefit status; for each chosen, the presentation change (e.g. Suspension - grey card with "Suspended" band and the code hidden; Expiry - "Renew now" message). *(source: screens/P08-venue-back-office.yaml#BO-351 / contracts/spine/access.yaml#/components/schemas/DigitalCardMembershipWearableDesignerInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Tier designs (primary button) | navigation or local | — | — | — | — |
| Membership types (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Variant preview**: Side-by-side Silver / Gold / Platinum cards for the sample member, plus the state previews (Active, Suspended, Expired). *(source: screens/P08-venue-back-office.yaml#BO-351)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save card design**: Whole-design PUT; published template returns to Draft; refused while in approval (409). *(source: contracts/spine/access.yaml#setDigitalCardMembership / contracts/spine/access.yaml#archiveMediaTemplate)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; carries `templateId`; calls `setDigitalCardMembership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital card membership configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital card membership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital card membership configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Member has Face Pass as primary medium**: Card shows "Face Pass active" badge; the QR remains as fallback (DI-640, BO-341 order). *(source: DI-640 / DI-608)*
- **Member photo missing**: Placeholder silhouette with "Photo needed" on the preview; issuance (BO-356) fails with Required data missing if the photo is mandatory. *(source: contracts/spine/access.yaml#/components/schemas/CredentialGenerationIssuanceMonitorView)*

#### Consistency with other screens

- Match `BO-349`: The physical membership card shares artwork with this digital card where both exist.
- Match `GST-069`: Face Pass status shown on the card matches the guest's enrolment status.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
variants:
- tier: Silver
  artwork: Silver wave
  member: Khalid Al Zaabi
  number: MBR-0045120
  valid: 1 Oct 2026 - 30 Sep 2027
  benefits: Unlimited entry, 10% F&B
- tier: Gold
  artwork: Gold dunes
  benefits: Unlimited entry, 2 guest admissions, 5 parking uses, 10% F&B
- tier: Platinum
  artwork: Platinum night
  benefits: Unlimited entry, Fast Pass x4 per visit, 20% F&B
```

#### Permissions

- `setDigitalCardMembership` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-350` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-350`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 12: Works in Digital Card, Membership & Wearable Designer → Provide specialized configuration for persistent credentials that may represent longer-lived relationships rather than a single event ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-350?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Tier designs, Membership types.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-351` Dynamic Fields, Data Mapping & Content Builder

**Create a centralized reusable field library so development team does not hard-code ticket fields separately into every media designer. This is another important architecture screen.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-351 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Custom Fields; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/dynamic-fields-data-mapping-content-builder-bo-351` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists the dynamic field library.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The shared field library every media designer draws from: field groups (Customer, Participant, Order, Virtual Ticket, Product/Event, Seating, Commercial, Membership, Compliance, Credential, Custom), each field's template key ({{ticket.seat}} -> A18), formatting, conditional visibility ("show Section / Row / Seat only if a seat is assigned"), which media may show it and whether it is sensitive. The one thing to get right: a library list with a field editor, not a page of formatting selects - and sensitive personal data is off printed media unless explicitly allowed.

**Known correction pending (do not draw the wrong version)**

- **The screen draws only the seven formatting selects** Why: The library (category, key, standard field, allowed media, sensitive) is the screen; formatting is one section of a field. *(source: screens/P08-venue-back-office.yaml#BO-351 / contracts/spine/access.yaml#/components/schemas/DynamicFieldsDataMappingContentBuilderInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the field library** Why: setDynamicFieldData writes one field; nothing lists the library, so neither this screen nor the designers can show the fields. *(source: contracts/spine/access.yaml#setDynamicFieldData; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Key style differs between the pack ({{event.start_time}}) and the contract example (ticket.seat)** Why: Agree one key convention before templates are built on it. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/DynamicFieldsDataMappingContentBuilderInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date formats | select field | — | — | — | — | — | — |
| Time formats | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Number formatting | select field | — | — | — | — | — | — |
| Text transformation | select field | — | — | — | — | — | — |
| Character limit | select field | — | — | — | — | — | — |
| Conditional visibility | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **category / fieldKey / standardField**: Group picker; key in dot notation (ticket.seat, event.start, customer.name), unique, immutable once a template uses it; standard source field from the platform list, or empty for a tenant custom field (custom fields need approval, per the pack). *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/DynamicFieldsDataMappingContentBuilderInput)*
- **dateFormats / timeFormat / numberFormat / textTransformation / characterLimit**: Formatting defaults to the region (VO-R10: dd MMM yyyy, 24-hour or 12-hour, AED with 2 decimals); override per field with presets and a live sample; text transformation None / UPPER / Title; character limit with an ellipsis preview in English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/DynamicFieldsDataMappingContentBuilderInput)*
- **conditionalVisibility**: A one-line condition builder "Show when [Seat assigned] [is] [Yes]", otherwise the block is hidden - the pack's example. *(source: screens/P08-venue-back-office.yaml#BO-352)*
- **allowedMedia / sensitive**: Media chips (QR ticket, PDF, Apple Wallet, Google Wallet, RFID/NFC card, Wristband, Membership card); "Sensitive personal data" toggle that removes Printed and PDF from allowed media unless re-enabled with a warning (mobile, e-mail, date of birth, photo, Emirates ID). *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/DynamicFieldsDataMappingContentBuilderInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Field library**: Grouped list (the eleven groups) with Key, Label, Sample value, Media (icons), Sensitive badge, Used by N templates. Search by key or label. *(source: screens/P08-venue-back-office.yaml#BO-351)*
- **Mapping preview**: Three-column sample "{{ticket.seat}} -> A18; {{event.start}} -> 19:30; {{customer.name}} -> Ahmed Hassan", rendered with the venue sample instead (VO-R17). *(source: screens/P08-venue-back-office.yaml#BO-352)*
- **AI assistance**: Suggestions ("Add Entrance to the concert ticket") and mapping warnings ("customer.mobile is sensitive and placed on a PDF template"), advisory (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-352)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save field**: Upsert of one field definition (whole field, VO-R04); a key change on a used field is refused with the templates named. *(source: contracts/spine/access.yaml#setDynamicFieldData)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; calls `setDynamicFieldData`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic fields data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic fields data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic fields data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Field made sensitive while published templates print it**: Warn with the templates; they keep the field until republished, and the BO-353 check flags them. *(source: contracts/spine/access.yaml#approveMultiMediaPreview / designer default)*

#### Consistency with other screens

- Match `BO-345`: All designers (BO-345 to BO-350) pick from this list; same keys in the Apple and Google mapping slots.
- Match `BO-235`: The access attribute catalogue uses the same dot-key style (guest.tier); keep one convention.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fields:
- group: Seating
  key: ticket.seat
  sample: Section A Row 3 Seat 18
  media: QR, PDF, Apple Wallet, Google Wallet
  condition: Seat assigned = Yes
- group: Product/Event
  key: event.start
  sample: '19:30'
  format: HH:mm (venue time)
- group: Customer
  key: customer.mobile
  sample: +971 50 *** 4471
  sensitive: true
  media: Apple Wallet, Google Wallet
- group: Commercial
  key: price.paid
  sample: AED 1,855.00
  format: AED, 2 decimals
```

#### Permissions

- `setDynamicFieldData` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-351` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-351`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 14: Works in Dynamic Fields, Data Mapping & Content Builder → Create a centralized reusable field library so development team does not hard-code ticket fields separately into every media designer. This is another important architecture screen.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-351?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-352` Branding, Localization & Template Inheritance

**Allow TICVAI's multi-tenant clients to control branding and localization without rebuilding every ticket template.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-352 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/branding-localization-template-inheritance-bo-352` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Branding and languages for ticket media by inheritance: tenant / corporate > brand > venue > event > product > media template, each level inheriting approved elements (logo, colours, typography, backgrounds, header/footer, legal footer, support information, sponsor placement, images) and overriding what it is allowed to. Languages are English and Arabic plus configured others, with right-to-left layout for Arabic, not just translated text. The one thing to get right: every value shows where it comes from ("Inherited from Yas Leisure Group") and can be reset to inherited.

**Known correction pending (do not draw the wrong version)**

- **Table columns are translation fields only (source language, translation, status, reviewer, approval, version)** Why: The list is the inheritance levels; translation status is one read-only section of a level. *(source: contracts/spine/access.yaml#/components/schemas/BrandingLocalizationTemplateInheritanceView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Additional configured languages" drawn as a primary button** Why: It is the languages field. *(source: contracts/spine/access.yaml#/components/schemas/BrandingLocalizationTemplateInheritanceInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save has no permission on the screen** Why: The write needs ACCESS_POINT_CONFIGURE (VO-R08). *(source: contracts/spine/access.yaml#setBrandingLocalizationTemplate; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Sent by *Save branding and languages*** (`setBrandingLocalizationTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Level `level` | select | required | — | Tenant · Brand · Venue · Event · Product · Media template | — | — | `setBrandingLocalizationTemplate` body |
| Scope `scopeId` | text field | required | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Parent scope `parentScopeId` | text field | optional | — | — | — | The level above this one inherits from; empty at tenant | `setBrandingLocalizationTemplate` body |
| Logo `logo` | text field | optional | — | — | — | Asset library reference | `setBrandingLocalizationTemplate` body |
| Colors `colors` | list of values (chips) | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Typography `typography` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Backgrounds `backgrounds` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Header footer `headerFooter` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Legal footer `legalFooter` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Support information `supportInformation` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Sponsor placement `sponsorPlacement` | text field | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Images `images` | list of values (chips) | optional | — | — | — | — | `setBrandingLocalizationTemplate` body |
| Source language `sourceLanguage` | text field | required | — | max length 35 | — | BCP 47 tag | `setBrandingLocalizationTemplate` body |
| Languages `languages` | list of values (chips) | optional | — | — | — | Additional configured languages (BCP 47) | `setBrandingLocalizationTemplate` body |
| RTL `rtl` | toggle | optional | off | — | — | Right-to-left layout for the RTL languages in `languages` | `setBrandingLocalizationTemplate` body |
| Field overrides `fieldOverrides` | key and value settings | optional | — | — | — | Field-level overrides of the inherited template, keyed by field name | `setBrandingLocalizationTemplate` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **level / scopeId / parentScopeId**: Chosen from an inheritance tree on the left (Yas Leisure Group > Aqua Park brand > Aqua Park > event > product > template), never typed. parentScopeId is derived from the tree. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#setBrandingLocalizationTemplate)*
- **Brand components (logo, colors, typography, backgrounds, headerFooter, legalFooter, supportInformation …**: Each row shows the effective value and its origin; an empty field inherits (unlike other PUT screens, empty here means "inherit", which the form must say). Colours as swatches, logo/images from the asset library, legal footer and support info as text with Arabic variants. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#setBrandingLocalizationTemplate)*
- **sourceLanguage / languages / rtl**: Source language (BCP 47, default en-AE), additional languages as chips (ar-AE pre-added), RTL toggle on automatically when an RTL language is added. The generated button "Additional configured languages" is this chip field. *(source: screens/P08-venue-back-office.yaml#BO-352 / contracts/spine/access.yaml#/components/schemas/BrandingLocalizationTemplateInheritanceInput)*
- **fieldOverrides**: Per-medium overrides (e.g. Apple Wallet uses the short logo) listed under "Media-specific overrides", each removable. *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/access.yaml#/components/schemas/BrandingLocalizationTemplateInheritanceInput)*

#### Outputs: what the screen shows and produces

**Shown**

**Every branding localization template** (data table, from `listBrandingLocalizationTemplate`)

| Shows | Format | Notes |
|---|---|---|
| Source language | text | Source language |
| Translation | text | Translation |
| Translation status | chip: Not started, In progress, In review, Approved | Translation status |
| Reviewer | text | Reviewer |
| Approval | text | Approval |
| Version | text | Version |

**The selected branding localization template** (detail panel): The pack groups this record's detail under its own headings: “Tenant / Corporate”, “Brand”, “Venue”, “Event”, “Product”, “Inheritance Example”.

| Shows | Format | Notes |
|---|---|---|
| Source language | text | Source language |
| Translation | text | Translation |
| Translation status | chip: Not started, In progress, In review, Approved | Translation status |
| Reviewer | text | Reviewer |
| Approval | text | Approval |
| Version | text | Version |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Additional configured languages (primary button) | navigation or local | — | — | — | — |
| Save branding and languages (primary button) | `setBrandingLocalizationTemplate` PUT `/branding-localization-template` | BrandingLocalizationTemplateInheritanceInput | BrandingLocalizationTemplateInheritanceView | 422 A language that is not a BCP 47 tag, or parentScopeId at a level that is not above | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Translation status**: Read-only per language - Not started, In progress, In review, Approved - with reviewer and version; the translation workflow owns it, not this form. *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/access.yaml#setBrandingLocalizationTemplate)*
- **Shared branding preview**: The corporate logo on QR, PDF, Apple Wallet, Google Wallet and RFID thumbnails side by side, each keeping its own layout; English and Arabic (mirrored) rows. *(source: screens/P08-venue-back-office.yaml#BO-353)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save branding and languages**: Upsert of the selected level (keyed by level and scope); lower levels that inherit pick up the change, which the confirmation counts ("Applies to 3 venues, 42 templates that inherit"). *(source: contracts/spine/access.yaml#setBrandingLocalizationTemplate)*
- **Reset to inherited**: Clears the field at this level so it inherits again. *(source: contracts/spine/access.yaml#setBrandingLocalizationTemplate)*

**Data it reads**: `listBrandingLocalizationTemplate` (onLoad, Branding, Localization & Template Inheritance)

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Returns to the board's landing screen*; calls `listBrandingLocalizationTemplate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The branding localization template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the branding localization template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No branding localization template yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the branding localization template are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A language that is not a BCP 47 tag, or parentScopeId at a level that is not above |

#### Edge cases to draw

- **Arabic layout overflows a printed template**: Flag on the preview and in the BO-353 checks ("Arabic layout exceeds printable area"). *(source: screens/P08-venue-back-office.yaml#BO-353)*
- **A level overrides an element the level above locked**: Field read-only with "Locked by Yas Leisure Group". *(source: screens/P08-venue-back-office.yaml#BO-352)*

#### Consistency with other screens

- Match `BO-353`: Localisation, RTL and branding are pre-publication checks there.
- Match `BO-345`: Designers show inherited branding as their starting point.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
chain: Yas Leisure Group (tenant) > Aqua Park (brand) > Aqua Park venue > Summer Splash Weekend (event) > VIP Cabana
  Admission (product) > Apple Wallet template
level:
  level: Venue
  scope: Aqua Park
  logo: Inherited from Aqua Park brand
  colours: '#0B4F6C, #F2A541 (own)'
  legalFooter: Inherited
  languages: en-AE, ar-AE
  rtl: true
  translation: ar-AE In review - Omar Haddad
```

#### Permissions

- `listBrandingLocalizationTemplate` → `SCOPE_VIEW` (read) · staff
- `setBrandingLocalizationTemplate` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-352` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-352`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 16: Works in Branding, Localization & Template Inheritance → Allow TICVAI's multi-tenant clients to control branding and localization without rebuilding every ticket template.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-352?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Additional configured languages, Save branding and languages.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-353` Multi-Media Preview, Testing, Approval & Publication

**Provide the final quality and governance gate before any media template becomes operational. This should be a particularly visual screen. Board 1 established the Virtual Ticket as the authoritative ticket identity and the one- Virtual-Ticket-to-many-media architecture. Board 2 established how administrators design and configure each media type. Board 3 manages what happens to the actual credential instances in production after a Virtual Ticket has been created.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-353 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/multi-media-preview-testing-approval-publication-bo-353` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of media templates, rendered previews or server-run check results, and no version list.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The final quality and approval gate for any media template, and a deliberately visual screen: pick a sample Virtual Ticket and see every medium it would produce side by side (Mobile QR, PDF, Apple Wallet, Google Wallet, RFID card, wristband, and the B2C front-end view), run the readability, layout, localisation and payload checks, send it through review, and publish now or on a schedule to chosen brands, venues, products and channels. The one thing to get right: publishing creates a new version and never rewrites credentials already issued.

**Known correction pending (do not draw the wrong version)**

- **Screen has only publication buttons and the gap says the pack gives nothing to draw** Why: The pack lists preview targets, sample data, checks, validation messages, the approval route and versioning; the preview grid and checks are the screen. *(source: screens/P08-venue-back-office.yaml#BO-353; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rollout scopes drawn as action buttons ("Selected Brands" etc.)** Why: They are scope fields of the write. *(source: contracts/spine/access.yaml#/components/schemas/MultiMediaPreviewTestingApprovalPublicationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of templates, rendered previews or check results; validationChecks is a list the client sends** Why: The server must run the checks and return results, or a client can claim checks it never ran; there is also no way to list versions. *(source: contracts/spine/access.yaml#approveMultiMediaPreview; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **templateVersion ("Version created by this publication") is a request field** Why: The version a publication creates is assigned by the server, never typed by the publisher (VO-R03). *(source: contracts/spine/access.yaml#approveMultiMediaPreview; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sample Virtual Ticket**: A picker of sample tickets (or a real one by ID, masked) driving every preview; defaults to the pack's VIP Concert sample re-cast in the venue world (VO-R17). *(source: screens/P08-venue-back-office.yaml#BO-353)*
- **previewTargets**: Chips Desktop, Mobile, Tablet, Printer, POS, Wallet, Encoder; each target adds a preview frame. *(source: contracts/spine/access.yaml#/components/schemas/MultiMediaPreviewTestingApprovalPublicationInput)*
- **publishMode / scheduledAt**: Publish now / Schedule; schedule asks a date-time in venue time, not in the past. *(source: contracts/spine/access.yaml#/components/schemas/MultiMediaPreviewTestingApprovalPublicationInput)*
- **Rollout (selectedBrands, selectedVenues, selectedProducts, selectedChannels, controlledRollout)**: Four scope pickers ("All" when empty) and a "Controlled rollout" toggle that starts with the chosen scope only. The generated buttons "Selected Brands", "Selected Venues", "Selected Products", "Selected Channels" are these pickers. *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/access.yaml#/components/schemas/MultiMediaPreviewTestingApprovalPublicationInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Selected Brands (secondary button) | navigation or local | — | — | — | — |
| Selected Venues (secondary button) | navigation or local | — | — | — | — |
| Selected Products (secondary button) | navigation or local | — | — | — | — |
| Selected Channels (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Universal preview**: A grid of rendered media for the sample ticket (VT number visible on each, proving one ticket behind all), plus the B2C storefront card - every output format the reviewer must see. *(source: screens/P08-venue-back-office.yaml#BO-353 / DI-444)*
- **Checks**: Pass / warning / fail list for Dynamic fields, Missing fields, QR readability, Barcode readability, Wallet configuration, Print boundaries, Localisation, RTL, Branding, Image resolution, Credential payload, Virtual Ticket resolution, Provider configuration; failures in the pack's words ("QR overlaps customer name", "Arabic layout exceeds printable area", "Wallet credential has no valid payload mapping", "RFID template has no encoder profile") with Fix linking to the designer. *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/access.yaml#/components/schemas/MultiMediaPreviewTestingApprovalPublicationInput)*
- **Approval rail**: Designer > Brand review > Operations review > Technical/security review (where applicable) > Approval > Publication; a human approves (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/approvals.yaml#decideApprovalRequest)*
- **AI pre-publication review**: Advisory findings ("The ticket holder name may be truncated on smaller mobile screens in Arabic"; "The QR occupies only 9% of the printable area"). *(source: screens/P08-venue-back-office.yaml#BO-353)*
- **Version history**: Versions with status (Pending approval, Scheduled, Published, Superseded, Rejected) and rollout scope; "Issued credentials keep the version they were issued with." *(source: screens/P08-venue-back-office.yaml#BO-353 / contracts/spine/access.yaml#approveMultiMediaPreview)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Submit for approval**: Sends the template, its checks, targets, publish mode and rollout; the template goes to Pending approval and is locked against edits until decided. Refused while any check fails. *(source: contracts/spine/access.yaml#approveMultiMediaPreview / contracts/spine/approvals.yaml#createApprovalRequest)*
- **Approve / Reject**: Approvers decide in the approval inbox or here; reject needs a reason and returns the template to Draft; approve publishes now or schedules. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*

**Where the user goes next**

- → `BO-344` Media Design Studio Command Center: *Media Design Studio Command Center*; carries `templateId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-media preview testing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-media preview testing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-media preview testing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-media preview testing are still there. The pack's own statuses are if Required → Expire → Audit — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Newer version published for an overlapping scope**: The older version shows Superseded with the date and the newer version linked. *(source: contracts/spine/access.yaml#approveMultiMediaPreview)*
- **Scheduled publication time passes while the venue is closed**: Publishes anyway at the time; the version list says "Published 02:00 (scheduled)". *(source: contracts/spine/access.yaml#approveMultiMediaPreview / designer default)*

#### Consistency with other screens

- Match `BO-343`: Same approval rail component as the Virtual Ticket board.
- Match `BO-344`: Template status on the studio hub follows the outcome here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sample:
  customer: Ahmed Al Mansoori
  ticket: VT-2026-009821
  product: VIP Concert - Etihad Park
  date: 15 Oct 2026
  time: '19:30'
  section: A
  row: 3
  seat: 18
checks:
  passed: 11
  warnings: 1
  failed: 1
  failure: Arabic layout exceeds printable area (Thermal 80 mm)
  warning: QR occupies 9% of printable area
rollout:
  mode: Schedule
  at: 12 Oct 2026 06:00
  venues: Aqua Park
  channels: Web, App
  controlled: true
```

#### Permissions

- `approveMultiMediaPreview` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-353` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-353`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 2
- Flow F169 *Ticket Media Credential Management board 2: Media Design Studio Command Center*, step 18: Works in Multi-Media Preview, Testing, Approval & Publication → Provide the final quality and governance gate before any media template becomes operational. This should be a particularly visual screen. Board 1 established the Virtual Ticket as the authoritative …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-353?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule, Selected Brands, Selected Venues, Selected Products, Selected Channels.
- [ ] Every transition is wired: `BO-344`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveMultiMediaPreview": {"method":"PUT","path":"/multi-media-preview","contract":"access","summary":"Multi-Media Preview, Testing, Approval & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MultiMediaPreviewTestingApprovalPublicationInput","responds":"MultiMediaPreviewTestingApprovalPublicationView"},
"archiveMediaTemplate": {"method":"POST","path":"/media-templates/{templateId}/archive","contract":"access","summary":"Archive a media template","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessMediaTemplate"},
"cloneTicketTemplate": {"method":"POST","path":"/ticket-templates/{templateId}/clone","contract":"orders","summary":"Create a ticket template from an existing one","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloneTicketTemplateInput","responds":"TicketTemplate"},
"createTicketTemplate": {"method":"POST","path":"/ticket-templates","contract":"orders","summary":"Create a ticket template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TicketTemplateRequest","responds":"TicketTemplate"},
"getPdfPrintablePos": {"method":"GET","path":"/pdf-printable-pos","contract":"access","summary":"The printable ticket design as saved","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PdfPrintablePosTicketDesignerView"},
"importTicketTemplate": {"method":"POST","path":"/ticket-templates/imports","contract":"orders","summary":"Import a ticket template definition","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TicketTemplateImportInput","responds":"TicketTemplate"},
"listBrandingLocalizationTemplate": {"method":"GET","path":"/branding-localization-template","contract":"access","summary":"Branding, Localization & Template Inheritance","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BrandingLocalizationTemplateInheritanceView"},
"listMediaDesign": {"method":"GET","path":"/media-design","contract":"access","summary":"Media Design Studio Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketTemplates": {"method":"GET","path":"/ticket-templates","contract":"orders","summary":"The ticket templates a venue issues from","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaType","in":"query","required":false},{"name":"includeInactive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"printTicketProof": {"method":"POST","path":"/ticket-templates/{templateId}/proof","contract":"orders","summary":"Print a sample without selling anything","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TicketProof"},
"setAppleWalletPass": {"method":"PUT","path":"/apple-wallet-pass","contract":"access","summary":"Apple Wallet Pass Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppleWalletPassDesignerInput","responds":"AppleWalletPassDesignerView"},
"setBrandingLocalizationTemplate": {"method":"PUT","path":"/branding-localization-template","contract":"access","summary":"Save branding and languages for a level","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BrandingLocalizationTemplateInheritanceInput","responds":"BrandingLocalizationTemplateInheritanceView"},
"setDigitalBarcodeTicket": {"method":"PUT","path":"/digital-barcode-ticket","contract":"access","summary":"Digital QR & Barcode Ticket Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DigitalQrBarcodeTicketDesignerInput","responds":"DigitalQrBarcodeTicketDesignerView"},
"setDigitalCardMembership": {"method":"PUT","path":"/digital-card-membership","contract":"access","summary":"Digital Card, Membership & Wearable Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DigitalCardMembershipWearableDesignerInput","responds":"DigitalCardMembershipWearableDesignerView"},
"setDynamicFieldData": {"method":"PUT","path":"/dynamic-field-data","contract":"access","summary":"Dynamic Fields, Data Mapping & Content Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicFieldsDataMappingContentBuilderInput","responds":"DynamicFieldsDataMappingContentBuilderView"},
"setGoogleWalletPass": {"method":"PUT","path":"/google-wallet-pass","contract":"access","summary":"Google Wallet Pass Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GoogleWalletPassDesignerInput","responds":"GoogleWalletPassDesignerView"},
"setPdfPrintablePos": {"method":"PUT","path":"/pdf-printable-pos","contract":"access","summary":"PDF, Printable & POS Ticket Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PdfPrintablePosTicketDesignerInput","responds":"PdfPrintablePosTicketDesignerView"},
"setRfidNfcCard": {"method":"PUT","path":"/rfid-nfc-card","contract":"access","summary":"RFID, NFC, Card & Wristband Media Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RfidNfcCardWristbandMediaDesignerInput","responds":"RfidNfcCardWristbandMediaDesignerView"},
"updateTicketTemplate": {"method":"PATCH","path":"/ticket-templates/{templateId}","contract":"orders","summary":"Change or retire a ticket template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TicketTemplateRequest","responds":"TicketTemplate"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessMediaTemplate": {"type":"object","x-ticvai-persistence":"access.media_template","description":"One media design template (QR/barcode, PDF/print/POS, Apple Wallet, Google Wallet, RFID/NFC card or wristband, digital card or membership) with its design document, status and effective range (declared 29 September, data-model close-out DM1). A designer write on a template `pendingApproval` or `scheduled` is refused `409 template-in-flight`; archiveMediaTemplate archives one (decided 29 September, writers pass).","required":["id","name","designer","mediaType","status","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The templateId of the designer operations"},"name":{"type":"string","maxLength":200},"designer":{"type":"string","enum":["digitalBarcode","pdfPrintablePos","appleWallet","googleWallet","rfidNfcCard","digitalCardMembership"],"description":"Which designer owns the design document"},"mediaType":{"type":"string","enum":["qrTicket","dynamicQrTicket","barcodeTicket","mobileTicket","pdf","a4A5","thermal","pos","customPrint","appleWallet","googleWallet","rfidCard","rfidWristband","nfcCard","nfcWristband","membershipCard","customWearable"]},"brandId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","nullable":true},"language":{"type":"string","maxLength":35,"nullable":true,"description":"BCP 47 tag"},"design":{"type":"object","description":"The working design document - the writable body of the designer operation named by designer, less templateId (jsonb)"},"status":{"type":"string","enum":["draft","pendingApproval","scheduled","published","archived"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"nullable":true,"description":"Latest published version (access.media_template_version)"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AppleWalletPassDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Apple Wallet Pass Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"passIdentity":{"type":"string","description":"Pass identity"},"organization":{"type":"string","description":"Organization"},"description":{"type":"string","description":"Description"},"logo":{"type":"string","description":"Logo"},"icon":{"type":"string","description":"Icon"},"imagesWhereSupported":{"type":"array","items":{"type":"string"},"description":"Images where supported"},"backgroundAppearance":{"type":"string","description":"Background appearance"},"foregroundAppearance":{"type":"string","description":"Foreground appearance"},"labelAppearance":{"type":"string","description":"Label appearance"},"primaryFields":{"type":"array","items":{"type":"string"},"description":"Primary fields"},"secondaryFields":{"type":"array","items":{"type":"string"},"description":"Secondary fields"},"auxiliaryFields":{"type":"array","items":{"type":"string"},"description":"Auxiliary fields"},"headerFields":{"type":"array","items":{"type":"string"},"description":"Header fields"},"backFields":{"type":"array","items":{"type":"string"},"description":"Back fields"},"credentialEncoding":{"type":"string","enum":["qr","barcode","tokenReference"],"description":"How the credential is carried on the pass, per the credential profile"},"dynamicUpdates":{"type":"boolean","description":"Issued passes receive updates"},"updateTriggers":{"type":"array","items":{"type":"string","enum":["eventChange","seatChange","ticketStatusChange"]},"description":"Changes that push an update to issued passes"},"relevantNotificationUpdateBehavior":{"type":"string","description":"Relevant notification/update behavior"},"expiry":{"type":"string","description":"Expiry rule for the pass, e.g. end of validity"},"revocationInvalidationBehaviorWhereSupported":{"type":"string","description":"Revocation/invalidation behavior where supported"}},"required":["templateId"]},
"AppleWalletPassDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Apple Wallet Pass Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"passIdentity":{"type":"string","description":"Pass identity"},"organization":{"type":"string","description":"Organization"},"description":{"type":"string","description":"Description"},"logo":{"type":"string","description":"Logo"},"icon":{"type":"string","description":"Icon"},"imagesWhereSupported":{"type":"array","items":{"type":"string"},"description":"Images where supported"},"backgroundAppearance":{"type":"string","description":"Background appearance"},"foregroundAppearance":{"type":"string","description":"Foreground appearance"},"labelAppearance":{"type":"string","description":"Label appearance"},"primaryFields":{"type":"array","items":{"type":"string"},"description":"Primary fields"},"secondaryFields":{"type":"array","items":{"type":"string"},"description":"Secondary fields"},"auxiliaryFields":{"type":"array","items":{"type":"string"},"description":"Auxiliary fields"},"headerFields":{"type":"array","items":{"type":"string"},"description":"Header fields"},"backFields":{"type":"array","items":{"type":"string"},"description":"Back fields"},"credentialEncoding":{"type":"string","enum":["qr","barcode","tokenReference"],"description":"How the credential is carried on the pass, per the credential profile"},"dynamicUpdates":{"type":"boolean","description":"Issued passes receive updates"},"updateTriggers":{"type":"array","items":{"type":"string","enum":["eventChange","seatChange","ticketStatusChange"]},"description":"Changes that push an update to issued passes"},"relevantNotificationUpdateBehavior":{"type":"string","description":"Relevant notification/update behavior"},"expiry":{"type":"string","description":"Expiry rule for the pass, e.g. end of validity"},"revocationInvalidationBehaviorWhereSupported":{"type":"string","description":"Revocation/invalidation behavior where supported"}},"required":["templateId"]},
"BrandingLocalizationTemplateInheritanceInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Branding, Localization & Template Inheritance submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["level","scopeId","sourceLanguage"],"properties":{"level":{"type":"string","enum":["tenant","brand","venue","event","product","mediaTemplate"]},"scopeId":{"type":"string"},"parentScopeId":{"type":"string","description":"The level above this one inherits from; empty at tenant"},"logo":{"type":"string","description":"Asset library reference"},"colors":{"type":"array","items":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}},"typography":{"type":"string"},"backgrounds":{"type":"string"},"headerFooter":{"type":"string"},"legalFooter":{"type":"string"},"supportInformation":{"type":"string"},"sponsorPlacement":{"type":"string"},"images":{"type":"array","items":{"type":"string"}},"sourceLanguage":{"type":"string","maxLength":35,"description":"BCP 47 tag"},"languages":{"type":"array","items":{"type":"string","maxLength":35},"description":"Additional configured languages (BCP 47)"},"rtl":{"type":"boolean","default":false,"description":"Right-to-left layout for the RTL languages in `languages`"},"fieldOverrides":{"type":"object","additionalProperties":{"type":"string"},"description":"Field-level overrides of the inherited template, keyed by field name"}}},
"BrandingLocalizationTemplateInheritanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Branding, Localization & Template Inheritance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"parentScopeId":{"type":"string","description":"The level above this one inherits from; empty at tenant (decided 29 September, VM close-out)"},"rtl":{"type":"boolean","description":"Right-to-left layout for the RTL languages in `languages` (decided 29 September, VM close-out)"},"scopeId":{"type":"string","description":"ID of the tenant, brand, venue, event, product or template at that level"},"level":{"type":"string","enum":["tenant","brand","venue","event","product","mediaTemplate"],"description":"Inheritance level"},"logo":{"type":"string","description":"Logo"},"colors":{"type":"array","items":{"type":"string"},"description":"Colors"},"typography":{"type":"string","description":"Typography"},"backgrounds":{"type":"string","description":"Backgrounds"},"headerFooter":{"type":"string","description":"Header/footer"},"legalFooter":{"type":"string","description":"Legal footer"},"supportInformation":{"type":"string","description":"Support information"},"sponsorPlacement":{"type":"string","description":"Sponsor placement"},"images":{"type":"array","items":{"type":"string"},"description":"Images"},"sourceLanguage":{"type":"string","description":"Source language"},"translation":{"type":"string","description":"Translation"},"translationStatus":{"type":"string","enum":["notStarted","inProgress","inReview","approved"],"description":"Translation status"},"reviewer":{"type":"string","description":"Reviewer"},"approval":{"type":"string","description":"Approval"},"version":{"type":"string","description":"Version"},"languages":{"type":"array","items":{"type":"string"},"description":"Language codes; English and Arabic at minimum, plus configured languages"}},"required":["level","scopeId"]},
"CloneTicketTemplateInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `cloneTicketTemplate` takes (decided 29 September, readiness close-out).","required":["name","source"],"properties":{"name":{"type":"string","maxLength":120},"source":{"type":"string","description":"What the template in the path is (decided 29 September, readiness close-out).","enum":["existingTemplate","venueTemplate","productTemplate"]},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"The venue whose template is copied. Required for `venueTemplate`."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product the template issues for. Required for `productTemplate`."}}},
"DigitalCardMembershipWearableDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Digital Card, Membership & Wearable Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"brand":{"type":"string","description":"Brand"},"cardArtwork":{"type":"string","description":"Card artwork"},"memberPhotograph":{"type":"string","description":"Member photograph"},"memberName":{"type":"string","description":"Member name"},"membershipNumber":{"type":"string","description":"Membership number"},"tier":{"type":"string","description":"Tier"},"validity":{"type":"string","description":"Validity"},"qrBarcode":{"type":"string","description":"QR/barcode"},"status":{"type":"string","description":"Status"},"benefitsSummary":{"type":"string","description":"Benefits summary"},"dynamicMessaging":{"type":"string","description":"Dynamic messaging"},"tierDesigns":{"type":"array","items":{"type":"string"},"description":"Artwork per tier, e.g. Silver, Gold, Platinum"},"membershipTypes":{"type":"array","items":{"type":"string"},"description":"Membership types"},"brands":{"type":"array","items":{"type":"string"},"description":"Brands"},"venues":{"type":"array","items":{"type":"string"},"description":"Venues"},"ageCategories":{"type":"array","items":{"type":"string"},"description":"Age categories"},"stateTriggers":{"type":"array","items":{"type":"string","enum":["membershipRenewal","tierChange","expiry","suspension","benefitStatus"]},"description":"Changes that alter how the persistent card is presented"}},"required":["templateId"]},
"DigitalCardMembershipWearableDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Digital Card, Membership & Wearable Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"brand":{"type":"string","description":"Brand"},"cardArtwork":{"type":"string","description":"Card artwork"},"memberPhotograph":{"type":"string","description":"Member photograph"},"memberName":{"type":"string","description":"Member name"},"membershipNumber":{"type":"string","description":"Membership number"},"tier":{"type":"string","description":"Tier"},"validity":{"type":"string","description":"Validity"},"qrBarcode":{"type":"string","description":"QR/barcode"},"status":{"type":"string","description":"Status"},"benefitsSummary":{"type":"string","description":"Benefits summary"},"dynamicMessaging":{"type":"string","description":"Dynamic messaging"},"tierDesigns":{"type":"array","items":{"type":"string"},"description":"Artwork per tier, e.g. Silver, Gold, Platinum"},"membershipTypes":{"type":"array","items":{"type":"string"},"description":"Membership types"},"brands":{"type":"array","items":{"type":"string"},"description":"Brands"},"venues":{"type":"array","items":{"type":"string"},"description":"Venues"},"ageCategories":{"type":"array","items":{"type":"string"},"description":"Age categories"},"stateTriggers":{"type":"array","items":{"type":"string","enum":["membershipRenewal","tierChange","expiry","suspension","benefitStatus"]},"description":"Changes that alter how the persistent card is presented"}},"required":["templateId"]},
"DigitalQrBarcodeTicketDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Digital QR & Barcode Ticket Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"components":{"type":"array","items":{"type":"string","enum":["logo","eventImage","eventName","ticketType","customerName","participantName","date","time","venue","entrance","section","row","seat","price","orderReference","virtualTicketId","qr","barcode","terms","instructions","waiverLinkStatus","sponsor","customFields"]},"description":"Components placed on the layout; values come from the dynamic-field library"},"qrMode":{"type":"string","enum":["staticQr","dynamicQr","signedQr","tokenizedQr"],"description":"QR payload profile"},"rotationBehaviorWhereSupported":{"type":"string","description":"Rotation behavior where supported"},"size":{"type":"string","description":"Size"},"position":{"type":"string","description":"Position"},"quietZone":{"type":"string","description":"Quiet zone"},"errorCorrection":{"type":"string","enum":["l","m","q","h"],"description":"QR error-correction level"},"expiration":{"type":"string","description":"Expiration"},"refreshBehavior":{"type":"string","description":"Refresh behavior"},"barcodeType":{"type":"string","description":"Barcode type"},"orientation":{"type":"string","description":"Orientation"},"humanReadableValue":{"type":"boolean","description":"Human-readable value"},"hideShowEncodedReference":{"type":"boolean","description":"Show the encoded reference"},"showPriceOnOff":{"type":"boolean","description":"Show price on the ticket"}},"required":["templateId"]},
"DigitalQrBarcodeTicketDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Digital QR & Barcode Ticket Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"components":{"type":"array","items":{"type":"string","enum":["logo","eventImage","eventName","ticketType","customerName","participantName","date","time","venue","entrance","section","row","seat","price","orderReference","virtualTicketId","qr","barcode","terms","instructions","waiverLinkStatus","sponsor","customFields"]},"description":"Components placed on the layout; values come from the dynamic-field library"},"qrMode":{"type":"string","enum":["staticQr","dynamicQr","signedQr","tokenizedQr"],"description":"QR payload profile"},"rotationBehaviorWhereSupported":{"type":"string","description":"Rotation behavior where supported"},"size":{"type":"string","description":"Size"},"position":{"type":"string","description":"Position"},"quietZone":{"type":"string","description":"Quiet zone"},"errorCorrection":{"type":"string","enum":["l","m","q","h"],"description":"QR error-correction level"},"expiration":{"type":"string","description":"Expiration"},"refreshBehavior":{"type":"string","description":"Refresh behavior"},"barcodeType":{"type":"string","description":"Barcode type"},"orientation":{"type":"string","description":"Orientation"},"humanReadableValue":{"type":"boolean","description":"Human-readable value"},"hideShowEncodedReference":{"type":"boolean","description":"Show the encoded reference"},"showPriceOnOff":{"type":"boolean","description":"Show price on the ticket"}},"required":["templateId"]},
"DynamicFieldsDataMappingContentBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.entitlement at 3%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Dynamic Fields, Data Mapping & Content Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"category":{"type":"string","enum":["customer","participant","order","virtualTicket","productEvent","seating","commercial","membership","compliance","credential","custom"],"description":"Field group"},"fieldKey":{"type":"string","description":"Token used in templates, e.g. ticket.seat"},"standardField":{"type":"string","enum":["customerName","customerId","mobile","email","photo","participantName","dobAgeCategory","participantId","orderId","bookingReference","purchaseDate","channel","virtualTicketId","ticketType","status","validity","usageStatus","product","event","performance","date","time","venue","entrance","section","block","row","seat","faceValue","paidPrice","discount","currency","membershipId","tier","expiry","waiverStatus","waiverLink","qr","barcode","credentialReference"],"description":"Standard source field; empty for a tenant-defined custom field"},"dateFormats":{"type":"string","description":"Date format pattern"},"timeFormat":{"type":"string","description":"Time format pattern"},"numberFormat":{"type":"string","description":"Number formatting"},"textTransformation":{"type":"string","description":"Text transformation"},"characterLimit":{"type":"integer","description":"Character limit"},"conditionalVisibility":{"type":"string","description":"Condition under which the field shows, e.g. seat assigned"},"allowedMedia":{"type":"array","items":{"type":"string"},"description":"Media types that may display this field"},"sensitive":{"type":"boolean","description":"Personal or sensitive data; not permitted on media by default"}},"required":["fieldKey","category"]},
"DynamicFieldsDataMappingContentBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Dynamic Fields, Data Mapping & Content Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"category":{"type":"string","enum":["customer","participant","order","virtualTicket","productEvent","seating","commercial","membership","compliance","credential","custom"],"description":"Field group"},"fieldKey":{"type":"string","description":"Token used in templates, e.g. ticket.seat"},"standardField":{"type":"string","enum":["customerName","customerId","mobile","email","photo","participantName","dobAgeCategory","participantId","orderId","bookingReference","purchaseDate","channel","virtualTicketId","ticketType","status","validity","usageStatus","product","event","performance","date","time","venue","entrance","section","block","row","seat","faceValue","paidPrice","discount","currency","membershipId","tier","expiry","waiverStatus","waiverLink","qr","barcode","credentialReference"],"description":"Standard source field; empty for a tenant-defined custom field"},"dateFormats":{"type":"string","description":"Date format pattern"},"timeFormat":{"type":"string","description":"Time format pattern"},"numberFormat":{"type":"string","description":"Number formatting"},"textTransformation":{"type":"string","description":"Text transformation"},"characterLimit":{"type":"integer","description":"Character limit"},"conditionalVisibility":{"type":"string","description":"Condition under which the field shows, e.g. seat assigned"},"allowedMedia":{"type":"array","items":{"type":"string"},"description":"Media types that may display this field"},"sensitive":{"type":"boolean","description":"Personal or sensitive data; not permitted on media by default"}},"required":["fieldKey","category"]},
"GoogleWalletPassDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Google Wallet Pass Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"passClass":{"type":"string","description":"Pass class"},"passTemplate":{"type":"string","description":"Pass template"},"issuer":{"type":"string","description":"Issuer"},"title":{"type":"string","description":"Title"},"logo":{"type":"string","description":"Logo"},"heroImageAssetsWhereApplicable":{"type":"array","items":{"type":"string"},"description":"Hero/image assets where applicable"},"eventInformation":{"type":"string","description":"Event information"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","description":"Field key mapped to the event date/time"},"ticketHolder":{"type":"string","description":"Ticket holder"},"seat":{"type":"string","description":"Seat"},"ticketType":{"type":"string","description":"Ticket type"},"customFields":{"type":"array","items":{"type":"string"},"description":"Custom fields"},"status":{"type":"string","description":"Status"},"links":{"type":"array","items":{"type":"string"},"description":"Links"},"additionalInformation":{"type":"string","description":"Additional information"},"credentialEncoding":{"type":"string","enum":["qr","barcode","credentialTokenReference"],"description":"How the credential is carried on the pass"},"updateTriggers":{"type":"array","items":{"type":"string","enum":["eventTimeChange","venueChange","seatReassignment","ticketStatusChange","otherTicketInformationChange"]},"description":"Changes that push an update to issued passes"}},"required":["templateId"]},
"GoogleWalletPassDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Google Wallet Pass Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"passClass":{"type":"string","description":"Pass class"},"passTemplate":{"type":"string","description":"Pass template"},"issuer":{"type":"string","description":"Issuer"},"title":{"type":"string","description":"Title"},"logo":{"type":"string","description":"Logo"},"heroImageAssetsWhereApplicable":{"type":"array","items":{"type":"string"},"description":"Hero/image assets where applicable"},"eventInformation":{"type":"string","description":"Event information"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","description":"Field key mapped to the event date/time"},"ticketHolder":{"type":"string","description":"Ticket holder"},"seat":{"type":"string","description":"Seat"},"ticketType":{"type":"string","description":"Ticket type"},"customFields":{"type":"array","items":{"type":"string"},"description":"Custom fields"},"status":{"type":"string","description":"Status"},"links":{"type":"array","items":{"type":"string"},"description":"Links"},"additionalInformation":{"type":"string","description":"Additional information"},"credentialEncoding":{"type":"string","enum":["qr","barcode","credentialTokenReference"],"description":"How the credential is carried on the pass"},"updateTriggers":{"type":"array","items":{"type":"string","enum":["eventTimeChange","venueChange","seatReassignment","ticketStatusChange","otherTicketInformationChange"]},"description":"Changes that push an update to issued passes"}},"required":["templateId"]},
"MediaDesignStudioCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Design Studio Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Template ID"},"templateName":{"type":"string","description":"Template Name"},"mediaType":{"type":"string","enum":["qrTicket","dynamicQrTicket","barcodeTicket","mobileTicket","pdf","a4A5","thermal","pos","customPrint","appleWallet","googleWallet","rfidCard","rfidWristband","nfcCard","nfcWristband","membershipCard","customWearable"],"description":"Media the template is for"},"brand":{"type":"string","description":"Brand"},"venue":{"type":"string","description":"Venue"},"productEventAssociation":{"type":"string","description":"Product / Event association"},"language":{"type":"string","description":"Language"},"version":{"type":"string","description":"Version"},"effectiveFrom":{"type":"string","format":"date-time","description":"Effective From"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective To"},"status":{"type":"string","enum":["draft","pendingApproval","scheduled","published","archived"],"description":"Template status"},"owner":{"type":"string","description":"Owner"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"}}},
"MediaDesignStudioCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalMediaTemplates":{"type":"integer","description":"Total Media Templates"},"published":{"type":"integer","description":"Published"},"draft":{"type":"integer","description":"Draft"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduled":{"type":"integer","description":"Scheduled"},"archived":{"type":"integer","description":"Archived"},"qrDigitalTemplates":{"type":"integer","description":"QR / Digital Templates"},"pdfPrintTemplates":{"type":"integer","description":"PDF / Print Templates"},"appleWalletTemplates":{"type":"integer","description":"Apple Wallet Templates"},"googleWalletTemplates":{"type":"integer","description":"Google Wallet Templates"},"rfidNfcTemplates":{"type":"integer","description":"RFID / NFC Templates"},"cardWristbandTemplates":{"type":"integer","description":"Card / Wristband Templates"},"templatesRequiringReview":{"type":"integer","description":"Templates Requiring Review"},"templatesWithValidationErrors":{"type":"integer","description":"Templates with Validation Errors"}}},
"MultiMediaPreviewTestingApprovalPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Multi-Media Preview, Testing, Approval & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"publishMode":{"type":"string","enum":["publishNow","schedule"],"description":"Publish now or on a schedule"},"templateId":{"type":"string","description":"Media template being published"},"validationChecks":{"type":"array","items":{"type":"string","enum":["dynamicFields","missingFields","qrReadability","barcodeReadability","walletConfiguration","printBoundaries","localization","rtl","branding","imageResolution","credentialPayload","virtualTicketResolution","providerConfiguration"]},"description":"Pre-publication checks run"},"previewTargets":{"type":"array","items":{"type":"string","enum":["desktop","mobile","tablet","printer","pos","wallet","encoder"]},"description":"Targets previewed"},"selectedBrands":{"type":"array","items":{"type":"string"},"description":"Selected Brands"},"selectedVenues":{"type":"array","items":{"type":"string"},"description":"Selected Venues"},"selectedProducts":{"type":"array","items":{"type":"string"},"description":"Selected Products"},"selectedChannels":{"type":"array","items":{"type":"string"},"description":"Selected Channels"},"controlledRollout":{"type":"boolean","description":"Controlled rollout"},"templateVersion":{"type":"string","description":"Version created by this publication"},"scheduledAt":{"type":"string","format":"date-time","description":"Publication time when scheduled"}},"required":["templateId","publishMode"]},
"MultiMediaPreviewTestingApprovalPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Media Preview, Testing, Approval & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publishMode":{"type":"string","enum":["publishNow","schedule"],"description":"Publish now or on a schedule"},"templateId":{"type":"string","description":"Media template being published"},"validationChecks":{"type":"array","items":{"type":"string","enum":["dynamicFields","missingFields","qrReadability","barcodeReadability","walletConfiguration","printBoundaries","localization","rtl","branding","imageResolution","credentialPayload","virtualTicketResolution","providerConfiguration"]},"description":"Pre-publication checks run"},"previewTargets":{"type":"array","items":{"type":"string","enum":["desktop","mobile","tablet","printer","pos","wallet","encoder"]},"description":"Targets previewed"},"selectedBrands":{"type":"array","items":{"type":"string"},"description":"Selected Brands"},"selectedVenues":{"type":"array","items":{"type":"string"},"description":"Selected Venues"},"selectedProducts":{"type":"array","items":{"type":"string"},"description":"Selected Products"},"selectedChannels":{"type":"array","items":{"type":"string"},"description":"Selected Channels"},"controlledRollout":{"type":"boolean","description":"Controlled rollout"},"templateVersion":{"type":"string","description":"Version created by this publication"},"scheduledAt":{"type":"string","format":"date-time","description":"Publication time when scheduled"}},"required":["templateId","publishMode"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PdfPrintablePosTicketDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What PDF, Printable & POS Ticket Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"outputFormat":{"type":"string","enum":["pdf","a4","a5","customDimensions","posReceipt","thermalTicket","boxOfficeStock","prePrintedStock"],"description":"Print output this template produces"},"pageSize":{"type":"string","description":"Page size"},"orientation":{"type":"string","description":"Orientation"},"margins":{"type":"string","description":"Margins"},"header":{"type":"string","description":"Header"},"footer":{"type":"string","description":"Footer"},"background":{"type":"string","description":"Background"},"logo":{"type":"string","description":"Logo"},"images":{"type":"array","items":{"type":"string"},"description":"Images"},"text":{"type":"string","description":"Text"},"dynamicFields":{"type":"array","items":{"type":"string"},"description":"Field keys from the dynamic-field library"},"qrBarcode":{"type":"string","description":"QR/barcode"},"terms":{"type":"string","description":"Terms"},"perforationIndicatorsWhereApplicable":{"type":"string","description":"Perforation indicators where applicable"},"printSafeZones":{"type":"string","description":"Print-safe zones"},"printerProfile":{"type":"string","description":"Printer profile"},"dpi":{"type":"integer","description":"DPI"},"paperStockType":{"type":"string","description":"Paper/stock type"},"thermalLayout":{"type":"string","description":"Thermal layout"},"cutBehavior":{"type":"string","description":"Cut behavior"},"supportedPrinterIntegration":{"type":"string","description":"Supported printer integration"}},"required":["templateId","outputFormat"]},
"PdfPrintablePosTicketDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What PDF, Printable & POS Ticket Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"outputFormat":{"type":"string","enum":["pdf","a4","a5","customDimensions","posReceipt","thermalTicket","boxOfficeStock","prePrintedStock"],"description":"Print output this template produces"},"pageSize":{"type":"string","description":"Page size"},"orientation":{"type":"string","description":"Orientation"},"margins":{"type":"string","description":"Margins"},"header":{"type":"string","description":"Header"},"footer":{"type":"string","description":"Footer"},"background":{"type":"string","description":"Background"},"logo":{"type":"string","description":"Logo"},"images":{"type":"array","items":{"type":"string"},"description":"Images"},"text":{"type":"string","description":"Text"},"dynamicFields":{"type":"array","items":{"type":"string"},"description":"Field keys from the dynamic-field library"},"qrBarcode":{"type":"string","description":"QR/barcode"},"terms":{"type":"string","description":"Terms"},"perforationIndicatorsWhereApplicable":{"type":"string","description":"Perforation indicators where applicable"},"printSafeZones":{"type":"string","description":"Print-safe zones"},"printerProfile":{"type":"string","description":"Printer profile"},"dpi":{"type":"integer","description":"DPI"},"paperStockType":{"type":"string","description":"Paper/stock type"},"thermalLayout":{"type":"string","description":"Thermal layout"},"cutBehavior":{"type":"string","description":"Cut behavior"},"supportedPrinterIntegration":{"type":"string","description":"Supported printer integration"}},"required":["templateId","outputFormat"]},
"RfidNfcCardWristbandMediaDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What RFID, NFC, Card & Wristband Media Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"mediaKind":{"type":"string","enum":["rfidCard","rfidWristband","nfcCard","nfcWristband","membershipCard","staffGuestCard","customWearable"],"description":"Physical medium"},"reusability":{"type":"string","enum":["disposable","reusable"],"description":"Disposable or reusable medium"},"printed":{"type":"boolean","description":"Printed"},"encoded":{"type":"boolean","description":"Encoded"},"colorCategory":{"type":"string","description":"Color/category"},"sizeWhereApplicable":{"type":"string","description":"Size where applicable"},"activationAtCollection":{"type":"boolean","description":"Activation at collection"},"depositReferenceWhereApplicable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit/reference where applicable"},"mediaDimensions":{"type":"string","description":"Media dimensions"},"front":{"type":"string","description":"Front"},"back":{"type":"string","description":"Back"},"printableArea":{"type":"string","description":"Printable area"},"logo":{"type":"string","description":"Logo"},"printedFields":{"type":"array","items":{"type":"string","enum":["customerName","photo","membershipTier","expiry","serialNumber","qrBarcode"]},"description":"Personal and reference fields printed on the medium"},"customArtwork":{"type":"string","description":"Custom artwork"},"sponsorVenueBranding":{"type":"string","description":"Sponsor/venue branding"},"rfidNfcTechnology":{"type":"string","description":"RFID/NFC technology"},"chipProfile":{"type":"string","description":"Chip/profile"},"uidReferenceHandling":{"type":"string","description":"UID/reference handling"},"encodingProfile":{"type":"string","description":"Encoding profile"},"provider":{"type":"string","description":"Provider"},"readerCompatibility":{"type":"array","items":{"type":"string"},"description":"Reader compatibility"},"printerEncoderIntegration":{"type":"string","description":"Printer/encoder integration"}},"required":["templateId","mediaKind"]},
"RfidNfcCardWristbandMediaDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What RFID, NFC, Card & Wristband Media Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Media template being designed"},"mediaKind":{"type":"string","enum":["rfidCard","rfidWristband","nfcCard","nfcWristband","membershipCard","staffGuestCard","customWearable"],"description":"Physical medium"},"reusability":{"type":"string","enum":["disposable","reusable"],"description":"Disposable or reusable medium"},"printed":{"type":"boolean","description":"Printed"},"encoded":{"type":"boolean","description":"Encoded"},"colorCategory":{"type":"string","description":"Color/category"},"sizeWhereApplicable":{"type":"string","description":"Size where applicable"},"activationAtCollection":{"type":"boolean","description":"Activation at collection"},"depositReferenceWhereApplicable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit/reference where applicable"},"mediaDimensions":{"type":"string","description":"Media dimensions"},"front":{"type":"string","description":"Front"},"back":{"type":"string","description":"Back"},"printableArea":{"type":"string","description":"Printable area"},"logo":{"type":"string","description":"Logo"},"printedFields":{"type":"array","items":{"type":"string","enum":["customerName","photo","membershipTier","expiry","serialNumber","qrBarcode"]},"description":"Personal and reference fields printed on the medium"},"customArtwork":{"type":"string","description":"Custom artwork"},"sponsorVenueBranding":{"type":"string","description":"Sponsor/venue branding"},"rfidNfcTechnology":{"type":"string","description":"RFID/NFC technology"},"chipProfile":{"type":"string","description":"Chip/profile"},"uidReferenceHandling":{"type":"string","description":"UID/reference handling"},"encodingProfile":{"type":"string","description":"Encoding profile"},"provider":{"type":"string","description":"Provider"},"readerCompatibility":{"type":"array","items":{"type":"string"},"description":"Reader compatibility"},"printerEncoderIntegration":{"type":"string","description":"Printer/encoder integration"}},"required":["templateId","mediaKind"]},
"TicketProof": {"type":"object","x-ticvai-persistence":"none — rendered on request, nothing is stored","description":"A sample ticket from a template, **marked as a proof on the artefact itself** so it cannot be presented at a gate.","required":["templateId","mediaType","contentRef"],"properties":{"templateId":{"type":"string","format":"uuid"},"mediaType":{"type":"string","enum":["thermalTicket","a4Pdf","wristband","rfidCard","walletPass","qrOnly","sms"]},"locale":{"type":"string","nullable":true},"contentRef":{"type":"string","format":"uri","description":"Where the rendered proof can be fetched or sent to the printer from."},"walletPlatform":{"type":"string","nullable":true,"enum":["appleWallet","googleWallet"],"description":"Which wallet the pass preview is for, where `mediaType` is `walletPass` (DEC-151; CHG-CSP-038)."}}},
"TicketTemplate": {"type":"object","x-ticvai-persistence":"orders.ticket_template + orders.ticket_template_channel","description":"BL-102. **A venue changing its ticket artwork had no path that was not a code change.**\n2.16.6 asks to print a proof without processing a sale — the equivalent of `white-label.createPreview`, and the same reason: **artwork is checked by looking at it, and the only way to look at it was to sell something.**\n","required":["id","name","mediaType","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isRecyclable":{"type":"boolean","default":false,"description":"BL-103. **An RFID wristband handed back at the exit is stock, not waste** — and nothing released it, so a venue reissuing one had a card serving two entitlements.\n**Replacement disables the previous medium automatically**, following the F23 rule: a guest issued a replacement wristband must not walk in on the old one, and relying on somebody remembering to blacklist it is how they do.\n"},"recycleAfterDays":{"type":"integer","nullable":true,"description":"**A quarantine before reissue.** A wristband returned today and reissued tomorrow to a different guest is a support call waiting to happen when the first guest's app still shows it.\n"},"mediaType":{"type":"string","enum":["thermalTicket","a4Pdf","wristband","rfidCard","walletPass","qrOnly","sms"]},"appliesToProductKinds":{"type":"array","items":{"type":"string"}},"appliesToChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"selectionPriority":{"type":"integer","default":100,"description":"2.16.x. **Automatic media-type selection**, which was absent — a kiosk with no printer and a guest with no smartphone need different answers, and neither should be chosen by the caller.\n"},"layoutRef":{"type":"string"},"localeVariants":{"type":"object","additionalProperties":{"type":"string"}},"isActive":{"type":"boolean"}}},
"TicketTemplateImportInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `importTicketTemplate` takes (decided 29 September, readiness close-out).","required":["format","fileRef","name"],"properties":{"format":{"type":"string","maxLength":30,"description":"The definition format of the file. One the service does not read is a 422."},"fileRef":{"type":"string","format":"uuid","description":"The uploaded definition file."},"name":{"type":"string","maxLength":120}}},
"TicketTemplateRequest": {"type":"object","description":"Request only; persisted as `TicketTemplate`. On update every field is optional and absent means unchanged. On create, `name` and `mediaType` are required and the operation enforces it.","properties":{"name":{"type":"string","maxLength":200},"mediaType":{"type":"string","enum":["thermalTicket","a4Pdf","wristband","rfidCard","walletPass","qrOnly","sms"]},"isRecyclable":{"type":"boolean"},"recycleAfterDays":{"type":"integer","minimum":0,"nullable":true},"appliesToProductKinds":{"type":"array","items":{"type":"string"}},"appliesToChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"selectionPriority":{"type":"integer"},"layoutRef":{"type":"string","description":"The artwork, as a media-asset reference."},"localeVariants":{"type":"object","additionalProperties":{"type":"string"}},"isActive":{"type":"boolean"}}}
}
```
