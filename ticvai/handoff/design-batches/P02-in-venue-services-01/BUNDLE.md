# P02-in-venue-services-01 — P02 · In-venue Services

**10 screens · 32 operations · 74 schemas · 7 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PARKING_CONFIGURE, PRODUCT_VIEW, QUEUE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **10 of these operations work offline**: createPayment, getOrder, getTenantAppStatus, getVenueMap, getVenueMapGraph, getWaitTimes, joinRestaurantWaitlist, listParkingFacilities
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `GST-021` | Interactive Map | A | 3 | 47 | 8 | 17 | 6 | 0 | guest | notStarted (client-verified) |
| `GST-022` | Attraction Wait Times | A | 0 | 10 | 4 | 4 | 5 | 6 | guest | notStarted (client-verified) |
| `GST-023` | Virtual Queue | A | 8 | 39 | 5 | 11 | 4 | 6 | guest | notStarted (client-verified) |
| `GST-024` | F&B – Browse & Order | A | 32 | 61 | 6 | 12 | 11 | 1 | guest | notStarted (client-verified) |
| `GST-025` | F&B – Order Tracking | A | 2 | 14 | 4 | 1 | 1 | 1 | guest | notStarted (client-verified) |
| `GST-027` | Parking – Reserve & Pay | A | 44 | 25 | 7 | 25 | 2 | 2 | guest | notStarted (client-verified) |
| `GST-028` | Parking – Reservation Confirmed | A | 1 | 27 | 6 | 7 | 1 | 2 | guest | notStarted (client-verified) |
| `GST-029` | Venue Info & Services | A | 2 | 40 | 5 | 0 | 0 | 0 | guest | notStarted (client-verified) |
| `GST-038` | At the Venue | A | 4 | 62 | 8 | 16 | 3 | 0 | guest | notStarted (client-verified) |
| `GST-070` | Reserve a Table | A | 44 | 0 | 6 | 17 | 7 | 1 | guest | notStarted (client-verified) |

## Thin screens in this batch

**GST-022, GST-025 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-021` Interactive Map

**See where things are in relation to each other.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `seating` module |
| Block | Block A · ticket #18148 (APP-MOB-GST-021) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest, venue manager |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the … |
| Opens with | `mapId` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/general/interactive-map` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired to the venue map 18 August (CF-123).** The whole map arrives in one call and the client filters locally — which is also what makes it work with no signal in the middle of a park. **Routing happens on the device.** The platform guarantees the graph — connected, versioned, with step-free marked — and the client walks it, because a phone with the graph cached routes with no signal and a server round-trip per step does not. **The version is how a stale route is caught**: a guest holding a route across a path that closed this morning gets told, rather than walking into a barrier. **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Mobile v4 (decided 29 September, MOB-1).** The **Map** view of GST-038 At the Venue: **one implementation with GST-038, the ids kept** (as GAP-D3). **3D navigation (client meeting 30 September, MoM 4.8): ADR-0069.** Where the venue map has a GLB model, this view renders it natively (react-three-fiber) and the walking-navigation mode follows the guest in 3D; the route still comes from `getVenueMapGraph`, snapped from live GPS, with no external mapping service. No model, a weak phone or …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, as on `getVenueMap`. | `getVenueMapGraph` ?draft |
| Step free only | toggle | off | — | `getVenueMapGraph` ?stepFreeOnly |

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**The selected product** (detail panel, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |

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

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Data it reads**: `listProducts` (onLoad, List products); `getWaitTimes` (onLoad, Wait times across a venue); `getVenueMap` (onLoad, A map with its points and paths); `getVenueMapGraph` (onLoad, The navigation graph, ready to route over)

**Where the user goes next**

- → `GST-022` Attraction Wait Times: *They compare waits across attractions*
- → `GST-001` Home: *Home – Default*
- → `BO-096` Resource Calendar: *The attendant checks what is free for the requested window*; calls `getVenueMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The interactive map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the interactive map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No interactive map yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the interactive map are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the guest to reconnect. |
| Map3d unavailable (`?state=map3dUnavailable`) | **No 3D model for this map: the 2D map, same route** (ADR-0069; client meeting 30 September, MoM 4.8). The venue has not published a GLB model for this map (the default for every venue until it supplies one), the phone fails the 3D capability check, or rendering drops below 20 fps. The 2D map shows the same route from `getVenueMapGraph` and the same live position dot; the 2D/3D toggle is hidden and nothing else is said: no message, no error. |
| Weak gps (`?state=weakGps`) | **Position approximate** (ADR-0069, section 4): reported GPS accuracy worse than 30 metres, or the route runs along an indoor path. The dot dims and an approximate-position ring is drawn round the last confident position, labelled *Position approximate*; the turn list and the remaining distance stay, and *I am at…* (tap a nearby location, or scan its QR sign) re-anchors. Routing does not stop, in 3D or in 2D. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public
- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getVenueMapGraph` → `VENUE_MAP_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 19.2.55 | Interactive Venue Map - System shall provide interactive venue maps. | Guest Mobile App & Branding | CONTRACTED | `getVenueMap` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In-park 3D navigation is built natively (React Three.js) from the venue's 3D GLB model plus a metadata file of pathways and locations, combined with the guest's live GPS position; no external mapping tool. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1103)*
- In-park navigation: a live map view lets a guest navigate to a selected point (e.g. the nearest food outlet), entering a walking-navigation mode that guides the guest in real time. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1102)*
- Item detail shows the item's location on the map and proposes the relevant product, e.g. restaurant -> "Buy meal combo", which automatically adds the required admission ticket (checkout in ~3 steps). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1019)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-021` · status **notStarted** · provenance client-verified · **Drawn by Claude Design on `Seat Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *At the venue → Nearest food → Start (walking navigation: the 3D map follows the route, turn-by-turn above it)*. Differences: The walking navigation follows the route in 3D, with turn-by-turn above the map and a live position (ADR-0069). The 2D/3D choice is a demo setting of the prototype (Config, Maps: 3D or 2D), not a switch the guest has, and neither the 3D-unavailable state (map3dUnavailable) nor the weak-GPS state (weakGps, "Position approximate") is drawn: both pending in design: specified, and built from the definition until the design shows it (handoff/design-batches/apps/1-guest-app/README.md).
- Derived from `wireframes/reference/Seat Board 4.dc.html`
- Client design-board frames: `Seat Board 4.dc.html#seat-4b`
- Flow F25 *A guest rents a cabana*, step 1: The guest finds cabanas on the venue map and taps one. → The map resolves the cabana zone to a bookable resource kind.
- Flow F26 *A venue maps its site*, step 7: A guest opens the map and is routed. → The whole map in one call, cached, and the graph small enough to route over on the device. **The platform guarantees the graph and the client walks it** — a phone with it cached routes with no signal.
- Flow F48 *A guest finds it, queues for it, and eats*, step 1: They open the map to see what is near. → **The map carries wait times, not just geometry.** A map that shows where things are and not how long they take sends a guest to the longest queue in the venue.
- Flow F25 branch at step 1 (recoverable): when The venue has no map, or the cabana is not placed on it., The guest browses resources as a list instead. **The map is how they find it, not how it works** — a venue without one still rents cabanas.
- Flow F26 branch at step 7 (recoverable): when A path closes after the guest cached the graph., `setPathClosure` bumps the graph version, and the client holding an older version knows its route may cross something closed. **A guest holding an offline route across a path that closed this morning …
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, map3dUnavailable, weakGps.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-022`, `GST-001`, `BO-096`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-022` Attraction Wait Times

**See attraction wait times for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `queue` module |
| Block | Block A · ticket #18149 (APP-MOB-GST-022) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getWaitTimes` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the … |
| Opens with | nothing: it opens on its own |
| Route | `/general/attraction-wait-times` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101) with the queue platform F21 runs on. **Mobile v4 (decided 29 September, MOB-1).** The **Waits** view of GST-038 At the Venue: **one implementation with GST-038, the ids kept** (as GAP-D3).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The wait time** (detail panel, from `getWaitTimes`): **A stale wait time is shown with a caveat, never hidden** (decided 28 September, audit R080 (b)): where `WaitTime.isStale` is true the minutes stay on screen marked out of date with their `asOf` time, as queue.yaml says.

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue)

**Where the user goes next**

- → `GST-003` Buy Tickets: *Picks something shorter from the attractions list*; calls `getWaitTimes`
- → `GST-023` Virtual Queue: *They join a virtual queue rather than stand in it*; calls `getWaitTimes`
- → `GST-001` Home: *Home – Default*
- → `GST-059` Plan in Progress: *Plan My Day – In Progress*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction wait times, read by `getWaitTimes`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction wait times untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction wait times yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Offline (`?state=offline`) | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the guest to reconnect. |

#### Permissions

- `getWaitTimes` → no permission · guest, public

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*
- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*
- Live wait time per ride/attraction shown in the app (e.g. "41 minutes"), fed by the venue's third-party camera/sensor system through a TICVAI API. *(agreed · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-204)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-022` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *At the venue → Waits*
- Flow F21 *A ride queue fills and a guest is redirected*, step 1: Guest sees the waits → With the age of each reading
- Flow F48 *A guest finds it, queues for it, and eats*, step 2: They compare waits across attractions. → **Adaptor-first** (ADR-0012) — the figure comes from whatever the venue runs, and a manually-entered wait from F67 appears here indistinguishably to the guest and distinguishably in the record.
- Flow F21 branch at step 1 (recoverable): when No feed at this attraction, **Manual entry, or nothing.** A venue with no sensors still has queues, and the platform must not require hardware to show a wait.
- Flow F21 branch at step 1 (recoverable): when The reading is stale, **Shown with a caveat, never hidden** (decided 28 September, audit R080 (b)). A stale reading comes back with `WaitTime.isStale` true and its `asOf`, and the screen shows the wait with its age and a …
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-022?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-003`, `GST-023`, `GST-001`, `GST-059`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-023` Virtual Queue

