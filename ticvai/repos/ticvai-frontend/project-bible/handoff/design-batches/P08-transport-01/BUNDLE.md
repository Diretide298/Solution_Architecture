# P08-transport-01 — P08 · Transport

**7 screens · 27 operations · 32 schemas · 5 permissions**

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
  `ASSET_LIBRARY_MANAGE, PERFORMANCE_CONFIGURE, TRANSPORT_MANAGE, TRANSPORT_PRICE, TRANSPORT_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1183` | Transport Stations | A | 13 | 13 | 7 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-1184` | Transport Routes & Stops | A | 27 | 18 | 7 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-1185` | Transport Fares & Passenger Types | A | 22 | 44 | 7 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-1186` | Transport Timetables | A | 21 | 14 | 7 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-1187` | Transport Departure Board | A | 14 | 17 | 7 | 4 | 0 | 6 | — | notStarted (generated) |
| `BO-1188` | Transport Pass Types | A | 19 | 18 | 7 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-1189` | Transport Network Import | A | 6 | 27 | 6 | 1 | 0 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1183` Transport Stations

**Create, edit and retire the stations a venue's routes stop at.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28067 (APP-SETUP-BO-1183) |
| Who uses it | venue staff holding `TRANSPORT_MANAGE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTransportStations` reads the population and the panel acts on one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `stationId` (navigation) · cold entry: Resolves the venue from the session; a cold arrival is the ordinary case. |
| Route | `/transport/stations` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Stations come first: a route is an ordered list of them. **A station carries coordinates** because the route map places it; one without them is listed in the stop list and left off the map.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The stations a venue's routes stop at, the first step of transport setup. A station with coordinates is placed on the route map; one without is listed in the stop list only. A station on an active route cannot be deactivated.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Station code or name | search field | — | — | — | — | Filters the loaded page by code and name, in either language. | — |
| Include retired stations | toggle | — | — | — | — | Sends `?includeInactive=true`; retired stations are shown greyed. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include inactive | toggle | off | — | `listTransportStations` ?includeInactive |

**Form: New station** (modal, opened by *New station*; *Create station* calls `createTransportStation`, *Cancel* sends nothing)

**Collects what `createTransportStation` sends before it is called.** Required: `code` (unique at this venue), `name` (every tenant language). Optional: `shortName`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createTransportStation` body |
| Code `code` | text field | required | — | max length 32 | — | Short operator code, e.g. `SHJ-JUB`. | `createTransportStation` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createTransportStation` body |
| Short name `shortName` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The label on the route diagram and the map pin (`Union Sq`, `MoE`). | `createTransportStation` body |
| Latitude `latitude` | number field | optional | — | min -90; max 90 | — | — | `createTransportStation` body |
| Longitude `longitude` | number field | optional | — | min -180; max 180 | — | — | `createTransportStation` body |

Errors to draw in the form: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Retire station** (confirmDialog, opened by *Retire station*; *Retire station* calls `updateTransportStation`, *Keep it* sends nothing)

Names the station and says it stops being offered as a stop. Refused while an active route stops there; the dialog then lists those routes instead of retiring.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateTransportStation` body |
| Short name `shortName` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateTransportStation` body |
| Latitude `latitude` | number field | optional | — | min -90; max 90 | — | — | `updateTransportStation` body |
| Longitude `longitude` | number field | optional | — | min -180; max 180 | — | — | `updateTransportStation` body |
| Active `active` | toggle | optional | — | — | — | — | `updateTransportStation` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The station is a stop on one or more active routes and cannot be deactivated.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **code**: Short operator code, unique in the venue, at most 32 characters (SHJ-JUB). *(source: contracts/satellite/transport.yaml#createTransportStation)*
- **name and shortName**: Every tenant language; the short name is what the route diagram and the map pin show. *(source: contracts/satellite/transport.yaml#createTransportStation)*
- **coordinates**: Picked on a small map or typed; optional, with the "not on map" consequence stated. *(source: contracts/satellite/transport.yaml#createTransportStation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every station at this venue** (data table, from `listTransportStations`): A station with no coordinates is marked "not on the map".

| Shows | Format | Notes |
|---|---|---|
| Code | text | Short operator code, e.g. `SHJ-JUB`. |
| Name | in the reader's language | — |
| Short name | in the reader's language | The label on the route diagram and the map pin (`Union Sq`, `MoE`). |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Active | yes / no (icon or chip) | — |

**The selected station** (detail panel, from `listTransportStations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Code | text | Short operator code, e.g. `SHJ-JUB`. |
| Name | in the reader's language | — |
| Short name | in the reader's language | The label on the route diagram and the map pin (`Union Sq`, `MoE`). |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New station (primary button) | `createTransportStation` POST `/transport/stations` | CreateStationRequest | Station | 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Save station (secondary button) | `updateTransportStation` PATCH `/transport/stations/{stationId}` | inline | Station | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The station is a stop on one or more active routes and cannot be deactivated. | opens confirmDialog first |
| Reactivate station (secondary button) | `updateTransportStation` PATCH `/transport/stations/{stationId}` | inline | Station | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The station is a stop on one or more active routes and cannot be deactivated. | opens confirmDialog first |
| Retire station (destructive button) | `updateTransportStation` PATCH `/transport/stations/{stationId}` | inline | Station | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The station is a stop on one or more active routes and cannot be deactivated. | opens confirmDialog first |

**Data it reads**: `listTransportStations` (onLoad, The venue's stations, retired ones on request)

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*
- → `BO-1189` Transport Network Import: *Import stations, routes and timetables*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's stations, read by `listTransportStations`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No stations yet, so no route can be built.** Offers New station and Import stations, routes and timetables (BO-1189). |
| Empty, no results (`?state=emptyNoResults`) | The search or the retired filter matched nothing and the stations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_MANAGE`, which `createTransportStation` requires, and names that permission. **Never an empty table** — that reads as *there is no data*. |
| Validation (`?state=validation`) | `400` on a missing code or name or a coordinate out of range, marked on the field; `409` on a code already used at this venue, naming the station that holds it; `409` on retiring a station an active route stops at, naming the routes. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 The station is a stop on one or more active routes and cannot be deactivated. |

#### Edge cases to draw

- **Deactivate a station on an active route**: Refused; the dialog lists the routes and offers to open them. *(source: contracts/satellite/transport.yaml#updateTransportStation)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
stations:
- code: AQ-METRO
  name: Al Qudra Metro
  nameAr: مترو القدرة
  short: Metro
- code: DP-MAIN
  name: Dune Park Main Gate
  nameAr: البوابة الرئيسية دون بارك
  short: Main Gate
- code: HOTEL-D
  name: Hotel District
  short: Hotels
```

#### Permissions

- `listTransportStations` → no permission · guest, public, staff
- `createTransportStation` → `TRANSPORT_MANAGE` (configure) · staff
- `updateTransportStation` → `TRANSPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TRANSPORT_MANAGE`, which `createTransportStation` requires, and names that permission. **Never an empty table** — that reads as *there is no data*.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1183` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1183?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: New station, Save station, Reactivate station, Retire station.
- [ ] Every transition is wired: `BO-1184`, `BO-1189`.
- [ ] Every gated control is gated: `TRANSPORT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1184` Transport Routes & Stops

**Create, edit, activate, suspend and retire a venue's routes and their ordered stops.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28068 (APP-SETUP-BO-1184) |
| Who uses it | venue staff holding `TRANSPORT_MANAGE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTransportRoutes` reads the population and `getTransportRoute` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `routeId` (navigation) · cold entry: Resolves the venue from the session and opens on the route list; a route id that is gone says so. |
| Route | `/transport/routes` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). A line run both ways is two routes (outbound and inbound) paired by `pairedRouteId`, which is what the guest's swap button lands on. **Creating a route creates its catalogue side** (an event its departures become performances of, and a timed-admission product whose variants are the passenger types), so a one-way ticket sells through the ordinary cart. Lifecycle draft, active, suspended, retired (states/transport-route.yaml).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where a venue builds each transport line as an ordered list of its stations and controls whether the line is on sale. A route is created as a draft and sells nothing until it is active with a fare table (BO-1185) and a published timetable (BO-1186); the screen must make that readiness visible per route. Creating a route also creates its catalogue side (an event and a timed product).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are the popular-route card's starting fare, featured order and image set per route in the back office?** → Drawn default accepted: Routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(decided by Chinmay, 2026-10-02; DEC-106 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select field | — | — | — | — | Sends `?status=`, draft, active, suspended or retired. Defaults to everything but retired. | — |
| Serves station | select field | — | — | — | — | Sends `?fromStationId=`; stations from `listTransportStations`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From station | picker: choose a from station | — | — | `listTransportRoutes` ?fromStationId |
| To station | picker: choose a to station | — | — | `listTransportRoutes` ?toStationId |
| Status | radio group | — | Draft · Active · Suspended · Retired | `listTransportRoutes` ?status |
| Include inactive | toggle | off | — | `listTransportStations` ?includeInactive |

**Form: New route** (modal, opened by *New route*; *Create route* calls `createTransportRoute`, *Cancel* sends nothing)

**Collects what `createTransportRoute` sends before it is called.** Required: `code`, `name`, `stops` (stations in order, each with its offset in minutes; the first is 0). Optional: `lineCode`, `colour`, `pairedRouteId` (the same line the other way), `bookingCutoffMinutes`. Created as a draft; nothing is on sale. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createTransportRoute` body |
| Code `code` | text field | required | — | max length 32 | — | The line and direction, e.g. `E101-Out`. | `createTransportRoute` body |
| Line code `lineCode` | text field | optional | — | max length 16 | — | The public line number shared by both directions, e.g. `E101`. | `createTransportRoute` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createTransportRoute` body |
| Colour `colour` | text field | optional | — | pattern `^#[0-9a-fA-F]{6}$` | — | — | `createTransportRoute` body |
| Paired route `pairedRouteId` | picker: choose a paired route | optional | — | — | shows names, sends the id | The same line run the other way. The swap button lands on it. | `createTransportRoute` body |
| Booking cutoff minutes `bookingCutoffMinutes` | number field (minutes) | optional | 5 | min 0; max 1440 | — | How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's "Boarding closes five minutes before departure", client to … | `createTransportRoute` body |
| Stops `stops` | repeatable rows | required | — | at least 2; at most 100 | — | — | `createTransportRoute` body |
| Station `stops[].stationId` | picker: choose a station | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `createTransportRoute` body |
| Offset minutes `stops[].offsetMinutes` | number field (minutes) | required | — | min 0; max 1440 | — | Minutes after the departure from the first stop that the coach leaves this one. 0 on the first stop; strictly increasing along the route. | `createTransportRoute` body |
| Boarding allowed `stops[].boardingAllowed` | toggle | optional | on | — | — | — | `createTransportRoute` body |
| Alighting allowed `stops[].alightingAllowed` | toggle | optional | on | — | — | — | `createTransportRoute` body |

Errors to draw in the form: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 Fewer than two stops, a station repeated, a station that is inactive or not in this venue, or offsets that do not start at 0 and strictly increase.

**Form: Activate, suspend or reactivate** (confirmDialog, opened by *Activate, suspend or reactivate*; *Change status* calls `setTransportRouteStatus`, *Cancel* sends nothing)

Names the route and the consequence of the new status for guests and for tickets already sold. Captures a `reason` for a suspension.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Draft · Active · Suspended · Retired | — | — | `setTransportRouteStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `setTransportRouteStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current status, the route has no fare table, or retiring a route with sold seats on a departure still on sale.

**Form: Retire route** (confirmDialog, opened by *Retire route*; *Retire route* calls `setTransportRouteStatus`, *Keep it* sends nothing)

**Retiring is final.** Refused while a departure still on sale has sold seats; the dialog then names those departures and offers the departure board (BO-1187) to cancel them first.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Draft · Active · Suspended · Retired | — | — | `setTransportRouteStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `setTransportRouteStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current status, the route has no fare table, or retiring a route with sold seats on a departure still on sale.

**Sent by *Save route*** (`updateTransportRoute`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateTransportRoute` body |
| Colour `colour` | text field | optional | — | pattern `^#[0-9a-fA-F]{6}$` | — | — | `updateTransportRoute` body |
| Paired route `pairedRouteId` | picker: choose a paired route | optional | — | — | shows names, sends the id | — | `updateTransportRoute` body |
| Booking cutoff minutes `bookingCutoffMinutes` | number field (minutes) | optional | — | min 0; max 1440 | — | — | `updateTransportRoute` body |
| Stops `stops` | repeatable rows | optional | — | at least 2 | — | — | `updateTransportRoute` body |
| Station `stops[].stationId` | picker: choose a station | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `updateTransportRoute` body |
| Offset minutes `stops[].offsetMinutes` | number field (minutes) | required | — | min 0; max 1440 | — | Minutes after the departure from the first stop that the coach leaves this one. 0 on the first stop; strictly increasing along the route. | `updateTransportRoute` body |
| Boarding allowed `stops[].boardingAllowed` | toggle | optional | on | — | — | — | `updateTransportRoute` body |
| Alighting allowed `stops[].alightingAllowed` | toggle | optional | on | — | — | — | `updateTransportRoute` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **stops**: An ordered, drag-to-reorder list of stations picked from BO-1183, each with its offset in minutes from the origin; the first is fixed at 0 and each later offset must be greater than the one before; boarding and alighting allowed per stop. *(source: contracts/satellite/transport.yaml#/components/schemas/RouteStopInput / screens/P08-venue-back-office.yaml#BO-1183)*
- **pairedRouteId**: Optional picker of the route that runs the same line the other way; labelled "Return route". *(source: contracts/satellite/transport.yaml#createTransportRoute)*
- **bookingCutoffMinutes**: Minutes before departure that online sale stops, 0 to 1440, default 5. *(source: contracts/satellite/transport.yaml#createTransportRoute)*

#### Outputs: what the screen shows and produces

**Shown**

**Every route at this venue** (data table, from `listTransportRoutes`): A draft route shows what it still needs before it can go live (a fare table, two stops).

| Shows | Format | Notes |
|---|---|---|
| Code | text | The line and direction, e.g. `E101-Out`. |
| Line code | text | The public line number shared by both directions, e.g. `E101`. |
| Name | in the reader's language | — |
| Colour | text | — |
| Status | chip: Draft, Active, Suspended, Retired | — |
| Paired route | the name it points at, never the id | The same line run the other way. The swap button lands on it. |
| Total minutes | 1,234 | The last stop's offset. |
| Booking cutoff minutes | 1,234 | How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's "Boarding closes five … |

**The selected route and its stops** (detail panel, from `getTransportRoute`): **Stops in order with their offset in minutes from the first**, which starts at 0 and strictly increases; arrival time and duration on a departure card are the difference of two offsets.

| Shows | Format | Notes |
|---|---|---|
| Code | text | The line and direction, e.g. `E101-Out`. |
| Line code | text | The public line number shared by both directions, e.g. `E101`. |
| Name | in the reader's language | — |
| Status | chip: Draft, Active, Suspended, Retired | — |
| Paired route | the name it points at, never the id | The same line run the other way. The swap button lands on it. |
| Booking cutoff minutes | 1,234 | How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's "Boarding closes five … |
| Stops | list or chips (count when long) | — |
| Total minutes | 1,234 | The last stop's offset. |
| Catalogue event | the name it points at, never the id | The catalogue event its departures are performances of. Created with the route. |
| Catalogue product | the name it points at, never the id | The one-way trip product (kind `timedAdmission`); one variant per passenger type. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What activating the route changes (publish gate) | navigation or local | — | — | — | — |
| New route (primary button) | `createTransportRoute` POST `/transport/routes` | CreateTransportRouteRequest | TransportRoute | 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 Fewer than two stops, a … | opens modal first |
| Save route (secondary button) | `updateTransportRoute` PATCH `/transport/routes/{routeId}` | inline | TransportRoute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Stops changed while a published timetable covers a future date.; 422 Invalid stops, as on … | — |
| Activate, suspend or reactivate (secondary button) | `setTransportRouteStatus` PUT `/transport/routes/{routeId}/status` | inline | TransportRoute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current status, the route has no fare table, or retiring a route with … | opens confirmDialog first |
| Retire route (destructive button) | `setTransportRouteStatus` PUT `/transport/routes/{routeId}/status` | inline | TransportRoute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current status, the route has no fare table, or retiring a route with … | opens confirmDialog first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **readiness per route**: Three checks on each row, Fare table, Published timetable, Active, so a draft explains why it is not on sale. *(source: screens/P08-venue-back-office.yaml#BO-1184 / REV3-21)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Suspend**: Stops new sales and keeps sold tickets valid; the confirmation says so and a reason is required (PR-6). *(source: contracts/satellite/transport.yaml#setTransportRouteStatus)*

**Data it reads**: `listTransportRoutes` (onLoad, The venue's routes, by status and station); `listTransportStations` (onLoad, Stations to build stops from)

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-1183` Transport Stations: *Stations*; carries `stationId`
- → `BO-1185` Transport Fares & Passenger Types: *Fares and passenger types*; carries `routeId`
- → `BO-1186` Transport Timetables: *Timetables*; carries `routeId`
- → `BO-1187` Transport Departure Board: *Departure board*; carries `routeId`
- → `BO-1188` Transport Pass Types: *Pass types*
- → `BO-1189` Transport Network Import: *Import stations, routes and timetables*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's routes, read by `listTransportRoutes`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the routes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No routes yet.** Offers New route (needs at least two stations, BO-1183) and Import stations, routes and timetables (BO-1189). |
| Empty, no results (`?state=emptyNoResults`) | The status or station filter matched nothing and the routes are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_MANAGE`, which `createTransportRoute` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Validation (`?state=validation`) | `422` on fewer than two stops, a station repeated, a station inactive or not at this venue, or offsets that do not start at 0 and strictly increase, each marked on the stop row; `409` on a code already used; `409` on a stop change under a published timetable; `409` on a status change the route cannot make (no fare table, or retiring with sold seats), naming what is missing. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Stops changed while a published timetable covers a future date.; 409 The transition is not allowed from the current status, the route has no fare table, or retiring a route with sold seats on a departure … |

#### Edge cases to draw

- **Change the stops while a published timetable covers a future date**: Refused; withdraw the timetable first. Name, colour and cut-off can still change. *(source: contracts/satellite/transport.yaml#updateTransportRoute)*
- **Retire a route with sold departures on sale**: Refused; the dialog lists those departures and links to the departure board (BO-1187). *(source: contracts/satellite/transport.yaml#setTransportRouteStatus)*

#### Consistency with other screens

- Match `BO-1186`: Same route picker and route header (code, colour chip, status badge) on fares, timetables and passes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
routes:
- code: E101-Out
  lineCode: E101
  name: Dune Park Shuttle, Metro to Main Gate
  nameAr: حافلة دون بارك، المترو إلى البوابة الرئيسية
  colour: '#0D6EFD'
  stops:
  - Al Qudra Metro 0
  - Hotel District 12
  - Main Gate 25
  status: active
- code: E101-In
  pairedWith: E101-Out
  status: draft
  readiness:
    fareTable: false
    timetable: false
```

#### Permissions

- `listTransportRoutes` → no permission · guest, public, staff
- `getTransportRoute` → no permission · guest, public, staff
- `listTransportStations` → no permission · guest, public, staff
- `createTransportRoute` → `TRANSPORT_MANAGE` (configure) · staff
- `updateTransportRoute` → `TRANSPORT_MANAGE` (configure) · staff
- `setTransportRouteStatus` → `TRANSPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TRANSPORT_MANAGE`, which `createTransportRoute` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1184` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1184?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: What activating the route changes, New route, Save route, Activate, suspend or reactivate, Retire route.
- [ ] Every transition is wired: `BO-108`, `BO-1183`, `BO-1185`, `BO-1186`, `BO-1187`, `BO-1188`, `BO-1189`.
- [ ] Every gated control is gated: `TRANSPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1185` Transport Fares & Passenger Types

**Set a route's fares and the passenger types it sells, and preview what a trip costs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28069 (APP-SETUP-BO-1185) |
| Who uses it | venue staff holding `TRANSPORT_PRICE` (1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): one fare table per route, replaced as a whole — settings that take effect on sales from a date, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `routeId` (BO-1184) · cold entry: Opens on the route picker when no route is carried. |
| Route | `/transport/fares` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). **The fares are the venue's, set by a holder of `TRANSPORT_PRICE`**, a separate permission from the timetable because the person who edits a timetable is not the one who sets fares. A route has no fare table until one is set here, and cannot be activated without one. The prototype's values (base AED 5, AED 2.50 per stop; child and student half fare, person of determination free) are seed data for the demo tenant, not a default.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A route's fares and the passenger types it sells (adult, child, student, person of determination), and a preview of what a trip costs. Fares are set by a holder of TRANSPORT_PRICE, separately from the timetable, and apply from a date; sold tickets keep their price.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The preview calls quoteTransportFare, whose audience is guest, public and service, not staff. (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Route | select field | — | — | — | — | The route whose fare table is edited; path `routeId`. | — |
| Fare model | segmented control | optional | — | Stop count · Matrix | — | `stopCount` (a base fare plus a fare per stop travelled) or `matrix` (a fare per ordered station pair). A matrix must cover every pair the route serves (`422`, naming the missing pairs). | `FareTable.model` |
| Base fare | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21). | `FareTable.baseFare` |
| Fare per stop | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21). | `FareTable.perStopFare` |
| Applies to sales from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | A ticket already sold keeps its price. | `FareTable.effectiveFrom` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From station | picker: choose a from station | — | — | `listTransportRoutes` ?fromStationId |
| To station | picker: choose a to station | — | — | `listTransportRoutes` ?toStationId |
| Status | radio group | — | Draft · Active · Suspended · Retired | `listTransportRoutes` ?status |
| At | date and time picker | — | — | `getTransportFareTable` ?at |

**Form: Save fare table** (confirmDialog, opened by *Save fare table*; *Save fares* calls `setTransportFareTable`, *Cancel* sends nothing)

**Names the route and the date the new fares apply from**, and that tickets already sold keep their price. Lists passenger types added or removed, since each adds or retires a ticket variant.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Model `model` | segmented control | required | — | Stop count · Matrix | — | `stopCount`: base plus an amount per stop travelled — the prototype's rule. `matrix`: a fare for each pair of stops, for a network whose fares are zonal or negotiated. | `setTransportFareTable` body |
| Base fare `baseFare` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21). | `setTransportFareTable` body |
| Per stop fare `perStopFare` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21). | `setTransportFareTable` body |
| Matrix `matrix` | repeatable rows | optional | — | — | — | `matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row. | `setTransportFareTable` body |
| From station `matrix[].fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `setTransportFareTable` body |
| To station `matrix[].toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `setTransportFareTable` body |
| Fare `matrix[].fare` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setTransportFareTable` body |
| Passenger types `passengerTypes` | repeatable rows | required | — | at least 1; at most 10 | — | — | `setTransportFareTable` body |
| Code `passengerTypes[].code` | text field | required | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | `adult`, `child`, `student`, `determination`. Unique in the fare table. | `setTransportFareTable` body |
| Name `passengerTypes[].name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `setTransportFareTable` body |
| Description `passengerTypes[].description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | What the picker shows under the name ("Age 5–11 · half fare"). | `setTransportFareTable` body |
| Fare multiplier `passengerTypes[].fareMultiplier` | stepper or slider | required | — | min 0; max 1 | — | Share of the adult fare, set by the venue. The demo tenant's seed is 1 adult, 0.5 child and student, 0 person of determination (seed data, not a default). | `setTransportFareTable` body |
| Min age `passengerTypes[].minAge` | number field | optional | — | min 0 | — | — | `setTransportFareTable` body |
| Max age `passengerTypes[].maxAge` | number field | optional | — | min 0 | — | — | `setTransportFareTable` body |
| Proof required `passengerTypes[].proofRequired` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Checked by the driver at boarding ("Valid student card", "Sanad card"). | `setTransportFareTable` body |
| Is default `passengerTypes[].isDefault` | toggle | optional | off | — | — | The type a new search starts with, one of it. Exactly one per table. | `setTransportFareTable` body |
| Effective from `effectiveFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setTransportFareTable` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A `matrix` model missing a station pair the route serves, a passenger type code repeated, no passenger type with `isDefault`, or a multiplier outside 0 to 1.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **model**: Stop count (base fare plus per stop) or a matrix (one adult fare per ordered pair; the reverse pair is its own cell); the matrix shown as a triangle grid of stations. *(source: contracts/satellite/transport.yaml#setTransportFareTable)*
- **passengerTypes**: Code, name, picker description ("Age 5-11, half fare"), share of the adult fare 0 to 1, age limits, proof checked at boarding; exactly one default type. *(source: contracts/satellite/transport.yaml#/components/schemas/PassengerType)*
- **effectiveFrom**: Required; the confirmation names the route and the date and lists passenger types added or removed (each adds or retires a ticket type). *(source: contracts/satellite/transport.yaml#setTransportFareTable / screens/P08-venue-back-office.yaml#BO-1185)*

#### Outputs: what the screen shows and produces

**Shown**

**Fares by station pair** (data table, from `getTransportFareTable`): Shown for the `matrix` model only.

| Shows | Format | Notes |
|---|---|---|
| Model | chip: Stop count, Matrix | `stopCount`: base plus an amount per stop travelled — the prototype's rule. `matrix`: a fare for each pair of stops, for a network whose … |
| Base fare | AED 1,234.50 | `stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21). |
| Per stop fare | AED 1,234.50 | `stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21). |
| Matrix | list or chips (count when long) | `matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row. |
| From station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| To station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Fare | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Passenger types | list or chips (count when long) | — |
| Code | text | `adult`, `child`, `student`, `determination`. Unique in the fare table. |
| Name | in the reader's language | — |
| Description | in the reader's language | What the picker shows under the name ("Age 5–11 · half fare"). |
| Fare multiplier | 1,234.5 | Share of the adult fare, set by the venue. The demo tenant's seed is 1 adult, 0.5 child and student, 0 person of determination (seed data … |
| Min age | 1,234 | — |
| Max age | 1,234 | — |
| Proof required | in the reader's language | Checked by the driver at boarding ("Valid student card", "Sanad card"). |
| Is default | yes / no (icon or chip) | The type a new search starts with, one of it. Exactly one per table. |
| Catalogue variant | the name it points at, never the id | The variant of the route's trip product this type is sold as. |
| Effective from | 1 Oct 2026, 14:30 | — |
| ID | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Route | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |

**Passenger types** (data table, from `getTransportFareTable`): **Each type with its multiplier (0 to 1), age band and the proof the driver checks** (student card, Sanad card). Codes unique, exactly one default. Adding or removing a type adds or retires the matching variant on the route's catalogue product.

| Shows | Format | Notes |
|---|---|---|
| Model | chip: Stop count, Matrix | `stopCount`: base plus an amount per stop travelled — the prototype's rule. `matrix`: a fare for each pair of stops, for a network whose … |
| Base fare | AED 1,234.50 | `stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21). |
| Per stop fare | AED 1,234.50 | `stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21). |
| Matrix | list or chips (count when long) | `matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row. |
| From station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| To station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Fare | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Passenger types | list or chips (count when long) | — |
| Code | text | `adult`, `child`, `student`, `determination`. Unique in the fare table. |
| Name | in the reader's language | — |
| Description | in the reader's language | What the picker shows under the name ("Age 5–11 · half fare"). |
| Fare multiplier | 1,234.5 | Share of the adult fare, set by the venue. The demo tenant's seed is 1 adult, 0.5 child and student, 0 person of determination (seed data … |
| Min age | 1,234 | — |
| Max age | 1,234 | — |
| Proof required | in the reader's language | Checked by the driver at boarding ("Valid student card", "Sanad card"). |
| Is default | yes / no (icon or chip) | The type a new search starts with, one of it. Exactly one per table. |
| Catalogue variant | the name it points at, never the id | The variant of the route's trip product this type is sold as. |
| Effective from | 1 Oct 2026, 14:30 | — |
| ID | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Route | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |

**Fare preview** (detail panel, from `quoteTransportFare`): Pick two stations and a party; shows what the guest will pay, from the same pricing rule the cart uses. Previews the saved table; save first to preview a change.

| Shows | Format | Notes |
|---|---|---|
| Stops travelled | 1,234 | — |
| Adult fare | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Lines | list or chips (count when long) | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save fare table (primary button) | `setTransportFareTable` PUT `/transport/routes/{routeId}/fare-table` | SetFareTableRequest | FareTable | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A `matrix` model missing a station pair the route serves, a passenger type code repeated, no passenger type … | opens confirmDialog first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **preview**: From, to and party; shows stops travelled, adult fare, price per type and total. *(source: contracts/satellite/transport.yaml#quoteTransportFare)*

**Data it reads**: `listTransportRoutes` (onLoad, The route picker); `getTransportFareTable` (onLoad, The route's fare table and passenger types)

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*; carries `routeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The route's fare table, read by `getTransportFareTable`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fare table untouched. |
| Empty, no results (`?state=emptyNoResults`) | A route picked with no fare table opens the empty form, named as the first-run state for that route. |
| Empty, first run (`?state=emptyFirstRun`) | **This route has no fares yet, so it cannot be activated or sold.** The form opens empty with the fare models explained. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_PRICE`, which `setTransportFareTable` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Validation (`?state=validation`) | `422` on a matrix missing a station pair, a passenger type code repeated, no default type or a multiplier outside 0 to 1, each marked on its row. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A `matrix` model missing a station pair the route serves, a passenger type code repeated, no passenger type with `isDefault`, or a multiplier outside 0 to 1.; 422 Stations not on the route or in the wrong order, an unknown passenger type, no passengers, or a pass type not offered on this route. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fareTable:
  route: E101-Out
  model: stopCount
  baseFare: AED 5.00
  perStopFare: AED 2.50
  types:
  - code: adult
    share: 1
  - code: child
    share: 0.5
    proof: Age 5-11
  - code: determination
    share: 0
    proof: Sanad card
  effectiveFrom: '2026-11-01'
preview:
  from: Al Qudra Metro
  to: Main Gate
  party: 2 adults, 1 child
  total: AED 25.00
```

#### Permissions

- `listTransportRoutes` → no permission · guest, public, staff
- `getTransportFareTable` → no permission · guest, public, staff
- `setTransportFareTable` → `TRANSPORT_PRICE` (operate) · staff
- `quoteTransportFare` → no permission · guest, public, service

**A refused user sees:** Shown when the caller lacks `TRANSPORT_PRICE`, which `setTransportFareTable` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1185` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1185?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: Save fare table, Cancel.
- [ ] Every transition is wired: `BO-1184`.
- [ ] Every gated control is gated: `TRANSPORT_PRICE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1186` Transport Timetables

**Draft, publish and withdraw a route's timetables.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28070 (APP-SETUP-BO-1186) |
| Who uses it | venue staff holding `TRANSPORT_MANAGE`, `TRANSPORT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTransportTimetables` reads the route's timetables and the panel acts on one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `routeId` (BO-1184), `timetableId` (navigation) · cold entry: Opens on the route picker when no route is carried. |
| Route | `/transport/timetables` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). A timetable is departure times from the route's origin by day of week, valid over a date range. **Nothing is on sale until it is published**; publishing generates the departures up to the release horizon (proposed 30 days, client to correct) as catalogue performances, and a nightly job releases one more day. A published timetable is never edited: a new one drafted from a later date supersedes it from that date (states/transport-timetable.yaml).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A route's timetables: departure times from the origin by day of week, valid over dates, drafted then published. Publishing generates departures up to the release horizon (proposed 30 days) and a nightly job releases one more day; a published timetable is never edited, it is superseded by a new one from a later date.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the 30-day release horizon right for the client?** → Drawn default accepted: 30, editable per timetable. *(decided by Chinmay, 2026-10-02; DEC-107 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Route | select field | — | — | — | — | Path `routeId` of `listTransportTimetables`. | — |
| Status | select field | — | — | — | — | Sends `?status=`, draft, published, superseded or withdrawn. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From station | picker: choose a from station | — | — | `listTransportRoutes` ?fromStationId |
| To station | picker: choose a to station | — | — | `listTransportRoutes` ?toStationId |
| Status | radio group | — | Draft · Active · Suspended · Retired | `listTransportRoutes` ?status |
| Status | radio group | — | Draft · Published · Superseded · Withdrawn | `listTransportTimetables` ?status |

**Form: New timetable** (modal, opened by *New timetable*; *Create draft* calls `createTransportTimetable`, *Cancel* sends nothing)

**Collects what `createTransportTimetable` sends before it is called.** Required: `name`, `validFrom`, `seatCapacity`, `runs` (departure times from the origin by day of week). Optional: `validTo`, `releaseHorizonDays` (proposed 30), `seatMapId` for a coach with numbered seats. Created as a draft. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 120 | — | — | `createTransportTimetable` body |
| Valid from `validFrom` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createTransportTimetable` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createTransportTimetable` body |
| Release horizon days `releaseHorizonDays` | number field (days) | optional | 30 | min 1; max 365 | — | How many days ahead departures go on sale. Proposed default 30, from the prototype, client to correct (rev 3 REV3-21). | `createTransportTimetable` body |
| Seat capacity `seatCapacity` | number field | required | — | min 1; max 200 | — | Seats per departure, unless a departure overrides it. | `createTransportTimetable` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | The coach seat map for Seat Selection (`seating`). Null sells unallocated seats. | `createTransportTimetable` body |
| Runs `runs` | repeatable rows | required | — | at least 1; at most 500 | — | — | `createTransportTimetable` body |
| Departs at `runs[].departsAt` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, at the route's first stop. | `createTransportTimetable` body |
| Days `runs[].days` | multi-select chips | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun; at least 1; no duplicates | — | — | `createTransportTimetable` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Publish** (confirmDialog, opened by *Publish*; *Publish and put on sale* calls `publishTransportTimetable`, *Cancel* sends nothing)

Names the dates and the number of departures that go on sale, and the timetable it supersedes and from when.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not a draft, the route is not active or has no fare table, or a superseded timetable has departures with sold seats on or after this `validFrom`.

**Form: Withdraw** (confirmDialog, opened by *Withdraw*; *Withdraw timetable* calls `withdrawTransportTimetable`, *Keep it* sends nothing)

**Collects the `reason`** and names the unsold departures that are removed. Refused while a future departure has sold seats.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `withdrawTransportTimetable` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not published, or a future departure has sold seats.

**Sent by *Save draft*** (`updateTransportTimetable`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 120 | — | — | `updateTransportTimetable` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateTransportTimetable` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateTransportTimetable` body |
| Release horizon days `releaseHorizonDays` | number field (days) | optional | — | min 1; max 365 | — | — | `updateTransportTimetable` body |
| Seat capacity `seatCapacity` | number field | optional | — | min 1; max 200 | — | — | `updateTransportTimetable` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | — | `updateTransportTimetable` body |
| Runs `runs` | repeatable rows | optional | — | at least 1 | — | — | `updateTransportTimetable` body |
| Departs at `runs[].departsAt` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, at the route's first stop. | `updateTransportTimetable` body |
| Days `runs[].days` | multi-select chips | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun; at least 1; no duplicates | — | — | `updateTransportTimetable` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **runs**: A weekly grid (rows are times HH:MM, columns Mon to Sun) rather than a list; times in venue local time. *(source: contracts/satellite/transport.yaml#/components/schemas/TimetableRun)*
- **seat capacity and seat map**: Seats per departure 1 to 200; optional coach seat map for seat selection, empty sells unallocated seats. *(source: contracts/satellite/transport.yaml#createTransportTimetable)*

#### Outputs: what the screen shows and produces

**Shown**

**Every timetable on this route** (data table, from `listTransportTimetables`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Status | chip: Draft, Published, Superseded, Withdrawn | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Seat capacity | 1,234 | Seats per departure, unless a departure overrides it. |
| Published at | 1 Oct 2026, 14:30 | — |

**The selected timetable** (detail panel, from `listTransportTimetables`): `runs`: departure times by day of week, shown as a week grid.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Status | chip: Draft, Published, Superseded, Withdrawn | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Release horizon days | 1,234 | How many days ahead departures go on sale. Proposed default 30, from the prototype, client to correct (rev 3 REV3-21). |
| Seat capacity | 1,234 | Seats per departure, unless a departure overrides it. |
| Seat map | the name it points at, never the id | The coach seat map for Seat Selection (`seating`). Null sells unallocated seats. |
| Runs | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing puts on sale (publish gate) | navigation or local | — | — | — | — |
| New timetable (primary button) | `createTransportTimetable` POST `/transport/routes/{routeId}/timetables` | CreateTimetableRequest | Timetable | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save draft (secondary button) | `updateTransportTimetable` PATCH `/transport/timetables/{timetableId}` | inline | Timetable | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The timetable is not a draft. | — |
| Publish (secondary button) | `publishTransportTimetable` POST `/transport/timetables/{timetableId}/publish` | — | Timetable | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not a draft, the route is not active or has no fare table, or a superseded timetable has departures with sold … | opens confirmDialog first |
| Withdraw (destructive button) | `withdrawTransportTimetable` POST `/transport/timetables/{timetableId}/withdraw` | inline | Timetable | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not published, or a future departure has sold seats. | opens confirmDialog first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Publish**: Names the dates and number of departures going on sale and the timetable it supersedes from when. *(source: screens/P08-venue-back-office.yaml#BO-1186 / contracts/satellite/transport.yaml#publishTransportTimetable)*
- **Withdraw**: Reason required; removes unsold future departures; refused while any future departure has sold seats. *(source: contracts/satellite/transport.yaml#withdrawTransportTimetable)*

**Data it reads**: `listTransportRoutes` (onLoad, The route picker); `listTransportTimetables` (onLoad, The route's timetables, by status)

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*; carries `routeId`
- → `BO-1187` Transport Departure Board: *Departure board*; carries `routeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The route's timetables, read by `listTransportTimetables`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the timetables untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No timetable on this route, so nothing is on sale.** Offers New timetable and Import stations, routes and timetables (BO-1189). |
| Empty, no results (`?state=emptyNoResults`) | The status filter matched nothing and the route's other timetables are still there. Names the filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportTimetables` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TRANSPORT_MANAGE` for `createTransportTimetable`, `updateTransportTimetable`, `publishTransportTimetable`, `withdrawTransportTimetable`. |
| Validation (`?state=validation`) | `400` on a missing name, start date, capacity or run, or a run time out of order, marked on the field; `409` on editing a published timetable, on publishing against an inactive route or one with no fare table, and on withdrawing with sold seats, each naming the cause. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not a draft, the route is not active or has no fare table, or a superseded timetable has departures with sold seats on or after this `validFrom`.; 409 Not published, or a future departure has sold seats.; 409 The timetable is not a draft. |

#### Edge cases to draw

- **Edit a published timetable**: Not offered; "Draft a new timetable from" a later date instead. *(source: contracts/satellite/transport.yaml#updateTransportTimetable)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
timetable:
  name: Winter 2026-27
  validFrom: '2026-11-01'
  validTo: '2027-03-31'
  releaseHorizonDays: 30
  seatCapacity: 49
  runs:
  - at: 08:00
    days:
    - mon
    - tue
    - wed
    - thu
    - fri
    - sat
    - sun
  - at: 08:30
    days:
    - fri
    - sat
```

#### Permissions

- `listTransportRoutes` → no permission · guest, public, staff
- `listTransportTimetables` → `TRANSPORT_VIEW` (read) · staff
- `createTransportTimetable` → `TRANSPORT_MANAGE` (configure) · staff
- `updateTransportTimetable` → `TRANSPORT_MANAGE` (configure) · staff
- `publishTransportTimetable` → `TRANSPORT_MANAGE` (configure) · staff
- `withdrawTransportTimetable` → `TRANSPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportTimetables` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TRANSPORT_MANAGE` for `createTransportTimetable`, `updateTransportTimetable`, `publishTransportTimetable`, `withdrawTransportTimetable`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1186` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1186?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: What publishing puts on sale, New timetable, Save draft, Publish, Withdraw.
- [ ] Every transition is wired: `BO-1184`, `BO-1187`.
- [ ] Every gated control is gated: `TRANSPORT_MANAGE`, `TRANSPORT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1187` Transport Departure Board

**See every departure on a route with seats sold, change a run's coach or capacity, and cancel a run.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 2 · needs the `transport` module |
| Block | Block A · ticket #28071 (APP-SETUP-BO-1187) |
| Who uses it | venue staff holding `PERFORMANCE_CONFIGURE`, `TRANSPORT_MANAGE`, `TRANSPORT_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTransportRouteDepartures` reads the population and the panel acts on one departure — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `routeId` (BO-1184), `departureId` (navigation), `performanceId` (navigation) · cold entry: Opens on the route picker when no route is carried. |
| Route | `/transport/departures` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Every departure the published timetables generated, in every status, with seats sold and the vehicle. A bigger or smaller coach on one run is changed here; **a departure is cancelled through its catalogue performance** (`cancelPerformance`), so every guest affected is refunded and told through the ordinary performance-cancelled path (states/transport-departure.yaml).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every departure on a route with seats sold; change a run's coach or capacity; cancel a run.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Route | select field | — | — | — | — | Path `routeId` of `listTransportRouteDepartures`. | — |
| From and to | date picker | — | — | — | — | Sends `?from=` and `?to=`; defaults to today and the next seven days. | — |
| Status | select field | — | — | — | — | Sends `?status=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From station | picker: choose a from station | — | — | `listTransportRoutes` ?fromStationId |
| To station | picker: choose a to station | — | — | `listTransportRoutes` ?toStationId |
| Status | radio group | — | Draft · Active · Suspended · Retired | `listTransportRoutes` ?status |
| From | date picker | — | — | `listTransportRouteDepartures` ?from |
| To | date picker | — | — | `listTransportRouteDepartures` ?to |
| Status | radio group | — | Scheduled · On sale · Sold out · Departed · Cancelled | `listTransportRouteDepartures` ?status |

**Form: Save departure** (modal, opened by *Save departure*; *Save departure* calls `updateTransportDeparture`, *Cancel* sends nothing)

**Collects what `updateTransportDeparture` sends before it is called.** Optional: `seatCapacity` (not below seats sold), `vehicleResourceId`, `note`. The new capacity is written to the performance's channel capacity. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Seat capacity `seatCapacity` | number field | optional | — | min 1; max 200 | — | — | `updateTransportDeparture` body |
| Vehicle resource `vehicleResourceId` | picker: choose a vehicle resource | optional | — | — | shows names, sends the id | — | `updateTransportDeparture` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `updateTransportDeparture` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Capacity below seats sold.

**Form: Cancel departure** (confirmDialog, opened by *Cancel departure*; *Cancel departure* calls `cancelPerformance`, *Keep it* sends nothing)

**Names the departure and the passengers affected**, and that each is refunded and told. Collects what `cancelPerformance` needs: a `reason`, an optional guest message, and a supervisor PIN for a real run (audit R144).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `cancelPerformance` body |
| Guest message `guestMessage` | key and value settings | optional | — | — | — | — | `cancelPerformance` body |
| Refund percentage `refundPercentage` | stepper or slider | optional | 100 | min 0; max 100 | — | — | `cancelPerformance` body |
| Offer alternative performance `offerAlternativePerformanceId` | picker: choose an offer alternative performance | optional | — | — | shows names, sends the id | — | `cancelPerformance` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `cancelPerformance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | Required unless `dryRun` (audit R144, proposed by the coordinator). | `cancelPerformance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `cancelPerformance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `cancelPerformance` body |

Errors to draw in the form: 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. `states/performance.yaml` cancels only from `scheduled`, `onSale` and `suspended`.

#### Outputs: what the screen shows and produces

**Shown**

**Every departure in the range** (data table, from `listTransportRouteDepartures`)

| Shows | Format | Notes |
|---|---|---|
| Service date | 1 Oct 2026 | — |
| Departs at | 1 Oct 2026, 14:30 | At the route's first stop. |
| Status | chip: Scheduled, On sale, Sold out, Departed, Cancelled | Mirrors the catalogue performance behind the departure, in the words a coach operator uses. |
| Seat capacity | 1,234 | — |
| Seats sold | 1,234 | From catalogue availability on read; not stored here. |
| Vehicle resource | the name it points at, never the id | — |
| Timetable | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Note | text | — |

**The selected departure** (detail panel, from `listTransportRouteDepartures`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Service date | 1 Oct 2026 | — |
| Departs at | 1 Oct 2026, 14:30 | At the route's first stop. |
| Status | chip: Scheduled, On sale, Sold out, Departed, Cancelled | Mirrors the catalogue performance behind the departure, in the words a coach operator uses. |
| Seat capacity | 1,234 | — |
| Seats sold | 1,234 | From catalogue availability on read; not stored here. |
| Vehicle resource | the name it points at, never the id | — |
| Performance | the name it points at, never the id | The catalogue performance this departure is sold as. Cart lines carry it. |
| Note | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save departure (primary button) | `updateTransportDeparture` PATCH `/transport/departures/{departureId}` | inline | Departure | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Capacity below seats sold. | opens modal first |
| Cancel departure (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …); opens confirmDialog first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Change capacity**: Refused below seats sold. *(source: contracts/satellite/transport.yaml#updateTransportDeparture)*
- **Cancel run**: Stops sales, notifies holders and queues a bulk refund for approval. *(source: contracts/spine/catalogue.yaml#cancelPerformance)*

**Data it reads**: `listTransportRoutes` (onLoad, The route picker); `listTransportRouteDepartures` (onLoad, Every departure on the route with seats sold)

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*; carries `routeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The route's departures, read by `listTransportRouteDepartures`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the departures untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No departures on this route**, because no timetable is published. Offers Timetables (BO-1186). |
| Empty, no results (`?state=emptyNoResults`) | The date range or status matched nothing and the route's other departures are still there. Names the filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportRouteDepartures` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERFORMANCE_CONFIGURE` for `cancelPerformance`; `TRANSPORT_MANAGE` for `updateTransportDeparture`. |
| Validation (`?state=validation`) | `422` on a capacity below the seats sold, naming the count; a cancellation follows the performance cancel rules (reason required, supervisor step-up for a real run). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The performance is `cancelled`, `completed` or `soldOut`. `states/performance.yaml` cancels only from `scheduled`, `onSale` and `suspended`.; 422 Capacity below seats sold. |

#### Consistency with other screens

- Match `BO-1184`: Retiring a route sends the user here to cancel sold departures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
departures:
- route: E101-Out
  at: Sat 22 Nov 08:00
  sold: 41
  capacity: 49
  coach: Coach 7
```

#### Permissions

- `listTransportRoutes` → no permission · guest, public, staff
- `listTransportRouteDepartures` → `TRANSPORT_VIEW` (read) · staff
- `updateTransportDeparture` → `TRANSPORT_MANAGE` (configure) · staff
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin

**A refused user sees:** Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportRouteDepartures` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERFORMANCE_CONFIGURE` for `cancelPerformance`; `TRANSPORT_MANAGE` for `updateTransportDeparture`.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.16 | System shall identify affected tickets, reservations, memberships, events and integrations before applying product changes. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1187` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1187?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: Save departure, Cancel departure.
- [ ] Every transition is wired: `BO-1184`.
- [ ] Every gated control is gated: `PERFORMANCE_CONFIGURE`, `TRANSPORT_MANAGE`, `TRANSPORT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1188` Transport Pass Types

**Create, edit, stop and resume selling a venue's transport passes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28072 (APP-SETUP-BO-1188) |
| Who uses it | venue staff holding `TRANSPORT_PRICE`, `TRANSPORT_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTransportPassTypes` reads the population and the panel acts on one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `passTypeId` (navigation) · cold entry: Resolves the venue from the session; a cold arrival is the ordinary case. |
| Route | `/transport/pass-types` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Multi-trip carnets and unlimited passes. **Creating a pass type creates its catalogue product** (open-dated, with entries allowed equal to the trips, or unlimited), so a pass sells through the ordinary cart and each boarding consumes an entry at the driver's scan. A pass already sold keeps its trips, validity and price. The prototype's four (5-trip, 10-trip, weekly and monthly unlimited) are seed data for the demo tenant, not a default.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Multi-trip and unlimited transport passes. Creating a pass type creates its catalogue product (open-dated, entries equal to trips), so a pass sells through the ordinary basket and each boarding consumes an entry. The price is a multiple of the single adult fare, and the saving is measured against a stated number of trips.

#### Inputs: what the user enters or picks

**Form: New pass type** (modal, opened by *New pass type*; *Create pass type* calls `createTransportPassType`, *Cancel* sends nothing)

**Collects what `createTransportPassType` sends before it is called.** Required: `code`, `name`, `kind` (multi-trip or unlimited), `fareMultiplier` (the price as a multiple of the single adult fare), `referenceTrips` (what the saving is compared with), `validityDays`. Optional: `trips` (multi-trip only), `description`, `routeIds` (empty means every route), `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createTransportPassType` body |
| Code `code` | text field | required | — | max length 32 | — | — | `createTransportPassType` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createTransportPassType` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createTransportPassType` body |
| Kind `kind` | segmented control | required | — | Multi trip · Unlimited | — | — | `createTransportPassType` body |
| Trips `trips` | stepper or slider | optional | — | min 2; max 100 | — | Journeys included. Required for `multiTrip`; null for `unlimited`. | `createTransportPassType` body |
| Fare multiplier `fareMultiplier` | number field | required | — | min 0; max 1000 | — | The pass price as a multiple of the single adult fare between its two stations. | `createTransportPassType` body |
| Reference trips `referenceTrips` | number field | required | — | min 1; max 1000 | — | The single trips the saving is measured against — `trips` for a multi-trip card, an number the venue sets for unlimited (14 a week, 60 a month in the demo seed data). | `createTransportPassType` body |
| Validity days `validityDays` | number field (days) | required | — | min 1; max 366 | — | — | `createTransportPassType` body |
| Routes `routeIds` | multi-picker: choose routes | optional | — | — | — | Routes it is sold on. Empty means every active route in the venue. | `createTransportPassType` body |
| Sort order `sortOrder` | number field | optional | 0 | min 0 | — | — | `createTransportPassType` body |

Errors to draw in the form: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Sent by *Save pass type*** (`updateTransportPassType`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateTransportPassType` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateTransportPassType` body |
| Fare multiplier `fareMultiplier` | number field | optional | — | min 0; max 1000 | — | — | `updateTransportPassType` body |
| Reference trips `referenceTrips` | number field | optional | — | min 1; max 1000 | — | — | `updateTransportPassType` body |
| Validity days `validityDays` | number field (days) | optional | — | min 1; max 366 | — | — | `updateTransportPassType` body |
| Routes `routeIds` | multi-picker: choose routes | optional | — | — | — | — | `updateTransportPassType` body |
| Sort order `sortOrder` | number field | optional | — | min 0 | — | — | `updateTransportPassType` body |
| Active `active` | toggle | optional | — | — | — | — | `updateTransportPassType` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kind, trips and referenceTrips**: Multi-trip needs trips (2 to 100); unlimited needs referenceTrips (the trips a week or month the saving is compared with). *(source: contracts/satellite/transport.yaml#createTransportPassType)*
- **fareMultiplier**: Shown with the resulting price and saving for a sample journey ("10 trips at 8x the adult fare: AED 120.00, save AED 30.00"). *(source: contracts/satellite/transport.yaml#createTransportPassType)*
- **routeIds**: Empty means every active route; say so. *(source: contracts/satellite/transport.yaml#createTransportPassType)*

#### Outputs: what the screen shows and produces

**Shown**

**Every pass type at this venue** (data table, from `listTransportPassTypes`): Shows each pass's saving against single fares (fare multiplier against reference trips).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Kind | chip: Multi trip, Unlimited | — |
| Trips | 1,234 | Journeys included. Required for `multiTrip`; null for `unlimited`. |
| Fare multiplier | 1,234.5 | The pass price as a multiple of the single adult fare between its two stations. |
| Reference trips | 1,234 | The single trips the saving is measured against — `trips` for a multi-trip card, an number the venue sets for unlimited (14 a week, 60 a … |

**The selected pass type** (detail panel, from `listTransportPassTypes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Description | in the reader's language | — |
| Kind | chip: Multi trip, Unlimited | — |
| Trips | 1,234 | Journeys included. Required for `multiTrip`; null for `unlimited`. |
| Fare multiplier | 1,234.5 | The pass price as a multiple of the single adult fare between its two stations. |
| Reference trips | 1,234 | The single trips the saving is measured against — `trips` for a multi-trip card, an number the venue sets for unlimited (14 a week, 60 a … |
| Validity days | 1,234 | — |
| Routes | list or chips (count when long) | Routes it is sold on. Empty means every active route in the venue. |
| Sort order | 1,234 | — |
| Active | yes / no (icon or chip) | — |
| Catalogue product | the name it points at, never the id | The catalogue `openDated` product this pass is sold as. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New pass type (primary button) | `createTransportPassType` POST `/transport/pass-types` | CreatePassTypeRequest | PassType | 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Save pass type (secondary button) | `updateTransportPassType` PATCH `/transport/pass-types/{passTypeId}` | inline | PassType | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Resume selling (secondary button) | `updateTransportPassType` PATCH `/transport/pass-types/{passTypeId}` | inline | PassType | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Stop selling (destructive button) | `updateTransportPassType` PATCH `/transport/pass-types/{passTypeId}` | inline | PassType | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listTransportPassTypes` (onLoad, The venue's pass types)

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*; carries `routeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's pass types, read by `listTransportPassTypes`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pass types untouched. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTransportPassTypes` takes no filter beyond the venue, so an empty list is the first-run state. |
| Empty, first run (`?state=emptyFirstRun`) | **No passes on sale.** Guests can buy one-way trips only. Offers New pass type. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportPassTypes` requires; creating and editing need `TRANSPORT_PRICE`, named on the disabled buttons. |
| Validation (`?state=validation`) | `400` on a missing field, a multi-trip pass with no trip count or an unlimited one with one, marked on the field; `409` on a code already used at this venue. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Edge cases to draw

- **Change a pass type that has sold**: Applies to passes sold after it; sold passes keep trips, validity and price. *(source: contracts/satellite/transport.yaml#updateTransportPassType)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
passTypes:
- code: CARNET10
  name: 10-trip card
  nameAr: بطاقة 10 رحلات
  kind: multiTrip
  trips: 10
  fareMultiplier: 8
  validityDays: 60
- code: WEEK-UNL
  name: 7-day unlimited
  kind: unlimited
  referenceTrips: 14
  fareMultiplier: 10
  validityDays: 7
```

#### Permissions

- `listTransportPassTypes` → `TRANSPORT_VIEW` (read) · staff
- `createTransportPassType` → `TRANSPORT_PRICE` (operate) · staff
- `updateTransportPassType` → `TRANSPORT_PRICE` (operate) · staff
- `listTransportRoutes` → no permission · guest, public, staff

**A refused user sees:** Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportPassTypes` requires; creating and editing need `TRANSPORT_PRICE`, named on the disabled buttons.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1188` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1188?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: New pass type, Save pass type, Resume selling, Stop selling.
- [ ] Every transition is wired: `BO-1184`.
- [ ] Every gated control is gated: `TRANSPORT_PRICE`, `TRANSPORT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1189` Transport Network Import

**Upload a file of stations, routes and timetables, review what it would change and every finding, and apply it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · ticket #28073 (APP-SETUP-BO-1189) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `TRANSPORT_MANAGE`, `TRANSPORT_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): an upload, a preview and one apply — a staged change to the network, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `importId` (deepLink), `uploadId` (navigation) · cold entry: **A link to an import opened cold shows where it stands**: still validating, ready for review, failed, applied, or expired and needing a new upload. |
| Route | `/transport/import` |

**What the spec says about it.** **Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). **Bulk entry for an operator with more than a handful of stations to type**, on the venue-map pattern: upload, validate, review the preview and the findings, then a person applies. **Nothing is written until the preview is applied, and applying never puts anything on sale**: routes arrive as drafts, still need a fare table and activation, and timetables still need publishing. An active route's stops are never changed by an import.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Bulk entry of a venue's network (stations, routes with stops, timetables) from a CSV bundle or a GTFS feed: upload, validate, review the preview and every finding, then a person applies. Nothing goes on sale on apply: routes arrive as drafts and timetables unpublished.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Network file | file upload | — | — | — | — | Uploaded to the asset library first (`createUpload`, then `completeUpload`); the import takes its asset id. `csvBundle` is a zip of four CSV files (stations, routes, route stops, timetables), header … | — |
| Format | select field | — | — | — | — | `csvBundle` or `gtfs`. Required. | — |
| Read | multi select | — | — | — | — | `include`: stations, routes, timetables. Absent reads all three. | — |

**Form: Apply** (confirmDialog, opened by *Apply*; *Apply to the network* calls `applyTransportNetworkImport`, *Cancel* sends nothing)

**Names what is created and what is updated**, and that routes arrive as drafts and timetables unpublished: nothing goes on sale until a route is activated with a fare table and its timetable is published.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not `previewReady`, has error findings, or the network changed since validation.

**Sent by *Validate file*** (`importTransportNetwork`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | segmented control | required | — | Csv bundle · Gtfs | — | A zip of the four CSV files described on `importTransportNetwork`, or a GTFS static feed. | `importTransportNetwork` body |
| Source ref `sourceRef` | picker: choose a source ref | required | — | — | shows names, sends the id | The uploaded file, as the `MediaAsset.id` from `assets.completeUpload`. Never a URL. | `importTransportNetwork` body |
| Include `include` | multi-select chips | optional | — | Stations · Routes · Timetables; no duplicates | — | Which parts of the file to read. Absent reads all three. | `importTransportNetwork` body |

#### Outputs: what the screen shows and produces

**Shown**

**Validating** (progress indicator, from `getTransportNetworkImport`): Polled while the status is `validating`; the operator may leave and come back.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Venue | the name it points at, never the id | — |
| Format | chip: Csv bundle, Gtfs | — |
| Source ref | the name it points at, never the id | — |
| Status | chip: Validating, Preview ready, Failed, Applied, Expired | `validating` → `previewReady` or `failed`; `previewReady` → `applied`, or `expired` after 7 days unapplied (proposed, client to correct). |
| Preview | grouped details | What applying would write. Null until `previewReady`. |
| Stations to create | 1,234 | — |
| Stations to update | 1,234 | — |
| Routes to create | 1,234 | — |
| Routes to update | 1,234 | — |
| Stops to write | 1,234 | — |
| Timetables to create | 1,234 | — |
| Findings | list or chips (count when long) | — |
| Code | chip: Nothing found, File missing, Header mismatch, Station code duplicate, Station … | `stationCoordinatesMissing` is a warning (the station is listed and left off the map); `routeActiveStopsChanged` is a warning (those stops … |
| Severity | chip: Error, Warning | — |
| File | text | e.g. `route_stops.csv` or `stop_times.txt`. |
| Row | 1,234 | — |
| Reference | text | The station |
| Message | text | — |
| Created by | the name it points at, never the id | — |

**What the file would change** (detail panel, from `getTransportNetworkImport`): **The preview lists stations, routes, stops and timetables to create and to update; the findings list each problem with its file, row and severity.** An error finding blocks Apply; a warning (such as `routeActiveStopsChanged`, whose stops the apply skips) is shown and does not.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Validating, Preview ready, Failed, Applied, Expired | `validating` → `previewReady` or `failed`; `previewReady` → `applied`, or `expired` after 7 days unapplied (proposed, client to correct). |
| Preview | grouped details | What applying would write. Null until `previewReady`. |
| Findings | list or chips (count when long) | — |
| Created by | the name it points at, never the id | — |
| Created at | 1 Oct 2026, 14:30 | — |
| Applied by | the name it points at, never the id | — |
| Applied at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Validate file (primary button) | `importTransportNetwork` POST `/transport/network-imports` | ImportTransportNetworkRequest | TransportNetworkImport | 400 Validation failed; 422 The asset is not ready, not in this venue, or not a zip. | — |
| Apply (secondary button) | `applyTransportNetworkImport` POST `/transport/network-imports/{importId}/apply` | — | TransportNetworkImport | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not `previewReady`, has error findings, or the network changed since validation. | opens confirmDialog first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **preview**: Counts to create and update per kind (stations, routes, stops, timetables) and findings with row and file, filterable by severity. *(source: contracts/satellite/transport.yaml#getTransportNetworkImport)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Apply**: One transaction; the confirmation repeats that nothing goes on sale until each route is activated with a fare table and a published timetable. *(source: contracts/satellite/transport.yaml#applyTransportNetworkImport)*

**Where the user goes next**

- → `BO-1184` Transport Routes & Stops: *Routes and stops*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The import, read by `getTransportNetworkImport`. |
| Error (`?state=error`) | Could not load. Names which read failed; nothing has been written to the network. |
| Empty, first run (`?state=emptyFirstRun`) | No import in progress. The form opens empty, with the two file formats explained and a template to download. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TRANSPORT_MANAGE`, which `importTransportNetwork` requires, and names that permission. |
| Validation (`?state=validation`) | `422` on a file that is not ready, not at this venue or not a zip; a `failed` import names why; error findings block Apply row by row; `409` on Apply when the network changed since validation. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 400 Validation failed; 409 Not `previewReady`, has error findings, or the network changed since validation.; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the … |

#### Edge cases to draw

- **Import link opened later**: Shows where it stands (validating, ready for review, failed, applied, expired needing a new upload). *(source: screens/P08-venue-back-office.yaml#BO-1189)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
import:
  file: dune-shuttle-network.zip
  format: csvBundle
  status: previewReady
  create:
    stations: 6
    routes: 4
    timetables: 4
  update:
    stations: 1
  findings:
    errors: 0
    warnings: 2
```

#### Permissions

- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `importTransportNetwork` → `TRANSPORT_MANAGE` (configure) · staff
- `getTransportNetworkImport` → `TRANSPORT_VIEW` (read) · staff
- `applyTransportNetworkImport` → `TRANSPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TRANSPORT_MANAGE`, which `importTransportNetwork` requires, and names that permission.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1189` · status **notStarted** · provenance generated
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1189?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: Validate file, Apply, Cancel.
- [ ] Every transition is wired: `BO-1184`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `TRANSPORT_MANAGE`, `TRANSPORT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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
"applyTransportNetworkImport": {"method":"POST","path":"/transport/network-imports/{importId}/apply","contract":"transport","summary":"Apply a previewed import to the network","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TransportNetworkImport"},
"cancelPerformance": {"method":"POST","path":"/performances/{performanceId}/cancel","contract":"catalogue","summary":"Cancel a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceCancellationResult"},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createTransportPassType": {"method":"POST","path":"/transport/pass-types","contract":"transport","summary":"Define a multi-trip or unlimited pass","permission":"TRANSPORT_PRICE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePassTypeRequest","responds":"PassType"},
"createTransportRoute": {"method":"POST","path":"/transport/routes","contract":"transport","summary":"Define a route with its ordered stops","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTransportRouteRequest","responds":"TransportRoute"},
"createTransportStation": {"method":"POST","path":"/transport/stations","contract":"transport","summary":"Add a station","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStationRequest","responds":"Station"},
"createTransportTimetable": {"method":"POST","path":"/transport/routes/{routeId}/timetables","contract":"transport","summary":"Draft a timetable for a route","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTimetableRequest","responds":"Timetable"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"getTransportFareTable": {"method":"GET","path":"/transport/routes/{routeId}/fare-table","contract":"transport","summary":"A route's fares and passenger types","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":false}],"requestBody":null,"responds":"FareTable"},
"getTransportNetworkImport": {"method":"GET","path":"/transport/network-imports/{importId}","contract":"transport","summary":"An import's status, preview counts and findings","permission":"TRANSPORT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TransportNetworkImport"},
"getTransportRoute": {"method":"GET","path":"/transport/routes/{routeId}","contract":"transport","summary":"A route with its stops","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TransportRoute"},
"importTransportNetwork": {"method":"POST","path":"/transport/network-imports","contract":"transport","summary":"Read a network file into a preview","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ImportTransportNetworkRequest","responds":null},
"listTransportPassTypes": {"method":"GET","path":"/transport/pass-types","contract":"transport","summary":"The venue's multi-trip pass types","permission":"TRANSPORT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportRouteDepartures": {"method":"GET","path":"/transport/routes/{routeId}/departures","contract":"transport","summary":"A route's departures, for operations","permission":"TRANSPORT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportRoutes": {"method":"GET","path":"/transport/routes","contract":"transport","summary":"Routes, optionally those serving a pair of stations","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"fromStationId","in":"query","required":null},{"name":"toStationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportStations": {"method":"GET","path":"/transport/stations","contract":"transport","summary":"Stations of a venue's transport network","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportTimetables": {"method":"GET","path":"/transport/routes/{routeId}/timetables","contract":"transport","summary":"A route's timetables","permission":"TRANSPORT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishTransportTimetable": {"method":"POST","path":"/transport/timetables/{timetableId}/publish","contract":"transport","summary":"Publish a timetable and release its departures","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Timetable"},
"quoteTransportFare": {"method":"POST","path":"/transport/fare-quotes","contract":"transport","summary":"Price a one-way trip or a pass for a party","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":"FareQuoteRequest","responds":"FareQuote"},
"setTransportFareTable": {"method":"PUT","path":"/transport/routes/{routeId}/fare-table","contract":"transport","summary":"Set a route's fares and passenger types","permission":"TRANSPORT_PRICE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetFareTableRequest","responds":"FareTable"},
"setTransportRouteStatus": {"method":"PUT","path":"/transport/routes/{routeId}/status","contract":"transport","summary":"Activate, suspend or retire a route","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TransportRoute"},
"updateTransportDeparture": {"method":"PATCH","path":"/transport/departures/{departureId}","contract":"transport","summary":"Change a departure's coach or capacity","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Departure"},
"updateTransportPassType": {"method":"PATCH","path":"/transport/pass-types/{passTypeId}","contract":"transport","summary":"Amend or retire a pass type","permission":"TRANSPORT_PRICE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PassType"},
"updateTransportRoute": {"method":"PATCH","path":"/transport/routes/{routeId}","contract":"transport","summary":"Amend a route","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TransportRoute"},
"updateTransportStation": {"method":"PATCH","path":"/transport/stations/{stationId}","contract":"transport","summary":"Amend or deactivate a station","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Station"},
"updateTransportTimetable": {"method":"PATCH","path":"/transport/timetables/{timetableId}","contract":"transport","summary":"Amend a draft timetable","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Timetable"},
"withdrawTransportTimetable": {"method":"POST","path":"/transport/timetables/{timetableId}/withdraw","contract":"transport","summary":"Withdraw a published timetable","permission":"TRANSPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Timetable"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreatePassTypeRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","code","name","kind","fareMultiplier","referenceTrips","validityDays"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":32,"x-ticvai-unique":"venue"},"name":{"$ref":"#/components/schemas/transport::LocalisedText"},"description":{"$ref":"#/components/schemas/transport::LocalisedText"},"kind":{"type":"string","enum":["multiTrip","unlimited"]},"trips":{"type":"integer","minimum":2,"maximum":100,"nullable":true,"description":"Journeys included. Required for `multiTrip`; null for `unlimited`."},"fareMultiplier":{"type":"number","minimum":0,"maximum":1000,"description":"The pass price as a multiple of the single adult fare between its two stations."},"referenceTrips":{"type":"integer","minimum":1,"maximum":1000,"description":"The single trips the saving is measured against — `trips` for a multi-trip card, an number the venue sets for unlimited (14 a week, 60 a month in the demo seed data).\n"},"validityDays":{"type":"integer","minimum":1,"maximum":366},"routeIds":{"type":"array","description":"Routes it is sold on. Empty means every active route in the venue.","items":{"$ref":"../shared/common.yaml#/components/schemas/Id"}},"sortOrder":{"type":"integer","minimum":0,"default":0}}},
"CreateStationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","code","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"Short operator code, e.g. `SHJ-JUB`. Unique in the venue."},"name":{"$ref":"#/components/schemas/transport::LocalisedText"},"shortName":{"$ref":"#/components/schemas/transport::LocalisedText","description":"The label on the route diagram and the map pin (`Union Sq`, `MoE`)."},"latitude":{"type":"number","minimum":-90,"maximum":90,"nullable":true},"longitude":{"type":"number","minimum":-180,"maximum":180,"nullable":true}}},
"CreateTimetableRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","validFrom","seatCapacity","runs"],"properties":{"name":{"type":"string","maxLength":120},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"releaseHorizonDays":{"type":"integer","minimum":1,"maximum":365,"default":30,"description":"How many days ahead departures go on sale. Proposed default 30, from the prototype, client to correct (rev 3 REV3-21).\n"},"seatCapacity":{"type":"integer","minimum":1,"maximum":200,"description":"Seats per departure, unless a departure overrides it."},"seatMapId":{"type":"string","format":"uuid","nullable":true,"description":"The coach seat map for Seat Selection (`seating`). Null sells unallocated seats."},"runs":{"type":"array","minItems":1,"maxItems":500,"items":{"$ref":"#/components/schemas/TimetableRun"}}}},
"CreateTransportRouteRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","code","name","stops"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"The line and direction, e.g. `E101-Out`. Unique in the venue."},"lineCode":{"type":"string","maxLength":16,"description":"The public line number shared by both directions, e.g. `E101`."},"name":{"$ref":"#/components/schemas/transport::LocalisedText"},"colour":{"type":"string","pattern":"^#[0-9a-fA-F]{6}$"},"pairedRouteId":{"type":"string","format":"uuid","nullable":true,"description":"The same line run the other way. The swap button lands on it."},"bookingCutoffMinutes":{"type":"integer","minimum":0,"maximum":1440,"default":5,"description":"How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's \"Boarding closes five minutes before departure\", client to correct (rev 3 REV3-21).\n"},"stops":{"type":"array","minItems":2,"maxItems":100,"items":{"$ref":"#/components/schemas/RouteStopInput"}}}},
"Departure": {"x-ticvai-persistence":"transport.departure","type":"object","required":["id","routeId","timetableId","performanceId","serviceDate","departsAt","status","seatCapacity"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"timetableId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"performanceId":{"type":"string","format":"uuid","description":"The catalogue performance this departure is sold as. Cart lines carry it."},"serviceDate":{"type":"string","format":"date"},"departsAt":{"type":"string","format":"date-time","description":"At the route's first stop."},"status":{"$ref":"#/components/schemas/TransportDepartureStatus"},"seatCapacity":{"type":"integer","minimum":1},"seatsSold":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"From catalogue availability on read; not stored here."},"vehicleResourceId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true}}},
"FareModel": {"type":"string","description":"`stopCount`: base plus an amount per stop travelled — the prototype's rule. `matrix`: a fare for each pair of stops, for a network whose fares are zonal or negotiated. Which one a route uses is the venue's choice in `setTransportFareTable` (rev 3 REV3-21).\n","enum":["stopCount","matrix"]},
"FareQuote": {"x-ticvai-persistence":"none — computed","type":"object","required":["routeId","stopsTravelled","adultFare","total"],"properties":{"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"stopsTravelled":{"type":"integer","minimum":1},"adultFare":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["code","count","unitPrice","lineTotal"],"properties":{"code":{"type":"string"},"catalogueVariantId":{"type":"string","format":"uuid"},"count":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"passTypeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"saving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"With `passTypeId`, single adult fare × `referenceTrips` minus the pass price."},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FareQuoteRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["fromStationId","toStationId"],"properties":{"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id","description":"Omitted, the active route serving the two stations in this order."},"fromStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"toStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"passengers":{"type":"array","maxItems":10,"description":"Omitted, one of the default type. Ignored with `passTypeId`.","items":{"type":"object","required":["code","count"],"properties":{"code":{"type":"string"},"count":{"type":"integer","minimum":0,"maximum":99}}}},"passTypeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"travelAt":{"type":"string","format":"date-time","description":"**When the trip is travelled** (the departure's time; for a pass, its first valid day). The fare table in force at this instant prices the quote (CHG-RUL-012). Default `at`, else now.\n"},"at":{"type":"string","format":"date-time","deprecated":true,"description":"Deprecated on 3 October (CHG-RUL-012): quotes price at travel time, so send `travelAt`. Kept for clients built at r1; read as `travelAt` when `travelAt` is absent.\n"}}},
"FareTable": {"x-ticvai-persistence":"transport.fare_table + transport.fare_passenger_type + transport.fare_matrix_cell","allOf":[{"$ref":"#/components/schemas/SetFareTableRequest"},{"type":"object","required":["id","routeId"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the next version takes over; null when none is set (CHG-RUL-012). Versions of a route never overlap: one table is in force at any instant.\n"},"upcoming":{"type":"object","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The next version, set and not yet in force (CHG-RUL-012); null when none.","properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"effectiveFrom":{"type":"string","format":"date-time"}}}}}]},
"ImportTransportNetworkRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["format","sourceRef"],"properties":{"format":{"type":"string","enum":["csvBundle","gtfs"],"description":"A zip of the four CSV files described on `importTransportNetwork`, or a GTFS static feed."},"sourceRef":{"type":"string","format":"uuid","description":"The uploaded file, as the `MediaAsset.id` from `assets.completeUpload`. Never a URL.","x-ticvai-references":"assets.MediaAsset"},"include":{"type":"array","uniqueItems":true,"description":"Which parts of the file to read. Absent reads all three.","items":{"type":"string","enum":["stations","routes","timetables"]}}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/assets::MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/assets::LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/assets::LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/assets::LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PassType": {"x-ticvai-persistence":"transport.pass_type","allOf":[{"$ref":"#/components/schemas/CreatePassTypeRequest"},{"type":"object","required":["id","active"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"active":{"type":"boolean","default":true},"catalogueProductId":{"type":"string","format":"uuid","readOnly":true,"description":"The catalogue `openDated` product this pass is sold as."}}}]},
"PassengerType": {"x-ticvai-persistence":"transport.fare_passenger_type","type":"object","required":["code","name","fareMultiplier"],"properties":{"code":{"type":"string","pattern":"^[a-z][a-zA-Z0-9]{0,31}$","description":"`adult`, `child`, `student`, `determination`. Unique in the fare table."},"name":{"$ref":"#/components/schemas/transport::LocalisedText"},"description":{"$ref":"#/components/schemas/transport::LocalisedText","description":"What the picker shows under the name (\"Age 5–11 · half fare\")."},"fareMultiplier":{"type":"number","minimum":0,"maximum":1,"description":"Share of the adult fare, set by the venue. The demo tenant's seed is 1 adult, 0.5 child and student, 0 person of determination (seed data, not a default)."},"minAge":{"type":"integer","minimum":0,"nullable":true},"maxAge":{"type":"integer","minimum":0,"nullable":true},"proofRequired":{"$ref":"#/components/schemas/transport::LocalisedText","nullable":true,"description":"Checked by the driver at boarding (\"Valid student card\", \"Sanad card\")."},"isDefault":{"type":"boolean","default":false,"description":"The type a new search starts with, one of it. Exactly one per table."},"catalogueVariantId":{"type":"string","format":"uuid","readOnly":true,"description":"The variant of the route's trip product this type is sold as."}}},
"PerformanceCancellationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["performanceId","dryRun","affectedOrders","refundExposure"],"properties":{"performanceId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"affectedOrders":{"type":"integer"},"affectedGuests":{"type":"integer"},"refundExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"},"bulkRefundBatchId":{"type":"string","nullable":true,"description":"**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"},"notificationsQueued":{"type":"integer"}}},
"RouteStop": {"x-ticvai-persistence":"transport.route_stop","allOf":[{"$ref":"#/components/schemas/RouteStopInput"},{"type":"object","required":["id","sequence"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"sequence":{"type":"integer","minimum":1,"description":"1 for the origin."},"station":{"$ref":"#/components/schemas/Station"}}}]},
"RouteStopInput": {"x-ticvai-persistence":"none — request only","type":"object","required":["stationId","offsetMinutes"],"properties":{"stationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"offsetMinutes":{"type":"integer","minimum":0,"maximum":1440,"description":"Minutes after the departure from the first stop that the coach leaves this one. 0 on the first stop; strictly increasing along the route.\n"},"boardingAllowed":{"type":"boolean","default":true},"alightingAllowed":{"type":"boolean","default":true}}},
"SetFareTableRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["model","passengerTypes","effectiveFrom"],"properties":{"model":{"$ref":"#/components/schemas/FareModel"},"baseFare":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"`stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21)."},"perStopFare":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"`stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21)."},"matrix":{"type":"array","description":"`matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row.","items":{"type":"object","required":["fromStationId","toStationId","fare"],"properties":{"fromStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"toStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"fare":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"passengerTypes":{"type":"array","minItems":1,"maxItems":10,"items":{"$ref":"#/components/schemas/PassengerType"}},"effectiveFrom":{"type":"string","format":"date-time"}}},
"Station": {"x-ticvai-persistence":"transport.station","allOf":[{"$ref":"#/components/schemas/CreateStationRequest"},{"type":"object","required":["id","active"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"active":{"type":"boolean","default":true}}}]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"Timetable": {"x-ticvai-persistence":"transport.timetable + transport.timetable_run","allOf":[{"$ref":"#/components/schemas/CreateTimetableRequest"},{"type":"object","required":["id","routeId","status"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"status":{"$ref":"#/components/schemas/TransportTimetableStatus"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"releasedThrough":{"type":"string","format":"date","nullable":true,"readOnly":true,"description":"The last date whose departures have been generated."},"supersededById":{"type":"string","format":"uuid","nullable":true,"readOnly":true}}}]},
"TimetableRun": {"x-ticvai-persistence":"transport.timetable_run","type":"object","required":["departsAt","days"],"properties":{"departsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, at the route's first stop."},"days":{"type":"array","minItems":1,"uniqueItems":true,"items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]}}}},
"TransportDepartureStatus": {"type":"string","description":"Mirrors the catalogue performance behind the departure, in the words a coach operator uses. `soldOut` is computed from availability, never set.\n","enum":["scheduled","onSale","soldOut","departed","cancelled"]},
"TransportNetworkImport": {"x-ticvai-persistence":"transport.network_import","type":"object","required":["id","venueId","format","sourceRef","status"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"venueId":{"type":"string","format":"uuid","readOnly":true},"format":{"type":"string","enum":["csvBundle","gtfs"]},"sourceRef":{"type":"string","format":"uuid","x-ticvai-references":"assets.MediaAsset"},"status":{"$ref":"#/components/schemas/TransportNetworkImportStatus"},"preview":{"type":"object","nullable":true,"readOnly":true,"description":"What applying would write. Null until `previewReady`.","properties":{"stationsToCreate":{"type":"integer","minimum":0},"stationsToUpdate":{"type":"integer","minimum":0},"routesToCreate":{"type":"integer","minimum":0},"routesToUpdate":{"type":"integer","minimum":0},"stopsToWrite":{"type":"integer","minimum":0},"timetablesToCreate":{"type":"integer","minimum":0}}},"findings":{"type":"array","readOnly":true,"maxItems":1000,"items":{"$ref":"#/components/schemas/TransportNetworkImportFinding"}},"createdBy":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"appliedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"appliedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"TransportNetworkImportFinding": {"x-ticvai-persistence":"none — stored as jsonb on transport.network_import.findings","type":"object","required":["code","severity","message"],"properties":{"code":{"type":"string","enum":["nothingFound","fileMissing","headerMismatch","stationCodeDuplicate","stationCoordinatesMissing","routeCodeDuplicate","routeStopUnknownStation","routeOffsetsNotIncreasing","routePairUnknown","routeActiveStopsChanged","timetableRouteUnknown","timetableTimeInvalid","timetableDatesInvalid","gtfsCalendarUnsupported"],"description":"`stationCoordinatesMissing` is a warning (the station is listed and left off the map); `routeActiveStopsChanged` is a warning (those stops are skipped); every other code is an error and blocks the apply.\n"},"severity":{"type":"string","enum":["error","warning"]},"file":{"type":"string","nullable":true,"description":"e.g. `route_stops.csv` or `stop_times.txt`."},"row":{"type":"integer","minimum":1,"nullable":true},"reference":{"type":"string","nullable":true,"description":"The station","route or timetable code concerned.":null},"message":{"type":"string","maxLength":500}}},
"TransportNetworkImportStatus": {"type":"string","description":"`validating` → `previewReady` or `failed`; `previewReady` → `applied`, or `expired` after 7 days unapplied (proposed, client to correct). States in `states/transport-network-import.yaml` (rev 3 REV3-21).\n","enum":["validating","previewReady","failed","applied","expired"]},
"TransportRoute": {"x-ticvai-persistence":"transport.route + transport.route_stop","allOf":[{"$ref":"#/components/schemas/CreateTransportRouteRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"status":{"$ref":"#/components/schemas/TransportRouteStatus"},"stops":{"type":"array","items":{"$ref":"#/components/schemas/RouteStop"}},"totalMinutes":{"type":"integer","readOnly":true,"description":"The last stop's offset."},"catalogueEventId":{"type":"string","format":"uuid","readOnly":true,"description":"The catalogue event its departures are performances of. Created with the route."},"catalogueProductId":{"type":"string","format":"uuid","readOnly":true,"description":"The one-way trip product (kind `timedAdmission`); one variant per passenger type. Created with the route.\n"}}}]},
"TransportRouteStatus": {"type":"string","enum":["draft","active","suspended","retired"]},
"TransportTimetableStatus": {"type":"string","enum":["draft","published","superseded","withdrawn"]},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}}
}
```