**Find the right one quickly, and act on it without opening it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 3 · needs the `queue` module |
| Block | Block A · ticket #18214 (APP-MOB-GST-023) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see. |
| Opens with | `entryId` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/general/virtual-queue-join-queue` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Virtual Queue / Join Queue*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Join queue** (modal, opened by *Join queue*; *Join queue* calls `joinQueue`, *Cancel* sends nothing)

**Collects what `joinQueue` sends before it is called.** Required: `id`, `queueId`, `partySize`, `recordedAt`. Optional: `entitlementId`, `partyHeightsCm`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `joinQueue` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `joinQueue` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `joinQueue` body |
| Entitlement `entitlementId` | text field | optional | — | — | — | Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it. | `joinQueue` body |
| Party heights cm `partyHeightsCm` | list of values (chips) | optional | — | — | — | Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited. | `joinQueue` body |
| Accessibility need declared `accessibilityNeedDeclared` | toggle | optional | off | — | — | The party declares an accessibility need (5.6.7; decided 29 September, build pass). | `joinQueue` body |
| Promotion code `promotionCode` | text field | optional | — | max length 64 | — | A promotion code the guest holds, checked against the lane's `QueueFastPass.promotionIds` (5.6.34). | `joinQueue` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `joinQueue` body |

Errors to draw in the form: 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The waiting guest** (detail panel, from `getWaitingGuest`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |
| Called at | 1 Oct 2026, 14:30 | — |
| Return window ends at | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |
| Admitted count | 1,234 | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Join queue (primary button) | `joinQueue` POST `/waiting-guests` | JoinQueueRequest | WaitingGuest | 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem) | opens modal first |
| Leave queue (secondary button) | `leaveQueue` DELETE `/waiting-guests/{entryId}` | — | — | 409 Already called or redeemed | — |

**Data it reads**: `getWaitingGuest` (onInterval, The guest's place and the call to come forward, read on …); `getWaitTimes` (onLoad, Wait times across a venue); `listQueues` (onLoad, Which virtual queues are running)

**Where the user goes next**

- → `GST-024` F&B – Browse & Order: *While waiting, they order food to where they are sitting*
- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual queue, read by `getWaitingGuest`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual queue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already called or redeemed; 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem) |

#### Permissions

- `joinQueue` → no permission · guest
- `getWaitingGuest` → no permission · guest
- `leaveQueue` → no permission · guest
- `getWaitTimes` → no permission · guest, public
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.35 | Virtual Queue Management - System shall support virtual queues. | Guest Mobile App & Branding | CONTRACTED | `joinQueue` |
| 2.13.31 | Queue Management Integration | Ticketing Sales | CONTRACTED | `joinQueue` |
| 5.6.10 | Support eligibility validation based on ticket type, membership, age, height restrictions, package entitlement, waiver status, or loyalty tier. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 5.6.30 | Expose APIs for third-party systems, kiosks, apps, CRM, and partners. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 5.6.32 | Allow self-service kiosks to support queue reservation, lookup, cancellation, and status viewing. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 19.2.36 | Queue Status Tracking - System shall provide queue status tracking. | Guest Mobile App & Branding | CONTRACTED | `getWaitingGuest` |
| 5.6.23 | Allow guests and staff to cancel reservations according to policy. | F&B & Guest Management | CONTRACTED | `leaveQueue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Virtual queue join flow with a persistent status notification (e.g. "in queue, 25 minutes"). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1090)*
- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-023` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 3 → Virtual queue; also At-venue card "Desert Coaster · queued"*. Differences: Prototype allows two queues at once; the YAML states no limit.
- Flow F48 *A guest finds it, queues for it, and eats*, step 3: They join a virtual queue rather than stand in it. → **The point of the whole feature**: the guest walks away and the place is kept. `redeemWaitingGuest` at the attraction closes it.
- Flow F48 *A guest finds it, queues for it, and eats*, step 6: Their queue place comes up and the queue screen shows it. → **The queue screen tells them, by polling its own status**, and a push reaches a guest who has the app closed. The call also lands in the in-venue notifications feed (GST-030), which is back in the …
- Flow F48 branch at step 3 (medium): when The queue is full or paused., **Told why and when it reopens.** *Unavailable* is the answer that sends a guest to a member of staff.
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-023?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Join queue, Leave queue.
- [ ] Every transition is wired: `GST-024`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-024` F&B – Browse & Order

**Order food to where the guest is sitting, or for collection.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18150 (APP-MOB-GST-024) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listDiningOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act |
| Offline | **The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making. |
| Opens with | `orderId` (deepLink), `outletId` (deepLink), `venueId` (session) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/fandb-browse-and-order` |

**What the spec says about it.** The inventory cited `GET /menu`, which never existed. Now getGuestMenu. Ordering to a cabana or a seat uses the same claimLocationSession as a table (4.6.26). States derived from the screen pattern on 17 August, not individually considered. **Cross-surface parity, 31 August**: added claimTableSession, listModifierGroups. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate. **Rev 3 (decided 29 September).** Add on an item with modifier groups opens the modifier side panel (GST-061, REV3-9); delivery fee, minimum, area and full slots are unchanged (DG-5).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Mode | segmented control | required | — | Collection · Delivery | — | Sends `?mode=` to `listFulfilmentSlots`. | `listFulfilmentSlots` ?mode |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listFulfilmentSlots`. | `listFulfilmentSlots` ?date |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `getFnbDeliveryPolicy` ?outletId |
| Open now | toggle | on | — | `listDiningOutlets` ?openNow |
| Ordering method | radio group | — | Table service · App to table · App to collect · Counter only · Not available | `listDiningOutlets` ?orderingMethod |
| At | date and time picker | — | — | `getGuestMenu` ?at |
| Language | language picker | — | — | `getGuestMenu` ?language |
| Kind | select | — | Table · Seat · Cabana · Sunbed · Poolside · Box · Suite · Lawn · Collection point · Named location | `listDeliveryLocations` ?kind |
| Serving outlet | picker: choose a serving outlet | — | — | `listDeliveryLocations` ?servingOutletId |

**Form: Claim location session** (modal, opened by *Claim location session*; *Claim location session* calls `claimLocationSession`, *Cancel* sends nothing)

**Collects what `claimLocationSession` sends before it is called.** Nothing in the body is required. Optional: `locationCode`, `seatReference`, `partySize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Location code `locationCode` | text field | optional | — | Rotates; a stale code is refused. | — | From the QR or NFC tag. Rotates; a stale code is refused. | `claimLocationSession` body |
| Seat reference `seatReference` | group | optional | — | — | — | For seated venues where the seat is the address and there is no code to scan. Validated against the performance's seat map. | `claimLocationSession` body |
| Performance `seatReference.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `claimLocationSession` body |
| Seat `seatReference.seatId` | text field | optional | — | — | — | — | `claimLocationSession` body |
| Party size `partySize` | number field | optional | — | min 1 | — | — | `claimLocationSession` body |

Errors to draw in the form: 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it.

**Form: Create guest F&B order** (modal, opened by *Create guest F&B order*; *Create guest F&B order* calls `createGuestFnbOrder`, *Cancel* sends nothing)

**Collects what `createGuestFnbOrder` sends before it is called.** Required: `id`, `lines`, `quotedTotal`, `recordedAt`. Optional: `locationSessionId`, `outletId`, `fulfilment`, `paymentMethod`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Location session `locationSessionId` | picker: choose a location session | optional | — | — | shows names, sends the id | From `claimLocationSession`. Where the order is going. | `createGuestFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | Required for collection. Ignored where a location session is supplied — the session names its outlet. | `createGuestFnbOrder` body |
| Fulfilment `fulfilment` | group | optional | — | — | — | Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`. | `createGuestFnbOrder` body |
| Mode `fulfilment.mode` | segmented control | required | — | Collection · Delivery · In venue | — | `collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). | `createGuestFnbOrder` body |
| Collection at `fulfilment.collectionAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Window start `fulfilment.windowStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Window end `fulfilment.windowEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Delivery address `fulfilment.deliveryAddress` | group | optional | — | — | — | — | `createGuestFnbOrder` body |
| Building `fulfilment.deliveryAddress.building` | text field | optional | — | max length 200 | — | — | `createGuestFnbOrder` body |
| Unit `fulfilment.deliveryAddress.unit` | text field | optional | — | max length 60 | — | — | `createGuestFnbOrder` body |
| Emirate `fulfilment.deliveryAddress.emirate` | text field | optional | — | max length 60 | — | — | `createGuestFnbOrder` body |
| Directions `fulfilment.deliveryAddress.directions` | text area | optional | — | max length 500 | — | — | `createGuestFnbOrder` body |
| Cutlery `fulfilment.cutlery` | toggle | optional | off | — | — | — | `createGuestFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createGuestFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Quantity `lines[].quantity` | stepper or slider | required | — | min 1; max 20 | — | — | `createGuestFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createGuestFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket. | `createGuestFnbOrder` body |
| Quoted total `quotedTotal` | money field | required | — | Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction. | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either … | `createGuestFnbOrder` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Wallet · Room charge · Add to tab | — | — | `createGuestFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |

Errors to draw in the form: 402 Payment required or declined; 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 422 The order breaks the outlet's `FnbDeliveryPolicy`. Names the rule in `refusedReason`.

**Form: Claim table session** (modal, opened by *Claim table session*; *Claim table session* calls `claimTableSession`, *Cancel* sends nothing)

**Collects what `claimTableSession` sends before it is called.** Required: `tableCode`. Optional: `partySize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Table code `tableCode` | text field | required | — | Rotates; a stale code is refused. | — | From the table QR. Rotates; a stale code is refused. | `claimTableSession` body |
| Party size `partySize` | number field | optional | — | min 1 | — | — | `claimTableSession` body |

Errors to draw in the form: 409 Code expired or unknown, the outlet is closed, or the table is out of service. One reason per cause.

#### Outputs: what the screen shows and produces

**Shown**

**Every browse order** (data table, from `listDiningOutlets`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Name | text | — |
| Kind | text | — |
| Zone | text | — |
| Cuisine | list or chips (count when long) | — |
| Is open now | yes / no (icon or chip) | — |
| Opens at | 1 Oct 2026, 14:30 | — |
| Closes at | 1 Oct 2026, 14:30 | — |
| Ordering method | chip: Table service, App to table, App to collect, Counter only, Not available | How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting. |
| Estimated wait minutes | 1,234 | From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented … |
| Image | the image or video | — |
| Menu | the name it points at, never the id | — |

**Every fulfilment slots** (data table, from `listFulfilmentSlots`)

| Shows | Format | Notes |
|---|---|---|
| Slots | list or chips (count when long) | — |

**Every delivery location** (data table, from `listDeliveryLocations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Table, Seat, Cabana, Sunbed, Poolside, Box… | 4.6.26. One concept, because a runner needs one instruction. |
| Label | text | What a runner is told. "Cabana 12", "Row H Seat 4", "Lawn — north gate". |
| Zone | text | — |
| Table | the name it points at, never the id | Set where the location is a restaurant table, so it shares table state. |
| Seat | text | Set where the seat is the address. References the seat map. |
| Serving outlets | list or chips (count when long) | Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an … |
| Is serviceable | yes / no (icon or chip) | False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift. |
| Unserviceable reason | text | — |
| Walk time minutes | 1,234 | From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen. |

**Every modifier group** (data table, from `listModifierGroups`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Min selections | 1,234 | Greater than zero makes the group required. |
| Max selections | 1,234 | — |
| Options | list or chips (count when long) | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected fulfilment slots** (detail panel, from `listFulfilmentSlots`)

| Shows | Format | Notes |
|---|---|---|
| Slots | list or chips (count when long) | — |

**The F&B delivery policy** (detail panel, from `getFnbDeliveryPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Collection enabled | yes / no (icon or chip) | — |
| Delivery enabled | yes / no (icon or chip) | — |
| Collection point | text | — |
| Collection hold minutes | 1,234 | — |
| Asap collection minutes | 1,234 | — |
| Asap delivery minutes | 1,234 | — |
| Slot minutes | 1,234 | — |
| Minimum order | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Delivery fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Free delivery above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Radius km | 1,234.5 | — |
| Emirates served | list or chips (count when long) | — |
| Cutlery opt in | yes / no (icon or chip) | Cutlery only when asked for, as in the design. |
| Scope path | text | The partition key (ADR-0005). Operations write it at `venue` scope. |

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**The guest menu** (detail panel, from `getGuestMenu`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Menu | the name it points at, never the id | — |
| Name | text | — |
| In force until | 1 Oct 2026, 14:30 | When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know. |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim location session (primary button) | `claimLocationSession` POST `/location-sessions` | inline | LocationSession | 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it. | opens modal first |
| Create guest F&B order (secondary button) | `createGuestFnbOrder` POST `/guest-orders` | CreateGuestOrderRequest | GuestOrderResult | 402 Payment required or declined; 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 422 The order breaks the outlet's … | emits `fnb.kitchenTicketCreated`; opens modal first |
| Claim table session (secondary button) | `claimTableSession` POST `/table-sessions` | inline | TableSession | 409 Code expired or unknown, the outlet is closed, or the table is out of service. One reason per cause. | opens modal first |

**Data it reads**: `getFnbDeliveryPolicy` (onLoad, Minimum order, delivery fee and area); `listFulfilmentSlots` (onLoad, Collection times or delivery windows still open); `listDiningOutlets` (onLoad, Outlets open now, with ordering method); `getGuestMenu` (onLoad, The menu in force at this moment); `getGuestOrderStatus` (onLoad, Track an order); `listDeliveryLocations` (onLoad, Where an order can be delivered); `listModifierGroups` (onLoad, List modifier groups)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-009` Review & Payment: *Pays*; carries `orderId`; calls `createGuestFnbOrder`
- → `GST-025` F&B – Order Tracking: *They watch the order progress*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The browse order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the browse order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No browse order yet. Offers Create guest F&B order (`createGuestFnbOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on mode, date and the browse order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getFnbDeliveryPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither a location code nor a seat reference supplied; 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it.; 409 Code expired or unknown, the outlet is … |

#### Permissions

- `getFnbDeliveryPolicy` → `PRODUCT_VIEW` (read) · staff, guest
- `listFulfilmentSlots` → no permission · guest
- `listDiningOutlets` → no permission · guest
- `getGuestMenu` → no permission · guest, staff
- `claimLocationSession` → no permission · guest
- `createGuestFnbOrder` → no permission · guest
- `getGuestOrderStatus` → no permission · guest
- `listDeliveryLocations` → no permission · guest
- `claimTableSession` → no permission · guest
- `listModifierGroups` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getFnbDeliveryPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.9 | APIs shall support menu retrieval, order creation, order status, kitchen status, inventory updates and promotions. | Developer & API Management | CONTRACTED | `getGuestMenu` |
| 19.2.50 | Location Delivery - System shall support delivery to guest location. | Guest Mobile App & Branding | CONTRACTED | `claimLocationSession` |
| 4.6.23 | Allow guests to place orders through mobile applications. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.24 | Allow guests to order by scanning QR codes. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.25 | Allow ordering directly from guest seats. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.26 | Deliver orders to tables, seats, cabanas or designated locations. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 19.2.47 | Mobile Food Ordering - System shall support mobile food ordering. | Guest Mobile App & Branding | CONTRACTED | `createGuestFnbOrder` |
| 19.2.48 | Table Ordering - System shall support table ordering. | Guest Mobile App & Branding | CONTRACTED | `claimTableSession` |
| 4.8.2 | The system should be able to send the modifier data of POS menu items to manage the stocking, reporting and re-order levels within the inventory system. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.8.3 | The system should have the ability to pass the modifier data to Kitchen printers and/or kitchen display system, in order for the kitchen to include the requests in their preparations. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.9.1 | The system should have the ability to set mandatory or optional modifiers for items. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.9.5 | the system should have a separate list of modifiers which the guest can either add or remove as per their choice and the actual order could be charged to the guest. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In-app food ordering from venue outlets is kept deliberately simple, not built out as a full e-commerce flow. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1091)*
- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Delivery basket shows the fee (AED 15, free from AED 200) and "Add AED X more for free delivery"; below AED 90 checkout is refused; outside Dubai shows "We don't deliver to this address" with Change address / Switch to takeaway. A slot can close mid-flow: "That time just filled". *(agreed · design review 29 Sep 2026, 5. Takeaway and delivery (WEB-036) · DI-1039)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Out of scope: buying F&B with no admission ticket (entering only to buy food). *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-292)*
- Guests already inside the venue order F&B in the app without visiting the counter, choosing pickup or in-park delivery to a specified location. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-291)*
- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A53** Build in-park mobile ordering flow for F&B and retail — a guest already inside the venue can order via the app and choose pickup or in-park delivery to a specified location, without visiting a counter *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-024` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → F&B – browse & order*
- Flow F11 *Guest orders food to a lounger*, step 1: Scans the QR on the lounger → The platform knows where they are. **Codes rotate**, so a photographed QR does not order to someone else's seat next week
- Flow F11 *Guest orders food to a lounger*, step 2: Browses the menu → Allergens are always present — 4.8.9
- Flow F11 *Guest orders food to a lounger*, step 3: Builds an order → Priced with any membership benefit applied
- Flow F48 *A guest finds it, queues for it, and eats*, step 4: While waiting, they order food to where they are sitting. → **`claimLocationSession` is the interesting one** — a table QR or a seat number binds the order to a place, so the food knows where to go without the guest explaining.
- Flow F11 branch at step 1 (recoverable): when QR is damaged or unreadable, Manual location entry by lounger number. Every location has a human-readable code for this reason.
- Flow F11 branch at step 1 (recoverable): when Location session expired, Re-scan. Sessions expire so that yesterday's guest cannot order to today's lounger.
- Flow F48 branch at step 4 (high): when The guest is somewhere with no delivery., `listDeliveryLocations` decides. **A venue that cannot deliver to a spot should not offer to** — the failure belongs before the order, not after the payment.

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 402, 403, 404, 409, 422).
- [ ] Every output is drawn (61 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim location session, Create guest F&B order, Claim table session.
- [ ] Every transition is wired: `GST-001`, `GST-009`, `GST-025`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 11 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-025` F&B – Order Tracking

**Track an order to the point it reaches the guest.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18151 (APP-MOB-GST-025) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** The last status stays on screen with its age and is never presented as current. Settling the bill waits for the connection. |
| Opens with | `orderId` (deepLink), `sessionId` (session) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/fandb-order-tracking` |

**What the spec says about it.** Nine states from 4.6.35. Collected and delivered are distinct from served — a counter handover, a runner delivery and a server putting a plate down are three different events. States derived from the screen pattern on 17 August, not individually considered. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-021. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**Form: Claim table session** (modal, opened by *Claim table session*; *Claim table session* calls `claimTableSession`, *Cancel* sends nothing)

**Collects what `claimTableSession` sends before it is called.** Required: `tableCode`. Optional: `partySize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Table code `tableCode` | text field | required | — | Rotates; a stale code is refused. | — | From the table QR. Rotates; a stale code is refused. | `claimTableSession` body |
| Party size `partySize` | number field | optional | — | min 1 | — | — | `claimTableSession` body |

Errors to draw in the form: 409 Code expired or unknown, the outlet is closed, or the table is out of service. One reason per cause.

#### Outputs: what the screen shows and produces

**Shown**

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**The bill** (detail panel, from `getGuestBill`)

| Shows | Format | Notes |
|---|---|---|
| Visit | text | — |
| Covers | 1,234 | — |
| Lines | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Service charge | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim table session (primary button) | `claimTableSession` POST `/table-sessions` | inline | TableSession | 409 Code expired or unknown, the outlet is closed, or the table is out of service. One reason per cause. | opens modal first |

**Data it reads**: `getGuestOrderStatus` (onInterval, The order's status (ordered, accepted, in preparation …); `getGuestBill` (onLoad, Everything ordered at this location this sitting)

**Where the user goes next**

- → `GST-030` In-Venue Notifications: *Their queue place comes up and they are told*
- → `GST-001` Home: *Home – Default*
- → `GST-023` Virtual Queue: *Their queue place comes up and the queue screen shows it*
- → `BO-021` Order Search: *Runner delivers to the lounger*; carries `orderId`; calls `getGuestOrderStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Availability is live, never cached |
| Error (`?state=error`) | Availability unavailable. **Selection is blocked** — overselling is worse than waiting |
| Empty, first run (`?state=emptyFirstRun`) | **Sold out is a real answer.** Offers the next available rather than a dead end |
| Offline (`?state=offline`) | **The offline banner shows.** The last status stays on screen with its age and is never presented as current. Settling the bill waits for the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Code expired or unknown, the outlet is closed, or the table is out of service. One reason per cause. |

#### Permissions

- `getGuestOrderStatus` → no permission · guest
- `getGuestBill` → no permission · guest
- `claimTableSession` → no permission · guest

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.48 | Table Ordering - System shall support table ordering. | Guest Mobile App & Branding | CONTRACTED | `claimTableSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A53** Build in-park mobile ordering flow for F&B and retail — a guest already inside the venue can order via the app and choose pickup or in-park delivery to a specified location, without visiting a counter *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-025` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → F&B – order tracking*. Differences: The YAML states come from an availability template ("Selection is blocked") and do not fit order tracking.
- Flow F11 *Guest orders food to a lounger*, step 6: Tracks the order → Nine states, and the guest sees the ones that matter
- Flow F48 *A guest finds it, queues for it, and eats*, step 5: They watch the order progress. → **The kitchen ticket from F29 is what moves this.** A guest watching a status that never changes is a guest walking to the counter.
- Flow F11 branch at step 6 (recoverable): when Guest loses signal mid-order, The order is already placed. Status updates resume on reconnect, and the food arrives regardless.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-025?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Claim table session.
- [ ] Every transition is wired: `GST-030`, `GST-001`, `GST-023`, `BO-021`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-027` Parking – Reserve & Pay

**Take the money, and be unambiguous about whether it worked.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 3 · needs the `access` module |
| Block | Block A · ticket #18220 (APP-MOB-GST-027) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Opens with | `entitlementId` (deepLink), `cartId` (session) · cold entry: **A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket … |
| Route | `/general/parking-reserve-and-pay` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design. **Cross-surface parity, 31 August**: added listParkingFacilities. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate. **Rebound 28 September** (decided 28 September, audit R166): parking is sold through the normal cart and checkout (`addCartLine`, `checkoutCart`, `createPayment`), so the entitlement gets its `orderId`; the guest no longer calls `createParkingEntitlement`, which the order service issues at payment. No live availability; a full car park is the `soldOutForDay` refusal. **Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listParkingFacilities`. | `listParkingFacilities` ?venueId |

**Form: Add parking to my cart** (modal, opened by *Add parking to my cart*; *Add to cart* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called.** Required: `variantId` (the car park's parking product), `quantity`. Optional: `performanceId`, `attributes` (the plate). A 409 `soldOutForDay` is shown as **the car park is full** for that day — capacity reached, not a live count (decided 28 September, audit R166). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Form: Save parking entitlement** (modal, opened by *Save parking entitlement*; *Save parking entitlement* calls `updateParkingEntitlement`, *Cancel* sends nothing)

**Collects what `updateParkingEntitlement` sends before it is called.** Nothing in the body is required. Optional: `plateNumber`, `plateCountry`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plate number `plateNumber` | text field | optional | — | — | — | Personal data, under the same rules as `ParkingEntitlement.plateNumber`. | `updateParkingEntitlement` body |
| Plate country `plateCountry` | text field | optional | — | — | — | — | `updateParkingEntitlement` body |
| Status `status` | segmented control | optional | — | Revoked | — | The only status a caller may set. Every other move is the server's. | `updateParkingEntitlement` body |

Errors to draw in the form: 400 Validation failed

**Sent by *Check out*** (`checkoutCart`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

**Sent by *Pay*** (`createPayment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `createPayment` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createPayment` body |
| Tender `tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createPayment` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPayment` body |
| Tender currency `tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `createPayment` body |
| Tender amount `tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `createPayment` body |
| Wallet authorisation `walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `createPayment` body |
| Wallet hold `walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `createPayment` body |
| Return URL `returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `createPayment` body |
| Terminal `terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `createPayment` body |
| Device `deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `createPayment` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPayment` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every parking facility** (data table, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |

**The selected parking facility** (detail panel, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add parking to my cart (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Check out (secondary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and … | emits `order.created` |
| Pay (primary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid`; works offline |
| Save parking entitlement (secondary button) | `updateParkingEntitlement` PATCH `/parking-entitlements/{entitlementId}` | UpdateParkingEntitlementRequest | ParkingEntitlement | 400 Validation failed | opens modal first |

**Data it reads**: `listParkingFacilities` (onLoad, Car parks at a venue, and how each integrates)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-028` Parking – Reservation Confirmed: *It is confirmed with a facility*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Terminal or gateway state, shown plainly |
| Error (`?state=error`) | **Declined reads differently from unresolved.** An unresolved payment inquires rather than retries, and nothing is issued until it resolves |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the parking reserve pay are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Sold out for day (`?state=soldOutForDay`) | **The car park is full.** `addCartLine` refused the parking line with `soldOutForDay`: issued entitlements have reached the facility's capacity for that day. Shown only then — there is no live space count in the first release, so the screen never promises spaces before the guest tries (decided 28 September, audit R166). |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a … |

#### Permissions

- `addCartLine` → no permission · guest, partner, staff
- `checkoutCart` → no permission · guest, partner
- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `updateParkingEntitlement` → no permission · guest
- `listParkingFacilities` → `PARKING_CONFIGURE` (configure) · staff, guest

**A refused user sees:** Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 19.2.10 | Ticket Purchase - System shall support ticket purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.23 | Membership Purchase - System shall support membership purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.24 | Membership Renewal - System shall support membership renewals. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.53 | Product Purchases - System shall support merchandise purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 1.1.98 | Membership renewals | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| 1.4.12 | System shall support dependencies between products, ensuring prerequisite products are purchased when required. | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| 2.1.10 | This system should provide a Self-service kiosk solution that enables the guests to skip the queues at POS and purchase all type of tickets defined in the system including multi-day, combo ticket … | Ticketing Sales | CONTRACTED | `checkoutCart` |
| 2.1.11 | The system should provide POS and Kiosk solution that allow the collection of tickets (free or not) booked on any portal. The kiosk should allow the collection of tickets using an identification … | Ticketing Sales | CONTRACTED | `checkoutCart` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A41** Analyse the integration effort for third-party systems (parking, ride/queue-timing sensors, etc.) to consume TAIS's own standardised API as the default integration model *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*
- **A42** Design the parking module to support both native QR-based validation (own solution) and a plate-number capture field for future ANPR/third-party parking integrations *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-027` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 3 → Parking – reserve & pay*
- Flow F50 *A guest arrives, parks, and gets in*, step 1: They add parking to their cart on the way. → **Parking is a product in the ordinary cart**, not a separate booking (decided 28 September, audit R166). **No live availability in the first release**: the line is accepted or refused against the …
- Flow F50 *A guest arrives, parks, and gets in*, step 2: They pay, and the parking entitlement is issued. → **Payment issues the parking entitlement, carrying the order id** (audit R166). It goes on the same media as the ticket, which is why a barrier and a gate read the same thing.
- Flow F50 branch at step 1 (high): when The car park is full., **`addCartLine` refuses the parking line `soldOutForDay`**: the entitlements issued for the day have reached the facility's capacity (decided 28 September, audit R166). Told before they drive, not at …
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (400, 402, 403, 409, 422).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, soldOutForDay.
- [ ] Every action is wired with its success and its failure: Add parking to my cart, Check out, Pay, Save parking entitlement.
- [ ] Every transition is wired: `GST-001`, `GST-028`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-028` Parking – Reservation Confirmed

**Confirm it worked, and give them what they need to prove it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 3 · needs the `access` module |
| Block | Block A · ticket #18221 (APP-MOB-GST-028) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Opens with | `orderId` (previousScreen) · cold entry: **Opened cold, it needs the order.** Without `orderId` it sends the guest to their orders rather than showing an empty confirmation. |
| Route | `/general/parking-reservation-confirmed` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design. **Rebound 28 September** (decided 28 September, audit R166): the guest no longer creates the parking entitlement; it is issued at payment of the cart order, and this screen reads that order (`getOrder`). **Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listParkingFacilities`. | `listParkingFacilities` ?venueId |

#### Outputs: what the screen shows and produces

**Shown**

**Every parking facility** (data table, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |

**The selected parking facility** (detail panel, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |
| Is active | yes / no (icon or chip) | — |

**The order the parking was paid on** (detail panel, from `getOrder`): **The parking entitlement is issued at payment, carrying this order's id** (decided 28 September, audit R166); this screen confirms the order and shows the car park and plate from it, and never creates the entitlement itself.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |

**Data it reads**: `getOrder` (onLoad, The paid order that carries the parking entitlement (audit …); `listParkingFacilities` (onLoad, Car parks at a venue, and how each integrates)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-012` My Tickets: *They open their tickets*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parking reservation confirmed list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parking reservation confirmed untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Paid, entitlement not yet shown.** The order is paid and the entitlement is issued at payment; until it appears the screen shows the order and says the car park pass follows (audit R166). |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the parking reservation confirmed are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `listParkingFacilities` → `PARKING_CONFIGURE` (configure) · staff, guest

**A refused user sees:** Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 3.4.1 | The payment can be done upfront or at exit. | Admission and Access | PARKED | data `ParkingFacility` |
| 7.4.12 | The system can manage Parking | F&B POS | PARKED | data `ParkingFacility` |
| 7.4.30 | For each PLU, it is possible to manage Parking tickets which can have a fixed rate per day or per hour. | F&B POS | PARKED | data `ParkingFacility` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A41** Analyse the integration effort for third-party systems (parking, ride/queue-timing sensors, etc.) to consume TAIS's own standardised API as the default integration model *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*
- **A42** Design the parking module to support both native QR-based validation (own solution) and a plate-number capture field for future ANPR/third-party parking integrations *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-028` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 3 → Parking – reservation confirmed*
- Flow F50 *A guest arrives, parks, and gets in*, step 3: It is confirmed with a facility. → **Facility, not space.** Reserving a numbered bay is a promise a venue cannot keep on a busy Saturday.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-012`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-029` Venue Info & Services

**See venue info & services for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18152 (APP-MOB-GST-029) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listDiningOutlets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. **`venueId` is the venue the guest picked on the home screen** (WEB-001 on the web, GST-001 in … |
| Route | `/general/venue-info-and-services` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Contact added 28 September** from `getTenantAppStatus.contact`, as on the web's WEB-028 (decided 28 September, audit R073 (f)).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Open now | toggle | optional | on | — | — | Sends `?openNow=` to `listDiningOutlets`. | `listDiningOutlets` ?openNow |
| Ordering method | radio group | optional | — | Table service · App to table · App to collect · Counter only · Not available | — | Sends `?orderingMethod=` to `listDiningOutlets`. | `listDiningOutlets` ?orderingMethod |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Table · Seat · Cabana · Sunbed · Poolside · Box · Suite · Lawn · Collection point · Named location | `listDeliveryLocations` ?kind |
| Serving outlet | picker: choose a serving outlet | — | — | `listDeliveryLocations` ?servingOutletId |

#### Outputs: what the screen shows and produces

**Shown**

**How to reach the venue** (detail panel, from `getTenantAppStatus`): **From `getTenantAppStatus.contact`** (decided 28 September, audit R073 (f)): phone, email, WhatsApp, address and opening hours, set from CMS-001 through `setMaintenanceMode`. Each is optional and a missing one is left out rather than shown blank.

| Shows | Format | Notes |
|---|---|---|
| Phone | +971 50 123 4567 | — |
| Email | email, tap to write | — |
| Whatsapp | text | — |
| Address | in the reader's language | — |
| Opening hours | in the reader's language | Prose, as the guest reads it. The bookable hours are the catalogue's. |

**Every dining outlet** (data table, from `listDiningOutlets`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Name | text | — |
| Kind | text | — |
| Zone | text | — |
| Cuisine | list or chips (count when long) | — |
| Is open now | yes / no (icon or chip) | — |
| Opens at | 1 Oct 2026, 14:30 | — |
| Closes at | 1 Oct 2026, 14:30 | — |
| Ordering method | chip: Table service, App to table, App to collect, Counter only, Not available | How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting. |
| Estimated wait minutes | 1,234 | From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented … |
| Image | the image or video | — |
| Menu | the name it points at, never the id | — |

**Every delivery location** (data table, from `listDeliveryLocations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Table, Seat, Cabana, Sunbed, Poolside, Box… | 4.6.26. One concept, because a runner needs one instruction. |
| Label | text | What a runner is told. "Cabana 12", "Row H Seat 4", "Lawn — north gate". |
| Zone | text | — |
| Table | the name it points at, never the id | Set where the location is a restaurant table, so it shares table state. |
| Seat | text | Set where the seat is the address. References the seat map. |
| Serving outlets | list or chips (count when long) | Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an … |
| Is serviceable | yes / no (icon or chip) | False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift. |
| Unserviceable reason | text | — |
| Walk time minutes | 1,234 | From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen. |

**The selected dining outlet** (detail panel, from `listDiningOutlets`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Name | text | — |
| Kind | text | — |
| Zone | text | — |
| Cuisine | list or chips (count when long) | — |
| Is open now | yes / no (icon or chip) | — |
| Opens at | 1 Oct 2026, 14:30 | — |
| Closes at | 1 Oct 2026, 14:30 | — |
| Ordering method | chip: Table service, App to table, App to collect, Counter only, Not available | How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting. |
| Estimated wait minutes | 1,234 | From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented … |
| Image | the image or video | — |
| Menu | the name it points at, never the id | — |

**Data it reads**: `getTenantAppStatus` (onLoad, How to reach the venue — phone, email, WhatsApp, address …); `listDiningOutlets` (onLoad, Where a guest can eat, right now); `listDeliveryLocations` (onLoad, Where an order can be delivered)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue info services list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue info services untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue info services yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on openNow, orderingMethod and the venue info services are still there. Names the active filter and offers to clear it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest
- `listDiningOutlets` → no permission · guest
- `listDeliveryLocations` → no permission · guest

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-029` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Venue info & services*. Differences: Prototype shows only dining and delivery points, no other venue services.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-038` At the Venue

**Everything live at the venue in one place: map, waits, food, shows, shop and services, with what is happening now.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 3 · needs the `queue` module |
| Block | Block A · ticket #18215 (APP-MOB-GST-038) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getTenantAppStatus` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own |
| Route | `/general/digital-companion-mode` |

**What the spec says about it.** **Mobile v4 (decided 29 September, MOB-1).** Retitled **At the Venue**, the in-venue mode and the optional Map tab: views Map, Waits, Food, Shows, Shop and Services, plus a *Happening now* panel (live orders and queues). **GST-021 Interactive Map and GST-022 Attraction Wait Times are its Map and Waits views: one implementation, three ids** (as GAP-D3). Food opens GST-024, Shop GST-026, Services GST-029, a queue GST-023. This answers CF-92: it is a real screen. (Was: *Not minuted and not in the matrix* — the only unsourced screen of the eight audited on 17 August.) **The Map view's in-park 3D navigation is ADR-0069** (client meeting 30 September, MoM 4.8): venue GLB model, pathway and location file, live GPS, built natively; 2D until a venue supplies a model.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |
| Map · Waits · Food · Shows · Shop · Services | select field | — | — | — | — | The view switcher. Map and Waits are GST-021 and GST-022 rendered in place. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Happening now** (banner, from `getWaitTimes`): Live orders, queue calls and the next show, from the guest's own orders and queues.

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The selected product** (detail panel, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The tenant app status** (detail panel, from `getTenantAppStatus`)

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Draft version | text | Staff only. |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |
| Active module count | 1,234 | Staff only. `ModuleEnablement` rows with `isEnabled` true. |
| Licensed module count | 1,234 | Staff only. `ModuleEnablement` rows with `isLicensed` true. |
| Active page count | 1,234 | Staff only. Content pages that are `published` and enabled. |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes); `getWaitTimes` (onLoad, Wait times across a venue); `listProducts` (onLoad, List products)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-021` Interactive Map: *Map view*
- → `GST-022` Attraction Wait Times: *Waits view*
- → `GST-024` F&B – Browse & Order: *Food*
- → `GST-026` Retail / Merchandise: *Shop*
- → `GST-029` Venue Info & Services: *Services*
- → `GST-023` Virtual Queue: *Join a virtual queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital companion mode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital companion mode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital companion mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the digital companion mode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Map3d unavailable (`?state=map3dUnavailable`) | **No 3D model for this map: the 2D map, same route** (ADR-0069; client meeting 30 September, MoM 4.8). The Map view of this screen is GST-021's map (one implementation): where the venue has not published a GLB model (the default until it supplies one), the phone fails the 3D capability check or rendering drops below 20 fps, the 2D map shows with the same route and the same live position dot; the 2D/3D toggle is hidden and nothing else is said. |
| Weak gps (`?state=weakGps`) | **Position approximate** (ADR-0069, section 4): reported GPS accuracy worse than 30 metres, or indoors. The Map view dims the dot and draws an approximate-position ring round the last confident position, labelled *Position approximate*; directions keep their turn list and remaining distance, and *I am at…* (a nearby location, or its QR sign) re-anchors. Waits, shows and services are unaffected. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest
- `getWaitTimes` → no permission · guest, public
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In-park 3D navigation is built natively (React Three.js) from the venue's 3D GLB model plus a metadata file of pathways and locations, combined with the guest's live GPS position; no external mapping tool. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1103)*
- In-park navigation: a live map view lets a guest navigate to a selected point (e.g. the nearest food outlet), entering a walking-navigation mode that guides the guest in real time. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1102)*
- Guests already inside the venue order F&B in the app without visiting the counter, choosing pickup or in-park delivery to a specified location. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-291)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-038` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Home → You're at Summit Peaks (At the venue · live, Map view)*. Differences: The live Map view renders the park in 3D with the route and the position dot (2D when the prototype's Maps setting is 2D). No guest-facing 2D/3D switch, and no map3dUnavailable or weakGps state: both pending in design: specified, and built from the definition until the design shows it (handoff/design-batches/apps/1-guest-app/README.md).
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, map3dUnavailable, weakGps.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-021`, `GST-022`, `GST-024`, `GST-026`, `GST-029`, `GST-023`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-070` Reserve a Table

****Book a restaurant table, or wait for one.** A guest reserves a table ahead, changes or cancels it, or joins and leaves a restaurant's waitlist. Tables only: cabanas, loungers and other spots on a venue map are booked on GST-074 (decided 29 September, rev 3 REV3-15 and GAP-C2, superseding audit R073 (c)). A deposit only where the venue enabled one (rev 3 REV3-8b, superseding audit R077 (a)).**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | In-venue Services · wave 2 · needs the `core` module |
| Block | Block A · ticket #18155 (APP-MOB-GST-070) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | form (comfortable density): A booking form (outlet, party size, time) and the restaurant waitlist, each one act; no guest-callable read of table availability exists, so `createTableReservation` is what says a time is full. … |
| Offline | **The offline banner shows.** Availability already loaded stays with its age. **Booking is not offered** — a table held offline is a table two people think they have. |
| Opens with | `entryId` (deepLink), `reservationId` (deepLink), `subjectId` (session), `cartId` (session) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/reserve-table-cabana` |

**What the spec says about it.** **Staff could book a table and a guest could not.** Seven guest-callable operations with no guest surface — reservations, cabanas, and both waitlists. **Table-only since 28 September** (decided 28 September, audit R073 (c)): the cabana wording, the `bookResource` button and `getResourceAvailability` left and the screen was renamed from *Reserve a Table or Cabana*. **R073 (c) is superseded on 29 September for resources on a venue map** (rev 3 REV3-15 and GAP-C2): guests pick a specific cabana, lounger or other spot — including non-dining tables placed on the map, sold like cabanas — on the map booking screen GST-074 and buy it. This screen stays the restaurant table reservation, the F&B flow. **Leave waitlist** is `leaveRestaurantWaitlist` (audit R073 (d)). **A table deposit is a venue option, off by default** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)): with it off, no card is needed and cancelling is free; with it on, the venue's `DepositPolicy.dining` sets the amount, the basis and the late-cancel and no-show terms. **Leaving a waitlist matters as much as joining one.** A guest who has given up and walked away still holds a place, and a queue full of people who left is a queue nobody trusts. **Rev 3 (decided 29 September).** **No basket without a deposit (REV3-8):** a table reservation and a waitlist place confirm straight after `createTableReservation` / `joinRestaurantWaitlist` with a *No card needed* confirmation; the prototype's basket line is prototype-only. **Deposit (REV3-8b):** when the venue enabled one, `createTableReservation` answers …

#### Inputs: what the user enters or picks

**Form: Create table reservation** (modal, opened by *Create table reservation*; *Create table reservation* calls `createTableReservation`, *Cancel* sends nothing)

**Collects what `createTableReservation` sends before it is called.** Required: `outletId`, `partySize`, `startsAt`. Optional: `id`, `subjectId`, `guestName`, `contactPoint`, `durationMinutes`, `tables`, `status`, `groupId`, `notes`, `actualPartySize`, `tableVisitId`. The form says **no card is needed** unless the venue enabled a dining deposit; then it shows the deposit amount and basis, when it stops being refundable and the late-cancel and no-show terms (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createTableReservation` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `createTableReservation` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `createTableReservation` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `createTableReservation` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservation` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `createTableReservation` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `createTableReservation` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservation` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `createTableReservation` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `createTableReservation` body |
| Notes `notes` | text area | optional | — | — | — | Allergies | `createTableReservation` body |

Errors to draw in the form: 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit …

**Form: Save table reservation** (modal, opened by *Save table reservation*; *Save table reservation* calls `updateTableReservation`, *Cancel* sends nothing)

**Collects what `updateTableReservation` sends before it is called.** Required: `outletId`, `partySize`, `startsAt`. Optional: `id`, `subjectId`, `guestName`, `contactPoint`, `durationMinutes`, `tables`, `status`, `groupId`, `notes`, `actualPartySize`, `tableVisitId`. Cancelling says **it is free** where no deposit was taken; where one was, whether it is returned or kept under the venue's terms (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `updateTableReservation` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `updateTableReservation` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `updateTableReservation` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `updateTableReservation` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `updateTableReservation` body |
| Notes `notes` | text area | optional | — | — | — | Allergies | `updateTableReservation` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Join restaurant waitlist** (modal, opened by *Join restaurant waitlist*; *Join restaurant waitlist* calls `joinRestaurantWaitlist`, *Cancel* sends nothing)

**Collects what `joinRestaurantWaitlist` sends before it is called.** Required: `id`, `outletId`, `partySize`, `status`, `recordedAt`. Optional: `subjectId`, `quotedWaitMinutes`, `seatingPreference`, `notifiedAt`, `syncedAt`, `holdExpiresAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Party size `partySize` | number field | required | — | — | — | — | `joinRestaurantWaitlist` body |
| Quoted wait minutes `quotedWaitMinutes` | number field (minutes) | optional | — | — | — | — | `joinRestaurantWaitlist` body |
| Seating preference `seatingPreference` | select | optional | — | Any · Indoor · Outdoor · Bar · Booth · High chair | — | — | `joinRestaurantWaitlist` body |
| Status `status` | select | required | — | Waiting · Notified · Seated · Walked away · No show · Cancelled | — | — | `joinRestaurantWaitlist` body |
| Notified at `notifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `joinRestaurantWaitlist` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the party joined, on the device. The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. | `joinRestaurantWaitlist` body |
| Hold expires at `holdExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | How long a table waits for somebody who was called. Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a … | `joinRestaurantWaitlist` body |

**Form: Join waitlist** (modal, opened by *Join waitlist*; *Join waitlist* calls `joinWaitlist`, *Cancel* sends nothing)

**Collects what `joinWaitlist` sends before it is called.** Required: `performanceId`, `partySize`. Optional: `id`, `variantId`, `subjectId`, `contactPoint`, `status`, `position`, `offeredAt`, `offerExpiresAt`, `joinedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Performance `performanceId` | picker: choose a performance | required | — | — | shows names, sends the id | — | `joinWaitlist` body |
| Variant `variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `joinWaitlist` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `joinWaitlist` body |
| Contact point `contactPoint` | text field | optional | — | — | — | Where the offer goes. An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest. | `joinWaitlist` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `joinWaitlist` body |

Errors to draw in the form: 409 The performance is not sold out (sold, held and leased units are below capacity, audit R101).

**Sent by *Leave restaurant waitlist*** (`leaveRestaurantWaitlist`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Why, where the guest or host gave a reason. Optional. | `leaveRestaurantWaitlist` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create table reservation (primary button) | `createTableReservation` POST `/table-reservations` | TableReservation | TableReservation | 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit … | opens modal first |
| Save table reservation (secondary button) | `updateTableReservation` PATCH `/table-reservations/{reservationId}` | TableReservation | TableReservation | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Join restaurant waitlist (secondary button) | `joinRestaurantWaitlist` POST `/waitlist` | RestaurantWaitlist | RestaurantWaitlist | — | works offline; opens modal first |
| Leave restaurant waitlist (destructive button) | `leaveRestaurantWaitlist` POST `/waitlist/{entryId}/leave` | inline | RestaurantWaitlist | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. | — |
| Join waitlist (secondary button) | `joinWaitlist` POST `/waitlist-entries` | WaitlistEntry | WaitlistEntry | 409 The performance is not sold out (sold, held and leased units are below capacity, audit R101). | opens modal first |
| Leave waitlist (secondary button) | `leaveWaitlist` DELETE `/waitlist-entries/{entryId}` | — | — | — | — |

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`
- → `GST-041` Checkout Entry: *Pay the deposit (only when the venue requires one)*; carries `cartId`; only when the reservation is awaitingDeposit; calls `addCartLine`

**What opens over it**

- confirmDialog *Leave restaurant waitlist*: **Says the place is given up and the next party moves up**, naming the restaurant and the party size. Leaving cannot be undone; joining again goes to the back (audit R073 (d)).

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing reserved.** The booking form is the screen: pick the restaurant, party size and time, and `createTableReservation` says if that time is full. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025). A guest who is not signed in is offered sign-in and brought back here. |
| Offline (`?state=offline`) | **The offline banner shows.** Availability already loaded stays with its age. **Booking is not offered** — a table held offline is a table two people think they have. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit …; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status.; 409 The performance is not sold out (sold, held … |

#### Permissions

- `createTableReservation` → no permission · guest
- `updateTableReservation` → no permission · guest
- `joinRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `leaveRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `joinWaitlist` → no permission · guest
- `leaveWaitlist` → no permission · guest
- `addCartLine` → no permission · guest, partner, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025). A guest who is not signed in is offered sign-in and brought back here.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.10 | The system should be able to create,modify and delete new/existing reservations | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 4.9.13 | The system should be able to allow table reservations in advance according to the requirements. | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 7.5.1 | Event scheduled services such as table booking or meal delivery can be managed by the system (sales only) | F&B POS | CONTRACTED | `createTableReservation` |
| 13.3.11 | APIs shall support reservation creation, modification, cancellation, waitlists and availability checks. | Developer & API Management | CONTRACTED | `createTableReservation` |
| 1.1.25 | System shall allow guests to join waitlists when capacity is fully booked and automatically notify guests when availability becomes available. | Ticketing Catalogue | CONTRACTED | `joinWaitlist` |
| 1.3.16 | System should provide ability to sell tickets for an event on a waitinglist in case if the capacity is not available. System should automatically allot the capacity in case of any cancellations | Ticketing Catalogue | CONTRACTED | `joinWaitlist` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 4.9.11 | The system should be able to create,modify, delete a new/old guest to the wait list | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.14 | Allow guests to make reservations via website, mobile app, kiosk, QR code, call center, and third-party reservation channels with real-time availability. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Dining deposit hold is a venue option, off unless enabled in Venue Management; amount and basis (per guest, per table, percentage) are venue configuration, never a hard-coded AED 100. Show the deposit step only when enabled. *(agreed · rev 3 design review 29 Sep 2026, REV3-8b · 8. deposit hold flow · DI-1049)*
- Table reservations and the waitlist do not go into the cart: after date, time and party size the guest gets a confirmation straight away ("no card needed"). *(agreed · rev 3 design review 29 Sep 2026, REV3-8 · 8. Unable to complete the table booking flow · DI-1048)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Cookie banner*, set in `CMS-026` Cookie Banner & Preference Center Designer:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Position (`cookieBanner.position`) | Top · Bottom · Popup · Modal | — | — |

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-070` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Reserve a table or cabana; Rev 3 feedback → Book a table (fixed)*. Differences: The YAML covers tables only (cabanas are staff-booked, R073c) and has no deposit (R077a). The prototype also reserves cabanas and shows a deposit on the reservation, and the Rev 3 web flow has a deposit-hold variant at AED 100 per guest.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (403, 404, 409, 412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create table reservation, Save table reservation, Join restaurant waitlist, Leave restaurant waitlist, Join waitlist, Leave waitlist.
- [ ] Every transition is wired: `GST-039`, `GST-041`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | body text on the background |
| Dark mode (`theme.darkMode`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `CMS-003`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-007` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-007` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-007` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-007` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-007` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-007` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-007` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-007` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-007` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Never configurable:** The *Powered by TICVAI* credit in the footer is fixed and never client-editable (MoM 3 Aug, DI-111; MoM 12 Aug, DI-250). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**40 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"checkoutCart": {"method":"POST","path":"/carts/{cartId}/checkout","contract":"orders","summary":"Turn the cart into an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"claimLocationSession": {"method":"POST","path":"/location-sessions","contract":"fnb","summary":"Tell the platform where the guest is","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LocationSession"},
"claimTableSession": {"method":"POST","path":"/table-sessions","contract":"fnb","summary":"Identify which table a guest is sitting at","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableSession"},
"createGuestFnbOrder": {"method":"POST","path":"/guest-orders","contract":"fnb","summary":"A guest orders food","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGuestOrderRequest","responds":"GuestOrderResult"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"createTableReservation": {"method":"POST","path":"/table-reservations","contract":"fnb","summary":"Book a table in advance","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"},
"getFnbDeliveryPolicy": {"method":"GET","path":"/fnb-delivery-policy","contract":"fnb","summary":"How an outlet does takeaway and delivery","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":true}],"requestBody":null,"responds":"FnbDeliveryPolicy"},
"getGuestBill": {"method":"GET","path":"/table-sessions/{sessionId}/bill","contract":"fnb","summary":"The bill for the guest's table","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bill"},
"getGuestMenu": {"method":"GET","path":"/outlets/{outletId}/guest-menu","contract":"fnb","summary":"The menu a guest sees","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"GuestMenu"},
"getGuestOrderStatus": {"method":"GET","path":"/guest-orders/{orderId}","contract":"fnb","summary":"Track an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestOrderStatus"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getVenueMapGraph": {"method":"GET","path":"/venue-maps/{mapId}/graph","contract":"venue-map","summary":"The navigation graph, ready to route over","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"draft","in":"query","required":null},{"name":"stepFreeOnly","in":"query","required":null}],"requestBody":null,"responds":"VenueMapGraph"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"getWaitingGuest": {"method":"GET","path":"/waiting-guests/{entryId}","contract":"queue","summary":"Read a queue entry","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WaitingGuest"},
"joinQueue": {"method":"POST","path":"/waiting-guests","contract":"queue","summary":"Join a virtual queue","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"JoinQueueRequest","responds":"WaitingGuest"},
"joinRestaurantWaitlist": {"method":"POST","path":"/waitlist","contract":"fnb","summary":"Add a party to an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RestaurantWaitlist","responds":"RestaurantWaitlist"},
"joinWaitlist": {"method":"POST","path":"/waitlist-entries","contract":"catalogue","summary":"Ask to be told if capacity frees up","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WaitlistEntry","responds":"WaitlistEntry"},
"leaveQueue": {"method":"DELETE","path":"/waiting-guests/{entryId}","contract":"queue","summary":"Leave a queue","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"leaveRestaurantWaitlist": {"method":"POST","path":"/waitlist/{entryId}/leave","contract":"fnb","summary":"Take a party off an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"leaveWaitlist": {"method":"DELETE","path":"/waitlist-entries/{entryId}","contract":"catalogue","summary":"Stop waiting","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listDeliveryLocations": {"method":"GET","path":"/venues/{venueId}/delivery-locations","contract":"fnb","summary":"Where an order can be delivered","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"servingOutletId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDiningOutlets": {"method":"GET","path":"/venues/{venueId}/dining","contract":"fnb","summary":"Where a guest can eat, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"openNow","in":"query","required":null},{"name":"orderingMethod","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFulfilmentSlots": {"method":"GET","path":"/outlets/{outletId}/fulfilment-slots","contract":"fnb","summary":"Collection times or delivery windows still open","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"path","required":true},{"name":"mode","in":"query","required":true},{"name":"date","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listModifierGroups": {"method":"GET","path":"/modifier-groups","contract":"fnb","summary":"List modifier groups","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParkingFacilities": {"method":"GET","path":"/parking-facilities","contract":"access","summary":"Car parks at a venue, and how each integrates","permission":"PARKING_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updateParkingEntitlement": {"method":"PATCH","path":"/parking-entitlements/{entitlementId}","contract":"access","summary":"Change the plate, or revoke","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpdateParkingEntitlementRequest","responds":"ParkingEntitlement"},
"updateTableReservation": {"method":"PATCH","path":"/table-reservations/{reservationId}","contract":"fnb","summary":"Change or cancel a booking","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"Bill": {"x-ticvai-persistence":"none — computed from visit orders","type":"object","required":["visitId","lines","subtotal","taxAmount","total"],"properties":{"visitId":{"type":"string"},"covers":{"type":"integer"},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","lineTotal"],"properties":{"lineId":{"type":"string"},"orderId":{"type":"string"},"name":{"type":"string"},"quantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryCode":{"type":"string","nullable":true},"seatNumber":{"type":"integer","nullable":true}}}},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serviceCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateGuestOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1,"maximum":20},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"}}},
"CreateGuestOrderRequest": {"type":"object","required":["id","lines","quotedTotal","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationSessionId":{"type":"string","format":"uuid","nullable":true,"description":"From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Required for collection. Ignored where a location session is supplied — the session names its outlet."},"fulfilment":{"allOf":[{"$ref":"#/components/schemas/GuestOrderFulfilment"}],"nullable":true,"description":"Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateGuestOrderLine"}},"quotedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"},"paymentMethod":{"type":"string","enum":["card","wallet","roomCharge","addToTab"]},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"DeliveryLocation": {"type":"object","x-ticvai-persistence":"fnb.delivery_location","required":["id","venueId","kind","label","isServiceable"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string","description":"What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."},"zone":{"type":"string","nullable":true},"tableId":{"type":"string","format":"uuid","nullable":true,"description":"Set where the location is a restaurant table, so it shares table state."},"seatId":{"type":"string","nullable":true,"description":"Set where the seat is the address. References the seat map."},"servingOutletIds":{"type":"array","description":"Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n","items":{"type":"string","format":"uuid"}},"isServiceable":{"type":"boolean","description":"False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"},"unserviceableReason":{"type":"string","nullable":true},"walkTimeMinutes":{"type":"integer","nullable":true,"description":"From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"DiningOutlet": {"type":"object","x-ticvai-persistence":"none — projection over outlet, menu and table state","required":["outletId","name","kind","isOpenNow","orderingMethod"],"properties":{"outletId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"},"zone":{"type":"string","nullable":true},"cuisine":{"type":"array","items":{"type":"string"}},"isOpenNow":{"type":"boolean"},"opensAt":{"type":"string","format":"date-time","nullable":true},"closesAt":{"type":"string","format":"date-time","nullable":true},"orderingMethod":{"$ref":"#/components/schemas/GuestOrderingMethod"},"estimatedWaitMinutes":{"type":"integer","nullable":true,"description":"From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented wait time is worse than none.\n"},"imageAssetRef":{"type":"string","nullable":true},"menuId":{"type":"string","format":"uuid","nullable":true}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FnbDeliveryPolicy": {"type":"object","x-ticvai-persistence":"fnb.delivery_policy","required":["outletId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"collectionEnabled":{"type":"boolean","default":true},"deliveryEnabled":{"type":"boolean","default":false},"collectionPoint":{"type":"string","maxLength":200,"nullable":true},"collectionHoldMinutes":{"type":"integer","default":20},"asapCollectionMinutes":{"type":"integer","default":25},"asapDeliveryMinutes":{"type":"integer","default":45},"slotMinutes":{"type":"integer","default":30},"minimumOrder":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"freeDeliveryAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"radiusKm":{"type":"number","minimum":0,"nullable":true},"emiratesServed":{"type":"array","items":{"type":"string"}},"cutleryOptIn":{"type":"boolean","default":true,"description":"Cutlery only when asked for, as in the design."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"FnbReservationTable": {"type":"object","x-ticvai-persistence":"fnb.reservation_table","description":"**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.","required":["reservationId","tableId","createdAt"],"properties":{"reservationId":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"FulfilmentSlots": {"type":"object","x-ticvai-persistence":"none — computed per request","properties":{"slots":{"type":"array","items":{"type":"object","properties":{"start":{"type":"string","format":"date-time"},"end":{"type":"string","format":"date-time","nullable":true},"isAsap":{"type":"boolean"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestMenu": {"type":"object","x-ticvai-persistence":"none — projection over menu, item and availability","required":["outletId","menuId","name","inForceUntil","sections"],"properties":{"outletId":{"type":"string","format":"uuid"},"menuId":{"type":"string","format":"uuid"},"name":{"type":"string"},"inForceUntil":{"type":"string","format":"date-time","nullable":true,"description":"When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"sections":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","items":{"type":"object","required":["menuItemId","name","price","isAvailable","allergens"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"},"unavailableReason":{"type":"string","nullable":true},"allergens":{"type":"array","description":"Always present. Not a field a tenant may choose to omit.","items":{"$ref":"#/components/schemas/AllergenCode"}},"preparationMinutes":{"type":"integer","nullable":true},"modifierGroups":{"type":"array","items":{"$ref":"#/components/schemas/ModifierGroup"}}}}}}}}}},
"GuestOrderFulfilment": {"type":"object","x-ticvai-persistence":"fnb.order_fulfilment","description":"How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.","required":["mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-column":"service_order_id","description":"The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."},"mode":{"type":"string","enum":["collection","delivery","inVenue"],"description":"`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."},"collectionAt":{"type":"string","format":"date-time","nullable":true},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true},"deliveryAddress":{"type":"object","nullable":true,"properties":{"building":{"type":"string","maxLength":200},"unit":{"type":"string","maxLength":60,"nullable":true},"emirate":{"type":"string","maxLength":60},"directions":{"type":"string","maxLength":500,"nullable":true}}},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true},"cutlery":{"type":"boolean","default":false},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestOrderResult": {"type":"object","x-ticvai-persistence":"none — projection over fnb_order","required":["orderId","orderNumber","status","total"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string","description":"Short and readable. It gets called out across a counter."},"fulfilment":{"type":"string","enum":["collect","deliverToLocation","tableService","deliverToAddress"],"description":"How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"collectionPoint":{"type":"string","nullable":true},"tableLabel":{"type":"string","nullable":true}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"GuestOrderingMethod": {"x-ticvai-persistence":"none — enum","type":"string","description":"How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting.\n","enum":["tableService","appToTable","appToCollect","counterOnly","notAvailable"]},
"JoinQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","queueId","partySize","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"queueId":{"type":"string","format":"uuid"},"partySize":{"type":"integer","minimum":1},"entitlementId":{"type":"string","nullable":true,"description":"Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it.\n"},"partyHeightsCm":{"type":"array","description":"Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited.\n","items":{"type":"integer"}},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"The party declares an accessibility need (5.6.7; decided 29 September, build pass). Grants priority only on a lane whose `QueueFastPass.accessibilityPriority` is on, and is recorded on the entry either way.\n"},"promotionCode":{"type":"string","maxLength":64,"nullable":true,"description":"A promotion code the guest holds, checked against the lane's `QueueFastPass.promotionIds` (5.6.34). A code for a promotion the lane does not list grants nothing and is not an error.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocationSession": {"type":"object","x-ticvai-persistence":"fnb.location_session","required":["id","locationId","kind","label","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"},"visitId":{"type":"string","format":"uuid","nullable":true,"description":"The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"},"joinedExistingVisit":{"type":"boolean"},"subjectId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","description":"Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"}}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParkingEntitlement": {"type":"object","x-ticvai-persistence":"access.parking_entitlement","description":"**Issued at payment of an order that contains a parking product** (decided 28 September, audit R166). Parking is sold through the normal cart and checkout (`orders.addCartLine`, `orders.checkoutCart`), so every entitlement carries that order's `orderId`. The guest pays for the parking right with their order; the facility's own system is never paid through the app (`ParkingFacility.takesPayment`). **No live availability in the first release**: the sale is refused as full only when the facility's issued entitlements reach its `capacity`.\n","required":["facilityId","orderId","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"facilityId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"subjectId":{"type":"string","format":"uuid","nullable":true},"plateNumber":{"type":"string","nullable":true,"description":"Required in `plateWhitelist` mode, meaningless in the others. **Personal data** — a plate identifies a person, so it lives under the same rules as a contact point.\n"},"plateCountry":{"type":"string","nullable":true},"mediaCode":{"type":"string","nullable":true,"description":"The code presented in `none` and `qrHandoff` modes."},"status":{"allOf":[{"$ref":"#/components/schemas/ParkingEntitlementStatus"}],"readOnly":true,"description":"Server-owned. Moves as `states/parking-entitlement.yaml` says; a create body does not send it."},"pushedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"pushFailureReason":{"type":"string","nullable":true,"readOnly":true},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"}}},
"ParkingEntitlementStatus": {"type":"string","enum":["pending","pushed","pushFailed","active","used","expired","revoked"]},
"ParkingFacility": {"type":"object","x-ticvai-persistence":"access.parking_facility","required":["name","venueId","mode"],"properties":{"id":{"type":"string","format":"uuid","description":"**Server-assigned, and the upsert key of `setParkingFacility`.** Absent in a body, it creates; present, it names the facility being replaced. A client never mints one.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"mode":{"$ref":"#/components/schemas/ParkingIntegrationMode"},"capacity":{"type":"integer","nullable":true,"description":"**What \"full\" means in the first release** (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. Null means no limit is enforced.\n"},"takesPayment":{"type":"boolean","readOnly":true,"default":false,"description":"**Always false, and stated rather than assumed** (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client decided on 14 August that it does not.\nAll three integration models are entitlement-based — the ticket carries the parking right and the platform pushes a plate or a code. **Pay-per-hour parking unrelated to a ticket runs on the parking system's own POS**, because taking that money here would make the venue an acquirer for parking, with a settlement path and a tax treatment nobody has designed.\nThe field exists so that a future reversal is a value change with a visible blast radius, rather than a silent gap somebody rediscovers.\n"},"vendorSwapTargetDays":{"type":"integer","readOnly":true,"default":5,"description":"**A new parking vendor should take days, not weeks** — Qossai, 14 August. The team has integrated parking APIs before and the architecture is expected to make the next one cheap.\nRecorded as a design constraint rather than a runtime value: **everything vendor-specific lives in `vendorName`, `endpoint` and `credentialRef`**, and the three modes are the adaptor surface (ADR-0012). A vendor needing a fourth mode is the signal this has been violated.\n"},"vendorName":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"endpoint":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"credentialRef":{"type":"string","nullable":true,"description":"A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response."},"pushLeadMinutes":{"type":"integer","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"},"accessPointIds":{"type":"array","description":"Where the platform validates its own code, in `none` and `qrHandoff` modes.","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"}}},
"ParkingIntegrationMode": {"type":"string","description":"CF-52, settled 14 August. **Not variations of one thing** — each decides what happens at sale and what a guest presents at the barrier.\n","enum":["none","plateWhitelist","qrHandoff"]},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueEntryStatus": {"type":"string","enum":["waiting","called","redeemed","expired","noShow","cancelled","released"]},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"RestaurantWaitlist": {"type":"object","x-ticvai-persistence":"fnb.waitlist_entry","description":"BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n","required":["id","outletId","partySize","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partySize":{"type":"integer"},"quotedWaitMinutes":{"type":"integer","nullable":true},"seatingPreference":{"type":"string","enum":["any","indoor","outdoor","bar","booth","highChair"],"nullable":true},"status":{"type":"string","enum":["waiting","notified","seated","walkedAway","noShow","cancelled"]},"notifiedAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time","description":"**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"}}},
"TableReservation": {"type":"object","x-ticvai-persistence":"fnb.table_reservation","x-ticvai-retired-columns":["table_ids"],"required":["outletId","startsAt","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string"},"contactPoint":{"type":"string"},"partySize":{"type":"integer","minimum":1},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer","description":"**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"},"tables":{"type":"array","description":"The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n","items":{"$ref":"#/components/schemas/FnbReservationTable"}},"status":{"$ref":"#/components/schemas/TableReservationStatus"},"groupId":{"type":"string","format":"uuid","nullable":true,"description":"5.1.2. Several bookings managed as one party across adjacent tables."},"notes":{"type":"string","description":"Allergies","occasion":null,"accessibility.":null},"actualPartySize":{"type":"integer","nullable":true,"readOnly":true},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"deposit":{"$ref":"#/components/schemas/TableReservationDeposit"},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"TableReservationDeposit": {"type":"object","nullable":true,"readOnly":true,"x-ticvai-persistence":"fnb.table_reservation","description":"**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n","required":["amount","basis"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"]},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."},"variantId":{"type":"string","format":"uuid","description":"The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.CartLine` carrying the deposit, once added."},"depositId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.deposit` row, once the payment is authorised."}}},
"TableReservationStatus": {"type":"string","description":"`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.","enum":["awaitingDeposit","booked","confirmed","seated","completed","cancelled","noShow"]},
"TableSession": {"type":"object","x-ticvai-persistence":"fnb.table_session","required":["id","outletId","tableId","tableLabel","visitId","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"outletName":{"type":"string"},"tableId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string"},"visitId":{"type":"string","format":"uuid","description":"The table visit this session orders onto. An existing open visit is joined rather than duplicated — a guest seated by a server and then ordering by app is one party, one bill.\n"},"joinedExistingVisit":{"type":"boolean"},"subjectId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","description":"Sessions expire so a guest who leaves cannot order to a table now occupied by someone else.\n"}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"UpdateParkingEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only; applied to access.parking_entitlement","description":"**The body of `updateParkingEntitlement`: only what changes.** A partial update, so a field left out keeps its stored value. Two changes are possible, one per call:\n- **A plate change** — `plateNumber`, and `plateCountry` where it differs. The new plate is re-pushed and the old one leaves the whitelist. Resending the current plate is how a failed push is retried.\n- **A revoke** — `status: revoked`. The plate leaves the whitelist and the entitlement is terminal.\nA body carrying both, or neither, is a `400`. Which states allow each change is `states/parking-entitlement.yaml`'s to say.\n","minProperties":1,"properties":{"plateNumber":{"type":"string","description":"Personal data, under the same rules as `ParkingEntitlement.plateNumber`."},"plateCountry":{"type":"string","nullable":true},"status":{"type":"string","enum":["revoked"],"description":"The only status a caller may set. Every other move is the server's."}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}}}},
"VenueMapGraph": {"type":"object","description":"19.2.56. **What a client needs to route, and nothing more.** Small enough to cache, versioned so a stale route is detectable.\n","required":["mapId","version","nodes","edges"],"properties":{"mapId":{"type":"string","format":"uuid"},"version":{"type":"integer","description":"**Bumped by a publish or a closure**, and stored as `VenueMap.graphVersion`. A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"},"generatedAt":{"type":"string","format":"date-time"},"nodes":{"type":"array","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"x":{"type":"number"},"y":{"type":"number"},"kind":{"type":"string"},"isStepFree":{"type":"boolean"}}}},"edges":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"uuid"},"to":{"type":"string","format":"uuid"},"distanceMetres":{"type":"number"},"isStepFree":{"type":"boolean"},"throughPointId":{"type":"string","nullable":true,"description":"Where an access point restricts this edge. **The direction lives on that point**, not here, so a gate reconfigured to bidirectional changes routing without a map edit.\n"},"isClosed":{"type":"boolean"}}}},"components":{"type":"integer","description":"How many disconnected parts. **One is the answer for a park.** More than one on a map that should be a single site means something is unreachable and the client can say so without walking the graph.\n"}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WaitingGuest": {"x-ticvai-persistence":"queue.entry","type":"object","required":["id","queueId","partyNumber","partySize","status","joinedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"},"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partyNumber":{"type":"integer","description":"What the guest sees and what appears on signage."},"partySize":{"type":"integer"},"status":{"$ref":"#/components/schemas/QueueEntryStatus"},"positionInQueue":{"type":"integer","nullable":true},"partiesAhead":{"type":"integer","nullable":true},"estimatedCallAt":{"type":"string","format":"date-time","nullable":true},"isFastPass":{"type":"boolean"},"priorityBasis":{"type":"string","enum":["none","entitlement","loyaltyTier","promotion","accessibility"],"default":"none","description":"Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"},"priorityTierId":{"type":"string","format":"uuid","nullable":true,"description":"The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."},"priorityPromotionId":{"type":"string","format":"uuid","nullable":true,"description":"The promotion that granted priority, where `priorityBasis` is `promotion`."},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"What the party declared at join, shown to the operator at the front."},"entitlementId":{"type":"string","nullable":true},"calledAt":{"type":"string","format":"date-time","nullable":true},"returnWindowEndsAt":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"admittedCount":{"type":"integer","nullable":true},"joinedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WaitlistEntry": {"type":"object","x-ticvai-persistence":"catalogue.waitlist_entry","required":["performanceId","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"performanceId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"contactPoint":{"type":"string","description":"**Where the offer goes.** An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest.\n"},"partySize":{"type":"integer","minimum":1},"status":{"allOf":[{"$ref":"#/components/schemas/WaitlistStatus"}],"readOnly":true,"description":"Set by the server. `joinWaitlist` does not take it; a new entry is `waiting`."},"position":{"type":"integer","readOnly":true,"description":"First in, first offered. Shown to the guest, because not knowing is worse than waiting."},"offeredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"offerExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**The offer moves on when this passes.** Notifying everyone at once produces a race the fastest guest wins; holding indefinitely for someone asleep leaves the seat unsold.\n"},"joinedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaitlistStatus": {"type":"string","enum":["waiting","offered","converted","expired","left"]}
}
```
